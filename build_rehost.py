# Generates rehost/index.html (generic), rehost/business.html (examples incl. hospitality) and rehost/hospitality.html (redirect). Self-contained; relative paths only
import html, hashlib
E=html.escape
ICONS={
'globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/>',
'map':'<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/>',
'cal':'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="M8 14h3v3H8z"/>',
'sync':'<path d="M20 11a8 8 0 0 0-14.3-4.9L4 8"/><path d="M4 3v5h5"/><path d="M4 13a8 8 0 0 0 14.3 4.9L20 16"/><path d="M20 21v-5h-5"/>',
'list':'<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
'inbox':'<path d="M3 13l3-8h12l3 8v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M3 13h5l1 3h6l1-3h5"/>',
'camera':'<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>',
'chat':'<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
'pen':'<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13.5 6.5l4 4"/>',
'hash':'<path d="M5 9h14M5 15h14M10 4 8 20M16 4l-2 16"/>',
'video':'<rect x="3" y="6" width="13" height="12" rx="2"/><path d="m16 10 5-3v10l-5-3"/>',
'star':'<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
'bolt':'<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
'basket':'<path d="M3 9h18l-2 11H5z"/><path d="M8 9l4-6 4 6"/><path d="M9 13v4M15 13v4"/>',
'glass':'<path d="M7 3h10l-1 8a4 4 0 0 1-8 0z"/><path d="M12 15v6M8 21h8"/>',
'check':'<path d="M5 12.5l4.5 4.5L19 7"/>',
'shield':'<path d="M12 3 4 6v6c0 5 3.4 8.4 8 9 4.6-.6 8-4 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
'lock':'<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
'key':'<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l3 3M14 9l2 2"/>',
'user':'<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
'info':'<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
'handshake':'<path d="M2 12l4-4 4 2 3-2 4 1 5 3"/><path d="M6 8v6l5 5 2-1 2 1 4-4"/><path d="M11 13l2 2"/>',
'euro':'<path d="M17 6a7 7 0 1 0 0 12"/><path d="M4 10h9M4 14h9"/>',
'doc':'<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
'search':'<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
'copy':'<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>',
'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
'server':'<rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 7.5h.01M7 16.5h.01"/>',
'chart':'<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
}
def I(n,cls=''):
    return f'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{(" class=%s"%chr(34)+cls+chr(34)) if cls else ""}>{ICONS[n]}</svg>'


ICONS.update({
'shop':'<path d="M3 9l1.5-5h15L21 9"/><path d="M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/><path d="M5 12v9h14v-9M10 21v-5h4v5"/>',
'wrench':'<path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
'plus':'<rect x="3" y="3" width="18" height="18" rx="5"/><path d="M12 8v8M8 12h8"/>',
'users':'<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2a5 5 0 0 1 5.5 5.8"/>',
'compass':'<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
'bed':'<path d="M3 18V6M3 13h18v5M21 13a3 3 0 0 0-3-3h-7v3"/><circle cx="7" cy="10.5" r="1.8"/>',
'home':'<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/>',
'spark':'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
'hammer':'<path d="M2 19h20"/><path d="M4 19v-1a8 8 0 0 1 16 0v1"/><path d="M10 11V6.5a2 2 0 0 1 4 0V11"/>',
'scissors':'<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.2 8.2 20 20M8.2 15.8 20 4"/>',
'car':'<path d="M5 17H3v-5l2-5h14l2 5v5h-2"/><path d="M3 12h18"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/><path d="M9.5 17h5"/>',
'leaf':'<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19c3-4 6-7 10-9"/>',
'calc':'<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h.01M12 12h.01M16 12h.01M8 16h.01M12 16h.01M16 16h.01"/>',
'flag':'<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
'tag':'<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.3"/>',
'link':'<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
})
OUTDIR='/workspace/rehost-repo/'
# Cache-busting: ?v= is a hash of the asset files, so every change to style.css/app.js/favicon.svg gets a new URL
# (GitHub Pages sends max-age=600, so without this a browser can pair new HTML with an old stylesheet).
def _ver():
    h=hashlib.sha1()
    for f in ('style.css','app.js','favicon.svg'):
        h.update(open(OUTDIR+f,'rb').read())
    return h.hexdigest()[:10]
VER=_ver()
LOGO='''<svg viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14b8a6"/><stop offset="1" stop-color="#0f5f73"/></linearGradient></defs><rect width="64" height="64" rx="16" fill="url(#lg)"/><path d="M45 22a16 16 0 1 0 3 14" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/><path d="M41 14l6 8-9 3" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><path d="M24 33l6 6 11-12" fill="none" stroke="#ffb199" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def BRAND(href): return f'<a class="brand" href="{href}" aria-label="rehost.expert home">{LOGO}<b>rehost<span>.expert</span></b></a>'

# ---------------- services (generic, home page picker) ----------------
SV=[
('Website','globe','Hosting and updates','Fast, low-cost hosting on your own domain with a secure (https) certificate. Text, photo, product, menu and price changes whenever you ask.','Changes within 2 working days',False),
('Website','shield','Domain and certificate care','Your domain kept in your name and set to auto-renew, certificates renewed automatically, and both checked from outside every day so the padlock never lapses.','Checked daily',False),
('Website','wrench','Fixes and rebuilds','Broken pages, WordPress errors, out-of-date plugins and slow, non-mobile sites repaired, or rebuilt on simple hosting with nothing to patch.','On request',False),
('Website','map','Area pages with maps','Pages on your area, what\u2019s nearby and how to find you, with a map. Customers find you in more local Google searches.','New page each season',False),
('Website','cal','News and events page','A news, offers or events page customers can follow, with bank holidays and seasonal hours marked.','Updates automatically',False),
('Bookings','sync','Live bookings or availability calendar','Your website calendar stays in sync with your booking or appointment system, so customers never pick a time or date that\u2019s already taken.','Every hour',False),
('Bookings','list','Listings and directories','Your Google Business Profile, directory and booking-site listings, photos and opening hours kept accurate and up to date.','Monthly check, plus on request',False),
('Customers','inbox','Email inbox management','Business inbox sorted, replies to enquiries drafted for you to approve, and reminders for anything needing a follow-up.','Daily',False),
('Social','camera','Instagram','DMs and comments checked, real enquiries flagged, spam ignored. Replies drafted for enquiries.','Daily checks',False),
('Social','chat','Facebook','Messages and comments checked, enquiries flagged. Replies drafted for enquiries.','Daily checks',False),
('Social','pen','Posts','A quarterly or six-monthly content calendar with posts, stories and reels written and scheduled across Instagram and Facebook, including offers, new stock and events.','Weekly or monthly',False),
('Social','hash','X (Twitter)','Posts on local news and updates from your business, with mentions and replies checked.','Weekly',False),
('Social','video','TikTok','Short videos of your work, products, premises and the area, planned and posted for you.','Weekly or monthly',False),
('Reviews','search','Google reviews','New Google reviews flagged and replies drafted for your approval, so every customer gets an answer.','Daily checks',False),
('Reviews','star','Other review sites','TripAdvisor, Facebook recommendations or the review sites your customers use: new reviews flagged and replies drafted for your approval.','Daily checks',False),
('Admin','sun','WhatsApp morning summary','One message each morning to you or your staff: new enquiries, bookings or orders, emails needing a reply, reviews and anything to do with the website.','Every morning',False),
('Admin','bolt','Utility costs monitoring','Electricity, heating, water and broadband costs tracked against how busy you were and the same month last year, using smart-meter data where available. Unusual jumps, billing errors and cheaper tariffs flagged.','Monthly report',False),
('AI','spark','AI consultation','A consultation to talk through how AI could help your business: automating repetitive admin, answering enquiries, summaries and reports, bookings and ordering, drafting posts and emails, and linking up the tools you already use.','One-off, price on request',False),
('Add-on','search','SEO and Google visibility','Page titles and descriptions written for the searches your customers make, your business details marked up for Google, and a short monthly report on how people find you.','Monthly',True),
('Add-on','basket','Supplier ordering automation','Regular supplier orders worked out from your bookings or sales, updated as things change, and approved by you on WhatsApp before they go.','Weekly',True),
]
GROUPS=[('Website','globe'),('Bookings','cal'),('Customers','inbox'),('Social','chat'),('Reviews','star'),('Admin','chart'),('AI','spark'),('Add-on','basket')]
NUMW={15:'Fifteen',16:'Sixteen',17:'Seventeen',18:'Eighteen'}
N_CORE=sum(1 for s in SV if not s[5]); N_ADD=len(SV)-N_CORE
def svc_html():
    out=[]
    for g,gi in GROUPS:
        items=[(i,s) for i,s in enumerate(SV) if s[0]==g]
        out.append(f'<div class="group rv"><h3>{I(gi)}{"Add-ons" if g=="Add-on" else "AI" if g=="AI" else E(g)}</h3>')
        for i,s in items:
            nm=E(s[2])
            out.append(f'''<article class="svc" data-i="{i}" data-area="{E(g)}" data-name="{nm}">
