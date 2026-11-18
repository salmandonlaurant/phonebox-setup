import json, urllib.request
c = json.load(open(r'C:\Users\Admin\AppData\Roaming\PhoneBox\config.json', encoding='utf-8'))
ap = c['display']['appearance']
print('appearance:', {k: ap.get(k) for k in ('style','font','fontScale','radius','gap','padding','pagePadding')})
wall = [w for p in c['pages'] for w in p['widgets'] if w.get('id') == 'pc-wallpaper']
glass = [w for p in c['pages'] for w in p['widgets'] if w.get('id') == 'liquid-glass']
h = glass[0]['options']['html']
print('wallpaper widgets:', len(wall), '| glass overlays:', len(glass))
print('glass gap matches config:', ('gap:' + str(ap['gap']) + 'px') in h)
print('glass radius matches config:', ('border-radius:' + str(ap['radius']) + 'px') in h)
print('theme:', c['display'].get('theme'), '| keepAwake:', c['display'].get('keepAwake'), '| night:', c['night']['enabled'])
i = json.load(urllib.request.urlopen('http://127.0.0.1:8765/api/info', timeout=15))
print('tablet:', i['connected'], 'via', i['via'])
