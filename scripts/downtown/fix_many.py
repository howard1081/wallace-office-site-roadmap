import asyncio, json, sys
from dtlib import *
POSTS={62:'/knox',51:'/anderson',52:'/blount',63:'/loudon',67:'/roane',69:'/sevier',61:'/jefferson',58:'/grainger',71:'/union',166:'/reviews'}
async def main():
    async with async_playwright() as p:
        pg=await browser(p)
        for post,path in POSTS.items():
            ui=await open_bb(pg,f"{S}/?page_id={post}&preview=true&fl_builder&fl_builder_ui")
            assert await pg.evaluate("()=>FLBuilderConfig.postId")==post
            json.dump(await pg.evaluate("()=>FLBuilderSettingsConfig.nodes"),open(f"/home/ubuntu/downtown/backup/post{post}.json","w"))
            print('==',post,path); await fix_texts(pg,ui); await publish(pg); await verify(pg,path)
asyncio.run(main())
