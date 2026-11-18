import json
c = json.load(open(r'C:\Users\Admin\AppData\Roaming\PhoneBox\config.json', encoding='utf-8'))
p = [x for x in c['pages'] if x['id'] == 'home'][0]
g = [w for w in p['widgets'] if w['id'] == 'liquid-glass'][0]
h = g['options']['html']
print('html chars:', len(h))
print('panels:', h.count('class="g"'))
print('has data url:', 'data:image/jpeg;base64' in h)
print('has bg-size:', 'background-size:' in h)
print('global radius:', c['display']['appearance'].get('radius'))
print('config size KB:', round(len(json.dumps(c)) / 1024))
print('sample panel:', [s for s in h.split('><') if 'class="g"' in s][:1])
