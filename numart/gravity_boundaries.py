"""FFT convolution laboratories: isolated 3D and horizontally periodic slabs.

Distinct kernels and gauges. Slab kernel includes the horizontal zero mode.
The sampled-kernel DFT and continuum Fourier coefficient are separate options.
"""
import numpy as np


def isolated_potential(rho,spacing=1.,self_kernel=0.):
    """Doubled-domain Hockney–Eastwood convolution, G=1, kernel -1/r.

    rho is a rectangular 3D grid. spacing is scalar or (dx,dy,dz).
    The singular origin is assigned self_kernel explicitly (default zero).
    This is exact for that discrete quadrature, not a cell-integrated kernel.
    """
    rho=np.asarray(rho,dtype=float);h=np.broadcast_to(np.asarray(spacing,dtype=float),(3,))
    if rho.ndim!=3 or min(rho.shape)<2 or not np.all(np.isfinite(rho)) or not np.all(np.isfinite(h)) or np.any(h<=0) or not np.isfinite(self_kernel):
        raise ValueError('Require finite 3D density, positive spacing and finite self kernel')
    doubled=tuple(2*n for n in rho.shape)
    displacement=[np.where(np.arange(2*n)<n,np.arange(2*n),np.arange(2*n)-2*n)*d for n,d in zip(rho.shape,h)]
    mesh=np.meshgrid(*displacement,indexing='ij');radius=np.sqrt(sum(v*v for v in mesh))
    kernel=np.zeros(doubled);np.divide(-1.,radius,out=kernel,where=radius>0);kernel[0,0,0]=self_kernel
    source=np.zeros(doubled);physical=tuple(slice(0,n) for n in rho.shape);source[physical]=rho
    potential=np.fft.ifftn(np.fft.fftn(source)*np.fft.fftn(kernel)).real*np.prod(h)
    return potential[physical]


def slab_green_transform(horizontal_k,nz,length,representation='sampled'):
    """Fourier multiplier for G_k(z), with all gravitational factors included.

    Returns shape k.shape+(2*nz,). Sampled = dz*DFT of the physical kernel.
    Continuum = integral from -L to L against exp(-i*pi*ell*z/L).
    Global zero coefficient is 2*pi*L^2 in both conventions, fixing a gauge.
    """
    k=np.asarray(horizontal_k,dtype=float)
    if not isinstance(nz,int) or nz<2 or not np.isfinite(length) or length<=0 or np.any(k<0) or not np.all(np.isfinite(k)):
        raise ValueError('Require k>=0, integer nz>=2 and positive length')
    ell=np.arange(2*nz);kz=2*np.pi*np.fft.fftfreq(2*nz,d=length/nz)
    if representation=='sampled':
        lag=np.where(ell<nz,ell,ell-2*nz)*length/nz
        decaying=np.exp(-k[...,None]*abs(lag))
        kernel=np.zeros_like(decaying)
        np.divide(-2*np.pi*decaying,k[...,None],out=kernel,where=k[...,None]>0)
        kernel=np.where((k==0)[...,None],2*np.pi*abs(lag),kernel)
        return np.fft.fft(kernel,axis=-1)*(length/nz)
    if representation=='continuum':
        denominator=k[...,None]**2+kz*kz
        numerator=-4*np.pi*(1-(-1.)**ell*np.exp(-k[...,None]*length))
        multiplier=np.zeros_like(denominator)
        np.divide(numerator,denominator,out=multiplier,where=denominator>0)
        return np.where(denominator==0,2*np.pi*length**2,multiplier)
    raise ValueError('Use sampled or continuum kernel representation')


def slab_potential(rho,lengths=(1.,1.,1.),representation='sampled'):
    """Periodic x/y, vacuum outside finite z support; G=1.

    Double z only. No mean-density subtraction. No shear-periodic remapping.
    """
    rho=np.asarray(rho,dtype=float);lengths=np.asarray(lengths,dtype=float)
    if rho.ndim!=3 or min(rho.shape)<2 or lengths.shape!=(3,) or np.any(lengths<=0) or not np.all(np.isfinite(lengths)) or not np.all(np.isfinite(rho)):
        raise ValueError('Require finite 3D density and positive 3D lengths')
    nx,ny,nz=rho.shape;lx,ly,lz=lengths
    kx=2*np.pi*np.fft.fftfreq(nx,d=lx/nx);ky=2*np.pi*np.fft.fftfreq(ny,d=ly/ny)
    k=np.sqrt(kx[:,None]**2+ky[None,:]**2)
    source=np.zeros((nx,ny,2*nz),dtype=complex)
    source[:,:,:nz]=np.fft.fftn(rho,axes=(0,1))
    multiplier=slab_green_transform(k,nz,lz,representation)
    transformed=np.fft.fft(source,axis=-1)*multiplier
    return np.fft.ifftn(transformed,axes=(0,1,2)).real[:,:,:nz]
