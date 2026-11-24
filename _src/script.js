(function(){
'use strict';
var d=document,h=d.documentElement,w=window;
var RM=matchMedia('(prefers-reduced-motion:reduce)').matches;
var HOVER=matchMedia('(hover:hover) and (pointer:fine)').matches;
var $=function(s,c){return (c||d).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};

/* ---------- split text ---------- */
function splitWords(el){ // hero display lines: word mask rise, keeps <em>
  var i=0;(function walk(n){Array.prototype.slice.call(n.childNodes).forEach(function(c){
    if(c.nodeType===3){var f=d.createDocumentFragment();c.textContent.split(/(\s+)/).forEach(function(t){if(!t)return;if(/^\s+$/.test(t)){f.appendChild(d.createTextNode(' '));return}
      var o=d.createElement('span');o.className='hw';var s=d.createElement('span');s.style.setProperty('--i',i++);s.textContent=t;o.appendChild(s);f.appendChild(o)});c.parentNode.replaceChild(f,c)}
    else if(c.nodeType===1&&c.tagName!=='BR')walk(c)})})(el)}
function splitHead(el){
  var fx=el.getAttribute('data-fx')||'',txt=el.textContent.replace(/\s+/g,' ').trim();el.setAttribute('aria-label',txt);
  var letters=0,words=0,all=[];
  (function walk(n){Array.prototype.slice.call(n.childNodes).forEach(function(c){
    if(c.nodeType===3){var f=d.createDocumentFragment();c.textContent.split(/(\s+)/).forEach(function(t){if(!t)return;if(/^\s+$/.test(t)){f.appendChild(d.createTextNode(' '));return}
      var ws=d.createElement('span');ws.className='lc-w';ws.setAttribute('aria-hidden','true');ws.style.setProperty('--w',words++);
      if(fx==='light'){ws.textContent=t}else{Array.prototype.forEach.call(t,function(ch){var s=d.createElement('span');s.className='lc-c';s.style.setProperty('--i',letters++);s.textContent=ch;ws.appendChild(s);all.push(s)})}
      f.appendChild(ws)});c.parentNode.replaceChild(f,c)}
    else if(c.nodeType===1&&c.tagName!=='BR')walk(c)})})(el);
  if(fx==='centre'){var m=(all.length-1)/2;all.forEach(function(s,k){var dd=k-m;s.style.setProperty('--d',dd>0?1:dd<0?-1:0);s.style.setProperty('--a',Math.round(Math.abs(dd)))})}
}
$$('.h-words').forEach(splitWords);
$$('.lc').forEach(splitHead);
$$('[data-words]').forEach(function(el){el.innerHTML=el.textContent.trim().split(/\s+/).map(function(t){return '<span class="qw">'+t+'</span>'}).join(' ')});

/* ---------- intro ---------- */
var intro=h.classList.contains('intro-on')&&$('.intro');
function ready(){h.classList.add('ready')}
if(intro&&!RM&&!d.hidden){
  requestAnimationFrame(function(){h.classList.add('intro-run')});
  setTimeout(function(){h.classList.add('intro-out')},1750);
  setTimeout(ready,1950);
  setTimeout(function(){h.classList.remove('intro-on','intro-run','intro-out');intro.remove()},3200);
}else{h.classList.remove('intro-on');if(intro)intro.remove();requestAnimationFrame(function(){requestAnimationFrame(ready)})}
setTimeout(ready,3600);

/* ---------- reveal ---------- */
var RSEL='.rv,.ink,.lc,.kick,.proof-in,.sc-grid,.oc-grid,.wk-grid,.faq-l,.cr-grid,.by-grid,.sv-list,.ha-g,.tp-grid,.sp-g,.pil-g,.gn,.wk3-g,.cf,.ct-g,.st-l,.kw,.ms,.mapbox,.pol,.draw-mk,.cta,.draw,.mb-g';
var els=$$(RSEL);
function count(el){var to=+el.getAttribute('data-count'),sep=el.getAttribute('data-sep'),fmt=function(v){v=Math.round(v);return sep?String(v).replace(/\B(?=(\d{3})+(?!\d))/g,sep):String(v)};
  if(RM||d.hidden){el.textContent=fmt(to);return}var from=to>1900?to-40:0,t0=null,dur=to>1900?1400:1600;
  function st(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/dur),e=1-Math.pow(1-p,3);el.textContent=fmt(from+(to-from)*e);if(p<1&&!d.hidden)requestAnimationFrame(st);else el.textContent=fmt(to)}
  requestAnimationFrame(st);setTimeout(function(){el.textContent=fmt(to)},dur+400)}
function show(el){el.classList.add('in');$$('[data-count]',el).forEach(function(c){if(!c.dataset.done){c.dataset.done=1;count(c)}})}
if(RM||!('IntersectionObserver' in w)){els.forEach(show)}else{
  var mob=innerWidth<700;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){show(e.target);io.unobserve(e.target)}})},{rootMargin:mob?'0px 0px -2% 0px':'0px 0px -8% 0px',threshold:.04});
  els.forEach(function(el){io.observe(el)});
  setTimeout(function(){els.forEach(function(el){var r=el.getBoundingClientRect();if(r.top<innerHeight&&r.bottom>0)show(el)})},2400);
}
$$('.hero [data-count],.proof [data-count]').forEach(function(){});

