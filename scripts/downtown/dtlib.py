import asyncio, json, re
from playwright.async_api import async_playwright
S="https://downtownoffice.agent.wallacetn.com"
OFF='/home/ubuntu/repos/wallace-office-site-roadmap/offices/downtown/'
LUX='/search#location_search_field=Knox%20County%2C%20TN&status=active&pricemin=650000'
REPL=[('https://nelson-realtors.com/directory/offices/office-1','/directory/offices/downtown-office'),
      ('https://nelson-realtors.com',''),('https://nelsonoffice.agent.wallacetn.com',''),
      ('Wallace Nelson','Wallace Downtown'),('WALLACE NELSON','WALLACE DOWNTOWN'),
      ('Knoxville &amp; East Tennessee','Downtown Knoxville &amp; Knox County'),('Knoxville & East Tennessee','Downtown Knoxville & Knox County'),
      ('KNOXVILLE & EAST TENNESSEE','DOWNTOWN KNOXVILLE & KNOX COUNTY'),('Knoxville and East Tennessee','downtown Knoxville and Knox County')]
async def ajax(pg,d,t=25000): return await pg.evaluate("([d,t])=>new Promise(res=>{setTimeout(()=>res('TIMEOUT'),t);FLBuilder.ajax(d,r=>res(String(r).slice(0,300)))})",[d,t])
async def save(pg,node,patch): return await pg.evaluate("""([id,patch])=>new Promise(res=>{setTimeout(()=>res('TIMEOUT'),25000);const s=Object.assign({},FLBuilderSettingsConfig.nodes[id]||{},patch);FLBuilder.ajax({action:'save_settings',node_id:id,settings:s},r=>res(String(r).slice(0,80)))})""",[node,patch])
async def wait_bb(pg):
    for _ in range(60):
        if await pg.evaluate("()=>!!(window.FLBuilderSettingsConfig&&FLBuilderSettingsConfig.nodes&&Object.keys(FLBuilderSettingsConfig.nodes).length)"): break
        await pg.wait_for_timeout(1000)
    await pg.wait_for_timeout(3000)
    fr=[f for f in pg.frames if 'fl_builder_ui_iframe' in f.url]
    return fr[0] if fr else pg.main_frame
async def open_bb(pg,url):
    await pg.goto(url,wait_until="domcontentloaded",timeout=120000); return await wait_bb(pg)
async def reload_bb(pg):
    await pg.reload(wait_until="domcontentloaded",timeout=120000); return await wait_bb(pg)
async def rows(ui): return await ui.evaluate("()=>[...document.querySelectorAll('.fl-builder-content > .fl-row')].map(r=>r.dataset.node)")
async def live_ids(ui): return set(await ui.evaluate("()=>[...document.querySelectorAll('.fl-builder-content [data-node]')].map(e=>e.dataset.node)"))
async def fix_texts(pg,ui,skip=()):
    live=await live_ids(ui); nodes=await pg.evaluate("()=>FLBuilderSettingsConfig.nodes")
    for i,s in nodes.items():
        if i not in live or i in skip: continue
        patch={}
        for k,v in s.items():
            if not isinstance(v,str): continue
            v2=v
            if 'Murfreesboro' in v2 and k.endswith('link'): v2=LUX
            for a,b in REPL: v2=v2.replace(a,b)
            if v2!=v: patch[k]=v2
        if patch: print(' fix',i,s.get('type'),list(patch), await save(pg,i,patch))
async def publish(pg):
    await ajax(pg,{"action":"render_layout"}); await pg.wait_for_timeout(2000)
    print(' publish',await pg.evaluate("()=>new Promise(res=>FLBuilder.ajax({action:'save_layout',publish:true},r=>res(String(r).slice(0,120))))"))
async def verify(pg,path):
    await pg.goto(f"{S}{path}?v={int(asyncio.get_event_loop().time())}",wait_until="load",timeout=120000); await pg.wait_for_timeout(4000)
    r=await pg.evaluate("()=>{const h=document.body.innerHTML; return {title:document.title, tlh:!!document.getElementById('tlh'), nelson:(h.match(/nelson/gi)||[]).length, maryville:(h.match(/maryville/gi)||[]).length, h2:[...document.querySelectorAll('#tlh h2')].map(h=>h.innerText.replace(/\\s+/g,' ')).slice(0,12)}}")
    print(' LIVE',path,json.dumps(r)); return r
async def browser(p):
    b=await p.chromium.connect_over_cdp("http://localhost:29229"); pg=await b.contexts[0].new_page(); await pg.set_viewport_size({"width":1440,"height":900}); return pg
