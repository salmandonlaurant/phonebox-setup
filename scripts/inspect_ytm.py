import json
c = json.load(open(r"C:\Users\Admin\AppData\Roaming\PhoneBox\config.json", encoding="utf-8"))
ytm = [s for s in c["shortcuts"] if s.get("id", "").startswith("ytm-")]
print("YT_SHORTCUT_COUNT:", len(ytm))
for s in ytm[:3]:
    print("SHORTCUT:", json.dumps(s, ensure_ascii=False))
print("LAST:", json.dumps(ytm[-1], ensure_ascii=False))
for p in c["pages"]:
    for w in p["widgets"]:
        if w.get("id") == "ytm-picker":
            html = w["options"].get("html", "")
            print("PICKER_PAGE:", p["id"], "HTML_LEN:", len(html))
            print("HTML_HEAD:", html[:3500])
            print("HTML_TAIL:", html[-1500:])
