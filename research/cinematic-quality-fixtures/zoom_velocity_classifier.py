import os, subprocess, sys, math, numpy as np
from PIL import Image
W,H=240,135
def frames(path):
    raw=subprocess.run(["ffmpeg","-v","error","-i",path,"-vf",f"scale={W}:{H},format=gray","-f","rawvideo","-"],capture_output=True,check=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(-1,H,W).astype(np.float32)
def warp(a,s):
    im=Image.fromarray(a.astype(np.uint8)); cx,cy=W/2,H/2
    # output(x) = input(cx+(x-cx)/s)  -> zoom by s about centre
    return np.asarray(im.transform((W,H),Image.AFFINE,(1/s,0,cx-cx/s,0,1/s,cy-cy/s),Image.BILINEAR),dtype=np.float32)
cands=np.linspace(0.994,1.016,45)
def logzoom(a,b):
    # Lucas-Kanade style least-squares estimate of the small zoom between two frames (about the frame centre)
    ys,xs=np.mgrid[0:H,0:W].astype(np.float32); xs-=W/2; ys-=H/2
    gy,gx=np.gradient(a)
    g=xs*gx+ys*gy; d=b-a
    c=(slice(15,H-15),slice(20,W-20))
    return float((d[c]*g[c]).sum()/((g[c]**2).sum()+1e-9))   # ~ d(ln zoom) for small steps
def velocity(path):
    a=frames(path); v=np.array([logzoom(a[i],a[i+1]) for i in range(len(a)-1)])
    return v*(1 if v.sum()>=0 else -1)   # make the dominant direction positive
def drawings(v):
    # detect twos: every other step ~0
    ev,od=np.abs(v[0::2]).mean(),np.abs(v[1::2]).mean()
    twos=min(ev,od)/max(ev,od)<0.25 if max(ev,od)>0 else False
    if twos:
        k=0 if ev>od else 1
        return twos, v[k::2]
    return twos, v
def smooth(x,k=5):
    p=np.pad(x,(k//2,k//2),mode='edge'); return np.convolve(p,np.ones(k)/k,mode='valid')
def features(v):
    twos,d=drawings(v)
    d=smooth(d,5 if not twos else 3)
    m=np.abs(d).max(); t=d/m; n=len(t); a=max(2,int(0.12*n))
    return dict(frames=len(v)+1, twos=bool(twos),
        ends=round(float((abs(t[:a]).mean()+abs(t[-a:]).mean())/2),2),
        cv=round(float(t.std()/abs(t).mean()),2),
        peak=round(float(abs(t).argmax()/(n-1)),2),
        overshoot=bool((t<-0.15).any()))
def classify(f):
    if f['overshoot'] and f['peak']<0.4: return 'ease-out WITH overshoot+settle'
    if f['cv']<0.12: return 'LINEAR/uniform (flag)'
    if f['ends']<0.45 and 0.3<f['peak']<0.7: return 'ease in-out'
    if f['peak']<0.3: return 'ease-out (decelerate)'
    if f['peak']>0.7: return 'ease-in (accelerate)'
    return 'other'
def roughness(v,k=9):
    # MO8 (M): std of the residual from a k-frame moving mean, relative to mean speed (edge-padded mean)
    v=np.asarray(v,dtype=float); p=np.pad(v,(k//2,k//2),mode='edge')
    m=np.convolve(p,np.ones(k)/k,mode='valid')
    return float((v-m).std()/max(np.abs(v).mean(),1e-12))
if __name__=="__main__":
    # ZV_SIZE=1920x1080 runs the estimator at that frame size (the saved default is 240x135; the M-C7 numbers used 960x540 and 1920x1080)
    if os.environ.get("ZV_SIZE"):
        W,H=map(int,os.environ["ZV_SIZE"].lower().split("x"))
    for p in sys.argv[1:]:
        v=velocity(p); f=features(v); print(f"{p:16s}",f,"->",classify(f))
        print(f"{p:16s} roughness {roughness(v):.3f} (MO8, frame {W}x{H})")
