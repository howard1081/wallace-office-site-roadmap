import asyncio, sys, json
from playwright.async_api import async_playwright
# usage: bbapply3.py <post> <html> <target_row> <rows_to_delete,comma> <slug> publish|draft
POST=int(sys.argv[1]); HTMLF=sys.argv[2]; ROW=sys.argv[3]; DEL=[x for x in sys.argv[4].split(',') if x]; SLUG=sys.argv[5]; MODE=sys.argv[6]
html=open(HTMLF).read()
URL=f"https://twinlakesoffice.agent.wallacetn.com/?page_id={POST}&preview=true&fl_builder&fl_builder_ui"
async def ajax(pg,d): return await pg.evaluate("(d)=>new Promise(res=>{setTimeout(()=>res('TIMEOUT'),25000);FLBuilder.ajax(d,r=>res(String(r).slice(0,120)))})",d)
async def save(pg,node,patch): return await pg.evaluate("""([id,patch])=>new Promise(res=>{setTimeout(()=>res('TIMEOUT'),25000);const s=Object.assign({},FLBuilderSettingsConfig.nodes[id]||{},patch);FLBuilder.ajax({action:'save_settings',node_id:id,settings:s},r=>res(String(r).slice(0,80)))})""",[node,patch])
async def ui_of(pg):
    await pg.reload(wait_until="domcontentloaded"); await pg.wait_for_timeout(15000)
    return [f for f in pg.frames if 'fl_builder_ui_iframe' in f.url][0]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp("http://localhost:29229"); pg=await b.contexts[0].new_page(); await pg.set_viewport_size({"width":1440,"height":900})
        await pg.goto(URL,wait_until="domcontentloaded",timeout=90000); await pg.wait_for_timeout(12000)
        print(await pg.evaluate("()=>({postId:FLBuilderConfig.postId,status:FLBuilderConfig.postStatus})"))
        ui=[f for f in pg.frames if 'fl_builder_ui_iframe' in f.url][0]
        info=await ui.evaluate("(row)=>{const r=document.querySelector('.fl-node-'+row); return {cols:[...r.querySelectorAll('.fl-col')].map(c=>c.dataset.node), mods:[...r.querySelectorAll('.fl-module')].map(m=>({n:m.dataset.node,t:m.dataset.type}))}}",ROW)
        print("row info",info)
        col=info['cols'][0]
        r=await ajax(pg,{"action":"render_new_module","parent_id":col,"type":"html","position":0,"node_preview":0})
        print("new module",r)
        ui=await ui_of(pg)
        info2=await ui.evaluate("(row)=>[...document.querySelector('.fl-node-'+row).querySelectorAll('.fl-module')].map(m=>({n:m.dataset.node,t:m.dataset.type}))",ROW)
        new=[m for m in info2 if m['t']=='html' and m['n'] not in [x['n'] for x in info['mods']]]
        print("html module",new)
        if not new: return
        nid=new[0]['n']
        print("html set",await save(pg,nid,{"html":html,"margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}))
        for m in info['mods']: print("del mod",m['n'],await ajax(pg,{"action":"delete_node","node_id":m['n']}))
        for cid in info['cols'][1:]: print("del col",cid,await ajax(pg,{"action":"delete_node","node_id":cid}))
        for d in DEL: print("del row",d,await ajax(pg,{"action":"delete_node","node_id":d}))
        print("row set",await save(pg,ROW,{"bg_type":"none","bg_color":"","padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","width":"full","content_width":"full","full_height":"default","min_height":""}))
        print("col set",await save(pg,col,{"size":"100","padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}))
        await ajax(pg,{"action":"render_layout"}); await pg.wait_for_timeout(3000)
        if MODE=='publish': print("publish",await pg.evaluate("()=>new Promise(res=>FLBuilder.ajax({action:'save_layout',publish:true},r=>res(String(r).slice(0,120))))"))
        else: print("draft",await pg.evaluate("()=>new Promise(res=>FLBuilder.ajax({action:'save_draft'},r=>res(String(r).slice(0,120))))"))
        await pg.wait_for_timeout(3000)
        await pg.goto(f"https://twinlakesoffice.agent.wallacetn.com/{SLUG}?v=31",wait_until="load",timeout=90000); await pg.wait_for_timeout(5000)
        print("LIVE", await pg.evaluate("()=>({rows:[...document.querySelectorAll('.fl-row')].map(r=>r.dataset.node+':'+(r.innerText||'').replace(/\\s+/g,' ').slice(0,40)), tlh:!!document.getElementById('tlh'), nelson:(document.body.innerHTML.match(/nelson/gi)||[]).length, h2:[...document.querySelectorAll('#tlh h2')].map(h=>h.innerText.replace(/\\s+/g,' '))})"))
        await pg.screenshot(path=f"/tmp/{SLUG}_new.png", full_page=True)
        await pg.close()
asyncio.run(main())
