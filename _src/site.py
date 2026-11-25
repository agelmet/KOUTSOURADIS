# -*- coding: utf-8 -*-
# Γιώργος Κουτσουραδής — πολυσέλιδο site. python3 site.py → /home/claude/k/repo/*.html
import re, json, html, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from services import SERVICES, COMMON_FAQ
K='/home/claude/k'; R=K+'/repo'; S=K+'/src'
MP=json.load(open(K+'/work/mark_paths.json'))
LG=json.load(open(K+'/work/logo_paths.json')); LC=json.load(open(K+'/work/logo_center.json'))
E=html.escape
PHONE='+30 698 588 0004'; TEL='+306985880004'; MAIL='gkoutsouradis.therapist@gmail.com'
ADDR='Μιαούλη 54, 121 31 Περιστέρι'; MAPQ='https://www.google.com/maps/search/?api=1&query=%CE%9C%CE%B9%CE%B1%CE%BF%CF%8D%CE%BB%CE%B7+54%2C+%CE%A0%CE%B5%CF%81%CE%B9%CF%83%CF%84%CE%AD%CF%81%CE%B9+121+31'
MAPEMB='https://maps.google.com/maps?q=38.0049331,23.6908265&z=16&output=embed'
DOMAIN='gkoutsouradis.gr'

# ---------- μικρά εργαλεία ----------
ICON={
 'chairs':'<path d="M3 18v-5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v5M3 15h6M4 18v2M8 18v2"/><path d="M21 18v-5a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v5M21 15h-6M20 18v2M16 18v2"/><path d="M9.5 7.5c1.5-1.6 3.5-1.6 5 0"/>',
 'layers':'<path d="M12 3 3 8l9 5 9-5z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/>',
 'sprout':'<path d="M12 21v-9M12 12c0-4-3-6-7-6 0 4 3 6 7 6zM12 10c0-3.6 2.6-5.6 6.5-5.6 0 3.6-2.6 5.6-6.5 5.6z"/><path d="M7 21h10"/>',
 'rings':'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5.5"/><circle cx="12" cy="12" r="2"/>',
 'compass':'<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
 'steps':'<path d="M3 20h5v-5h5v-5h5V5h3"/><path d="m16 5 2-2 2 2"/>',
 'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
 'phone':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 7 8.5-7"/>',
 'pin':'<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 'screen':'<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4"/>',
 'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'book':'<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5M8 7h7"/>',
 'mic':'<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M9 21h6"/>',
 'pen':'<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13.5 6.5 4 4"/>',
 'leaf':'<path d="M5 19C5 10 11 5 20 4c0 9-5 15-14 15z"/><path d="M5 19 13 11"/>',
 'film':'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"/>',
 'people':'<circle cx="8" cy="8" r="3"/><circle cx="16.5" cy="9" r="2.5"/><path d="M3 20c0-3 2.2-5.5 5-5.5s5 2.5 5 5.5M13.5 20c.2-2.6 1.4-4.5 3.2-4.5 2 0 3.3 2 3.3 4.5"/>',
 'cap':'<path d="M2 9 12 4l10 5-10 5z"/><path d="M6 11v5c2 2 10 2 12 0v-5M22 9v6"/>',
 'shield':'<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
 'x':'<path d="M6 6l12 12M18 6 6 18"/>',
 'chev':'<path d="m6 9 6 6 6-6"/>',
 'plus':'<path d="M12 5v14M5 12h14"/>',
 'quote':'<path d="M9 7H5v6h4v4H5M19 7h-4v6h4v4h-4"/>',
}
def icon(n,cls='ic'):
    inner=re.sub(r'<(path|circle|rect)\b',r'<\1 pathLength="1"',ICON[n])
    return '<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'%(cls,inner)

SYM=('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><symbol id="mk" viewBox="250 10 260 236">'
 '<path class="mk-sg" d="%s" fill-rule="evenodd" style="fill:var(--mk-s,#C6C690);fill-opacity:calc(1 - var(--m2,0))"/>'
 '<path d="%s" fill="none" pathLength="1" style="stroke:var(--mk-o,#9D4125);stroke-width:calc(var(--mk-w,4) * 1.22);stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:var(--m1,0)"/>'
 '<path d="%s" fill="none" pathLength="1" style="stroke:var(--mk-g,#404A1E);stroke-width:calc(var(--mk-w,4) * .95);stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:var(--m3,0)"/>'
 '</symbol></defs></svg>')%(LG['sage'],LC['red'],LC['dg'])
BYMK='<img class="by-mk" src="assets/img/giorgos-koutsouradis-logo-icon.svg" width="260" height="236" alt="" loading="lazy">'
def mark(cls='mk'): return '<svg class="%s" viewBox="0 0 260 236" aria-hidden="true"><use href="#mk"/></svg>'%cls

IMGS={
 'portrait':('giorgos-koutsouradis-symvoulos-psychikis-ygeias-peristeri-portreto',[640,960,1400],1600,1600,'Ο Γιώργος Κουτσουραδής, σύμβουλος ψυχικής υγείας και ψυχοθεραπευτής, στο Περιστέρι'),
 'armchair':('giorgos-koutsouradis-psychotherapeftis-grafeio-polythrona',[720,1080,1448],1448,1086,'Ο ψυχοθεραπευτής Γιώργος Κουτσουραδής στην πολυθρόνα του γραφείου του, δίπλα στα πτυχία του'),
 'office':('giorgos-koutsouradis-synthetikos-psychotherapeftis-peristeri-grafeio',[720,1080,1448],1448,1086,'Ο Γιώργος Κουτσουραδής στο γραφείο συμβουλευτικής στο Περιστέρι'),
 'shelf':('giorgos-koutsouradis-grafeio-vivliothiki-peristeri',[483],483,640,'Η βιβλιοθήκη και η πολυθρόνα στο γραφείο του Γιώργου Κουτσουραδή στο Περιστέρι'),
 'room':('giorgos-koutsouradis-grafeio-symvouleftikis-peristeri',[960,1440,2048],2048,1152,'Το γραφείο συμβουλευτικής και ψυχοθεραπείας του Γιώργου Κουτσουραδή στο Περιστέρι'),
 'conf':('giorgos-koutsouradis-karakasidou-synedrio-poster',[600,1000],1200,1600,'Ο Γιώργος Κουτσουραδής και η Ειρήνη Καρακασίδου μπροστά στην αναρτημένη ανακοίνωσή τους σε πανελλήνιο συνέδριο'),
 'book':('chartografontas-ti-stadiodromia-karakasidou-koutsouradis-vivlio',[400,670],670,948,'Το εξώφυλλο του βιβλίου «Χαρτογραφώντας τη σταδιοδρομία» των Ειρήνης Καρακασίδου και Γιώργου Κουτσουραδή, Εκδόσεις Παρισιάνου'),
 'p2025':('poster-19o-synedrio-psychologikis-erevnas-ioannina-2025',[560,1206],1206,1997,'Η αναρτημένη ανακοίνωση των Γ. Κουτσουραδή και Ε. Καρακασίδου στο 19ο Πανελλήνιο Συνέδριο Ψυχολογικής Έρευνας, Ιωάννινα 2025'),
 'p2023':('poster-8o-synedrio-symvouleftikis-psychologias-2023',[560,1125],1125,1837,'Η αναρτημένη ανακοίνωση των Γ. Κουτσουραδή και Ε. Καρακασίδου στο 8ο Πανελλήνιο Συνέδριο Συμβουλευτικής Ψυχολογίας, Αθήνα 2023'),
 'patra':('9o-panellinio-synedrio-symvouleftikis-psychologias-patra-2025',[1143],1143,200,'Το λογότυπο του 9ου Πανελλήνιου Συνεδρίου Συμβουλευτικής Ψυχολογίας, Πάτρα, 6–9 Νοεμβρίου 2025'),
 'pa_eis':('giorgos-koutsouradis-9o-synedrio-symvouleftikis-patra-2025-eisigisi',[480,900,1200],1200,1600,'Η συνεδρία του Γιώργου Κουτσουραδή στο 9ο Πανελλήνιο Συνέδριο Συμβουλευτικής Ψυχολογίας στην Πάτρα, στο τέλος της παρουσίασης'),
 'pa_om':('giorgos-koutsouradis-9o-synedrio-symvouleftikis-patra-2025-omada',[640,1200,1600],1600,1200,'Ο Γιώργος Κουτσουραδής με συναδέλφους στο 9ο Πανελλήνιο Συνέδριο Συμβουλευτικής Ψυχολογίας, Πανεπιστήμιο Πατρών 2025'),
 'thess':('8o-panellinio-synedrio-anaptyxiakis-psychologias-thessaloniki-2026',[650],650,300,'Το λογότυπο του 8ου Πανελλήνιου Συνεδρίου Αναπτυξιακής Ψυχολογίας «τὰ πάντα ῥεῖ…», Θεσσαλονίκη, 15–18 Οκτωβρίου 2026'),
 'th_om':('giorgos-koutsouradis-8o-synedrio-anaptyxiakis-thessaloniki-2026-omada',[480,900,1200],1200,1600,'Ο Γιώργος Κουτσουραδής με τους ομιλητές της συνεδρίας στο 8ο Πανελλήνιο Συνέδριο Αναπτυξιακής Ψυχολογίας, Θεσσαλονίκη 2026'),
 'th_eis':('giorgos-koutsouradis-8o-synedrio-anaptyxiakis-thessaloniki-2026-eisigisi',[640,1200,1600],1600,1200,'Ο Γιώργος Κουτσουραδής παρουσιάζει την εισήγηση «Συμβουλευτική Ψυχολογία στην Τρίτη Ηλικία» στο 8ο Πανελλήνιο Συνέδριο Αναπτυξιακής Ψυχολογίας'),
 'th_vima':('giorgos-koutsouradis-8o-synedrio-anaptyxiakis-thessaloniki-2026-vima',[480,900,1200],1200,1600,'Ο Γιώργος Κουτσουραδής στο βήμα του 8ου Πανελλήνιου Συνεδρίου Αναπτυξιακής Ψυχολογίας, Θεσσαλονίκη 2026'),
 'es_dia':('esyom-symposio-atomiki-symvouleftiki-omotimon-patra-2025-diafaneia',[640,1268],1268,726,'Η πρώτη διαφάνεια της εισήγησης «Ατομική Συμβουλευτική Ομοτίμων» των Γ. Κουτσουραδή, Γ. Σύρακα και Α. Σωτηρίου'),
 'es_om':('esyom-symposio-atomiki-symvouleftiki-omotimon-patra-2025-omada',[320],320,200,'Οι ομιλητές του συμποσίου της Ε.ΣΥ.ΟΜ για τη Συμβουλευτική Ομοτίμων, με τον Γιώργο Κουτσουραδή'),
 'es_pan':('esyom-symposio-atomiki-symvouleftiki-omotimon-patra-2025-panel',[320],320,180,'Ο Γιώργος Κουτσουραδής στο πάνελ του συμποσίου για τη Συμβουλευτική Ομοτίμων'),
 'ioannina':('19o-panellinio-synedrio-psychologikis-erevnas-ioannina',[1003],1003,260,'Το λογότυπο του 19ου Πανελλήνιου Συνεδρίου Ψυχολογικής Έρευνας, Ιωάννινα 2025'),
}
def img(k,sizes='100vw',cls='',eager=False,lb=True,alt=None):
    n,ws,w,h,a=IMGS[k]
    ss=', '.join('assets/img/%s-%d.webp %dw'%(n,x,x) for x in ws)
    big='assets/img/%s-%d.webp'%(n,ws[-1]); mid='assets/img/%s-%d.webp'%(n,ws[min(1,len(ws)-1)])
    at='loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return '<img class="%s" src="%s" srcset="%s" sizes="%s" width="%d" height="%d" alt="%s" %s%s>'%(cls,mid,ss,sizes,w,h,E(alt or a),at,(' data-lb="%s"'%big) if lb else '')
def h2(t,fx='',cls=''):
    return '<h2 class="lc%s"%s>%s</h2>'%((' '+cls) if cls else '',(' data-fx="%s"'%fx) if fx else '',t)
def kick(t): return '<p class="kick">%s</p>'%t
def btn(href,t,cls='btn',ic='arrow'): return '<a class="%s" href="%s"><span>%s</span>%s</a>'%(cls,href,t,icon(ic,'bi'))

NAV_SERV=[(s['slug']+'.html',s['short']) for s in SERVICES]
APPR=[('synthetiki-prosengisi','Συνθετική Προσέγγιση','Συνδυάζοντας θεραπευτικές μεθόδους, με επίκεντρο τον άνθρωπο.'),
      ('yparxiaki-prosengisi','Υπαρξιακή Προσέγγιση','Αναζητώντας νόημα, ελευθερία και αυθεντική ύπαρξη.'),
      ('prosopokentriki-prosengisi','Προσωποκεντρική Προσέγγιση','Ενσυναίσθηση, αποδοχή και αυθεντικότητα στη θεραπευτική σχέση.'),
      ('gnosiaki-symperiforiki-prosengisi','Γνωσιακή Συμπεριφορική Προσέγγιση','Αναγνωρίζοντας και αλλάζοντας σκέψεις και συμπεριφορές που δεν βοηθούν.')]
WORK=[('synedria.html','Συνέδρια'),('vivlia.html','Βιβλία'),('arthra.html','Κείμενα & Άρθρα')]

def header(cur):
    def a(h,t,c=''): return '<a href="%s"%s>%s</a>'%(h,' aria-current="page"' if cur==h else '',t)
    dd=lambda lab,items,key,hub: ('<div class="dd%s"><a class="ddb" href="%s"%s>%s %s</a><div class="ddm"><div class="ddi">%s</div></div></div>'%(
        ' cur' if cur in [i[0] for i in items]+[hub] else '',hub,' aria-current="page"' if cur==hub else '',lab,icon('chev','cv'),''.join('<a href="%s">%s</a>'%i for i in items)))
    nav=(a('poios-eimai.html','Ποιος είμαι')+dd('Υπηρεσίες',NAV_SERV,'s','ypiresies.html')+dd('Το έργο μου',WORK,'w','to-ergo-mou.html')+a('epikoinonia.html','Επικοινωνία'))
    mob=''.join('<a href="%s">%s</a>'%x for x in [('index.html','Αρχική'),('poios-eimai.html','Ποιος είμαι'),('ypiresies.html','Υπηρεσίες')])
    mob+='<div class="msub">'+''.join('<a href="%s">%s</a>'%x for x in NAV_SERV)+'</div>'
    mob+='<a href="to-ergo-mou.html">Το έργο μου</a><div class="msub">'+''.join('<a href="%s">%s</a>'%x for x in WORK)+'</div><a href="epikoinonia.html">Επικοινωνία</a>'
    home='#top' if cur=='index.html' else 'index.html'
    return ('<a class="skip" href="#main">Μετάβαση στο περιεχόμενο</a><div class="prog" aria-hidden="true"></div>'
     '<header class="hd" id="hd"><div class="hd-in"><a class="brand" href="%s" aria-label="Γιώργος Κουτσουραδής — αρχική σελίδα"><img class="lgh" src="assets/img/giorgos-koutsouradis-logo-header.svg" width="640" height="132" alt="Γιώργος Κουτσουραδής – Σύμβουλος Ψυχικής Υγείας"></a>'
     '<nav class="nav" aria-label="Κύριο μενού">%s</nav><a class="hcta" href="tel:%s">%s<span>%s</span></a>'
     '<button class="burger" type="button" aria-label="Άνοιγμα μενού" aria-expanded="false" aria-controls="mnav"><i></i><i></i></button></div></header>'
     '<div class="mnav" id="mnav" hidden><button class="mx" type="button" aria-label="Κλείσιμο μενού">%s</button><nav aria-label="Μενού κινητού">%s</nav>'
     '<div class="mfoot"><a href="tel:%s">%s %s</a><a href="mailto:%s">%s</a></div></div>')%(home,nav,TEL,icon('phone','bi'),PHONE,icon('x'),mob,TEL,icon('phone','bi'),PHONE,MAIL,MAIL)

