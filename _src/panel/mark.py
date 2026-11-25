"""mark.py <site-dir> — marks every editable text, photo and repeating block for the Advon in-page editor.
Idempotent: strips old marks first. Never re-serialises HTML (inserts at source offsets).
Text  : <p data-e="K"><!--e:K-->…<!--/e:K--></p>
Photo : <img data-ei="K" …>
List  : <div data-el="K"><!--l:K-->…<!--/l:K--></div>
Keys are hashes of the original content, so they survive rebuilds."""
import sys,os,re,glob,hashlib,html as H
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tree import parse
TEXT={'h1','h2','h3','h4','h5','h6','p','li','figcaption','dt','dd','summary','blockquote','td','th','label','span','b','strong','em','i','small','a','div'}
INLINE={'em','i','b','strong','a','br','span','sup','sub','small','abbr','mark','u','s','cite','q','time'}
LISTCLS={'prose','cf-l','cf-phs','mb-g','kw','pil-g','gn','faq-l','tp-grid','chips','proof-in','oc-grid','syn-steps','pt-list','cr-grid','eth-ch','by-grid','ha-g','st-l','sp-g'}
SKIPCLS={'crumbs','ar-prog','mnav','mbar','hd','ft-bot','ft-nav','fcol','cf-line','ac','amb'}
def h(s,n=7): return hashlib.sha1(s.encode()).hexdigest()[:n]
def strip_marks(s):
    s=re.sub(r'<!--/?[eli]:[\w-]+-->','',s)
    s=re.sub(r' data-e[il]?="[\w-]+"','',s)
    return s
def text_of(src,e): return re.sub(r'\s+',' ',H.unescape(re.sub(r'<[^>]+>','',src[e.s1:e.e0]))).strip()
def skip(e):
    if e.tag in ('svg','script','style','noscript','template','iframe','nav','select','form','button'): return True
    if e.attrs.get('aria-hidden')=='true': return True
    if set(e.cls())&SKIPCLS: return True
    return False
def leaf(e):
    for k in e.walk():
        if k is e: continue
        if k.tag not in INLINE: return False
        if k.tag=='span' and k.attrs.get('class'): return False
    return True
def page_id(f): return os.path.basename(f)[:-5]
def mark_file(path):
    src=strip_marks(open(path,encoding='utf-8').read())
    root=parse(src); pid=page_id(path)
    ins=[]  # (offset, order, text)
    seen={}
    def key(prefix,basis):
        k=prefix+h(basis); n=seen.get(k,0); seen[k]=n+1
        return k if n==0 else f'{k}-{n+1}'
    def addattr(e,attr):
        # insert before the closing > of the start tag (handle "/>")
        end=e.s1-1
        if src[end-1]=='/': end-=1
        ins.append((end,0,f' {attr}'))
    def walk(e,zone):
        for k in e.kids:
            if skip(k): continue
            cls=set(k.cls())
            if k.tag=='img':
                s=k.attrs.get('src','')
                if s and not s.endswith('.svg') and k.attrs.get('alt','')!='':
                    K=key(zone[0]+'i',s); addattr(k,f'data-ei="{K}"')
                continue
            if zone[1]=='main' and (cls&LISTCLS or (pid=='arthra' and k.tag=='div' and 'wrap' in cls and k.parent and 'ar-list' in k.parent.cls())):
                K=key(zone[0]+'l',k.tag+'.'+'.'.join(sorted(cls))+'|'+text_of(src,k)[:80])
                addattr(k,f'data-el="{K}"'); ins.append((k.s1,1,f'<!--l:{K}-->')); ins.append((k.e0,-1,f'<!--/l:{K}-->'))
            if k.tag in TEXT and leaf(k) and text_of(src,k) and k.e0 is not None and k.e0>k.s1:
                if zone[1]=='foot' and k.tag!='p': continue
                K=key(zone[0]+'t',k.tag+'|'+text_of(src,k))
                addattr(k,f'data-e="{K}"'); ins.append((k.s1,2,f'<!--e:{K}-->')); ins.append((k.e0,-2,f'<!--/e:{K}-->'))
                continue
            walk(k,zone)
    for e in root.walk():
        if e.tag=='main': walk(e,('','main'))
        if e.tag=='footer': walk(e,('f','foot'))
    # apply from the end; for equal offsets: closing markers (-) before opening (+) in text order
    ins.sort(key=lambda x:(x[0],x[1]))
    out=[];last=0
    for off,_,t in ins:
        out.append(src[last:off]); out.append(t); last=off
    out.append(src[last:])
    res=''.join(out)
    open(path,'w',encoding='utf-8').write(res)
    return sum(1 for x in ins if x[2].startswith(' data-e=')), sum(1 for x in ins if 'data-ei' in x[2]), sum(1 for x in ins if 'data-el' in x[2])
if __name__=='__main__':
    d=sys.argv[1]; tot=[0,0,0]
    for f in sorted(glob.glob(os.path.join(d,'*.html'))):
        b=os.path.basename(f)
        if b in ('privacy.html','admin.html') or b.startswith('index.backup'): continue
        r=mark_file(f); tot=[a+b2 for a,b2 in zip(tot,r)]
        print(f'{b:45s} texts {r[0]:4d}  photos {r[1]:3d}  lists {r[2]:2d}')
    print('total',tot)
