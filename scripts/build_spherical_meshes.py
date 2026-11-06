"""Reproducible orthographic spherical mesh diagrams, not flow simulations."""
from pathlib import Path
import hashlib
import json
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from numart.spherical_meshes import (YIN_YANG_ROTATION, cube_panels, icosphere,
                                    lonlat, triangle_areas, unit, yin_yang_contains)

OUT = ROOT/'docs/figures'
BG = '#f5f2ea'
INK = '#23392f'
COLORS = ['#90aa9a', '#c2b17d', '#a4bacb', '#cf9f84', '#aca0bb', '#b5c8a4']
view = lonlat(np.deg2rad(30), np.deg2rad(28))
east = unit(np.cross([0, 0, 1], view))
north = np.cross(view, east)


def sphere(ax, kind):
    size = 700
    x, y = np.meshgrid(np.linspace(-1, 1, size), np.linspace(-1, 1, size))
    inside = x*x+y*y <= 1
    z = np.sqrt(np.maximum(0, 1-x*x-y*y))
    p = x[...,None]*east+y[...,None]*north+z[...,None]*view
    palette = COLORS
    if kind == 'cube':
        axis = np.argmax(abs(p), axis=-1)
        component = np.take_along_axis(p, axis[...,None], axis=-1)[...,0]
        index = 2*axis+(component > 0)
    elif kind == 'yin':
        a, b = yin_yang_contains(p, np.deg2rad(3))
        index = np.where(a & b, 2, np.where(a, 0, 1))
        palette = ['#a4bacb', '#d4ab8d', '#b3a1c3']
    else:
        index = np.zeros_like(x, dtype=int)
        palette = ['#dce3db']
    from matplotlib.colors import to_rgb
    rgba = np.ones((size, size, 4))
    rgb = np.array([to_rgb(c) for c in palette])[index]
    rgba[...,:3] = rgb*(.84+.16*z)[...,None]
    rgba[...,3] = inside.astype(float)
    ax.imshow(rgba, extent=(-1,1,-1,1), origin='lower', zorder=0)
    ax.add_patch(Circle((0,0),1,fill=False,color=INK,lw=.8,zorder=5))
    ax.set(xlim=(-1.08,1.08),ylim=(-1.08,1.08),aspect='equal')
    ax.axis('off')


def line(ax, points, color=INK, lw=.65, alpha=.8):
    points = np.asarray(points)
    visible = np.einsum('ij,j->i', points, view) >= 0
    xy = np.column_stack((np.einsum('ij,j->i', points, east), np.einsum('ij,j->i', points, north)))
    xy[~visible] = np.nan
    ax.plot(xy[:,0],xy[:,1],color=color,lw=lw,alpha=alpha,zorder=3)


def arc(ax, a, b, **kwargs):
    t = np.linspace(0,1,30)
    line(ax, unit((1-t[:,None])*a+t[:,None]*b), **kwargs)


fig, axes = plt.subplots(2,2,figsize=(10,10),facecolor=BG)
for ax in axes.ravel(): ax.set_facecolor(BG)
ax = axes[0,0];sphere(ax,'latlon')
for latitude in np.deg2rad(np.arange(-80,90,10)):
    line(ax, lonlat(np.linspace(-np.pi,np.pi,721),latitude))
for longitude in np.deg2rad(np.arange(-180,180,15)):
    line(ax, lonlat(longitude,np.linspace(-np.pi/2,np.pi/2,361)))
ax.plot([0],[np.array([0,0,1])@north],'o',color='#ad4b31',ms=5,zorder=6)
ax.set_title('01  LATITUDE / LONGITUDE',loc='left',color=INK,fontsize=12)
ax.text(.5,-.03,'Meridians converge at the geographic pole.\nZonal spacing shrinks as cos(latitude).',transform=ax.transAxes,ha='center',fontsize=10,color=INK)

ax=axes[0,1];sphere(ax,'yin')
for rotation, color in [(np.eye(3),'#345f81'),(YIN_YANG_ROTATION,'#97522e')]:
    lo=np.deg2rad(138);la=np.deg2rad(48)
    for latitude in np.linspace(-la,la,13):
        line(ax,np.einsum('...j,ij->...i',lonlat(np.linspace(-lo,lo,500),latitude), rotation),color=color)
    for longitude in np.linspace(-lo,lo,35):
        line(ax,np.einsum('...j,ij->...i',lonlat(longitude,np.linspace(-la,la,200)), rotation),color=color)
    for latitude in (-la,la):
        line(ax,np.einsum('...j,ij->...i',lonlat(np.linspace(-lo,lo,500),latitude), rotation),color=color,lw=1.7)
    for longitude in (-lo,lo):
        line(ax,np.einsum('...j,ij->...i',lonlat(longitude,np.linspace(-la,la,200)), rotation),color=color,lw=1.7)
