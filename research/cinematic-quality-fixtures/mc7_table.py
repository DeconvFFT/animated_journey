import json,glob,sys,collections
rows=[]
for f in sorted(glob.glob(sys.argv[1])):
    rows+= [json.loads(l) for l in open(f)]
d=collections.defaultdict(dict)
for r in rows:
    key=(r['print'][:2],r['src'],r['method'])
    tag=('orig' if r['scale']=='orig240' else f"{r['codec']}{r['scale']}")
    d[key][tag]=r
print(f"{'print':5s}{'src':5s}{'method':11s}{'orig240':>9s}{'LK raw':>8s}{'LK h264':>9s}{'txjit':>7s}{'tyjit':>7s}{'bytes':>9s}")
for k in sorted(d):
    v=d[k]; g=lambda t,f='rough': v[t][f] if t in v else float('nan')
    print(f"{k[0]:5s}{k[1]:5s}{k[2]:11s}{g('orig'):9.3f}{g('raw4'):8.3f}{g('h2644'):9.3f}{g('raw4','tx_jit_px1080'):7.3f}{g('raw4','ty_jit_px1080'):7.3f}{v.get('orig',{}).get('bytes_h264',0):9d}")
