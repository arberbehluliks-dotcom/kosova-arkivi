import json,re
D='/home/claude/kosova-arkivi/data/'
ser={x['id']:x for x in json.load(open(D+'series.json'))}
obs=json.load(open(D+'observations.json'))
def key(o):return (o['collected'],o['seq'])
cur={}
for o in obs:
    k=(o['s'],o['p'])
    if k not in cur or key(o)>key(cur[k]):cur[k]=o
def get(s,p):
    o=cur.get((s,p));return o
def pk(p):
    m=re.search(r'(\d{4})',p);y=int(m.group(1)) if m else 0
    q=re.search(r'(?:T|TM)(\d)',p);mm=re.match(r'\d{4}-(\d\d)',p)
    return (y,int(q.group(1)) if q else int(mm.group(1)) if mm else 0)
def latest(s):
    c=[o for (ss,p),o in cur.items() if ss==s and not o['f']]
    return max(c,key=lambda o:pk(o['p'])) if c else None
def pack(s,p=None):
    o=get(s,p) if p else latest(s)
    se=ser[s];src=o['src'][0]
    return {'s':s,'t':se['t'],'u':se['unit'],'p':o['p'],'v':o['v'],'src':src.get('t',''),'url':src.get('u',''),'m':o['method'][:160],'pub':o.get('pub')}
def tile(s,p,pp,good,tol,ik,title,fmt):
    a=pack(s,p);b=get(s,pp)
    d=None if not b else round(a['v']-b['v'],1)
    if d is None:st='na'
    elif abs(d)<=tol:st='same'
    else:st='good' if (d>0)==(good=='up') else 'bad'
    return dict(a,ik=ik,title=title,fmt=fmt,prev=None if not b else {'p':pp,'v':b['v']},d=d,st=st)
tiles=[
 tile('cpi-vjetor','2026-10','2025-10','down',0.3,'price','Inflacioni, tetor','%'),
 tile('punesimi-3','2025','2024','down',0.3,'work','Papunësia','%'),
 tile('punesimi-1','2025','2024','up',10,'wage','Paga neto mesatare','€'),
 tile('bqk-0','TM2 2026','TM2 2025','up',0.3,'growth','Rritja e ekonomisë','%'),
 tile('tj-eksport','2026-10','2025-10','up',2,'export','Eksporti, tetor','mln €'),
]
z=json.load(open(D+'zotimet26.json'));c=z['cols']
plan=[{'t':r[0],'st':r[c.index('st')],'pg':r[c.index('pg')],'now':r[c.index('now')]} for r in z['rows']]
# kërkimi: të gjitha serite me vlerën e fundit
search=[pack(s) for s in ser if latest(s)]
news=[pack(s) for s in ['tj-eksport','tj-bilanc','ppi-2','bqk-7','bqk-8','bqk-3']]
extra={s:pack(s) for s in ['bqk-7','bqk-8','bqk-3','bqk-5','tj-mbulim','punesimi-0','bqk-1']}
extra['cmimet-0']=pack('cmimet-0','2026 (parashikim)')
data=dict(tiles=tiles,plan=plan,search=search,news=news,x=extra,n_obs=len(obs),n_ser=len(ser),upd=max(o['collected'] for o in obs))
html=open('tpl.html',encoding='utf-8').read().replace('/*DATA*/null',json.dumps(data,ensure_ascii=False))
open('ballina.html','w',encoding='utf-8').write(html)
print(len(html),[ (t['title'],t['st'],t['d']) for t in tiles])
