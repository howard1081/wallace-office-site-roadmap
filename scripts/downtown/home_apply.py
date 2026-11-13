import asyncio, sys
from dtlib import *
DEL=['k1zcma9i7f6d','pdm9eytrqjai','kbmixq7h2tu9','ympoewjd2f85','f69hrpzev1wi','29owediz548f','xg72mkltr3y5']
async def main():
    async with async_playwright() as p:
        pg=await browser(p); ui=await open_bb(pg,f"{S}/?fl_builder&fl_builder_ui")
        print(await pg.evaluate("()=>({postId:FLBuilderConfig.postId,status:FLBuilderConfig.postStatus})"))
        assert await pg.evaluate("()=>FLBuilderConfig.postId")==5
        rs=await rows(ui); print('rows',rs)
        for r in DEL:
            if r in rs: print('del row',r,await ajax(pg,{"action":"delete_node","node_id":r}))
        ui=await reload_bb(pg)
        mods=await ui.evaluate("()=>[...document.querySelectorAll('.fl-node-iwo6h2u8lrn0 .fl-module')].map(m=>({n:m.dataset.node,t:m.dataset.type}))")
        col=await ui.evaluate("()=>document.querySelector('.fl-node-2rqte7ysud41').closest('.fl-col').dataset.node")
        for m in mods:
            if m['t']!='html': print('del mod',m,await ajax(pg,{"action":"delete_node","node_id":m['n']}))
        print('html',await save(pg,'2rqte7ysud41',{"html":open(OFF+'block.html').read(),"margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}))
        print('row',await save(pg,'iwo6h2u8lrn0',{"bg_type":"none","bg_color":"","padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","width":"full","content_width":"full"}))
        print('col',col,await save(pg,col,{"padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"}))
        print('hero',await save(pg,'6cgdauv9y24w',{"heading":"Downtown Knoxville & Knox County Homes for Sale - Wallace Downtown"}))
        print('intro',await save(pg,'pnb805qdh2l4',{"text":'<em><span style="font-size: 14px;">Use the search tools below to explore homes in downtown Knoxville, South Knoxville, Sequoyah Hills, Fountain City and surrounding Knox County communities.</span></em>'}))
        ui=await reload_bb(pg)
        await fix_texts(pg,ui,skip=('2rqte7ysud41',))
        await publish(pg)
        await verify(pg,'/')
        await pg.screenshot(path='/tmp/live_home.png',full_page=True)
asyncio.run(main())