<div><h4>{nm}{' <span class="addon">Add-on</span>' if s[5] else ''} <span class="freq">{I('clock')}{E(s[4])}</span></h4><p>{E(s[3])}</p></div>
<fieldset class="seg"><legend>Include {nm}?</legend>
<label class="y"><input type="radio" name="s{i}" value="yes"><span>Yes</span></label>
<label class="m"><input type="radio" name="s{i}" value="maybe"><span>Maybe</span></label>
<label class="n"><input type="radio" name="s{i}" value="no"><span>No</span></label>
</fieldset></article>''')
        out.append('</div>')
    return '\n'.join(out)

# ---------------- browser "screens" for problems ----------------
def screen(kind,dom):
    base='<svg viewBox="0 0 320 150" role="img" aria-label="{a}"><rect x="1" y="1" width="318" height="148" rx="10" fill="#fff" stroke="#dfe3e7"/><rect x="1" y="1" width="318" height="26" rx="10" fill="#eef1f4"/><rect x="1" y="17" width="318" height="10" fill="#eef1f4"/><circle cx="16" cy="14" r="4" fill="#f87171"/><circle cx="29" cy="14" r="4" fill="#fbbf24"/><circle cx="42" cy="14" r="4" fill="#34d399"/><rect x="58" y="7" width="200" height="14" rx="7" fill="#fff"/>{u}{b}</svg>'
    if kind=='cert':
        u='<path d="M66 11l5 0 0 6-5 0z" fill="#ef4444"/><text x="76" y="18" font-size="8" fill="#b91c1c" font-family="system-ui">Not secure \u00b7 https://DOM</text>'
        b='<g transform="translate(26 44)"><path d="M18 0 36 32H0z" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/><path d="M18 10v11M18 25v2" stroke="#b91c1c" stroke-width="3" stroke-linecap="round"/></g><text x="78" y="58" font-size="12" font-weight="700" fill="#1f2937" font-family="system-ui">Your connection is not private</text><text x="78" y="74" font-size="8.5" fill="#6b7280" font-family="system-ui">NET::ERR_CERT_DATE_INVALID</text><rect x="78" y="86" width="190" height="6" rx="3" fill="#e5e7eb"/><rect x="78" y="98" width="150" height="6" rx="3" fill="#e5e7eb"/><rect x="218" y="114" width="80" height="22" rx="11" fill="#2563eb"/><text x="258" y="129" font-size="9" fill="#fff" text-anchor="middle" font-family="system-ui">Back to safety</text>'
        a='Browser warning: your connection is not private'
    elif kind=='domain':
        u='<text x="66" y="18" font-size="8" fill="#6b7280" font-family="system-ui">DOM</text>'
        b='<rect x="20" y="40" width="280" height="96" rx="8" fill="#fff7ed"/><text x="160" y="70" font-size="15" font-weight="800" fill="#9a3412" text-anchor="middle" font-family="system-ui">This domain is for sale!</text><text x="160" y="88" font-size="9" fill="#7c2d12" text-anchor="middle" font-family="system-ui">DOM may be available. Make an offer today.</text><rect x="110" y="100" width="100" height="22" rx="11" fill="#ea580c"/><text x="160" y="115" font-size="9" fill="#fff" text-anchor="middle" font-family="system-ui">Buy this domain</text>'
        a='Parked page: this domain is for sale'
    elif kind=='wp':
        u='<text x="66" y="18" font-size="8" fill="#6b7280" font-family="system-ui">https://DOM</text>'
        b='<text x="24" y="62" font-size="12" font-weight="700" fill="#1f2937" font-family="system-ui">There has been a critical error</text><text x="24" y="78" font-size="12" font-weight="700" fill="#1f2937" font-family="system-ui">on this website.</text><text x="24" y="100" font-size="9" fill="#2563eb" text-decoration="underline" font-family="system-ui">Learn more about troubleshooting WordPress.</text><rect x="24" y="114" width="120" height="6" rx="3" fill="#e5e7eb"/><text x="296" y="140" font-size="8" fill="#9ca3af" text-anchor="end" font-family="system-ui">HTTP 500</text>'
        a='WordPress critical error page'
    elif kind=='host':
        u='<path d="M66 11l5 0 0 6-5 0z" fill="#ef4444"/><text x="76" y="18" font-size="8" fill="#b91c1c" font-family="system-ui">https://DOM</text>'
        b='<g transform="translate(24 42)"><rect width="120" height="80" rx="8" fill="#f8fafc" stroke="#cbd5e1"/><text x="10" y="18" font-size="8" fill="#64748b" font-family="system-ui">Certificate issued to:</text><text x="10" y="34" font-size="10" font-weight="700" fill="#b91c1c" font-family="system-ui">*.shared-host.net</text><text x="10" y="52" font-size="8" fill="#64748b" font-family="system-ui">Expected:</text><text x="10" y="66" font-size="10" font-weight="700" fill="#15803d" font-family="system-ui">DOM</text></g><text x="160" y="64" font-size="11" font-weight="700" fill="#1f2937" font-family="system-ui">Warning: potential</text><text x="160" y="79" font-size="11" font-weight="700" fill="#1f2937" font-family="system-ui">security risk ahead</text><text x="160" y="97" font-size="8.5" fill="#6b7280" font-family="system-ui">ERR_CERT_COMMON_NAME_INVALID</text>'
        a='Wrong certificate: issued to the hosting company, not your domain'
    else:
        u='<text x="66" y="18" font-size="8" fill="#6b7280" font-family="system-ui">https://DOM</text>'
        b='<text x="160" y="80" font-size="40" font-weight="900" fill="#e5e7eb" text-anchor="middle" font-family="system-ui">5xx</text><text x="160" y="104" font-size="11" font-weight="700" fill="#1f2937" text-anchor="middle" font-family="system-ui">503 Service Unavailable</text><text x="160" y="120" font-size="8.5" fill="#6b7280" text-anchor="middle" font-family="system-ui">The server is temporarily unable to handle your request.</text>'
        a='Server error: 503 Service Unavailable'
    return base.format(a=a,u=u,b=b).replace('DOM',dom)

PROBS=[
('cert','Expired certificate','Visitors get a full-screen \u201cYour connection is not private\u201d warning. Most turn back, and Google marks the site as not secure.','We install free, auto-renewing certificates and monitor them, so the padlock never lapses.'),
('domain','Lapsed domain','The domain renewal was missed, and now the address shows a parked \u201cfor sale\u201d page or nothing at all. Customers think you\u2019ve closed.','We recover or move the domain into your name, set it to auto-renew and track the renewal date for you.'),
('wp','WordPress critical error','An out-of-date plugin or theme crashes the site, leaving a blank page with \u201cThere has been a critical error on this website.\u201d','We rebuild the site on fast, low-maintenance hosting with nothing to patch, or repair and update it.'),
('host','The host\u2019s wrong certificate','Your hosting company serves its own certificate instead of yours, so browsers say the site might be impersonating you.','We set up the certificate for your own domain and check it from outside every day.'),
('server','Server errors','500 and 503 errors, timeouts and suspended hosting accounts. The site is down, and nobody notices until a customer mentions it.','We rehost on reliable infrastructure with 24/7 uptime checks, and we fix problems before customers see them.'),
]
def probs_html():
    return '\n'.join(f'<article class="prob rv"><div class="screen">{screen(k,"yourbusiness.ie")}</div><div class="body"><span class="tag">What customers see</span><h3>{E(t)}</h3><p class="muted">{E(d)}</p><div class="fix">{I("shield")}<span><b>How we fix it:</b> {E(f)}</span></div></div></article>' for k,t,d,f in PROBS)

# ---------------- hospitality ordering ----------------
FOOD=[('Eggs','2','280'),('Rashers','2','280'),('Sausages','2','280'),('Black and white pudding','1 slice of each','140 slices of each'),('Tomatoes','\u00bd','70'),('Mushrooms','50 g','7 kg'),('Brown soda bread','2 slices','280 slices (about 20 loaves)'),('White bread for toast','2 slices','280 slices (about 14 sliced pans)'),('Butter','15 g','2.1 kg'),('Jam and marmalade','1 portion','140 portions'),('Cereal','40 g','5.6 kg'),('Yogurt','\u00bd pot','70 pots'),('Orange juice','200 ml','28 L'),('Milk','0.25 L','35 L'),('Tea','2 bags','280 bags'),('Coffee','15 g','2.1 kg')]
DRINK=[('Draught stout (kegs)',2,3),('House wine (bottles)',24,34),('Soft drinks (cases)',4,6)]
FOOD_STEPS=[('Created every Monday.','A draft order for the week is built from confirmed bookings: guests each night, breakfasts, and arrivals needing a welcome pack.'),('Worked out for you.','Quantities come from a per-guest list we agree once, minus what\u2019s already in stock from a 2-minute stock check on your phone.'),('Updated as bookings change.','When a booking comes in, changes or is cancelled, the order adjusts itself and WhatsApp tells you what moved, for example \u201c+40 eggs, +10 L milk: new booking Fri to Sun\u201d.'),('Approved, then sent.','Before each supplier\u2019s cut-off, you get the final order on WhatsApp. Reply OK or change it, and it goes to the supplier by email or their ordering site.'),('Tuned daily, weekly or monthly.','We compare what was ordered with what was used, and adjust quantities to cut waste.')]
DRINK_STEPS=[('Forecast from bookings.','Guests each night, plus any group, wedding or event bookings, set the base for the week.'),('Adjusted for the season.','Bank holidays, the summer peak and local events such as regattas and festivals raise the forecast. Quiet months lower it.'),('Checked against stock.','A quick weekly count on your phone of kegs, spirits, wine, soft drinks and welcome bottles, with each item ordered back up to an agreed level.'),('Timed for each supplier.','Kegs and wine often need ordering earlier, so each order is raised in time for that distributor\u2019s delivery day.'),('Updated, approved, sent.','The order changes as bookings change, you approve the final version on WhatsApp, and it goes to your suppliers.'),('Learns from your sales.','If your till can export sales, the same week last year is used to sharpen the forecast.')]
def steps(L): return '<ol class="steps">'+''.join(f'<li class="rv"><b>{E(a)}</b><span>{E(b)}</span></li>' for a,b in L)+'</ol>'
food_rows=''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td class="num">{E(c)}</td></tr>' for a,b,c in FOOD)
def pct(v,m): return round(v/m*100)
drink_rows=''.join(f'<tr><td>{E(a)}</td><td><div class="cmp" style="--v:{pct(n,max(n,b)*1.0)*0.7:.0f}"><i></i><em>{n}</em></div></td><td><div class="cmp bh" style="--v:{70}"><i></i><em>{b}</em><span class="uplift">+{round((b-n)/n*100)}%</span></div></td></tr>' for a,n,b in DRINK)

# ---------------- morning summaries ----------------
MORNING_G=[
('<b>Good morning \u2014 Tuesday 4 August</b> \u2600\ufe0f','07:30'),
('<b>Enquiries: 3 new.</b><ul><li>Quote request from the website form <span class="pill">website</span></li><li>Opening hours on Saturday <span class="pill">Facebook</span></li><li>Is the blue one back in stock? <span class="pill">Instagram</span></li></ul>Replies drafted, waiting for your OK.','07:30'),
('<b>Today:</b> 4 appointments booked online, 2 orders to collect.','07:30'),
('<b>Reviews:</b> 1 new Google review \u2b50\u2b50\u2b50\u2b50\u2b50. Thank-you reply drafted.','07:30'),
('<b>Email:</b> 1 needs your reply: a supplier invoice query.','07:30'),
('<b>Website:</b> all checks OK. Domain auto-renews in 23 days.','07:30'),
]
MORNING_H=[
('<b>Good morning \u2014 Tuesday 4 August</b> \u2600\ufe0f','07:30'),
('<b>Bookings: 10 new since yesterday.</b><ul><li>Room 1: Murphy, 3 nights from 14 Aug <span class="pill">Booking.com</span></li><li>Room 2: O\u2019Sullivan, 2 nights from 15 Aug <span class="pill">direct</span></li><li>Room 4: Schmidt, 4 nights from 16 Aug <span class="pill">Booking.com</span></li><li>Room 5: Walsh, 1 night from 14 Aug <span class="pill">Expedia</span></li><li>Room 7: Brennan, 2 nights from 21 Aug <span class="pill">phone</span></li><li>Room 8: Dubois, 3 nights from 18 Aug <span class="pill">Booking.com</span></li><li>Room 9: Kelly, 5 nights from 22 Aug <span class="pill">direct</span></li><li>Room 11: Thompson, 2 nights from 15 Aug <span class="pill">Expedia</span></li><li>Room 12: McCarthy, 1 night from 17 Aug <span class="pill">Booking.com</span></li><li>Room 14: Rossi, 3 nights from 25 Aug <span class="pill">direct</span></li></ul>','07:30'),
('<b>Today:</b> 2 check-ins (rooms 3 and 6), 1 check-out (room 10).','07:30'),
('<b>Enquiries: 2 new.</b> A family of 5 asking about August availability (reply drafted, waiting for your OK). An Instagram DM asking about dogs.','07:30'),
('<b>Email:</b> 1 needs your reply: a supplier invoice query.','07:30'),
('<b>On today:</b> guided walk in Glengarriff Nature Reserve at 10am, and a trad session at 9pm in Harrington\u2019s.','07:30'),
]
def chat_html(M,reply):
    return '<div class="day">TODAY</div>'+''.join(f'<div class="bub">{t}<time>{tm}</time></div>' for t,tm in M)+f'<div class="bub me">{reply}<time>07:42</time></div>'
def phone(M,reply):
    return f'''<div class="phone" role="img" aria-label="Example morning summary message on a phone"><div class="screen-in">
