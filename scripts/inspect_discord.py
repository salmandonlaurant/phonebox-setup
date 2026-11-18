import json
c = json.load(open(r"C:\Users\Admin\AppData\Roaming\PhoneBox\config.json", encoding="utf-8"))
p = [x for x in c["pages"] if x["id"] == "work"][0]
print("WIDGETS:", [(w.get("id"), w.get("type"), w.get("x"), w.get("y"), w.get("w"), w.get("h")) for w in p["widgets"]])
for w in p["widgets"]:
    if w.get("id") == "discord-sfx":
        h = w["options"].get("html", "")
        print("SFX_HTML_LEN:", len(h))
        print("SFX_HEAD:", h[:5000])
        print("SFX_TAIL:", h[-1200:])