def footer(cur):
    home='#top' if cur=='index.html' else 'index.html'
    col=lambda t,items: '<div class="fcol"><p class="fh">%s</p>%s</div>'%(t,''.join('<a href="%s">%s</a>'%i for i in items))
    return ('<footer class="ft" data-amb="profiles"><div class="ft-in">'
     '<div class="fbrand"><a class="brand lgcard" href="%s" aria-label="Γιώργος Κουτσουραδής — αρχική σελίδα"><img class="lgf" src="assets/img/giorgos-koutsouradis-logo.svg" width="502" height="370" alt="Γιώργος Κουτσουραδής – Σύμβουλος Ψυχικής Υγείας, Ψυχοθεραπευτής Συνθετικής Προσέγγισης" loading="lazy" decoding="async"></a>'
     '<p>Συμβουλευτική και ψυχοθεραπεία ενηλίκων στο Περιστέρι και online. Ένας ασφαλής χώρος κατανόησης, σύνδεσης και προσωπικής εξέλιξης.</p>'
     '<p class="fct"><a href="tel:%s">%s</a><a href="mailto:%s">%s</a><a href="%s" target="_blank" rel="noopener">%s</a></p></div>'
     '%s%s%s</div><div class="ft-bot"><span>© 2026 Γιώργος Κουτσουραδής</span><span class="fl"><a href="privacy.html">Απόρρητο &amp; cookies</a>'
     '<a class="cr" href="https://advonmedia.com" target="_blank" rel="noopener">Designed by <b class="adv">Advon Media</b></a></span></div></footer>'
     '<div class="mbar"><a href="tel:%s">%s<span>Κλήση</span></a><a href="epikoinonia.html#rantevou">%s<span>Ραντεβού</span></a><a href="%s" target="_blank" rel="noopener">%s<span>Οδηγίες</span></a></div>'
     '<button class="totop" type="button" aria-label="Επιστροφή στην κορυφή"><svg viewBox="0 0 44 44" aria-hidden="true"><circle class="tr" cx="22" cy="22" r="20"/><circle class="tp" cx="22" cy="22" r="20" pathLength="1"/></svg>%s</button>'
     '<div class="lb" hidden><button class="lbx" type="button" aria-label="Κλείσιμο">%s</button><img alt=""></div>'
    )%(home,TEL,PHONE,MAIL,MAIL,MAPQ,ADDR,
       col('Υπηρεσίες',NAV_SERV),col('Προσεγγίσεις',[(a+'.html',t) for a,t,_ in APPR]),col('Το έργο μου',[('poios-eimai.html','Ποιος είμαι')]+WORK+[('epikoinonia.html','Επικοινωνία')]),
       TEL,icon('phone','bi'),icon('mail','bi'),MAPQ,icon('pin','bi'),icon('chev','bi up'),icon('x'))

def crumbs(items):
    li=''.join('<li><a href="%s">%s</a></li>'%(h,t) for h,t in items[:-1])+'<li aria-current="page">%s</li>'%items[-1][1]
    return '<nav class="crumbs" aria-label="Διαδρομή"><ol><li><a href="index.html">Αρχική</a></li>%s</ol></nav>'%li

def faq(items,first_open=False):
    out=[]
    for i,it in enumerate(items):
        q,a=COMMON_FAQ[it] if isinstance(it,str) else it
        out.append('<details class="qa"%s><summary><span>%s</span><i>%s</i></summary><div class="ans"><p>%s</p></div></details>'%(' open' if first_open and i==0 else '',E(q),icon('plus','bi'),E(a)))
    return ''.join(out)
def faq_ld(items):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":(COMMON_FAQ[i] if isinstance(i,str) else i)[0],"acceptedAnswer":{"@type":"Answer","text":(COMMON_FAQ[i] if isinstance(i,str) else i)[1]}} for i in items]}

def cta_band(t='Ίσως είναι η στιγμή για το πρώτο βήμα.',p='Η απόφαση είναι δική σας. Αν νιώθετε ότι ήρθε η ώρα, θα χαρώ να σας γνωρίσω, σε έναν χώρο εμπιστοσύνης, με τον δικό σας ρυθμό. Η πρώτη επικοινωνία δεν σας δεσμεύει σε τίποτα.'):
    return ('<section class="cta" data-amb="rings"><div class="wrap cta-in">%s<div><p class="cta-t lc" data-fx="light">%s</p><p class="cta-p rv">%s</p>'
     '<div class="cta-b rv">%s%s</div></div></div></section>')%(mark('mk cmk draw-mk'),t,p,btn('epikoinonia.html#rantevou','Κλείστε ραντεβού','btn btn-l pulse'),'<a class="tl tl-l" href="tel:%s">ή καλέστε στο %s</a>'%(TEL,PHONE))

# ---------- σελίδες ----------
PAGES=[]
def page(fn,title,desc,body,cur=None,ld=None,crumbs_ld=None,og=None,cls=''):
    PAGES.append(dict(fn=fn,title=title,desc=desc,body=body,cur=cur or fn,ld=ld or [],crumbs=crumbs_ld,og=og,cls=cls))

# ===== ΑΡΧΙΚΗ =====
serv_cards=''.join(('<a class="sc tilt" href="%s.html" style="--i:%d"><span class="sc-n">0%d</span>%s<h3>%s</h3><p>%s</p><span class="sc-go">Περισσότερα %s</span></a>')%(
    s['slug'],i,i+1,icon(s['icon'],'ic sc-ic'),s['title'],s['card'],icon('arrow','bi')) for i,s in enumerate(SERVICES))
OUT4=[('Αυτογνωσία','Κατανόηση των σκέψεων, των συναισθημάτων και των προσωπικών σας αναγκών.'),
      ('Διαχείριση άγχους','Αναγνώριση και πιο αποτελεσματική διαχείριση του άγχους και της συναισθηματικής πίεσης.'),
      ('Υγιείς σχέσεις','Ουσιαστικές σχέσεις με σαφή όρια, επικοινωνία και αμοιβαίο σεβασμό.'),
      ('Ψυχική ανθεκτικότητα','Μεγαλύτερη ικανότητα προσαρμογής απέναντι στις δυσκολίες της ζωής.')]
outs=''.join('<div class="oc" style="--i:%d"><svg class="oc-r" viewBox="0 0 80 80" aria-hidden="true"><circle cx="40" cy="40" r="36"/><circle class="f" cx="40" cy="40" r="36" pathLength="1"/></svg><span class="oc-n">%d</span><h3>%s</h3><p>%s</p></div>'%(i,i+1,t,p) for i,(t,p) in enumerate(OUT4))
SYN=('<div class="syn-stage"><svg class="syn-svg" viewBox="0 0 600 560" role="img" aria-label="Τρεις θεραπευτικές προσεγγίσεις που συναντιούνται στη συνθετική ψυχοθεραπεία">'
 '<defs><radialGradient id="sg1" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#F3E6D3" stop-opacity=".9"/><stop offset="1" stop-color="#F3E6D3" stop-opacity="0"/></radialGradient></defs>'
 '<circle class="syn-glow" cx="300" cy="290" r="150" fill="url(#sg1)"/>'
 '<g class="syn-c c1"><circle cx="300" cy="290" r="128"/><text x="300" y="290">Υπαρξιακή</text></g>'
 '<g class="syn-c c2"><circle cx="300" cy="290" r="128"/><text x="300" y="282">Προσωπο-</text><text x="300" y="306">κεντρική</text></g>'
 '<g class="syn-c c3"><circle cx="300" cy="290" r="128"/><text x="300" y="282">Γνωσιακή</text><text x="300" y="306">Συμπεριφορική</text></g>'
 '<g class="syn-core"><circle cx="300" cy="290" r="44"/><text x="300" y="284">Εσείς</text><text class="sm" x="300" y="304">στο κέντρο</text></g>'
 '</svg></div>')
syn_steps=[('Κάθε προσέγγιση φωτίζει μια πλευρά','Η υπαρξιακή ρωτά τι δίνει νόημα. Η προσωποκεντρική φροντίζει τη σχέση και την αποδοχή. Η γνωσιακή συμπεριφορική δουλεύει με τις σκέψεις και τις συνήθειες.'),
           ('Συναντιούνται, δεν αθροίζονται','Η συνθετική ψυχοθεραπεία δεν είναι ένα «μείγμα» τεχνικών. Είναι ένα ενιαίο πλαίσιο, όπου οι προσεγγίσεις συνομιλούν με συνέπεια.'),
           ('Στο κέντρο, ο άνθρωπος','Η θεραπεία δεν μπορεί να είναι ίδια για όλους. Προσαρμόζεται στη δική σας ιστορία, στις ανάγκες και στον ρυθμό σας.')]
appr_links=''.join('<a class="ap" href="%s.html" style="--i:%d"><span class="ap-d d%d"></span><b>%s</b><span>%s</span>%s</a>'%(s,i,i,t,d,icon('arrow','bi')) for i,(s,t,d) in enumerate(APPR))
def synth_section(home=True):
    steps=''.join('<div class="syn-step" data-s="%d"><span class="ss-n">0%d</span><h3>%s</h3><p>%s</p></div>'%(i,i+1,t,p) for i,(t,p) in enumerate(syn_steps))
    return ('<section class="syn" id="prosengisi" data-amb="dots"><div class="syn-track"><div class="syn-pin"><div class="wrap syn-in"><div class="syn-txt">%s%s'
     '<p class="syn-lead rv">Κάθε άνθρωπος έχει τη δική του ιστορία και τον δικό του τρόπο να δίνει νόημα στη ζωή. Γι’ αυτό και η θεραπεία δεν μπορεί να είναι ίδια για όλους.</p>'
     '<div class="syn-steps">%s</div></div>%s</div></div></div>%s</section>')%(
     kick('Η θεραπευτική μου προσέγγιση'),h2('Τρεις ματιές.<br>Ένας άνθρωπος.','centre'),steps,SYN,
     '<div class="wrap ap-row">%s</div>'%appr_links if home else '')

HOME_FAQ=[('Σε ποιους απευθύνεστε;','Σε ενήλικες κάθε ηλικίας, μεταξύ άλλων και ανθρώπους της τρίτης ηλικίας, που περνούν μια δύσκολη περίοδο, βρίσκονται μπροστά σε μια αλλαγή ή απλώς θέλουν να γνωρίσουν καλύτερα τον εαυτό τους, καθώς και σε επαγγελματίες και στελέχη για coaching και επαγγελματική συμβουλευτική.'),
          'online','length','first','confidential','book']
home=('<section class="hero" id="top" data-amb="wash"><div class="hero-bg" aria-hidden="true">%s</div><div class="wrap hero-in">'
 '<figure class="hero-ph"><span class="hp-o o1"></span><span class="hp-o o2"></span><span class="hp-o o3"></span><span class="hp-fr">%s</span>'
 '<figcaption class="hp-cap"><span class="dot"></span>Περιστέρι · δια ζώσης &amp; online</figcaption></figure>'
 '<div class="hero-txt"><p class="eyebrow h-up">Συμβουλευτική &amp; Ψυχοθεραπεία Ενηλίκων</p>'
 '<h1 class="h1"><span class="w-name">Γιώργος Κουτσουραδής</span><span class="h1-role">Σύμβουλος Ψυχικής Υγείας &amp; Ψυχοθεραπευτής στο Περιστέρι</span></h1>'
 '<p class="display h-words">Ένας ασφαλής χώρος <em>κατανόησης</em>, σύνδεσης και προσωπικής εξέλιξης.</p>'
 '<p class="hero-lead h-up">Μέσα από μια συνθετική ψυχοθεραπευτική προσέγγιση, η θεραπεία γίνεται μια ουσιαστική συνάντηση με τον εαυτό σας και τις δυνατότητές σας. Είμαι εδώ για να σας συνοδεύσω σε αυτή τη διαδρομή.</p>'
 '<div class="hero-cta h-up">%s<a class="tl" href="poios-eimai.html">Γνωρίστε με</a></div>'
 '<ul class="chips h-up"><li>%s 50 λεπτά</li><li>%s Δια ζώσης &amp; online</li><li>%s Εμπιστευτικότητα</li></ul></div></div>'
 '<a class="scue" href="#proof" aria-label="Συνέχεια προς τα κάτω"><span></span></a></section>'
 # proof
 '<section class="proof" id="proof"><div class="wrap proof-in">'
 '<div class="pf" style="--i:0"><b><span data-count="2700" data-sep=".">2.700</span>+</b><span>ώρες εποπτευόμενης συμβουλευτικής &amp; ψυχοθεραπευτικής πρακτικής</span></div>'
 '<div class="pf" style="--i:1"><b data-count="5">5</b><span>χρόνια εκπαίδευσης στη Συνθετική Ψυχοθεραπεία (EICP)</span></div>'
 '<div class="pf" style="--i:2"><b data-count="6">6</b><span>πεδία εργασίας, από την ατομική συμβουλευτική έως το coaching</span></div>'
 '<div class="pf" style="--i:3"><b data-count="2025">2025</b><span>το βιβλίο «Χαρτογραφώντας τη σταδιοδρομία», Εκδόσεις Παρισιάνου</span></div>'
 '</div></section>'
 # services
 '<section class="serv" id="ypiresies" data-amb="lines"><div class="wrap"><div class="sh">%s%s<p class="sh-p rv">Κάθε άνθρωπος έχει τη δική του διαδρομή. Δημιουργούμε μαζί έναν ασφαλή χώρο κατανόησης, σύνδεσης και ουσιαστικής αλλαγής, προσαρμοσμένο στις δικές σας ανάγκες.</p></div>'
 '<div class="sc-grid">%s</div></div></section>'
 # for you
 '<section class="foryou" data-amb="wash2"><div class="wrap fy-in"><div class="fy-ph" data-par=".08"><div class="pol">%s</div></div>'
 '<div class="fy-txt">%s%s<p class="ink">Κάθε άνθρωπος έχει τη δική του μοναδική διαδρομή. Μέσα από μια συνθετική ψυχοθεραπευτική προσέγγιση, η θεραπεία γίνεται ένας ασφαλής χώρος κατανόησης, σύνδεσης και προσωπικής εξέλιξης.</p>'
 '<p class="ink">Μαζί διερευνούμε τις προκλήσεις, τις ανάγκες και τις δυνατότητές σας, με στόχο μια πιο ουσιαστική και ισορροπημένη σχέση με τον εαυτό σας και με τη ζωή.</p>'
 '<p class="sig rv">Γιώργος Κουτσουραδής</p></div></div></section>'
 # outcomes
 '<section class="outc" data-amb="rings"><div class="wrap"><div class="sh sh-c">%s%s</div><div class="oc-grid">%s</div></div></section>'
 + synth_section(True) +
 # quote
 '<section class="quote" data-amb="profiles"><div class="wrap q-in"><p class="qt" data-words>«Η ψυχοθεραπεία δεν είναι μια διαδικασία έτοιμων απαντήσεων. Είναι πρωτίστως μια ανθρώπινη συνάντηση, μέσα στην οποία η εμπιστοσύνη, η αυθεντικότητα και ο σεβασμός δημιουργούν τις προϋποθέσεις για αλλαγή.»</p>'
 '<p class="q-who rv">Γιώργος Κουτσουραδής</p>%s</div></section>'
 # work
 '<section class="work" data-amb="lines2"><div class="wrap"><div class="sh">%s%s<p class="sh-p rv">Η κλινική δουλειά συνομιλεί με την έρευνα και τη γραφή: ένα βιβλίο για τη σταδιοδρομία, ανακοινώσεις σε πανελλήνια συνέδρια και κείμενα για την ανθρώπινη εμπειρία.</p></div>'
 '<div class="wk-grid"><a class="wk wk-book" href="vivlia.html"><div class="wk-cv">%s</div><div class="wk-t"><span class="tag">Βιβλίο · 2025</span><h3>Χαρτογραφώντας τη σταδιοδρομία</h3><p>Θεωρία, αυτογνωσία και πράξη στη σύγχρονη συμβουλευτική. Με την Ειρήνη Καρακασίδου, Επιστημονικές Εκδόσεις Παρισιάνου.</p><span class="sc-go">Το βιβλίο %s</span></div></a>'
 '<a class="wk wk-c" href="synedria.html">%s<span class="tag">Συνέδρια</span><h3>Ανακοινώσεις σε πανελλήνια συνέδρια</h3><p>Θεσσαλονίκη 2026 · Πάτρα 2025 · Ιωάννινα 2025 · Αθήνα 2023: η συμβουλευτική στην τρίτη ηλικία, η συμβουλευτική ομοτίμων και προγράμματα παρέμβασης για ενήλικες.</p><span class="sc-go">Τα συνέδρια %s</span></a>'
 '<a class="wk wk-c" href="arthro-aftosympnonia-triti-ilikia.html">%s<span class="tag">Άρθρο</span><h3>Αυτοσυμπόνια στην τρίτη ηλικία</h3><p>Μια πιο ήπια σχέση με τον εαυτό στα χρόνια της ωρίμανσης.</p><span class="sc-go">Διαβάστε το %s</span></a></div></div></section>'
 # faq
 '<section class="faq" data-amb="dots2"><div class="wrap faq-in"><div class="faq-h">%s%s<div class="glance rv"><p class="g-t">Με μια ματιά</p><dl>'
 '<dt>Ποιος</dt><dd>Γιώργος Κουτσουραδής, Σύμβουλος Ψυχικής Υγείας &amp; Συνθετικός Ψυχοθεραπευτής</dd>'
 '<dt>Εκπαίδευση</dt><dd>Πενταετής εκπαίδευση στη Συμβουλευτική &amp; Συνθετική Ψυχοθεραπεία (European Institute of Counselling &amp; Psychotherapy), σπουδές Ψυχολογίας (University of Sunderland)</dd>'
 '<dt>Πού</dt><dd>Μιαούλη 54, Περιστέρι 121 31 · και online</dd><dt>Συνεδρία</dt><dd>Περίπου 50 λεπτά, συνήθως εβδομαδιαία</dd><dt>Ραντεβού</dt><dd><a href="tel:%s">%s</a> · <a href="mailto:%s">email</a></dd></dl></div></div>'
 '<div class="faq-l">%s</div></div></section>'
 + cta_band() )%(
 mark('mk hbg-mk'), img('portrait','(max-width: 900px) 92vw, 44vw','hp-img',eager=True),
 btn('epikoinonia.html#rantevou','Κλείστε ραντεβού','btn pulse0'), icon('clock','bi'),icon('screen','bi'),icon('shield','bi'),
 kick('Πώς μπορώ να σας υποστηρίξω'),h2('Έξι τρόποι να ξεκινήσουμε.','mask'),serv_cards,
 img('office','(max-width: 900px) 92vw, 46vw'),kick('Για εσάς'),h2('Μια πιο ουσιαστική σχέση με τον εαυτό σας.','roll'),
 kick('Τι μπορείτε να κερδίσετε'),h2('Τι αλλάζει μέσα από τη θεραπευτική διαδικασία','light'),outs,
 btn('poios-eimai.html','Ποιος είμαι','btn btn-ghost'),
 kick('Το έργο μου'),h2('Πέρα από το γραφείο.','mask'),img('book','(max-width: 900px) 40vw, 200px','',lb=False),icon('arrow','bi'),
 icon('mic','ic wk-ic'),icon('arrow','bi'),icon('pen','ic wk-ic'),icon('arrow','bi'),
 kick('Συχνές ερωτήσεις'),h2('Καλό είναι να γνωρίζετε','centre'),TEL,PHONE,MAIL,faq(HOME_FAQ,True))
