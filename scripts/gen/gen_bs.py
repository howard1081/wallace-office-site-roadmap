import json, sys, urllib.parse as up
R='/home/ubuntu/repos/wallace-office-site-roadmap/'
IMG='https://brokerage.agent.wallacetn.com/files/2026/01/'
def q(p): return '/search#location_search_field='+up.quote(p+', TN')+'&status=active'
def tel(p): return 'tel:+1'+''.join(c for c in p if c.isdigit())
def parts(t,start):
    s=open(R+'templates/'+t).read(); return s[:s.index(start)], s[s.index('<script>', s.index('<!-- FAQ -->')):]
def faq(items): return ''.join(f'   <div class="tl-faq-i"><div class="tl-q" role="button" tabindex="0">{a}</div><div class="tl-a"><p>{b}</p></div></div>\n' for a,b in items)
def stats(items): return ''.join(f'   <div class="tl-stat"><i class="fa fa-{i}"></i><h4>{h}</h4><p>{p}</p></div>\n' for i,h,p in items)
def svc(items): return ''.join(f'   <div class="tl-svc-c"><i class="fa fa-{i}"></i><h3>{a} <span>{b}</span></h3><p>{p}</p></div>\n' for i,a,b,p in items)
def intro(sec,o,h2a,ps,btns,img,alt):
    P=''.join(f'    <p style="color:#333">{p}</p>\n' for p in ps)
    return f'''<section class="tl-sec tl-light" id="{sec}" style="padding-top:70px">
 <div class="tl-in">
  <div class="tl-why tl-flip" style="padding-top:0">
   <div class="tl-why-txt">
    <p class="tl-eyebrow" style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#93a2b5;margin:0 0 10px">{o['name']} &middot; {o['city']}, TN</p>
    <h2 class="tl-h2" style="text-align:left;margin-bottom:20px">{h2a} <span>{o['town']} &amp; {o['county']}</span></h2>
{P}    <p style="margin-top:26px">{btns}</p>
   </div>
   <div class="tl-why-img tl-r">
    <img src="{IMG}{img}" alt="{alt}" loading="lazy">
   </div>
  </div>
 </div>
</section>
'''
def buyers(o,d):
    head,tail=parts('buyers.html','<!-- BUYER INTRO -->'); C=o['county']; T=o['town']; P=o['phone']
    tiles=''.join(f'   <a class="tl-tile" href="{q(p)}"><img src="{IMG}{im}" alt="{t} TN homes for sale" loading="lazy"><div class="tl-tile-d"><p>{ds}</p></div><div class="tl-tile-t">{t} <span>{sp}</span></div></a>\n' for p,im,ds,t,sp in d['tiles'])
    body='<!-- BUYER INTRO -->\n'+intro('tl-buy-intro',o,'Buying A Home In',d['intro'],f'<a class="tl-btn" href="/directory"><i class="fa fa-user"></i>Talk To A {o["short"]} Agent</a> <a class="tl-btn tl-soft" href="{q(C)}" style="margin-left:8px"><i class="fa fa-search"></i>Search {C} Homes</a>',d['img'],f'Buying a home in {T}, Tennessee')
    body+=f'''
<!-- WHY BUY HERE -->
<section class="tl-sec tl-dark" id="tl-buy-why">
 <div class="tl-in">
  <h2 class="tl-h2">Why Buyers Choose <span>{C}</span></h2>
  <p class="tl-lead">{d['why_lead']}</p>
  <div class="tl-market-grid">
{stats(d['why'])}  </div>
 </div>
</section>

<!-- AREAS -->
<section class="tl-sec tl-sage" id="tl-buy-areas">
 <div class="tl-in">
  <h2 class="tl-h2">Where We Help You <span>Buy</span></h2>
  <p class="tl-lead">Browse homes for sale in the {T} and {C} communities we serve every day. Hover a tile for a quick feel of each area, then click to see current listings.</p>
  <div class="tl-tiles">
{tiles}  </div>
 </div>
</section>

<!-- PROCESS -->
<section class="tl-sec tl-light" id="tl-buy-steps">
 <div class="tl-in">
  <h2 class="tl-h2">How We Help You <span>Buy</span></h2>
  <p class="tl-lead">From the first conversation to the keys in your hand, here is what working with a {o['name']} buyer's agent looks like.</p>
  <div class="tl-svc">
{svc([('comments-o','1. Plan','&amp; Pre-Approve','We talk through your <b>timeline</b>, <b>budget</b> and must-haves, then connect you with a local lender so you shop with a pre-approval in hand.'),
('search','2. Search','&amp; Tour',f'You get a custom {C} search with instant alerts, plus <b>video tours</b> if you are buying from out of town. {d["tour"]}'),
('handshake-o','3. Offer','&amp; Negotiate',f'We price your offer from <b>recent {C} comps</b>, structure terms that win without overpaying, and negotiate repairs and credits on your behalf.'),
('check-square-o','4. Inspect','&amp; Verify',d['inspect']),
('key','5. Close','&amp; Move In','We keep lender, title company and sellers on schedule, do the final walk-through with you and hand you the keys at a local closing table.'),
('home','After','Closing',f'Need a contractor, HVAC tech or lawn service? Our {T} vendor list is yours, and we stay your real estate resource for as long as you own the home.')])}  </div>
  <div class="tl-center" style="margin-top:36px">
   <a class="tl-btn" href="/contact"><i class="fa fa-envelope-o"></i>Start My Home Search</a>
   <a class="tl-btn tl-soft" href="/relocation"><i class="fa fa-plane"></i>Relocating To {T}?</a>
  </div>
 </div>
</section>

<!-- FAQ -->
<section class="tl-sec tl-dark" id="tl-buy-faq" style="padding-top:50px;padding-bottom:60px">
 <div class="tl-in">
  <h2 class="tl-h2">{T} Home Buyer <span>FAQ</span></h2>
  <div class="tl-faq">
{faq(d['faq'])}  </div>
  <p class="tl-faq-foot">Have more questions? <a href="/contact">Send us a message</a> or call <a href="{tel(P)}">{P}</a>. Our office is at {o['street']} in {o['city']}.</p>
 </div>
</section>

'''
    return head+body+tail
