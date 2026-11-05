"""Reproducible runs and a static figure gallery, ready for later publishing."""
import argparse
import json
from pathlib import Path
import platform
import subprocess
import hashlib
import numpy as np
from .benchmarks import get_problem, list_problems
from .solvers import solve
from .limiters import LIMITERS
from .mhd import solve_orszag_tang, primitive as mhd_primitive
from .euler2d import solve_double_mach, primitive as euler2d_primitive
from .advection import (amplification, difference_step, dg_advection,
                        spectral_advection, dual_time_advection, conditioning_example)
from .linear import (diffusion_1d,poisson_1d,Boundary,poisson_boundary_1d,
                     iteration_matrix,spectral_radius)
from .multigrid import solve_poisson_multigrid,red_black_gauss_seidel,laplacian_operator


def _plotting():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"figure.dpi":140,"axes.spines.top":False,"axes.spines.right":False,
                         "axes.grid":True,"grid.alpha":.2,"font.size":10,"savefig.bbox":"tight"})
    return plt


def _metadata():
    try:
        revision = subprocess.check_output(["git","rev-parse","HEAD"],stderr=subprocess.DEVNULL,text=True).strip()
        dirty = bool(subprocess.check_output(["git","status","--porcelain"],text=True).strip())
    except (subprocess.CalledProcessError,FileNotFoundError):
        revision,dirty = None,True
    hashes = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob("*.py"))}
    return {"python":platform.python_version(),"numpy":np.__version__,"source_sha256":hashes,"git_revision":revision,
            "git_dirty":dirty,"scope":"educational implementations; not original-figure reproductions"}


def _write_json(path, value):
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False)+"\n",encoding="utf-8")


def run_case(args):
    if args.limiter != "minmod" and (args.problem in ("double-mach", "orszag-tang") or args.method not in (None, "muscl")):
        raise ValueError("--limiter selects a 1D MUSCL reconstruction only")
    out = Path(args.output)
    out.mkdir(parents=True,exist_ok=True)
    if args.problem == "double-mach":
        if args.method not in (None,"godunov") or args.riemann not in (None,"hll"):
            raise ValueError("The 2D double-mach baseline supports godunov + hll only")
        method = "godunov"
        r = solve_double_mach(args.n,args.time if args.time is not None else .2,args.cfl)
        w = euler2d_primitive(r.q)
        np.savez_compressed(out/"solution.npz",x=r.x,y=r.y,q=r.q,time=r.time)
        plt = _plotting()
        fig,axes = plt.subplots(2,1,figsize=(12,6))
        image = axes[0].pcolormesh(r.x,r.y,w[...,0].T,shading="nearest",cmap="magma")
        fig.colorbar(image,ax=axes[0],label="density")
        levels = np.linspace(float(w[...,0].min()),float(w[...,0].max()),32)[1:-1]
        axes[1].contour(r.x,r.y,w[...,0].T,levels=levels,colors="#26382f",linewidths=.5)
        for ax in axes:
            ax.set(xlim=(0,4),ylim=(0,1),xlabel="x",ylabel="y",aspect="equal")
        axes[0].set_title(f"Double Mach Reflection | {4*args.n} x {args.n} | t={r.time:g} | first-order HLL + SSPRK2")
        axes[1].set_title("Density contours | qualitative baseline; not the original PPM resolution")
        fig.tight_layout();fig.savefig(out/"double-mach.png");plt.close(fig)
        stats = {"steps":r.steps,"time":r.time,"riemann":"HLL with Davis wave speeds",
                 "shape":[4*args.n,args.n],"domain":[[0,4],[0,1]],"gamma":1.4,
                 "min_density":float(w[...,0].min()),"min_pressure":float(w[...,3].min()),
                 "boundary":"postshock left; outflow right; mixed reflecting/inflow bottom; moving shock top",
                 "citation":"woodward1984","scope":"first-order 2D educational baseline; no fine-grid reproduction claim"}
    elif args.problem == "orszag-tang":
        method = args.method or "ct"
        r = solve_orszag_tang(args.n,args.time if args.time is not None else .5,method,args.cfl)
        np.savez_compressed(out/"solution.npz",q=r.q,time=r.time,divergence=r.divergence,
                            history=r.history,bx_face=r.bx_face if r.bx_face is not None else [],
                            by_face=r.by_face if r.by_face is not None else [])
        stats = {"max_abs_divB":float(abs(r.divergence).max()),"steps":r.steps,"time":r.time}
    else:
        p = get_problem(args.problem)
        method = args.method or "muscl"
        solver = args.riemann or ("hlle" if p.name == "double-rarefaction" else "hllc" if p.equation.name == "euler" else "hll")
        r = solve(p,args.n,method,solver,args.cfl,args.time,limiter=args.limiter)
        np.savez_compressed(out/"solution.npz",x=r.x,q=r.q,time=r.time)
        stats = {"steps":r.steps,"time":r.time,"riemann":solver if method != "weno5" else "global LF flux splitting",
                 "boundary":p.boundary,"domain":p.domain,"citation":p.citation,
                 "limiter":args.limiter if method == "muscl" else None}
        if p.reference:
            stats["density_L1_pointwise"] = float(np.mean(abs(r.q[:,0]-p.reference(r.x,r.time)[:,0])))
    _write_json(out/"run.json",{**_metadata(),"problem":args.problem,"n":args.n,"method":method,"cfl":args.cfl,**stats})
    print(out.resolve())


