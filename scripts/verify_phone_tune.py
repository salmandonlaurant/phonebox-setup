import json, urllib.request
c = json.load(open(r"C:\Users\Admin\AppData\Roaming\PhoneBox\config.json", encoding="utf-8"))
d = c["display"]
print("appearance:", d["appearance"])
print("orientation:", d["orientation"], "| theme:", d["theme"],
      "| keepAwake:", d["keepAwake"], "| idleDimMin:", d["idleDimMin"])
p = [x for x in c["pages"] if x["id"] == "ai"][0]
h = [w for w in p["widgets"] if w.get("id") == "ytm-picker"][0]["options"]["html"]
print("picker title 14px:", ".tt{font-size:14px" in h,
      "| thumbs 52px:", "width:52px;height:52px" in h,
      "| songs:", h.count('"v":'))
g = [w for w in p["widgets"] if w.get("id") == "liquid-glass"][0]["options"]["html"]
print("glass radius 22:", "border-radius:22px" in g, "| gap 8:", "gap:8px" in g)
i = json.load(urllib.request.urlopen("http://127.0.0.1:8765/api/info", timeout=15))
print("tablet:", i["connected"], i["via"])
