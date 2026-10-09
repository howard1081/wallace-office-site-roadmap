import asyncio, sys
from playwright.async_api import async_playwright
POST=int(sys.argv[1])
TITLE="Lenoir City TN Real Estate | Wallace Twin Lakes Office"
DESC="Wallace Twin Lakes is Wallace Real Estate's Lenoir City, TN office. Search Lenoir City, Tellico Village & Loudon County homes for sale or call (865) 328-1111."
KW="Lenoir City TN real estate"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp("http://localhost:29229")
        pg = await b.contexts[0].new_page(); await pg.set_viewport_size({"width":1440,"height":1000})
        await pg.goto(f"https://twinlakesoffice.agent.wallacetn.com/wp-admin/post.php?post={POST}&action=edit", wait_until="domcontentloaded", timeout=90000); await pg.wait_for_timeout(6000)
        print(await pg.title())
        print("before:", await pg.evaluate("() => ['yoast_wpseo_focuskw','yoast_wpseo_title','yoast_wpseo_metadesc'].map(n => (document.querySelector('[name='+n+']')||{}).value)"))
        await pg.evaluate("""([t,d,k]) => { const set=(n,v)=>{const e=document.querySelector('[name='+n+']'); if(e){ e.value=v; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true})); } }; set('yoast_wpseo_title',t); set('yoast_wpseo_metadesc',d); set('yoast_wpseo_focuskw',k); }""", [TITLE,DESC,KW])
        await pg.wait_for_timeout(1000)
        async with pg.expect_navigation(timeout=90000):
            await pg.click('#publish')
        await pg.wait_for_timeout(4000)
        print("after:", await pg.evaluate("() => ['yoast_wpseo_focuskw','yoast_wpseo_title','yoast_wpseo_metadesc'].map(n => (document.querySelector('[name='+n+']')||{}).value)"))
        print("notice:", await pg.evaluate("() => (document.querySelector('#message')||{}).innerText"))
        await pg.close()
asyncio.run(main())