/* ---------- ambient layers ---------- */
var DARK={syn:1,cta:1,how:1,ft:1};
function amb(sec){var t=sec.getAttribute('data-amb'),dark=Array.prototype.some.call(sec.classList,function(c){return DARK[c]}),a=d.createElement('div');a.className='amb';a.setAttribute('aria-hidden','true');
  var C=dark?['rgba(232,164,126,.22)','rgba(201,214,180,.18)','rgba(157,181,145,.2)']:['rgba(217,116,74,.16)','rgba(201,214,180,.5)','rgba(110,140,99,.16)'],L=dark?'rgba(243,230,211,.22)':'rgba(77,97,66,.28)',x='';
  function r(a,b){return (a+Math.random()*(b-a)).toFixed(1)}
  if(t==='wash'||t==='wash2'){for(var i=0;i<(t==='wash'?3:2);i++)x+='<span class="wa" style="--s:'+r(38,60)+'vw;--x:'+r(-15,70)+'%;--y:'+r(-25,55)+'%;--c:'+C[i%3]+';--t:'+r(22,34)+'s;--dx:'+r(-60,60)+'px;--dy:'+r(-50,50)+'px"></span>'}
  if(t==='lines'||t==='lines2'){for(i=0;i<(t==='lines'?4:3);i++)x+='<span class="am-line" style="--y:'+r(8,92)+'%;--c:'+L+';--t:'+r(14,24)+'s;--o:'+r(-40,40)+'px"></span>'}
  if(t==='rings'){for(i=0;i<3;i++)x+='<span class="am-ring" style="--s:'+r(240,520)+'px;--x:'+r(-10,80)+'%;--y:'+r(-10,70)+'%;--c:'+L+';--t:'+r(9,14)+'s;--d:'+(i*3)+'s"></span>'}
  if(t==='dots'||t==='dots2')x+='<span class="am-dots" style="--c:'+L+'"></span>';
  if(t==='profiles'){for(i=0;i<2;i++)x+='<svg class="mk am-mk" viewBox="-6 -6 198 216" style="--s:'+r(180,320)+'px;--x:'+(i?r(70,86):r(-4,10))+'%;--y:'+r(5,55)+'%;--t:'+r(16,24)+'s'+(dark?';--mk-s:rgba(201,214,180,.5);--mk-o:#E8A47E;--mk-g:#9DB591':'')+'"><use href="#mk"/></svg>'}
  a.innerHTML=x;sec.insertBefore(a,sec.firstChild);return a}
if(!RM){var ambs=$$('[data-amb]').map(amb);
  if('IntersectionObserver' in w){var aio=new IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle('off',!e.isIntersecting)})},{rootMargin:'100px'});ambs.forEach(function(a){a.classList.add('off');aio.observe(a)})}}

