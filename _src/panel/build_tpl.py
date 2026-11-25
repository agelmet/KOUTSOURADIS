"""build_tpl.py <site-dir> — writes arthro-neo.html (the template the server fills for every new article) from the existing article page."""
import sys,re,os
d=sys.argv[1]
s=open(os.path.join(d,'arthro-aftosympnonia-triti-ilikia.html'),encoding='utf-8').read()
s=re.sub(r'<!--/?[eil]:[\w-]+-->','',s); s=re.sub(r' data-e[il]?="[\w-]+"','',s)
def sub(pat,rep,flags=re.S,count=1):
    global s
    n=len(re.findall(pat,s,flags))
    if n<1: sys.exit('MISSING '+pat)
    s=re.sub(pat,rep,s,count=count,flags=flags)
sub(r'<title>.*?</title>','<title>{{TITLE_T}} | Άρθρο Γιώργου Κουτσουραδή</title>')
sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="{{DESC}}">')
sub(r'<link rel="canonical" href="[^"]*">','<link rel="canonical" href="{{URL}}">')
sub(r'<meta property="og:url" content="[^"]*">','<meta property="og:url" content="{{URL}}">')
sub(r'<meta property="og:title" content="[^"]*">','<meta property="og:title" content="{{TITLE_T}}">')
sub(r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="{{DESC}}">')
s=re.sub(r'<meta name="twitter:(title|description)" content="[^"]*">','',s)
s=re.sub(r'<link rel="alternate" hreflang[^>]*>','',s)
# all JSON-LD blocks -> one BlogPosting
lds=re.findall(r'<script type="application/ld\+json"[^>]*>.*?</script>',s,re.S)
for i,b in enumerate(lds): s=s.replace(b,'<script type="application/ld+json">{{LD}}</script>' if i==0 else '',1)
sub(r'<li aria-current="page">.*?</li>','<li aria-current="page">{{TITLE}}</li>')
sub(r'<p class="kick">Άρθρο · [^<]*</p>','<p class="kick">Άρθρο · {{TAG}} · {{DATE}}</p>')
sub(r'(<span class="w-name">).*?(</span>)',r'\1{{TITLE}}\2')
sub(r'(<p class="display h-words[^"]*"[^>]*>).*?(</p>)',r'\1{{SUB}}\2')
# body: everything inside .prose up to the author block; drop the references
sub(r'(<div class="wrap narrow prose"[^>]*>).*?(<div class="ar-end">)',r'\1{{IMG}}<div class="ar-new">{{BODY}}</div>\2')
s=s.replace('<link rel="canonical"','<meta name="gk-template" content="article"><link rel="canonical"',1)
open(os.path.join(d,'arthro-neo.html'),'w',encoding='utf-8').write(s)
print('arthro-neo.html',len(s),'placeholders',sorted(set(re.findall(r'\{\{(\w+)\}\}',s))))
