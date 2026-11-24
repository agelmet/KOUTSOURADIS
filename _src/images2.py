# Συνέδρια 2025–2026 (υλικό πελάτη, 24 Νοε 2026) → assets/img
from PIL import Image, ImageOps
import sys
D='/home/claude/kts/docs/'; O='/home/claude/k/repo/assets/img/'
A=D+'05472218-Engrapho/media/'; B=D+'3d3ea19e-_____________________/media/'; C=D+'46a2cb60-______________________________________/media/'
J=[ # (src, name, widths)
 (A+'image1.jpg','9o-panellinio-synedrio-symvouleftikis-psychologias-patra-2025',[1143]),
 (A+'image2.JPG','giorgos-koutsouradis-9o-synedrio-symvouleftikis-patra-2025-eisigisi',[480,900,1200]),
 (A+'image3.JPG','giorgos-koutsouradis-9o-synedrio-symvouleftikis-patra-2025-omada',[640,1200,1600]),
 (B+'image3.png','8o-panellinio-synedrio-anaptyxiakis-psychologias-thessaloniki-2026',[650]),
 (B+'image1.JPG','giorgos-koutsouradis-8o-synedrio-anaptyxiakis-thessaloniki-2026-omada',[480,900,1200]),
 (B+'image2.JPG','giorgos-koutsouradis-8o-synedrio-anaptyxiakis-thessaloniki-2026-eisigisi',[640,1200,1600]),
 (B+'image4.JPG','giorgos-koutsouradis-8o-synedrio-anaptyxiakis-thessaloniki-2026-vima',[480,900,1200]),
 (C+'image1.png','esyom-symposio-atomiki-symvouleftiki-omotimon-patra-2025-diafaneia',[640,1268]),
 (C+'image2.jpeg','esyom-symposio-atomiki-symvouleftiki-omotimon-patra-2025-omada',[320]),
 (C+'image3.png','esyom-symposio-atomiki-symvouleftiki-omotimon-patra-2025-panel',[320]),
]
for src,name,ws in J:
    im=ImageOps.exif_transpose(Image.open(src))
    im=im.convert('RGBA') if im.mode in ('RGBA','LA','P') else im.convert('RGB')
    for w in ws:
        x=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS) if w<im.width else im
        x.save(O+'%s-%d.webp'%(name,w),'WEBP',quality=84,method=6)
    print(name,im.size,im.mode)
