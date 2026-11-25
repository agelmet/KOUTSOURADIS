"""Offset-preserving HTML tree (no re-serialisation): every element knows where its tags start/end in the source."""
from html.parser import HTMLParser
VOID={'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr'}
class El:
    __slots__=('tag','attrs','s0','s1','e0','e1','kids','parent','raw')
    def __init__(s,tag,attrs,s0,s1,parent,raw):
        s.tag=tag;s.attrs=dict(attrs);s.s0=s0;s.s1=s1;s.e0=None;s.e1=None;s.kids=[];s.parent=parent;s.raw=raw
    def cls(s): return (s.attrs.get('class') or '').split()
    def walk(s):
        yield s
        for k in s.kids: yield from k.walk()
class P(HTMLParser):
    def __init__(s,src):
        super().__init__(convert_charrefs=False); s.src=src
        s.lines=[0]
        for i,ch in enumerate(src):
            if ch=='\n': s.lines.append(i+1)
        s.root=El('#root',[],0,0,None,''); s.cur=s.root
    def off(s):
        l,c=s.getpos(); return s.lines[l-1]+c
    def handle_starttag(s,tag,attrs):
        o=s.off(); raw=s.get_starttag_text(); e=El(tag,attrs,o,o+len(raw),s.cur,raw); s.cur.kids.append(e)
        if tag in VOID: e.e0=e.e1=e.s1
        else: s.cur=e
    def handle_startendtag(s,tag,attrs):
        o=s.off(); raw=s.get_starttag_text(); e=El(tag,attrs,o,o+len(raw),s.cur,raw); e.e0=e.e1=e.s1; s.cur.kids.append(e)
    def handle_endtag(s,tag):
        o=s.off(); n=s.cur
        while n is not s.root and n.tag!=tag: n=n.parent
        if n is s.root: return
        # close everything up to n
        m=s.cur
        while m is not n:
            if m.e0 is None: m.e0=m.e1=o
            m=m.parent
        n.e0=o; n.e1=s.src.index('>',o)+1; s.cur=n.parent
def parse(src):
    p=P(src)
    # raw-text elements: let html.parser handle script/style via CDATA_CONTENT_ELEMENTS (it does)
    p.feed(src); p.close(); return p.root
