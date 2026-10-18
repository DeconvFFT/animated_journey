import bpy,sys
p=sys.argv[-1]
bpy.ops.wm.open_mainfile(filepath=p)
s=bpy.context.scene
r=s.render; c=s.cycles
print("FILE",p)
print("blender",bpy.app.version_string)
print("res",r.resolution_x,r.resolution_y,r.resolution_percentage,"engine",r.engine)
print("samples",c.samples,"adaptive",c.use_adaptive_sampling,"adaptive_thr",c.adaptive_threshold,"min",c.adaptive_min_samples)
print("denoise render",c.use_denoising,"denoiser",getattr(c,'denoiser',None))
print("max_bounces",c.max_bounces,"diffuse",c.diffuse_bounces,"glossy",c.glossy_bounces,"trans",c.transmission_bounces,"vol",c.volume_bounces)
print("device",c.device,"frame",s.frame_current,"film_transparent",r.film_transparent)
print("objects",len(s.objects),"mesh tris approx:")
dg=bpy.context.evaluated_depsgraph_get()
tris=0
for o in s.objects:
    if o.type=='MESH':
        eo=o.evaluated_get(dg)
        try:
            m=eo.to_mesh(); m.calc_loop_triangles(); tris+=len(m.loop_triangles); eo.to_mesh_clear()
        except Exception as e: pass
print("triangles",tris)
