import numpy as np, subprocess
from PIL import Image
W,H=1920,1080
img=np.full((H,W,3),128,np.uint8)
specs=[(200,1),(400,2),(600,3),(800,4)]
for x,w in specs:
    img[:,x:x+w]=(230,30,30)            # saturated red line
for x,w in specs:
    img[:,x+1000:x+1000+w]=(10,10,10)   # near-black line (luma only)
Image.fromarray(img).save('lines.png')
subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i','lines.png','-t','1','-r','24','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','lines.mp4'],check=True)
raw=subprocess.run(['ffmpeg','-v','error','-i','lines.mp4','-frames:v','1','-vf','format=rgb24','-f','rawvideo','-'],capture_output=True,check=True).stdout
dec=np.frombuffer(raw,np.uint8).reshape(H,W,3).astype(float)
row=slice(300,700)
def retention(x,w,orig_rgb):
    bg=128.0
    # contrast = max abs deviation from background across the 3 channels along the line's centre vs original
    cx=x+w//2
    got=np.abs(dec[row,x:x+w].mean(axis=(0,1))-bg).max()
    want=np.abs(np.array(orig_rgb,float)-bg).max()
    return got/want
print('width_px  red-line contrast kept  black-line contrast kept   (1920x1080, H.264 crf18, yuv420p)')
for (x,w) in specs:
    print(f'{w:8d}  {retention(x,w,(230,30,30)):20.0%}  {retention(x+1000,w,(10,10,10)):22.0%}')
