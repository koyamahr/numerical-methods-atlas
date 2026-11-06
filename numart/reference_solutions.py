"""Reference solution catalog with explicit field and averaging conventions.

No PDE discretization is advanced here. Formula evaluation, bracketed wave
matching and finite-order quadrature have distinct, inspectable tolerances.
"""
from dataclasses import dataclass, field
from functools import lru_cache
from itertools import product
from typing import Callable, Optional

import numpy as np

from .reference_riemann import RiemannSolution
from .scalar_gallery import riemann as scalar_riemann


@lru_cache(None)
def _gauss(order):
    if not isinstance(order,int) or not 1 <= order <= 256:
        raise ValueError('Quadrature order must be an integer from 1 to 256')
    return np.polynomial.legendre.leggauss(order)


@dataclass(frozen=True)
class ReferenceSolution:
    id: str
    title: str
    model: str
    kind: str
    components: tuple
    bounds: tuple
    final_time: float
    formula: str
    assumptions: str
    sources: tuple
    evaluator: Callable = field(repr=False)
    fronts: Callable = field(default=lambda t: (),repr=False)
    forcing: Optional[Callable] = field(default=None,repr=False)
    parameters: dict = field(default_factory=dict)
    diagnostics: dict = field(default_factory=dict)
    field_type: str = 'conserved'

    @property
    def dimension(self): return len(self.bounds)

    def point(self,x,t=0.):
        x=np.asarray(x,dtype=float)
        if not np.all(np.isfinite(x)) or not np.isfinite(t) or t<0:
            raise ValueError('Coordinates and time must be finite; time must be nonnegative')
        if self.dimension>1 and (x.ndim==0 or x.shape[-1]!=self.dimension):
            raise ValueError('Multidimensional coordinates need a last coordinate axis')
        result=np.asarray(self.evaluator(x,float(t)),dtype=float)
        expected=x.shape+(len(self.components),) if self.dimension==1 else x.shape[:-1]+(len(self.components),)
        if result.shape!=expected or not np.all(np.isfinite(result)):
            raise ArithmeticError('Reference returned invalid shape or nonfinite values')
        return result

    def source(self,x,t=0.):
        self.point(x,t)  # Apply the same coordinate/time validation.
        if self.forcing is None: raise ValueError('No source term is specified for this reference')
        return np.asarray(self.forcing(np.asarray(x,dtype=float),float(t)))

    def cell_average(self,edges,t=0.,order=24):
        """1D component means: split at all known fronts, then Gauss integrate.

        For systems these are means of CONSERVED variables, never the primitive
        variables of point values. Finite-order quadrature is not exact arithmetic.
        """
        if self.dimension!=1: raise ValueError('Use box_average for multidimensional cells')
        edges=np.asarray(edges,dtype=float)
        if edges.ndim!=1 or len(edges)<2 or not np.all(np.isfinite(edges)) or np.any(np.diff(edges)<=0):
            raise ValueError('Edges must be a finite, strictly increasing 1D vector')
        self.point(edges[:1],t)
        nodes,weights=_gauss(order)
        fronts=np.asarray(self.fronts(float(t)),dtype=float)
        result=[]
        for a,b in zip(edges[:-1],edges[1:]):
            cuts=np.unique(np.r_[a,fronts[(fronts>a)&(fronts<b)],b])
            integral=np.zeros(len(self.components))
            for lo,hi in zip(cuts[:-1],cuts[1:]):
                points=(lo+hi)/2+(hi-lo)*nodes/2
                integral+=(hi-lo)/2*np.einsum('i,ij->j',weights,self.point(points,t))
            result.append(integral/(b-a))
        return np.array(result)

    def cell_average_report(self,edges,t=0.,order=24):
        low=self.cell_average(edges,t,order)
        high=self.cell_average(edges,t,2*order)
        return dict(values=high,order=2*order,comparison_order=order,
                    max_order_difference=np.max(abs(high-low),axis=0),
                    convention='Known-front split Gauss quadrature of the listed components; order difference is an estimate, not a rigorous error bound.')

    def box_average(self,lower,upper,t=0.,order=12):
        """One axis-aligned multidimensional box; smooth reference fields only."""
        lower,upper=np.asarray(lower,dtype=float),np.asarray(upper,dtype=float)
        if lower.shape!=(self.dimension,) or upper.shape!=lower.shape or not np.all(np.isfinite([lower,upper])) or np.any(upper<=lower):
            raise ValueError('Box limits must be finite coordinate vectors with positive widths')
        if self.dimension==1: return self.cell_average([lower[0],upper[0]],t,order)[0]
        nodes,weights=_gauss(order)
        indices=np.array(list(product(range(order),repeat=self.dimension)))
        points=(lower+upper)/2+(upper-lower)*nodes[indices]/2
        values=self.point(points,t)
        tensor_weights=np.prod(weights[indices]/2,axis=1)
        return np.einsum('i,ij->j',tensor_weights,values)

    def compare_means(self,computed,edges,t=0.,order=24):
        reference=self.cell_average_report(edges,t,order)
        q=np.asarray(computed,dtype=float)
        if q.shape!=reference['values'].shape or not np.all(np.isfinite(q)):
            raise ValueError('Computed conserved means must match the reference shape and be finite')
        error=q-reference['values'];weights=np.diff(edges)/(edges[-1]-edges[0])
        return dict(l1=np.einsum('i,ij->j',weights,abs(error)),
                    l2=np.sqrt(np.einsum('i,ij->j',weights,error**2)),
                    linf=np.max(abs(error),axis=0),quadrature=reference)

    def metadata(self):
        return {k:getattr(self,k) for k in ('id','title','model','kind','components','bounds','final_time','formula','assumptions','sources','parameters','diagnostics','field_type')}