page('index.html','Ψυχοθεραπευτής & Σύμβουλος Περιστέρι | Γιώργος Κουτσουραδής',
 'Γιώργος Κουτσουραδής, Σύμβουλος Ψυχικής Υγείας & Συνθετικός Ψυχοθεραπευτής στο Περιστέρι και online. Ψυχοθεραπεία ενηλίκων, συμβουλευτική, coaching.',
 home,ld=[faq_ld(HOME_FAQ)],cls='pg-home')

# ===== ΠΟΙΟΣ ΕΙΜΑΙ =====
PATH=[('Πληροφορική','Η πρώτη επαγγελματική στέγη: συστήματα, λογική, δομή.'),('Οικονομικά','Αριθμοί, αποφάσεις και οι πιέσεις που φέρνουν.'),
      ('Διοίκηση Επιχειρήσεων','Ομάδες, ευθύνη, ανθρώπινες σχέσεις στη δουλειά.'),('Coaching','Η πρώτη στροφή προς τον ίδιο τον άνθρωπο.'),
      ('Συμβουλευτική & Ψυχοθεραπεία','Μια συνειδητή επιλογή, δεμένη με την προσωπική μου εξέλιξη.')]
path_html=''.join('<li class="pt-st" style="--i:%d"><span class="pt-dot"></span><b>%s</b><span>%s</span></li>'%(i,t,d) for i,(t,d) in enumerate(PATH))
CRED=[('cap','Συμβουλευτική & Συνθετική Ψυχοθεραπεία','Πενταετής εκπαίδευση στο European Institute of Counselling & Psychotherapy.'),
      ('book','Σπουδές Ψυχολογίας','University of Sunderland.'),
      ('sprout','Θετική Ψυχολογία','Εκπαίδευση που εμπλουτίζει τη θεραπευτική μου ματιά.'),
      ('steps','Evidence-Based Coaching','Τεκμηριωμένες μέθοδοι για στόχους και εξέλιξη.')]
creds=''.join('<div class="cr-c tilt" style="--i:%d">%s<h3>%s</h3><p>%s</p></div>'%(i,icon(a,'ic'),t,d) for i,(a,t,d) in enumerate(CRED))
MEMB=[('people','Ελληνική Συμβουλευτική Εταιρεία (Ε.Ε.Σ.)','Τακτικό μέλος'),
      ('rings','Ελληνική Επιστημονική Εταιρεία Συμβουλευτικής Ομηλίκων (Ε.ΣΥ.ΟΜ)','Τακτικό μέλος'),
      ('layers','Ελληνική Εταιρεία Συνθετικών Ψυχοθεραπευτών (Ε.Ε.ΣΥ.Ψ.)','Τακτικό μέλος'),
       ('sprout','Ελληνική Εταιρεία Θετικής Ψυχολογίας (Ε.Ε.ΘΕ.ΨΥ.)','Μέλος'),
      ('compass','European Mentoring &amp; Coaching Council (EMCC Global)','Μέλος')]
memb=''.join('<li class="mb" style="--i:%d">%s<span class="mb-k">%s</span><b>%s</b></li>'%(i,icon(a,'ic'),k,t) for i,(a,t,k) in enumerate(MEMB))
ETH=['Εμπιστευτικότητα','Εχεμύθεια','Σεβασμός της αξιοπρέπειας','Αυτονομία κάθε ανθρώπου','Υψηλά πρότυπα πρακτικής']
MEMBERS_SEC=('<section class="memb" id="syllogoi" data-amb="lines"><div class="wrap mb-in"><div class="mb-h">%s%s'
 '<p class="ink">Η ενεργή συμμετοχή σε επιστημονικές εταιρείες και επαγγελματικούς φορείς αποτελεί σημαντικό μέρος της επαγγελματικής μου ταυτότητας. Μέσα από αυτήν διατηρώ συνεχή επαφή με τις εξελίξεις στον χώρο της συμβουλευτικής, της ψυχοθεραπείας και της ψυχικής υγείας, ενισχύοντας τη διαρκή επιστημονική μου εξέλιξη.</p></div>'
 '<ul class="mb-g" aria-label="Επιστημονικές και επαγγελματικές εταιρείες">%s</ul></div></section>'
 '<section class="eth" id="deontologia" data-amb="rings"><div class="wrap eth-in"><div class="eth-mk">%s</div><div class="eth-txt">%s%s'
 '<p class="ink">Η άσκηση της συμβουλευτικής και της ψυχοθεραπείας αποτελεί για εμένα μια πράξη ευθύνης, η οποία βασίζεται στην επιστημονική γνώση, τον σεβασμό προς τον άνθρωπο και την αυστηρή τήρηση των αρχών της επαγγελματικής δεοντολογίας. Ως μέλος των παραπάνω επιστημονικών και επαγγελματικών φορέων, διέπομαι από τους αντίστοιχους κώδικες δεοντολογίας τους, οι οποίοι αποτελούν το θεμέλιο για την υπεύθυνη άσκηση του επαγγέλματος και διασφαλίζουν την εμπιστευτικότητα, την εχεμύθεια, τον σεβασμό της αξιοπρέπειας και της αυτονομίας κάθε ανθρώπου, καθώς και τη διατήρηση υψηλών προτύπων επαγγελματικής πρακτικής.</p>'
 '<ul class="eth-ch">%s</ul>'
 '<p class="ink">Η συνεχής εκπαίδευση, η προσωπική θεραπεία, η κλινική εποπτεία και η ενεργή συμμετοχή στην επιστημονική κοινότητα αποτελούν αναπόσπαστο μέρος αυτής της δέσμευσης, ώστε οι υπηρεσίες που παρέχω να παραμένουν σύγχρονες, επιστημονικά τεκμηριωμένες και προσαρμοσμένες στις ανάγκες κάθε ανθρώπου.</p></div></div></section>'
)%(kick('Επιστημονικές &amp; επαγγελματικές εταιρείες'),h2('Μέλος της επιστημονικής κοινότητας.','mask'),memb,
   icon('shield','ic eth-ic'),kick('Κώδικας δεοντολογίας'),h2('Μια πράξη ευθύνης.','light'),''.join('<li style="--i:%d">%s</li>'%(i,t) for i,t in enumerate(ETH)))
BEYOND=[('people','Άνθρωποι & συζητήσεις','Οι συναντήσεις, η ανταλλαγή απόψεων και οι εμπειρίες που διευρύνουν τον τρόπο που βλέπουμε τον κόσμο.'),
        ('leaf','Η φύση','Ένας τρόπος να απομακρύνομαι από τους έντονους ρυθμούς, να παρατηρώ και να ξαναβρίσκω όσα συχνά περνούν απαρατήρητα.'),
        ('film','Κινηματογράφος & θέατρο','Διαφορετικές οπτικές πάνω στις σχέσεις, στις επιλογές, στις συγκρούσεις και στα υπαρξιακά ερωτήματα που μας συνοδεύουν.')]
beyond=''.join('<div class="by" style="--i:%d">%s<h3>%s</h3><p>%s</p></div>'%(i,icon(a,'ic'),t,d) for i,(a,t,d) in enumerate(BEYOND))
about=('<section class="phero ab-hero" id="top" data-amb="wash"><div class="wrap ph-in"><div class="ph-txt">%s%s'
 '<h1 class="h1"><span class="w-name">Ποιος είμαι</span><span class="h1-role r2"><span class="r2-n">Γιώργος Κουτσουραδής</span><span class="r2-t">Σύμβουλος Ψυχικής Υγείας &amp; Συνθετικός Ψυχοθεραπευτής</span></span></h1>'
 '<p class="display h-words">Η θεραπευτική σχέση ξεκινά από τη <em>συνάντηση</em> δύο ανθρώπων.</p></div>'
 '<figure class="ph-ph"><div class="rv-cur">%s</div></figure></div></section>'
 '<section class="ab-intro" data-amb="lines"><div class="wrap narrow">'
 '<p class="lead-l ink">Στη συμβουλευτική και την ψυχοθεραπεία, εργάζομαι ακολουθώντας τη συνθετική προσέγγιση. Ο βασικός μου στόχος είναι να δημιουργώ έναν ασφαλή και ουσιαστικό χώρο, όπου κάθε άνθρωπος μπορεί να εκφραστεί, να διερευνήσει τις δυσκολίες του και να ανακαλύψει νέους τρόπους να σχετίζεται με τον εαυτό του και με τους άλλους.</p>'
 '<p class="ink">Για μένα, η ψυχοθεραπεία δεν είναι μια διαδικασία έτοιμων απαντήσεων ούτε μια προσπάθεια να αλλάξει κάποιος για να ανταποκριθεί σε εξωτερικές προσδοκίες. Είναι πρωτίστως μια ανθρώπινη συνάντηση, όπου η εμπιστοσύνη, η αυθεντικότητα και ο σεβασμός δημιουργούν τις προϋποθέσεις για βαθύτερη κατανόηση και προσωπική αλλαγή.</p>'
 '<p class="ink">Κάθε άνθρωπος φέρνει τη δική του ιστορία, τις εμπειρίες, τις δυνατότητες και τις αντιφάσεις του. Ο ρόλος μου είναι να τον συνοδεύω σε αυτή την προσωπική διαδρομή, χωρίς προκαθορισμένες απαντήσεις, με σεβασμό στον τρόπο και στον χρόνο που χρειάζεται.</p></div></section>'
 '<section class="journey" data-amb="dots"><div class="wrap jr-in"><div class="jr-txt">%s%s'
 '<p class="ink">Η επαγγελματική μου πορεία δεν ξεκίνησε από την Ψυχολογία. Πέρασα από την Πληροφορική και τα Οικονομικά, από τη Διοίκηση Επιχειρήσεων και το Coaching. Γνώρισα διαφορετικά επαγγελματικά περιβάλλοντα, συνεργάστηκα με ανθρώπους κάθε ηλικίας και κατάλαβα από κοντά τις απαιτήσεις και τις πιέσεις της προσωπικής και επαγγελματικής ζωής.</p>'
 '<p class="ink">Σταδιακά, το ενδιαφέρον μου στράφηκε όλο και περισσότερο στον ίδιο τον άνθρωπο: στο πώς χτίζει τις σχέσεις του, πώς αντιμετωπίζει τις δυσκολίες, πώς αναζητά την ταυτότητά του και δίνει νόημα στις εμπειρίες του. Αυτή η αναζήτηση με οδήγησε στη Συμβουλευτική και στην Ψυχοθεραπεία. Δεν ήταν απλώς μια επαγγελματική αλλαγή, αλλά μια συνειδητή επιλογή, δεμένη με την προσωπική μου εξέλιξη.</p>'
 '<p class="pull rv">Η αλλαγή δεν ακολουθεί πάντα ευθεία γραμμή. Χρειάζεται χρόνο, αναστοχασμό και τη διάθεση να ξανακοιτάξουμε όσα θεωρούσαμε δεδομένα.</p></div>'
 '<div class="jr-path"><svg class="pt-svg" viewBox="0 0 400 900" preserveAspectRatio="none" aria-hidden="true"><path class="pt-bg" d="M200 10 C 40 120, 360 200, 200 300 S 40 480, 200 560 S 360 760, 200 890"/><path class="pt-ln" pathLength="1" d="M200 10 C 40 120, 360 200, 200 300 S 40 480, 200 560 S 360 760, 200 890"/></svg>'
 '<ol class="pt-list">%s</ol></div></div></section>'
 '<section class="edu" data-amb="rings"><div class="wrap"><div class="sh">%s%s<p class="sh-p rv">Κεντρικός άξονας της εκπαίδευσής μου είναι η πενταετής εκπαίδευση στη Συμβουλευτική και τη Συνθετική Ψυχοθεραπεία στο European Institute of Counselling &amp; Psychotherapy.</p></div>'
 '<div class="edu-in"><div class="edu-big"><b><span data-count="2700" data-sep=".">2.700</span>+</b><span>ώρες εποπτευόμενης συμβουλευτικής και ψυχοθεραπευτικής πρακτικής</span>'
 '<p>Η επαφή με διαφορετικές ανθρώπινες ιστορίες, μαζί με τη συστηματική εποπτεία και τον αναστοχασμό, με βοηθά να συνδέω τη θεωρία με την καθημερινή θεραπευτική πράξη.</p></div>'
 '<div class="cr-grid">%s</div></div>'
 '<div class="edu-more"><p class="ink">Η συνθετική προσέγγιση μού επιτρέπει να αξιοποιώ διαφορετικά θεωρητικά πλαίσια και μεθόδους, προσαρμόζοντας τη θεραπεία στις ανάγκες, στις δυσκολίες και στην ιστορία κάθε ανθρώπου. Σημαντικές επιρροές στη δουλειά μου είναι η <a href="yparxiaki-prosengisi.html">υπαρξιακή</a>, η <a href="prosopokentriki-prosengisi.html">προσωποκεντρική</a> και η <a href="gnosiaki-symperiforiki-prosengisi.html">γνωσιακή συμπεριφορική</a> προσέγγιση.</p>'
 '<p class="ink">Βλέπω την εκπαίδευση του ψυχοθεραπευτή ως μια συνεχή διαδικασία. Η επιστημονική γνώση εξελίσσεται, αλλά εξίσου σημαντική είναι η διαρκής καλλιέργεια της αυτογνωσίας, της επαγγελματικής ευθύνης και της ικανότητας να συναντάς τον άλλον χωρίς βεβαιότητες και προκαταλήψεις.</p></div>'
 '<figure class="edu-ph">%s<figcaption>Με την Ειρήνη Καρακασίδου, στην αναρτημένη ανακοίνωσή μας σε πανελλήνιο συνέδριο. <a href="synedria.html">Τα συνέδρια →</a></figcaption></figure></div></section>'
 +MEMBERS_SEC+'<section class="beyond" data-amb="wash2"><div class="wrap"><div class="sh sh-c">%s%s</div><div class="by-grid">%s</div>'
 '<p class="by-end ink">Η προσωπική καλλιέργεια δεν περιορίζεται στις σπουδές. Μεγαλώνει μέσα από τις σχέσεις, τις εμπειρίες, την τέχνη, την καθημερινότητα και τη διάθεση να μένουμε ανοιχτοί σε όσα δεν γνωρίζουμε ακόμη. Αυτή η ανθρώπινη πλευρά δεν είναι ξεχωριστή από τη δουλειά μου· είναι μέρος του τρόπου που την κάνω: με ενδιαφέρον για τον άνθρωπο και σεβασμό στη διαφορετικότητα.</p></div></section>'
 + cta_band('Ας γνωριστούμε.','Αν θέλετε να μιλήσουμε για όσα σας απασχολούν, μπορείτε να με καλέσετε ή να μου στείλετε ένα μήνυμα. Η πρώτη επικοινωνία δεν σας δεσμεύει σε τίποτα.'))%(
 crumbs([('poios-eimai.html','Ποιος είμαι')]),kick('Ποιος είμαι'),img('armchair','(max-width: 900px) 92vw, 50vw','',eager=True),
 kick('Η διαδρομή μου'),h2('Από τους αριθμούς,<br>στον άνθρωπο.','mask'),path_html,
 kick('Εκπαίδευση &amp; επαγγελματική ταυτότητα'),h2('Μια εκπαίδευση που δεν τελειώνει.','roll'),creds,img('conf','(max-width: 900px) 80vw, 30vw'),
 kick('Πέρα από την επαγγελματική ιδιότητα'),h2('Ο άνθρωπος πίσω από τον θεραπευτή','light'),beyond)
