# Κεντρικές γραμμές (για «ζωγράφισμα») της κόκκινης και της πράσινης γραμμής του λογοτύπου
import numpy as np, json, sys
from skimage.morphology import skeletonize
from collections import deque
S=4; L=np.load(sys.argv[1])
def longest_path(sk):
    ys,xs=np.nonzero(sk); pts=set(zip(ys,xs))
    def nb(p):
        y,x=p
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if (dy or dx) and (y+dy,x+dx) in pts: yield (y+dy,x+dx)
    def bfs(s):
        prev={s:None};q=deque([s]);last=s
        while q:
            p=q.popleft();last=p
            for n in nb(p):
                if n not in prev: prev[n]=p;q.append(n)
        return last,prev
    # largest component start
    s=next(iter(pts)); a,_=bfs(s); b,prev=bfs(a)
    path=[];p=b
    while p is not None: path.append(p);p=prev[p]
    return path
def rdp(pts,eps):
    if len(pts)<3: return pts
    a=np.array(pts[0],float);b=np.array(pts[-1],float);ab=b-a;n=np.hypot(*ab) or 1
    d=[abs(ab[0]*(p[1]-a[1])-ab[1]*(p[0]-a[0]))/n for p in pts]
    i=int(np.argmax(d))
    if d[i]>eps: return rdp(pts[:i+1],eps)[:-1]+rdp(pts[i:],eps)
    return [pts[0],pts[-1]]
def smooth(pts):
    P=[np.array(p,float) for p in pts]; d='M%.1f %.1f'%tuple(P[0])
    for i in range(len(P)-1):
        p0=P[i-1] if i>0 else P[i]; p1=P[i]; p2=P[i+1]; p3=P[i+2] if i+2<len(P) else P[i+1]
        c1=p1+(p2-p0)/6; c2=p2-(p3-p1)/6
        d+='C%.1f %.1f %.1f %.1f %.1f %.1f'%(c1[0],c1[1],c2[0],c2[1],p2[0],p2[1])
    return d
out={}
for k in ('red','dg'):
    m=L[k].copy(); m[240*S:]=False
    sk=skeletonize(m)
    path=longest_path(sk)
    pts=[(x/S,y/S) for (y,x) in path]
    pts=rdp(pts,0.35)
    out[k]=smooth(pts)
    # line thickness = area / length
    length=sum(np.hypot(pts[i+1][0]-pts[i][0],pts[i+1][1]-pts[i][1]) for i in range(len(pts)-1))
    print(k,len(path),'pts',len(pts),'length %.0f'%length,'width %.2f'%(m.sum()/S/S/length))
json.dump(out,open(sys.argv[2],'w'))