/* ---------- pointer ---------- */
var hero=$('.hero'),bk=$('.bk-3d');
if(HOVER&&!RM){
  var mx=0,my=0,tx=0,ty=0,run=0;
  addEventListener('pointermove',function(e){tx=e.clientX/innerWidth-.5;ty=e.clientY/innerHeight-.5;if(!run){run=1;requestAnimationFrame(pt)}},{passive:true});
  function pt(){mx+=(tx-mx)*.08;my+=(ty-my)*.08;[hero,bk].forEach(function(el){if(el){el.style.setProperty('--mx',mx.toFixed(3));el.style.setProperty('--my',my.toFixed(3))}});
    $$('.am-dots').forEach(function(el){el.style.setProperty('--mx',(50+mx*60)+'%');el.style.setProperty('--my',(40+my*60)+'%')});
    if(Math.abs(tx-mx)+Math.abs(ty-my)>.002)requestAnimationFrame(pt);else run=0}
  $$('.tilt').forEach(function(el){
    el.addEventListener('pointermove',function(e){var r=el.getBoundingClientRect(),px=(e.clientX-r.left)/r.width,py=(e.clientY-r.top)/r.height;
      el.classList.add('tilting');el.style.setProperty('--gx',(px*100)+'%');el.style.setProperty('--gy',(py*100)+'%');
      el.style.transform='perspective(900px) rotateX('+((.5-py)*7).toFixed(2)+'deg) rotateY('+((px-.5)*9).toFixed(2)+'deg) translateY(-4px)'});
    el.addEventListener('pointerleave',function(){el.classList.remove('tilting');el.style.transform=''})})
}

/* ---------- journey stations ---------- */
var jp=$('.pt-ln'),sts=$$('.pt-st'),FR=[0,.24,.5,.76,1];
function placeSt(){if(!jp)return;var L=jp.getTotalLength();sts.forEach(function(s,i){var p=jp.getPointAtLength(L*FR[i]);s.style.setProperty('--x',(p.x/4)+'%');s.style.setProperty('--y',(p.y/9)+'%')})}
placeSt();

/* ---------- synthesis ---------- */
var syn=$('.syn'),cs=$$('.syn-c'),core=$('.syn-svg'),steps=$$('.syn-step');
function synSet(p){var k=1-Math.min(1,p/.7)*(1-.38);cs.forEach(function(c){c.style.setProperty('--k',k.toFixed(3))});
  if(core)core.style.setProperty('--cs',Math.max(0,Math.min(1,(p-.62)/.25)).toFixed(3));
  steps.forEach(function(s,i){s.classList.toggle('on',p>=i*.33-.02)})}
var pinned=false;
function synMode(){if(!syn)return;pinned=!RM&&innerWidth>900&&innerHeight>=700;syn.classList.toggle('pinned',pinned);
  if(!pinned){if(RM){synSet(1);return}synSet(0);var so=new IntersectionObserver(function(es){if(es[0].isIntersecting){setTimeout(function(){synSet(1)},150);so.disconnect()}},{threshold:.3});so.observe($('.syn-stage'))}}
synMode();