<div class="chat-top"><span class="av">{I('sun')}</span><span><b>Morning summary</b><small>rehost.expert \u00b7 example</small></span></div>
<div class="chat" id="chat">{chat_html(M,reply)}</div></div></div>'''

# ---------------- packages ----------------
PLANS=[('Essentials','For getting your site fixed, secure and looked after.',['Website hosting and updates','Domain and certificate care','Renewals and backups'],None,False),
('Growth','For being found by more customers.',['Google Business Profile and listings','Area pages with maps','News and events page'],'Everything in Essentials, plus',True),
('Full service','For handing over the day-to-day screen work.',['Instagram and Facebook','Inbox management','WhatsApp morning summary'],'Everything in Growth, plus',False)]
def plans_html():
    o=[]
    for n,d,inc,inh,feat in PLANS:
        li=(f'<li class="inh">{I("check")}{E(inh)}</li>' if inh else '')+''.join(f'<li>{I("check")}{E(x)}</li>' for x in inc)
        o.append(f'<article class="plan rv{" feat" if feat else ""}"><h3>{E(n)}</h3><p class="muted">{E(d)}</p><div class="price" aria-label="Monthly fee: to be confirmed"><b>\u20ac[&nbsp;&nbsp;]</b><small>/ month ex VAT</small></div><span class="por">Price on request</span><ul>{li}</ul></article>')
    return '\n'.join(o)
ADDONS_G=[('search','SEO and Google visibility','Your Google Business Profile kept up to date, page titles and descriptions written for the searches your customers make, your business details marked up for Google, and a short monthly report on how people find you.'),
('basket','Supplier ordering automation','Regular supplier orders worked out from your bookings or sales, updated as things change, approved on WhatsApp and sent to your suppliers. Adds to any package. <a href="business.html#ordering">See the hospitality example</a>.'),
('spark','AI consultation','A one-off consultation to talk through where AI could help your business, and where it wouldn\u2019t. <a href="#ai">What we cover</a>.','POR')]
ADDONS_H=[('basket','Food ordering automation','Weekly food order built from bookings, updated as bookings change, approved on WhatsApp and sent to your suppliers. Adds to any package; needs access to your booking confirmation emails.'),
('glass','Drink ordering automation','Weekly drinks order built from bookings, events and the time of year, timed for each supplier\u2019s delivery day and approved on WhatsApp. Adds to any package.'),
('search','SEO and Google visibility','Your Google Business Profile kept up to date, page titles and descriptions written for the searches guests make, hotel and restaurant details marked up for Google, and a short monthly report on how people find you.')]
def addons_html(L):
    o=[]
    for it in L:
        i,t,d=it[:3]; por=len(it)>3
        price='<span class="p por-p">Price on request</span>' if por else '<span class="p">\u20ac[&nbsp;&nbsp;]<small class="muted" style="font-weight:600;font-size:.8rem"> / month</small></span>'
        tag='<span class="addon">One-off</span>' if por else '<span class="addon">Add-on</span>'
        o.append(f'<article class="addon-card rv{" ai-card" if por else ""}"><div class="top-row">{I(i,"ic")}{price}</div>{tag}<h4>{E(t)}</h4><p>{d if "<a" in d else E(d)}</p></article>')
    return '\n'.join(o)

TOG=[('key','Your domain, your control','You control everything to do with your website domain. If we stop working together, the domain is transferred back to you or to a provider of your choosing.'),
('user','No shared passwords','We\u2019re added as a user or page admin on your accounts, such as Google Business Profile, Facebook, Instagram and your booking system. You can remove our access at any time.'),
('shield','Nothing goes out without you','Replies to customers are drafted for your approval, unless you ask us to send routine ones directly.'),
('chat','One point of contact','WhatsApp or email us for any changes you require.')]
tog_html='\n'.join(f'<div class="tog rv">{I(i)}<b>{E(t)}</b><p>{E(d)}</p></div>' for i,t,d in TOG)

NEXT=[('Introductory consultation','A 90-minute consultation to go through what you need and pick a package.',None,None),
('Contract agreement','Once the services are agreed, we send a contract detailing the services and fees.',None,None),
('Service onboarding','Once the contract is signed, an onboarding period of about one week begins. It includes:',[('Access','to your website, domain, booking or sales systems and social accounts.'),('Automation review:','a meeting to walk through how your business runs day to day, catch anything we\u2019ve missed, and agree which other tasks would be useful to automate.')],'About one week'),
('Branding and photos','We agree the look of the new site, including logo, colours and tone, and arrange photos of your premises, products or work, team and surroundings.',None,None),
('Build and design','We build the site and refine the look and feel with you during the design phase.',None,None),
('Go live','Your new site and morning summary are live within <span class="ph" title="To be confirmed">[&nbsp;&nbsp;]</span> weeks.',None,None)]
def next_html():
    o=[]
    for i,(t,d,sub,w) in enumerate(NEXT,1):
        s=''
        if sub: s='<ol>'+''.join(f'<li><strong>{E(a)}</strong> {E(b)}</li>' for a,b in sub)+'</ol>'
        o.append(f'<li class="rv"><span class="k">{i}</span><div class="c">{f"<span class=when>{E(w)}</span>" if w else ""}<b>{E(t)}</b><span>{d}</span>{s}</div></li>')
    return '<ol class="timeline">'+''.join(o)+'</ol>'

# ---------------- AI consultation ----------------
AI_EX=[('sync','Repetitive processes and admin','The jobs you do the same way every week, such as copying details between systems, chasing invoices or filling in forms.'),
('chat','Customer enquiries and messages','Drafting replies to common questions from email, your website, Facebook and Instagram, for you to check before they go.'),
('sun','Morning summaries and reports','One short message or report pulling together what happened yesterday and what needs you today.'),
('cal','Bookings and ordering','Keeping calendars in step, and working out supplier orders from your bookings or sales, with you approving each one.'),
('pen','Social posts and emails','First drafts of posts, newsletters and emails in your own tone, ready for you to edit.'),
('link','Linking up your tools','Getting the tools you already use, such as your inbox, calendar, till, booking system and spreadsheets, to pass information to each other.')]
ai_ex_html='\n'.join(f'<div class="ai-ex rv">{I(i)}<b>{E(t)}</b><p>{E(d)}</p></div>' for i,t,d in AI_EX)
def chipsvg(x,y,label,cls,icon,w=150):
    return f'<g transform="translate({x} {y})"><g class="{cls}"><rect width="{w}" height="44" rx="12" fill="#1d2f3d" stroke="rgba(255,255,255,.12)"/><g transform="translate(12 10)"><rect width="24" height="24" rx="7" fill="rgba(20,184,166,.18)"/><svg x="4" y="4" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#5eead4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</svg></g><text x="46" y="27" font-size="12" font-weight="700" fill="#e9eef2" font-family="system-ui">{label}</text></g></g>'
AI_CHIPS=[(10,30,'Email inbox','float','inbox'),(320,30,'Calendar','float2','cal'),(0,178,'Till and orders','float3','basket'),(330,178,'Social posts','float','pen'),(10,326,'Spreadsheets','float2','list'),(296,326,'WhatsApp summary','float3','sun',176)]
def ai_art():
    lines=''.join(f'<path class="flow" d="M240 200 L{c[0]+75} {c[1]+22}" stroke="url(#aig)" stroke-width="2" stroke-dasharray="3 7" fill="none"/>' for c in AI_CHIPS)
    chips=''.join(chipsvg(*c) for c in AI_CHIPS)
    return f'''<svg viewBox="0 0 480 400" role="img" aria-label="Illustration: an AI assistant in the middle, linked to your email inbox, calendar, till and orders, social posts, spreadsheets and WhatsApp summary">
