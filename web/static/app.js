/* NOVAPLAY web player — drives the Python backend, renders 64x64
   frames on the console's glass, sends keyboard/click/button actions. */

const PALETTE = [
  "#FFFFFF","#D2D2D2","#A0A0A0","#646464","#3C3C3C","#000000",
  "#E53AA3","#FF7BCC","#F93C31","#1E93FF","#87D8F1","#FFDC00",
  "#FF851B","#921231","#4FCC30","#88379B",
];
const PALETTE_RGB = PALETTE.map(h => [
  parseInt(h.slice(1,3),16), parseInt(h.slice(3,5),16), parseInt(h.slice(5,7),16),
]);
const KEY_TO_ACTION = { ArrowUp:1, ArrowDown:2, ArrowLeft:3, ArrowRight:4, " ":5, z:7, Z:7 };
const ANIM_MS = 70;

const $ = id => document.getElementById(id);
const listEl=$("gamelist"), searchEl=$("search"), countEl=$("count");
const screenEl=$("screen"), placeholder=$("placeholder"), glass=$("glass");
const banner=$("banner"), bannerText=$("bannerText"), bannerSub=$("bannerSub");
const gameTag=$("gameTag"), gameTitle=$("gameTitle");
const hudLevel=$("hudLevel"), hudWin=$("hudWin"), hudState=$("hudState"), hudLast=$("hudLast");
const captionEl=document.querySelector(".caption");
const ctx=screenEl.getContext("2d"); ctx.imageSmoothingEnabled=false;
const buf=document.createElement("canvas"); const bctx=buf.getContext("2d");

let GAMES=[], sel=null, session=null, actions=new Set();
let curW=64, curH=64, locked=false, lostBanner=false, wonBanner=false, prevLevel=1;

// header palette band (the 16 colours these games actually use)
PALETTE.forEach(h=>{const s=document.createElement("span");s.style.background=h;$("paletteStrip").appendChild(s);});

async function loadGames(){
  const r=await fetch("/api/games"); GAMES=(await r.json()).games;
  if(captionEl) captionEl.textContent=`NOVAPLAY™ portable · 16-colour · 64×64 · ${GAMES.length} cartridges`;
  renderList();
}
function renderList(){
  const q=searchEl.value.trim().toLowerCase();
  const filt=GAMES.filter(g=>!q||(g.short+" "+g.id+" "+g.title).toLowerCase().includes(q));
  countEl.textContent=`${filt.length}/${GAMES.length}`;
  listEl.innerHTML="";
  filt.forEach((g,i)=>{
    const ref=g.group==="reference";
    const li=document.createElement("li");
    li.className="cart"+(ref?" ref":"")+(g.id===sel?" active":"");
    li.dataset.id=g.id;
    li.style.animationDelay=Math.min(i*11,420)+"ms";
    li.innerHTML=
      `<span class="pad"></span>`+
      `<span><span class="gid">${g.short}</span>`+
      `<span class="gtitle">${g.title||g.id}</span></span>`+
      `<span class="grp">${ref?"REF":"GEN"}</span>`;
    li.onclick=()=>selectGame(g.id);
    listEl.appendChild(li);
  });
}
searchEl.addEventListener("input",renderList);

async function selectGame(id){
  sel=id; renderList(); hideBanner();
  try{
    const r=await fetch("/api/new",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({id})});
    const d=await r.json();
    if(d.error){alert(d.error);return;}
    session=d.session; actions=new Set(d.actions);
    gameTag.textContent=d.short; gameTitle.textContent=d.title||"";
    placeholder.style.display="none";
    prevLevel=d.state.level;
    updateButtons(); updateHud(d.state);
    glass.classList.remove("on"); void glass.offsetWidth; glass.classList.add("on");  // power-on flash
    await playFrames(d.frames);
  }catch(e){console.error(e);}
}

async function sendAction(action,x,y){
  if(!session||locked) return;
  if(typeof action==="number" && !actions.has(action)) return;
  let url="/api/step", body={session,action};
  if(action===6){body.x=x;body.y=y;}
  if(action==="reset"){url="/api/reset";body={session,full:false};}
  if(action==="full"){url="/api/reset";body={session,full:true};}
  if(typeof action==="object"&&action.level!==undefined){url="/api/level";body={session,level:action.level};}
  try{
    const r=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    const d=await r.json();
    if(d.error){console.warn(d.error);return;}
    if(url!=="/api/step"){prevLevel=d.state.level;hideBanner();}
    updateHud(d.state);
    await playFrames(d.frames);
    applyBanners(d.state);
  }catch(e){console.error(e);}
}

