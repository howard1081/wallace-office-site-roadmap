import json, os, urllib.parse as up
T = '/home/ubuntu/repos/wallace-office-site-roadmap/templates/block.html'
src = open(T).read()
head = src[:src.index('<!-- EXPLORE -->')]
tail = src[src.index('<script>', src.index('<!-- FAQ -->')):]
IMG = 'https://brokerage.agent.wallacetn.com/files/2026/01/'
def q(place): return '/search#location_search_field=' + up.quote(place + ', TN') + '&status=active'
def tel(p): return 'tel:+1' + ''.join(c for c in p if c.isdigit())

def build(o):
    T_, C = o['town'], o['county']
    tiles = ''.join(f'   <a class="tl-tile" href="{q(t[0])}"><img src="{IMG}{t[2]}" alt="{t[0]} TN homes for sale" loading="lazy"><div class="tl-tile-d"><p>{t[3]}</p></div><div class="tl-tile-t">{t[1]}</div></a>\n' for t in o['tiles'])
    life_img = ['Lakes-and-Waterfront.jpg', 'Mountain-Homes-02.jpg', 'Suburban-and-Downtown.jpg', 'Country-and-Land-02.jpg']
    life_icon = ['fa-tint', 'fa-tree', 'fa-home', 'fa-tree']
    life = ''.join(f'   <div class="tl-life-c"><img src="{IMG}{life_img[i]}" alt="{l[3]}"><h3 class="tl-h3"><b>{l[0]}</b> {l[1]}</h3><p>{l[2]}</p><a class="tl-btn tl-full" href="{l[4]}"><i class="fa {life_icon[i]}"></i>{l[5]}</a></div>\n' for i, l in enumerate(o['life']))
    cq = q(C)
    svc = [
      ('fa-plane','Relocation','Services', f"Moving to {o['region']} from out of state? We help with <b>area shortlists</b>, video tours, timelines and trusted local vendors so your move to {T_} goes smoothly.", '/relocation', 'Get Relocation Help'),
      ('fa-diamond','Luxury','Services', f"{o['luxury']} need <b>elevated presentation</b> and <b>targeted marketing</b>. As a Luxury Portfolio International affiliate we put {C}'s finest homes in front of qualified buyers.", '/luxury', 'Get Luxury Strategy'),
      ('fa-building-o','Property','Management', "Own a rental or second home you're not using year-round? Wallace's property management team handles <b>tenant placement</b>, <b>maintenance</b> and <b>reporting</b> so your investment stays steady.", '/contact', 'Get Management Help'),
      ('fa-briefcase','Commercial','Services', f"{o['commercial']}, Wallace Commercial brings local knowledge and underwriting support to every deal.", '/contact', 'Get Commercial Guidance'),
      ('fa-home','Residential','Services', "We help buyers win with <b>smart search and negotiation</b>, and help sellers get top dollar with prep strategy, strong marketing and steady follow-through from list to close.", '/contact', 'Get Buying &amp; Selling Help'),
      ('fa-wrench','New','Construction', f"New homes are going up across {T_} and {C}. We help you compare <b>builders</b>, <b>lots</b>, <b>timelines</b> and <b>upgrades</b>, and we read the contract and warranty with you.", cq + '&new_const=1', 'Get New Build Help')]
    svch = ''.join(f'   <div class="tl-svc-c"><i class="fa {s[0]}"></i><h3>{s[1]} <span>{s[2]}</span></h3><p>{s[3]}</p><a class="tl-btn tl-full" href="{s[4]}"><i class="fa {s[0]}"></i>{s[5]}</a></div>\n' for s in svc)
    why_img = [o['why_imgs'][0], o['why_imgs'][1], 'Walace-Real-Estate-Relocation.jpg', 'Wallace-Real-Estate-Google-Reviews.png']
    whys = ''
    for i, w in enumerate(o['why']):
        img = f'<img src="{IMG}{why_img[i]}" alt="{w[4]}">'
        if i == 3: img = f'<div class="tl-frame"><div class="tl-ph">{img}</div></div>'
        txt = f'<div class="tl-why-txt"><h3 class="tl-h3"><span>{w[0]}</span> {w[1]}</h3><p>{w[2]}</p><a class="tl-btn" href="{w[3][0]}"><i class="fa {w[3][2]}"></i>{w[3][1]}</a></div>'
        if i % 2 == 0: whys += f'  <div class="tl-why">\n   <div class="tl-why-img tl-noframe">{img}</div>\n   {txt}\n  </div>\n\n'
        else: whys += f'  <div class="tl-why tl-flip">\n   {txt}\n   <div class="tl-why-img tl-r tl-noframe">{img}</div>\n  </div>\n\n'
    partners = ' </div>\n</section>\n\n'
    addr_q = up.quote_plus(f"{o['street']}, {o['city']}, TN {o['zip']}")
    email = f'    <p class="tl-nap"><i class="fa fa-envelope-o"></i><a href="mailto:{o["email"]}">{o["email"]}</a></p>\n' if o.get('email') else ''
    plan = [
      ('Sell','With Confidence','Walace-Real-Estate-Listing-a-Home02.jpg', f'Selling a home in {T_}', f"Get a pricing plan built on <b>real {C} comps</b>, <b>local demand</b> and <b>your timeline</b>. We'll map prep priorities, launch strategy and negotiation levers, then market your home with modern media and consistent follow-up.", '/contact', 'Get My Home Value'),
      ('Relocation','Concierge','Walace-Real-Estate-Relocation.jpg', f'Relocating to {C}', f"Moving to {o['region']}? Share your <b>timeline</b>, <b>commute</b> and <b>must-haves</b>. We'll narrow areas quickly, connect trusted lenders and vendors, and keep details organized so your move feels simple instead of stressful.", '/relocation', 'Plan My Move'),
      ('Investment','Opportunities','Wallace-Real-Estate-Investment-Opportunities.jpg', f'Investment property in {T_}', o['invest'] + " Compare deals with clarity using <b>cash flow</b>, <b>demand</b>, <b>resale upside</b> and <b>risk</b>, and move fast when the numbers work.", cq, 'Browse Investment Homes')]
    planh = ''.join(f'   <div class="tl-plan-c"><h3>{p[0]} <span>{p[1]}</span></h3><img src="{IMG}{p[2]}" alt="{p[3]}"><p>{p[4]}</p><a class="tl-btn tl-full" href="{p[5]}">{p[6]}</a></div>\n' for p in plan)
    comm = '<span>&#10022;</span>\n'.join(f'   <a href="{q(c)}">{c}</a>' for c in o['communities'] + [C])
    faq = ''.join(f'   <div class="tl-faq-i"><div class="tl-q" role="button" tabindex="0">{f[0]}</div><div class="tl-a"><p>{f[1]}</p></div></div>\n' for f in o['faq'])
    P = o['phone']
    body = f'''<!-- EXPLORE -->
<section class="tl-sec tl-sage" id="tl-explore">
 <div class="tl-in">
  <h2 class="tl-h2">Explore {T_} <span>&amp; {C}</span></h2>
  <p class="tl-lead">{o['explore']}</p>
  <div class="tl-tiles">
{tiles}  </div>
 </div>
</section>

<!-- LIFESTYLE -->
<section class="tl-sec tl-light" id="tl-lifestyle">
 <div class="tl-in">
  <h2 class="tl-h2">Search Homes <span>By Lifestyle</span></h2>
  <p class="tl-lead"><em>{o['life_lead']}</em></p>
  <div class="tl-life">
{life}  </div>
 </div>
</section>

<!-- MARKET -->
<section class="tl-sec tl-dark" id="tl-market">
 <div class="tl-in">
  <h2 class="tl-h2">{C} <span>Market Snapshot</span></h2>
  <p class="tl-lead">{o['market']}</p>
  <div class="tl-market-grid">
   <div class="tl-stat"><i class="fa fa-line-chart"></i><h4>Neighborhood Pricing</h4><p>Recent sales and active competition for the specific area or subdivision you're watching.</p></div>
   <div class="tl-stat"><i class="fa fa-tint"></i><h4>{o['trend'][0]}</h4><p>{o['trend'][1]}</p></div>
   <div class="tl-stat"><i class="fa fa-home"></i><h4>Your Home's Value</h4><p>A no-pressure estimate from an agent who works {T_} and {C} every day.</p></div>
  </div>
  <div class="tl-center">
   <a class="tl-btn" href="/contact"><i class="fa fa-file-text-o"></i>Request a {C} Market Report</a>
   <a class="tl-btn tl-ghost" href="{tel(P)}"><i class="fa fa-phone"></i>Call {P}</a>
  </div>
 </div>
</section>

<!-- SERVICES -->
<section class="tl-sec tl-light" id="tl-services">
 <div class="tl-in">
  <h2 class="tl-h2">Real Estate <span>Services</span></h2>
  <p class="tl-lead">{o['name']} supports <b>buyers</b>, <b>sellers</b>, <b>investors</b> and <b>relocating clients</b> across {T_} and {C}, backed by the full resources of Wallace Real Estate. Explore the services below to find the right help.</p>
  <div class="tl-svc">
{svch}  </div>
 </div>
</section>

<!-- WHY -->
<section class="tl-sec tl-dark" id="tl-why">
 <div class="tl-in">
  <h2 class="tl-h2">Why Wallace <span>{o['short']}</span></h2>
  <p class="tl-lead"><em>A local {T_} office backed by the data, marketing and reach of Wallace Real Estate, serving Tennessee since 1936.</em></p>

{whys}{partners}<!-- OFFICE -->
<section class="tl-sec tl-sage" id="tl-office">
 <div class="tl-in">
  <h2 class="tl-h2">Visit Our <span>{o['city']} Office</span></h2>
  <p class="tl-lead">{o['office_lead']}</p>
  <div class="tl-office">
   <div class="tl-office-card">
    <p class="tl-eyebrow">Wallace Real Estate</p>
    <h3><b>{o['short']}</b> Office</h3>
    <p class="tl-nap"><i class="fa fa-map-marker"></i>{o['street']}<br><span style="display:inline-block;width:26px"></span>{o['city']}, TN {o['zip']}</p>
    <p class="tl-nap"><i class="fa fa-phone"></i><a href="{tel(P)}">{P}</a></p>
{email}    <p>{o['broker_title']}: {o['broker']}</p>
    <a class="tl-btn" href="https://www.google.com/maps/search/?api=1&query={up.quote_plus(o['name'])}+{addr_q}" target="_blank" rel="noopener"><i class="fa fa-location-arrow"></i>Get Directions</a>
    <a class="tl-btn tl-soft" href="/directory" style="margin-left:8px"><i class="fa fa-users"></i>Meet Our Agents</a>
   </div>
   <div class="tl-office-map"><iframe title="Map to {o['name']}, {o['street']}, {o['city']} TN" src="https://maps.google.com/maps?q={addr_q}&z=15&output=embed" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
 </div>
</section>

<!-- PLAN -->
<section class="tl-sec tl-light" id="tl-plan">
 <div class="tl-wide">
  <h2 class="tl-h2">Plan <span>Your Next Move</span></h2>
  <p class="tl-lead">Talk with a {T_}-based Wallace agent to get neighborhood-specific comps, strategy and showing coordination.</p>
  <div class="tl-plan">
{planh}  </div>
 </div>
</section>

<!-- COMMUNITY -->
<section class="tl-sec tl-dark" id="tl-community">
 <div class="tl-wide">
  <h2 class="tl-h2">Search <span>By Community</span></h2>
  <p class="tl-lead">Not sure where to start? Browse the {T_} and {C} communities we serve, then filter listings by price, home type and lifestyle.</p>
  <p class="tl-comm">
{comm}
  </p>
  <div class="tl-center"><a class="tl-btn" href="{cq}"><i class="fa fa-search"></i>Search All {C} Homes</a></div>
 </div>
</section>

<!-- FAQ -->
<section class="tl-sec tl-dark" id="tl-faq" style="padding-top:40px;padding-bottom:50px;border-top:1px solid #3b4d66">
 <div class="tl-in">
  <h2 class="tl-h2">{T_} &amp; {C} <span>Real Estate FAQs</span></h2>
  <p class="tl-lead"><em>Quick answers to the questions we hear most about buying, selling and relocating to {T_} and the rest of {C}.</em></p>
  <div class="tl-faq">
{faq}  </div>
  <p class="tl-faq-foot">Have more questions? <a href="/contact">Get in touch</a> or call <a href="{tel(P)}">{P}</a> and tell us what you're looking for.</p>
 </div>
</section>

'''
    return head + body + tail

if __name__ == '__main__':
    import sys
    for f in sys.argv[1:]:
        o = json.load(open(f))
        out = f'/home/ubuntu/repos/wallace-office-site-roadmap/offices/{o["slug"]}/block.html'
        os.makedirs(os.path.dirname(out), exist_ok=True)
        h = build(o); open(out, 'w').write(h); print(out, len(h))