<defs><linearGradient id="aig" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14b8a6"/><stop offset="1" stop-color="#f26b4f"/></linearGradient>
<radialGradient id="aiglow"><stop offset="0" stop-color="rgba(20,184,166,.35)"/><stop offset="1" stop-color="rgba(20,184,166,0)"/></radialGradient>
<linearGradient id="aicore" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14b8a6"/><stop offset="1" stop-color="#0f5f73"/></linearGradient></defs>
<circle cx="240" cy="200" r="150" fill="url(#aiglow)"/>
<circle cx="240" cy="200" r="96" fill="none" stroke="rgba(255,255,255,.1)" stroke-width="1.5"/>
<circle class="spin" cx="240" cy="200" r="70" fill="none" stroke="rgba(20,184,166,.45)" stroke-width="1.5" stroke-dasharray="4 9"/>
{lines}
<g transform="translate(200 160)"><rect width="80" height="80" rx="22" fill="url(#aicore)"/><path d="M40 16l4.5 13L57.5 33.5 44.5 38 40 51l-4.5-13-13-4.5 13-4.5z" fill="#fff"/><path d="M60 50l2 5.5 5.5 2-5.5 2-2 5.5-2-5.5-5.5-2 5.5-2z" fill="#ffb199"/></g>
<text x="240" y="268" font-size="11" font-weight="800" fill="#5eead4" text-anchor="middle" font-family="system-ui" letter-spacing="1.5">YOUR AI ASSISTANT</text>
{chips}
</svg>'''


CFIELDS=[('name','Your name','text','name',''),('biz','Business','text','organization','e.g. your shop, practice or club'),('email','Email address','email','email','e.g. you@yourbusiness.ie'),('phone','Phone number','tel','tel','e.g. 087 123 4567'),('site','Website address','text','url','e.g. yourbusiness.ie')]
def contact_fields(pre='f-'):
    o=[]
    for k,l,t,ac,ph in CFIELDS:
        i=pre+k
        im=' inputmode="url"' if i=='f-site' else ''
        o.append(f'<div class="fld"><label class="f" for="{i}">{E(l)} <span class="req" aria-hidden="true">*</span></label><input type="{t}" id="{i}" name="{k}" autocomplete="{ac}"{im} placeholder="{E(ph)}" required aria-required="true" aria-describedby="{i}-err"><p class="ferr" id="{i}-err" hidden></p></div>')
    return '\n'.join(o)

# ---------------- sectors (add a page later by setting the href) ----------------
SECTORS=[('bed','Hospitality','Hotels, B&Bs, guesthouses, restaurants, caf\u00e9s and bars: booking calendars, guest messages, reviews, and food and drink orders built from bookings.','business.html#hospitality'),
('hammer','Builders and trades','A site that wins quote requests, with enquiries from every channel in one morning message, and quotes and invoices drafted for you.','business.html#builders'),
('shop','Shops and retail','Opening hours, products and offers kept current, Google listing looked after, and customer messages answered.','business.html#retail'),
('plus','Clinics and practices','Appointment calendars in sync, clear contact details, and a secure site patients can trust.','business.html#clinics'),
('users','Clubs and community groups','Fixtures, events and news pages that stay up to date, and a site that doesn\u2019t depend on one volunteer.','business.html#clubs'),
('compass','Tourism and activities','Tours, attractions and activity providers: availability, area guides with maps, and reviews answered.','business.html#tours')]
def sectors_html():
    return '\n'.join(f'<a class="sector lnk rv" href="{h}">{I(ic,"ic")}<b>{E(t)}</b><p>{E(d)}</p><span class="go">See the example {I("arrow")}</span></a>' for ic,t,d,h in SECTORS)

# ---------------- hero art (generic or hotel) ----------------
def hero_art(kind):
    if kind=='hotel':
        dom='yourhotel.ie'; title='Your hotel'; sub='Rooms \u00b7 Restaurant \u00b7 Bar'; btn='Book direct'
        bld='<g transform="translate(150 118)"><rect x="0" y="8" width="34" height="22" fill="#fffdf9"/><path d="M-4 10 17 -6 38 10z" fill="#b93d1f"/><rect x="13" y="18" width="8" height="12" fill="#0f5f73"/><rect x="4" y="14" width="6" height="6" fill="#bfe9e2"/><rect x="24" y="14" width="6" height="6" fill="#bfe9e2"/></g>'
        chip=('Calendar in sync','Airbnb \u00b7 Booking.com \u00b7 direct','cal')
        aria='a broken hotel website with a security warning being rehosted into a secure, working site with bookings, reviews and messages'
    else:
        dom='yourbusiness.ie'; title='Your business'; sub='Shop \u00b7 Services \u00b7 Contact'; btn='Get in touch'
        bld=('<g transform="translate(140 104)"><rect x="0" y="12" width="56" height="30" fill="#fffdf9"/>'
             '<path d="M-3 12h62l-5-10H2z" fill="#f26b4f"/><path d="M9 2l-3 10M19 2l-1 10M29 2v10M39 2l1 10M49 2l3 10" stroke="#fff" stroke-width="3"/>'
             '<rect x="6" y="20" width="18" height="12" rx="1.5" fill="#bfe9e2"/><rect x="32" y="19" width="14" height="23" fill="#0f5f73"/><circle cx="43" cy="31" r="1.2" fill="#ffd27a"/></g>')
        chip=('Enquiries answered','Email \u00b7 Facebook \u00b7 Instagram','chat')
        aria='a broken business website with a security warning being rehosted into a secure, working site with enquiries, reviews and messages'
    if chip[2]=='cal': chipic='<g transform="translate(18 20)" fill="none" stroke="#b93d1f" stroke-width="2"><rect x="0" y="2" width="20" height="17" rx="2"/><path d="M0 7h20M5 0v4M15 0v4"/></g>'
    else: chipic='<g transform="translate(17 19)" fill="none" stroke="#b93d1f" stroke-width="2" stroke-linejoin="round"><path d="M2 2h18v12H9l-5 4v-4H2z"/></g>'
    return f'''<svg viewBox="0 0 560 470" role="img" aria-label="Illustration: {aria}">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe9e2"/><stop offset="1" stop-color="#eaf7f4"/></linearGradient>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14b8a6"/><stop offset="1" stop-color="#0f5f73"/></linearGradient>
<linearGradient id="arc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f26b4f"/><stop offset="1" stop-color="#14b8a6"/></linearGradient>
</defs>
<g transform="translate(8 26) rotate(-6 120 90)" opacity=".95"><g class="float2">
<rect width="230" height="160" rx="14" fill="#fff"/>
<rect width="230" height="28" rx="14" fill="#f3e3df"/><rect y="16" width="230" height="12" fill="#f3e3df"/>
<circle cx="16" cy="14" r="4" fill="#f87171"/><circle cx="29" cy="14" r="4" fill="#fbbf24"/><circle cx="42" cy="14" r="4" fill="#d1d5db"/>
<rect x="56" y="8" width="150" height="12" rx="6" fill="#fff"/><path d="M62 11h5v6h-5z" fill="#ef4444"/><text x="71" y="17.5" font-size="7.5" fill="#b91c1c" font-family="system-ui">Not secure</text>
<path d="M92 46 116 88H68z" fill="#fee2e2" stroke="#ef4444" stroke-width="2.5" stroke-linejoin="round"/><path d="M92 59v14M92 79v2" stroke="#b91c1c" stroke-width="4" stroke-linecap="round"/>
<text x="92" y="110" font-size="11" font-weight="800" fill="#1f2937" text-anchor="middle" font-family="system-ui">Your connection</text>
<text x="92" y="124" font-size="11" font-weight="800" fill="#1f2937" text-anchor="middle" font-family="system-ui">is not private</text>
<rect x="42" y="136" width="100" height="6" rx="3" fill="#eceff2"/>
</g></g>
<path class="scan" d="M168 214c40 40 90 52 140 36" fill="none" stroke="url(#arc)" stroke-width="4" stroke-linecap="round" stroke-dasharray="2 10"/>
<path class="scan" d="M300 240l14 8-12 10" fill="none" stroke="#14b8a6" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<g transform="translate(196 112)">
<rect width="350" height="250" rx="18" fill="#fff"/>
<rect width="350" height="32" rx="18" fill="#eef4f3"/><rect y="18" width="350" height="14" fill="#eef4f3"/>
<circle cx="18" cy="16" r="4.5" fill="#f87171"/><circle cx="32" cy="16" r="4.5" fill="#fbbf24"/><circle cx="46" cy="16" r="4.5" fill="#34d399"/>
<rect x="62" y="8" width="230" height="16" rx="8" fill="#fff"/>
<rect x="70" y="12" width="8" height="8" rx="2" fill="none" stroke="#15803d" stroke-width="1.6"/><path d="M71.5 12v-2a2.5 2.5 0 0 1 5 0v2" fill="none" stroke="#15803d" stroke-width="1.6"/>
<text x="84" y="20" font-size="8.5" fill="#15803d" font-weight="700" font-family="system-ui">https://{dom}</text>
<clipPath id="hc"><rect x="14" y="44" width="322" height="118" rx="10"/></clipPath>
<g clip-path="url(#hc)">
<rect x="14" y="44" width="322" height="118" fill="url(#sky)"/>
<circle cx="276" cy="72" r="14" fill="#ffd27a"/>
<path d="M14 132 70 92l36 22 50-40 58 42 40-26 52 34 30-14v52H14z" fill="#3f7f6f"/>
<path d="M14 140 60 116l46 18 54-24 66 28 52-18 58 22v20H14z" fill="#2d6457"/>
<path d="M14 146h322v16H14z" fill="url(#sea)"/>
<path d="M30 152c12-4 24 4 36 0s24 4 36 0M190 156c12-4 24 4 36 0s24 4 36 0" stroke="#c9f3ec" stroke-width="1.6" fill="none" stroke-linecap="round"/>
{bld}
<text x="30" y="74" font-size="17" font-weight="850" fill="#0e1b26" font-family="system-ui" letter-spacing="-.5">{title}</text>
<text x="30" y="90" font-size="9" fill="#1d2f3d" font-family="system-ui">{sub}</text>
</g>
<rect x="14" y="174" width="96" height="10" rx="5" fill="#e6ecef"/><rect x="14" y="192" width="150" height="7" rx="3.5" fill="#eef2f4"/><rect x="14" y="205" width="130" height="7" rx="3.5" fill="#eef2f4"/>
<rect x="236" y="178" width="100" height="30" rx="15" fill="#0e1b26"/><text x="286" y="197" font-size="10" fill="#fff" text-anchor="middle" font-weight="700" font-family="system-ui">{btn}</text>
<rect x="14" y="222" width="322" height="16" rx="8" fill="#e6f6f3"/><text x="24" y="233" font-size="8" fill="#0f766e" font-weight="700" font-family="system-ui">\u2713 Certificate valid \u00b7 \u2713 Domain renewed \u00b7 \u2713 Backups OK \u00b7 \u2713 Online 24/7</text>
</g>
<g transform="translate(372 46)"><g class="float"><rect width="168" height="54" rx="14" fill="#fff"/><rect x="10" y="11" width="32" height="32" rx="10" fill="#e6f6f3"/><path d="M19 27l5 5 10-11" fill="none" stroke="#0f766e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><text x="52" y="25" font-size="10" font-weight="800" fill="#0e1b26" font-family="system-ui">Site rehosted</text><text x="52" y="39" font-size="8.5" fill="#55626d" font-family="system-ui">Secure \u00b7 fast \u00b7 monitored</text></g></g>
<g transform="translate(20 300)"><g class="float3"><rect width="190" height="62" rx="14" fill="#fff"/><rect x="10" y="12" width="36" height="36" rx="11" fill="#fde7e1"/>{chipic}<text x="56" y="28" font-size="10" font-weight="800" fill="#0e1b26" font-family="system-ui">{chip[0]}</text><text x="56" y="43" font-size="8.5" fill="#55626d" font-family="system-ui">{chip[1]}</text></g></g>
<g transform="translate(330 384)"><g class="float2"><rect width="200" height="62" rx="14" fill="#0e1b26"/><rect x="10" y="12" width="36" height="36" rx="11" fill="rgba(20,184,166,.2)"/><path d="M28 19l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z" fill="#14b8a6"/><text x="56" y="28" font-size="10" font-weight="800" fill="#fff" font-family="system-ui">3 reviews answered</text><text x="56" y="43" font-size="8.5" fill="#a9b8c3" font-family="system-ui">Drafted for your OK, 07:30</text></g></g>
</svg>'''

CTA_ART='''<svg viewBox="0 0 240 240" aria-hidden="true"><circle cx="120" cy="120" r="110" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="2"/><circle cx="120" cy="120" r="78" fill="none" stroke="rgba(20,184,166,.35)" stroke-width="2" stroke-dasharray="4 8"/><g transform="translate(60 60) scale(1.875)"><rect width="64" height="64" rx="16" fill="#14b8a6"/><path d="M45 22a16 16 0 1 0 3 14" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/><path d="M41 14l6 8-9 3" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><path d="M24 33l6 6 11-12" fill="none" stroke="#ffb199" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g></svg>'''

# Contact address, shown as plain text only (no email links; all contact goes through the Google Form)
CONTACT='cara@rehost.expert'

def head(title,desc,ogdesc):
    return f'''<!doctype html>