function drawHex(px,w,h){
  if(buf.width!==w||buf.height!==h){buf.width=w;buf.height=h;}
  const img=bctx.createImageData(w,h), data=img.data;
  for(let i=0;i<w*h;i++){
    const v=parseInt(px[i],16)&15, [r,g,b]=PALETTE_RGB[v], o=i*4;
    data[o]=r;data[o+1]=g;data[o+2]=b;data[o+3]=255;
  }
  bctx.putImageData(img,0,0);
  curW=w;curH=h;
  ctx.clearRect(0,0,screenEl.width,screenEl.height);
  ctx.drawImage(buf,0,0,screenEl.width,screenEl.height);
}
function playFrames(frames){
  return new Promise(resolve=>{
    if(!frames||!frames.length){resolve();return;}
    locked=true; let i=0;
    const step=()=>{
      const f=frames[i]; drawHex(f.px,f.w,f.h); i++;
      if(i<frames.length) setTimeout(step,ANIM_MS);
      else{locked=false;resolve();}
    };
    step();
  });
}

function updateHud(s){hudLevel.textContent=s.level;hudWin.textContent=s.win_levels;hudState.textContent=s.state;hudLast.textContent=s.last_action;}
function showBanner(cls,t,sub){banner.className="banner "+cls;bannerText.textContent=t;bannerSub.textContent=sub||"";}
function hideBanner(){banner.className="banner hidden";lostBanner=wonBanner=false;}
function applyBanners(s){
  if(s.won){wonBanner=true;locked=true;showBanner("win","YOU WIN!","R restart · or insert another cartridge");}
  else if(s.lost){lostBanner=true;locked=true;showBanner("lose","GAME OVER","press R to restart the level");}
  else if(s.level>prevLevel){showBanner("levelup","LEVEL "+s.level,"");setTimeout(()=>{if(!wonBanner&&!lostBanner)hideBanner();},1100);}
  prevLevel=s.level;
}
function updateButtons(){
  document.querySelectorAll("[data-act]").forEach(b=>{
    const a=parseInt(b.dataset.act,10);
    if(!isNaN(a)) b.disabled=!actions.has(a);
  });
}

// keyboard
document.addEventListener("keydown",e=>{
  if(e.target===searchEl) return;
  if(e.key==="Escape"){sel=null;renderList();return;}
  if(e.key==="r"||e.key==="R"){sendAction(e.shiftKey?"full":"reset");e.preventDefault();return;}
  if(e.key==="1"){sendAction({level:0});return;}
  if(e.key==="2"){sendAction({level:1});return;}
  if(e.key==="3"){sendAction({level:2});return;}
  const a=KEY_TO_ACTION[e.key];
  if(a!==undefined){if(lostBanner||wonBanner)return;sendAction(a);if(e.key===" ")e.preventDefault();}
});
// canvas click = ACTION6
screenEl.addEventListener("click",e=>{
  if(!session||locked||!actions.has(6))return;
  const rect=screenEl.getBoundingClientRect();
  const col=Math.floor((e.clientX-rect.left)/rect.width*curW);
  const row=Math.floor((e.clientY-rect.top)/rect.height*curH);
  sendAction(6,Math.max(0,Math.min(curW-1,col)),Math.max(0,Math.min(curH-1,row)));
});
// on-screen buttons
document.querySelectorAll("[data-act]").forEach(b=>{
  if(b.classList.contains("hub"))return;
  b.addEventListener("click",()=>{const a=parseInt(b.dataset.act,10);if(isNaN(a))return;if(lostBanner||wonBanner)return;sendAction(a);});
});
$("btnReset").onclick=()=>sendAction("reset");
$("btnFull").onclick=()=>sendAction("full");
document.querySelectorAll(".tab[data-level]").forEach(b=>b.onclick=()=>sendAction({level:parseInt(b.dataset.level,10)}));

loadGames();
