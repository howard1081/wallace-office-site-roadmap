import asyncio, json
from dtlib import *
HIDE=['Home Copy','Buyers Copy','Sellers Copy','Relocation Copy']
async def main():
    async with async_playwright() as p:
        pg=await browser(p)
        await pg.goto(f"{S}/wp-admin/admin.php?page=mx-site-pages",wait_until="domcontentloaded",timeout=120000); await pg.wait_for_timeout(5000)
        r=await pg.evaluate("""(hide)=>{document.querySelectorAll('iframe#launcher, iframe[title*=essag]').forEach(f=>f.remove());
          const label=d=>d.innerText.trim().split('\\n')[0].replace(/\\s*\\(Hidden\\)/i,'').trim();
          const divs=[...document.querySelectorAll('div.mxMoveableRow')]; const out={hidden:[],nested:null};
          divs.forEach(d=>{ if(hide.includes(label(d))){ jQuery(d).setShowHideValues('Hide'); out.hidden.push(d.id+' '+label(d)); }});
          const office=divs.find(d=>label(d)==='Our Office'); const about=divs.find(d=>label(d)==='About Us');
          if(office&&about){ const ol=about.parentElement.querySelector(':scope > ol'); ol.insertBefore(office.parentElement, ol.firstElementChild); jQuery(office).setShowHideValues('Show'); out.nested=office.id; }
          return out;}""",HIDE)
        print(json.dumps(r))
        async with pg.expect_navigation(timeout=120000):
            await pg.evaluate("()=>jQuery('input#publish').click()")
        await pg.wait_for_timeout(4000)
        nav=await pg.evaluate("""()=>[...document.querySelectorAll('div.mxMoveableRow')].map(d=>'  '.repeat($(d).parents('ol').length-1)+d.innerText.split('\\n')[0]).filter(x=>/Copy|Our Office|About Us|Our Team|Home/.test(x))""")
        print('\n'.join(nav))
asyncio.run(main())
