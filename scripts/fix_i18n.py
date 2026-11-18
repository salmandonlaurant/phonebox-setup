import io

p = r"C:\Users\Admin\Projects\drift-tool\static\i18n.js"
s = io.open(p, encoding="utf-8").read()
old = "    paste_clipboard: 'Επικόλληση από το πρόχειρο',\\n    paste_clipboard_title: 'Διαβάζει το πρόχειρο και γεμίζει τον πίνακα',"
new = "    paste_clipboard: 'Επικόλληση από το πρόχειρο',\n    paste_clipboard_title: 'Διαβάζει το πρόχειρο και γεμίζει τον πίνακα',"
assert old in s, "pattern not found"
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8").write(s)
print("fixed")
