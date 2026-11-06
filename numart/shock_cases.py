"""Planar inviscid shock benchmarks, first-order finite volumes + SSPRK2.

NASA 15-degree wedges on an independent body-fitted mesh; classical Mach-3
forward step on grid-aligned blocked cells. No viscosity or turbulence model.
"""
from dataclasses import dataclass
import numpy as np
from .euler2d import GAMMA, conserved, primitive, hll_flux
from .snapshots import SnapshotRecorder


def oblique_shock(mach=2.5, angle=15.):
    """Attached weak theta-beta-Mach solution; rho1=1, p1=1/gamma, a1=1."""
    if not np.isfinite(mach) or mach <= 1 or not np.isfinite(angle) or not 0 < angle < 45:
        raise ValueError('Require supersonic Mach number and 0 < angle < 45 degrees')
    theta = np.deg2rad(angle)
    def residual(beta):
        return (2/np.tan(beta)*(mach**2*np.sin(beta)**2-1)
                /(mach**2*(GAMMA+np.cos(2*beta))+2)-np.tan(theta))
    samples = np.linspace(np.arcsin(1/mach)+1e-10, np.pi/2-1e-10, 2049)
    brackets = np.flatnonzero(residual(samples[:-1])*residual(samples[1:]) < 0)
    if not len(brackets):
        raise ValueError('No attached oblique shock for these controls')
    lo, hi = samples[brackets[0]:brackets[0]+2]
    for _ in range(60):
        mid = (lo+hi)/2
        if residual(mid) > 0: hi = mid
        else: lo = mid
    beta = (lo+hi)/2
    mn2 = (mach*np.sin(beta))**2
    pressure_ratio = 1+2*GAMMA/(GAMMA+1)*(mn2-1)
    density_ratio = (GAMMA+1)*mn2/(2+(GAMMA-1)*mn2)
    downstream_mach = np.sqrt((1+.5*(GAMMA-1)*mn2)/(GAMMA*mn2-.5*(GAMMA-1)))/np.sin(beta-theta)
    speed = downstream_mach*np.sqrt(pressure_ratio/density_ratio)
    return dict(beta=float(beta), angle=angle, mach=mach,
                pressure_ratio=float(pressure_ratio), density_ratio=float(density_ratio),
                downstream_mach=float(downstream_mach),
                upstream=conserved([1., mach, 0., 1/GAMMA]),
                downstream=conserved([density_ratio, speed*np.cos(theta), speed*np.sin(theta), pressure_ratio/GAMMA]))


def normal_flux(left, right, nx, ny):
    """Rotate into a unit face normal, apply Cartesian HLL, then rotate back."""
    nx, ny = np.asarray(nx), np.asarray(ny)
    def rotate(q):
        r = q.copy()
        r[..., 1] = nx*q[..., 1]+ny*q[..., 2]
        r[..., 2] = -ny*q[..., 1]+nx*q[..., 2]
        return r
    f = hll_flux(rotate(left), rotate(right), 0)
    result = f.copy()
    result[..., 1] = nx*f[..., 1]-ny*f[..., 2]
    result[..., 2] = ny*f[..., 1]+nx*f[..., 2]
    return result


def reflected(q, nx, ny):
    r = q.copy()
    momentum = nx*q[..., 1]+ny*q[..., 2]
    r[..., 1] -= 2*momentum*nx
    r[..., 2] -= 2*momentum*ny
    return r


@dataclass
class ShockResult:
    x_nodes: np.ndarray
    y_nodes: np.ndarray
    q: np.ndarray
    time: float
    steps: int
    fluid: np.ndarray
    volumes: np.ndarray
    history: np.ndarray
    snapshots: object = None


