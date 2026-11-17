from PIL import Image, ImageOps, ImageFilter
import os
M='/home/claude/mat/img/'; O='/home/claude/k/repo/assets/img/'
def save(im,name,widths,q=82):
    for w in widths:
        if w>im.width*1.02: continue
        x=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS) if w<im.width else im
        x.save(O+'%s-%d.webp'%(name,w),'WEBP',quality=q,method=6)
    print(name,im.size)
P='giorgos-koutsouradis-'
im=Image.open(M+'i00.webp').convert('RGB'); save(im,P+'symvoulos-psychikis-ygeias-peristeri-portreto',[640,960,1400])
im=Image.open(M+'i02.webp').convert('RGB'); save(im,P+'psychotherapeftis-grafeio-polythrona',[720,1080,1448])
im=Image.open(M+'i03.webp').convert('RGB'); save(im,P+'synthetikos-psychotherapeftis-peristeri-grafeio',[720,1080,1448])
im=Image.open(M+'i04.webp').convert('RGB'); save(im,P+'grafeio-symvouleftikis-peristeri',[960,1440,2048])
im=Image.open(M+'i20.jpg').convert('RGB'); save(im,P+'karakasidou-synedrio-poster',[600,1000])
im=Image.open(M+'i22.jpg').convert('RGB'); save(im,'chartografontas-ti-stadiodromia-karakasidou-koutsouradis-vivlio',[400,670])
im=Image.open(M+'i19.webp').convert('RGB'); save(im,'poster-19o-synedrio-psychologikis-erevnas-ioannina-2025',[560,1206])
im=Image.open(M+'i21.jpg').convert('RGB'); save(im,'poster-8o-synedrio-symvouleftikis-psychologias-2023',[560,1125])
im=Image.open(M+'i18.jpeg').convert('RGB'); save(im,'19o-panellinio-synedrio-psychologikis-erevnas-ioannina',[1003])
