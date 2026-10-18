# Compare two SVGs: which ids / data-* attributes / element kinds survived? (stdlib only)
import sys, re, xml.etree.ElementTree as ET
def scan(path):
    t = ET.parse(path).getroot(); out = {}
    for e in t.iter():
        tag = e.tag.split("}")[-1]; i = e.get("id")
        if i: out[i] = (tag, {k: v for k, v in e.attrib.items() if k.startswith("data-") and k != "data-name"})
    return out, t
a, ta = scan(sys.argv[1]); b, tb = scan(sys.argv[2])
# VectorCraft may rename ids it sanitises (spaces -> _, duplicates -> -2) and regenerates def ids (gradients, clips, masks, filters)
authored = {i for i, (tag, _) in a.items() if tag not in ("linearGradient", "radialGradient", "clipPath", "mask", "filter", "symbol", "stop")}
lost   = sorted(i for i in authored if i not in b)
moved  = sorted(i for i in authored if i in b and a[i][0] != b[i][0])
datalost = sorted(i for i in authored if i in b and any(b[i][1].get(k) != v for k, v in a[i][1].items()))
print("ids authored:", len(authored), "| lost:", lost or "none", "| element kind changed:", moved or "none", "| data-* changed:", datalost or "none")
print("root viewBox:", ta.get("viewBox"), "->", tb.get("viewBox"))
print("classes in output:", sorted(set(re.findall(r'class="([^"]+)"', open(sys.argv[2], encoding="utf8").read()))))
print("<style> kept verbatim:", "#sun { stroke" in open(sys.argv[2], encoding="utf8").read())
sys.exit(1 if lost or datalost else 0)