<html lang="en-IE" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="format-detection" content="telephone=no, email=no">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0e1b26">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{ogdesc}">
<meta property="og:type" content="website">
<link rel="icon" href="favicon.svg?v={VER}" type="image/svg+xml">
<link rel="stylesheet" href="style.css?v={VER}">
<script>document.documentElement.classList.remove('no-js')</script>
</head>
<body id="top">
<a class="skip" href="#main">Skip to content</a>'''

GFORM_ID='1FAIpQLSfOo1K7R60t8rfbQOhOktBgd1-iivUf306MHqamL8B0WoUY5g'
GFORM_URL=f'https://docs.google.com/forms/d/e/{GFORM_ID}/viewform'
GFORM_POST=f'https://docs.google.com/forms/d/e/{GFORM_ID}/formResponse'
# Google Form entry ids (from FB_PUBLIC_LOAD_DATA_ on the public viewform page)
GF_ENTRY={'name':'2115183178','biz':'842009210','email':'922822673','phone':'1982738485','site':'1405773933','help':'2019704753'}

def gf_post(fid):
    # hidden form + hidden iframe that POST straight to the Google Form (no relay, no email links)
    hid=''.join(f'<input type="hidden" name="entry.{GF_ENTRY[k]}" data-k="{k}">' for k in ('name','biz','email','phone','site','help'))
    return (f'<form id="{fid}-post" action="{GFORM_POST}" method="POST" target="{fid}-sink" hidden>{hid}'
            f'<input type="hidden" name="fvv" value="1"><input type="hidden" name="pageHistory" value="0"></form>'
            f'<iframe name="{fid}-sink" id="{fid}-sink" title="Sending" hidden tabindex="-1" aria-hidden="true"></iframe>')

def cfield(k,label,typ,ac,ph,wide=False):
    i='c-'+k
    im={'site':' inputmode="url" autocapitalize="off" spellcheck="false"','email':' autocapitalize="off" spellcheck="false"','phone':' inputmode="tel"'}.get(k,'')
    return (f'<div class="cf{" cf--wide" if wide else ""}"><label for="{i}">{E(label)} <span class="req" aria-hidden="true">*</span></label>'
            f'<input type="{typ}" id="{i}" name="{k}" autocomplete="{ac}"{im} placeholder="{E(ph)}" required aria-required="true" aria-describedby="{i}-err">'
            f'<p class="ferr" id="{i}-err" aria-live="polite" hidden></p></div>')

def cta(h2,p,pick_href):
    # Get in touch: native form that posts to the rehost.expert Google Form (answers land in its Sheet)
    fields=''.join([cfield('name','Your name','text','name','e.g. Mary Murphy'),
        cfield('biz','Business','text','organization','e.g. Murphy\u2019s Caf\u00e9'),
        cfield('email','Email address','email','email','you@yourbusiness.ie'),
        cfield('phone','Phone number','tel','tel','087 123 4567'),
        cfield('site','Website address','text','url','yourbusiness.ie',True)])
    return f'''<section class="section" id="contact" aria-labelledby="ct-h"><div class="wrap">
<div class="cta cta--contact rv"><div class="cta-copy"><span class="eyebrow" style="color:var(--sea-2)">Get in touch</span><h2 id="ct-h">{h2}</h2><p>{p}</p>
<ul class="cta-points" style="list-style:none;padding:0"><li>{I('check')}We look at your current site first</li><li>{I('check')}A personal reply from Cara</li><li>{I('check')}No obligation</li></ul>
<div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:22px"><a class="btn btn--ghost" href="{pick_href}" style="color:#fff">Pick your services</a></div>
</div>
<div class="ccard" id="c-card">
<form class="cform" id="c-form" novalidate aria-labelledby="c-title">
<div class="cform-head"><h3 id="c-title">Send us a message</h3><p class="req-note"><span class="req" aria-hidden="true">*</span> required</p></div>
<div class="cgrid">{fields}
<div class="cf cf--wide"><label for="c-help">How can we help? <span class="opt">(optional)</span></label><textarea id="c-help" name="help" rows="4" placeholder="Tell us what\u2019s going wrong, or what you\u2019d like your website to do."></textarea></div>
</div>
<p class="form-msg" id="c-msg" role="alert" hidden></p>
<button type="submit" class="btn btn--accent csend" id="c-send"><span class="csend-t">Send message</span>{I('arrow')}</button>
<p class="cform-alt">Prefer Google Forms? <a href="{GFORM_URL}" target="_blank" rel="noopener">Open the form</a></p>
</form>
<div class="cthanks" id="c-thanks" role="status" aria-live="polite" tabindex="-1" hidden><span class="cthanks-i">{I('check')}</span><div><h3>Thanks, we\u2019ve got your message.</h3><p>Cara will be in touch soon.</p><button type="button" class="linkbtn" id="c-again">Send another message</button></div></div>
{gf_post('c')}
</div></div>
</div></section>'''

def foot(line,home):
    return f'''<footer class="foot"><div class="wrap">{BRAND(home)}<span>{line}</span><span class="foot-mail">{CONTACT}</span><span>\u00a9 2026 rehost.expert</span></div></footer>
<script src="app.js?v={VER}"></script>
</body>
</html>
'''

# ================= HOME (generic) =================
HOME=head('rehost.expert \u00b7 Broken website? We rehost, fix and look after it',
 'rehost.expert rehosts and fixes broken websites for small businesses, looks after domain and certificate renewals, and takes the screen work off your desk: enquiries, social media, reviews and online admin.',
 'Website rescue, hosting and digital services for small businesses.')+f'''
<header class="top"><div class="wrap">{BRAND('#top')}
<nav class="menu" aria-label="Sections"><a href="#broken">Broken site?</a><a href="#services">Services</a><a href="#ai">AI consultation</a><a href="#sectors">Who it\u2019s for</a><a href="business.html">Business</a><a href="#packages">Packages</a><a class="btn btn--primary" href="#contact">Get in touch</a></nav></div></header>
<main id="main">
<section class="hero"><div class="wrap">
<div class="rv">
<span class="eyebrow">For small businesses, clubs and practices</span>
<h1>Your website, <span class="hl">back online</span> and looked after.</h1>
<p class="lead">Expired certificates, lapsed domains, crashed WordPress sites. We rehost and fix them, keep every renewal on track, and take the rest of the screen work off your desk, so you can get on with running your business.</p>
<div class="ctas"><a class="btn btn--primary" href="#broken">Is my site broken? {I('arrow')}</a><a class="btn btn--ghost" href="#services">Pick your services</a></div>
<div class="trust"><span>{I('lock')}Secure https on your own domain</span><span>{I('sync')}Renewals and backups handled</span><span>{I('handshake')}Month to month, no long contract</span></div>
</div>
<div class="hero-art rv">{hero_art('generic')}</div>
</div></section>

<section class="section" id="broken" aria-labelledby="br-h"><div class="wrap">
<div class="head rv"><span class="eyebrow">Is your website broken?</span><h2 id="br-h">Five ways a website quietly stops working.</h2><p class="lead">Most owners only find out when a customer mentions it. Here\u2019s what visitors actually see, and what we do about it.</p></div>
<div class="problems">{probs_html()}
<article class="prob rv" style="background:var(--ink);color:#e9eef2;border-color:var(--ink);justify-content:center"><div class="body" style="padding:30px"><span class="eyebrow" style="color:var(--sea-2)">The fix</span><h3 style="color:#fff;font-size:1.6rem;margin-top:10px">We rehost it, fix it, and keep it fixed.</h3><p style="color:#a9b8c3">Your site moves to fast, low-cost hosting on your own domain. Certificates, domain renewals and backups are tracked for you, and we check it from outside around the clock.</p><a class="btn btn--accent" href="#contact" style="background:var(--sea-2);color:var(--ink)">Get a site check {I('arrow')}</a></div></article>
</div>
<div class="how">
<div class="rv"><span class="n">1</span><b>Move</b><p>After reviewing your site we build you a new site, with your content and photos, and move it to new hosting, with the domain name management.</p></div>
<div class="rv"><span class="n">2</span><b>Fix</b><p>We install a valid certificate, repair or rebuild what\u2019s broken, and get you back on Google with a fast, mobile-friendly site.</p></div>
<div class="rv"><span class="n">3</span><b>Look after</b><p>We track domain and certificate renewals, back up the site, watch it 24/7, and make your changes within 2 working days.</p></div>
</div>
</div></section>