def wedge_mesh(ny=40, angle=15.):
    if not isinstance(ny, int) or ny < 8 or ny % 2:
        raise ValueError('Require an even ny >= 8')
    nx = 3*ny
    x = np.linspace(-.5, 1., nx+1)
    bottom = np.maximum(x, 0)*np.tan(np.deg2rad(angle))
    eta = np.linspace(0, 1, ny+1)
    xx = np.broadcast_to(x[:, None], (nx+1, ny+1)).copy()
    # Keep the farfield above the Mach-2 weak shock at the outlet (y ~ 1.012).
    yy = bottom[:, None]+(1.2-bottom[:, None])*eta
    dx = np.diff(x)[:, None]
    horizontal_dy = np.diff(yy, axis=0)
    lengths = np.hypot(dx, horizontal_dy)
    normals = (-horizontal_dy/lengths, np.broadcast_to(dx, lengths.shape)/lengths)
    vertical_lengths = np.diff(yy, axis=1)
    volumes = dx*.5*(vertical_lengths[:-1]+vertical_lengths[1:])
    return xx, yy, volumes, vertical_lengths, lengths, normals


def wedge_rhs(q, upstream, vertical_lengths, lengths, normals, volumes):
    nx, ny = normals
    g = np.pad(q, ((1, 1), (1, 1), (0, 0)), mode='edge')
    g[0, 1:-1] = upstream
    g[1:-1, -1] = upstream
    g[1:-1, 0] = reflected(q[:, 0], nx[:, 0], ny[:, 0])
    fx = hll_flux(g[:-1, 1:-1], g[1:, 1:-1], 0)*vertical_lengths[..., None]
    fy = normal_flux(g[1:-1, :-1], g[1:-1, 1:], nx, ny)*lengths[..., None]
    return (-(fx[1:]-fx[:-1])-(fy[:, 1:]-fy[:, :-1]))/volumes[..., None]


def solve_wedge(ny=40, mach=2.5, angle=15., final_time=2., cfl=.4):
    if not np.isfinite(final_time) or final_time < 0 or not 0 < cfl <= .4:
        raise ValueError('Require finite nonnegative time and 0 < CFL <= .4')
    reference = oblique_shock(mach, angle)
    x, y, volumes, vertical, lengths, normals = wedge_mesh(ny, angle)
    q = np.broadcast_to(reference['upstream'], (*volumes.shape, 4)).copy()
    time = 0.; steps = 0; history = []
    dx = np.diff(x[:, 0])[:, None]
    horizontal_dy = np.maximum(abs(np.diff(y, axis=0)[:, :-1]), abs(np.diff(y, axis=0)[:, 1:]))
    vertical_average = .5*(vertical[:-1]+vertical[1:])
    while time < final_time:
        w = primitive(q); sound = np.sqrt(GAMMA*w[..., 3]/w[..., 0])
        sx = np.max(abs(w[..., 1])+sound); sy = np.max(abs(w[..., 2])+sound)
        dt = min(final_time-time, cfl*np.min(volumes/(sx*(vertical_average+horizontal_dy)+sy*dx)))
        rhs = lambda state: wedge_rhs(state, reference['upstream'], vertical, lengths, normals, volumes)
        before = q
        first = q+dt*rhs(q)
        q = .5*q+.5*(first+dt*rhs(first))
        primitive(q); time += dt; steps += 1
        if steps % 50 == 0 or time == final_time:
            history.append((time, np.max(abs(q-before))/dt))
    return ShockResult(x, y, q, time, steps, np.ones(volumes.shape, dtype=bool), volumes, np.array(history))