def riemann_reference(model,left,right,parameter=None,origin=.5,id='custom-riemann',title=None,bounds=(0.,1.),final_time=.1):
    parameter=(1.4 if model=='euler' else 1.) if parameter is None else parameter
    solution=RiemannSolution(model,left,right,parameter)
    if not np.isfinite(origin): raise ValueError('Origin must be finite')
    components=('rho','rho u','E') if model=='euler' else ('h','h u') if model=='shallow-water' else ('rho','rho u')
    source=('https://www.clawpack.org/riemann_book/html/Euler.html' if model=='euler' else
            'https://www.clawpack.org/riemann_book/html/Shallow_water.html' if model=='shallow-water' else
            'https://www.sfu.ca/~van/papers/Riemann-inv.pdf')
    return ReferenceSolution(id,title or model+' Riemann problem',model,
        'analytic' if solution.vacuum else 'semi-analytic',components,(tuple(bounds),),final_time,
        'U(x,t) = R((x−x0)/t)',
        ('Ideal gas; gamma>1; planar 1D waves; vacuum has zero conserved state and undefined velocity.' if model=='euler' else
         'Flat bottom; constant g; dry states allowed in the reference only, not the existing FV solver.' if model=='shallow-water' else
         'p = c_s² rho; constant c_s; strictly positive initial density; no vacuum state or energy equation.'),
        (source,),lambda x,t:solution.point(x,t,origin),
        lambda t:[origin] if t==0 else [origin+t*s for s in solution.speeds],
        parameters=dict(left=list(left),right=list(right),parameter=float(parameter),origin=origin),
        diagnostics=dict(solution.diagnostics,star=solution.star,star_velocity=solution.velocity,
                         vacuum=solution.vacuum,waves=solution.waves))


def _scalar_reference(id,equation,left,right,title):
    shock=left>right if equation=='burgers' else left<right
    speeds=[.5*(left+right) if equation=='burgers' else 1-left-right] if shock else ([left,right] if equation=='burgers' else [1-2*left,1-2*right])
    def point(x,t):
        q=np.where(x<.5,left,right) if t==0 else scalar_riemann((x-.5)/t,left,right,equation)
        return np.asarray(q)[...,None]
    return ReferenceSolution(id,title,equation,'analytic',('u' if equation=='burgers' else 'rho',),((0.,1.),),.4,
        'u_t + (u²/2)_x = 0' if equation=='burgers' else 'rho_t + [rho(1−rho)]_x = 0',
        'Entropy solution of a scalar whole-line Riemann problem; constant endpoint continuation.',
        ('https://www.clawpack.org/riemann_book/html/Burgers.html' if equation=='burgers' else 'https://www.clawpack.org/riemann_book/html/Traffic_flow.html',),
        point,lambda t:[.5+t*s for s in speeds],parameters=dict(left=left,right=right,origin=.5),field_type='scalar')


