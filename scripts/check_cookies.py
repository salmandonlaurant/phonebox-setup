import sqlite3, os, shutil, tempfile

base = os.path.join(os.environ['LOCALAPPDATA'], 'BraveSoftware', 'Brave-Browser', 'User Data')
tmpdir = tempfile.gettempdir()
for prof in ['Default', 'Profile 1', 'Profile 2']:
    path = os.path.join(base, prof, 'Network', 'Cookies')
    if not os.path.exists(path):
        continue
    dst = os.path.join(tmpdir, 'ck_' + prof.replace(' ', '_') + '.db')
    shutil.copyfile(path, dst)
    con = sqlite3.connect(dst)
    rows = con.execute("select host_key, name, length(encrypted_value), substr(hex(encrypted_value),1,6) from cookies where host_key like '%youtube.com%' or host_key like '%google.com%' limit 12").fetchall()
    print('===', prof, '===', len(rows))
    for r in rows:
        print(r)
    con.close()
    os.remove(dst)
