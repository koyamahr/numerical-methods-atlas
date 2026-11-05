"""Periodic 2D MAC projection, centered convection, explicit SSPRK2.

Unit density, square [0,L)^2. FFT inverts the discrete DG Laplacian,
not the continuum k^2 symbol. This is not a wall/cavity solver.
"""
import numpy as np


def divergence(u, v, h):
    return (np.roll(u, -1, 0)-u+np.roll(v, -1, 1)-v)/h


def gradient(p, h):
    return (p-np.roll(p, 1, 0))/h, (p-np.roll(p, 1, 1))/h


def laplacian(q, h):
    return (np.roll(q, 1, 0)+np.roll(q, -1, 0)+np.roll(q, 1, 1)+np.roll(q, -1, 1)-4*q)/h**2


def poisson(rhs, h):
    nx, ny = rhs.shape
    symbol = -4/h**2*(np.sin(np.pi*np.fft.fftfreq(nx))[:, None]**2
                       +np.sin(np.pi*np.fft.fftfreq(ny))[None, :]**2)
    symbol[0, 0] = 1.
    transformed = np.fft.fft2(rhs-rhs.mean())/symbol
    transformed[0, 0] = 0.
    return np.fft.ifft2(transformed).real


def project(u, v, h):
    multiplier = poisson(divergence(u, v, h), h)
    gx, gy = gradient(multiplier, h)
    return u-gx, v-gy


def rhs(u, v, h, viscosity):
    vu = (v+np.roll(v, 1, 0)+np.roll(v, -1, 1)+np.roll(np.roll(v, 1, 0), -1, 1))/4
    uv = (u+np.roll(u, -1, 0)+np.roll(u, 1, 1)+np.roll(np.roll(u, -1, 0), 1, 1))/4
    derivative = lambda q, axis: (np.roll(q, -1, axis)-np.roll(q, 1, axis))/(2*h)
    return (-u*derivative(u, 0)-vu*derivative(u, 1)+viscosity*laplacian(u, h),
            -uv*derivative(v, 0)-v*derivative(v, 1)+viscosity*laplacian(v, h))


def taylor_green(n=32, final_time=.5, viscosity=.1, cfl=.2):
    if n < 4 or final_time < 0 or viscosity < 0 or not 0 < cfl <= .4:
        raise ValueError('Invalid MAC controls')
    h = 2*np.pi/n
    face = np.arange(n)*h; center = face+h/2
    u = np.sin(face[:, None])*np.cos(center[None, :])
    v = -np.cos(center[:, None])*np.sin(face[None, :])
    t = 0.; history = [[t, .5*np.mean(u*u+v*v), np.max(abs(divergence(u, v, h)))]]
    while t < final_time:
        dt = min(final_time-t, cfl/(np.max(abs(u))/h+np.max(abs(v))/h+4*viscosity/h**2))
        a, b = rhs(u, v, h, viscosity); ua, va = project(u+dt*a, v+dt*b, h)
        a, b = rhs(ua, va, h, viscosity); ub, vb = project(ua+dt*a, va+dt*b, h)
        u, v = (u+ub)/2, (v+vb)/2; t += dt
        history.append([t, .5*np.mean(u*u+v*v), np.max(abs(divergence(u, v, h)))])
    a, b = rhs(u, v, h, viscosity)
    pressure = poisson(divergence(a, b, h), h)
    exact_u = np.sin(face[:, None])*np.cos(center[None, :])*np.exp(-2*viscosity*t)
    exact_v = -np.cos(center[:, None])*np.sin(face[None, :])*np.exp(-2*viscosity*t)
    return dict(u=u, v=v, pressure=pressure, exact_u=exact_u, exact_v=exact_v,
                h=h, time=t, history=np.array(history),
                error=float(np.sqrt(np.mean((u-exact_u)**2+(v-exact_v)**2))))