@lru_cache(None)
def _catalog():
    cases=[]
    for heat in (False,True):
        def point(x,t,heat=heat):
            return (1+.25*np.sin(2*np.pi*(x if heat else x-t))*np.exp(-.02*(2*np.pi)**2*t if heat else 0))[...,None]
        cases.append(ReferenceSolution('sine-heat' if heat else 'sine-advection',
            'Heat / Fourier-mode decay' if heat else 'Advection / sine translation',
            'heat' if heat else 'advection','analytic',('u',),((0.,1.),),1.,
            'u = 1 + 0.25 sin(2πx) exp[−0.02(2π)²t]' if heat else 'u = 1 + 0.25 sin[2π(x−t)]',
            'Periodic unit interval; viscosity 0.02.' if heat else 'Periodic unit interval; constant advection speed 1.',
            ('https://doi.org/10.1137/1.9780898717839',),point,field_type='scalar'))
    cases += [_scalar_reference('burgers-shock','burgers',1.,0.,'Burgers / shock'),
              _scalar_reference('burgers-fan','burgers',0.,1.,'Burgers / rarefaction'),
              _scalar_reference('traffic-jam','traffic',.3,.9,'Traffic / upstream shock'),
              _scalar_reference('traffic-fan','traffic',.9,.1,'Traffic / clearing fan')]
    for id,title,left,right,domain,origin,time in [
        ('euler-sod','Euler / Sod',(1.,0.,1.),(.125,0.,.1),(0.,1.),.5,.2),
        ('euler-lax','Euler / Lax',(.445,.698,3.528),(.5,0.,.571),(-5.,5.),0.,1.3),
        ('euler-double-rarefaction','Euler / double rarefaction',(1.,-2.,.4),(1.,2.,.4),(0.,1.),.5,.15),
        ('euler-vacuum','Euler / generated vacuum',(1.,-4.,.4),(1.,4.,.4),(0.,1.),.5,.05)]:
        cases.append(riemann_reference('euler',left,right,id=id,title=title,bounds=domain,origin=origin,final_time=time))
    cases += [riemann_reference('shallow-water',(2.,0.),(1.,0.),id='swe-dam-break',title='Shallow water / wet dam break'),
              riemann_reference('shallow-water',(1.,0.),(0.,0.),id='swe-dry-bed',title='Shallow water / dry-bed fan',final_time=.15),
              riemann_reference('shallow-water',(1.,-3.),(1.,3.),id='swe-vacuum',title='Shallow water / dry middle state',final_time=.1),
              riemann_reference('isothermal',(1.,0.),(.125,0.),id='isothermal-jump',title='Isothermal / density jump')]
    cases.append(ReferenceSolution('poisson-manufactured','Poisson / manufactured sine','poisson','manufactured',('u',),((0.,1.),),0.,
        'u = sin(πx); −u_xx = f = π² sin(πx)',
        'Zero Dirichlet endpoints. The forcing is chosen from the target solution; this is not an arbitrary-source Poisson solution.',
        ('https://doi.org/10.1137/1.9780898717839',),lambda x,t:np.sin(np.pi*x)[...,None],
        forcing=lambda x,t:(np.pi**2*np.sin(np.pi*x))[...,None],field_type='scalar'))
    for parabolic in (False,True):
        cases.append(ReferenceSolution('poiseuille' if parabolic else 'couette',
            'Viscous channel / Poiseuille' if parabolic else 'Viscous channel / Couette',
            'steady incompressible channel','analytic',('u',),((0.,1.),),0.,
            'u(y) = G y(1−y)/(2ν); G=1, ν=0.1' if parabolic else 'u(y) = y',
            'Fully developed planar steady channel, no slip, unit density; −dp/dx=G or body acceleration G.' if parabolic else
            'Fully developed planar steady channel; walls u(0)=0,u(1)=1; zero pressure gradient.',
            ('https://doi.org/10.1007/978-3-319-99693-6',),
            (lambda y,t:(5*y*(1-y))[...,None]) if parabolic else (lambda y,t:y[...,None]),field_type='velocity profile'))
    def tg(p,t):
        x,y=np.moveaxis(p,-1,0);decay=np.exp(-.2*t)
        return np.stack((np.sin(x)*np.cos(y)*decay,-np.cos(x)*np.sin(y)*decay,
                         .25*(np.cos(2*x)+np.cos(2*y))*decay**2),axis=-1)
    cases.append(ReferenceSolution('taylor-green','Viscous flow / 2D Taylor–Green','incompressible Navier–Stokes','analytic',
        ('u','v','p'),((0.,2*np.pi),(0.,2*np.pi)),.5,
        '(u,v)=(sin x cos y,−cos x sin y)e^(−2νt); p=(cos 2x+cos 2y)e^(−4νt)/4',
        'Periodic [0,2π]²; unit density; viscosity 0.1; zero mean pressure. Web profile is an x-slice at y=π/4.',
        ('https://doi.org/10.1090/S0025-5718-1968-0242392-2',),tg,parameters=dict(viscosity=.1),field_type='velocity and pressure'))
    return {c.id:c for c in cases}


def list_references(): return tuple(_catalog())


def get_reference(id):
    try: return _catalog()[id]
    except KeyError: raise ValueError('Unknown reference: '+str(id)) from None