def shock_cell_fractions(x, y, beta):
    """Exact polygon clipping fractions below y=tan(beta)*x in each quad."""
    slope = np.tan(beta)
    fractions = np.zeros((x.shape[0]-1, x.shape[1]-1))
    def area(poly):
        return .5*abs(sum(a[0]*b[1]-b[0]*a[1] for a, b in zip(poly, poly[1:]+poly[:1])))
    for i, j in np.ndindex(fractions.shape):
        vertices = [(x[a,b], y[a,b]) for a,b in ((i,j),(i+1,j),(i+1,j+1),(i,j+1))]
        clipped = []
        for a,b in zip(vertices, vertices[1:]+vertices[:1]):
            fa, fb = a[1]-slope*a[0], b[1]-slope*b[0]
            if fa <= 0: clipped.append(a)
            if (fa < 0 < fb) or (fb < 0 < fa):
                t = fa/(fa-fb)
                clipped.append((a[0]+t*(b[0]-a[0]), a[1]+t*(b[1]-a[1])))
        fractions[i,j] = area(clipped)/area(vertices) if len(clipped) >= 3 else 0.
    return np.clip(fractions, 0, 1)


def step_geometry(ny=40):
    if not isinstance(ny, int) or ny < 10 or ny % 5:
        raise ValueError('Require ny >= 10 divisible by 5 to align the step exactly')
    x = np.linspace(0, 3, 3*ny+1); y = np.linspace(0, 1, ny+1)
    xx, yy = np.meshgrid(x, y, indexing='ij')
    xc = .5*(x[:-1]+x[1:]); yc = .5*(y[:-1]+y[1:])
    fluid = ~((xc[:,None] >= .6) & (yc[None,:] < .2))
    return xx, yy, fluid


def step_rhs(q, fluid, dx):
    g = np.pad(q, ((1,1),(1,1),(0,0)), mode='edge')
    g[0,1:-1] = conserved([1.4,3.,0.,1.])
    g[1:-1,0] = reflected(q[:,0], 0, 1)
    g[1:-1,-1] = reflected(q[:,-1], 0, 1)
    active = np.pad(fluid, ((1,1),(1,1)), mode='edge')
    fluxes = []
    for axis in (0,1):
        left, right = (g[:-1,1:-1], g[1:,1:-1]) if axis == 0 else (g[1:-1,:-1], g[1:-1,1:])
        ml, mr = (active[:-1,1:-1], active[1:,1:-1]) if axis == 0 else (active[1:-1,:-1], active[1:-1,1:])
        flux = hll_flux(left, right, axis)
        for mask, source, side in ((ml & ~mr, left, 'right'), (~ml & mr, right, 'left')):
            if not np.any(mask): continue
            wall = reflected(source[mask], int(axis==0), int(axis==1))
            flux[mask] = hll_flux(source[mask], wall, axis) if side == 'right' else hll_flux(wall, source[mask], axis)
        fluxes.append(flux)
    fx, fy = fluxes
    result = -(fx[1:]-fx[:-1]+fy[:,1:]-fy[:,:-1])/dx
    result[~fluid] = 0.
    return result


def solve_forward_step(ny=40, final_time=4., cfl=.4, snapshot_times=None):
    if not np.isfinite(final_time) or final_time < 0 or not 0 < cfl <= .4:
        raise ValueError('Require finite nonnegative time and 0 < CFL <= .4')
    x,y,fluid = step_geometry(ny)
    q = np.broadcast_to(conserved([1.4,3.,0.,1.]), (*fluid.shape,4)).copy()
    dx = 1/ny; time = 0.; steps = 0; history = []
    recorder = SnapshotRecorder(snapshot_times, final_time); recorder.capture(time,steps,q)
    while time < final_time:
        w = primitive(q)[fluid]; sound = np.sqrt(GAMMA*w[:,3]/w[:,0])
        dt = min(final_time-time, cfl*dx/(np.max(abs(w[:,1])+sound)+np.max(abs(w[:,2])+sound)))
        before = q
        first = q+dt*step_rhs(q,fluid,dx)
        q = .5*q+.5*(first+dt*step_rhs(first,fluid,dx))
        primitive(q); time += dt; steps += 1
        recorder.capture(time,steps,q)
        if steps % 50 == 0 or time == final_time:
            history.append((time,np.max(abs(q-before))/dt))
    return ShockResult(x,y,q,time,steps,fluid,np.full(fluid.shape,dx*dx),np.array(history),recorder.frames)
