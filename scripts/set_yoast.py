"""Set Yoast SEO title / meta description / focus keyword on a page.
usage: python3 set_yoast.py <post_id> "<title>" "<description>" "<focus kw>" [site_url]"""
import asyncio, sys
from playwright.async_api import async_playwright
POST=sys.argv[1]; TITLE=sys.argv[2]; DESC=sys.argv[3]; KW=sys.argv[4] if len(sys.argv)>4 else ''
SITE=sys.argv[5] if len(sys.argv)>5 else "https://twinlakesoffice.agent.wallacetn.com"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp("http://localhost:29229"); pg=await b.contexts[0].new_page()
        await pg.goto(f"{SITE}/wp-admin/post.php?post={POST}&action=edit",wait_until="domcontentloaded",timeout=90000); await pg.wait_for_timeout(5000)
        await pg.evaluate("""([t,d,k])=>{const set=(id,v)=>{const e=document.querySelector(id); if(!e) return; e.value=v; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true}));};
          set('#yoast_wpseo_title',t); set('#yoast_wpseo_metadesc',d); if(k) set('#yoast_wpseo_focuskw',k);
          document.querySelectorAll('iframe#launcher, iframe[title*=essag]').forEach(f=>f.remove());}""",[TITLE,DESC,KW])
        async with pg.expect_navigation(timeout=90000):
            await pg.evaluate("()=>document.querySelector('#publish').click()")
        print("saved", POST); await pg.close()
asyncio.run(main())
