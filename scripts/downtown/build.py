import json, re, subprocess, urllib.parse as up, sys, importlib.util
R='/home/ubuntu/repos/wallace-office-site-roadmap/'; OUT=R+'offices/downtown/'; REF='/home/ubuntu/office_build/'
subprocess.run(['python3',REF+'gen_home.py',REF+'downtown.json'],check=True)
subprocess.run(['python3',REF+'gen_office.py','downtown'],check=True)
subprocess.run(['python3',REF+'gen_footer.py','downtown'],check=True)
subprocess.run(['python3',REF+'gen_bs.py','downtown'],check=True)
o=json.load(open(REF+'downtown.json')); P=o['phone']; TEL='tel:+18653211111'
IMG='https://brokerage.agent.wallacetn.com/files/2026/01/'
def q(p): return '/search#location_search_field='+up.quote(p+', TN')+'&status=active'
UC='/home/ubuntu/downtown/src/'
# relocation
s=open(UC+'relocation.html').read(); head=s[:s.index('<section class="tl-sec tl-light" id="tl-relo-intro"')]; tail=s[s.index('<script>',s.index('id="tl-relo-faq"')):]
def stat(i,h,p): return f'   <div class="tl-stat"><i class="fa fa-{i}"></i><h4>{h}</h4><p>{p}</p></div>\n'
def svc(i,a,b,p): return f'   <div class="tl-svc-c"><i class="fa fa-{i}"></i><h3>{a} <span>{b}</span></h3><p>{p}</p></div>\n'
def faq(a,b): return f'   <div class="tl-faq-i"><div class="tl-q" role="button" tabindex="0">{a}</div><div class="tl-a"><p>{b}</p></div></div>\n'
def tile(p,im,alt,d,t): return f'   <a class="tl-tile" href="{p}"><img src="{IMG}{im}" alt="{alt}" loading="lazy"><div class="tl-tile-d"><p>{d}</p></div><div class="tl-tile-t">{t}</div></a>\n'
relo=head+f'''<section class="tl-sec tl-light" id="tl-relo-intro" style="padding-top:70px">
 <div class="tl-in">
  <div class="tl-why tl-flip" style="padding-top:0">
   <div class="tl-why-txt">
    <p class="tl-eyebrow" style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#93a2b5;margin:0 0 10px">Wallace Downtown &middot; Knoxville, TN</p>
    <h2 class="tl-h2" style="text-align:left;margin-bottom:20px">Relocating To <span>Downtown Knoxville &amp; Knox County</span></h2>
    <p style="color:#333">Thinking about a move to Knoxville? You get a lively, walkable downtown, the University of Tennessee, <b>no state income tax on wages</b>, four real seasons and the Smoky Mountains about an hour away.</p>
    <p style="color:#333">Our Downtown office on Gay Street helps families, students' parents, professionals and retirees from across the country land in downtown Knoxville, the historic in-town neighborhoods and communities across Knox County. We handle the area shortlists, video tours, lender introductions and the tour weekend, so you can decide from a distance with confidence.</p>
    <p style="margin-top:26px"><a class="tl-btn" href="/contact"><i class="fa fa-plane"></i>Plan My Move</a> <a class="tl-btn tl-soft" href="https://s3.amazonaws.com/files.usmre.com/9302/260123_Referral%20Connections_PDF_01.pdf" target="_blank" rel="noopener" style="margin-left:8px"><i class="fa fa-file-pdf-o"></i>Relocation Guide</a></p>
   </div>
   <div class="tl-why-img tl-r"><img src="{IMG}Walace-Real-Estate-Relocation.jpg" alt="Relocating to downtown Knoxville, Tennessee" loading="lazy"></div>
  </div>
 </div>
</section>
<section class="tl-sec tl-dark" id="tl-relo-why">
 <div class="tl-in">
  <h2 class="tl-h2">Why People Move To <span>Knoxville</span></h2>
  <p class="tl-lead">The reasons we hear most from clients who moved here from other states.</p>
  <div class="tl-market-grid">
{stat('usd','Lower Cost Of Living','No state income tax on wages, and home prices below most large metro areas people move from.')}{stat('building-o','A Real Downtown','Market Square, the Old City, Gay Street theaters, the riverfront and festivals all year long.')}{stat('university','UT &amp; Jobs','The University of Tennessee, major hospitals, Oak Ridge National Laboratory and a growing job base.')}{stat('leaf','Outdoors Everywhere','The Urban Wilderness, Ijams Nature Center, area lakes and the Great Smoky Mountains.')}{stat('medkit','Healthcare','UT Medical Center, Fort Sanders Regional and other hospitals are in and around Knoxville.')}{stat('road','Easy To Get Around','I-40 and I-75 meet here, and McGhee Tyson Airport is about 20 to 25 minutes from downtown.')}  </div>
 </div>
</section>
<section class="tl-sec tl-sage" id="tl-relo-life">
 <div class="tl-in">
  <h2 class="tl-h2">Choose Your <span>Lifestyle</span></h2>
  <p class="tl-lead">Start with how you want to live, then we will narrow it to the right Knoxville and Knox County neighborhoods and send you current homes for sale.</p>
  <div class="tl-tiles">
{tile(q('Downtown, Knoxville'),'Suburban-and-Downtown.jpg','Downtown Knoxville lofts and condos','Walk to dinner, shows and games from a loft or condo in the urban core.','Lofts &amp; <span>Condos</span>')}{tile(q('Knoxville'),'Knox-County-Tennessee.jpg','Historic homes in Knoxville','Victorian and craftsman homes in Fourth &amp; Gill, Old North and other in-town neighborhoods.','Historic <span>In-Town</span>')}{tile(q('Knox County')+'&water=1','Lakes-and-Waterfront.jpg','River and lake homes in Knox County','Homes on or near the Tennessee River, Fort Loudoun Lake and Melton Hill Lake.','River <span>&amp; Lake</span>')}{tile(q('Knox County')+'&ptype=5','Country-and-Land-02.jpg','Land and acreage in Knox County','Acreage and room to spread out in east and north Knox County.','Country <span>&amp; Land</span>')}  </div>
 </div>
</section>
<section class="tl-sec tl-light" id="tl-relo-steps">
 <div class="tl-in">
  <h2 class="tl-h2">How A Long-Distance Move <span>Works With Us</span></h2>
  <div class="tl-svc">
{svc('comments-o','1. Discovery','Call','We learn your <b>timeline, budget, commute and must-haves</b>, and explain the differences between downtown, in-town and suburban living here.')}{svc('map-o','2. Area','Shortlist','You get a shortlist of Knoxville and Knox County areas with price ranges, taxes, school zones and drive times, plus a custom home search with alerts.')}{svc('video-camera','3. Video','Tours',"Can't fly in for every home? We walk it live on video, check the building or street, and tell you what the photos don't.")}{svc('calendar-o','4. Tour','Weekend','We plan a tour of downtown and the neighborhoods on your list so you can compare them in person and meet a local lender.')}{svc('handshake-o','5. Offer','&amp; Close','Remote-friendly offers, inspections and closing with e-signatures and a local title company.')}{svc('truck','6. Settle','In','Movers, utilities, contractors, doctors and the best local restaurants: our Knoxville vendor list and local know-how are yours after closing.')}  </div>
  <div class="tl-center" style="margin-top:36px"><a class="tl-btn" href="/contact"><i class="fa fa-envelope-o"></i>Start My Relocation Plan</a> <a class="tl-btn tl-soft" href="/directory"><i class="fa fa-user"></i>Meet Our Downtown Agents</a></div>
 </div>
</section>
<section class="tl-sec tl-dark" id="tl-relo-faq" style="padding-top:50px;padding-bottom:60px">
 <div class="tl-in">
  <h2 class="tl-h2">Moving To Knoxville <span>FAQ</span></h2>
  <div class="tl-faq">
{faq('Does Tennessee have a state income tax?','No. Tennessee does <b>not tax wages or salaries</b>. Sales tax is higher than in many states, and homes inside Knoxville city limits pay both city and Knox County property taxes.')}{faq('How far is Knoxville from other cities?','Chattanooga is about 1 hour 45 minutes, Nashville about 3 hours and Atlanta about 3 hours 30 minutes by car. McGhee Tyson Airport (TYS) is about 20 to 25 minutes from downtown.')}{faq('What is the weather like?','Knoxville has <b>four seasons</b>: warm, humid summers, colorful falls, mild springs and short winters with only occasional snow.')}{faq('Is downtown Knoxville a good place to live?','Many people love it. You can walk to restaurants, shops, theaters, the riverfront and UT events. We help you pick the right building and street for your lifestyle.')}{faq('What about healthcare?','Knoxville has several large hospitals, including <b>UT Medical Center</b> and <b>Fort Sanders Regional</b>, plus many clinics across Knox County.')}{faq('Can I buy a home before I move?','Yes. Many of our relocation clients buy after one or two visits, using video tours, remote inspections and e-signatures, and close with a local title company.')}{faq('How are the schools?','Public schools are run by <b>Knox County Schools</b>, with private and faith-based options in the area. Zoning follows the address, so we verify assigned schools for each home.')}{faq('Where do I start?','Call us or send a message. We will set up a discovery call, build your area shortlist and start a custom home search the same week.')}  </div>
  <p class="tl-faq-foot">Ready to plan your move? <a href="/contact">Send us a message</a> or call <a href="{TEL}">{P}</a>. Our office is at 625 S. Gay Street #205 in downtown Knoxville.</p>
 </div>
</section>
'''+tail
open(OUT+'relocation.html','w').write(relo)
# contact
s=open(UC+'contact.html').read(); head=s[:s.index('<section class="tl-sec tl-light" id="tl-contact-office"')]
aq=up.quote_plus('625 S. Gay Street #205, Knoxville, TN 37902')
open(OUT+'contact.html','w').write(head+f'''<section class="tl-sec tl-light" id="tl-contact-office" style="padding-top:70px;padding-bottom:60px">
 <div class="tl-in">
  <p class="tl-eyebrow" style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#93a2b5;margin:0 0 10px;text-align:center">Wallace Downtown &middot; Knoxville, TN</p>
  <h2 class="tl-h2">Contact Our <span>Downtown Knoxville Office</span></h2>
  <p class="tl-lead">Stop by our office on Gay Street, call, or send us a message below. A Downtown agent will get back to you the same business day.</p>
  <div class="tl-office" style="padding-top:10px">
   <div class="tl-office-card">
    <h3>Wallace <span>Downtown</span></h3>
    <p><i class="fa fa-map-marker"></i><a href="https://www.google.com/maps/dir/?api=1&destination={aq}" target="_blank" rel="noopener">625 S. Gay Street #205<br>Knoxville, TN 37902</a></p>
    <p><i class="fa fa-phone"></i><a href="{TEL}">{P}</a></p>
    <p><i class="fa fa-envelope-o"></i><a href="mailto:jennifer@wallacetn.com">jennifer@wallacetn.com</a></p>
    <p><i class="fa fa-user"></i>Jennifer Montgomery, Principal Broker</p>
    <p style="margin-top:22px"><a class="tl-btn" href="https://www.google.com/maps/dir/?api=1&destination={aq}" target="_blank" rel="noopener"><i class="fa fa-location-arrow"></i>Get Directions</a> <a class="tl-btn tl-soft" href="/directory"><i class="fa fa-users"></i>Meet Our Agents</a></p>
   </div>
   <div class="tl-office-map"><iframe title="Wallace Downtown office map" src="https://www.google.com/maps?q={aq}&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
 </div>
</section>

</div>
''')
# post-process all
NB=['South Knoxville','Sequoyah Hills','Fountain City','West Hills','Hardin Valley']
for f in ['block.html','office.html','footer.html','buyers.html','sellers.html','relocation.html','contact.html']:
    h=open(OUT+f).read()
    h=h.replace(up.quote('Downtown Knoxville, TN'),up.quote('Downtown, Knoxville, TN'))
    for n in NB: h=h.replace('location_search_field='+up.quote(n+', TN'),'location_search_field='+up.quote(n+', Knoxville, TN'))
    h=re.sub(r'alt="([A-Za-z ]+), Knoxville TN homes',r'alt="\1 Knoxville TN homes',h)
    h=h.replace('Visit Our <span>Knoxville Office','Visit Our <span>Downtown Knoxville Office').replace('Visit Our Knoxville Office','Visit Our Downtown Knoxville Office')
    h=h.replace('https://wallacetwinlakes.com/files/2026/10/Wallace-Twin-Lakes-Logo-Vector.svg','https://ebdf5ndp4dy.exactdn.com/files/2023/04/Wallace-Footer-Logo.png').replace('alt="Wallace Real Estate Twin Lakes"','alt="Wallace Real Estate"')
    h=h.replace('https://wallacetwinlakes.com/files/2026/10/Wallace-Luxury-Twin-Lakes-Logo-Vector.svg','https://ebdf5ndp4dy.exactdn.com/files/2023/04/Wallace-Luxury-Footer-Logo.png').replace('alt="Wallace Luxury Twin Lakes"','alt="Wallace Luxury"')
    open(OUT+f,'w').write(h)
    bad=[w for w in ['Lenoir City office','Loudon County,','Tellico','Twin Lakes','328-1111','105 N','Crossville','Cumberland','Upper Cumberland','931','Victoria','Nelson','Maryville office','nelson-realtors','Fort Loudoun &amp; Tellico'] if w in h]
    print(f,len(h),'BAD' if bad else 'ok',bad)
