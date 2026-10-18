import zipfile,json,sys,collections,statistics
z=zipfile.ZipFile(sys.argv[1])
name=[n for n in z.namelist() if n.endswith('.jsonl')][0]
g=collections.defaultdict(list)
with z.open(name) as f:
    for line in f:
        if b'NVIDIA GeForce RTX 4090"' not in line: continue
        d=json.loads(line)
        for r in d['data']:
            di=r.get('device_info',{})
            devs=[x['name'] for x in di.get('compute_devices',[])]
            if devs!=['NVIDIA GeForce RTX 4090'] or di.get('device_type')!='OPTIX': continue
            if not r['blender_version']['version'].startswith('5.2'): continue
            st=r['stats']
            if 'samples_per_minute' not in st: continue
            g[r['scene']['label']].append((st['samples_per_minute'],st['total_render_time']-st['time_for_samples'],st['total_render_time'],r['timestamp'][:10]))
res={'classroom':(1920,1080),'monster':(1024,1024),'junkshop':(2000,1000)}
print("scene n spm_med spm_p10 spm_p90 overhead_med_s")
tp={}
for sc,v in sorted(g.items()):
    spm=sorted(x[0] for x in v); n=len(v)
    med=statistics.median(spm)
    ov=statistics.median(x[1] for x in v)
    w,h=res[sc]
    tp[sc]=med/60*w*h/1e6   # MP*spp/s
    print(sc,n,round(med),round(spm[n//10]),round(spm[n*9//10]),round(ov,2),'MP*spp/s=%.1f'%tp[sc],'dates',min(x[3] for x in v),max(x[3] for x in v))
for name,(w,h) in [('1080p',(1920,1080)),('2K DCI',(2048,1080)),('4K UHD',(3840,2160))]:
    mp=w*h/1e6
    for N in (24,64,128,256,512):
        print(name,N,'spp:',{sc:round(N*mp/tp[sc],2) for sc in tp})
