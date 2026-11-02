#!/usr/bin/env python3
"""Build an SVG dashboard from public GitHub data. Uses no third-party packages."""
import json, urllib.request, pathlib, datetime, html
username='nikolas-AI'
req=urllib.request.Request(f'https://api.github.com/users/{username}',headers={'Accept':'application/vnd.github+json','User-Agent':'zek-profile-readme'})
with urllib.request.urlopen(req,timeout=20) as response: user=json.load(response)
req=urllib.request.Request(f'https://api.github.com/users/{username}/repos?per_page=100&type=owner&sort=pushed',headers={'Accept':'application/vnd.github+json','User-Agent':'zek-profile-readme'})
with urllib.request.urlopen(req,timeout=20) as response: repos=json.load(response)
repos=[r for r in repos if not r.get('fork')]
from collections import Counter
langs=Counter(r.get('language') for r in repos if r.get('language'))
top=langs.most_common(5)
repo_count=int(user.get('public_repos',0)); followers=int(user.get('followers',0)); stars=sum(int(r.get('stargazers_count',0)) for r in repos)
last=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d UTC')
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="245" viewBox="0 0 1100 245">','<rect width="1100" height="245" rx="20" fill="#0d1528"/>','<rect x="15" y="15" width="1070" height="215" rx="16" fill="none" stroke="#29364d"/>','<text x="40" y="50" fill="#67e8f9" font-family="monospace" font-size="20">GITHUB / ACTIVITY</text>',f'<text x="820" y="48" fill="#8c9cb6" font-family="monospace" font-size="13">updated {last}</text>']
for i,(label,value) in enumerate([('PUBLIC REPOS',repo_count),('FOLLOWERS',followers),('REPO STARS',stars)]):
 x=40+i*185;parts.extend([f'<text x="{x}" y="104" fill="#f1f5f9" font-size="36" font-family="monospace" font-weight="bold">{value}</text>',f'<text x="{x}" y="132" fill="#93a4bd" font-size="13" font-family="monospace">{label}</text>'])
parts.append('<text x="620" y="92" fill="#a78bfa" font-size="16" font-family="monospace">REPOSITORIES BY PRIMARY LANGUAGE</text>')
colors=['#67e8f9','#a78bfa','#6d7cc8','#3b648e','#30445a'];total=sum(c for _,c in top) or 1
x=620
for (_,count),color in zip(top,colors):
 width=round(420*count/total);parts.append(f'<rect x="{x}" y="112" width="{max(1,width)}" height="19" rx="2" fill="{color}"/>'); x+=width
parts.append('<text x="620" y="160" fill="#cbd5e1" font-size="13" font-family="monospace">'+html.escape('  ·  '.join(f'{lang} {count}' for lang,count in top)[:57])+'</text>')
parts.append('<text x="40" y="211" fill="#64748b" font-size="12" font-family="monospace">Source: public GitHub API · primary language per repo (not code volume)</text></svg>')
pathlib.Path('assets/dashboard.svg').write_text(''.join(parts),encoding='utf-8')