<section class="section section--sand" id="service" aria-labelledby="sv-h"><div class="wrap intro-grid">
<div class="rv"><span class="eyebrow">Our service</span><h2 id="sv-h" class="sr" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Our service</h2>
<blockquote>We look after your website, enquiries, social media and online admin. <em>You look after your customers.</em></blockquote>
<p class="lead" style="margin-top:22px">Running a small business means the screen work never stops: enquiries arriving late at night, reviews to answer, listings to keep current and renewals to remember. We take that off your desk and run it quietly in the background. Our systems monitor everything 24/7, so you can get on with everything else.</p>
<p class="muted">Everything is set up around how your business already works.</p></div>
<div class="pillars">
<div class="pillar rv">{I('globe')}<div><b>Website rescue and hosting</b><span>Rehosting, fixes and updates, with changes made when you ask</span></div></div>
<div class="pillar rv">{I('shield')}<div><b>Domain and certificate care</b><span>Renewals tracked, padlock always on, checked from outside every day</span></div></div>
<div class="pillar rv">{I('chat')}<div><b>Social media and reviews</b><span>Instagram, Facebook, Google and other reviews, with replies drafted for your OK</span></div></div>
<div class="pillar rv">{I('sun')}<div><b>WhatsApp morning summaries</b><span>One message a day with everything that needs you</span></div></div>
</div>
</div></section>

<section class="section section--ink" id="ai" aria-labelledby="ai-h"><div class="wrap">
<div class="ai-grid">
<div class="rv"><span class="eyebrow" style="color:var(--sea-2)">AI consultation</span><h2 id="ai-h">How could AI help your business?</h2>
<p class="lead">Book a consultation to talk through how AI and automation could help with the way your business already runs. We look at your day-to-day processes together, pick out the repetitive jobs, and talk plainly about where AI could help and where it wouldn\u2019t.</p>
<p style="color:#a9b8c3">You decide what, if anything, to go ahead with. Anything we set up drafts for your approval first, unless you ask otherwise.</p>
<div class="ctas"><a class="btn btn--accent" data-pick-ai href="#services" style="background:var(--sea-2);color:var(--ink)">{I('spark')}Book an AI consultation</a><span class="ai-price">AI consultation \u2014 Price on request</span></div>
</div>
<div class="ai-art rv">{ai_art()}</div>
</div>
<h3 class="ai-sub rv">Things we can look at together</h3>
<div class="ai-exs">{ai_ex_html}</div>
</div></section>

<section class="section" id="services" aria-labelledby="pk-h"><div class="wrap">
<div class="head rv"><span class="eyebrow">What we\u2019ll handle for you</span><h2 id="pk-h">{NUMW.get(N_CORE,N_CORE)} services and {'two' if N_ADD==2 else N_ADD} add-ons. Pick what you need.</h2><p class="lead">They\u2019re grouped by what they do for your business. Choose Yes, Maybe or No for each one. Your picks add up on the right, and you can email them to us in one click.</p></div>
<div class="picker">
<div id="svc-list">{svc_html()}</div>
<aside class="summary" aria-labelledby="sum-h" aria-live="polite">
<h3 id="sum-h">Your selection</h3>
<p class="muted" style="margin:0;color:#a9b8c3;font-size:.92rem" id="sum-sub">Nothing picked yet. Choose Yes, Maybe or No for each service.</p>
<div class="meter" aria-hidden="true"><i class="y" style="width:0"></i><i class="m" style="width:0"></i><i class="n" style="width:0"></i></div>
<div class="counts"><span><i class="dot" style="background:var(--sea-2)"></i>Yes <b id="c-yes">0</b></span><span><i class="dot" style="background:#f59e0b"></i>Maybe <b id="c-maybe">0</b></span><span><i class="dot" style="background:#7b8790"></i>No <b id="c-no">0</b></span><span>To decide <b id="c-left">{len(SV)}</b></span></div>
<div class="chosen" id="chosen"><p class="empty">Your Yes and Maybe picks will appear here.</p></div>
<div class="suggest" id="suggest" hidden></div>
<form id="sel-form" novalidate>
<p class="req-note"><span class="req" aria-hidden="true">*</span> required</p>
{contact_fields()}
<div class="fld"><label class="f" for="f-notes">Anything else? <span class="opt">(optional)</span></label><textarea id="f-notes" name="notes" rows="3" placeholder="Questions, deadlines, anything we should know"></textarea></div>
<p class="form-msg" id="form-msg" role="alert" hidden></p>
<button type="submit" class="btn btn--accent" id="send">{I('arrow')}Send my selection</button>
</form>
<p class="sel-thanks" id="sel-thanks" role="status" aria-live="polite" hidden>Thanks, your selection has been sent. We\u2019ll be in touch soon.</p>
{gf_post('sel')}
<button type="button" class="linkbtn" id="reset">Clear all choices</button>
</aside>
</div>
</div></section>

<section class="section section--sand" id="morning" aria-labelledby="mo-h"><div class="wrap morning">
<div class="rv"><span class="eyebrow">What your morning looks like</span><h2 id="mo-h">One message. Everything that needs you.</h2>
<p class="lead">Each day starts with one WhatsApp message that tells you what needs your attention. Here\u2019s an example.</p>
<div class="morning-points">
<div>{I('chat')}<span><b>Enquiries with replies ready</b><br><span class="muted">From your website, email, Facebook and Instagram. Drafted for your OK.</span></span></div>
<div>{I('cal')}<span><b>Today\u2019s bookings and orders</b><br><span class="muted">Appointments, collections or bookings from your systems.</span></span></div>
<div>{I('shield')}<span><b>Reviews and website health</b><br><span class="muted">New reviews to answer, and renewals coming up.</span></span></div>
</div>
<p class="muted">Everything else, such as spam, routine notifications and platform emails, is handled or filtered so you don\u2019t have to see it.</p></div>
<div class="rv">{phone(MORNING_G,'OK, send the quote reply \U0001f44d')}</div>
</div></section>

<section class="section" id="sectors" aria-labelledby="se-h"><div class="wrap">
<div class="head rv"><span class="eyebrow">Who it\u2019s for</span><h2 id="se-h">Built for any small business.</h2><p class="lead">The same services work for builders, trades, salons, shops, garages, clinics, offices, farms, tourism, clubs and hospitality. We set them up around how your business runs.</p></div>
<div class="sectors">{sectors_html()}</div>
<div class="ctas rv" style="margin-top:26px"><a class="btn btn--primary" href="business.html">See examples for 11 kinds of business {I('arrow')}</a></div>
</div></section>

<section class="section section--sand" id="packages" aria-labelledby="pa-h"><div class="wrap">
<div class="head rv"><span class="eyebrow">Packages</span><h2 id="pa-h">Three monthly packages. Add what you need.</h2><p class="lead">Three monthly packages, add-ons and an AI consultation, plus a one-off setup fee to build or move the site and connect your accounts. Prices are per month, excluding VAT.</p></div>
<div class="plans">{plans_html()}</div>
<div class="addons">{addons_html(ADDONS_G)}</div>
<div class="terms">
<div class="rv">{I('doc')}<span><b>One-off setup: \u20ac[&nbsp;&nbsp;]</b><span>Covers building or moving the website, connecting your accounts, and setting up your first pages.</span></span></div>
<div class="rv">{I('euro')}<span><b>Running costs at cost, no mark-up</b><span>Your domain name (roughly \u20ac15\u2013\u20ac30 a year) and any paid tools you choose, such as a WhatsApp Business account.</span></span></div>
<div class="rv">{I('handshake')}<span><b>No long contract</b><span>Month to month, with one month\u2019s notice either way.</span></span></div>
</div>
</div></section>

<section class="section section--ink" id="together" aria-labelledby="to-h"><div class="wrap">
<div class="head rv"><span class="eyebrow">How we\u2019ll work together</span><h2 id="to-h">You stay in control.</h2><p class="lead">You stay in control of your accounts and your customers\u2019 data at all times.</p></div>
<div class="together">{tog_html}</div>
</div></section>

<section class="section section--sand" id="next" aria-labelledby="nx-h"><div class="wrap next-grid">
<div class="stick rv"><span class="eyebrow">Next steps</span><h2 id="nx-h">From first chat to live site.</h2><p class="lead">A clear path, with you approving each stage.</p><a class="btn btn--primary" href="#contact">Book a consultation {I('arrow')}</a></div>
{next_html()}
</div></section>

