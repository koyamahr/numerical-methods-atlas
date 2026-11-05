"""Render genuine 2D solver snapshots as inspectable WebP frames and MP4s.

Install optional encoder: python -m pip install '.[movies]'. Numerical steps
are unchanged by output requests. Regeneration keeps full states in outputs/.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.euler2d import solve_double_mach,primitive as euler_primitive
from numart.mhd import solve_orszag_tang,primitive as mhd_primitive
from numart.keep import solve_vortex


def build(output,quick=False):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    from PIL import Image,__version__ as pillow_version
    try:import imageio_ffmpeg
    except ImportError:raise SystemExit("Install the optional encoder with: python -m pip install '.[movies]'")
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fps=12;requested=9 if quick else 81
    n=16 if quick else 64
    specs=[('double-mach','Double Mach Reflection','euler',.02 if quick else .2,.4,'double-mach'),
           ('orszag-tang-ct','Orszag–Tang / constrained transport','ct',.04 if quick else .5,.3,'mhd'),
           ('orszag-tang-glm','Orszag–Tang / GLM cleaning','glm',.04 if quick else .5,.3,'mhd'),
           ('keep-vortex','Isentropic vortex / original KEEP','keep',.04 if quick else 4.,.25,'keep')]
    movies=[]
    for slug,title,method,final,cfl,chapter in specs:
        n=16 if quick else 96 if method=='keep' else 64
        times=np.linspace(0,final,requested)
        result=solve_double_mach(n,final,cfl,snapshot_times=times) if method=='euler' else solve_vortex(n,final,cfl,snapshot_times=times) if method=='keep' else solve_orszag_tang(n,final,method,cfl,snapshot_times=times)
        frames=result.snapshots;fields=[];diagnostics=[]
        for frame in frames:
            if method in ('euler','keep'):
                w=euler_primitive(frame.q);density,pressure= w[...,0],w[...,3]
            else:
                w=mhd_primitive(frame.q);density,pressure=w[0],w[3]
            fields.append((density,pressure))
            diagnostics.append({'time':frame.time,'step':frame.step,
                'min_density':float(density.min()),'max_density':float(density.max()),
                'min_pressure':float(pressure.min()),'max_pressure':float(pressure.max()),
                'mean_density':float(density.mean()),'mean_energy':float(frame.q[...,3].mean()),
                **frame.diagnostics})
        scales=[{'label':'Density ρ','min':float(min(f[k].min() for f in fields)),
                 'max':float(max(f[k].max() for f in fields))} for k in (0,1)]
        scales[1]['label']='Pressure p'
        target=output/slug;target.mkdir(exist_ok=True)
        fig,axes=plt.subplots(2,1,figsize=(9.6,6.4),dpi=100) if method=='euler' else plt.subplots(1,2,figsize=(9.6,6.4),dpi=100)
        fig.subplots_adjust(left=.07,right=.95,bottom=.16,top=.83,hspace=.52,wspace=.38)
        x_length=4 if method=='euler' else 20 if method=='keep' else 1
        extent=(-10,10,-10,10) if method=='keep' else (0,x_length,0,1);artists=[]
        for k,ax in enumerate(axes):
            artist=ax.imshow(fields[0][k].T,origin='lower',extent=extent,interpolation='nearest',
                             cmap='magma' if k==0 else 'viridis',norm=Normalize(scales[k]['min'],scales[k]['max']),aspect='equal')
            fig.colorbar(artist,ax=ax,pad=.025,fraction=.04,label=scales[k]['label'])
            ax.set(xlabel='x',ylabel='y',title=scales[k]['label']);artists.append(artist)
        heading=fig.suptitle('',fontsize=15,y=.965)
        scheme='First-order HLL + SSPRK2' if method=='euler' else 'Second-order original KEEP + classical RK4' if method=='keep' else f'First-order Rusanov + forward Euler | {method.upper()}'
        fig.text(.5,.9,f'{scheme} | {4*n if method=="euler" else n} × {n} | CFL={cfl}',ha='center',fontsize=11)
        note=fig.text(.5,.075,'',ha='center',fontsize=10)
        fig.text(.5,.025,'Fixed color scales over the complete run | genuine computed states | educational baseline',ha='center',fontsize=9,color='#555555')
        encoder=imageio_ffmpeg.write_frames(str(target/'evolution.mp4'),(960,640),pix_fmt_in='rgba',
                    fps=fps,codec='libx264',quality=8,ffmpeg_timeout=30,output_params=['-movflags','+faststart'])
        encoder.send(None);records=[]
        try:
            for index,(frame,field,stats) in enumerate(zip(frames,fields,diagnostics)):
                for artist,values in zip(artists,field):artist.set_data(values.T)
                heading.set_text(f'{title} | t = {frame.time:.6f}')
                text=f'Frame {index+1}/{len(frames)} | solver step {frame.step} | min ρ={stats["min_density"]:.5g} | min p={stats["min_pressure"]:.5g}'
                if method in ('ct','glm'):text+=f'\nmax |div B| ({"face" if method=="ct" else "central"}) = {stats["max_abs_divB"]:.3e}'
                note.set_text(text);fig.canvas.draw();rgba=np.asarray(fig.canvas.buffer_rgba()).copy()
                path=target/f'frame-{index:03d}.webp';Image.fromarray(rgba).save(path,format='WEBP',lossless=True)
                encoder.send(rgba)
                records.append({**stats,'file':f'{slug}/{path.name}',
                                'image_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                                'state_sha256':hashlib.sha256(frame.q.astype('<f8').tobytes()).hexdigest()})
        finally:encoder.close();plt.close(fig)
        archive=ROOT/'outputs/movies'/('quick' if quick else '');archive.mkdir(parents=True,exist_ok=True)
        np.savez_compressed(archive/(slug+'.npz'),q=np.stack([f.q for f in frames]),
                            times=[f.time for f in frames],steps=[f.step for f in frames])
        movies.append({'id':slug,'title':title,'chapter':chapter,'method':scheme,'shape':[4*n if method=='euler' else n,n],
                       'domain':[[-10,10],[-10,10]] if method=='keep' else [[0,x_length],[0,1]],'boundary':'mixed inflow / reflecting wall / moving top shock' if method=='euler' else 'periodic square',
                       'cfl':cfl,'final_time':final,'solver_steps':result.steps,'frames':records,'requested_frames':requested,
                       'scales':scales,'fps':fps,'video':f'{slug}/evolution.mp4','poster':records[-1]['file'],
                       'video_sha256':hashlib.sha256((target/'evolution.mp4').read_bytes()).hexdigest(),
                       'divergence_operator':None if method in ('euler','keep') else 'staggered face difference' if method=='ct' else 'cell-centered central difference',
                       'scope':'Diffusive first-order baseline; no fine wall-jet reproduction.' if method=='euler' else 'Smooth vortex only; original second-order KEEP, approximate entropy preservation, no shock stabilization or PEP extension.' if method=='keep' else 'First-order planar ideal MHD; CT/GLM native divergence operators differ; not an equal-accuracy ranking.'})
        print(f'{slug}: {len(frames)} frames, {result.steps} solver steps, t={result.time}',flush=True)
    sources=['numart/euler2d.py','numart/mhd.py','numart/snapshots.py','numart/keep.py','scripts/build_movies.py']
    data={'movies':movies,'sampling':'First completed state at/after each requested time; no interpolation and no time-step clipping.',
          'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
          'software':{'numpy':np.__version__,'matplotlib':matplotlib.__version__,'pillow':pillow_version,
                      'imageio_ffmpeg':imageio_ffmpeg.__version__,'ffmpeg':imageio_ffmpeg.get_ffmpeg_version()},
          'quick':quick,'pixel_size':[960,640],'playback':'One saved state per frame; FPS controls presentation speed, not physical dt.'}
    (output/'catalog.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    print('Wrote movie catalog and provenance:',output/'catalog.json')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'website/public/assets/movies')
    parser.add_argument('--quick',action='store_true',help='Small-grid, short-run encoder smoke test')
    args=parser.parse_args();build(args.output,args.quick)
