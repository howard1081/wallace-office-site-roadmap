# usage: page_apply.py office | bb3 <post> <file> <row> <del,csv> <path> | contact | luxury | fix <post> <path>
import asyncio, sys
from dtlib import *
ZERO={"padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}
async def main():
    a=sys.argv[1:]
    async with async_playwright() as p:
        pg=await browser(p)
        if a[0]=='office':
            ui=await open_bb(pg,f"{S}/?page_id=178&preview=true&fl_builder&fl_builder_ui")
            assert await pg.evaluate("()=>FLBuilderConfig.postId")==178
            for r in await rows(ui):
                if r!='iwo6h2u8lrn0': print('del row',r,await ajax(pg,{"action":"delete_node","node_id":r}))
            ui=await reload_bb(pg)
            mods=await ui.evaluate("()=>[...document.querySelectorAll('.fl-builder-content .fl-module')].map(m=>({n:m.dataset.node,t:m.dataset.type}))")
            col=await ui.evaluate("()=>document.querySelector('.fl-node-2rqte7ysud41').closest('.fl-col').dataset.node")
            for m in mods:
                if m['t']!='html': print('del mod',m,await ajax(pg,{"action":"delete_node","node_id":m['n']}))
            print('html',await save(pg,'2rqte7ysud41',{"html":open(OFF+'office.html').read(),**{k:"0" for k in ZERO if k.startswith('margin')}}))
            print('row',await save(pg,'iwo6h2u8lrn0',{"bg_type":"none","bg_color":"","padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","width":"full","content_width":"full"}))
            print('col',await save(pg,col,ZERO))
            await publish(pg); return
        if a[0]=='bb3':
            post,f,row,dels,path=int(a[1]),a[2],a[3],[x for x in a[4].split(',') if x],a[5]
            ui=await open_bb(pg,f"{S}/?page_id={post}&preview=true&fl_builder&fl_builder_ui")
            assert await pg.evaluate("()=>FLBuilderConfig.postId")==post
            info=await ui.evaluate("(row)=>{const r=document.querySelector('.fl-node-'+row); return {cols:[...r.querySelectorAll('.fl-col')].map(c=>c.dataset.node), mods:[...r.querySelectorAll('.fl-module')].map(m=>({n:m.dataset.node,t:m.dataset.type}))}}",row)
            col=info['cols'][0]
            print('new',(await ajax(pg,{"action":"render_new_module","parent_id":col,"type":"html","position":0,"node_preview":0}))[:80])
            ui=await reload_bb(pg)
            info2=await ui.evaluate("(row)=>[...document.querySelector('.fl-node-'+row).querySelectorAll('.fl-module')].map(m=>({n:m.dataset.node,t:m.dataset.type}))",row)
            new=[m for m in info2 if m['t']=='html' and m['n'] not in [x['n'] for x in info['mods']]]
            print('html module',new); nid=new[0]['n']
            print('html',await save(pg,nid,{"html":open(OFF+f).read(),"margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}))
            for m in info['mods']: print('del mod',m['n'],await ajax(pg,{"action":"delete_node","node_id":m['n']}))
            for c in info['cols'][1:]: print('del col',c,await ajax(pg,{"action":"delete_node","node_id":c}))
            for d in dels: print('del row',d,await ajax(pg,{"action":"delete_node","node_id":d}))
            print('row',await save(pg,row,{"bg_type":"none","bg_color":"","padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","width":"full","content_width":"full","full_height":"default","min_height":""}))
            print('col',await save(pg,col,{"size":"100",**ZERO}))
            ui=await reload_bb(pg); await fix_texts(pg,ui,skip=(nid,)); await publish(pg)
            await verify(pg,path); await pg.screenshot(path=f"/tmp/live_{post}.png",full_page=True); return
        if a[0]=='contact':
            ui=await open_bb(pg,f"{S}/?page_id=16&preview=true&fl_builder&fl_builder_ui")
            assert await pg.evaluate("()=>FLBuilderConfig.postId")==16
            info=await ui.evaluate("()=>{const r=document.querySelector('.fl-node-yquxi1ed8cvw'); return {cols:[...r.querySelectorAll('.fl-col')].map(c=>c.dataset.node), mods:[...r.querySelectorAll('.fl-module')].map(m=>m.dataset.node)}}")
            print(info)
            print('new',(await ajax(pg,{"action":"render_new_module","parent_id":info['cols'][0],"type":"html","position":0,"node_preview":0}))[:80])
            ui=await reload_bb(pg)
            m2=await ui.evaluate("()=>[...document.querySelectorAll('.fl-node-yquxi1ed8cvw .fl-module')].map(m=>({n:m.dataset.node,t:m.dataset.type}))")
            new=[m for m in m2 if m['t']=='html' and m['n'] not in info['mods']]; print(new); nid=new[0]['n']
            print('html',await save(pg,nid,{"html":open(OFF+'contact.html').read(),"margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}))
            print('row',await save(pg,'yquxi1ed8cvw',{"bg_type":"none","bg_color":"","padding_top":"0","padding_left":"0","padding_right":"0"}))
            await publish(pg); await verify(pg,'/contact'); await pg.screenshot(path="/tmp/live_16.png",full_page=True); return
        if a[0]=='luxury':
            ui=await open_bb(pg,f"{S}/?page_id=8&preview=true&fl_builder&fl_builder_ui")
            assert await pg.evaluate("()=>FLBuilderConfig.postId")==8
            print('btn',await save(pg,'o4sa9wpijymh',{"link":LUX}))
            print('head',await save(pg,'4106jk28egci',{"text":"SOPHISTICATED GUIDANCE FOR LUXURY HOMES IN DOWNTOWN KNOXVILLE &amp; KNOX COUNTY"}))
            await fix_texts(pg,ui); await publish(pg); await verify(pg,'/luxury'); return
        if a[0]=='fix':
            post,path=int(a[1]),a[2]
            ui=await open_bb(pg,f"{S}/?page_id={post}&preview=true&fl_builder&fl_builder_ui")
            assert await pg.evaluate("()=>FLBuilderConfig.postId")==post
            await fix_texts(pg,ui); await publish(pg); await verify(pg,path); return
asyncio.run(main())
