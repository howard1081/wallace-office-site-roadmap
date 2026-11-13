import asyncio
from dtlib import *
async def main():
    async with async_playwright() as p:
        pg=await browser(p)
        ui=await open_bb(pg,f"{S}/?page_id=178&preview=true&fl_builder&fl_builder_ui")
        assert await pg.evaluate("()=>FLBuilderConfig.postId")==178
        rs=await rows(ui); print('rows',rs)
        for r in rs:
            if r!='iwo6h2u8lrn0':
                print('del',r,await ajax(pg,{"action":"delete_node","node_id":r})); await pg.wait_for_timeout(800)
        ui=await reload_bb(pg); print('rows now',await rows(ui))
        await publish(pg); await verify(pg,'/our-office')
        print('live rows',await pg.evaluate("()=>[...document.querySelectorAll('.fl-builder-content-178 > .fl-row')].map(r=>r.dataset.node)"))
asyncio.run(main())
