import io
p = r"C:\Users\Admin\Projects\drift-tool\static\app.js"
s = io.open(p, encoding="utf-8").read()
old = r"  if (!/[\\t\\n]/.test(text)) return;"
new = "  if (!/[\\t\\n]/.test(text)) return;".replace("\\\\t","\\t").replace("\\\\n","\\n")
# simpler: target literal double-backslash
old2 = "  if (!/[\\\\t\\\\n]/.test(text)) return;"
new2 = "  if (!/[\\t\\n]/.test(text)) return;"
assert old2 in s, "not found"
s = s.replace(old2, new2)
io.open(p, "w", encoding="utf-8").write(s)
print("done")
