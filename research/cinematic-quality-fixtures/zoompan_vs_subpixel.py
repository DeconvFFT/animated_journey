import math, subprocess, numpy as np
from PIL import Image
src=Image.open('still.png').convert('RGB').resize((3840,2160),Image.BICUBIC)
def clip_pil(path):
    p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-','-c:v','libx264','-crf','14','-pix_fmt','yuv420p',path],stdin=subprocess.PIPE)
    for i in range(96):
        u=i/95; z=1+0.04*(0.5-0.5*math.cos(math.pi*u)); w,h=3840/z,2160/z; x0,y0=(3840-w)/2,(2160-h)/2
        p.stdin.write(src.transform((1920,1080),Image.EXTENT,(x0,y0,x0+w,y0+h),Image.BICUBIC).tobytes())
    p.stdin.close(); p.wait()
clip_pil('pil_slow.mp4')
# zoompan from the same 4K source, piped in as a raw image via a single-frame loop
import io
buf=io.BytesIO(); src.save(buf,'BMP'); open('s4k.bmp','wb').write(buf.getvalue())
subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i','s4k.bmp','-vf',"zoompan=z='1+0.04*(0.5-0.5*cos(PI*on/95))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=24:d=96,format=yuv420p",'-t','4','-c:v','libx264','-crf','14','zp_slow.mp4'],check=True)