page('poios-eimai.html','Ποιος είμαι | Γιώργος Κουτσουραδής, Συνθετικός Ψυχοθεραπευτής Περιστέρι',
 'Γνωρίστε τον Γιώργο Κουτσουραδή: Σύμβουλος Ψυχικής Υγείας και Συνθετικός Ψυχοθεραπευτής στο Περιστέρι, με πενταετή εκπαίδευση στο EICP και 2.700+ ώρες εποπτευόμενης πρακτικής.',
 about,crumbs_ld=[('poios-eimai.html','Ποιος είμαι')],og='armchair')

# ===== ΥΠΗΡΕΣΙΕΣ (κόμβος) =====
rows=''.join(('<a class="sv-row" href="%s.html" style="--i:%d"><span class="sv-n">0%d</span>%s<span class="sv-t"><b>%s</b><span>%s</span></span><span class="sv-go">%s</span></a>')%(
  s['slug'],i,i+1,icon(s['icon'],'ic'),s['title'],s['card'],icon('arrow','bi')) for i,s in enumerate(SERVICES))
hub=('<section class="phero" id="top" data-amb="wash"><div class="wrap">%s%s<h1 class="h1 h1-s"><span class="w-name">Υπηρεσίες</span><span class="h1-role">Συμβουλευτική, ψυχοθεραπεία &amp; coaching στο Περιστέρι και online</span></h1>'
 '<p class="display h-words">Κάθε άνθρωπος έχει τη δική του διαδρομή. Η <em>υποστήριξη</em> προσαρμόζεται σε αυτήν.</p></div></section>'
 '<section class="sv-list" data-amb="lines"><div class="wrap">%s</div></section>'
 '<section class="howall" data-amb="dots"><div class="wrap ha-in"><div>%s%s</div><div class="ha-g">'
 '<div class="ha" style="--i:0">%s<b>50 λεπτά</b><span>Η διάρκεια κάθε συνεδρίας, συνήθως μία φορά την εβδομάδα.</span></div>'
 '<div class="ha" style="--i:1">%s<b>Δια ζώσης &amp; online</b><span>Στο γραφείο στο Περιστέρι ή μέσω ασφαλούς τηλεδιάσκεψης.</span></div>'
 '<div class="ha" style="--i:2">%s<b>Εμπιστευτικότητα</b><span>Ό,τι μοιράζεστε προστατεύεται από το επαγγελματικό απόρρητο.</span></div>'
 '<div class="ha" style="--i:3">%s<b>Χωρίς δέσμευση</b><span>Η πρώτη επικοινωνία δεν σας δεσμεύει σε τίποτα.</span></div></div></div></section>'
 + synth_section(False).replace('class="syn"','class="syn syn-s"') + '<section class="aprow"><div class="wrap ap-row">%s</div></section>' + cta_band())%(
 crumbs([('ypiresies.html','Υπηρεσίες')]),kick('Πώς μπορώ να σας υποστηρίξω'),rows,kick('Πώς δουλεύουμε'),h2('Το πλαίσιο, απλά.','mask'),
 icon('clock','ic'),icon('screen','ic'),icon('shield','ic'),icon('phone','ic'),appr_links)
page('ypiresies.html','Υπηρεσίες | Συμβουλευτική & Ψυχοθεραπεία Περιστέρι | Γ. Κουτσουραδής',
 'Ατομική συμβουλευτική, ψυχοθεραπεία ενηλίκων, προσωπική ανάπτυξη, συμβουλευτική τρίτης ηλικίας, επαγγελματική συμβουλευτική και coaching, στο Περιστέρι και online.',
 hub,crumbs_ld=[('ypiresies.html','Υπηρεσίες')])

# ===== ΣΕΛΙΔΕΣ ΥΠΗΡΕΣΙΩΝ =====
ART={ # μικρή γραμμική εικονογράφηση ανά υπηρεσία (σχεδιάζεται)
 'chairs':'<path d="M30 250h260"/><path d="M58 110v138M58 186h64M58 158h52a10 10 0 0 1 0 20M122 186v62"/><path d="M262 110v138M262 186h-64M262 158h-52a10 10 0 0 0 0 20M198 186v62"/><path d="M146 206h28M160 206v42"/><path class="acc" d="M96 92c34-40 94-40 128 0"/><circle class="acc" cx="160" cy="62" r="5"/>',
 'layers':'<path d="M160 60 40 120l120 60 120-60z"/><path d="m40 160 120 60 120-60"/><path class="acc" d="m40 200 120 60 120-60"/>',
 'sprout':'<path d="M160 250v-110"/><path d="M160 140c0-50-36-74-86-74 0 50 36 74 86 74z"/><path class="acc" d="M160 118c0-44 32-68 80-68 0 44-32 68-80 68z"/><path d="M90 250h140"/>',
 'rings':'<circle cx="160" cy="150" r="110"/><circle cx="160" cy="150" r="78"/><circle class="acc" cx="160" cy="150" r="46"/><circle cx="160" cy="150" r="16"/>',
 'compass':'<circle cx="160" cy="150" r="110"/><path class="acc" d="m214 96-30 76-76 30 30-76z"/><path d="M160 30v20M160 250v20M40 150h20M260 150h20"/>',
 'steps':'<path d="M40 250h60v-50h60v-50h60v-50h60"/><path class="acc" d="m250 60 30-30 30 30M280 30v70"/>',
}
def svc_page(s):
    tp=''.join('<div class="tp tilt" style="--i:%d"><span class="tp-n">0%d</span><h3>%s</h3><p>%s</p></div>'%(i,i+1,t,d) for i,(t,d) in enumerate(s['topics']))
    pil=''.join('<div class="pil" style="--i:%d"><span class="pil-l"></span><h3>%s</h3><p>%s</p></div>'%(i,t,d) for i,(t,d) in enumerate(s['pillars']))
    gn=''.join('<li style="--i:%d"><svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="17"/><path pathLength="1" d="m13 20.5 5 5 9-10"/></svg><b>%s</b><span>%s</span></li>'%(i,t,d) for i,(t,d) in enumerate(s['gains']))
    others=''.join('<a href="%s.html">%s<span>%s</span></a>'%(o['slug'],icon(o['icon'],'ic'),o['title']) for o in SERVICES if o is not s)
    split=''
    if s.get('split'):
        split='<section class="split2" data-amb="lines2"><div class="wrap sp-g">%s</div></section>'%''.join('<div class="sp tilt" style="--i:%d"><span class="tag">%s</span><h3>%s</h3><p>%s</p></div>'%(i,'Για εσάς' if i==0 else 'Για επαγγελματίες &amp; οργανισμούς',t,d) for i,(t,d) in enumerate(s['split']))
    extra=''
    if s.get('book'):
        extra=('<section class="xbook" data-amb="rings"><div class="wrap xb-in"><a class="xb-cv" href="vivlia.html">%s</a><div>%s<p class="xb-t lc" data-fx="mask">Χαρτογραφώντας τη σταδιοδρομία</p><p class="rv">Θεωρία, αυτογνωσία και πράξη στη σύγχρονη συμβουλευτική. Το βιβλίο που έγραψα με την Ειρήνη Καρακασίδου για το πώς χτίζεται σήμερα μια σταδιοδρομία με νόημα.</p>%s</div></div></section>')%(img('book','200px','',lb=False),kick('Από το έργο μου'),btn('vivlia.html','Δείτε το βιβλίο','btn btn-ghost'))
    if s.get('article'):
        extra=('<section class="xbook" data-amb="rings"><div class="wrap xb-in"><a class="xb-ic" href="arthro-aftosympnonia-triti-ilikia.html">%s</a><div>%s<p class="xb-t lc" data-fx="mask">Αυτοσυμπόνια στην τρίτη ηλικία</p><p class="rv">Μια πιο ήπια σχέση με τον εαυτό στα χρόνια της ωρίμανσης: τι σημαίνει, τι λέει η έρευνα και γιατί δεν είναι ακόμη μια «συνταγή» για το πώς πρέπει να γερνά κανείς.</p>%s</div></div></section>')%(icon('pen','ic'),kick('Από τα κείμενά μου'),btn('arthro-aftosympnonia-triti-ilikia.html','Διαβάστε το άρθρο','btn btn-ghost'))
    when=''.join('<p class="ink">%s</p>'%p for p in s['when'])
    body=('<section class="phero sv-hero" id="top" data-amb="wash"><div class="wrap sh-in"><div class="ph-txt">%s%s'
     '<h1 class="h1 h1-s"><span class="w-name">%s</span><span class="h1-role">με τον Γιώργο Κουτσουραδή · Περιστέρι &amp; online</span></h1>'
     '<p class="hero-lead h-up">%s</p><div class="hero-cta h-up">%s<a class="tl" href="tel:%s">%s</a></div></div>'
     '<div class="sv-art"><svg class="art" viewBox="0 0 320 300" aria-hidden="true" fill="none">%s</svg>%s</div></div></section>'
     '<section class="when" data-amb="lines"><div class="wrap wh-in"><div class="wh-txt">%s%s%s</div><figure class="wh-ph"><div class="pol">%s</div></figure></div></section>'
     '<section class="topics" data-amb="dots"><div class="wrap"><div class="sh">%s%s</div><div class="tp-grid">%s</div></div></section>'
     '%s'
     '<section class="how" data-amb="profiles"><div class="wrap"><div class="sh sh-c">%s%s<p class="sh-p rv">%s</p></div><div class="pil-g">%s</div></div></section>'
     '<section class="gain" data-amb="rings"><div class="wrap gn-in"><div>%s%s<p class="ink">%s</p></div><ul class="gn">%s</ul></div></section>'
     '%s'
     '<section class="faq" data-amb="dots2"><div class="wrap faq-in"><div class="faq-h">%s%s<p class="rv faq-note">Δεν βρίσκετε την απάντηση που ψάχνετε; <a href="epikoinonia.html">Επικοινωνήστε μαζί μου.</a></p></div><div class="faq-l">%s</div></div></section>'
     + cta_band() +
     '<section class="others"><div class="wrap"><p class="kick">Άλλες υπηρεσίες</p><div class="ot-g">%s</div></div></section>')%(
     crumbs([('ypiresies.html','Υπηρεσίες'),(s['slug']+'.html',s['title'])]),kick('Υπηρεσίες'),s['title'],s['lead'],
     btn('epikoinonia.html#rantevou','Κλείστε ραντεβού','btn'),TEL,PHONE,ART[s['icon']],mark('mk sv-mk'),
     kick('Πότε'),h2(s['when_h'],'mask'),when,img(s['photo'],'(max-width: 900px) 92vw, 40vw'),
     kick('Θεματολογία'),h2(s['topics_h'],'roll'),tp,split,
     kick('Η προσέγγιση'),h2(s['how_h'],'centre'),s['how'],pil,
     kick('Τι κερδίζετε'),h2(s['gain_h'],'light'),s['gain_p'],gn,extra,
     kick('Συχνές ερωτήσεις'),h2('Καλό είναι να γνωρίζετε','mask'),faq(s['faq'],True),others)
    page(s['slug']+'.html',s['seo_t'],s['seo_d'],body,ld=[faq_ld(s['faq']),{"@type":"Service","name":s['title'],"serviceType":s['title'],"description":s['lead'],"provider":{"@id":"#giorgos"},"areaServed":["Περιστέρι","Αθήνα","Online"]}],
         crumbs_ld=[('ypiresies.html','Υπηρεσίες'),(s['slug']+'.html',s['title'])],og=s['photo'],cur=s['slug']+'.html')
for s in SERVICES: svc_page(s)

