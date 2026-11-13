import json, sys, os, urllib.parse as up
T='/home/ubuntu/repos/wallace-office-site-roadmap/templates/office.html'
src=open(T).read(); head=src[:src.index('<section class="to-hero">')]
def q(p): return '/search#location_search_field='+up.quote(p+', TN')+'&status=active'
def tel(p): return 'tel:+1'+''.join(c for c in p if c.isdigit())
IMG='https://brokerage.agent.wallacetn.com/files/2026/01/'
def build(o, f):
    P=o['phone']; addr=f"{o['street']}, {o['city']}, TN {o['zip']}"; aq=up.quote_plus(addr)
    stories=''
    for i,s in enumerate(f['stories']):
        btn='<a class="tl-btn" href="/relocation"><i class="fa fa-map-o"></i> Relocating To '+o['town']+'?</a>' if i==2 else ''
        img=f'<div class="tl-why-img{" tl-r" if i%2 else ""} tl-noframe"><img src="{IMG}{s[3]}" alt="{s[4]}"></div>'
        txt=f'<div class="tl-why-txt"><h3 class="tl-h3"><span>{s[0]}</span> {s[1]}</h3><p>{s[2]}</p>{btn}</div>'
        stories+=f'  <div class="tl-why{" tl-flip" if i%2 else ""}">\n   '+(txt+'\n   '+img if i%2 else img+'\n   '+txt)+'\n  </div>\n'
    team=''.join(f'   <div class="to-agent{" to-mgr" if a.get("mgr") else ""}"><h3>{a["n"]}</h3><p class="to-role">{a["r"]}</p><p><i class="fa fa-phone"></i><a href="{tel(a["p"])}">{a["p"]}</a></p><p><i class="fa fa-building-o"></i>{o["name"]}, {o["city"]}</p><a class="to-prof" href="/directory/agents/{a["s"]}">View Profile</a></div>\n' for a in f['agents'])
    areas=''.join(f'   <a href="{q(c)}">{c}</a>\n' for c in o['communities'])+f'   <a href="{q(o["county"])}&ptype=5">{o["county"]} Land</a>\n'
    email=f'   <div><i class="fa fa-envelope-o"></i><b>Email</b><p><a href="mailto:{f["email"]}">{f["email"]}</a></p></div>\n' if f.get('email') else ''
    brk=f'   <div><i class="fa fa-user"></i><b>{o["broker_title"]}</b><p>{o["broker"]}<br><a href="{tel(f["broker_phone"])}">{f["broker_phone"]}</a></p></div>\n' if o.get('broker') else ''
    body=f'''<section class="to-hero">
 <div class="to-hero-in">
  <img src="{IMG}Wallace-Real-Estate-TN-Logo.png" alt="Wallace Real Estate {o['short']} office logo">
  <div>
   <p class="to-kicker">About Our Office</p>
   <h1 class="to-h1">{o['name']} <span>{o['city']}, Tennessee</span></h1>
   <p>{f['intro']}</p>
   <div class="to-btns">
    <a class="tl-btn" href="{tel(P)}"><i class="fa fa-phone"></i> {P}</a>
    <a class="tl-btn tl-ghost" href="https://www.google.com/maps/dir/?api=1&destination={aq}" target="_blank" rel="noopener"><i class="fa fa-location-arrow"></i> Get Directions</a>
    <a class="tl-btn tl-ghost" href="#tl-team"><i class="fa fa-users"></i> Meet The Team</a>
   </div>
  </div>
 </div>
</section>

<section class="tl-sec tl-light" id="tl-office">
 <div class="tl-in">
  <h2 class="tl-h2">Visit Us <span>In {o['city']}</span></h2>
  <p class="tl-lead">{f['visit']}</p>
  <div class="to-fact">
   <div><i class="fa fa-map-marker"></i><b>Address</b><p>{o['street']}<br>{o['city']}, TN {o['zip']}</p></div>
   <div><i class="fa fa-phone"></i><b>Phone</b><p><a href="{tel(P)}">{P}</a></p></div>
{email}{brk}  </div>
  <div class="tl-office-map" style="margin-top:30px">
   <iframe title="Map to {o['name']}, {addr}" src="https://maps.google.com/maps?q={aq}&z=15&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" style="width:100%;height:380px;border:0;display:block"></iframe>
  </div>
 </div>
</section>

<section class="tl-sec tl-dark to-story" id="tl-story">
 <div class="tl-wide">
  <h2 class="tl-h2">Why We Call <span>{o['town']} Home</span></h2>
  <p class="tl-lead" style="color:#cfd8e1">A few words from our office about the town we live and work in.</p>
{stories} </div>
</section>

<section class="tl-sec tl-light" id="tl-team">
 <div class="tl-in">
  <h2 class="tl-h2">Meet The <span>{o['short']} Team</span></h2>
  <p class="tl-lead">{f['team_lead']}</p>
  <div class="to-team">
{team}  </div>
  <p style="text-align:center;margin:30px 0 0"><a class="tl-btn" href="/directory"><i class="fa fa-users"></i> Full Office Directory</a></p>
 </div>
</section>

<section class="tl-sec tl-sage" id="tl-areas">
 <div class="tl-in">
  <h2 class="tl-h2">Areas <span>We Serve</span></h2>
  <p class="tl-lead">{o['town']} and {o['county']} are our home turf. Pick a community to see current homes for sale.</p>
  <div class="to-areas">
{areas}  </div>
 </div>
</section>

<section class="to-cta">
 <h2 class="tl-h2">Let's Talk About <span>Your Move</span></h2>
 <p>Buying, selling or just curious what your {o['county']} home is worth? Call the office, send us a message, or stop by {o['street']} in {o['city']}.</p>
 <div class="to-btns" style="text-align:center">
  <a class="tl-btn" href="{tel(P)}"><i class="fa fa-phone"></i> Call {P}</a>
  <a class="tl-btn tl-ghost" href="/contact"><i class="fa fa-envelope-o"></i> Send A Message</a>
  <a class="tl-btn tl-ghost" href="{q(o['town'])}"><i class="fa fa-search"></i> Search {o['town']} Homes</a>
 </div>
</section>
</div>
'''
    return head+body
for slug in sys.argv[1:]:
    o=json.load(open(f'/home/ubuntu/office_build/{slug}.json')); f=json.load(open(f'/home/ubuntu/office_build/{slug}_office.json'))
    out=f'/home/ubuntu/repos/wallace-office-site-roadmap/offices/{slug}/office.html'; h=build(o,f); open(out,'w').write(h); print(out,len(h))