{cta('Is your website broken, or just taking up too much of your time?','Tell us your website address and we\u2019ll check it. Then we\u2019ll talk through what you need, with no obligation.','#services')}
</main>
{foot('Website rescue, hosting and digital services for small businesses.','#top')}'''

# ================= HOSPITALITY =================
HSV=[('sync','Live availability calendar','Your website calendar stays in sync with Airbnb and Booking.com (or your booking system), so guests never see a date that\u2019s already taken. Updated every hour.'),
('list','Listing management','Airbnb and Booking.com listings, photos and guidebook kept accurate and up to date. Checked monthly, plus on request.'),
('map','Local guides with maps','Places to see, things to do, nearby attractions and experiences unique to the area, with a map. Guests plan longer stays, and the site shows up in more Google searches.'),
('cal','Local events calendar','A local events page guests can follow, with bank holidays marked. Updates automatically.'),
('star','TripAdvisor and Google reviews','New reviews flagged, replies drafted for your approval, and your TripAdvisor listing kept up to date.'),
('inbox','Guest inbox and social','Booking inbox sorted, enquiries answered with drafts for your OK, and posts for music nights, dinner specials and events.')]
hsv_html='\n'.join(f'<div class="tog rv">{I(i)}<b>{E(t)}</b><p>{E(d)}</p></div>' for i,t,d in HSV)
def hero_art_u(kind,suf):
    a=hero_art(kind)
    for i in ('arc','hc','sea','sky'): a=a.replace(f'id="{i}"',f'id="{i}{suf}"').replace(f'url(#{i})',f'url(#{i}{suf})').replace(f'href="#{i}"',f'href="#{i}{suf}"')
    return a
def ai_btn(name): return f'<a class="btn btn--accent" data-pick-ai href="index.html?pick=ai#services">{I("spark")}Book an AI consultation</a>'
EXAMPLES=[
('builders','hammer','Builders and construction','Builders, extensions, renovations and groundworks',
 'Quote requests, site photos and project updates, without the late nights at the laptop.',
 [('Quote draft','doc'),('Site photos','camera'),('Job schedule','cal'),('Invoice reminder','euro')],
 ['A site that shows recent projects, with before and after photos','A quote request form that asks for the job type, location, photos and timing','Your Google Business Profile and reviews looked after','Enquiries from phone, email and Facebook gathered into one morning message'],
 ['Drafting quotes from your site notes and price list, for you to check and send','Suggesting a week\u2019s job schedule from confirmed jobs, crew and deliveries','Replying to new enquiries with the first questions and a site visit time','Chasing unpaid invoices with polite reminders you approve','Turning site photos into customer updates and social posts']),
('trades','bolt','Electricians, plumbers and trades','Electricians, plumbers, heating engineers, painters and handymen',
 'Call-outs, quotes and service reminders sorted, so the phone isn\u2019t ringing while you\u2019re up a ladder.',
 [('Call-out request','inbox'),('Today\u2019s jobs','list'),('Service due','clock'),('Job invoice','euro')],
 ['Clear service areas, call-out details and opening hours','An online booking or call-back request form','Certifications and reviews shown where customers look','Google listing kept accurate, so the right number shows up'],
 ['Sorting enquiries by urgency and area, with replies drafted for you','\u201cOn my way\u201d and appointment reminder messages','Turning job notes into invoices, and chasing ones that are overdue','Reminding past customers when a boiler or alarm service is due','A daily summary of tomorrow\u2019s jobs and parts to pick up']),
('salons','scissors','Hair and beauty salons','Hairdressers, barbers, beauty and nail salons, spas',
 'A full diary and a quiet phone: bookings, reminders and messages that look after themselves.',
 [('New booking','cal'),('Reminder sent','mail'),('Waiting list','users'),('Instagram post','camera')],
 ['Online booking linked to your booking system','Price list, team and gallery pages that stay current','Instagram and Facebook kept active','Google and Facebook reviews answered'],
 ['Appointment reminders and rebooking prompts sent automatically','Answering messages about prices and free slots, with you checking anything unusual','Offering late cancellations to people on your waiting list','First drafts of posts from photos of your work','A morning summary of the day\u2019s bookings and gaps']),
('retail','shop','Retail shops','Gift shops, hardware, fashion, pharmacies and convenience stores',
 'Your shop open online too: hours, stock and offers kept current, and questions answered.',
 [('Stock reorder','basket'),('Product listing','tag'),('Customer question','chat'),('Weekly sales','chart')],
 ['Opening hours, offers and product pages kept current','Google Business Profile with products and photos','A simple online catalogue or click and collect','Reviews answered and seasonal posts planned'],
 ['Suggested stock reorders from till sales, approved by you before they go','Drafting product descriptions and offer posts','Answering \u201cdo you have this in stock?\u201d messages','A weekly sales and stock summary on WhatsApp','Supplier order emails drafted and sent once you approve']),
('garages','car','Garages and mechanics','Garages, mechanics, tyre centres and car valeting',
 'Bookings, estimates and \u201cyour car is ready\u201d messages, handled while you work.',
 [('Service booking','cal'),('NCT reminder','clock'),('Repair estimate','doc'),('Car ready','chat')],
 ['Services, opening hours and booking requests online','Google listing and reviews looked after','A clear page for NCT preparation and servicing','Enquiries from every channel in one place'],
 ['NCT and service due reminders to past customers','Booking requests turned into diary slots for you to confirm','Repair estimates drafted from your notes and parts prices','Parts orders worked out from booked jobs','\u201cYour car is ready\u201d and collection messages']),
('clinics','plus','Clinics and therapists','Physios, dentists, counsellors, vets and complementary therapists',
 'A calm, secure site and an appointment book that runs smoothly. AI is only used on admin, never on clinical decisions.',
 [('Appointment','cal'),('Reminder','mail'),('Forms','doc'),('Daily list','list')],
 ['A secure site with clear services, prices and directions','Online booking kept in sync with your diary','Privacy-friendly contact and intake forms','Google listing and reviews looked after'],
 ['Appointment reminders and rebooking prompts','Replies drafted to common questions about prices, parking and what to bring','Tidying the daily appointment list and invoices','Reminders for follow-up and review appointments','Everything kept private, with you approving what goes out']),
('professional','calc','Accountants and professional services','Accountants, solicitors, architects, engineers and consultants',
 'Fewer emails chasing paperwork, and a site that makes the right first impression.',
 [('Missing documents','doc'),('Deadline','clock'),('Inbox summary','inbox'),('Engagement letter','pen')],
 ['A professional site with services, team and contact pages','Enquiry forms that ask the right questions up front','LinkedIn and Google listings kept current','Secure hosting, renewals and backups looked after'],
 ['Chasing clients for missing documents before deadlines','Reminders before tax and filing dates','Sorting and summarising your inbox each morning','First drafts of standard letters and replies, for you to edit','Pulling details from emails into your spreadsheets or practice software']),
('farms','leaf','Farms and food producers','Farm shops, cheesemakers, bakers, growers and market traders',
 'Orders in from shops, restaurants and markets, all in one list, with deliveries planned.',
 [('Order list','list'),('Delivery round','map'),('Market day','cal'),('Invoice','euro')],
 ['A producer site with your story, products and where to buy','A markets and events calendar','A simple wholesale order form for shops and restaurants','Social posts for what\u2019s in season'],
 ['Gathering orders from email, phone and WhatsApp into one list','Suggesting a delivery round from the week\u2019s orders','Drafting posts and updates about stock and harvests','Invoice reminders to shops and restaurants','A weekly summary of orders, deliveries and payments']),
('tours','compass','Tour and activity operators','Tours, boat trips, kayaking, cycling, attractions and outdoor activities',
 'Bookings, weather changes and reviews handled, while you\u2019re out with the group.',
 [('Booking','cal'),('Weather check','sun'),('Guest reply','chat'),('Review reply','star')],
 ['Live availability and online booking','Clear meeting points, maps and what to bring','TripAdvisor and Google reviews looked after','Local area guides that help your site show up in searches'],
 ['Drafting reschedule messages when the weather changes plans','Replying to enquiries, including in the guest\u2019s own language','Review replies drafted for your approval','A daily summary of bookings, group sizes and guides','Reminder messages with meeting point and what to bring']),
('clubs','flag','Sports clubs and charities','Sports clubs, community groups, charities and festivals',
 'A site that doesn\u2019t depend on one volunteer, with the admin shared out.',
 [('Fixtures','cal'),('Renewal reminder','mail'),('Newsletter','pen'),('Volunteer rota','users')],
 ['Fixtures, events and news pages that stay up to date','Membership, registration and donation pages','A site handed over cleanly when committees change','Social posts for match days and events'],
 ['Membership renewal and payment reminders','Newsletters drafted from results and news','Volunteer and coaching rotas suggested and shared','First drafts of funding applications and reports, for you to edit','Replies drafted to common questions from parents and members'])]
def ex_art(eid,icon,title,chips):
    pos=[(14,26,'float'),(None,26,'float2'),(14,252,'float3'),(None,252,'float')]
    lines='';cs=''
    for (lab,ic),(x,y,cl) in zip(chips,pos):
        w=round(58+len(lab)*6.9)
        if x is None: x=480-14-w
        lines+=f'<path class="flow" d="M240 160 L{x+w//2} {y+22}" stroke="url(#exg-{eid})" stroke-width="2" stroke-dasharray="3 7" fill="none"/>'
        cs+=chipsvg(x,y,lab,cl,ic,w)
    return f'''<svg viewBox="0 0 480 320" role="img" aria-label="Illustration: {E(title)}, with AI helping on {E(', '.join(c[0] for c in chips))}">
<defs><linearGradient id="exg-{eid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14b8a6"/><stop offset="1" stop-color="#f26b4f"/></linearGradient>
<radialGradient id="exr-{eid}"><stop offset="0" stop-color="rgba(20,184,166,.32)"/><stop offset="1" stop-color="rgba(20,184,166,0)"/></radialGradient>
<linearGradient id="exc-{eid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14b8a6"/><stop offset="1" stop-color="#0f5f73"/></linearGradient></defs>
<circle cx="240" cy="160" r="130" fill="url(#exr-{eid})"/>
<circle class="spin" cx="240" cy="160" r="72" fill="none" stroke="rgba(20,184,166,.45)" stroke-width="1.5" stroke-dasharray="4 9"/>
{lines}
<g transform="translate(196 116)"><rect width="88" height="88" rx="24" fill="url(#exc-{eid})"/><svg x="20" y="20" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</svg>
<g transform="translate(70 -8)"><circle r="13" fill="#f26b4f"/><path d="M0-7l1.6 4.6L6.2-.8 1.6.8 0 5.4-1.6.8-6.2-.8-1.6-2.4z" fill="#fff"/></g></g>
{cs}
</svg>'''
def ex_html():
    o=[]
    for n,(eid,icon,title,who,lead,chips,do,ai) in enumerate(EXAMPLES):
        li=lambda L: '<ul class="ticks">'+''.join(f'<li>{I("check")}<span>{E(x)}</span></li>' for x in L)+'</ul>'
        o.append(f'''<section class="section ex-sec{' section--sand' if n%2==0 else ''}" id="{eid}" aria-labelledby="{eid}-h"><div class="wrap">
