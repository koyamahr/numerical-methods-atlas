"""Reproducible first-order/minmod/MC Euler fields and synchronized clips."""
from pathlib import Path
import hashlib,json,sys,time,argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.patches import Polygon
from PIL import Image
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.muscl2d import solve_shock,smooth_entropy,entropy_average
from numart.shock_cases import solve_wedge,solve_forward_step
from numart.euler2d import primitive
from scripts.build_shock_gallery import wedge_diagnostics

SOURCES=['numart/muscl2d.py','numart/shock_cases.py','numart/euler2d.py','numart/snapshots.py']
OUT=ROOT/'website/public/assets/comparisons';CACHE=ROOT/'outputs/euler-comparison'
digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
LABELS={'first':'First order','minmod':'MUSCL / minmod','mc':'MUSCL / MC'}


def run(case,mach,n,method):
    key=f'{case}-{mach:g}-{n}-{method}';path=CACHE/(key+'.npz');record=CACHE/(key+'.json')
    config=dict(case=case,mach=mach,n=n,method=method,final_time=3. if case=='wedge' else 4.,cfl=.4,saved_frames=81 if case=='step' else 0)
    hashes={p:digest(ROOT/p) for p in SOURCES}
    metadata=dict(config=config,source_sha256=hashes)
    if path.exists() and record.exists() and json.loads(record.read_text())==metadata:
        with np.load(path) as f:return {k:f[k] for k in f.files}
    start=time.monotonic()
    if method=='first':
        legacy=ROOT/'outputs/shock-gallery'/((f'wedge-{mach:g}-{n}' if case=='wedge' else f'forward-step-{n}')+'.npz')
        legacy_record=legacy.with_suffix('.json')
        if legacy.exists() and legacy_record.exists() and all(digest(ROOT/p)==h for p,h in json.loads(legacy_record.read_text())['source_sha256'].items()):
            with np.load(legacy) as f:data={k:f[k] for k in f.files}
        else:
            r=solve_wedge(n,mach,final_time=3.) if case=='wedge' else solve_forward_step(n,4.,snapshot_times=np.linspace(0,4,81))
            data=dict(q=r.q,x=r.x_nodes,y=r.y_nodes,volumes=r.volumes,fluid=r.fluid,history=r.history,time=r.time,steps=r.steps)
            if r.snapshots:data.update(states=np.stack([s.q for s in r.snapshots]),times=[s.time for s in r.snapshots],saved_steps=[s.step for s in r.snapshots])
        data['retries']=np.array(0);data['scaled']=np.array(0)
    else:
        r=solve_shock(case,n,mach,method,config['final_time'],snapshot_times=np.linspace(0,4,81) if case=='step' else None)
        data=dict(q=r.q,x=r.geometry.x,y=r.geometry.y,volumes=r.geometry.volume,fluid=r.fluid,history=r.history,time=r.time,steps=r.steps,retries=r.retries,scaled=r.scaled_faces)
        if r.snapshots:data.update(states=np.stack([s.q for s in r.snapshots]),times=[s.time for s in r.snapshots],saved_steps=[s.step for s in r.snapshots])
    assert float(data['time'])==config['final_time'] and data['q'].shape==(3*n,n,4)
    assert hashes=={p:digest(ROOT/p) for p in SOURCES},'Sources changed during run'
    np.savez_compressed(path,**data);record.write_text(json.dumps(metadata,indent=2)+'\n')
    print(key,'steps',int(data['steps']),'seconds',round(time.monotonic()-start,1),flush=True)
    return data