/* ---------- scroll ---------- */
var hd=$('#hd'),prog=$('.prog'),top=$('.totop'),mbar=$('.mbar'),scue=$('.scue'),hbg=$('.hbg-mk'),pars=$$('[data-par]'),jr=$('.jr-path'),q=$('.qt'),qws=q?$$('.qw',q):[],arp=$('.ar-prog'),ab=$('.prose'),cfl=$('.cf-line'),cfw=$('.cf-l'),tk=0;
function onScroll(){tk=0;var y=scrollY,vh=innerHeight,max=d.documentElement.scrollHeight-vh,p=max>0?y/max:0;
  if(prog)prog.style.setProperty('--p',p.toFixed(4));if(top){top.style.setProperty('--p',p.toFixed(4));top.classList.toggle('on',y>700)}
  if(hd)hd.classList.toggle('solid',y>30);if(mbar)mbar.classList.toggle('on',y>320);if(scue)scue.style.setProperty('--so',Math.max(0,1-y/200));
  if(RM)return;
  if(hbg&&y<vh*1.4)hbg.style.setProperty('--sy',(y*.18).toFixed(1)+'px');
  pars.forEach(function(el){var r=el.getBoundingClientRect();if(r.bottom<-100||r.top>vh+100)return;el.style.setProperty('--py',((r.top+r.height/2-vh/2)*-(+el.getAttribute('data-par'))).toFixed(1)+'px')});
  if(syn&&pinned){var r=syn.querySelector('.syn-track').getBoundingClientRect(),pp=Math.max(0,Math.min(1,-r.top/(r.height-vh)));synSet(pp)}
  if(jr){var r2=jr.getBoundingClientRect(),pj=Math.max(0,Math.min(1,(vh*.62-r2.top)/r2.height));jr.style.setProperty('--pp',pj.toFixed(3));sts.forEach(function(s,i){s.classList.toggle('on',pj>=FR[i]-.03)})}
  if(q){var r3=q.getBoundingClientRect(),pq=Math.max(0,Math.min(1,(vh*.85-r3.top)/(r3.height+vh*.35)));var n=Math.round(pq*qws.length*1.15);qws.forEach(function(s,i){s.classList.toggle('on',i<n)})}
  if(arp&&ab){var r4=ab.getBoundingClientRect();arp.style.setProperty('--ap',Math.max(0,Math.min(1,(vh*.3-r4.top)/(r4.height-vh*.5))).toFixed(4))}
  if(cfl&&cfw){var r5=cfw.getBoundingClientRect();cfl.style.setProperty('--cl',Math.max(0,Math.min(1,(vh*.7-r5.top)/r5.height)).toFixed(3))}
}
addEventListener('scroll',function(){if(!tk){tk=1;requestAnimationFrame(onScroll)}},{passive:true});
addEventListener('resize',function(){placeSt();synMode();onScroll()});
onScroll();
if(top)top.addEventListener('click',function(){scrollTo({top:0,behavior:RM?'auto':'smooth'})});
if(RM&&jr){jr.style.setProperty('--pp',1);sts.forEach(function(s){s.classList.add('on')})}
if(RM&&q)qws.forEach(function(s){s.classList.add('on')});

/* ---------- menus ---------- */
var bg=$('.burger'),mn=$('#mnav');
function mOpen(o){if(!mn)return;if(o){mn.hidden=false;requestAnimationFrame(function(){mn.classList.add('on')});d.body.style.overflow='hidden';bg.setAttribute('aria-expanded','true');$('.mx',mn).focus()}
  else{mn.classList.remove('on');d.body.style.overflow='';bg.setAttribute('aria-expanded','false');setTimeout(function(){mn.hidden=true},350);bg.focus()}}
if(bg){bg.addEventListener('click',function(){mOpen(true)});$('.mx',mn).addEventListener('click',function(){mOpen(false)});
  $$('a',mn).forEach(function(a){a.addEventListener('click',function(){mOpen(false)})});
  $$('nav>a',mn).forEach(function(a,i){a.style.transitionDelay=(i*50+80)+'ms'})}
$$('.ddb').forEach(function(b){b.addEventListener('click',function(e){var dd=b.parentNode;if(!HOVER&&!dd.classList.contains('open')){e.preventDefault();$$('.dd.open').forEach(function(x){x.classList.remove('open')});dd.classList.add('open')}})});
d.addEventListener('click',function(e){if(!e.target.closest('.dd'))$$('.dd.open').forEach(function(x){x.classList.remove('open')})});

/* ---------- faq: one open per list ---------- */
$$('.faq-l').forEach(function(l){var it=$$('details',l);it.forEach(function(x){x.addEventListener('toggle',function(){if(x.open)it.forEach(function(o){if(o!==x)o.open=false})})})});

/* ---------- lightbox ---------- */
var lb=$('.lb'),lbi=lb&&$('img',lb),last;
function lbClose(){lb.classList.remove('on');setTimeout(function(){lb.hidden=true;lbi.src=''},300);d.body.style.overflow='';if(last)last.focus()}
$$('img[data-lb]').forEach(function(im){im.setAttribute('tabindex','0');im.setAttribute('role','button');
  function op(){last=im;lbi.src=im.getAttribute('data-lb');lbi.alt=im.alt;lb.hidden=false;requestAnimationFrame(function(){lb.classList.add('on')});d.body.style.overflow='hidden';$('.lbx',lb).focus()}
  im.addEventListener('click',op);im.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();op()}})});
if(lb){lb.addEventListener('click',function(e){if(e.target!==lbi)lbClose()})}
d.addEventListener('keydown',function(e){if(e.key==='Escape'){if(lb&&!lb.hidden)lbClose();else if(mn&&!mn.hidden)mOpen(false)}});
})();
