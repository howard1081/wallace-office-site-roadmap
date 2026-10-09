import asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp("http://localhost:29229")
        ctx = b.contexts[0]
        page = [pg for pg in ctx.pages if "twinlakesoffice" in pg.url][-1]
        await page.goto("https://twinlakesoffice.agent.wallacetn.com/wp-admin/edit.php?post_type=page&s=Home", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        rows = await page.evaluate("""() => [...document.querySelectorAll('#the-list tr')].map(tr => ({id: tr.id, title: (tr.querySelector('a.row-title')||{}).innerText, state:(tr.querySelector('.post-state')||{}).innerText||'', links:[...tr.querySelectorAll('.row-actions a')].map(a=>a.innerText+'='+a.href)}))""")
        for r in rows: print(r)
        dup = [l for r in rows if r['id']=='post-4' for l in r['links'] if l.startswith('Duplicate')]
        print("DUP:", dup)
        if dup:
            await page.goto(dup[0].split('=',1)[1], wait_until="domcontentloaded")
            await page.wait_for_timeout(4000)
            print("after dup:", page.url)
        await page.goto("https://twinlakesoffice.agent.wallacetn.com/wp-admin/edit.php?post_type=page&s=Home&post_status=all", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        rows = await page.evaluate("""() => [...document.querySelectorAll('#the-list tr')].map(tr => ({id: tr.id, title: (tr.querySelector('a.row-title')||{}).innerText, state:(tr.querySelector('.post-state')||{}).innerText||''}))""")
        for r in rows: print(r)
        # Yoast fields on page 4
        await page.goto("https://twinlakesoffice.agent.wallacetn.com/wp-admin/post.php?post=4&action=edit", wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)
        y = await page.evaluate("""() => { const o={}; for (const el of document.querySelectorAll('input[name^="yoast_wpseo"], textarea[name^="yoast_wpseo"], input#title, input[name=post_name]')) o[el.name||el.id]=el.value; return o; }""")
        print(json.dumps(y, indent=1))
        content = await page.evaluate("() => (document.querySelector('#content')||{}).value")
        print("CONTENT LEN", len(content or ''), (content or '')[:500])
asyncio.run(main())
