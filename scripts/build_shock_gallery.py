"""Compute NASA wedge baselines and a classical forward-step shock movie.

Use --reuse to render unchanged cached trajectories without rerunning solvers.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.patches import Polygon
from PIL import Image
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from numart.shock_cases import solve_wedge, solve_forward_step, oblique_shock, shock_cell_fractions
from numart.euler2d import primitive

SOURCES=['numart/shock_cases.py','numart/euler2d.py','numart/snapshots.py']
CACHE=ROOT/'outputs/shock-gallery'
OUT=ROOT/'docs/figures'
MOVIES=ROOT/'website/public/assets/movies'
digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def trajectory(name, solver, reuse):
    path=CACHE/(name+'.npz'); record=CACHE/(name+'.json')
    hashes={p:digest(ROOT/p) for p in SOURCES}
    if reuse:
        assert json.loads(record.read_text())['source_sha256']==hashes, 'Cached numerical source changed'
        with np.load(path) as f: return {k:f[k] for k in f.files}
    start=time.monotonic();r=solver()
    data=dict(x=r.x_nodes,y=r.y_nodes,q=r.q,fluid=r.fluid,volumes=r.volumes,
              time=np.array(r.time),steps=np.array(r.steps),history=r.history)
    if r.snapshots:
        data.update(states=np.stack([s.q for s in r.snapshots]),
                    times=np.array([s.time for s in r.snapshots]),
                    saved_steps=np.array([s.step for s in r.snapshots]))
    np.savez_compressed(path,**data)
    record.write_text(json.dumps(dict(source_sha256=hashes),indent=2)+'\n')
    print(name, r.steps, 'steps;',round(time.monotonic()-start,1),'seconds',flush=True)
    return data


def wedge_diagnostics(data,mach):
    reference=oblique_shock(mach)
    fraction=shock_cell_fractions(data['x'],data['y'],reference['beta'])
    density_reference=1+(reference['density_ratio']-1)*fraction
    w=primitive(data['q']);volumes=data['volumes']
    xc=data['x'][:-1,0]+np.diff(data['x'][:,0])/2
    wall=(xc>.5)&(xc<.9)
    shock_points=[]
    centers=.25*(data['y'][:-1,:-1]+data['y'][1:,:-1]+data['y'][:-1,1:]+data['y'][1:,1:])
    for i in np.flatnonzero((xc>.35)&(xc<.85)):
        j=int(np.argmax(abs(np.diff(w[i,:,0]))))
        shock_points.append((xc[i],.5*(centers[i,j]+centers[i,j+1])))
    fitted=np.polyfit(*np.array(shock_points).T,1)
    return dict(shape=list(volumes.shape),time=float(data['time']),steps=int(data['steps']),
        beta_exact_degrees=float(np.rad2deg(reference['beta'])),
        beta_gradient_fit_degrees=float(np.rad2deg(np.arctan(fitted[0]))),
        pressure_ratio_exact=reference['pressure_ratio'],density_ratio_exact=reference['density_ratio'],
        downstream_mach_exact=reference['downstream_mach'],
        wall_pressure_ratio_median=float(np.median(w[wall,0,3])*1.4),
        density_cell_average_l1=float(np.sum(volumes*abs(w[...,0]-density_reference))/volumes.sum()),
        min_density=float(w[...,0].min()),min_pressure=float(w[...,3].min()),
        final_maximum_conserved_update_rate=float(data['history'][-1,1]))


def render_wedge(data,mach,diagnostics):
    w=primitive(data['q']);speed=np.hypot(w[...,1],w[...,2]);m=speed/np.sqrt(1.4*w[...,3]/w[...,0])
    fig,axes=plt.subplots(1,2,figsize=(11,5),layout='constrained')
    fields=(m,w[...,3]*1.4)
    for ax,field,title,cmap in zip(axes,fields,('Mach number','Pressure / upstream pressure'),('turbo','viridis')):
        image=ax.pcolormesh(data['x'],data['y'],field,cmap=cmap,shading='flat',rasterized=True)
        fig.colorbar(image,ax=ax,pad=.02)
        shockx=np.linspace(0,1,101)
        ax.plot(shockx,np.tan(np.deg2rad(diagnostics['beta_exact_degrees']))*shockx,'k--',lw=1.2,label='Exact weak shock')
        ax.fill_between(data['x'][:,0],0,data['y'][:,0],color='#333333')
        ax.set(title=title,xlabel='x',ylabel='y',xlim=(-.5,1),ylim=(0,1.2),aspect='equal')
        ax.legend(loc='upper left',fontsize=8)
    fig.suptitle(f'NASA 15-degree wedge | Mach {mach:g} | independent {data["q"].shape[0]} x {data["q"].shape[1]} body-fitted FV\n'
                 f'First-order HLL / SSPRK2 | t = {float(data["time"]):g} | '
                 f'wall p2/p1: {diagnostics["wall_pressure_ratio_median"]:.4f} (exact {diagnostics["pressure_ratio_exact"]:.4f})',fontsize=11)
    path=OUT/('nasa-wedge-m'+str(mach).replace('.','')+'.png')
    fig.savefig(path,dpi=140);plt.close(fig)
    return path.name


def render_step(data):
    target=MOVIES/'forward-step';target.mkdir(parents=True,exist_ok=True)
    primitive_states=[primitive(q) for q in data['states']];fluid=data['fluid']
    scales=[dict(label=label,min=float(min(w[...,k][fluid].min() for w in primitive_states)),
                 max=float(max(w[...,k][fluid].max() for w in primitive_states)))
            for label,k in [('Density ρ',0),('Pressure p',3)]]
    fig,axes=plt.subplots(2,1,figsize=(9.6,6.4),dpi=100)
    fig.subplots_adjust(left=.065,right=.92,bottom=.14,top=.83,hspace=.55)
    artists=[]
    for ax,k,scale in zip(axes,(0,3),scales):
        image=ax.imshow(np.ma.array(primitive_states[0][...,k],mask=~fluid).T,origin='lower',
            extent=(0,3,0,1),interpolation='nearest',cmap='magma' if k==0 else 'viridis',
            norm=Normalize(scale['min'],scale['max']),aspect='equal')
        ax.add_patch(Polygon([[.6,0],[3,0],[3,.2],[.6,.2]],color='#333333'))
        ax.set(xlabel='x',ylabel='y',title=scale['label'])
        fig.colorbar(image,ax=ax,fraction=.035,pad=.02);artists.append(image)
    heading=fig.suptitle('',y=.975,fontsize=13)
    fig.text(.5,.91,f'First-order HLL + SSPRK2 | {data["q"].shape[0]} x {data["q"].shape[1]} | CFL 0.4 | gamma 1.4',ha='center',fontsize=10)
    footer=fig.text(.5,.07,'',ha='center',fontsize=9)
    fig.text(.5,.025,'Classical forward-facing step | no corner entropy reset | not a NASA experimental validation',ha='center',fontsize=9)
    encoder=imageio_ffmpeg.write_frames(str(target/'evolution.mp4'),(960,640),pix_fmt_in='rgba',fps=12,
        codec='libx264',quality=8,ffmpeg_timeout=30,output_params=['-movflags','+faststart'])
    encoder.send(None);records=[]
    try:
        for i,w in enumerate(primitive_states):
            heading.set_text(f'Mach 3 forward-facing step | t = {data["times"][i]:.6f}')
            for artist,k in zip(artists,(0,3)):artist.set_data(np.ma.array(w[...,k],mask=~fluid).T)
            footer.set_text(f'Saved state {i+1}/{len(primitive_states)} | solver step {data["saved_steps"][i]} | fixed color scales')
            fig.canvas.draw();rgba=np.asarray(fig.canvas.buffer_rgba()).copy()
            path=target/f'frame-{i:03d}.webp';Image.fromarray(rgba).save(path,format='WEBP',lossless=True);encoder.send(rgba)
            records.append(dict(time=float(data['times'][i]),step=int(data['saved_steps'][i]),
                min_density=float(w[...,0][fluid].min()),max_density=float(w[...,0][fluid].max()),
                min_pressure=float(w[...,3][fluid].min()),max_pressure=float(w[...,3][fluid].max()),
                file='forward-step/'+path.name,image_sha256=digest(path),
                state_sha256=hashlib.sha256(data['states'][i].astype('<f8').tobytes()).hexdigest()))
    finally:encoder.close();plt.close(fig)
    # Final field: additional numerical schlieren exposes reflected shocks.
    w=primitive(data['q']);rho=np.ma.array(w[...,0],mask=~fluid)
    gx,gy=np.gradient(w[...,0],1/data['q'].shape[1]);gradient=np.hypot(gx,gy)
    interior=fluid.copy()
    interior[1:] &= fluid[:-1]; interior[:-1] &= fluid[1:]
    interior[:,1:] &= fluid[:,:-1]; interior[:,:-1] &= fluid[:,1:]
    fig,axes=plt.subplots(2,1,figsize=(10,7),layout='constrained')
    for ax,field,title,cmap in zip(axes,(rho,np.ma.array(np.log1p(gradient),mask=~interior)),
        ('Density','Numerical schlieren: log(1 + |grad density|); wall-adjacent differences masked'),('magma','gray_r')):
        image=ax.imshow(field.T,origin='lower',extent=(0,3,0,1),cmap=cmap,interpolation='nearest')
        ax.add_patch(Polygon([[.6,0],[3,0],[3,.2],[.6,.2]],color='#333333'))
        fig.colorbar(image,ax=ax,pad=.02);ax.set(title=title,xlabel='x',ylabel='y')
    fig.suptitle('Mach 3 forward-facing step | t = 4 | first-order HLL / SSPRK2\n'
                 'Classical inviscid benchmark; no special corner entropy correction',fontsize=11)
    fig.savefig(OUT/'forward-step.png',dpi=140);plt.close(fig)
    movie=dict(id='forward-step',title='Mach 3 forward-facing step',chapter='nasa-2d',
        method='First-order HLL + SSPRK2',shape=list(data['fluid'].shape),domain=[[0,3],[0,1]],
        boundary='fixed Mach-3 inflow / extrapolated outflow / reflecting tunnel and step walls',
        cfl=.4,final_time=4.,solver_steps=int(data['steps']),frames=records,requested_frames=81,
        scales=scales,fps=12,video='forward-step/evolution.mp4',poster=records[-1]['file'],
        video_sha256=digest(target/'evolution.mp4'),divergence_operator=None,
        scope='Classical inviscid step, not a NASA experimental case. First-order diffusive baseline; '
              'no special corner entropy reset, no viscosity or grid-converged fine structures. Diagnostics exclude solid cells.')
    return movie


def build(reuse=False):
    CACHE.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    wedges={};metrics={};files=[]
    for mach in (2.,2.5):
        series=[]
        for n in (40,80):
            key=f'wedge-{mach:g}-{n}'
            data=trajectory(key,lambda n=n,mach=mach:solve_wedge(n,mach,final_time=3.),reuse)
            diagnostics=wedge_diagnostics(data,mach);series.append(diagnostics)
        assert series[1]['density_cell_average_l1'] < series[0]['density_cell_average_l1']
        assert abs(series[-1]['wall_pressure_ratio_median']/series[-1]['pressure_ratio_exact']-1)<.03
        assert abs(series[-1]['beta_gradient_fit_degrees']-series[-1]['beta_exact_degrees'])<3
        files.append(render_wedge(data,mach,series[-1]));metrics[f'mach-{mach:g}']=series
        wedges[f'wedge{mach:g}']=data
        print('wedge diagnostics',mach,json.dumps(series),flush=True)
    step=trajectory('forward-step-80',lambda:solve_forward_step(80,4.,snapshot_times=np.linspace(0,4,81)),reuse)
    movie=render_step(step);files.append('forward-step.png')
    source_hashes={p:digest(ROOT/p) for p in SOURCES+['scripts/build_shock_gallery.py']}
    (MOVIES/'shock-catalog.json').write_text(json.dumps(dict(movies=[movie],source_sha256=source_hashes,
        quick=False,pixel_size=[960,640],sampling='First completed state at/after each output request; no shortened step or interpolation.'),indent=2)+'\n')
    arrays={}
    for key,data in {**wedges,'forward_step':step}.items():
        for name in ('x','y','q','fluid','time','steps'):arrays[key+'_'+name]=data[name]
    np.savez_compressed(OUT/'shock-gallery.npz',**arrays)
    files.append('shock-gallery.npz')
    manifest=dict(wedges=metrics,wedge_controls=dict(angle_degrees=15.,gamma=1.4,cfl=.4,
        upstream_density=1.,upstream_pressure=1/1.4,upstream_sound_speed=1.,
        x_domain=[-.5,1.],upper_boundary_y=1.2,lower_wall='max(x,0)*tan(15 degrees)',
        boundaries='fixed freestream inlet/top; extrapolated outlet; reflecting slip wall',
        initial_state='uniform freestream, no imposed analytical shock'),
        forward_step=dict(shape=list(step['fluid'].shape),time=4.,steps=int(step['steps']),
        fluid_area=float(step['volumes'][step['fluid']].sum()),frames=len(movie['frames']),
        min_density=movie['frames'][-1]['min_density'],min_pressure=movie['frames'][-1]['min_pressure']),
        method='First-order HLL / conservative body-fitted or grid-aligned finite volumes / SSPRK2',
        sources=['https://www.grc.nasa.gov/WWW/wind/valid/wedgeM2/wedgeM2.html',
                 'https://www.grc.nasa.gov/WWW/wind/valid/wedge/wedge.html',
                 'https://www.researchgate.net/publication/222459521_The_numerical_simulation_of_two-dimensional_fluid_flow_with_strong_shocks'],
        source_sha256=source_hashes,artifact_sha256={name:digest(OUT/name) for name in files},
        scope='Independent nondimensional Euler baselines, not Wind-US output or original PPM reproduction. '
              'Wedges start from uniform freestream, with two grids at the same finite terminal time. '
              'Density errors compare exactly clipped reference cell averages. '
              'Step uses plain reflecting corner treatment, one grid, and no exact solution.')
    (OUT/'shock-gallery.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Rendered shock fields, arrays and 81-frame step movie.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--reuse',action='store_true')
    build(parser.parse_args().reuse)
