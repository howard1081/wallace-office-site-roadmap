# usage: meta.py <post> "<title>" "<seo title>" "<desc>" "<kw>" [slug]
import asyncio, sys
from dtlib import *
async def main():
    post,title,st,desc,kw=sys.argv[1:6]; slug=sys.argv[6] if len(sys.argv)>6 else ''
    async with async_playwright() as p:
        pg=await browser(p)
        await pg.goto(f"{S}/wp-admin/post.php?post={post}&action=edit",wait_until="domcontentloaded",timeout=120000); await pg.wait_for_timeout(5000)
        r=await pg.evaluate("""([t,st,d,k,slug])=>{const set=(sel,v)=>{const e=document.querySelector(sel); if(!e) return sel+':missing'; e.value=v; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true})); return sel+':ok';};
          document.querySelectorAll('iframe#launcher, iframe[title*=essag]').forEach(f=>f.remove());
          const out=[];
          if(t) out.push(set('#title',t));
          if(slug){ out.push(set('#post_name',slug)); const n=document.querySelector('#new-post-slug'); if(n) n.value=slug; }
          out.push(set('#yoast_wpseo_title',st)); out.push(set('#yoast_wpseo_metadesc',d)); if(k) out.push(set('#yoast_wpseo_focuskw',k)); return out;}""",[title,st,desc,kw,slug])
        print(r)
        async with pg.expect_navigation(timeout=120000):
            await pg.evaluate("()=>document.querySelector('#publish').click()")
        print('saved',post, await pg.evaluate("()=>({title:(document.querySelector('#title')||{}).value, slug:(document.querySelector('#post_name')||{}).value, st:(document.querySelector('#yoast_wpseo_title')||{}).value})"))
asyncio.run(main())
