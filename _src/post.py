import re,glob,os,json,urllib.parse
R='/home/claude/k/repo'; D='https://gkoutsouradis.gr'
def url(fn): return D+'/' if fn=='index.html' else D+'/'+fn[:-5]
pages=sorted(os.path.basename(f) for f in glob.glob(R+'/*.html'))
for fn in pages:
    p=R+'/'+fn; s=open(p).read()
    if fn!='index.html' and 'rel="canonical"' not in s:
        s=s.replace('<meta name="robots"','<link rel="canonical" href="%s">\n<meta property="og:url" content="%s">\n<meta name="robots"'%(url(fn),url(fn)),1)
    s=re.sub(r'(<meta property="og:image" content=")(assets/[^"]+)"',lambda m:m.group(1)+D+'/'+m.group(2)+'"',s)
    def fixld(m):
        j=json.loads(m.group(1))
        def walk(o):
            if isinstance(o,dict):
                for k,v in list(o.items()):
                    if isinstance(v,str) and (v.startswith('assets/') or re.match(r'^[\w-]+\.html(#.*)?$',v)) and k in ('image','item','url'):
                        o[k]=D+'/'+v if v.startswith('assets/') else (url(v.split('#')[0])+('#'+v.split('#')[1] if '#' in v else ''))
                    else: walk(v)
            elif isinstance(o,list): [walk(x) for x in o]
        walk(j); return '<script type="application/ld+json">'+json.dumps(j,ensure_ascii=False,separators=(',',':'))+'</script>'
    s=re.sub(r'<script type="application/ld\+json">(.*?)</script>',fixld,s,flags=re.S)
    open(p,'w').write(s)
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for fn in ['index.html']+[x for x in pages if x!='index.html']:
    sm+='  <url><loc>%s</loc><lastmod>2026-11-24</lastmod><priority>%s</priority></url>\n'%(url(fn),'1.0' if fn=='index.html' else ('0.3' if fn=='privacy.html' else '0.8'))
open(R+'/sitemap.xml','w').write(sm+'</urlset>\n')
# παλιές διευθύνσεις WordPress → νέες (Netlify _redirects)
OLD={'σχετικά-με-εμένα':'poios-eimai','υπηρεσίες':'ypiresies','άρθρα':'arthra','επικοινωνία':'epikoinonia','κλείστε-ραντεβού':'epikoinonia',
 'ατομική-συμβουλευτική':'atomiki-symvouleftiki','ψυχοθεραπεία-ενηλίκων':'psychotherapeia-enilikon','προσωπική-ανάπτυξη':'prosopiki-anaptyxi',
 'επαγγελματική-συμβουλευτική':'epaggelmatiki-symvouleftiki','coaching-business-coaching':'coaching','συμβουλευτική-στην-τρίτη-ηλικία':'symvouleftiki-triti-ilikia',
 'επιστημονικό-έργο':'to-ergo-mou','c1-συνθετική-προσέγγιση':'synthetiki-prosengisi','c2-υπαρξιακή-προσέγγιση':'yparxiaki-prosengisi',
 'c3-προσωποκεντρική-προσέγγιση':'prosopokentriki-prosengisi','c4-γνωσιακή-συμπεριφορική-προσέγγιση':'gnosiaki-symperiforiki-prosengisi',
 'd1-επιστημονικά-συνέδρια':'synedria','d2-βιβλία':'vivlia','customer-cabinet':'epikoinonia','hello-world':'arthra','form':'epikoinonia'}
rd=''.join('/%s/* /%s 301!\n/%s /%s 301!\n'%(urllib.parse.quote(k),v,urllib.parse.quote(k),v) for k,v in OLD.items())
open(R+'/_redirects','w').write('# παλιές σελίδες WordPress\n'+rd+'/category/* / 301!\n/wp-content/* / 301!\n')
print('post ok',len(pages))
