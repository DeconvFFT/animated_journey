import bpy,sys,time,os
p=sys.argv[-1]
bpy.ops.wm.open_mainfile(filepath=p)
s=bpy.context.scene
s.render.engine='CYCLES'
c=s.cycles
c.device='CPU'
c.use_adaptive_sampling=False
s.render.resolution_x=1920; s.render.resolution_y=1080; s.render.resolution_percentage=100
s.render.threads_mode='AUTO'
s.render.filepath='/tmp/claude-0/-home-user/8016b042-43ae-5ade-a7e4-661ffdf4579d/scratchpad/out_'
for n,den in [(8,False),(24,False),(24,True)]:
    c.samples=n; c.use_denoising=den
    t=time.time(); bpy.ops.render.render(write_still=False); dt=time.time()-t
    print(f"RESULT samples={n} denoise={den} wall_s={dt:.2f}",flush=True)
