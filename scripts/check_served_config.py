import json, urllib.request
d = json.load(urllib.request.urlopen('http://127.0.0.1:8765/api/config', timeout=15))
cfg = d.get('config', d)
pages = cfg.get('pages', [])
print('page count:', len(pages))
for i, p in enumerate(pages):
    if p.get('id') == 'system':
        print('system index:', i + 1, 'enabled:', p.get('enabled'))
        print('widgets:', [(w.get('id'), w.get('type'), w.get('x'), w.get('y'), w.get('w'), w.get('h')) for w in p.get('widgets', [])])
for s in cfg.get('shortcuts', []):
    if str(s.get('id', '')).startswith('launcher-'):
        print('served shortcut:', s)
