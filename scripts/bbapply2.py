import asyncio, sys
from playwright.async_api import async_playwright
POST=int(sys.argv[1]); HTMLF=sys.argv[2]; MODE=sys.argv[3] if len(sys.argv)>3 else 'dry'   # dry | draft | publish
KEEP_ROWS={'iwo6h2u8lrn0'}
html=open(HTMLF).read()
URL=f"https://twinlakesoffice.agent.wallacetn.com/?page_id={POST}&preview=true&fl_builder&fl_builder_ui"
async def ajax(pg,d): return await pg.evaluate("(d)=>new Promise(res=>{setTimeout(()=>res('TIMEOUT'),20000);FLBuilder.ajax(d,r=>res(String(r).slice(0,120)))})",d)
async def save(pg,node,patch): return await pg.evaluate("""([id,patch])=>new Promise(res=>{setTimeout(()=>res('TIMEOUT'),20000);const s=Object.assign({},FLBuilderSettingsConfig.nodes[id],patch);FLBuilder.ajax({action:'save_settings',node_id:id,settings:s},r=>res(String(r).slice(0,80)))})""",[node,patch])
async def ui_of(pg):
    await pg.reload(wait_until="domcontentloaded"); await pg.wait_for_timeout(15000)
    return [f for f in pg.frames if 'fl_builder_ui_iframe' in f.url][0]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp("http://localhost:29229"); pg=await b.contexts[0].new_page(); await pg.set_viewport_size({"width":1440,"height":900})
        await pg.goto(URL,wait_until="domcontentloaded",timeout=90000); await pg.wait_for_timeout(12000)
        print(await pg.evaluate("()=>({postId:FLBuilderConfig.postId,status:FLBuilderConfig.postStatus})"))
        ui=[f for f in pg.frames if 'fl_builder_ui_iframe' in f.url][0]
        rows=await ui.evaluate("()=>[...document.querySelectorAll('.fl-builder-content > .fl-row')].map(r=>[r.dataset.node,(r.innerText||'').replace(/\\s+/g,' ').slice(0,70)])")
        print("rows",rows)
        if MODE=='dry': return
        for r,_ in rows:
            if r not in KEEP_ROWS: print("del",r,await ajax(pg,{"action":"delete_node","node_id":r}))
        ui=await ui_of(pg)
        live=set(await ui.evaluate("()=>[...document.querySelectorAll('.fl-builder-content [data-node]')].map(e=>e.dataset.node)"))
        mods=await ui.evaluate("()=>[...document.querySelectorAll('.fl-builder-content .fl-module')].map(m=>({n:m.dataset.node,t:m.dataset.type}))")
        for m in mods:
            if m['n'] in live and m['t']!='html': print("del mod",m['n'],await ajax(pg,{"action":"delete_node","node_id":m['n']}))
        print("html set",await save(pg,'2rqte7ysud41',{"html":html,"margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}))
        print("row set",await save(pg,'iwo6h2u8lrn0',{"bg_type":"none","bg_color":"","padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","width":"full","content_width":"full"}))
        print("col set",await save(pg,'tx3lp5ae6g7c',{"padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}))
        await ajax(pg,{"action":"render_layout"}); await pg.wait_for_timeout(3000)
        if MODE=='publish': print("publish",await pg.evaluate("()=>new Promise(res=>FLBuilder.ajax({action:'save_layout',publish:true},r=>res(String(r).slice(0,120))))"))
        else: print("draft save",await pg.evaluate("()=>new Promise(res=>FLBuilder.ajax({action:'save_draft'},r=>res(String(r).slice(0,120))))"))
        ui=await ui_of(pg)
        print("rows after",await ui.evaluate("()=>[...document.querySelectorAll('.fl-builder-content > .fl-row')].map(r=>r.dataset.node)"),"tlh:",await ui.evaluate("()=>!!document.getElementById('tlh')"))
asyncio.run(main())
