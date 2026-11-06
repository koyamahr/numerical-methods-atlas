"""Spherical mesh geometry for illustrations; no PDE discretization or solver."""
from itertools import combinations

import numpy as np

YIN_YANG_ROTATION = np.array([[-1., 0., 0.], [0., 0., 1.], [0., 1., 0.]])


def unit(points):
    points = np.asarray(points, dtype=float)
    return points / np.linalg.norm(points, axis=-1, keepdims=True)


def lonlat(longitude, latitude):
    longitude, latitude = np.broadcast_arrays(longitude, latitude)
    return np.stack((np.cos(latitude)*np.cos(longitude),
                     np.cos(latitude)*np.sin(longitude), np.sin(latitude)), axis=-1)


def yin_yang_contains(points, buffer=0.):
    """Membership of both patches; latitude/longitude limits in radians."""
    if not 0 <= buffer < np.pi/4:
        raise ValueError('Buffer must lie in [0, pi/4).')
    def contains(p):
        p = unit(p)
        return ((abs(np.arcsin(np.clip(p[..., 2], -1, 1))) <= np.pi/4+buffer+1e-14)
                & (abs(np.arctan2(p[..., 1], p[..., 0])) <= 3*np.pi/4+buffer+1e-14))
    return contains(points), contains(np.einsum('...j,ij->...i', points, YIN_YANG_ROTATION))


def cube_panels(n=8):
    """Six equiangular gnomonic panels, each (n+1,n+1,3), outward oriented."""
    if not isinstance(n, int) or n < 1:
        raise ValueError('Panel cell count must be a positive integer.')
    a, b = np.meshgrid(np.linspace(-np.pi/4, np.pi/4, n+1),
                       np.linspace(-np.pi/4, np.pi/4, n+1), indexing='ij')
    panels = []
    for axis in range(3):
        for sign in (-1, 1):
            normal = np.eye(3)[axis]*sign
            east = np.eye(3)[(axis+1) % 3]
            north = np.cross(normal, east)
            panels.append(unit(normal + np.tan(a)[..., None]*east + np.tan(b)[..., None]*north))
    return np.array(panels)


def icosphere(level=2):
    """Midpoint refinement and radial projection, without mesh optimization."""
    if not isinstance(level, int) or not 0 <= level <= 5:
        raise ValueError('Refinement level must be an integer from 0 to 5.')
    phi = (1+np.sqrt(5))/2
    vertices = unit([(0, a, b*phi) for a in (-1, 1) for b in (-1, 1)]
                    + [(a, b*phi, 0) for a in (-1, 1) for b in (-1, 1)]
                    + [(b*phi, 0, a) for a in (-1, 1) for b in (-1, 1)])
    distance = np.linalg.norm(vertices[:, None]-vertices[None, :], axis=-1)
    edge = np.isclose(distance, distance[distance > 1e-10].min())
    faces = []
    for i, j, k in combinations(range(12), 3):
        if edge[i, j] and edge[j, k] and edge[k, i]:
            if np.dot(np.cross(vertices[j]-vertices[i], vertices[k]-vertices[i]), vertices[i]) < 0:
                j, k = k, j
            faces.append((i, j, k))
    for _ in range(level):
        points, cache, refined = list(vertices), {}, []
        def midpoint(i, j):
            key = tuple(sorted((i, j)))
            if key not in cache:
                cache[key] = len(points)
                points.append(unit(vertices[i]+vertices[j]))
            return cache[key]
        for a, b, c in faces:
            ab, bc, ca = midpoint(a, b), midpoint(b, c), midpoint(c, a)
            refined.extend(((a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)))
        vertices, faces = np.array(points), refined
    return vertices, np.array(faces, dtype=int)


def triangle_areas(vertices, faces):
    """Unsigned solid angles on a unit sphere (minor great-circle triangles)."""
    a, b, c = np.moveaxis(vertices[faces], 1, 0)
    determinant = np.einsum('ij,ij->i', a, np.cross(b, c))
    denominator = 1+np.einsum('ij,ij->i', a, b)+np.einsum('ij,ij->i', b, c)+np.einsum('ij,ij->i', c, a)
    return 2*np.arctan2(abs(determinant), denominator)
