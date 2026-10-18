# numpy port of EffectCraft 0.12.0 crates/effects/src/noise.rs (Add Grain) and generate.rs (value_noise, lattice, fade)
# Written from reading the source; NOT the EffectCraft binary. Gaussian = scipy gaussian_filter (EffectCraft uses 3 box blurs).
import numpy as np
def gaussian_filter(a,sigma):
    sy,sx=sigma
    h,w=a.shape
    fy=np.fft.fftfreq(h)[:,None]; fx=np.fft.rfftfreq(w)[None,:]
    H=np.exp(-2*np.pi**2*((sy*fy)**2+(sx*fx)**2))
    return np.fft.irfft2(np.fft.rfft2(a)*H,s=a.shape).astype(np.float32)
M=np.uint32
def lattice(ix,iy,iz,seed):
    ix=ix.astype(np.int64).astype(np.uint32); iy=np.asarray(iy).astype(np.int64).astype(np.uint32); iz=np.asarray(iz).astype(np.int64).astype(np.uint32)
    with np.errstate(over='ignore'):
        h=(ix*M(0x27d4eb2d))^(iy*M(0x165667b1))^(iz*M(0x9e3779b9))^(M(seed)*M(0x85ebca6b))
        h^=h>>M(15); h=h*M(0x2c1b3c6d); h^=h>>M(12); h=h*M(0x297a2d39); h^=h>>M(15)
    return (h&M(0xffff)).astype(np.float32)/65535.0
def fade(t): return t*t*t*(t*(t*6.0-15.0)+10.0)
def value_noise(x,y,z,seed):
    x0=np.floor(x); y0=np.floor(y); z0=np.floor(z)
    fx=fade(x-x0); fy=fade(y-y0); fz=fade(np.float32(z-z0))
    ix=x0.astype(np.int64); iy=y0.astype(np.int64); iz=int(z0)
    def c(dx,dy,dz): return lattice(ix+dx,iy+dy,np.full_like(ix,iz+dz),seed)
    l=lambda a,b,t:a+(b-a)*t
    a=l(l(c(0,0,0),c(1,0,0),fx),l(c(0,1,0),c(1,1,0),fx),fy)
    if fz==0: return a
    b=l(l(c(0,0,1),c(1,0,1),fx),l(c(0,1,1),c(1,1,1),fx),fy)
    return l(a,b,fz)
PRESETS={0:None,1:(0.6,0.7,0.2,0.6,False),2:(1.3,1.8,0.4,0.8,False),3:(1.8,2.5,0.8,0.5,False),4:(1.0,0.6,0.0,1.0,False),5:(1.6,1.4,0.3,1.0,True)}
def add_grain(img, t, fps_ignored=None, preset=0, intensity=1.0, size=1.0, softness=0.0, aspect=1.0, mono=False, sat=1.0, speed=1.0, smooth=True, seed_param=0, ctx_seed=3, scale=1.0):
    h,w=img.shape[:2]
    ft=t*24.0*speed
    frame=ft if (smooth and ft-np.floor(ft)!=0.0) else np.floor(ft)
    ki,ks,soft,ksat,pm=(1,1,0,1,False) if PRESETS[preset] is None else PRESETS[preset]
    intensity*=ki; size=max(size,0.05)*ks; softness+=soft; sat*=ksat; mono=mono or pm
    seed=(seed_param ^ ((ctx_seed*0x9e37)&0xffffffff))&0xffffffff
    s=max(size*scale,0.05)
    ys,xs=np.mgrid[0:h,0:w].astype(np.float32)
    nch=1 if mono else 3
    planes=[]
    for k in range(nch):
        pl=value_noise(xs/(s*aspect),ys/s,np.float32(frame),(seed+k*101)&0xffffffff)-0.5
        sf=softness*scale
        if sf>0.05: pl=gaussian_filter(pl,sigma=(sf,sf*aspect))
        planes.append(pl.astype(np.float32))
    amp=intensity*0.25
    out=np.empty((h,w,3),np.float32)
    lum=0.2126*img[...,0]+0.7152*img[...,1]+0.0722*img[...,2]
    for k in range(3):
        g=planes[0] if mono else planes[k]
        out[...,k]=g
    if not mono:
        gm=out.mean(axis=2,keepdims=True); out=gm+(out-gm)*sat
    res=np.empty_like(out)
    for k in range(3):
        c=img[...,k]
        res[...,k]=np.maximum(c+out[...,k]*amp*(1.0-0.5*c),0.0)  # Film blend (default), weight=1 at default tones
    return res
