import re, html, os, json

path = os.path.join(os.environ['TEMP'], 'phonebox-ytm-clip.html')
raw = open(path, encoding='utf-8', errors='replace').read()
m = re.search(r'StartHTML:(\d+)', raw)
if m:
    raw = raw[int(m.group(1)):]

def clean(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s).replace('\xa0', ' ').strip()

items = []
seen = set()
for m in re.finditer(r'<a\b([^>]*?)href="https://music\.youtube\.com/watch\?v=([A-Za-z0-9_-]{11})[^"]*"([^>]*)>(.*?)</a>', raw, re.S):
    vid = m.group(2)
    if vid in seen:
        continue
    attrs = m.group(1) + ' ' + m.group(3)
    tm = re.search(r'title="([^"]*)"', attrs)
    title = html.unescape(tm.group(1)).strip() if tm else clean(m.group(4))
    if not title:
        continue
    seen.add(vid)
    # look backwards for the nearest secondary-text (artist) in the same renderer
    pre = raw[max(0, m.start() - 4000):m.start()]
    ar = list(re.finditer(r'class="[^"]*secondary-text[^"]*"[^>]*>(.*?)</yt-formatted-string>', pre, re.S))
    artist = clean(ar[-1].group(1)) if ar else ''
    artist = re.split(r'\s+[·•]\s+|\s+\d+(\.\d+)?[mkbn]?\s+views|\s+\d+(\.\d+)?[mkbn]?\s+plays', artist)[0].strip()
    items.append({'id': vid, 'title': title[:70], 'artist': artist[:50]})

print('COUNT', len(items))
for i, it in enumerate(items, 1):
    print(f"{i:2}. {it['id']}  {it['title']}  | {it['artist']}")

open(os.path.join(os.environ['TEMP'], 'phonebox-home-songs.json'), 'w', encoding='utf-8').write(json.dumps(items, ensure_ascii=False, indent=2))
