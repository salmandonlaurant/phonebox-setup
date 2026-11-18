import io
p = r"C:\Users\Admin\Projects\drift-tool\static\i18n.js"
s = io.open(p, encoding="utf-8").read()

# Greek block: insert after paste_cols line (Greek)
old_el = "    paste_cols: '— στήλες: Όροφος, u, προαιρετικά h',\n"
new_el = ("    paste_cols: '— στήλες: Όροφος, u, προαιρετικά h',\n"
          "    paste_help_html: 'Επικόλληση από Excel/SAP με Tab ή κενά. Αν λείπουν ύψη, συμπληρώνονται από τον πίνακα υψών του μοντέλου. Τα κενά <b>δεν</b> αντικαθίστανται με μηδέν.',\n"
          "    paste_table_hint: 'Συμβουλή: επικολλήστε (Ctrl+V) ένα μπλοκ από Excel/SAP απευθείας στον πίνακα.',\n")
assert old_el in s, "el anchor not found"
s = s.replace(old_el, new_el, 1)

# English block
old_en = "    paste_cols: '— columns: storey, u, optional h',\n"
new_en = ("    paste_cols: '— columns: storey, u, optional h',\n"
          "    paste_help_html: 'Paste from Excel/SAP with Tab or spaces. Missing heights are filled from the model height table. Empty cells are <b>never</b> replaced with zero.',\n"
          "    paste_table_hint: 'Tip: paste (Ctrl+V) an Excel/SAP block directly into the table.',\n")
assert old_en in s, "en anchor not found"
s = s.replace(old_en, new_en, 1)

io.open(p, "w", encoding="utf-8").write(s)
print("done")
