/* rehost.expert — interactions. All contact goes through the Google Form (no email links). */
(function(){
  var top=document.querySelector('.top');
  function onScroll(){top.classList.toggle('scrolled',window.scrollY>8);}
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();

  // reveal on scroll
  var rv=document.querySelectorAll('.rv,.stat');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    rv.forEach(function(el){io.observe(el);});
  } else rv.forEach(function(el){el.classList.add('in');});

  // count-up stats
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nums=document.querySelectorAll('[data-count]');
  if(!reduce&&'IntersectionObserver' in window){
    var co=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;co.unobserve(e.target);var el=e.target,to=+el.dataset.count,t0=null;
      function step(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/1200);el.textContent=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(step);}
      el.textContent='0';requestAnimationFrame(step);});},{threshold:.4});
    nums.forEach(function(n){co.observe(n);});
  }

  // chat bubbles appear one by one
  var chat=document.getElementById('chat');
  if(chat){var bubs=chat.querySelectorAll('.bub');
    function play(){bubs.forEach(function(b,i){setTimeout(function(){b.classList.add('in');if(!reduce&&i>0)chat.scrollTo({top:b.offsetTop-60,behavior:'smooth'});},reduce?0:400+i*1100);});}
    if('IntersectionObserver' in window&&!reduce){var po=new IntersectionObserver(function(es){if(es[0].isIntersecting){play();po.disconnect();}},{threshold:.3});po.observe(chat);}else play();}

  // tabs (food / drink)
  var tabs=[].slice.call(document.querySelectorAll('[role=tab]'));
  function sel(t){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;var p=document.getElementById(x.getAttribute('aria-controls'));p.hidden=!on;if(on)p.querySelectorAll('.rv').forEach(function(r){r.classList.add('in');});});}
  tabs.forEach(function(t,i){t.addEventListener('click',function(){sel(t);});t.addEventListener('keydown',function(e){var k=e.key,j=null;if(k==='ArrowRight')j=(i+1)%tabs.length;if(k==='ArrowLeft')j=(i-1+tabs.length)%tabs.length;if(j!==null){e.preventDefault();sel(tabs[j]);tabs[j].focus();}});});

  // ---- shared contact details: selection panel + Get in touch (one validation, one saved copy in localStorage) ----
  var g=function(id){return document.getElementById(id);};
  var CKEYS=['name','biz','email','phone','site'],CKEY='rehost-contact-v1',cd={};
  try{var raw=JSON.parse(localStorage.getItem(CKEY)||'{}')||{};CKEYS.forEach(function(k){cd[k]=raw[k]||raw['f-'+k]||'';});if(!cd.site)cd.site=localStorage.getItem('rehost-site-v1')||'';}catch(e){CKEYS.forEach(function(k){cd[k]=cd[k]||'';});}
  function saveCd(){try{localStorage.setItem(CKEY,JSON.stringify(cd));}catch(e){}}
  var EMPTY={name:'Please enter your name.',biz:'Please enter your business name.',email:'Please enter your email address.',phone:'Please enter your phone number.',site:'Please enter your website address.'};
  function fieldError(k,v){v=(v||'').trim();
    if(!v)return EMPTY[k];
    if(k==='email'&&!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v))return 'Please enter a valid email address, like you@yourbusiness.ie.';
    if(k==='phone'&&(v.replace(/\D/g,'').length<7||/[^\d\s()+.\-]/.test(v)))return 'Please enter a valid phone number, like 087 123 4567.';
    if(k==='site'&&(/\s/.test(v)||!/[a-z0-9-]\.[a-z]{2,}/i.test(v)))return 'Please enter a website address, like yourbusiness.ie.';
    return '';}
  var groups=[];
  function ContactGroup(pre,msgId,onChange){
    var grp={pre:pre,onChange:onChange};
    grp.show=function(k,msg){var el=g(pre+k),er=g(pre+k+'-err');if(!el)return;if(msg){el.setAttribute('aria-invalid','true');er.textContent=msg;er.hidden=false;}else{el.removeAttribute('aria-invalid');er.textContent='';er.hidden=true;}};
    grp.values=function(){var v={};CKEYS.forEach(function(k){v[k]=g(pre+k).value.trim();});return v;};
    grp.allOk=function(){return CKEYS.every(function(k){return !fieldError(k,g(pre+k).value);});};
    grp.validate=function(){var first=null;CKEYS.forEach(function(k){var m=fieldError(k,g(pre+k).value);grp.show(k,m);if(m&&!first)first=k;});
      var fm=g(msgId);if(first){fm.textContent='Please fill in all the required fields before sending.';fm.hidden=false;g(pre+first).focus();}else{fm.hidden=true;fm.textContent='';}
      return !first;};
    grp.tidy=function(k){var el=g(pre+k);if(el.getAttribute('aria-invalid')&&!fieldError(k,el.value))grp.show(k,'');if(!g(msgId).hidden&&grp.allOk())g(msgId).hidden=true;};
    CKEYS.forEach(function(k){var el=g(pre+k);el.value=cd[k]||'';
      el.addEventListener('input',function(){cd[k]=el.value;saveCd();
        groups.forEach(function(o){if(o!==grp){var x=g(o.pre+k);if(x.value!==el.value)x.value=el.value;o.tidy(k);}if(o.onChange)o.onChange();});
        grp.tidy(k);});
      el.addEventListener('blur',function(){if(el.getAttribute('aria-invalid'))grp.show(k,fieldError(k,el.value));});});
    groups.push(grp);return grp;}
  // Send values to the Google Form: a normal HTML form POST into a hidden iframe (no relay, no email links).
  function gfSend(fid,v,btn,label,done){
    var post=g(fid+'-post'),sink=g(fid+'-sink'),t=btn.querySelector('.csend-t')||btn.lastChild,timer;
    post.querySelectorAll('[data-k]').forEach(function(inp){inp.value=v[inp.dataset.k]||'';});
    function finish(ok){sink.removeEventListener('load',onLoad);clearTimeout(timer);btn.disabled=false;btn.classList.remove('sending');t.textContent=label;done(ok);}
    function onLoad(){finish(true);}
    sink.addEventListener('load',onLoad);
    btn.disabled=true;btn.classList.add('sending');t.textContent='Sending\u2026';
    timer=setTimeout(function(){finish(false);},20000);
    post.submit();}

  // Get in touch form
  if(g('c-form')){
    var cgrp=ContactGroup('c-','c-msg',null),cform=g('c-form'),cthx=g('c-thanks');
    cform.addEventListener('submit',function(e){e.preventDefault();
      if(!cgrp.validate())return;
      var v=cgrp.values();v.help=g('c-help').value.trim();
      gfSend('c',v,g('c-send'),'Send message',function(ok){
        var m=g('c-msg');
        if(!ok){m.textContent='Sorry, that didn\u2019t send. Please try again, or use the Google Form link below.';m.hidden=false;return;}
        cform.hidden=true;cthx.hidden=false;g('c-help').value='';
        g('c-card').scrollIntoView({behavior:reduce?'auto':'smooth',block:'center'});cthx.focus({preventScroll:true});});});
    g('c-again').addEventListener('click',function(){cthx.hidden=true;cform.hidden=false;g('c-help').focus();});
  }

  // services picker
  var rows=[].slice.call(document.querySelectorAll('.svc'));
  if(!rows.length||!document.getElementById('send'))return;
  var KEY='rehost-picks-v3',state={};
  try{state=JSON.parse(localStorage.getItem(KEY)||'{}')||{};}catch(e){state={};}
  rows.forEach(function(r){var i=r.dataset.i;if(state[i]){var inp=r.querySelector('input[value='+state[i]+']');if(inp){inp.checked=true;r.dataset.v=state[i];}}
    r.addEventListener('change',function(e){state[i]=e.target.value;r.dataset.v=e.target.value;save();render();});});
  function save(){try{localStorage.setItem(KEY,JSON.stringify(state));}catch(e){}}
  var $=function(id){return document.getElementById(id);};
  function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
  function pick(v){return rows.filter(function(r){return state[r.dataset.i]===v;});}
  function nm(r){return r.dataset.name.replace(/&amp;/g,'&');}
  function suggest(yes){
    var names=yes.map(nm),has=function(a){return a.some(function(x){return names.indexOf(x)>-1;});};
    if(!names.length)return null;
    var pkg=has(['Instagram','Facebook','Email inbox management','WhatsApp morning summary','Posts','X (Twitter)','TikTok','Google reviews','Other review sites'])?'Full service':has(['Area pages with maps','News and events page','Listings and directories','Live bookings or availability calendar'])?'Growth':'Essentials';
    var add=names.filter(function(x){return /ordering automation|SEO|AI consultation/.test(x);});
    if(add.length===names.length)pkg=null;
    return {pkg:pkg,add:add};
  }
  function render(){
    var y=pick('yes'),m=pick('maybe'),n=pick('no'),left=rows.length-y.length-m.length-n.length;
    $('c-yes').textContent=y.length;$('c-maybe').textContent=m.length;$('c-no').textContent=n.length;$('c-left').textContent=left;
    var tot=rows.length,mt=document.querySelector('.meter');
    mt.querySelector('.y').style.width=(y.length/tot*100)+'%';mt.querySelector('.m').style.width=(m.length/tot*100)+'%';mt.querySelector('.n').style.width=(n.length/tot*100)+'%';
    $('sum-sub').textContent=(y.length+m.length+n.length)?(left?left+' still to decide.':'All '+tot+' decided. Nice one.'):'Nothing picked yet. Choose Yes, Maybe or No for each service.';
    var h='';
    if(y.length)h+='<h4>Yes</h4><ul>'+y.map(function(r){return '<li>'+esc(nm(r))+'</li>';}).join('')+'</ul>';
    if(m.length)h+='<h4>Maybe</h4><ul>'+m.map(function(r){return '<li>'+esc(nm(r))+'</li>';}).join('')+'</ul>';
    $('chosen').innerHTML=h||'<p class="empty">Your Yes and Maybe picks will appear here.</p>';
    var s=suggest(y),sg=$('suggest');
    if(s){sg.hidden=false;sg.innerHTML=(s.pkg?'Closest package: <b>'+s.pkg+'</b>'+(s.add.length?' + '+s.add.length+' extra'+(s.add.length>1?'s':''):''):'<b>'+esc(s.add.join(', '))+'</b> on its own, or with any package')+'. <a href="#packages" style="color:#5eead4">See packages</a>';}else sg.hidden=true;
  }
  function selectionText(){
    var L=['Services selection:',''];
    ['yes','maybe','no'].forEach(function(v){var list=pick(v);if(!list.length)return;L.push((v==='yes'?'Yes':v==='maybe'?'Maybe':'No')+' ('+list.length+')');list.forEach(function(r){L.push('- '+nm(r)+' ['+r.dataset.area+']');});L.push('');});
    var undec=rows.filter(function(r){return !state[r.dataset.i];}).length;
    if(undec)L.push('Not decided: '+undec+' service'+(undec>1?'s':''),'');
    var s=suggest(pick('yes'));if(s)L.push(s.pkg?'Closest package: '+s.pkg+(s.add.length?' + '+s.add.join(', '):''):'Extras only: '+s.add.join(', '),'');
    var notes=$('f-notes').value.trim();if(notes)L.push('Notes:',notes);
    return L.join('\n').trim();
  }
  var pgrp=ContactGroup('f-','form-msg',null);
  var thanks=$('sel-thanks');
  $('sel-form').addEventListener('submit',function(e){e.preventDefault();thanks.hidden=true;
    if(!pgrp.validate())return;
    var v=pgrp.values();v.help=selectionText();
    gfSend('sel',v,$('send'),'Send my selection',function(ok){
      var m=$('form-msg');
      if(!ok){m.textContent='Sorry, that didn\u2019t send. Please try again.';m.hidden=false;return;}
      thanks.hidden=false;thanks.scrollIntoView({behavior:reduce?'auto':'smooth',block:'nearest'});});});
  // "Book an AI consultation": mark AI consultation as Yes and jump to the selection panel
  function pickAI(){var r=rows.filter(function(x){return nm(x)==='AI consultation';})[0];if(!r)return;
    state[r.dataset.i]='yes';r.dataset.v='yes';var inp=r.querySelector('input[value=yes]');if(inp)inp.checked=true;save();render();
    var p=document.querySelector('aside.summary');if(p)p.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});
    var first=CKEYS.map(function(k){return $('f-'+k);}).filter(function(x){return !x.value.trim();})[0];if(first)setTimeout(function(){first.focus({preventScroll:true});},400);}
  document.querySelectorAll('[data-pick-ai]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();pickAI();});});
  $('reset').addEventListener('click',function(){state={};save();rows.forEach(function(r){delete r.dataset.v;r.querySelectorAll('input').forEach(function(i){i.checked=false;});});render();});
  render();
  if(/[?&]pick=ai\b/.test(location.search))setTimeout(pickAI,300);
})();