# ===== ΠΡΟΣΕΓΓΙΣΕΙΣ =====
OUT6=[('Αυτογνωσία','Μια βαθύτερη κατανόηση του εαυτού σας.'),('Αυτοεκτίμηση','Περισσότερη εμπιστοσύνη στις δυνατότητές σας.'),('Υγιέστερες σχέσεις','Πιο ουσιαστικές σχέσεις με τους άλλους.'),
      ('Συναισθηματική αυθεντικότητα','Επαφή με ό,τι πραγματικά νιώθετε.'),('Διαχείριση δυσκολιών','Πιο αποτελεσματικοί τρόποι αντιμετώπισης.'),('Προσωπική ανάπτυξη','Πορεία προς μεγαλύτερη ισορροπία και πληρότητα.')]
DIAG={
 'synthetiki-prosengisi':'<svg class="dg dg-syn" viewBox="0 0 400 400"><circle class="d1" cx="200" cy="158" r="92"/><circle class="d2" cx="146" cy="248" r="92"/><circle class="d3" cx="254" cy="248" r="92"/><circle class="dc" cx="200" cy="218" r="24"/><text class="dt" x="200" y="40">Υπαρξιακή</text><text class="dt" x="116" y="372">Προσωποκεντρική</text><text class="dt" x="290" y="364">Γνωσιακή</text><text class="dt" x="290" y="384">Συμπεριφορική</text></svg>',
 'yparxiaki-prosengisi':'<svg class="dg dg-ex" viewBox="0 0 400 380"><circle class="dl" cx="200" cy="190" r="140" pathLength="1"/><circle class="dc" cx="200" cy="190" r="40"/><text class="tc" x="200" y="195">Ύπαρξη</text>'+''.join('<g class="dn" style="--i:%d"><circle cx="%d" cy="%d" r="7"/><text x="%d" y="%d">%s</text></g>'%(i,x,y,tx,ty,''.join('<tspan x="%d" dy="%s">%s</tspan>'%(tx,'0' if k==0 else '1.15em',w) for k,w in enumerate(t.split('|')))) for i,(x,y,tx,ty,t) in enumerate([(200,50,200,30,'Νόημα'),(340,190,340,220,'Ελευθερία &amp;|ευθύνη'),(200,330,200,362,'Περατότητα'),(60,190,60,220,'Σχέση &amp;|μοναξιά')]))+'</svg>',
 'prosopokentriki-prosengisi':'<svg class="dg dg-pc" viewBox="0 0 400 380"><path class="dl" pathLength="1" d="M200 50 345 300H55z"/><circle class="dc" cx="200" cy="215" r="34"/><text class="tc" x="200" y="220">Ο άνθρωπος</text>'+''.join('<g class="dn" style="--i:%d"><circle cx="%d" cy="%d" r="8"/><text x="%d" y="%d">%s</text></g>'%(i,x,y,tx,ty,t) for i,(x,y,tx,ty,t) in enumerate([(200,50,200,30,'Ενσυναίσθηση'),(345,300,330,334,'Γνησιότητα'),(55,300,80,334,'Άνευ όρων αποδοχή')]))+'</svg>',
 'gnosiaki-symperiforiki-prosengisi':'<svg class="dg dg-cbt" viewBox="0 0 400 380"><circle class="dl" cx="200" cy="200" r="120" pathLength="1"/><g class="orb"><circle class="od" cx="200" cy="80" r="7"/></g>'+''.join('<g class="dn" style="--i:%d"><circle class="nb" cx="%d" cy="%d" r="44"/><text x="%d" y="%d">%s</text></g>'%(i,x,y,x,y+5,t) for i,(x,y,t) in enumerate([(200,80,'Σκέψεις'),(304,260,'Συναισθήματα'),(96,260,'Συμπεριφορές')]))+'</svg>',
}
APX={
 'synthetiki-prosengisi':dict(kw=['Θεραπευτική σχέση στο κέντρο','Προσαρμογή στον άνθρωπο','Ενιαίο πλαίσιο, όχι «μείγμα»','Σεβασμός στην προσωπική ιστορία'],
  p=['Η συνθετική ψυχοθεραπεία ξεκινά από μια απλή διαπίστωση: κανένα θεωρητικό μοντέλο δεν χωράει ολόκληρο τον άνθρωπο. Αντί να προσαρμόζεται ο άνθρωπος σε μια μέθοδο, η θεραπεία προσαρμόζεται σε εκείνον.',
     'Συνδυάζει με συνέπεια έννοιες και τεχνικές από διαφορετικές θεραπευτικές παραδόσεις, όπως η υπαρξιακή, η προσωποκεντρική και η γνωσιακή συμπεριφορική, μέσα σε ένα ενιαίο πλαίσιο. Στο κέντρο του βρίσκεται η θεραπευτική σχέση.',
     'Αυτή είναι και η βάση της δικής μου εκπαίδευσης: πέντε χρόνια στη Συμβουλευτική και τη Συνθετική Ψυχοθεραπεία, στο European Institute of Counselling &amp; Psychotherapy.'],
  q='Η θεραπεία δεν μπορεί να είναι ίδια για όλους.'),
 'yparxiaki-prosengisi':dict(kw=['Νόημα','Ελευθερία και ευθύνη','Αυθεντικότητα','Περατότητα και χρόνος'],
  p=['Η υπαρξιακή προσέγγιση στρέφεται στα μεγάλα ερωτήματα που συναντά κάθε άνθρωπος: τι δίνει νόημα στη ζωή μου, πώς χρησιμοποιώ την ελευθερία μου, πώς στέκομαι απέναντι στην αβεβαιότητα, στη μοναξιά και στο πεπερασμένο του χρόνου.',
     'Δεν βλέπει τη δυσκολία μόνο ως «σύμπτωμα» που πρέπει να εξαλειφθεί, αλλά ως μέρος του τρόπου με τον οποίο ζούμε. Στη θεραπεία, αυτό σημαίνει χώρο για να σκεφτείτε τις επιλογές σας, τις αξίες σας και το πώς θέλετε να ζείτε.',
     'Είναι μια ματιά που με επηρεάζει βαθιά, και φαίνεται και στα κείμενά μου, όπως στο άρθρο για την <a href="arthro-aftosympnonia-triti-ilikia.html">αυτοσυμπόνια στην τρίτη ηλικία</a>.'],
  q='Το ζητούμενο δεν είναι μόνο να αντέξουμε τη ζωή, αλλά να τη ζήσουμε με νόημα.'),
 'prosopokentriki-prosengisi':dict(kw=['Ενσυναίσθηση','Άνευ όρων αποδοχή','Γνησιότητα','Εμπιστοσύνη στην τάση για ανάπτυξη'],
  p=['Η προσωποκεντρική προσέγγιση, όπως τη διατύπωσε ο Carl Rogers, εμπιστεύεται ότι κάθε άνθρωπος έχει μέσα του την τάση να μεγαλώνει και να εξελίσσεται, όταν βρεθεί στις κατάλληλες συνθήκες.',
     'Αυτές οι συνθήκες είναι τρεις: η ενσυναίσθηση, δηλαδή η προσπάθεια να κατανοήσω τον κόσμο σας όπως τον βιώνετε· η άνευ όρων αποδοχή, χωρίς κριτική· και η γνησιότητα, μια σχέση αληθινή και όχι «ρόλος».',
     'Ο θεραπευόμενος είναι ο ειδικός της δικής του ζωής. Ο θεραπευτής δεν δίνει έτοιμες απαντήσεις· συνοδεύει.'],
  q='Ό,τι γίνεται αποδεκτό μπορεί να αλλάξει.'),
 'gnosiaki-symperiforiki-prosengisi':dict(kw=['Σκέψεις, συναισθήματα, συμπεριφορές','Σαφείς στόχοι','Πρακτικά εργαλεία','Συνεργασία'],
  p=['Η γνωσιακή συμπεριφορική προσέγγιση ξεκινά από τη σύνδεση ανάμεσα σε σκέψεις, συναισθήματα και συμπεριφορές: ο τρόπος που ερμηνεύουμε μια κατάσταση επηρεάζει το πώς νιώθουμε και το τι κάνουμε.',
     'Στη θεραπεία αναγνωρίζουμε σκέψεις και μοτίβα που δεν βοηθούν, τα εξετάζουμε μαζί και δοκιμάζουμε πιο λειτουργικούς τρόπους σκέψης και δράσης. Η δουλειά είναι δομημένη, συνεργατική και συχνά συνεχίζεται με μικρές ασκήσεις ανάμεσα στις συνεδρίες.',
     'Είναι μια από τις πιο ερευνημένες θεραπευτικές προσεγγίσεις, ιδιαίτερα για το άγχος και τη διάθεση. Στη συνθετική δουλειά τη χρησιμοποιώ όπου εξυπηρετεί τους δικούς σας στόχους.'],
  q='Δεν αλλάζουμε πάντα αυτό που συμβαίνει· μπορούμε όμως να αλλάξουμε τον τρόπο που το ερμηνεύουμε.'),
}
for i,(slug,t,d) in enumerate(APPR):
    a=APX[slug]
    oc=''.join('<div class="tp tilt" style="--i:%d"><span class="tp-n">0%d</span><h3>%s</h3><p>%s</p></div>'%(j,j+1,x,y) for j,(x,y) in enumerate(OUT6))
    kw=''.join('<li style="--i:%d">%s</li>'%(j,k) for j,k in enumerate(a['kw']))
    oth=''.join('<a class="ap" href="%s.html"><span class="ap-d d%d"></span><b>%s</b><span>%s</span>%s</a>'%(s2,k,t2,d2,icon('arrow','bi')) for k,(s2,t2,d2) in enumerate(APPR) if s2!=slug)
    body=('<section class="phero apx-hero" id="top" data-amb="wash"><div class="wrap sh-in"><div class="ph-txt">%s%s<h1 class="h1 h1-s"><span class="w-name">%s</span><span class="h1-role">στη θεραπευτική δουλειά του Γιώργου Κουτσουραδή</span></h1>'
     '<p class="display h-words">%s</p></div><div class="apx-dg">%s</div></div></section>'
     '<section class="apx-body" data-amb="lines"><div class="wrap narrow">%s<ul class="kw">%s</ul><p class="pull rv">%s</p></div></section>'
     '<section class="topics" data-amb="dots"><div class="wrap"><div class="sh">%s%s</div><div class="tp-grid">%s</div></div></section>'
     '<section class="aprow"><div class="wrap"><p class="kick">Οι άλλες προσεγγίσεις</p><div class="ap-row ap3">%s</div></div></section>'+cta_band())%(
     crumbs([('index.html#prosengisi','Η προσέγγισή μου'),(slug+'.html',t)]),kick('Η θεραπευτική μου προσέγγιση'),t,d,DIAG[slug],
     ''.join('<p class="ink">%s</p>'%p for p in a['p']),kw,a['q'],kick('Τι μπορείτε να κερδίσετε'),h2('Όσα καλλιεργούνται μέσα στη θεραπεία','roll'),oc,oth)
    page(slug+'.html','%s | Γιώργος Κουτσουραδής, Ψυχοθεραπευτής Περιστέρι'%t,'%s %s'%(d,'Πώς την αξιοποιεί ο Γιώργος Κουτσουραδής στη συνθετική ψυχοθεραπεία, στο Περιστέρι και online.'),body,
         crumbs_ld=[('index.html#prosengisi','Η προσέγγισή μου'),(slug+'.html',t)])

# ===== ΤΟ ΕΡΓΟ ΜΟΥ =====
wk=('<section class="phero" id="top" data-amb="wash"><div class="wrap">%s%s<h1 class="h1 h1-s"><span class="w-name">Το έργο μου</span><span class="h1-role">Βιβλία, συνέδρια και κείμενα του Γιώργου Κουτσουραδή</span></h1>'
 '<p class="display h-words">Η κλινική δουλειά <em>συνομιλεί</em> με την έρευνα και τη γραφή.</p></div></section>'
 '<section class="wk3" data-amb="lines"><div class="wrap wk3-g">'
 '<a class="w3 tilt" href="synedria.html" style="--i:0"><span class="w3-n">01</span>%s<h2>Συνέδρια</h2><p>Εισηγήσεις και ανακοινώσεις σε πανελλήνια συνέδρια: Αναπτυξιακής Ψυχολογίας (Θεσσαλονίκη, 2026), Συμβουλευτικής Ψυχολογίας (Πάτρα, 2025 · Αθήνα, 2023) και Ψυχολογικής Έρευνας (Ιωάννινα, 2025).</p><span class="sc-go">Δείτε τα %s</span></a>'
 '<a class="w3 tilt" href="vivlia.html" style="--i:1"><span class="w3-n">02</span>%s<h2>Βιβλία</h2><p>«Χαρτογραφώντας τη σταδιοδρομία: Θεωρία, αυτογνωσία και πράξη στη σύγχρονη συμβουλευτική», Εκδόσεις Παρισιάνου, 2025.</p><span class="sc-go">Το βιβλίο %s</span></a>'
 '<a class="w3 tilt" href="arthra.html" style="--i:2"><span class="w3-n">03</span>%s<h2>Κείμενα &amp; Άρθρα</h2><p>Κείμενα για την ψυχοθεραπεία, τη συμβουλευτική, την προσωπική ανάπτυξη και τη σύγχρονη ανθρώπινη εμπειρία.</p><span class="sc-go">Διαβάστε %s</span></a>'
 '</div></section>'+cta_band())%(crumbs([('to-ergo-mou.html','Το έργο μου')]),kick('Επιστημονικό έργο'),icon('mic','ic'),icon('arrow','bi'),icon('book','ic'),icon('arrow','bi'),icon('pen','ic'),icon('arrow','bi'))
page('to-ergo-mou.html','Το έργο μου: βιβλία, συνέδρια, άρθρα | Γιώργος Κουτσουραδής','Το επιστημονικό έργο του Γιώργου Κουτσουραδή: το βιβλίο «Χαρτογραφώντας τη σταδιοδρομία», ανακοινώσεις σε πανελλήνια συνέδρια ψυχολογίας και κείμενα.',wk,crumbs_ld=[('to-ergo-mou.html','Το έργο μου')])

