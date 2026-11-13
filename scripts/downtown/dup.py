import asyncio, sys
from playwright.async_api import async_playwright
S="https://downtownoffice.agent.wallacetn.com"
ROWS=sys.argv[1].split(',')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp("http://localhost:29229"); pg=await b.contexts[0].new_page()
        pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
        for r in ROWS:
            await pg.goto(f"{S}/wp-admin/admin.php?page=mx-site-pages",wait_until="domcontentloaded",timeout=90000); await pg.wait_for_timeout(4000)
            await pg.evaluate("()=>document.querySelectorAll('iframe#launcher, iframe[title*=essag]').forEach(f=>f.remove())")
            n0=await pg.evaluate("()=>document.querySelectorAll('div.mxMoveableRow').length")
            await pg.click(f"#{r} a.m4c-duplicate-post", force=True)
            await pg.wait_for_timeout(12000)
            print(r, "url", pg.url, "rows before", n0, "now", await pg.evaluate("()=>document.querySelectorAll('div.mxMoveableRow').length"))
        await pg.goto(f"{S}/wp-admin/edit.php?post_type=page&post_status=all&s=Copy",wait_until="domcontentloaded",timeout=90000)
        print(await pg.evaluate("()=>[...document.querySelectorAll('#the-list tr')].map(r=>r.id+' | '+((r.querySelector('.row-title')||{}).innerText||'')+' | '+((r.querySelector('.post-state')||{}).innerText||''))"))
asyncio.run(main())