def sellers(o,d):
    head,tail=parts('sellers.html','<!-- SELLER INTRO -->'); C=o['county']; T=o['town']; P=o['phone']
    body='<!-- SELLER INTRO -->\n'+intro('tl-sell-intro',o,'Selling Your Home In',d['intro'],'<a class="tl-btn" href="/contact"><i class="fa fa-home"></i>Get My Home Value</a> <a class="tl-btn tl-soft" href="/directory" style="margin-left:8px"><i class="fa fa-user"></i>Find A Listing Agent</a>','Walace-Real-Estate-Listing-a-Home02.jpg',f'Selling a home in {T}, Tennessee')
    body+=f'''
<!-- WHAT BUYERS WANT -->
<section class="tl-sec tl-dark" id="tl-sell-demand">
 <div class="tl-in">
  <h2 class="tl-h2">Who Is Buying In <span>{C}</span></h2>
  <p class="tl-lead">Knowing your buyer is the first step to pricing and marketing your home. These are the buyers we talk to every day at the {o['short']} office.</p>
  <div class="tl-market-grid">
{stats(d['who'])}  </div>
  <div class="tl-center">
   <a class="tl-btn" href="/contact"><i class="fa fa-file-text-o"></i>Request a {C} Market Report</a>
   <a class="tl-btn tl-ghost" href="{tel(P)}"><i class="fa fa-phone"></i>Call {P}</a>
  </div>
 </div>
</section>

<!-- PROCESS -->
<section class="tl-sec tl-sage" id="tl-sell-steps">
 <div class="tl-in">
  <h2 class="tl-h2">How We Sell <span>Your Home</span></h2>
  <p class="tl-lead">From the first walk-through to closing day, here is how a {o['name']} listing agent gets you top dollar in {T} and {C}.</p>
  <div class="tl-svc">
{svc([('line-chart','1. Price','It Right',f'We price from <b>recent {C} sales</b>, active competition and what {d["features"]} are really bringing, not a website estimate.'),
('paint-brush','2. Prepare','&amp; Stage','A pre-listing walk-through pinpoints the <b>high-return fixes</b>. We arrange staging advice, cleaners and vendors so your home shows its best from day one.'),
('camera','3. Photograph','&amp; Film',f'<b>Professional photography</b>, drone shots of {d["drone"]}, video and 3D tours, because most of your buyers will see your home online before they see it in person.'),
('bullhorn','4. Market','Everywhere','MLS, Zillow, Realtor.com, targeted social ads, email to our buyer database and the Wallace network of 12 offices and 500+ agents. Luxury homes get <b>Luxury Portfolio International</b> exposure.'),
('handshake-o','5. Negotiate','&amp; Manage','We vet every offer&#39;s <b>financing and terms</b>, negotiate price, repairs and timelines, and manage inspections, appraisal and title so nothing stalls.'),
('key','6. Close','&amp; Move On',f'We keep you informed to the closing table and help with your next move, whether it is across {C} or across the country through our relocation network.')])}  </div>
  <div class="tl-center" style="margin-top:36px">
   <a class="tl-btn" href="/contact"><i class="fa fa-calendar-o"></i>Schedule A Listing Consult</a>
   <a class="tl-btn tl-soft" href="/luxury"><i class="fa fa-diamond"></i>Luxury Home Marketing</a>
  </div>
 </div>
</section>

<!-- FAQ -->
<section class="tl-sec tl-dark" id="tl-sell-faq" style="padding-top:50px;padding-bottom:60px">
 <div class="tl-in">
  <h2 class="tl-h2">{T} Home Seller <span>FAQ</span></h2>
  <div class="tl-faq">
{faq(d['faq'])}  </div>
  <p class="tl-faq-foot">Ready to talk? <a href="/contact">Request an evaluation</a> or call <a href="{tel(P)}">{P}</a>. Our office is at {o['street']} in {o['city']}.</p>
 </div>
</section>

'''
    return head+body+tail
BAD=['Lenoir','Loudon','Tellico','Twin Lakes','328-1111','105 N','Fort Loudoun']
for slug in sys.argv[1:]:
    o=json.load(open(f'/home/ubuntu/office_build/{slug}.json')); d=json.load(open(f'/home/ubuntu/office_build/{slug}_bs.json'))
    for name,fn in (('buyers',buyers),('sellers',sellers)):
        h=fn(o,d[name]); out=R+f'offices/{slug}/{name}.html'; open(out,'w').write(h)
        print(out,len(h),'bad',[b for b in BAD if b in h and not (slug=='nelson' and b in d.get('allow',[]))])