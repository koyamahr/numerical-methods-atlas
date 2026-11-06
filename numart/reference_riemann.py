"""Independent reference evaluators, not numerical interface fluxes.

Ideal-gas Euler, flat-bottom shallow water and isothermal Euler. Wave curves
are analytic; non-vacuum star states use a bracketed logarithmic root solve.
See Toro (2009), the Clawpack Riemann book, and Bhat--Fetecau (2009).
"""
import numpy as np


def _log_root(function, seeds):
    lo, hi = float(np.log(min(seeds))), float(np.log(max(seeds)))
    for _ in range(360):
        if function(np.exp(lo)) <= 0: break
        lo -= 2.
        if lo < -700: raise ArithmeticError('Star state is below the supported float64 range')
    else: raise ArithmeticError('Could not bracket star state from below')
    for _ in range(360):
        if function(np.exp(hi)) >= 0: break
        hi += 2.
        if hi > 700: raise ArithmeticError('Star state is above the supported float64 range')
    else: raise ArithmeticError('Could not bracket star state from above')
    for iteration in range(160):
        mid = (lo+hi)/2
        value = function(np.exp(mid))
        if not np.isfinite(value): raise ArithmeticError('Nonfinite wave curve')
        if value == 0 or hi-lo < 2e-13: break
        if value > 0: hi = mid
        else: lo = mid
    else: raise ArithmeticError('Star root did not converge')
    root = float(np.exp(mid))
    return root, dict(iterations=iteration+1, log_bracket_width=hi-lo,
                      wave_residual=float(function(root)))


