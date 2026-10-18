import numpy as np, math
W,H=1998,1080
def load(p):
    a=np.fromfile(p,dtype='<u2').reshape(H,W,3)>>4
    return a
patch_rgb=[0x00,0x1a,0x40,0x80,0xbf,0xe6,0xff]
names=["0x00","0x1a","0x40","0x80","0xbf","0xe6","0xff"]
x0=39  # 1920 picture centred in 1998 container
def centre(i): return x0+int(213*i+106)
out={}
for tag,f in (("rec709 preset (gamma 2.2)","f709.raw"),("rec1886 preset (gamma 2.4)","f1886.raw")):
    a=load(f)
    ys=[]
    for i in range(7):
        x=centre(i); blk=a[400:700,x-30:x+30,:]
        ys.append(blk.reshape(-1,3).mean(axis=0))
    out[tag]=np.array(ys)
def expected(v,g):
    # limited-range: Y' signal = v (full range RGB converted to tv and back); linear = v**g ; DCP Y code
    lin=v**g
    return ((lin*48/52.37)**(1/2.6))*4095
print("patch   v     meas709(Y)  exp(g=2.2)  meas1886(Y)  exp(g=2.4)   ratio lin(2.2/2.4) measured  expected")
for i in range(7):
    v=patch_rgb[i]/255
    # video-range quantisation: (v*219+16) round to 10-bit then expand
    y10=round((16+219*v)*4); vq=(y10/4-16)/219
    vq=max(0,min(1,vq))
    m709=out["rec709 preset (gamma 2.2)"][i][1]; m1886=out["rec1886 preset (gamma 2.4)"][i][1]
    e22=expected(vq,2.2); e24=expected(vq,2.4)
    lin709=(m709/4095)**2.6; lin1886=(m1886/4095)**2.6
    r=(lin709/lin1886) if lin1886>0 else float('nan')
    er=(vq**2.2/vq**2.4) if vq>0 else float('nan')
    print(f"{names[i]}  {vq:5.3f}  {m709:9.1f}  {e22:9.1f}  {m1886:10.1f}  {e24:9.1f}   {r:7.3f}  {er:7.3f}")
print("XYZ at 0xff (709):", out["rec709 preset (gamma 2.2)"][6])
