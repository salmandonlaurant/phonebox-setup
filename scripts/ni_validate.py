import requests

base = 'http://127.0.0.1:8080'
s = requests.Session()


def show(label, r):
    print(f'--- {label}: {r.status_code} {r.headers.get("content-type", "")[:40]}')
    if 'content-disposition' in r.headers:
        print('   disposition:', r.headers['content-disposition'])


r = s.get(base + '/api/overview', timeout=30)
show('overview unscoped', r)
d = r.json()
p = d['payload']
print('   repo opts:', len(d.get('repository_options') or []), '| scope:', d.get('repository'),
      '| posture:', p['summary']['posture_score'], '| comps:', len(p['components']),
      '| trend:', len(p['trend']))

r = s.get(base + '/api/overview', params={'repository': 'maven-central'}, timeout=30)
show('overview maven-central', r)
d = r.json()
p = d['payload']
print('   scope:', p.get('scope'))
print('   summary:', {k: p['summary'][k] for k in (
    'repositories', 'components', 'components_evaluated', 'critical', 'high',
    'quarantined', 'applications', 'posture_score', 'grade')})
print('   comps:', len(p['components']), 'apps:', len(p['applications']),
      'quar:', len(p['quarantine']), 'trend:', len(p['trend']))
print('   notes:', p.get('notes'))

r = s.get(base + '/api/overview', params={'repository': 'does-not-exist-xyz'}, timeout=30)
show('overview missing repo', r)
p = r.json()['payload']
print('   scope:', p.get('scope'))
print('   summary comps:', p['summary']['components'], 'repos:', p['summary']['repositories'])

r = s.get(base + '/report', params={'repository': 'maven-central'}, timeout=30)
show('report maven-central', r)
t = r.text
for needle in ['Repository briefing', 'maven-central', 'Repository scope', 'Board report',
               'Priority components', 'Generated']:
    print(f'   contains {needle!r}:', needle in t)
print('   report len:', len(t))

for kind in ['repositories', 'components', 'applications', 'quarantine', 'licenses', 'all']:
    r = s.get(base + f'/api/export/{kind}.csv', params={'repository': 'maven-central'}, timeout=30)
    show(f'csv {kind} scoped', r)
    if r.status_code != 200:
        print('   body:', r.text[:300])

for kind in ['all', 'snapshot', 'report', 'bogus']:
    r = s.get(base + f'/api/export/{kind}.json', params={'repository': 'maven-central'}, timeout=30)
    show(f'json {kind} scoped', r)
