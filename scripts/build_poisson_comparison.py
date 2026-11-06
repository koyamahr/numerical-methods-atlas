"""Reproducible same-system solver experiments; timings are host-specific."""
from pathlib import Path
import hashlib,json,sys,os,platform
from time import perf_counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from numart.poisson_comparison import problem,solve,direct_1d,direct_2d,METHODS
OUT=ROOT/'website/public/assets/poisson-comparison';OUT.mkdir(parents=True,exist_ok=True)
CACHE=ROOT/'outputs/poisson-comparison';CACHE.mkdir(parents=True,exist_ok=True)
SOURCES=['numart/poisson_comparison.py','numart/linear.py','numart/multigrid.py','scripts/build_poisson_comparison.py']
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
hashes={p:digest(ROOT/p) for p in SOURCES}
labels=['Jacobi','Weighted Jacobi / 2/3','Red-black Gauss–Seidel','Red-black SOR / model omega','Conjugate gradients','Geometric multigrid / V-cycle','DST + Thomas / separable direct','FFT / DST-I direct']
colors=['#a98064','#ba6265','#749a78','#9979a9','#527fa8','#a88e30','#4e9a9a','#444e42']
units=['sweeps','sweeps','sweeps','sweeps','CG iterations','V-cycles','direct pass','direct pass']
methods=[dict(id=m,label=label,color=color,unit=unit,direct=unit=='direct pass') for m,label,color,unit in zip(METHODS,labels,colors,units)]
# Initialize code paths on a small grid; no full-size untimed solve.
for method in METHODS:solve(problem(7)[1],method)
runs=[];cases=[];arrays={};tolerance=1e-8
for case in ['manufactured','localized','single-mode']:
 for n in ([31] if case=='single-mode' else [31,63,127]):
  x,f,exact=problem(n,case);ref=direct_2d(f);current=[]
  arrays[f'{case}-{n}-forcing']=f;arrays[f'{case}-{n}-reference']=ref
  if exact is not None:arrays[f'{case}-{n}-continuous']=exact
  for method in methods:
   trials=[]
   for repeat in range(3):
    result=solve(f,method['id'],tolerance)
    if not result.converged:raise RuntimeError(f'{case} {n} {method["id"]} failed common tolerance')
    trials.append(result)
    np.savez_compressed(CACHE/f'{case}-{n}-{method["id"]}-{repeat}.npz',q=result.q,history=result.history)
   order=np.argsort([r.seconds for r in trials]);selected=int(order[1]);r=trials[selected];count=len(r.history)
   indices=np.unique(np.concatenate((np.arange(min(count,17)),np.linspace(0,count-1,min(count,220),dtype=int),np.geomspace(1,count,min(count,80)).astype(int)-1)))
   data=dict(case=case,n=n,unknowns=n*n,method=method['id'],steps=r.steps,unit=method['unit'],omega=r.omega,seconds=r.seconds,trial_seconds=[v.seconds for v in trials],selected_trial=selected,
             relative_residual=float(r.history[-1,2]),algebraic_rms=float(np.sqrt(np.mean((r.q-ref)**2))),continuous_rms=float(np.sqrt(np.mean((r.q-exact)**2))) if exact is not None else None,
             history=r.history[indices].tolist(),full_history_length=count)
   runs.append(data);current.append(data);arrays[f'{case}-{n}-{method["id"]}-solution']=r.q;arrays[f'{case}-{n}-{method["id"]}-history']=r.history
   print(case,n,method['id'],'units',r.steps,'median',round(r.seconds,5),'residual',round(data['relative_residual'],12),flush=True)
  fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
  for ax,value,title in zip(axs,(f,ref),('Forcing f','Discrete solution / FFT-DST')):
   im=ax.imshow(value.T,origin='lower',extent=(0,1,0,1),cmap='RdBu_r');ax.set(title=title,xlabel='x',ylabel='y');fig.colorbar(im,ax=ax,shrink=.8)
  fig.suptitle(f'{case} | {n} x {n} interior unknowns | -Laplacian u=f | zero Dirichlet / same five-point operator')
  name=f'{case}-{n}-fields.png';fig.savefig(OUT/name,dpi=125);plt.close(fig)
  cases.append(dict(id=case,n=n,fields_image=name,discrete_continuous_rms=float(np.sqrt(np.mean((ref-exact)**2))) if exact is not None else None))