def field(data,case,mach,method):
    w=primitive(data['q']);m=np.hypot(w[...,1],w[...,2])/np.sqrt(1.4*w[...,3]/w[...,0])
    fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout='constrained') if case=='wedge' else plt.subplots(2,1,figsize=(10,7),layout='constrained')
    for ax,values,label,cmap,limits in zip(axes,(m,w[...,3]*1.4 if case=='wedge' else w[...,3]),
        ('Mach number','Pressure / p1' if case=='wedge' else 'Pressure'),('turbo','viridis'),
        ((0,mach),(1,2.7)) if case=='wedge' else ((0,4),(0,18))):
        values=np.ma.array(values,mask=~data['fluid'])
        im=ax.pcolormesh(data['x'],data['y'],values,shading='flat',cmap=cmap,vmin=limits[0],vmax=limits[1])
        fig.colorbar(im,ax=ax,pad=.02);ax.set(title=label,xlabel='x',ylabel='y',aspect='equal')
        if case=='wedge':
            ref=wedge_diagnostics(data,mach);x=np.linspace(0,1,100)
            ax.plot(x,np.tan(np.deg2rad(ref['beta_exact_degrees']))*x,'k--',lw=1,label='Exact weak shock')
            ax.fill_between(data['x'][:,0],0,data['y'][:,0],color='#333');ax.legend(fontsize=8,loc='upper left')
        else:ax.add_patch(Polygon([[.6,0],[3,0],[3,.2],[.6,.2]],color='#333'))
    fig.suptitle(f'{"NASA wedge" if case=="wedge" else "Mach-3 forward step"} | M = {mach:g} | {LABELS[method]} / HLL / SSPRK2\n'
                 f'{data["q"].shape[0]} x {data["q"].shape[1]} | t = {float(data["time"]):g} | CFL 0.4 | common color scales',fontsize=11)
    name=f'{case}-m{mach:g}-{method}.png';fig.savefig(OUT/name,dpi=130);plt.close(fig);return name


def movie(data,method,scales):
    target=OUT/('step-'+method);target.mkdir(exist_ok=True)
    fig,axes=plt.subplots(2,1,figsize=(9.6,6.4),dpi=100);fig.subplots_adjust(left=.07,right=.94,bottom=.14,top=.83,hspace=.55)
    artists=[];fluid=data['fluid']
    for ax,k,scale in zip(axes,(0,3),scales):
        im=ax.imshow(np.zeros(fluid.shape).T,extent=(0,3,0,1),origin='lower',cmap='magma' if k==0 else 'viridis',norm=Normalize(scale['min'],scale['max']))
        ax.add_patch(Polygon([[.6,0],[3,0],[3,.2],[.6,.2]],color='#333'));ax.set(title=scale['label'],xlabel='x',ylabel='y')
        fig.colorbar(im,ax=ax,fraction=.035,pad=.02);artists.append(im)
    title=fig.suptitle('',y=.975,fontsize=14)
    fig.text(.5,.91,LABELS[method]+' / HLL / SSPRK2 | 240 x 80 | nominal CFL 0.4',ha='center',fontsize=10)
    footer=fig.text(.5,.07,'',ha='center',fontsize=9)
    fig.text(.5,.025,'Common scales across all three methods and all saved times | no corner entropy reset',ha='center',fontsize=9)
    encoder=imageio_ffmpeg.write_frames(str(target/'evolution.mp4'),(960,640),pix_fmt_in='rgba',fps=12,codec='libx264',quality=8,output_params=['-movflags','+faststart']);encoder.send(None)
    frames=[]
    try:
        for i,state in enumerate(data['states']):
            w=primitive(state)
            for im,k in zip(artists,(0,3)):im.set_data(np.ma.array(w[...,k],mask=~fluid).T)
            t=float(data['times'][i]);title.set_text(f'Mach-3 step | {LABELS[method]} | physical t = {t:.6f}')
            footer.set_text(f'Saved state {i+1}/81 | solver step {data["saved_steps"][i]}')
            fig.canvas.draw();rgba=np.asarray(fig.canvas.buffer_rgba()).copy();encoder.send(rgba)
            if i==len(data['states'])-1:Image.fromarray(rgba).save(target/'poster.webp',format='WEBP',lossless=True)
            frames.append(dict(time=t,step=int(data['saved_steps'][i]),state_sha256=hashlib.sha256(state.astype('<f8').tobytes()).hexdigest()))
    finally:encoder.close();plt.close(fig)
    decoder=imageio_ffmpeg.read_frames(str(target/'evolution.mp4'));info=next(decoder);assert sum(1 for _ in decoder)==81
    return dict(video=f'step-{method}/evolution.mp4',poster=f'step-{method}/poster.webp',frames=frames,fps=12,pixels=list(info['size']))