def build_gallery(output):
    plt = _plotting()
    out = Path(output)
    out.mkdir(parents=True,exist_ok=True)
    metrics = {}
    def save(fig,name):
        fig.savefig(out/(name+".png"))
        plt.close(fig)

    fig,axes = plt.subplots(1,3,figsize=(13,3.8))
    p = get_problem("sod")
    for solver in ("rusanov","hll","hllc","roe"):
        r = solve(p,200,riemann=solver)
        w = p.equation.primitive(r.q)
        for k,ax in enumerate(axes):
            ax.plot(r.x,w[:,k],label=solver.upper(),lw=1.2)
        metrics["sod_"+solver+"_density_L1"] = float(np.mean(abs(r.q[:,0]-p.reference(r.x,r.time)[:,0])))
    w = p.equation.primitive(p.reference(r.x,r.time))
    for k,ax in enumerate(axes):
        ax.plot(r.x,w[:,k],"k--",label="exact",lw=1)
        ax.set(xlabel="x",ylabel=("density","velocity","pressure")[k])
    axes[0].legend(fontsize=8)
    fig.suptitle("Sod (1978) | MUSCL + Riemann solvers | N=200, t=0.2")
    fig.tight_layout()
    save(fig,"sod")

    p = get_problem("shu-osher")
    fig,ax = plt.subplots(figsize=(9,3.8))
    for method in ("muscl","weno5"):
        r = solve(p,400,method=method)
        ax.plot(r.x,r.q[:,0],label=method,lw=1.1)
        np.savez_compressed(out/("shu-osher-"+method+".npz"),x=r.x,q=r.q,time=r.time)
    ax.set(xlabel="x",ylabel="density",title="Shu–Osher (1989) | N=400, t=1.8 | numerical comparison")
    ax.legend()
    save(fig,"shu-osher")

    fig,axes = plt.subplots(1,2,figsize=(10,3.8))
    theta = np.linspace(0,np.pi,1000)
    for c in (.5,1.,1.1):
        for method,ls in (("lax-friedrichs","--"),("lax-wendroff","-")):
            axes[0].plot(theta,abs(amplification(theta,c,method)),ls,label=f"{method}, C={c}")
    axes[0].axhline(1,color="k",lw=.6)
    axes[0].set(xlabel="wavenumber angle",ylabel="|G|",title="von Neumann amplification")
    axes[0].legend(fontsize=6)
    x = (np.arange(128)+.5)/128
    for c in (.8,1.1):
        q = np.sin(2*np.pi*x)+1.e-7*(-1.)**np.arange(128)
        amplitudes = [float(abs(q).max())]
        for _ in range(80):
            q = difference_step(q,c,"lax-wendroff")
            amplitudes.append(float(abs(q).max()))
        axes[1].semilogy(amplitudes,label=f"C={c}")
    axes[1].set(xlabel="step",ylabel="max |u|",title="Lax–Wendroff: seeded Nyquist mode")
    axes[1].legend()
    fig.tight_layout()
    save(fig,"stability")

    fig,axes = plt.subplots(1,2,figsize=(10,3.8))
    x,u,_ = dg_advection(n=24,degree=2)
    axes[0].plot(x.ravel(),u.ravel(),".",ms=2,label="DG P2, 24 elements")
    xs = np.arange(32)/32
    us = spectral_advection(np.sin(2*np.pi*xs),1.)
    axes[0].plot(xs,us,"+",label="Fourier, 32 points")
    axes[0].plot(np.linspace(0,1,500),np.sin(2*np.pi*np.linspace(0,1,500)),"k--",lw=1,label="exact")
    axes[0].set(xlabel="x",ylabel="u",title="Periodic advection, t=1")
    axes[0].legend(fontsize=8)
    for degree in (0,1,2):
        errors=[]
        ns=[8,16,32,64]
        for n in ns:
            x,u,_ = dg_advection(n,degree,final_time=.2)
            errors.append(float(np.sqrt(np.mean((u-np.sin(2*np.pi*(x-.2)))**2))))
        axes[1].loglog(ns,errors,"o-",label=f"DG P{degree}")
        metrics[f"dg_p{degree}_errors"] = errors
    axes[1].set(xlabel="elements",ylabel="quadrature-sampled RMS error",title="DG grid refinement (not DOF matched)")
    axes[1].legend()
    fig.tight_layout()
    save(fig,"dg-spectral")

    fig,axes = plt.subplots(1,2,figsize=(10,3.8))
    for name,ax in zip(("dam-break","isothermal"),axes):
        p = get_problem(name)
        for solver in ("rusanov","hll"):
            r = solve(p,200,riemann=solver)
            ax.plot(r.x,r.q[:,0],label=solver)
        ax.set(xlabel="x",ylabel="depth" if name == "dam-break" else "density",title=f"{name}, t=0.1")
        ax.legend()
    fig.tight_layout()
    save(fig,"barotropic")

    mhd_runs={method:solve_orszag_tang(64,method=method) for method in ("ct","glm")}
    density_min=min(r.q[...,0].min() for r in mhd_runs.values())
    density_max=max(r.q[...,0].max() for r in mhd_runs.values())
    fig,axes = plt.subplots(1,3,figsize=(12,3.8))
    for method,ax in zip(("ct","glm"),axes[:2]):
        r = mhd_runs[method]
        im = ax.imshow(r.q[...,0].T,origin="lower",extent=(0,1,0,1),cmap="magma",vmin=density_min,vmax=density_max)
        ax.set(title=f"{method.upper()} | density, t=0.5",xlabel="x",ylabel="y")
        fig.colorbar(im,ax=ax,shrink=.75)
        axes[2].semilogy(r.history[:,0],np.maximum(r.history[:,1],1.e-16),label=method.upper())
        metrics["orszag_tang_"+method] = {"n":64,"steps":r.steps,"time":r.time,
            "min_pressure":float(mhd_primitive(r.q)[3].min()),"max_abs_divB":float(abs(r.divergence).max()),
            "relative_mass_drift":float(abs(r.history[-1,2]/r.history[0,2]-1)),
            "relative_energy_drift":float(abs(r.history[-1,3]/r.history[0,3]-1))}
        np.savez_compressed(out/("orszag-tang-"+method+".npz"),q=r.q,history=r.history,
                            divergence=r.divergence,time=r.time)
    axes[2].set(xlabel="time",ylabel="max |discrete div B|",title="Native discrete operators differ")
    axes[2].legend()
    fig.tight_layout()
    save(fig,"orszag-tang")

    fig,axes = plt.subplots(1,2,figsize=(10,3.8))
    x,q,res = dual_time_advection()
    axes[0].semilogy(res)
    axes[0].set(xlabel="pseudo-time iteration",ylabel="residual infinity norm",title="BDF2 + Jacobi pseudo-time | last step")
    a,scaled = conditioning_example()
    conditions = [float(np.linalg.cond(a)),float(np.linalg.cond(scaled))]
    axes[1].bar(["A","P^(-1/2) A P^(-1/2)"],conditions,color=["#b95545","#327f83"])
    axes[1].set(yscale="log",ylabel="2-norm condition number",title="Jacobi scaling | SPD model matrix")
    metrics["conditioning"] = {"before":conditions[0],"after":conditions[1]}
    metrics["dual_time"] = {"n":64,"physical_dt":.02,"time":.2,"last_inner_residual":float(res[-1]),"last_inner_iterations":len(res)}
    fig.tight_layout()
    save(fig,"implicit")

    fig,axes=plt.subplots(1,2,figsize=(10,3.8))
    p=get_problem("lax")
    for solver in ("hllc","roe","hlle"):
        r=solve(p,200,riemann=solver)
        axes[0].plot(r.x,r.q[:,0],label=solver,lw=1)
    axes[0].plot(r.x,p.reference(r.x,r.time)[:,0],"k--",label="exact",lw=1)
    axes[0].set(xlabel="x",ylabel="density",title="Lax shock tube | N=200, t=1.3")
    axes[0].legend(fontsize=8)
    p=get_problem("entropy-wave")
    for method in ("muscl","weno5"):
        errors=[]
        ns=(40,80,160)
        for n in ns:
            r=solve(p,n,method=method)
            errors.append(float(np.mean(abs(r.q[:,0]-p.reference(r.x,r.time)[:,0]))))
        axes[1].loglog(ns,errors,"o-",label=method)
        metrics["entropy_"+method+"_density_L1"]=errors
    axes[1].set(xlabel="grid points/cells",ylabel="pointwise L1 error",title="Euler entropy wave | t=1")
    axes[1].legend()
    fig.tight_layout()
    save(fig,"lax-entropy")

    fig,axes=plt.subplots(1,2,figsize=(10,3.8))
    for method in ("ftcs","backward-euler","crank-nicolson"):
        x,q,meta=diffusion_1d(n=63,dt=None if method=="ftcs" else .005,method=method)
        axes[0].plot(x,q,label=method,lw=1)
        metrics["diffusion_"+method]={**meta,"n":63,"max_error":float(abs(q-np.exp(-np.pi**2*.1)*np.sin(np.pi*x)).max())}
    axes[0].plot(x,np.exp(-np.pi**2*.1)*np.sin(np.pi*x),"k--",label="exact",lw=1)
    axes[0].set(xlabel="x",ylabel="u",title="Diffusion | Dirichlet, t=0.1 | different dt")
    axes[0].legend(fontsize=8)
    for name,left,right in (("Dirichlet",Boundary.dirichlet(1.),Boundary.dirichlet(2.)),
                            ("mixed",Boundary.dirichlet(1.),Boundary.neumann(2.)),
                            ("Robin",Boundary(1.,1.,1.),Boundary(1.,1.,4.))):
        x,q=poisson_boundary_1d(31,-2.,left,right)
        axes[1].plot(x,q,label=name,lw=1.2)
    axes[1].plot(x,1+x*x,"k--",label="manufactured 1+x^2",lw=1)
    axes[1].set(xlabel="x",ylabel="u",title="Same Poisson solution | three boundary sets")
    axes[1].legend(fontsize=7)
    fig.tight_layout()
    save(fig,"diffusion-boundaries")

    fig,axes=plt.subplots(1,2,figsize=(10,3.8))
    n=63
    f=np.ones((n,n))
    mg,res=solve_poisson_multigrid(f)
    q=np.zeros_like(f)
    relaxation=[float(np.linalg.norm(f))]
    for _ in range(len(res)-1):
        q=red_black_gauss_seidel(q,f,1/(n+1),6)
        relaxation.append(float(np.linalg.norm(f-laplacian_operator(q,1/(n+1)))))
    axes[0].semilogy(np.asarray(res)/res[0],"o-",label="V-cycle (3+3 sweeps per level)")
    axes[0].semilogy(np.asarray(relaxation)/res[0],"o-",label="6 finest-grid RBGS sweeps")
    axes[0].set(xlabel="cycle/group (work not identical)",ylabel="relative residual 2-norm",title="Poisson | 63 x 63 interior points")
    axes[0].legend(fontsize=7)
    metrics["multigrid"]={"n":n,"cycles":len(res)-1,"final_relative_residual":float(res[-1]/res[0]),"residual_history":res.tolist()}
    a=2*np.eye(20)-np.eye(20,k=1)-np.eye(20,k=-1)
    omega=np.linspace(.1,1.95,100)
    axes[1].plot(omega,[spectral_radius(iteration_matrix(a,"sor",w)) for w in omega],label="SOR")
    axes[1].axhline(spectral_radius(iteration_matrix(a,"jacobi")),ls="--",label="Jacobi")
    axes[1].axhline(spectral_radius(iteration_matrix(a,"gauss-seidel")),ls=":",label="Gauss–Seidel")
    axes[1].set(xlabel="relaxation omega",ylabel="spectral radius rho(T)",title="1D Poisson | 20 unknowns")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    save(fig,"multigrid-radius")

    fig,ax=plt.subplots(figsize=(7,3.8))
    for damping in (0.,.18):
        r=solve_orszag_tang(32,.2,"glm",damping=damping,magnetic_error=.01)
        ax.plot(r.history[:,0],r.history[:,1],label=f"GLM, damping={damping}")
    ax.set(xlabel="time",ylabel="max |central div B|",title="GLM diagnostic | OT + longitudinal B error | N=32")
    ax.legend()
    save(fig,"glm-cleaning")
    _write_json(out/"validation.json",{**_metadata(),"settings":{"euler_cfl":.3,"mhd_cfl":.3,
                 "dg_cfl":.2,"mhd_ch":3.,"mhd_damping":.18},"metrics":metrics})
    print(out.resolve())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command",required=True)
    run = sub.add_parser("run")
    run.add_argument("problem",choices=(*list_problems(),"orszag-tang","double-mach"))
    run.add_argument("--n",type=int,default=200)
    run.add_argument("--method",choices=("godunov","muscl","weno5","ct","glm"))
    run.add_argument("--riemann",choices=("rusanov","hll","hlle","hllc","roe"))
    run.add_argument("--cfl",type=float,default=.3)
    run.add_argument("--limiter",choices=LIMITERS,default="minmod",help="1D MUSCL slope limiter (default: minmod)")
    run.add_argument("--time",type=float)
    run.add_argument("--output",default="outputs/run")
    gallery = sub.add_parser("gallery")
    gallery.add_argument("--output",default="outputs/gallery")
    args = parser.parse_args()
    if args.command == "gallery":
        build_gallery(args.output)
    else:
        run_case(args)


if __name__ == "__main__":
    main()
