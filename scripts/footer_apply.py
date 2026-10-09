import asyncio, sys, json
from playwright.async_api import async_playwright
html=open('footer.html').read()
URL="https://twinlakesoffice.agent.wallacetn.com/fl-builder-template/footer?fl_builder&fl_builder_ui"
async def ajax(pg,d): return await pg.evaluate("(d)=>new Promise(res=>{setTimeout(()=>res('TIMEOUT'),25000);FLBuilder.ajax(d,r=>res(String(r).slice(0,300)))})",d)
async def save(pg,node,patch): return await pg.evaluate("""([id,patch])=>new Promise(res=>{setTimeout(()=>res('TIMEOUT'),25000);const s=Object.assign({},FLBuilderSettingsConfig.nodes[id]||{},patch);FLBuilder.ajax({action:'save_settings',node_id:id,settings:s},r=>res(String(r).slice(0,100)))})""",[node,patch])
async def ui_of(pg):
    await pg.reload(wait_until="domcontentloaded"); await pg.wait_for_timeout(15000)
    return [f for f in pg.frames if 'fl_builder_ui_iframe' in f.url][0]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp("http://localhost:29229"); pg=await b.contexts[0].new_page(); await pg.set_viewport_size({"width":1440,"height":900})
        await pg.goto(URL,wait_until="domcontentloaded",timeout=90000); await pg.wait_for_timeout(12000)
        print(await pg.evaluate("()=>({postId:FLBuilderConfig.postId,status:FLBuilderConfig.postStatus})"))
        ui=[f for f in pg.frames if 'fl_builder_ui_iframe' in f.url][0]
        own=lambda sel: ui.evaluate(f"()=>[...document.querySelectorAll('.fl-builder-content-162 {sel}')].map(e=>e.dataset.node)")
        mods=await own('.fl-module'); cols=await own('.fl-col'); print("mods",mods,"cols",cols)
        # add html module into first column
        r=await ajax(pg,{"action":"render_new_module","parent_id":"zjcymbla25ko","type":"html","position":0,"node_preview":0})
        print("new module raw:", r[:300])
        try: nid=json.loads(r)['nodeId'] if r.startswith('{') else None
        except Exception: nid=None
        if not nid:
            import re; m=re.search(r'fl-node-([a-z0-9]{12})',r); nid=m.group(1) if m else None
        print("nid",nid)
        if not nid: return
        print("html set",await save(pg,nid,{"type":"html","html":html,"margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}))
        for m in mods: print("del mod",m,await ajax(pg,{"action":"delete_node","node_id":m}))
        ui=await ui_of(pg)
        cols=await own('.fl-col'); print("cols now",cols)
        for c in cols:
            if c!='zjcymbla25ko': print("del col",c,await ajax(pg,{"action":"delete_node","node_id":c}))
        print("col set",await save(pg,'zjcymbla25ko',{"size":100,"padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}))
        print("row set",await save(pg,'epw93ztkybmf',{"bg_type":"none","bg_color":"","padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","margin_top":"0","margin_bottom":"0","width":"full","content_width":"full"}))
        await ajax(pg,{"action":"render_layout"}); await pg.wait_for_timeout(3000)
        print("publish",await pg.evaluate("()=>new Promise(res=>FLBuilder.ajax({action:'save_layout',publish:true},r=>res(String(r).slice(0,120))))"))
        ui=await ui_of(pg)
        print("after: mods",await own('.fl-module'),"cols",await own('.fl-col'),"tlf:",await ui.evaluate("()=>!!document.getElementById('tlf')"))
        await pg.close()
asyncio.run(main())
