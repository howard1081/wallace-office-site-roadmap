import json, sys, urllib.parse as up
T='/home/ubuntu/repos/wallace-office-site-roadmap/templates/footer.html'
def q(p,extra=''): return '/search#location_search_field='+up.quote(p+', TN')+'&status=active'+extra
def tel(p): return 'tel:+1'+''.join(c for c in p if c.isdigit())
for slug in sys.argv[1:]:
    o=json.load(open(f'/home/ubuntu/office_build/{slug}.json')); f=json.load(open(f'/home/ubuntu/office_build/{slug}_office.json'))
    s=open(T).read(); P=o['phone']; c2=o['communities'][1]
    rep=[
     ('<h4>Wallace Twin Lakes</h4>',f"<h4>{o['name']}</h4>"),
     ("<p>Wallace Real Estate's Lenoir City office, serving buyers and sellers across Loudon County, Tellico Village and the Fort Loudoun &amp; Tellico Lake communities.</p>",f"<p>{f['footer_blurb']}</p>"),
     ('<a href="tel:+18653281111">(865) 328-1111</a><a href="mailto:TwinLakes@Wallacetn.com">TwinLakes@Wallacetn.com</a><p style="margin-top:8px">105 N. A Street<br>Lenoir City, TN 37771</p>',f'<a href="{tel(P)}">{P}</a><a href="mailto:{f["email"]}">{f["email"]}</a><p style="margin-top:8px">{o["street"]}<br>{o["city"]}, TN {o["zip"]}</p>'),
     ('<li><a href="/search#location_search_field=Lenoir%20City%2C%20TN&status=active">Lenoir City Homes For Sale</a></li>',f'<li><a href="{q(o["town"])}">{o["town"]} Homes For Sale</a></li>'),
     ('<li><a href="/search#location_search_field=Tellico%20Village%2C%20Loudon%2C%20TN&status=active&water=1">Tellico Village &amp; Lakefront</a></li>',f'<li><a href="{q(f["footer_second"][1])}">{f["footer_second"][0]}</a></li>'),
     ('Buying In Loudon County',f"Buying In {o['county']}"),
     ('Relocating To Lenoir City',f"Relocating To {o['town']}"),
     ('<li><a href="/b/b-blog-2?postID=7683">Blog</a></li>',f'<li><a href="{f["blog"]}">Blog</a></li>' if f.get('blog') else ''),
     ('Thinking about a move in Lenoir City or Loudon County? Get a free, no-obligation evaluation of your home from a Twin Lakes agent.',f"Thinking about a move in {o['town']} or {o['county']}? Get a free, no-obligation evaluation of your home from a {o['short']} agent."),
     ('Visit Our Lenoir City Office',f"Visit Our {o['city']} Office"),
     ('<a href="/our-office">Wallace Twin Lakes</a> &nbsp;·&nbsp; 105 N. A Street, Lenoir City, TN 37771 &nbsp;·&nbsp; <a href="tel:+18653281111">(865) 328-1111</a>',f'<a href="/our-office">{o["name"]}</a> &nbsp;·&nbsp; {o["street"]}, {o["city"]}, TN {o["zip"]} &nbsp;·&nbsp; <a href="{tel(P)}">{P}</a>'),
     ('Find A Twin Lakes Agent',f"Find A {o['short']} Agent"),
     ('<a class="tlf-btn tlf-ghost" href="/search#location_search_field=Loudon%20County%2C%20TN&status=active"><i class="fa fa-search"></i>&nbsp; Search Loudon County Homes</a>',f'<a class="tlf-btn tlf-ghost" href="{q(o["county"])}"><i class="fa fa-search"></i>&nbsp; Search {o["county"]} Homes</a>'),
    ]
    for a,b in rep:
        assert a in s, a[:60]; s=s.replace(a,b)
    bad=[w for w in ['Lenoir','Loudon','Tellico','Twin Lakes','328-1111','105 N'] if w in s]
    out=f'/home/ubuntu/repos/wallace-office-site-roadmap/offices/{slug}/footer.html'; open(out,'w').write(s); print(out,len(s),'bad',bad)