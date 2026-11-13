import asyncio, sys, json, re
from dtlib import *
async def main():
    async with async_playwright() as p:
        pg=await browser(p)
        pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
        await pg.goto(f"{S}/wp-admin/admin.php?page=mx-appearance-responsive-footer",wait_until="domcontentloaded",timeout=120000); await pg.wait_for_timeout(3000)
        await pg.evaluate("()=>document.querySelectorAll('iframe#launcher, iframe[title*=essag]').forEach(f=>f.remove())")
        print('before',await pg.evaluate("()=>[...document.querySelectorAll('input[name=flbuilder]')].map(e=>e.value+(e.checked?'*':''))"))
        await pg.check('input[name=flbuilder][value="1"]',force=True)
        subs=await pg.evaluate("()=>[...document.querySelectorAll('input[type=submit],button[type=submit]')].map(e=>(e.name||'')+'|'+(e.value||e.innerText))")
        print('submits',subs)
        async with pg.expect_navigation(timeout=120000):
            await pg.evaluate("()=>{const b=[...document.querySelectorAll('input[type=submit],button[type=submit]')].find(e=>/update/i.test(e.value||e.innerText)); b.click();}")
        await pg.wait_for_timeout(3000)
        print('after',await pg.evaluate("()=>[...document.querySelectorAll('input[name=flbuilder]')].map(e=>e.value+(e.checked?'*':''))"),
              await pg.evaluate("()=>[...document.querySelectorAll('a')].filter(a=>/fl-builder-template|fl_builder/.test(a.href)).map(a=>a.innerText.trim()+'='+a.href).slice(0,5)"))
        ui=await open_bb(pg,f"{S}/fl-builder-template/footer?fl_builder&fl_builder_ui")
        pid=await pg.evaluate("()=>FLBuilderConfig.postId"); print('template post',pid, pg.url)
        own=lambda sel: ui.evaluate(f"()=>[...document.querySelectorAll('.fl-builder-content-{pid} {sel}')].map(e=>e.dataset.node)")
        mods=await own('.fl-module'); cols=await own('.fl-col'); rws=await own('.fl-row'); print('rows',rws,'cols',cols,'mods',mods)
        if not cols: print('NO COLUMNS - stop'); return
        col=cols[0]; row=rws[0]
        r=await ajax(pg,{"action":"render_new_module","parent_id":col,"type":"html","position":0,"node_preview":0})
        nid=re.search(r'"nodeId":"(\w+)"',r).group(1)
        print('nid',nid,'html',await save(pg,nid,{"type":"html","html":open(OFF+'footer.html').read(),"margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}))
        for m in mods: print('del mod',m,await ajax(pg,{"action":"delete_node","node_id":m}))
        ui=await reload_bb(pg)
        for c in await own('.fl-col'):
            if c!=col: print('del col',c,await ajax(pg,{"action":"delete_node","node_id":c}))
        for rr in (await own('.fl-row'))[1:]: print('del row',rr,await ajax(pg,{"action":"delete_node","node_id":rr}))
        print('col',await save(pg,col,{"size":100,"padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}))
        print('row',await save(pg,row,{"bg_type":"none","bg_color":"","padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","margin_top":"0","margin_bottom":"0","width":"full","content_width":"full"}))
        await publish(pg)
        ui=await reload_bb(pg); print('after mods',await own('.fl-module'),'tlf',await ui.evaluate("()=>!!document.getElementById('tlf')"))
        for path in ['/','/buyers']:
            await pg.goto(f"{S}{path}?v=f{pid}",wait_until="load",timeout=120000); await pg.wait_for_timeout(3000)
            print(path,'tlf',await pg.evaluate("()=>!!document.getElementById('tlf')"),'old8',await pg.evaluate("()=>document.body.innerText.includes('NORTHSHORE & PROPERTY MANAGEMENT')"))
asyncio.run(main())
