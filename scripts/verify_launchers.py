import json, urllib.request
c = json.load(open(r'C:\Users\Admin\AppData\Roaming\PhoneBox\config.json', encoding='utf-8'))
p = [x for x in c['pages'] if x['id'] == 'system'][0]
print('system:', [(w['id'], w['x'], w['y'], w['w'], w['h']) for w in p['widgets']])
g = [w for w in p['widgets'] if w['id'] == 'liquid-glass'][0]
print('glass panels:', g['options']['html'].count('class="g"'))
print('launcher options:', [w['options'] for w in p['widgets'] if w['id'] == 'launchers'])
print('launcher shortcuts:', [(s['id'], s['label']) for s in c['shortcuts'] if s['id'].startswith('launcher-')])
i = json.load(urllib.request.urlopen('http://127.0.0.1:8765/api/info', timeout=15))
print('connected:', i['connected'], 'via', i['via'])
