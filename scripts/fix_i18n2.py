import io
p = r"C:\Users\Admin\Projects\drift-tool\static\i18n.js"
s = io.open(p, encoding="utf-8").read()
old = "    paste_clipboard: 'Paste from clipboard',\\n    paste_clipboard_title: 'Reads the clipboard and fills the table',"
new = "    paste_clipboard: 'Paste from clipboard',\n    paste_clipboard_title: 'Reads the clipboard and fills the table',"
assert old in s, "not found"
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8").write(s)
print("done")