class RiemannSolution:
    """Primitive input; conserved output with components on the last axis.

    Euler input is (rho,u,p); other models take (depth/density,u). Zero depth
    and vacuum Euler states are supported, including vacuum generated between
    separating fans. Isothermal input must have strictly positive densities.
    """
    def __init__(self, model, left, right, parameter=1.4):
        if model not in ('euler', 'shallow-water', 'isothermal'):
            raise ValueError('Unknown reference model')
        self.model, self.parameter = model, float(parameter)
        self.left, self.right = np.array(left, dtype=float), np.array(right, dtype=float)
        size = 3 if model == 'euler' else 2
        if any(w.shape != (size,) or not np.all(np.isfinite(w)) for w in (self.left,self.right)):
            raise ValueError('States must be finite primitive vectors of the correct size')
        if not np.isfinite(parameter) or parameter <= (1 if model == 'euler' else 0):
            raise ValueError('Require gamma>1, gravity>0 or sound speed>0')
        for w in (self.left,self.right):
            if w[0] < 0 or (model == 'isothermal' and w[0] == 0):
                raise ValueError('Nonnegative depth/density required; isothermal excludes vacuum')
            if model == 'euler' and (w[2] < 0 or (w[0] == 0) != (w[2] == 0)):
                raise ValueError('Euler rho and p must both be positive, or both zero')
        self.sounds = [self._sound(w) for w in (self.left,self.right)]
        self.vacuum = bool(model != 'isothermal' and
                       (min(self.left[0],self.right[0]) == 0 or
                        self.right[1]-self.left[1] >= self._expansion()*sum(self.sounds)))
        self.diagnostics = dict(iterations=0, log_bracket_width=0., wave_residual=0.)
        self.star = self.velocity = None
        if not self.vacuum:
            seeds = [self.left[2],self.right[2]] if model == 'euler' else [self.left[0],self.right[0]]
            residual = lambda z: self._curve(z,self.left)+self._curve(z,self.right)+self.right[1]-self.left[1]
            self.star, self.diagnostics = _log_root(residual,seeds)
            self.velocity = float((self.left[1]+self.right[1]+self._curve(self.star,self.right)-self._curve(self.star,self.left))/2)
            scale = max(1., abs(self.left[1]),abs(self.right[1]),*self.sounds)
            if abs(self.diagnostics['wave_residual']) > 2e-10*scale:
                raise ArithmeticError('Star wave matching residual exceeds tolerance')
        self.waves = []
        for side,w,c in zip((-1,1),(self.left,self.right),self.sounds):
            if w[0] == 0: continue
            if self.vacuum:
                head,tail = w[1]+side*c, w[1]-side*self._expansion()*c
                self.waves.append(dict(family=side,kind='rarefaction',speeds=(float(head),float(tail))))
            elif self.star > (w[2] if model == 'euler' else w[0]):
                if model == 'euler':
                    speed = w[1]+side*c*np.sqrt((parameter+1)/(2*parameter)*self.star/w[2]+(parameter-1)/(2*parameter))
                elif model == 'shallow-water':
                    speed = w[1]+side*np.sqrt(.5*parameter*self.star*(self.star+w[0])/w[0])
                else: speed = w[1]+side*parameter*np.sqrt(self.star/w[0])
                self.waves.append(dict(family=side,kind='shock',speeds=(float(speed),)))
            else:
                cs = (c*(self.star/w[2])**((parameter-1)/(2*parameter)) if model == 'euler'
                      else np.sqrt(parameter*self.star) if model == 'shallow-water' else parameter)
                self.waves.append(dict(family=side,kind='rarefaction',speeds=(float(w[1]+side*c),float(self.velocity+side*cs))))
        if model == 'euler' and not self.vacuum:
            self.waves.append(dict(family=0,kind='contact',speeds=(self.velocity,)))

    def _expansion(self):
        return 2/(self.parameter-1) if self.model == 'euler' else 2.

    def _sound(self,w):
        if self.model == 'isothermal': return self.parameter
        if w[0] == 0: return 0.
        return float(np.sqrt(self.parameter*(w[2]/w[0] if self.model == 'euler' else w[0])))

    def _curve(self,z,w):
        r,u = w[:2]
        if self.model == 'euler':
            p,g,c = w[2],self.parameter,self._sound(w)
            if z > p: return (z-p)*np.sqrt(2/((g+1)*r)/(z+(g-1)/(g+1)*p))
            return 2*c/(g-1)*((z/p)**((g-1)/(2*g))-1)
        if self.model == 'shallow-water':
            if z > r: return (z-r)*np.sqrt(.5*self.parameter*(1/z+1/r))
            return 2*(np.sqrt(self.parameter*z)-self._sound(w))
        if z > r: return self.parameter*(z-r)/np.sqrt(z*r)
        return self.parameter*np.log(z/r)

    def conserved(self,w):
        w = np.asarray(w,dtype=float)
        r,u = w[...,0],w[...,1]
        values = [r,r*u]
        if self.model == 'euler': values.append(w[...,2]/(self.parameter-1)+.5*r*u*u)
        return np.stack(values,axis=-1)

    def primitive(self,q):
        q = np.asarray(q,dtype=float)
        r = q[...,0]
        u = np.divide(q[...,1],r,out=np.zeros_like(r),where=r>0)
        # Velocity in vacuum is undefined physically; zero is only a display convention.
        if self.model != 'euler': return np.stack((r,u),axis=-1)
        p = (self.parameter-1)*(q[...,2]-.5*r*u*u)
        return np.stack((r,u,p),axis=-1)

    def flux(self,q):
        w = self.primitive(q); r,u = w[...,0],w[...,1]
        p = w[...,2] if self.model == 'euler' else .5*self.parameter*r*r if self.model == 'shallow-water' else self.parameter**2*r
        values = [r*u,r*u*u+p]
        if self.model == 'euler': values.append(u*(q[...,2]+p))
        return np.stack(values,axis=-1)

    def _star_primitive(self,w):
        if self.model != 'euler': return np.array([self.star,self.velocity])
        ratio = self.star/w[2];beta = (self.parameter-1)/(self.parameter+1)
        density = w[0]*((ratio+beta)/(beta*ratio+1) if ratio>1 else ratio**(1/self.parameter))
        return np.array([density,self.velocity,self.star])

    def _fan(self,xi,w,side):
        c = self._sound(w)
        if self.model == 'euler':
            g = self.parameter
            u = 2/(g+1)*(xi+(g-1)*w[1]/2-side*c)
            ratio = np.maximum(0.,2/(g+1)*(c+side*(g-1)*(xi-w[1])/2)/c)
            return np.stack((w[0]*ratio**(2/(g-1)),u,w[2]*ratio**(2*g/(g-1))),axis=-1)
        if self.model == 'shallow-water':
            u = (w[1]-2*side*c+2*xi)/3
            sound = np.maximum(0.,(2*c+side*(xi-w[1]))/3)
            return np.stack((sound**2/self.parameter,u),axis=-1)
        u = xi-side*c
        return np.stack((w[0]*np.exp(side*(u-w[1])/c),u),axis=-1)

    @property
    def speeds(self):
        return sorted(set(s for wave in self.waves for s in wave['speeds']))

    def sample(self,xi):
        xi = np.asarray(xi,dtype=float)
        if not np.all(np.isfinite(xi)): raise ValueError('Similarity coordinates must be finite')
        q = np.zeros(xi.shape+(len(self.left),))
        for side,w in zip((-1,1),(self.left,self.right)):
            if w[0] == 0: continue
            wave = next(v for v in self.waves if v['family']==side)
            if not self.vacuum:
                mask = xi <= self.velocity if side == -1 else xi > self.velocity
                q[mask] = self.conserved(self._star_primitive(w))
            speed = wave['speeds'][0]
            outside = xi <= speed if side == -1 else xi >= speed
            q[outside] = self.conserved(w)
            if wave['kind']=='rarefaction':
                a,b = sorted(wave['speeds'])
                fan = (xi>a)&(xi<b)
                q[fan] = self.conserved(self._fan(xi[fan],w,side))
        return q

    def point(self,x,t,origin=.5):
        x = np.asarray(x,dtype=float)
        if not np.isfinite(t) or t < 0 or not np.all(np.isfinite(x)) or not np.isfinite(origin):
            raise ValueError('Require finite coordinates, origin and nonnegative finite time')
        if t == 0:
            return np.where((x<origin)[...,None],self.conserved(self.left),self.conserved(self.right))
        return self.sample((x-origin)/t)