CONF=[dict(y='2026',n='8ο Πανελλήνιο Συνέδριο Αναπτυξιακής Ψυχολογίας',th='«τὰ πάντα ῥεῖ…»',kind='Εισήγηση',
   pl='Θεσσαλονίκη · 15–18 Οκτωβρίου 2026',au='Γιώργος Κουτσουραδής · Ειρήνη Καρακασίδου, Επίκουρη Καθηγήτρια Παντείου Πανεπιστημίου',
   t='Παρεμβάσεις συμβουλευτικής ψυχολογίας στην τρίτη ηλικία, με έμφαση στη στήριξη των αναπτυξιακών διεργασιών και της ψυχοσυναισθηματικής προσαρμογής κατά την ύστερη ενήλικη ζωή',
   s='Η παρούσα εισήγηση επικεντρώνεται στις παρεμβάσεις συμβουλευτικής ψυχολογίας στην τρίτη ηλικία, με έμφαση στη στήριξη των αναπτυξιακών διεργασιών και της ψυχοσυναισθηματικής προσαρμογής κατά την ύστερη ενήλικη ζωή. Η τρίτη ηλικία προσεγγίζεται ως ένα ενεργό αναπτυξιακό στάδιο, το οποίο χαρακτηρίζεται από σημαντικές ψυχοκοινωνικές μεταβάσεις, επαναπροσδιορισμό ρόλων και αυξημένη ανάγκη προσαρμογής σε αλλαγές που αφορούν την υγεία, τις κοινωνικές σχέσεις και τη βιωμένη εμπειρία του χρόνου.',
   more=['Οι παρεμβάσεις που παρουσιάζονται υλοποιούνται σε κοινοτικά πλαίσια, όπως οι Λέσχες Φιλίας και τα ΚΑΠΗ των Δήμων, και έχουν πολυδιάστατο χαρακτήρα, καθώς στοχεύουν στην ενίσχυση της ψυχικής ανθεκτικότητας, την υποστήριξη στη διαχείριση απωλειών και τη διευκόλυνση της συναισθηματικής έκφρασης και αυτογνωσίας. Μέσα από ατομικές και ομαδικές συναντήσεις εφαρμόζονται τεχνικές ενεργητικής ακρόασης, ενδυνάμωσης, ενίσχυσης της αυτοεκτίμησης και καλλιέργειας δεξιοτήτων προσαρμογής, οι οποίες υποστηρίζουν τη διατήρηση της ψυχικής ισορροπίας και της αναπτυξιακής συνέχειας.',
         'Ιδιαίτερη έμφαση δίνεται στη δημιουργία ενός ασφαλούς και αποδοτικού θεραπευτικού πλαισίου, όπου οι ηλικιωμένοι ενθαρρύνονται να μοιραστούν εμπειρίες, να επεξεργαστούν τις αλλαγές που συνοδεύουν τη γήρανση και να ενισχύσουν το αίσθημα του ανήκειν και της κοινωνικής σύνδεσης. Η συμβουλευτική προσέγγιση είναι κυρίως προσωποκεντρική, εστιάζοντας στις ιδιαίτερες ανάγκες, τις προσωπικές διαδρομές και τις αξίες των συμμετεχόντων, ενώ η αξιολόγηση της αποτελεσματικότητας των παρεμβάσεων βασίζεται κυρίως σε ποιοτικά δεδομένα, όπως προσωπικές αφηγήσεις και βιωματικές μαρτυρίες. Οι παρεμβάσεις συμβουλευτικής ψυχολογίας στην τρίτη ηλικία αναδεικνύονται ως ουσιαστικός παράγοντας ενίσχυσης της ψυχοσυναισθηματικής προσαρμογής και της ενεργού συμμετοχής των ηλικιωμένων στην κοινότητα.'],
   kw='τρίτη ηλικία, παρεμβάσεις συμβουλευτικής, αναπτυξιακές διεργασίες, ψυχοσυναισθηματική προσαρμογή, ενεργός γήρανση',
   ph=['th_eis','th_om','th_vima'],logo='thess'),
  dict(y='2025',n='9ο Πανελλήνιο Συνέδριο Συμβουλευτικής Ψυχολογίας',th='',kind='Εισήγηση',
   pl='Πανεπιστήμιο Πατρών, Πάτρα · 6–9 Νοεμβρίου 2025',au='Γιώργος Κουτσουραδής',
   t='Παρεμβάσεις συμβουλευτικής ψυχολογίας σε άτομα τρίτης ηλικίας',
   s='Οι παρεμβάσεις συμβουλευτικής ψυχολογίας σε άτομα τρίτης ηλικίας που υλοποιούνται σε Λέσχες Φιλίας έχουν πολυδιάστατο χαρακτήρα και αποσκοπούν στην ενίσχυση της ψυχικής ανθεκτικότητας, την υποστήριξη στη διαχείριση απωλειών (όπως η απώλεια συντρόφου, φίλων ή ρόλων), καθώς και στην προώθηση της κοινωνικής ένταξης και ενεργού γήρανσης. Μέσα από ατομικές και ομαδικές συναντήσεις, εφαρμόζονται τεχνικές ενδυνάμωσης, ενεργητικής ακρόασης, ενίσχυσης της αυτοεκτίμησης και καλλιέργειας της αυτογνωσίας.',
   more=['Οι συμμετέχοντες ενθαρρύνονται να μοιραστούν εμπειρίες, να εκφράσουν συναισθήματα και να επεξεργαστούν τις αλλαγές που σχετίζονται με τη γήρανση, ενισχύοντας παράλληλα το αίσθημα του ανήκειν και της αλληλοϋποστήριξης.',
         'Η προσέγγιση είναι προσωποκεντρική, εστιάζοντας στις ιδιαίτερες ανάγκες, τις προσωπικές διαδρομές και τις αξίες των ηλικιωμένων. Η αξιολόγηση της αποτελεσματικότητας της παρέμβασης προβλέπεται να βασιστεί κυρίως σε ποιοτικά δεδομένα, μέσα από προσωπικές αφηγήσεις, συνεντεύξεις και βιωματικές μαρτυρίες των συμμετεχόντων, με στόχο την αποτύπωση των αλλαγών στην ψυχοσυναισθηματική κατάσταση και τη βελτίωση της καθημερινής ζωής τους. Η ενδυνάμωση των ηλικιωμένων μέσω τέτοιων δράσεων δεν αφορά μόνο την ατομική ευημερία, αλλά συμβάλλει και στη δημιουργία πιο συνεκτικών και υποστηρικτικών κοινοτήτων.'],
   ph=['pa_om','pa_eis'],logo='patra'),
  dict(y='2025',n='Συμπόσιο της Ε.ΣΥ.ΟΜ · 9ο Πανελλήνιο Συνέδριο Συμβουλευτικής Ψυχολογίας',th='«Ομαδική και Ατομική Συμβουλευτική Ομοτίμων: εφαρμοσμένα παραδείγματα με διαφορετικές ομάδες στόχο»',kind='Συμπόσιο · 4η εισήγηση',
   pl='Πάτρα · Νοέμβριος 2025',au='Γιώργος Κουτσουραδής · Γιώργος Σύρακας · Αγγελική Σωτηρίου, Ελληνική Επιστημονική Εταιρεία Συμβουλευτικής Ομηλίκων (Ε.ΣΥ.ΟΜ)',
   t='Ατομική Συμβουλευτική Ομοτίμων',
   s='Η Συμβουλευτική Ομοτίμων αποτελεί μια μορφή ενδυνάμωσης και ψυχοκοινωνικής υποστήριξης, που παρέχεται από εκπαιδευμένους εθελοντές, συχνά μη επαγγελματίες, με δεξιότητες ενεργητικής ακρόασης, συμβουλευτικής και αποτελεσματικής επικοινωνίας. Βασίζεται στην ανθρώπινη ανάγκη για σύνδεση με άτομα που βρίσκονται σε παρόμοια φάση ζωής ή έχουν κοινές εμπειρίες, ανησυχίες και προκλήσεις.',
   more=['Αν και η ομαδική συμβουλευτική αποτελεί βασικό άξονα της δράσης της Ελληνικής Επιστημονικής Εταιρείας Συμβουλευτικής Ομηλίκων (Ε.ΣΥ.ΟΜ), τελευταία αναπτύσσεται δυναμικά και η ατομική Συμβουλευτική Ομηλίκων/Ομοτίμων σε ενήλικα άτομα. Στην Ελλάδα, η ατομική Συμβουλευτική Ομοτίμων είχε ξεκινήσει να εφαρμόζεται από το 1995 στο Συμβουλευτικό Κέντρο Ομηλίκων του ΕΚΠΑ, όπου εκπαιδευμένοι φοιτητές προσέφεραν ατομική ή ομαδική συμβουλευτική σε συμφοιτητές τους. Η ανάγκη κάποιων συμβουλευόμενων για ατομική, πιο εστιασμένη υποστήριξη σε συνδυασμό με τη διάθεση των μελών της Ε.ΣΥ.ΟΜ να προσφέρουν υποστήριξη μέσα από τις προσωπικές τους εμπειρίες, οδήγησε στη θεσμοθέτηση της ατομικής πρακτικής.',
         'Στην παρουσίαση αναπτύσσονται ο τρόπος με τον οποίο εφαρμόζεται η δράση σε συγκεκριμένες θεματικές περιοχές (π.χ. χωρισμένοι γονείς, νέοι σε επαγγελματική μετάβαση, γονείς ενήλικων παιδιών κ.ά.), η διαδικασία συντονισμού της δράσης, από την υποβολή αιτημάτων μέσω της ιστοσελίδας της Ε.ΣΥ.ΟΜ έως τη σύζευξη συμβουλευόμενου και συμβούλου, το εγχειρίδιο Ατομικής Συμβουλευτικής Ομοτίμων, το οποίο δημιουργήθηκε βάσει διεθνούς βιβλιογραφίας, και τέλος η ομαδική εποπτεία και ο ρόλος της για τη διασφάλιση της ποιότητας της υποστήριξης, της διαρκούς ανατροφοδότησης και βελτίωσης της πρακτικής. Η παρουσίαση στοχεύει να αναδείξει την αξία της ατομικής συμβουλευτικής μεταξύ ομοτίμων ως εργαλείο πρόληψης, ενδυνάμωσης και ανάπτυξης, σε ένα πλήρως δομημένο και εποπτευόμενο πλαίσιο.',
         '<b>Το συμπόσιο.</b> Η Συμβουλευτική Ομηλίκων/Ομοτίμων (Σ.Ο) είναι ένα σύστημα προσφοράς και αποδοχής βοήθειας μεταξύ ατόμων σε παρόμοια φάση ζωής και με παρόμοια προβλήματα. Στηρίζεται στις βασικές αρχές του αμοιβαίου σεβασμού, της υπευθυνότητας και της κατανόησης. Η Ε.ΣΥ.ΟΜ, στα 10 και πλέον χρόνια της λειτουργίας της, υποστηρίζει τη δημιουργία και λειτουργία προγραμμάτων Συμβουλευτικής Ομοτίμων, ομαδικών και ατομικών. Στο συμπόσιο παρουσιάστηκαν το πρόγραμμα «We Support our MS» (WSOMS) για ασθενείς με Πολλαπλή Σκλήρυνση, η μεθοδολογία της Ε.ΣΥ.ΟΜ για την ενδυνάμωση υπαρχόντων προγραμμάτων Σ.Ο σε διάφορους φορείς, μια ομάδα ομοτίμων για ψυχοθεραπευτές και, τέλος, η ατομική Συμβουλευτική Ομοτίμων.'],
   kw='Ατομική Συμβουλευτική Ομοτίμων, Ε.ΣΥ.ΟΜ, εγχειρίδιο δράσης, θεματικές υποστήριξης, εποπτεία',
   ph=['es_dia','es_om','es_pan'],logo=None),
  dict(y='2025',n='19ο Πανελλήνιο Συνέδριο Ψυχολογικής Έρευνας',th='«Μοιραζόμαστε τις ομοιότητές μας, γιορτάζουμε τις διαφορές μας»',
   pl='Συνεδριακό Κέντρο «Κάρολος Παπούλιας», Πανεπιστήμιο Ιωαννίνων · 7–11 Μαΐου 2025',t='Πρόγραμμα Παρέμβασης Συμβουλευτικής Ψυχολογίας σε ενήλικες με ψυχοκοινωνικές δυσκολίες, λήπτες φαρμακευτικής αγωγής',
   s='Η εργασία παρουσιάζει ένα ομαδικό ψυχοεκπαιδευτικό πρόγραμμα Συμβουλευτικής Ψυχολογίας για 16 ενήλικες ενός Κέντρου Ημέρας στην Αττική: οκτώ εβδομαδιαίες συναντήσεις των 50 λεπτών, με ασκήσεις αυτοσυμπόνιας, ενσυνειδητότητας και ευγνωμοσύνης, για τη σχέση με τον εαυτό και με τους άλλους.',
   more=['Τα προγράμματα κοινωνικοποίησης απευθύνονται σε ενήλικες με κοινωνικές δυσκολίες που χρειάζονται καθημερινή απασχόληση. Στηρίζουν τη συνέχεια της θεραπείας και την πρόληψη των υποτροπών, την ανάπτυξη δεξιοτήτων, την κοινωνική ένταξη και την επαγγελματική αποκατάσταση, την αντιμετώπιση του στίγματος και της απόσυρσης, και το δικαίωμα αυτών των ανθρώπων να είναι ενεργά μέλη της κοινωνίας.',
         'Η έρευνα στοχεύει στην ενίσχυση της αυτοσυμπόνιας, του σχετίζεσθαι και της ενσυνειδητότητας, και εξετάζει τον ρόλο της Συμβουλευτικής Ψυχολογίας και της θετικότητας σε αυτόν τον πληθυσμό: πώς επηρεάζονται, πριν και μετά το πρόγραμμα, τα θετικά και αρνητικά συναισθήματα, η επίγνωση προσοχής, η ευγνωμοσύνη και η ποιότητα ζωής των συμμετεχόντων.',
         'Το πρόγραμμα περιλαμβάνει ασκήσεις αυτοσυμπόνιας, ενσυνειδητότητας, ευγνωμοσύνης, απόλαυσης θετικών εμπειριών και αξιοποίησης των δυνάμεων του χαρακτήρα. Έγινε σε δύο ομάδες των οκτώ ατόμων. Η αξιολόγηση έγινε με τέσσερα ψυχομετρικά εργαλεία, πριν, αμέσως μετά και έξι μήνες μετά την παρέμβαση. Κατά την υποβολή της περίληψης, η έρευνα βρισκόταν σε εξέλιξη.'],
   ph=['p2025'],logo='ioannina',kind='Αναρτημένη ανακοίνωση',au='Γιώργος Κουτσουραδής · Ειρήνη Καρακασίδου'),
  dict(y='2023',n='8ο Πανελλήνιο Συνέδριο Συμβουλευτικής Ψυχολογίας & 3ο Πανελλήνιο Συνέδριο Θετικής Ψυχολογίας',th='«Συναντήσεις, Αφηγήσεις, Προκλήσεις»',
   pl='Πάντειο Πανεπιστήμιο Κοινωνικών και Πολιτικών Επιστημών, Αθήνα · 9–12 Νοεμβρίου 2023',t='Πρόγραμμα παρεμβάσεων Θετικής Ψυχολογίας σε ενήλικες με ψυχοκοινωνικές δυσκολίες, λήπτες φαρμακευτικής αγωγής',
   s='Η αναρτημένη ανακοίνωση παρουσιάζει ένα ψυχοεκπαιδευτικό πρόγραμμα Θετικής Ψυχολογίας για 16 ενήλικες σε Κέντρο Ημέρας στην Αττική. Σε οκτώ εβδομαδιαίες συναντήσεις, οι συμμετέχοντες εξασκήθηκαν στην αυτοσυμπόνια, στην ενσυνειδητότητα και στην ευγνωμοσύνη, στην απόλαυση θετικών εμπειριών και στην αξιοποίηση των δυνάμεων του χαρακτήρα τους.',
   more=['Τα προγράμματα κοινωνικοποίησης απευθύνονται σε ενήλικες με ψυχοκοινωνικές δυσκολίες και προσφέρουν καθημερινή απασχόληση, ανάπτυξη δεξιοτήτων, κοινωνική ένταξη και επαγγελματική αποκατάσταση. Στόχος τους είναι επίσης η συνέχεια της θεραπείας, η πρόληψη των υποτροπών, η αντιμετώπιση του στίγματος και της κοινωνικής απόσυρσης.',
         'Η μελέτη αφορούσε ενήλικες με ψυχοκοινωνικές δυσκολίες που λάμβαναν φαρμακευτική αγωγή. Σκοπός ήταν η ενίσχυση της αυτοσυμπόνιας, της ενσυνειδητότητας και της σύνδεσης με τους άλλους, και η διερεύνηση των μεταβολών στα θετικά και αρνητικά συναισθήματα, στην επίγνωση της προσοχής, στην ευγνωμοσύνη και στην ποιότητα ζωής.',
         'Δύο ομάδες των οκτώ ατόμων, οκτώ εβδομαδιαίες συναντήσεις των 50 λεπτών. Η αξιολόγηση έγινε με τέσσερα ψυχομετρικά εργαλεία σε τρεις στιγμές: πριν από την παρέμβαση, αμέσως μετά και έξι μήνες αργότερα.'],
   ph=['p2023','conf'],logo=None,kind='Αναρτημένη ανακοίνωση',au='Γιώργος Κουτσουραδής · Ειρήνη Καρακασίδου')]
