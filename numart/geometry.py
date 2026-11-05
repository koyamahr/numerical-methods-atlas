"""Small mesh, SPH reconstruction, and moving-volume examples; no flow solver."""
import numpy as np


def polygon_area(vertices):
    p = np.asarray(vertices,dtype=float)
    return .5*float(np.sum(p[:,0]*np.roll(p[:,1],-1)-p[:,1]*np.roll(p[:,0],-1)))


def mesh_topology(points, cells):
    p = np.asarray(points,dtype=float)
    areas,centers,edge_cells = [],[],{}
    for i,cell in enumerate(cells):
        vertices = p[cell]
        area = polygon_area(vertices)
        if area <= 0:raise ValueError('Cells must be counterclockwise and nondegenerate')
        areas.append(area);centers.append(vertices.mean(axis=0).tolist())
        for a,b in zip(cell,cell[1:]+cell[:1]):
            edge_cells.setdefault(tuple(sorted((a,b))),[]).append(i)
    neighbors = [set() for _ in cells]
    for adjacent in edge_cells.values():
        if len(adjacent)>2:raise ValueError('Nonmanifold mesh edge')
        if len(adjacent)==2:
            a,b = adjacent;neighbors[a].add(b);neighbors[b].add(a)
    return {'points':p.tolist(),'cells':cells,'areas':areas,'centers':centers,
            'edges':[list(e) for e in edge_cells],'neighbors':[sorted(n) for n in neighbors],
            'boundary_edges':sum(len(c)==1 for c in edge_cells.values())}


def example_meshes():
    from matplotlib.tri import Triangulation
    nx,ny = 8,6
    points = [[i/nx,j/ny] for j in range(ny+1) for i in range(nx+1)]
    quads,triangles = [],[]
    for j in range(ny):
        for i in range(nx):
            a = j*(nx+1)+i;b = a+1;d = a+nx+1;c = d+1
            quads.append([a,b,c,d]);triangles.extend(([a,b,c],[a,c,d]))
    boundary = [p for p in points if p[0] in (0,1) or p[1] in (0,1)]
    rng = np.random.default_rng(37);irregular = list(boundary)
    while len(irregular)<len(boundary)+38:
        candidate = rng.uniform(.06,.94,2)
        if min(np.linalg.norm(candidate-np.asarray(p)) for p in irregular)>.075:
            irregular.append(candidate.tolist())
    vertices = np.asarray(irregular)
    connectivity = Triangulation(vertices[:,0],vertices[:,1]).triangles.tolist()
    for cell in connectivity:
        if polygon_area(vertices[cell])<0:cell[1],cell[2]=cell[2],cell[1]
    return {'structured':mesh_topology(points,quads),
            'triangular':mesh_topology(points,triangles),
            'unstructured':mesh_topology(irregular,connectivity)}


def cubic_spline_kernel(distance,h):
    if h<=0:raise ValueError('Smoothing length must be positive')
    q = np.abs(np.asarray(distance))/h
    shape = np.where(q<1,1-1.5*q*q+.75*q**3,np.where(q<2,.25*(2-q)**3,0))
    return (2/(3*h))*shape


def sph_reconstruct(samples,particles,values,h,normalize=False):
    """Periodic 1D kernel sum, equal volume weights 1/N; not SPH dynamics."""
    if not 0<h<.25:raise ValueError('Periodic minimum-image kernel requires 0 < h < 1/4')
    x,p,v = np.asarray(samples),np.asarray(particles),np.asarray(values)
    delta = (x[:,None]-p[None,:]+.5)%1-.5
    weights = cubic_spline_kernel(delta,h)/len(p)
    result = np.sum(weights*v[None,:],axis=1)
    partition = weights.sum(axis=1)
    if normalize:
        if np.any(partition<=0):raise ValueError('No particle in kernel support')
        result = result/partition
    return result,partition


def moving_volume_uniform_test(n=24,amplitude=.06,phase=.8,dt=.1,value=1.,speed=.7):
    """One conservative ALE step of a uniform scalar, with consistent swept volumes."""
    if n<2 or abs(amplitude)>=1/(2*np.pi) or dt<=0:raise ValueError('Invalid moving-volume parameters')
    old = np.linspace(0,1,n+1)
    new = old+amplitude*np.sin(2*np.pi*old)*np.sin(phase)
    velocity = (new-old)/dt
    flux = (speed-velocity)*value
    mass = np.diff(old)*value-dt*np.diff(flux)
    updated = mass/np.diff(new)
    return old,new,updated
