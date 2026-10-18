"""Summarise pan_ease_validate.py output.  python3 -I pan_ease_table.py A.jsonl B.jsonl ...
Prints, per treatment: clips, exact template right, family right, axis right, low_confidence flagged, feature-rule family right, mean |total px error|,
then the misses one per line (truth -> answer, rmse, margin, flags)."""
import sys, json, collections
rows = [json.loads(l) for f in sys.argv[1:] for l in open(f) if l.strip()]
by = collections.OrderedDict()
for r in rows: by.setdefault(r["treat"], []).append(r)
print(f"{'treatment':12s} {'clips':>5s} {'template':>9s} {'family':>7s} {'axis':>5s} {'lowconf':>8s} {'feat.fam':>8s} {'|dtotal| px':>11s} {'hold ok':>8s}")
for t, rs in by.items():
    n = len(rs); ok = lambda k: sum(1 for r in rs if r[k])
    fam_feat = sum(1 for r in rs if r.get("feature_family") == r["truth_family"])
    dtot = [abs((r["est_total_px"] or 0) - r["truth_total_px"]) for r in rs if r.get("est_total_px") is not None]
    holds = [r for r in rs if r["truth_hold_lead"] or r["truth_hold_trail"]]
    hold_ok = sum(1 for r in holds if abs((r["est_hold_lead"] or 0) - r["truth_hold_lead"]) <= 0.06 and abs((r["est_hold_trail"] or 0) - r["truth_hold_trail"]) <= 0.06)
    print(f"{t:12s} {n:5d} {ok('class_ok'):4d}/{n:<4d} {ok('family_ok'):3d}/{n:<3d} {ok('axis_ok'):2d}/{n:<2d} {ok('low_confidence'):4d}/{n:<3d} {fam_feat:3d}/{n:<4d} {sum(dtot)/max(len(dtot),1):11.1f} {hold_ok:3d}/{len(holds):<4d}")
print("\nmisses (family wrong, or template wrong):")
for r in rows:
    if not r["family_ok"] or not r["class_ok"]:
        print(f"  {r['treat']:10s} {r['truth']:22s} -> {str(r['est']):18s} fam {r['truth_family']}->{r['est_family']}  rmse {r['rmse']}  margin {r['margin_other_family']}  agree {r['agree']}  lowconf {r['low_confidence']}  twos {r['twos_detected']}")
