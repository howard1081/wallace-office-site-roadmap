"""Reorder + hide children of a top-menu dropdown in Moxi Site Pages WITHOUT deleting pages.
usage: python3 nav_hide.py "<Parent label, e.g. Counties>" "Loudon,Anderson,Knox,Blount,Monroe,Roane"
Keeps the listed children visible in that order, hides every other child (pages stay published; direct URLs still work)."""
import asyncio, sys, json
from playwright.async_api import async_playwright
PARENT=sys.argv[1]; KEEP=[k.strip() for k in sys.argv[2].split(',')]
SITE=sys.argv[3] if len(sys.argv)>3 else "https://twinlakesoffice.agent.wallacetn.com"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp("http://localhost:29229"); pg=await b.contexts[0].new_page()
        await pg.goto(f"{SITE}/wp-admin/admin.php?page=mx-site-pages",wait_until="domcontentloaded",timeout=90000); await pg.wait_for_timeout(5000)
        r=await pg.evaluate("""([parent,keep])=>{
          document.querySelectorAll('iframe#launcher, iframe[title*=essag]').forEach(f=>f.remove());   // Zendesk launcher blocks clicks
          const divs=[...document.querySelectorAll('div.mxMoveableRow')];
          const c=divs.find(d=>d.innerText.trim().toLowerCase().startsWith(parent.toLowerCase()));
          if(!c) return 'parent not found';
          const ol=c.parentElement.querySelector(':scope > ol'); const kids=[...ol.querySelectorAll(':scope > li')];
          const label=li=>li.querySelector(':scope > div.mxMoveableRow').innerText.trim().split('\\n')[0].replace(/\\s*\\(Hidden\\)/i,'').trim();
          const pick=n=>kids.find(li=>label(li).toLowerCase()===n.toLowerCase());
          const keepLis=keep.map(pick).filter(Boolean); const rest=kids.filter(li=>!keepLis.includes(li));
          keepLis.forEach(li=>ol.appendChild(li)); rest.forEach(li=>ol.appendChild(li));
          rest.forEach(li=>jQuery(li.querySelector(':scope > div.mxMoveableRow')).setShowHideValues('Hide'));
          keepLis.forEach(li=>jQuery(li.querySelector(':scope > div.mxMoveableRow')).setShowHideValues('Show'));
          return {kept:keepLis.map(label),hidden:rest.map(label),missing:keep.filter(n=>!pick(n))};}""",[PARENT,KEEP])
        print(json.dumps(r,indent=1))
        if isinstance(r,dict):
            async with pg.expect_navigation(timeout=90000):
                await pg.evaluate("()=>jQuery('input#publish').click()")
            print("saved")
        await pg.close()
asyncio.run(main())