<div class="ex{' flip' if n%2 else ''}">
<div class="ex-art rv">{ex_art(eid,icon,title,chips)}</div>
<div class="rv"><span class="eyebrow">{I(icon)}Example {n+2} \u00b7 {E(title)}</span><h2 id="{eid}-h">{E(lead)}</h2><p class="muted">For {E(who[0].lower()+who[1:])}.</p></div>
</div>
<div class="ex-cols">
<div class="ex-col rv"><h3>{I('wrench')}What we\u2019d do</h3>{li(do)}</div>
<div class="ex-col ex-col--ai rv"><h3>{I('spark')}How AI can help</h3>{li(ai)}</div>
</div>
<div class="ctas rv">{ai_btn(title)}<a class="btn btn--ghost" href="#contact">Get in touch</a><a class="back" href="#jump">{I('list')}All examples</a></div>
</div></section>''')
    return '\n'.join(o)
JUMP=[('hospitality','bed','Hospitality')]+[(e[0],e[1],e[2]) for e in EXAMPLES]
jump_html='\n'.join(f'<a href="#{i}">{I(ic)}{E(t)}</a>' for i,ic,t in JUMP)
BUS=head('Business examples \u00b7 rehost.expert \u00b7 Websites, admin and AI help for small businesses',
 'rehost.expert for small businesses: examples for hospitality, builders, trades, salons, shops, garages, clinics, professional services, farms, tour operators, clubs and charities, with what we\u2019d do and how AI can help.',
 'Website rescue, admin and AI help for small businesses, with examples by type of business.')+f'''
<header class="top"><div class="wrap">{BRAND('index.html')}
<nav class="menu" aria-label="Sections"><a href="index.html">All services</a><a href="#jump">Examples</a><a href="#hospitality">Hospitality</a><a href="index.html#ai">AI consultation</a><a href="index.html#packages">Packages</a><a class="btn btn--primary" href="#contact">Get in touch</a></nav></div></header>
<main id="main">
<section class="hero"><div class="wrap">
<div class="rv">
<a class="crumb" href="index.html">{I('home')}rehost.expert</a><span class="crumb-sep" aria-hidden="true">/</span><span class="eyebrow" style="display:inline-flex">Business</span>
<h1>Small businesses, <span class="hl">looked after.</span></h1>
<p class="lead">Every business has its own screen work: quotes, bookings, orders, reminders and messages. Here\u2019s what we\u2019d do for different kinds of business, and how AI can help with the repetitive parts, with you approving anything that goes out.</p>
<div class="ctas"><a class="btn btn--primary" href="#jump">Find your business {I('arrow')}</a>{ai_btn('Business')}</div>
<div class="trust"><span>{I('shield')}Your site rescued and looked after</span><span>{I('spark')}AI drafts, you approve</span><span>{I('handshake')}Month to month, no long contract</span></div>
</div>
<div class="hero-art rv">{hero_art('generic')}</div>
</div></section>

<section class="section section--sand section--tight" id="jump" aria-labelledby="ju-h"><div class="wrap">
<div class="head rv"><span class="eyebrow">Examples</span><h2 id="ju-h">Jump to your kind of business.</h2><p class="lead">Don\u2019t see yours? The same services work for most small businesses. Book an AI consultation and we\u2019ll go through how you work.</p></div>
<nav class="jump rv" aria-label="Business examples">{jump_html}</nav>
</div></section>

'''+f'''<section class="hero hero--ex" id="hospitality" aria-labelledby="ho-h"><div class="wrap">
<div class="rv">
<span class="eyebrow">{I('bed')}Example 1 \u00b7 Hospitality</span>
<h2 class="h1" id="ho-h">Hotels, B&amp;Bs and restaurants, <span class="hl">looked after.</span></h2>
<p class="lead">We look after your website, bookings, guest messages and online admin. You look after the guests. Your site rehosted and fixed, calendars kept in sync, reviews answered, and food and drink orders built from your bookings.</p>
<div class="ctas"><a class="btn btn--primary" href="#morning">See a morning summary {I('arrow')}</a>{ai_btn('Hospitality')}<a class="btn btn--ghost" href="#contact">Get in touch</a></div>
<div class="trust"><span>{I('sync')}Airbnb and Booking.com in sync</span><span>{I('star')}Reviews answered</span><span>{I('handshake')}Month to month, no long contract</span></div>
</div>
<div class="hero-art rv">{hero_art_u('hotel','-h')}</div>
</div></section>

<section class="section section--sand" id="hosp-services" aria-labelledby="hs-h"><div class="wrap">
<div class="head rv"><span class="eyebrow">For hospitality</span><h2 id="hs-h">The screen work of a family hotel, handled.</h2><p class="lead">Enquiries arriving late at night, reviews to answer, orders to place and listings to keep current. We take that off your desk and run it quietly in the background, including the restaurant and bar.</p></div>
<div class="together light">{hsv_html}</div>
<p class="muted rv" style="margin-top:22px">No shared passwords: we\u2019re added as a co-host on Airbnb, a user on Booking.com, and a page admin on Facebook and Instagram. You can remove our access at any time. <a href="index.html#services">Choose these in the services picker</a>.</p>
</div></section>

<section class="section" id="morning" aria-labelledby="mo-h"><div class="wrap morning">
<div class="rv"><span class="eyebrow">What your morning looks like</span><h2 id="mo-h">One message. Everything that needs you.</h2>
<p class="lead">Each day starts with one WhatsApp message that tells you what needs your attention. Here\u2019s an example.</p>
<div class="morning-points">
<div>{I('cal')}<span><b>Bookings and today\u2019s arrivals</b><br><span class="muted">New bookings from every channel, check-ins and check-outs.</span></span></div>
<div>{I('chat')}<span><b>Enquiries with replies ready</b><br><span class="muted">Drafted for your OK. Reply in one tap.</span></span></div>
<div>{I('map')}<span><b>What\u2019s on locally</b><br><span class="muted">Walks, music and events your guests will ask about.</span></span></div>
</div>
<p class="muted">Everything else, such as spam, routine notifications and platform emails, is handled or filtered so you don\u2019t have to see it.</p></div>
<div class="rv">{phone(MORNING_H,'OK, send the reply to the family \U0001f44d')}</div>
</div></section>

<section class="section section--sand" id="ordering" aria-labelledby="or-h"><div class="wrap">
<div class="head rv"><span class="eyebrow">Add-ons</span><h2 id="or-h">Food and drink orders that build themselves.</h2><p class="lead">Orders are worked out from your bookings, updated as they change, and approved by you on WhatsApp before anything goes to a supplier.</p></div>
<div class="tabs" role="tablist" aria-label="Ordering automation">
<button role="tab" id="t-food" aria-controls="p-food" aria-selected="true">{I('basket')}Food ordering</button>
<button role="tab" id="t-drink" aria-controls="p-drink" aria-selected="false" tabindex="-1">{I('glass')}Drink ordering</button>
</div>
<div class="order" id="p-food" role="tabpanel" aria-labelledby="t-food">
<div><h3 style="font-size:1.6rem">Food ordering automation</h3>
<p>Your weekly food order is created automatically from your bookings and updates itself as bookings change, so you buy what you\u2019ll use and never run short.</p>
<p class="muted">Breakfast and welcome packs are planned from your bookings. Restaurant orders also use your till\u2019s sales history, so walk-in trade from locals and day visitors is included.</p>
{steps(FOOD_STEPS)}
<div class="note">{I('info')}<span>Bank holidays and big local events are flagged in advance, so busy weekends are ordered for early. Guest numbers come from the booking confirmation emails, not the calendar sync, so this works best alongside inbox management.</span></div></div>
<div class="tcard rv"><header><b>Example: one week\u2019s breakfast order</b><small>Next week: 10 double rooms, 7 nights (140 breakfasts)</small></header><div class="tscroll"><table><thead><tr><th scope="col">Item</th><th scope="col">Per breakfast (average)</th><th scope="col">Next week</th></tr></thead><tbody>{food_rows}</tbody></table></div></div>
</div>
<div class="order" id="p-drink" role="tabpanel" aria-labelledby="t-drink" hidden>
<div><h3 style="font-size:1.6rem">Drink ordering automation</h3>
<p>Your bar and drinks orders are planned from bookings and the time of year, so you\u2019re stocked for busy weekends without cash tied up in slow-moving stock.</p>
<p class="muted">Bar orders use both your bookings and your till\u2019s sales history, so walk-in trade from locals and day visitors is included.</p>
{steps(DRINK_STEPS)}</div>
<div class="tcard rv"><header><b>Example: how the season changes one week\u2019s order</b><small>Normal week compared with a bank holiday week</small></header><div class="tscroll"><table><thead><tr><th scope="col">Item</th><th scope="col">Normal week</th><th scope="col">Bank holiday week</th></tr></thead><tbody>{drink_rows}</tbody></table></div></div>
</div>
</div></section>

<section class="section" id="hosp-addons" aria-labelledby="ha-h"><div class="wrap">
<div class="head rv"><span class="eyebrow">Hospitality add-ons</span><h2 id="ha-h">Add to any package.</h2><p class="lead">The same three monthly packages apply to every business. These add-ons are popular with hotels, B&amp;Bs and restaurants. Prices are per month, excluding VAT.</p></div>
<div class="addons">{addons_html(ADDONS_H)}</div>
<div class="ctas rv" style="margin-top:26px"><a class="btn btn--primary" href="index.html#packages">See the packages {I('arrow')}</a><a class="btn btn--ghost" href="index.html#services">Pick your services</a><a class="back" href="#jump">{I('list')}All examples</a></div>
</div></section>

'''+f'''
{ex_html()}

{cta('Is your website holding your business back?','Tell us your website address and we\u2019ll check it. Then we\u2019ll talk through what you need, with no obligation.','index.html#services')}
</main>
{foot('Website rescue, hosting and digital services for small businesses. <a href="index.html">All services</a>','index.html')}'''
REDIRECT='''<!doctype html>
<html lang="en-IE"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><title>Hospitality \u00b7 rehost.expert</title>
<meta http-equiv="refresh" content="0; url=business.html#hospitality"><link rel="icon" href="favicon.svg?v=__VER__" type="image/svg+xml">
<script>location.replace('business.html#hospitality'+(location.search||''))</script></head>
<body><p>This page has moved to <a href="business.html#hospitality">Business examples: Hospitality</a>.</p></body></html>
'''
for fn,pg in (('index.html',HOME),('business.html',BUS),('hospitality.html',REDIRECT)):
    pg=pg.replace('__VER__',VER); open(OUTDIR+fn,'w').write(pg); print('wrote',fn,len(pg))