def build():
    OUT.mkdir(parents=True,exist_ok=True);CACHE.mkdir(parents=True,exist_ok=True)
    smooth=[]
    for method in LABELS:
        errors=[]
        for n in (16,32,64,128):
            r=smooth_entropy(n,limiter=method);errors.append(float(np.mean(abs(r.q[...,0]-entropy_average(n,.5)[...,0]))))
        smooth.append(dict(id=method,label=LABELS[method],n=[16,32,64,128],l1=errors,orders=np.log2(np.array(errors[:-1])/errors[1:]).tolist()))
    assert smooth[-1]['orders'][-1]>1.8
    fig,ax=plt.subplots(figsize=(7.5,4.5),layout='constrained')
    for row in smooth:ax.loglog(row['n'],row['l1'],'o-',label=row['label'])
    ax.set(title='2D smooth entropy wave | HLL / SSPRK2 / t = 0.5',xlabel='Cells per side',ylabel='Mean absolute density cell-average error');ax.legend();ax.grid(alpha=.2)
    fig.savefig(OUT/'smooth-refinement.png',dpi=140);plt.close(fig)
    cases=[];arrays={}
    for mach in (2.,2.5):
        methods=[]
        for method in LABELS:
            series=[]
            for n in (40,80):
                data=run('wedge',mach,n,method);stats=wedge_diagnostics(data,mach)
                stats.update(retried_steps=int(data['retries']),positivity_scaled_cells=int(data['scaled']));series.append(stats)
            name=field(data,'wedge',mach,method)
            methods.append(dict(id=method,label=LABELS[method],image=name,refinement=series,metrics=series[-1]))
            arrays[f'wedge{mach:g}_{method}']=data['q']
        cases.append(dict(id=f'wedge-m{mach:g}',title=f'NASA 15-degree wedge / Mach {mach:g}',kind='wedge',shape=[240,80],final_time=3.,methods=methods))
    step={method:run('step',3.,80,method) for method in LABELS}
    scales=[dict(label=label,min=min(float(np.min(primitive(d['states'][i])[...,k][d['fluid']])) for d in step.values() for i in range(81)),
                  max=max(float(np.max(primitive(d['states'][i])[...,k][d['fluid']])) for d in step.values() for i in range(81))) for label,k in [('Density',0),('Pressure',3)]]
    methods=[]
    for method,data in step.items():
        name=field(data,'step',3.,method);video=movie(data,method,scales)
        w=primitive(data['q']);metrics=dict(steps=int(data['steps']),retried_steps=int(data['retries']),positivity_scaled_cells=int(data['scaled']),
            min_density=float(w[...,0][data['fluid']].min()),min_pressure=float(w[...,3][data['fluid']].min()))
        methods.append(dict(id=method,label=LABELS[method],image=name,metrics=metrics,**video));arrays['step_'+method]=data['q']
    cases.append(dict(id='forward-step',title='Mach-3 forward-facing step',kind='step',shape=[240,80],final_time=4.,methods=methods,scales=scales))
    np.savez_compressed(OUT/'final-fields.npz',**arrays)
    sources=SOURCES+['scripts/build_euler_comparison.py','scripts/build_shock_gallery.py']
    files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='euler-comparison.json')
    manifest=dict(cases=cases,smooth=dict(series=smooth,image='smooth-refinement.png',reference='Exact 2D sinusoidal density cell averages; constant velocity (0.7,0.3), pressure 1; unit periodic square.'),
        cfl=.4,method='Acoustic HLL + SSPRK2; primitive first-order/minmod/MC reconstruction.',
        sampling='Same requested times; first completed state at/after each request. Intermediate physical timestamps differ. No interpolation.',
        scope='Same grid, nominal CFL, flux and RK method. Not equal step count or equal cost. Shock errors are not smooth-order tests. No step-corner entropy reset. Local face positivity scaling and time-step retries are counted, without clipping cell averages.',
        source_sha256={p:digest(ROOT/p) for p in sources},artifact_sha256={p.relative_to(OUT).as_posix():digest(p) for p in files})
    (OUT/'euler-comparison.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Euler comparison ready',flush=True)

if __name__=='__main__':build()
