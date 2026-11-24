# Το λογότυπο του πελάτη (εικόνα Viber 24/11/2026) → διανυσματικά σύμβολα, πιστά στο πρωτότυπο
import numpy as np, potrace, json, sys
S=4; L=np.load(sys.argv[1]); out=sys.argv[2]
def path(m):
    bm=potrace.Bitmap(~m.astype(bool)); pl=bm.trace(turdsize=8,alphamax=1.0,opticurve=True,opttolerance=0.2)
    d=[]
    for c in pl:
        p=c.start_point; d.append('M%.1f %.1f'%(p.x/S,p.y/S))
        for s in c.segments:
            if s.is_corner: d.append('L%.1f %.1f L%.1f %.1f'%(s.c.x/S,s.c.y/S,s.end_point.x/S,s.end_point.y/S))
            else: d.append('C%.1f %.1f %.1f %.1f %.1f %.1f'%(s.c1.x/S,s.c1.y/S,s.c2.x/S,s.c2.y/S,s.end_point.x/S,s.end_point.y/S))
        d.append('Z')
    return ''.join(d)
def band(k,y0,y1):
    m=np.zeros_like(L[k]); m[y0*S:y1*S]=L[k][y0*S:y1*S]; return path(m)
P={'sage':band('sage',0,240),'line_r':band('red',0,240),'line_g':band('dg',0,240),
   'name':band('red',240,301),'sub1':band('dg',301,343),'sub2':band('dg',343,400)}
json.dump(P,open(out,'w')); print({k:len(v) for k,v in P.items()})
