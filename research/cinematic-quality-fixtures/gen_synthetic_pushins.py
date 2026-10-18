import math, subprocess, os, shutil, numpy as np
from PIL import Image
src=Image.open('still.png').convert('RGB').resize((1920,1080))
OW,OH=960,540
def zoom_frame(z):
    # sample a (1/z)-sized window centred, resampled to OWxOH with bicubic (sub-pixel)
    w,h=1920/z,1080/z; x0,y0=(1920-w)/2,(1080-h)/2
    return src.transform((OW,OH),Image.EXTENT,(x0,y0,x0+w,y0+h),Image.BICUBIC)
def render(name, f, twos=False, n=96):
    d=f'fr_{name}'; shutil.rmtree(d,ignore_errors=True); os.makedirs(d)
    for i in range(n):
        j = (i//2)*2 if twos else i
        zoom_frame(1+0.10*f(j/(n-1))).save(f'{d}/{i:03d}.png')
    subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',f'{d}/%03d.png','-c:v','libx264','-crf','14','-pix_fmt','yuv420p',f'{name}.mp4'],check=True)
    shutil.rmtree(d)
lin=lambda u:u
inout=lambda u:0.5-0.5*math.cos(math.pi*u)
out3=lambda u:1-(1-u)**3
def settle(u):  # ease-out with small overshoot then settle (back-out style)
    c1=1.2; c3=c1+1; return 1+c3*(u-1)**3+c1*(u-1)**2
smooth5=lambda u:6*u**5-15*u**4+10*u**3
for nm,f,t in [('p_lin',lin,False),('p_inout',inout,False),('p_out3',out3,False),('p_settle',settle,False),('p_lin_twos',lin,True),('p_inout_twos',inout,True)]:
    render(nm,f,t)
print('ok')