ax.set_title('02  YIN–YANG / TWO OVERSET PATCHES',loc='left',color=INK,fontsize=12)
ax.text(.5,-.03,'Blue + orange = overlap (purple).\nEach patch excludes its own coordinate poles.',transform=ax.transAxes,ha='center',fontsize=10,color=INK)

ax=axes[1,0];sphere(ax,'cube')
for panel in cube_panels(8):
    for q in [*panel,*panel.transpose(1,0,2)]:
        for a,b in zip(q[:-1],q[1:]):arc(ax,a,b)
    for q in (panel[0],panel[-1],panel[:,0],panel[:,-1]):
        for a,b in zip(q[:-1],q[1:]):arc(ax,a,b,lw=1.7)
ax.set_title('03  CUBED SPHERE / SIX PANELS',loc='left',color=INK,fontsize=12)
ax.text(.5,-.03,'Equiangular gnomonic mapping shown.\nPanel seams replace latitude–longitude poles.',transform=ax.transAxes,ha='center',fontsize=10,color=INK)

v,f=icosphere(2)
edges=np.unique(np.sort(np.concatenate((f[:,:2],f[:,1:],f[:,[2,0]])),axis=1),axis=0)
ax=axes[1,1];sphere(ax,'ico')
for a,b in edges:arc(ax,v[a],v[b])
for p in v[:12]:
    if p@view>0:ax.plot(p@east,p@north,'o',ms=5,color='#ad4b31',zorder=5)
ax.set_title('04  ICOSAHEDRAL / TRIANGULAR',loc='left',color=INK,fontsize=12)
ax.text(.5,-.03,'20 base faces → 320 triangles (level 2).\nRed vertices have five neighbours; others have six.',transform=ax.transAxes,ha='center',fontsize=10,color=INK)
fig.suptitle('Cover a sphere. Move the difficult geometry.',fontsize=19,color=INK,y=.98)
fig.text(.5,.937,'Shared orthographic view · geometry illustrations, not computed fluid fields',ha='center',fontsize=10,color=INK)
fig.subplots_adjust(top=.90,bottom=.07,hspace=.32,wspace=.17)
fig.savefig(OUT/'spherical-meshes.png',dpi=160,facecolor=BG);plt.close(fig)

# A barycentric dual: normalized face centroids, explicitly not a Voronoi mesh.
centres=unit(v[f].sum(axis=1));adjacency={}
for j,face in enumerate(f):
    for a,b in ((face[0],face[1]),(face[1],face[2]),(face[2],face[0])):
        adjacency.setdefault(tuple(sorted((a,b))),[]).append(j)
fig,axes=plt.subplots(1,2,figsize=(10,5.4),facecolor=BG)
for ax,title in zip(axes,('Primal / triangular cells','Barycentric dual / pentagons + hexagons')):
    sphere(ax,'ico');ax.set_title(title,fontsize=12,color=INK)
for a,b in edges:arc(axes[0],v[a],v[b])
for (a,b), adjacent in adjacency.items():
    middle = unit(v[a]+v[b])
    arc(axes[1],centres[adjacent[0]],middle,color='#486ba2',lw=.9)
    arc(axes[1],middle,centres[adjacent[1]],color='#486ba2',lw=.9)
for ax in axes:
    for p in v[:12]:
        if p@view>0:ax.plot(p@east,p@north,'o',ms=5,color='#ad4b31',zorder=5)
fig.text(.5,.025,'Same level-2 mesh · red: the 12 five-valent vertices / pentagonal dual cells\nCentroids joined via edge midpoints; no ICON, NICAM or Voronoi mesh optimization.',ha='center',color=INK,fontsize=10)
fig.subplots_adjust(top=.90,bottom=.14,wspace=.12)
fig.savefig(OUT/'spherical-dual.png',dpi=160,facecolor=BG);plt.close(fig)

areas=triangle_areas(v,f)
data=dict(schema_version=1,scope='Spherical geometry diagrams only; no transport or dynamical-core solver.',
          view_longitude_degrees=30,view_latitude_degrees=28,
          yin_yang_buffer_degrees=3,cubed_sphere_cells_per_panel_axis=8,
          icosphere=dict(level=2,vertices=len(v),edges=len(edges),faces=len(f),
                         area_sum=float(sum(areas)),area_max_over_min=float(max(areas)/min(areas)),
                         dual='Normalized face-centroid barycentric dual, not Voronoi'),
          source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in
                         ('numart/spherical_meshes.py','scripts/build_spherical_meshes.py')},
          artifact_sha256={p:hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in ('spherical-meshes.png','spherical-dual.png')})
(OUT/'spherical-meshes.json').write_text(json.dumps(data,indent=2)+'\n')
print('Built spherical mesh overview and primal/dual comparison; area ratio:',data['icosphere']['area_max_over_min'])
