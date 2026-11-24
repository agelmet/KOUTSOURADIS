# Γράφει τα αρχεία λογοτύπου (ακριβές λογότυπο του πελάτη) στο repo
import json, sys
P=json.load(open('/home/claude/k/work/logo_paths.json')); O='/home/claude/k/repo/assets/img/'
COL={'sage':'#C6C690','line_r':'#9D4125','line_g':'#404A1E','name':'#8D3420','sub1':'#3E4320','sub2':'#3E4320'}
def p(k): return '<path fill-rule="evenodd" fill="%s" d="%s"/>'%(COL[k],P[k])
MARK=''.join(p(k) for k in ('sage','line_r','line_g'))
def svg(vb,body,title):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img"><title>%s</title>%s</svg>'%(vb,title,body)
T='Γιώργος Κουτσουραδής – Σύμβουλος Ψυχικής Υγείας, Ψυχοθεραπευτής Συνθετικής Προσέγγισης'
files={
 # πλήρες λογότυπο (κάθετο), όπως το έστειλε
 'giorgos-koutsouradis-logo.svg':svg('138 12 502 370',MARK+p('name')+p('sub1')+p('sub2'),T),
 # μόνο το σήμα (κεφάλια) για εικονίδιο/favicon
 'giorgos-koutsouradis-logo-icon.svg':svg('250 10 260 236',MARK,'Γιώργος Κουτσουραδής'),
 # οριζόντιο για την κεφαλίδα: σήμα + όνομα + «Σύμβουλος Ψυχικής Υγείας»
 'giorgos-koutsouradis-logo-header.svg':svg('0 0 640 132',
   '<g transform="translate(0 2) scale(.565) translate(-258 -15)">%s</g>'%MARK+
   '<g transform="translate(20 -238)">%s</g>'%p('name')+
   '<g transform="translate(-35 -224)">%s</g>'%p('sub1'),T),
}
for n,s in files.items(): open(O+n,'w').write(s); print(n,len(s)//1024,'KB')
