import subprocess, os, numpy as np
def frame(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-frames:v','1','-vf','format=gray','-f','rawvideo','-'],capture_output=True,check=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(540,960).astype(np.float64)
x=np.arange(960)
print('noise_strength  file_KB(2s,crf18)  distinct-8bit-levels(single row)  largest-step(8px avgs, in 8-bit LSB; ideal 0.2)  residual-noise-std(8-bit LSB)')
for A in (0,4,8,16,32):
    a=frame(f'g{A}.mp4'); r=a[270]
    box=np.convolve(r,np.ones(16)/16,mode='valid')[::16]; step=np.abs(np.diff(box)).max()
    lowpass=np.convolve(a.mean(axis=0),np.ones(32)/32,mode='same')
    noise=(a[270]-np.convolve(r,np.ones(32)/32,mode='same'))[40:-40].std()
    print(f'{A:14d}  {os.path.getsize(f"g{A}.mp4")/1024:16.1f}  {len(np.unique(r)):30d}  {step/1:44.2f}  {noise:.2f}')
