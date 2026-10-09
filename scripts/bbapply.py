import asyncio, json, sys, re
from playwright.async_api import async_playwright
POST = int(sys.argv[1]); PUBLISH = len(sys.argv)>2 and sys.argv[2]=='publish'
URL = "https://twinlakesoffice.agent.wallacetn.com/?fl_builder&fl_builder_ui" if POST==4 else f"https://twinlakesoffice.agent.wallacetn.com/?page_id={POST}&preview=true&fl_builder&fl_builder_ui"
html = open('block.html').read()
DEL_ROWS = ['k1zcma9i7f6d','pdm9eytrqjai','kbmixq7h2tu9','ympoewjd2f85','f69hrpzev1wi','29owediz548f','xg72mkltr3y5']
async def ajax(pg, data):
    return await pg.evaluate("(d) => new Promise(res => { setTimeout(()=>res('TIMEOUT'), 20000); FLBuilder.ajax(d, r => res(String(r).slice(0,200))); })", data)
async def save(pg, node, patch):
    return await pg.evaluate("""([id,patch]) => new Promise(res => { setTimeout(()=>res('TIMEOUT'), 20000); const s = Object.assign({}, FLBuilderSettingsConfig.nodes[id], patch); FLBuilder.ajax({action:'save_settings', node_id:id, settings:s}, r => res(String(r).slice(0,80))); })""", [node, patch])
async def reload_ui(pg):
    await pg.reload(wait_until="domcontentloaded"); await pg.wait_for_timeout(15000)
    return [f for f in pg.frames if 'fl_builder_ui_iframe' in f.url][0]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp("http://localhost:29229")
        ctx = b.contexts[0]
        pg = await ctx.new_page(); await pg.set_viewport_size({"width":1440,"height":900})
        await pg.goto(URL, wait_until="domcontentloaded", timeout=90000); await pg.wait_for_timeout(12000)
        print(await pg.evaluate("() => ({postId: FLBuilderConfig.postId, status: FLBuilderConfig.postStatus})"))
        ui = [f for f in pg.frames if 'fl_builder_ui_iframe' in f.url][0]
        rows = await ui.evaluate("() => [...document.querySelectorAll('.fl-builder-content > .fl-row')].map(r=>r.dataset.node)")
        print("rows", rows)
        # module map
        mods = await ui.evaluate("() => [...document.querySelectorAll('.fl-builder-content .fl-module')].map(m=>({n:m.dataset.node,t:m.dataset.type,row:m.closest('.fl-builder-content > .fl-row').dataset.node, txt:(m.innerText||'').slice(0,60)}))")
        # 1. delete rows
        for r in DEL_ROWS:
            if r in rows: print("del row", r, await ajax(pg, {"action":"delete_node","node_id":r}))
        ui = await reload_ui(pg)
        live = set(await ui.evaluate("() => [...document.querySelectorAll('.fl-builder-content [data-node]')].map(e=>e.dataset.node)"))
        # 2. market row: delete heading + rich text modules, set html module
        for m in mods:
            if m['n'] not in live: continue
            if m['row']=='iwo6h2u8lrn0' and m['t']!='html':
                print("del mod", m['n'], m['t'], await ajax(pg, {"action":"delete_node","node_id":m['n']}))
        r = await save(pg, '2rqte7ysud41', {"html": html, "margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"})
        print("html set", r)
        r = await save(pg, 'iwo6h2u8lrn0', {"bg_type":"none","bg_color":"","padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","width":"full","content_width":"full"})
        print("row set", r)
        # column padding of html module's column
        col = await pg.evaluate("() => FLBuilderSettingsConfig.nodes['tx3lp5ae6g7c'] ? ['tx3lp5ae6g7c', FLBuilderSettingsConfig.nodes['tx3lp5ae6g7c'].padding_top, FLBuilderSettingsConfig.nodes['tx3lp5ae6g7c'].padding_left] : null")
        print("col", col)
        if col:
            r = await save(pg, 'tx3lp5ae6g7c', {"padding_top":"0","padding_bottom":"0","padding_left":"0","padding_right":"0","margin_top":"0","margin_bottom":"0","margin_left":"0","margin_right":"0"})
            print("col set", r)
        # 3. rich-text link fixes in kept rows
        fixes = await pg.evaluate("""() => { const n=FLBuilderSettingsConfig.nodes; const out=[]; for (const [id,s] of Object.entries(n)) { if (s.text && /nelson|East Tennessee/i.test(s.text)) out.push({id, text:s.text}); } return out; }""")
        for f in fixes:
            if f['id'] not in live: continue
            t = f['text']
            t2 = re.sub(r'https://nelson-realtors\.com/contact[^"]*', '/contact', t)
            t2 = re.sub(r'https://nelson-realtors\.com/directory[^"]*', '/directory', t2)
            t2 = re.sub(r'https://nelson-realtors\.com/search[^"]*', '/search#location_search_field=Loudon%20County%2C%20TN&amp;status=active', t2)
            t2 = re.sub(r'https://nelsonoffice\.agent\.wallacetn\.com/[^"]*', '/contact', t2)
            t2 = t2.replace('Lenoir City and East Tennessee', 'Lenoir City and Loudon County').replace('Lenoir City&nbsp;and East Tennessee', 'Lenoir City and Loudon County').replace('Lenoir City\xa0and East Tennessee', 'Lenoir City and Loudon County')
            t2 = t2.replace('Knoxville and East Tennessee real estate', 'Lenoir City, Loudon County and East Tennessee real estate').replace('Local reporting on Knoxville and East Tennessee', 'Local reporting on Lenoir City, Loudon County and East Tennessee')
            if t2 != t:
                r = await save(pg, f['id'], {"text": t2})
                print("fixed text", f['id'], r)
        # journal heading
        heads = await pg.evaluate("""() => { const n=FLBuilderSettingsConfig.nodes; const out=[]; for (const [id,s] of Object.entries(n)) { for (const k of Object.keys(s)) { if (typeof s[k]==='string' && /Knoxville/i.test(s[k]) && k!=='text') out.push({id,k,v:s[k]}); } } return out; }""")
        print("heads", heads)
        for h in heads:
            if h['id'] not in live or h['id']=='2rqte7ysud41': continue
            v2 = h['v'].replace('Knoxville &amp; East Tennessee','Lenoir City &amp; Loudon County').replace('Knoxville & East Tennessee','Lenoir City & Loudon County').replace('KNOXVILLE & EAST TENNESSEE','LENOIR CITY & LOUDON COUNTY')
            r = await save(pg, h['id'], {h['k']: v2})
            print("head fixed", h['id'], r)
        # render
        await ajax(pg, {"action":"render_layout"}); await pg.wait_for_timeout(3000)
        if PUBLISH:
            r = await pg.evaluate("() => new Promise(res => FLBuilder.ajax({action:'save_layout', publish: true}, r => res(String(r).slice(0,200))))")
            print("publish", r)
        ui = await reload_ui(pg)
        print("rows after", await ui.evaluate("() => [...document.querySelectorAll('.fl-builder-content > .fl-row')].map(r=>r.dataset.node)"))
        print("tlh present:", await ui.evaluate("() => !!document.getElementById('tlh')"), "nelson refs:", await ui.evaluate("() => document.querySelectorAll('.fl-builder-content a[href*=nelson]').length"))
        await pg.screenshot(path=f"/tmp/bb_{POST}.png", full_page=False)
        print("done; keep tab open")
asyncio.run(main())
