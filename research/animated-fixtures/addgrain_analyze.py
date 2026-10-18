import numpy as np, sys
sys.path.insert(0,".")
import addgrain_port as grain
def luma(a): return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
def acorr_x(d):
    # autocorrelation along x averaged over rows via FFT
    h,w=d.shape
    f=np.fft.rfft(d,n=2*w,axis=1)
    ac=np.fft.irfft(f*np.conj(f),axis=1)[:, :w].mean(axis=0)
    return ac/ac[0]
def widths(ac):
    half=int(np.argmax(ac<0.5)); e=int(np.argmax(ac<np.exp(-1)))
    return half,e
def corr(a,b):
    a=a-a.mean(); b=b-b.mean(); return float((a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum()))
names={0:'None(defaults)',1:'Fine 35mm',2:'Coarse 16mm',3:'Vintage 8mm',4:'Video Noise',5:'Mono High Speed'}
print('--- spatial, 2048x1080, mid grey 0.45, t=0')
img=np.full((1080,2048,3),0.45,np.float32)
for p in range(6):
    r=grain.add_grain(img,0.0,preset=p)
    d=r-0.45; L=luma(d)
    ac=acorr_x(L); hw,e=widths(ac)
    chroma=(d-L[...,None]).std()
    print(f'{names[p]:18s} std/ch={d.std()*255:5.2f} lv  luma std={L.std()*255:5.2f} lv  chroma std={chroma*255:4.2f} lv  acorr half-width={hw}px  1/e={e}px  = {hw/2048*100:.3f}% of width')
print('--- tonal: Film blend, Fine 35mm preset=0 defaults, std in levels at different grey')
for g in (0.1,0.2,0.45,0.7,0.9):
    im=np.full((256,512,3),g,np.float32); r=grain.add_grain(im,0.0); print(g, round(float((r-g).std())*255,2))
print('--- same params at three timeline widths (defaults, Size=1): grain width as % of picture width')
for (w,h) in ((1920,1080),(2048,1080),(3840,2160)):
    im=np.full((h,w,3),0.45,np.float32); r=grain.add_grain(im,0.0,preset=3)
    ac=acorr_x(luma(r-0.45)); hw,e=widths(ac); print((w,h),'Vintage 8mm: half-width px',hw,'->',round(hw/w*100,3),'% of width')
print('--- compensated: Size scaled with width to match 2048 look (size=2048-relative)')
for (w,h) in ((1920,1080),(3840,2160)):
    im=np.full((h,w,3),0.45,np.float32); r=grain.add_grain(im,0.0,preset=3,size=w/2048,softness=0.0)
    ac=acorr_x(luma(r-0.45)); hw,e=widths(ac); print((w,h),'size=',round(w/2048,3),'half-width px',hw,'->',round(hw/w*100,3),'%')
print('--- temporal, 2048x1080 Fine 35mm preset, std and frame-to-frame correlation')
im=np.full((1080,2048,3),0.45,np.float32)
for fps in (24.0,25.0,30.0):
    fr=[grain.add_grain(im,k/fps,preset=0,size=3.0) for k in range(8)]
    stds=[round(float((f-0.45).std())*255,2) for f in fr]
    cs=[round(corr(luma(fr[k]),luma(fr[k+1])),2) for k in range(7)]
    print(fps,'fps  std per frame',stds); print('      consecutive-frame corr',cs)
print('--- temporal with Animate Smoothly off at 25 fps')
fr=[grain.add_grain(im,k/25.0,preset=0,size=3.0,smooth=False) for k in range(8)]
print([round(float((f-0.45).std())*255,2) for f in fr],[round(corr(luma(fr[k]),luma(fr[k+1])),2) for k in range(7)])