def conf_html(c,i):
    phs=''.join('<figure class="cf-ph">%s</figure>'%img(p,'(max-width: 900px) 44vw, 220px') for p in c['ph'])
    more=''.join('<p>%s</p>'%m for m in c['more'])
    logo=('<div class="cf-logo">%s</div>'%img(c['logo'],'(max-width: 900px) 80vw, 420px')) if c['logo'] else ''
    if c.get('kw'): more+='<p class="cf-kw"><b>Λέξεις-κλειδιά:</b> %s</p>'%c['kw']
    th=('<p class="cf-th">%s</p>'%c['th']) if c['th'] else ''
    return ('<article class="cf" style="--i:%d"><div class="cf-y"><span>%s</span></div><div class="cf-b">%s<p class="tag">%s</p><h2 class="cf-n">%s</h2>%s'
     '<p class="cf-pl">%s %s</p><p class="cf-au">%s</p><h3 class="cf-t">«%s»</h3><p class="cf-s ink">%s</p>'
     '<details class="qa cf-more"><summary><span>Διαβάστε την πλήρη περίληψη</span><i>%s</i></summary><div class="ans">%s</div></details><div class="cf-phs">%s</div></div></article>')%(
     i,c['y'],logo,c['kind'],c['n'],th,icon('pin','bi'),c['pl'],c['au'],c['t'],c['s'],icon('plus','bi'),more,phs)
conf=('<section class="phero" id="top" data-amb="wash"><div class="wrap">%s%s<h1 class="h1 h1-s"><span class="w-name">Συνέδρια</span><span class="h1-role">Εισηγήσεις και ανακοινώσεις του Γιώργου Κουτσουραδή σε πανελλήνια συνέδρια ψυχολογίας</span></h1>'
 '<p class="display h-words">Από την <em>πράξη</em> στην έρευνα, και πίσω.</p></div></section>'
 '<section class="cfs" data-amb="lines"><div class="wrap cf-l"><span class="cf-line" aria-hidden="true"></span>%s</div></section>'+cta_band())%(
 crumbs([('to-ergo-mou.html','Το έργο μου'),('synedria.html','Συνέδρια')]),kick('Το έργο μου'),''.join(conf_html(c,i) for i,c in enumerate(CONF)))
page('synedria.html','Συνέδρια | Γιώργος Κουτσουραδής, Σύμβουλος Ψυχικής Υγείας','Οι εισηγήσεις του Γιώργου Κουτσουραδή σε πανελλήνια συνέδρια ψυχολογίας: τρίτη ηλικία (Θεσσαλονίκη 2026, Πάτρα 2025), Συμβουλευτική Ομοτίμων με την Ε.ΣΥ.ΟΜ (Πάτρα 2025), Ιωάννινα 2025 και Αθήνα 2023.',
 conf,crumbs_ld=[('to-ergo-mou.html','Το έργο μου'),('synedria.html','Συνέδρια')],og='conf')

book=('<section class="phero bk-hero" id="top" data-amb="wash"><div class="wrap bk-in"><div class="bk-3d"><div class="bk-cv">%s<span class="bk-sp"></span></div><span class="bk-sh"></span></div>'
 '<div class="ph-txt">%s%s<h1 class="h1 h1-s"><span class="w-name">Χαρτογραφώντας τη σταδιοδρομία</span><span class="h1-role">Θεωρία, αυτογνωσία και πράξη στη σύγχρονη συμβουλευτική</span></h1>'
 '<p class="bk-au h-up">Ειρήνη Καρακασίδου · Γιώργος Κουτσουραδής</p><dl class="bk-meta h-up"><dt>Εκδότης</dt><dd>Επιστημονικές Εκδόσεις Παρισιάνου Α.Ε.</dd><dt>Έτος</dt><dd>2025</dd><dt>ISBN</dt><dd>978-960-583-803-4</dd></dl></div></div></section>'
 '<section class="bk-body" data-amb="lines"><div class="wrap narrow"><p class="lead-l ink">Η σταδιοδρομία δεν είναι πια μια σταθερή και προβλέψιμη πορεία. Είναι μια ζωντανή διαδικασία, που διαμορφώνεται από αλλαγές, επιλογές και μεταβάσεις.</p>'
 '<p class="ink">Το «Χαρτογραφώντας τη σταδιοδρομία» συνδέει τη θεωρία με την αυτογνωσία και την πράξη. Προσεγγίζει τη συμβουλευτική σταδιοδρομίας ως ένα σύγχρονο πεδίο που δεν περιορίζεται στην επιλογή επαγγέλματος, αλλά αγγίζει την ταυτότητα, την προσαρμοστικότητα και τη διαχείριση των επαγγελματικών μεταβάσεων.</p>'
 '<p class="ink">Παρουσιάζει κλασικές και σύγχρονες θεωρίες επαγγελματικής ανάπτυξης, όπως των Holland, Super, Savickas και Krumboltz και τη Social Cognitive Career Theory, και τον τρόπο που εφαρμόζονται στη συμβουλευτική πράξη. Ιδιαίτερη έμφαση δίνεται στην αυτογνωσία, στην αυτοαντίληψη, στη λήψη αποφάσεων, στην ευελιξία και στη δια βίου διαχείριση της σταδιοδρομίας, με τεχνικές και μεθόδους για την πράξη.</p>'
 '<ul class="kw"><li>Holland</li><li>Super</li><li>Savickas</li><li>Krumboltz</li><li>Social Cognitive Career Theory</li></ul></div></section>'
 '<section class="bk-for" data-amb="dots"><div class="wrap"><div class="sh sh-c">%s%s</div><div class="pil-g">'
 '<div class="pil" style="--i:0"><span class="pil-l"></span><h3>Φοιτητές</h3><p>Ένας οδηγός στις θεωρίες και στις εφαρμογές της συμβουλευτικής σταδιοδρομίας.</p></div>'
 '<div class="pil" style="--i:1"><span class="pil-l"></span><h3>Επαγγελματίες σύμβουλοι &amp; εκπαιδευτικοί</h3><p>Τεχνικές, μέθοδοι και εφαρμογές για τη συμβουλευτική πράξη.</p></div>'
 '<div class="pil" style="--i:2"><span class="pil-l"></span><h3>Όποιον ψάχνει την πορεία του</h3><p>Για να κατανοήσει βαθύτερα τη δική του διαδρομή και να χτίσει μια σταδιοδρομία με νόημα.</p></div></div>'
 '<p class="bk-link rv">Αν το θέμα σας αφορά προσωπικά, δείτε την <a href="epaggelmatiki-symvouleftiki.html">επαγγελματική συμβουλευτική</a>.</p></div></section>'+cta_band())%(
 img('book','(max-width: 900px) 56vw, 340px','',eager=True),crumbs([('to-ergo-mou.html','Το έργο μου'),('vivlia.html','Βιβλία')]),kick('Βιβλίο · 2025'),kick('Σε ποιους απευθύνεται'),h2('Ένα βιβλίο για όσους συνοδεύουν, και για όσους ψάχνουν','light'))
page('vivlia.html','«Χαρτογραφώντας τη σταδιοδρομία» | Βιβλίο Γ. Κουτσουραδή & Ε. Καρακασίδου','«Χαρτογραφώντας τη σταδιοδρομία: Θεωρία, αυτογνωσία και πράξη στη σύγχρονη συμβουλευτική», Ειρήνη Καρακασίδου & Γιώργος Κουτσουραδής, Εκδόσεις Παρισιάνου 2025, ISBN 978-960-583-803-4.',
 book,ld=[{"@type":"Book","name":"Χαρτογραφώντας τη σταδιοδρομία: Θεωρία, αυτογνωσία και πράξη στη σύγχρονη συμβουλευτική","author":[{"@type":"Person","name":"Ειρήνη Καρακασίδου"},{"@id":"#giorgos"}],"publisher":{"@type":"Organization","name":"Επιστημονικές Εκδόσεις Παρισιάνου"},"datePublished":"2025","isbn":"978-960-583-803-4","inLanguage":"el","image":"assets/img/chartografontas-ti-stadiodromia-karakasidou-koutsouradis-vivlio-670.webp"}],
 crumbs_ld=[('to-ergo-mou.html','Το έργο μου'),('vivlia.html','Βιβλία')],og='book')

ART_SLUG='arthro-aftosympnonia-triti-ilikia.html'
arth=('<section class="phero" id="top" data-amb="wash"><div class="wrap">%s%s<h1 class="h1 h1-s"><span class="w-name">Κείμενα &amp; Άρθρα</span><span class="h1-role">Γράφει ο Γιώργος Κουτσουραδής</span></h1>'
 '<p class="display h-words">Για την ψυχοθεραπεία, τη συμβουλευτική και τη σύγχρονη <em>ανθρώπινη</em> εμπειρία.</p></div></section>'
 '<section class="ar-list" data-amb="lines"><div class="wrap"><a class="arc" href="%s"><div class="arc-art">%s<span class="arc-q">«Πώς μπορώ να παραμείνω σε σχέση με τον εαυτό μου;»</span></div>'
 '<div class="arc-t"><span class="tag">Τρίτη ηλικία · Υπαρξιακή ματιά · περίπου 9 λεπτά</span><h2>Αυτοσυμπόνια στην τρίτη ηλικία</h2><p class="arc-sub">Μια πιο ήπια σχέση με τον εαυτό στα χρόνια της ωρίμανσης</p>'
 '<p>Η γήρανση δεν είναι μόνο μια βιολογική διαδικασία. Είναι και μια υπαρξιακή εμπειρία, που μας φέρνει αντιμέτωπους με την αλλαγή, την απώλεια και τα όρια. Η αυτοσυμπόνια μπορεί να γίνει ένας διαφορετικός τρόπος να τη συναντήσουμε: όχι ως παραίτηση, αλλά ως δυνατότητα να αναγνωρίζουμε την ευαλωτότητά μας χωρίς να στρεφόμαστε εναντίον μας.</p>'
 '<span class="sc-go">Διαβάστε το άρθρο %s</span></div></a><p class="ar-soon rv">Νέα κείμενα θα προστίθενται εδώ.</p></div></section>'+cta_band())%(
 crumbs([('to-ergo-mou.html','Το έργο μου'),('arthra.html','Κείμενα & Άρθρα')]),kick('Το έργο μου'),ART_SLUG,mark('mk arc-mk'),icon('arrow','bi'))
page('arthra.html','Κείμενα & Άρθρα | Γιώργος Κουτσουραδής, Ψυχοθεραπευτής','Κείμενα του Γιώργου Κουτσουραδή για την ψυχοθεραπεία, τη συμβουλευτική, την προσωπική ανάπτυξη και τη σύγχρονη ανθρώπινη εμπειρία.',
 arth,crumbs_ld=[('to-ergo-mou.html','Το έργο μου'),('arthra.html','Κείμενα & Άρθρα')])

# --- το άρθρο: το κείμενο του συγγραφέα, με διορθώσεις στίξης/ορθογραφίας και υπότιτλους για την ανάγνωση ---
raw=open(K+'/work/article_raw.txt').read()
P=[l.strip() for l in raw.replace('\n\n','\n').split('\n') if l.strip()]
FIX=[('H ενσυνείδητη','Η ενσυνείδητη'),('‘Iσως','Ίσως'),('ερώτημα, πώς μιλά','ερώτημα: πώς μιλά'),('Σε αυτή την έννοια','Με αυτή την έννοια'),
     ('σε κάτι περισσότερο ανθρώπινο το να μπορούμε','σε κάτι πιο ανθρώπινο: να μπορούμε'),('αυτό που παραμένει και να εξακολουθούμε','αυτό που παραμένει, και να εξακολουθούμε'),
     ('ψυχική ανθεκτικότητα όχι ως άρνηση','ψυχική ανθεκτικότητα, όχι ως άρνηση'),('ευαλωτότητας αλλά ως','ευαλωτότητας, αλλά ως'),('⁠','')]
def fx(t):
    for a,b in FIX: t=t.replace(a,b)
    return t
P=[fx(p) for p in P]
bi=P.index('Βιβλιογραφία'); body_p=P[:bi]; refs=P[bi+1:]
H={2:'Τι είναι η αυτοσυμπόνια',8:'Ερωτήματα που δεν αναβάλλονται πια',12:'Τι λέει η έρευνα, και τι όχι',16:'Η αποδοχή ως σχέση, όχι ως τέρμα',20:'Μια υπαρξιακή ματιά'}
ab=[]
i=0
while i<len(body_p):
    if i in H: ab.append('<h2 class="lc" data-fx="mask">%s</h2>'%H[i])
    p=body_p[i]
    if i==21:
        ab.append('<blockquote class="aq"><p>%s %s</p><p class="aq-b">%s</p></blockquote>'%(p,body_p[22],body_p[23])); i=24; continue
    if i==17 or i==25: ab.append('<p class="pull-s">%s</p>'%p)
    else: ab.append('<p>%s</p>'%p)
    i+=1
def ref(r):
    r=re.sub(r'(https://doi\.org/\S+)',r'<a href="\1" target="_blank" rel="noopener">\1</a>',r); return '<li>%s</li>'%r
art=('<article class="art-pg"><header class="phero ar-hero" id="top" data-amb="wash"><div class="wrap narrow">%s%s<h1 class="h1 h1-s ar-h1"><span class="w-name">Αυτοσυμπόνια στην τρίτη ηλικία</span></h1>'
 '<p class="display h-words">Μια πιο ήπια σχέση με τον εαυτό στα χρόνια της <em>ωρίμανσης</em>.</p><p class="ar-by h-up">%s<span>Γιώργος Κουτσουραδής · Σύμβουλος Ψυχικής Υγείας &amp; Συνθετικός Ψυχοθεραπευτής</span></p></div></header>'
 '<div class="ar-prog" aria-hidden="true"></div><section class="ar-body" data-amb="lines"><div class="wrap narrow prose">'
 '<p class="ar-lede">Η γήρανση δεν είναι μόνο μια βιολογική διαδικασία. Είναι και μια υπαρξιακή εμπειρία που μας φέρνει αντιμέτωπους με την αλλαγή, την απώλεια, τα όρια, αλλά και με το ερώτημα του πώς στεκόμαστε απέναντι στον εαυτό μας όταν η ζωή δεν μπορεί πια να είναι ακριβώς όπως πριν. Η αυτοσυμπόνια μπορεί να αποτελέσει έναν διαφορετικό τρόπο συνάντησης με αυτή την πραγματικότητα: όχι ως παραίτηση, αλλά ως δυνατότητα να αναγνωρίζουμε την ευαλωτότητά μας χωρίς να στρεφόμαστε εναντίον μας.</p>'
 '%s<div class="refs"><h2>Βιβλιογραφία</h2><ol>%s</ol></div>'
 '<div class="ar-end">%s<div><p class="g-t">Γιώργος Κουτσουραδής</p><p>Σύμβουλος Ψυχικής Υγείας &amp; Συνθετικός Ψυχοθεραπευτής. Δουλεύει μεταξύ άλλων με ανθρώπους της τρίτης ηλικίας. <a href="symvouleftiki-triti-ilikia.html">Συμβουλευτική στην τρίτη ηλικία →</a></p></div></div></div></section></article>'+cta_band())%(
 crumbs([('to-ergo-mou.html','Το έργο μου'),('arthra.html','Κείμενα & Άρθρα'),(ART_SLUG,'Αυτοσυμπόνια στην τρίτη ηλικία')]),kick('Άρθρο · Τρίτη ηλικία'),BYMK,''.join(ab),''.join(ref(r) for r in refs),BYMK)
