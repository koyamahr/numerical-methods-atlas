import numpy as np
import pytest

from numart.spherical_meshes import (YIN_YANG_ROTATION, cube_panels, icosphere,
                                    lonlat, triangle_areas, yin_yang_contains)


@pytest.mark.parametrize('level', [0, 1, 2, 3])
def test_icosphere_closed_oriented_topology_and_area(level):
    v, f = icosphere(level)
    assert len(v) == 10*4**level+2
    assert len(f) == 20*4**level
    np.testing.assert_allclose(np.linalg.norm(v, axis=1), 1, atol=3e-16)
    edges, incidence = np.unique(np.sort(np.concatenate((f[:, :2], f[:, 1:], f[:, [2, 0]])), axis=1), axis=0, return_counts=True)
    assert len(edges) == 30*4**level
    assert np.all(incidence == 2)
    valence = np.bincount(edges.ravel(), minlength=len(v))
    assert np.sum(valence == 5) == 12
    assert np.all((valence == 5) | (valence == 6))
    assert np.all(np.einsum('ij,ij->i', np.cross(v[f[:, 1]]-v[f[:, 0]], v[f[:, 2]]-v[f[:, 0]]), v[f[:, 0]]) > 0)
    area = triangle_areas(v, f)
    assert min(area) > 0
    assert abs(sum(area)-4*np.pi) < 2e-13


def test_cube_boundaries_match_and_spherical_cells_tile_area():
    n = 9
    p = cube_panels(n)
    np.testing.assert_allclose(np.linalg.norm(p, axis=-1), 1, atol=3e-16)
    boundary = np.concatenate([np.concatenate((q[0], q[-1], q[1:-1, 0], q[1:-1, -1])) for q in p])
    _, count = np.unique(np.round(boundary, 12), axis=0, return_counts=True)
    assert np.sum(count == 3) == 8  # cube corners
    assert np.all((count == 2) | (count == 3))
    triangles = []
    for q in p:
        for i in range(n):
            for j in range(n):
                triangles.extend(([q[i,j],q[i+1,j],q[i+1,j+1]], [q[i,j],q[i+1,j+1],q[i,j+1]]))
    v = np.array(triangles).reshape(-1, 3)
    assert abs(sum(triangle_areas(v, np.arange(len(v)).reshape(-1,3)))-4*np.pi) < 1e-13


def test_yin_yang_rotation_coverage_and_overlap():
    r = YIN_YANG_ROTATION
    np.testing.assert_array_equal(r @ r.T, np.eye(3))
    assert np.linalg.det(r) == 1
    # Deterministic equal-area point sample; geometric coverage, not a PDE test.
    i = np.arange(30000)
    z = 1-2*(i+.5)/len(i)
    p = lonlat(i*np.pi*(3-np.sqrt(5)), np.arcsin(z))
    a, b = yin_yang_contains(p)
    assert np.all(a | b)
    assert abs(np.mean(a & b)-(3/(2*np.sqrt(2))-1)) < .002
    assert not yin_yang_contains([0,0,1])[0]
    assert yin_yang_contains([0,0,1])[1]