# 1D plain Thomas versus FFT-DST, distinct from the separable 2D method.
one_d=[]
for n in [63,255,1023]:
 x=(np.arange(n)+1)/(n+1);exact=x*(1-x)*np.exp(2*x);f=-(4*x*(1-x)+4*(1-2*x)-2)*np.exp(2*x)
 for method in ['thomas','fft-dst']:
  samples=[]
  for _ in range(3):
   start=perf_counter();q=direct_1d(f,method);a=np.pad(q,1);res=f-(2*q-a[:-2]-a[2:])*(n+1)**2
   relative=float(np.sqrt(np.sum(res*res))/np.sqrt(np.sum(f*f)));samples.append(perf_counter()-start)
  one_d.append(dict(n=n,method=method,seconds=float(np.median(samples)),trial_seconds=samples,relative_residual=relative,continuous_rms=float(np.sqrt(np.mean((q-exact)**2)))))
# A static overview, with no claim that iterations are equal-cost operations.
fig,axs=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
for method in methods:
 values=[r for r in runs if r['case']=='manufactured' and r['method']==method['id']];r=next(r for r in values if r['n']==63);h=np.asarray(r['history'])
 if method['direct']:axs[0].scatter([r['steps']],[r['relative_residual']],color=method['color'],marker='D')
 else:axs[0].semilogy(h[:,0],h[:,2],color=method['color'],label=method['label'])
 axs[1].loglog([r['unknowns'] for r in values],[r['seconds'] for r in values],'o-',color=method['color'],label=method['label'])
axs[0].axhline(tolerance,color='k',ls='--',lw=.8);axs[0].set(yscale='log',xlabel='Sweeps, CG iterations or V-cycles (different work)',ylabel='Recomputed relative residual',title='Broad smooth forcing | 63 x 63')
axs[1].set(xlabel='Interior unknowns N squared',ylabel='Median diagnostic solve seconds / 3 trials',title='One host, these implementations');axs[1].legend(fontsize=7)
for ax in axs:ax.grid(alpha=.2)
fig.suptitle('Poisson solver comparison | same grid, operator, boundaries and relative tolerance 1e-8')
fig.savefig(OUT/'overview.png',dpi=130);plt.close(fig)
np.savez_compressed(OUT/'fields-and-histories.npz',**arrays)
assert hashes=={p:digest(ROOT/p) for p in SOURCES},'Sources changed during build'
manifest=dict(methods=methods,runs=runs,cases=cases,one_dimensional=one_d,tolerance=tolerance,
 history_columns=['completed_method_units','elapsed_seconds','true_relative_residual'],
 environment=dict(python=platform.python_version(),numpy=np.__version__,system=platform.system(),release=platform.release(),machine=platform.machine(),thread_environment={k:os.environ.get(k) for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']}),
 timing='Three fresh diagnostic solves per method/problem/grid after a small n=7 code-path warmup. Zero initial iterate. Median wall time; its own sampled history is displayed. Includes validation, allocation, residual recomputation every unit, and logging; excludes imports, problem generation, disk I/O, reference construction and plots. No reuse of factorizations/eigenvalues. Single-host Python/NumPy implementations, not a universal algorithm or hardware ranking.',
 scope='Constant coefficient -Laplacian on [0,1]^2, zero Dirichlet, square uniform grids and identical five-point SPD systems. Relative residual ||f-Au||2/||f||2 <=1e-8, explicitly recomputed for every solver including CG. Continuous error is nodal RMS, not a continuous L2 norm; localized-source case has only a discrete reference. Single sine mode is a special CG one-iteration diagnostic. FFT uses odd-extension DST-I and discrete eigenvalues, not periodic boundaries or continuum k squared. SOR omega=2/(1+sin(pi/(n+1))) is specific to this model/order. MG uses existing rediscretized V-cycle with three RBGS pre/post sweeps per level. Thomas alone is 1D; 2D DST+Thomas requires separability. No variable coefficient, anisotropy, Neumann nullspace or irregular mesh claims.',
 source_sha256=hashes,artifact_sha256={p.name:digest(p) for p in OUT.iterdir() if p.suffix in ('.png','.npz')})
(OUT/'comparison.json').write_text(json.dumps(manifest,separators=(',',':'),allow_nan=False)+'\n')
print('Poisson comparison ready',flush=True)