page(ART_SLUG,'Αυτοσυμπόνια στην τρίτη ηλικία | Άρθρο Γιώργου Κουτσουραδή','Η αυτοσυμπόνια στα χρόνια της ωρίμανσης: τι σημαίνει κατά την Kristin Neff, τι λέει η έρευνα για τους μεγαλύτερους ενήλικες και μια υπαρξιακή ματιά. Του Γιώργου Κουτσουραδή.',
 art,ld=[{"@type":"BlogPosting","headline":"Αυτοσυμπόνια στην τρίτη ηλικία","alternativeHeadline":"Μια πιο ήπια σχέση με τον εαυτό στα χρόνια της ωρίμανσης","author":{"@id":"#giorgos"},"inLanguage":"el","datePublished":"2026-11","dateModified":"2026-11-17","about":["Αυτοσυμπόνια","Τρίτη ηλικία","Γήρανση"]}],
 crumbs_ld=[('to-ergo-mou.html','Το έργο μου'),('arthra.html','Κείμενα & Άρθρα'),(ART_SLUG,'Αυτοσυμπόνια στην τρίτη ηλικία')])

# ===== ΕΠΙΚΟΙΝΩΝΙΑ =====
STEPS=[('Επικοινωνία','Τηλεφωνήστε μου ή στείλτε μου email. Θα σας απαντήσω το συντομότερο.'),('Μια πρώτη κουβέντα','Λύνουμε τις απορίες σας και βρίσκουμε ημέρα και ώρα που σας εξυπηρετεί, δια ζώσης ή online.'),('Η πρώτη συνάντηση','Γνωριζόμαστε χωρίς πίεση. Στο τέλος αποφασίζετε με ηρεμία αν θέλετε να συνεχίσουμε.')]
steps=''.join('<li style="--i:%d"><span class="st-n">%d</span><b>%s</b><span>%s</span></li>'%(i,i+1,t,d) for i,(t,d) in enumerate(STEPS))
contact=('<section class="phero ct-hero" id="top" data-amb="wash"><div class="wrap">%s%s<h1 class="h1 h1-s"><span class="w-name">Επικοινωνία</span><span class="h1-role">Γιώργος Κουτσουραδής · Σύμβουλος Ψυχικής Υγείας στο Περιστέρι</span></h1>'
 '<p class="display h-words">Το πρώτο βήμα είναι <em>ένα μήνυμα</em>. Τα υπόλοιπα τα βρίσκουμε μαζί.</p></div></section>'
 '<section class="ct" id="rantevou" data-amb="lines"><div class="wrap ct-g">'
 '<a class="ctc tilt" href="tel:%s" style="--i:0">%s<span class="ctc-l">Τηλέφωνο</span><b>%s</b><span class="ctc-h">Καλέστε για ραντεβού</span></a>'
 '<a class="ctc tilt" href="mailto:%s" style="--i:1">%s<span class="ctc-l">Email</span><b class="em">%s</b><span class="ctc-h">Γράψτε μου όποτε σας βολεύει</span></a>'
 '<a class="ctc tilt" href="%s" target="_blank" rel="noopener" style="--i:2">%s<span class="ctc-l">Γραφείο</span><b>Μιαούλη 54</b><span class="ctc-h">121 31 Περιστέρι Αττικής · Οδηγίες ↗</span></a></div></section>'
 '<section class="steps" data-amb="dots"><div class="wrap st-in"><div>%s%s<p class="rv">Η διαδικασία είναι απλή και σέβεται τον χρόνο σας. Συνεδρίες δια ζώσης στο γραφείο ή online, μέσω ασφαλούς πλατφόρμας τηλεδιάσκεψης.</p></div><ol class="st-l"><span class="st-line" aria-hidden="true"></span>%s</ol></div></section>'
 '<section class="office" data-amb="profiles"><div class="wrap of-in"><figure class="of-ph of-two"><div class="ms of-a"><div class="ms-in">%s</div></div><div class="of-b rv">%s</div></figure>'
 '<div class="of-map">%s%s<p class="rv">Το γραφείο βρίσκεται στην οδό Μιαούλη 54, στο Περιστέρι. Αν σας βολεύει περισσότερο, μπορούμε να συναντηθούμε online.</p>'
 '<div class="mapbox"><iframe class="map" src="about:blank" data-advon-src="%s" data-advon-kind="map" data-advon-provider="Google" data-advon-link="%s" title="Χάρτης: Μιαούλη 54, Περιστέρι" loading="lazy"></iframe></div></div></div></section>'
 '<section class="faq" data-amb="dots2"><div class="wrap faq-in"><div class="faq-h">%s%s</div><div class="faq-l">%s</div></div></section>')%(
 crumbs([('epikoinonia.html','Επικοινωνία')]),kick('Ραντεβού'),TEL,icon('phone','ic'),PHONE,MAIL,icon('mail','ic'),MAIL,MAPQ,icon('pin','ic'),
 kick('Πώς κλείνουμε ραντεβού'),h2('Τρία απλά βήματα','mask'),steps,img('room','(max-width: 900px) 92vw, 36vw'),img('shelf','(max-width: 900px) 92vw, 16vw'),kick('Ο χώρος'),h2('Ένα ήσυχο γραφείο στο Περιστέρι','roll'),MAPEMB,MAPQ,
 kick('Πριν έρθετε'),h2('Χρήσιμα να ξέρετε','light'),faq(['book','online','length','cancel','confidential','nervous'],True))
page('epikoinonia.html','Επικοινωνία & Ραντεβού | Γιώργος Κουτσουραδής, Περιστέρι','Κλείστε ραντεβού με τον Γιώργο Κουτσουραδή, Σύμβουλο Ψυχικής Υγείας: +30 698 588 0004, '+MAIL+'. Γραφείο: Μιαούλη 54, Περιστέρι. Συνεδρίες και online.',
 contact,ld=[faq_ld(['book','online','length','cancel','confidential','nervous'])],crumbs_ld=[('epikoinonia.html','Επικοινωνία')],og='room')

# ---------- κοινό head / build ----------
C=json.load(open(K+'/work/center_raw.json'))
import numpy as _np
G=_np.array(C['dg'][0])  # top -> bottom, face looks right
# μαλάκωμα
k=_np.ones(9)/9; Gs=_np.column_stack([_np.convolve(_np.pad(G[:,0],4,'edge'),k,'valid'),_np.convolve(_np.pad(G[:,1],4,'edge'),k,'valid')])[::4]
X0=Gs[:,0].min()-4; X1=Gs[:,0].max()+4
pts=[(X1-x+2, y) for x,y in Gs]          # καθρέφτισμα: το πρόσωπο κοιτά αριστερά
top=(pts[0][0],0); bot=(pts[-1][0],204); W=X1-X0+8
poly='M%.1f 0L'%(W+6)+' L'.join('%.1f %.1f'%p for p in [top]+pts+[bot])+' L%.1f 204Z'%(W+6)
EDGE='<svg class="edge" viewBox="0 0 %.1f 204" preserveAspectRatio="none" style="aspect-ratio:%.1f/204" aria-hidden="true"><path d="%s"/></svg>'%(W+6,W+6,poly)
INTRO=('<div class="intro" aria-hidden="true"><div class="il il3">%s</div><div class="il il2">%s</div><div class="il il1">%s<div class="i-ct">'
 '<div class="i-lg"><img class="i-lgt" src="assets/img/giorgos-koutsouradis-logo.svg" width="502" height="370" alt=""></div></div></div></div>')%(EDGE,EDGE,EDGE)

FONTS=[('Brygada 1918','normal',400,'brygada-1918'),('Brygada 1918','normal',500,'brygada-1918'),('Brygada 1918','italic',400,'brygada-1918'),('Commissioner','normal',400,'commissioner'),('Commissioner','normal',600,'commissioner')]
UR={'greek':'U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF','latin':'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'}
FF_UNUSED=''.join("@font-face{font-family:'%s';font-style:%s;font-weight:%d;font-display:swap;src:url(assets/fonts/%s-%s-%d-%s.woff2) format('woff2');unicode-range:%s}"%(f,s,w,p,sub,w,s,UR[sub]) for f,s,w,p in FONTS for sub in ('greek','latin'))
FF=''
css=open(S+'/style.css').read()
mcss=re.sub(r'/\*[\s\S]*?\*/','',css); mcss=re.sub(r'\s*\n\s*','',mcss); mcss=re.sub(r'\s*([{};,>])\s*',r'\1',mcss).replace(';}','}')
open('/tmp/k.js','w').write(open(S+'/script.js').read())
mjs=subprocess.check_output(['/home/claude/tools/node_modules/.bin/terser','/tmp/k.js','-c','-m']).decode()
BASE=[
 {"@type":"MedicalBusiness","@id":"#practice","name":"Γιώργος Κουτσουραδής – Σύμβουλος Ψυχικής Υγείας & Ψυχοθεραπευτής","alternateName":["Giorgos Koutsouradis","Γιώργος Κουτσουραδής Ψυχοθεραπευτής Περιστέρι"],
  "description":"Συμβουλευτική και συνθετική ψυχοθεραπεία ενηλίκων στο Περιστέρι και online: ατομική συμβουλευτική, ψυχοθεραπεία ενηλίκων, προσωπική ανάπτυξη, συμβουλευτική τρίτης ηλικίας, επαγγελματική συμβουλευτική, personal & business coaching.",
  "image":"assets/img/giorgos-koutsouradis-symvoulos-psychikis-ygeias-peristeri-portreto-960.webp","telephone":"+30 698 588 0004","email":MAIL,
  "address":{"@type":"PostalAddress","streetAddress":"Μιαούλη 54","addressLocality":"Περιστέρι","postalCode":"121 31","addressRegion":"Αττική","addressCountry":"GR"},
  "geo":{"@type":"GeoCoordinates","latitude":38.0049331,"longitude":23.6908265},"hasMap":"https://www.google.com/maps/place/?q=place_id:0x14a1a34a6edb11c1:0x7da1f7f7c9964a09",
  "areaServed":["Περιστέρι","Δυτική Αθήνα","Αθήνα","Online"],"founder":{"@id":"#giorgos"},
  "knowsAbout":[s['title'] for s in SERVICES]+["Συνθετική ψυχοθεραπεία","Υπαρξιακή ψυχοθεραπεία","Προσωποκεντρική προσέγγιση","Γνωσιακή συμπεριφορική προσέγγιση","Θετική ψυχολογία","Συμβουλευτική σταδιοδρομίας"]},
 {"@type":"Person","@id":"#giorgos","name":"Γιώργος Κουτσουραδής","alternateName":["Giorgos Koutsouradis","Γεώργιος Κουτσουραδής","Georgios Koutsouradis"],"jobTitle":"Σύμβουλος Ψυχικής Υγείας & Συνθετικός Ψυχοθεραπευτής",
  "image":"assets/img/giorgos-koutsouradis-symvoulos-psychikis-ygeias-peristeri-portreto-960.webp","worksFor":{"@id":"#practice"},"telephone":"+30 698 588 0004","email":MAIL,
  "memberOf":[{"@type":"Organization","name":"Ελληνική Συμβουλευτική Εταιρεία (Ε.Ε.Σ.)"},{"@type":"Organization","name":"Ελληνική Επιστημονική Εταιρεία Συμβουλευτικής Ομηλίκων (Ε.ΣΥ.ΟΜ)"},{"@type":"Organization","name":"Ελληνική Εταιρεία Συνθετικών Ψυχοθεραπευτών (Ε.Ε.ΣΥ.Ψ.)"},{"@type":"Organization","name":"Ελληνική Εταιρεία Θετικής Ψυχολογίας (Ε.Ε.ΘΕ.ΨΥ.)"},{"@type":"Organization","name":"European Mentoring & Coaching Council (EMCC Global)"}],"alumniOf":[{"@type":"EducationalOrganization","name":"European Institute of Counselling & Psychotherapy"},{"@type":"CollegeOrUniversity","name":"University of Sunderland"}],
  "hasCredential":[{"@type":"EducationalOccupationalCredential","name":"Πενταετής εκπαίδευση στη Συμβουλευτική και τη Συνθετική Ψυχοθεραπεία","recognizedBy":{"@type":"Organization","name":"European Institute of Counselling & Psychotherapy"}}],
  "knowsAbout":["Συνθετική ψυχοθεραπεία","Συμβουλευτική","Θετική ψυχολογία","Evidence-Based Coaching","Συμβουλευτική σταδιοδρομίας","Αυτοσυμπόνια"]},
 {"@type":"WebSite","@id":"#website","name":"Γιώργος Κουτσουραδής","alternateName":["Giorgos Koutsouradis","Γεώργιος Κουτσουραδής","Κουτσουραδής Γιώργος","Γιώργος Κουτσουράδης","gkoutsouradis",DOMAIN],"url":"https://"+DOMAIN+"/","inLanguage":"el"}]
OGI={k:'assets/img/%s-%d.webp'%(IMGS[k][0],IMGS[k][1][min(1,len(IMGS[k][1])-1)]) for k in IMGS}
def build(pg):
    fn=pg['fn']; graph=list(BASE)+pg['ld']
    if pg['crumbs']:
        graph.append({"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Αρχική","item":"index.html"}]+[{"@type":"ListItem","position":i+2,"name":t,"item":h} for i,(h,t) in enumerate(pg['crumbs'])]})
    og=OGI[pg['og'] or 'portrait']
    preload=''
    if fn=='index.html':
        n,ws=IMGS['portrait'][0],IMGS['portrait'][1]
        preload='<link rel="preload" as="image" href="assets/img/%s-960.webp" imagesrcset="%s" imagesizes="(max-width: 900px) 92vw, 44vw" fetchpriority="high">'%(n,', '.join('assets/img/%s-%d.webp %dw'%(n,x,x) for x in ws))
    head=f'''<!DOCTYPE html>
<html lang="el">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(pg['title'])}</title>
<meta name="description" content="{E(pg['desc'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#F7F3EC">
<meta property="og:type" content="{'article' if fn.startswith('arthro-') else 'website'}"><meta property="og:locale" content="el_GR"><meta property="og:site_name" content="Γιώργος Κουτσουραδής">
<meta property="og:title" content="{E(pg['title'])}"><meta property="og:description" content="{E(pg['desc'])}">
<meta property="og:image" content="{og}"><meta property="og:image:alt" content="Γιώργος Κουτσουραδής, Σύμβουλος Ψυχικής Υγείας &amp; Ψυχοθεραπευτής">
<meta name="twitter:card" content="summary_large_image">
{preload}
<script>(function(h){{h.classList.add('js');try{{if(!sessionStorage.getItem('gk-intro')&&!document.hidden&&!matchMedia('(prefers-reduced-motion:reduce)').matches){{h.classList.add('intro-on');sessionStorage.setItem('gk-intro','1')}}}}catch(e){{}}}})(document.documentElement)</script>
<style id="gk-css">{mcss}</style>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False,separators=(',',':'))}</script>
</head>
<body class="{pg['cls']}">
'''
    out=head+SYM+INTRO+header(pg['cur'])+'<main id="main">'+pg['body']+'</main>'+footer(pg['cur'])+'\n<script id="gk-js">'+mjs+'</script>\n</body>\n</html>\n'
    assert '{{' not in out
    open(R+'/'+fn,'w').write(out); return len(out)
if __name__=='__main__':
    for pg in PAGES: print('%-44s %4d KB'%(pg['fn'],build(pg)//1024))
    print('css',len(mcss)//1024,'KB · js',len(mjs)//1024,'KB · pages',len(PAGES))
