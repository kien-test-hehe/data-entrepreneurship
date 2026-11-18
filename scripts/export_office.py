"""Build English investor deck and report from the executed notebook, never from hand-entered EDA metrics."""
from pathlib import Path
import json, hashlib, math
from pptx import Presentation
from pptx.util import Inches as I, Pt as P
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from docx import Document
from docx.shared import Inches, Pt, RGBColor as DColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'; FIG=OUT/'figures'; REPORT=ROOT/'reports'
REPORT.mkdir(exist_ok=True)
E=json.loads((OUT/'evidence.json').read_text())
assert E['raw_observations']==24896 and E['unique_listings']==19686
N=E['vn_listings']; S=E['vn_shops']; finance=E['finance']; case=E['pricing_case']
def fmt(x): return f'{x:,.0f}' if x is not None else 'Not available'
def pct(x): return f'{x:.1%}'
NAVY='101B2D'; ORANGE='F56636'; TEAL='078C78'; WHITE='FFFFFF'; GRAY='64748B'; PALE='F4F6F8'; LIGHT='DDE5EB'
SOURCE='Easy Data, Shopee diaper snapshot, 18 Nov 2025 | ShopScope executed notebook'
MARKET='https://en.vcci.com.vn/economic-news/online-retail-sales-in-vietnam-jump-35-to-over-16-bln-in-2025-report-114817'
COMP='https://metric.vn/pricing'
EVIDENCE_ID=hashlib.sha256((OUT/'evidence.json').read_bytes()).hexdigest()[:12]
INS=[
 ('01_coverage','Six markets; one historical snapshot',f"{fmt(E['raw_observations'])} observations reduce to {fmt(E['unique_listings'])} unique listing keys. Vietnam contributes {fmt(N)} distinct listings.",'Start with Vietnam; use other markets for localization research, not demand comparisons.'),
 ('02_quality','Data quality is a product feature',f"{fmt(E['vn_price_conflicts'])} Vietnam listing keys have conflicting positive price observations; {fmt(E['vn_brand_known'])} have usable source brand labels.",'Show confidence and coverage; do not hide uncertainty or fill unknown attributes with guesses.'),
 ('03_price','A wide price band is not a price recommendation',f"Median observed asking price: {fmt(E['vn_price_median'])} VND (n={fmt(E['vn_valid_prices'])}); interquartile band {fmt(E['vn_price_q25'])}–{fmt(E['vn_price_q75'])} VND.",'Use this for orientation only. Compare equivalent product packs before deciding a selling price.'),
 ('04_brands','Brand presence reveals competitors',f"The most frequent usable raw brand label is {E['top_brand'] or 'unavailable'} ({fmt(E['top_brand_n'])} listings).",'Explore positioning within a brand; listing frequency is not market share or brand revenue.'),
 ('05_concentration','Competitive catalogs are uneven',f"The ten largest observed shops by listing count contribute {pct(E['top10_shop_share'])} of Vietnamese unique listings.",'Review these catalogs for assortment patterns; keep shop counts separate from company counts.'),
 ('06_brand_price','Control for product mix before pricing','Brand-level medians and interquartile ranges show observed price positions for sufficiently represented raw labels.','Do not interpret price differences as brand premiums without controlling for variants and pack sizes.'),
 ('07_popularity','Popularity is a signal, not a sales forecast',f"{fmt(E['popularity_n'])} listings have both usable prices and the source field {E['popularity_field']}.",'Investigate counter patterns; do not multiply the counter by asking price to claim revenue.'),
 ('08_eligibility','Reliable unit pricing requires abstention',f"Only {fmt(E['eligible_units'])} of {fmt(N)} listings pass the conservative title and single-price screen ({pct(E['eligible_units']/N)}).",'Confirm exact pack and variant manually. A smaller trustworthy benchmark is better than a broad misleading one.'),
 ('09_unit_price','Unit-price comparison can clarify value','The chart includes only brand groups with at least five eligible listings; all others are withheld.','Treat price-per-diaper estimates as indicative until a reviewer confirms the pack and selected variant.'),
 ('10_opportunity','Prioritize research, not inventory bets',f"{E['opportunity_segments']} segments pass the minimum size and shop thresholds. Top heuristic segment: {E['top_opportunity'] or 'none supported'}.",'Check supplier cost, product suitability and customer demand before committing capital.'),
 ('11_pricing_case','A recommendation must respect margin',f"Advisor result: {case['status']}. "+(f"Historical cohort: {case['brand']}, {case['size']}, {case['type']}, {case['quantity']} pieces; {case['shops']} shops. Cost assumption: {fmt(case['cost_assumption'])} VND; floor: {fmt(case['floor'])} VND." if 'shops' in case else (f"Broad {case['orientation_brand']} orientation: {case['orientation_shops']} shops; median {fmt(case['orientation_median'])} VND. Assumed cost floor {fmt(case['floor'])} VND. Not a matched SKU." if 'orientation_brand' in case else 'A reliable cross-shop exact-title cohort was not available.')),'Use a feasible test price, or reduce costs / differentiate. Verify the SKU and refresh market prices before acting.'),
 ('12_finance','Recurring revenue needs viable unit economics',f"At 99,000 VND/month, 20,000 VND variable cost and 20 million VND fixed monthly cost, operating break-even is {finance['breakeven']} paying accounts.",'Validate willingness to pay and actual licensing costs. This is an assumption-driven scenario, not traction.'),
 ('13_brand_agreement','Multimodal labels are not ground truth',f"{fmt(E['annotation_agreement'])} of {fmt(E['annotation_pairs'])} usable image/text annotation pairs agree.",'Route disagreements and missing labels to a reviewer; agreement does not establish correctness.'),
 ('14_repeats','Repeated observations are not extra products','Repeat-key rates differ by country because the collection uses overlapping filtered views.','Deduplicate keys before counting listings or comparing observed coverage.'),
 ('15_variant_risk','Variant ambiguity is a commercial bottleneck',f"{fmt(E['variant_status']['Single recorded price'])} of {fmt(N)} listings have an equal recorded price and min/max range.",'Request variant-level details; an equal range is necessary but not sufficient for SKU equivalence.'),
 ('16_variant_spread','The lowest displayed price can mislead',f"{fmt(E['variant_spread_gt_2'])} of {fmt(E['variant_spread_n'])} usable ranges have a maximum above twice the minimum.",'Do not compare listing minimums as if they represented identical quantities.'),
 ('17_opportunity_sensitivity','Opportunity scores need sensitivity checks',f"{E['opportunity_stable_top10']} brand segments stay in the top 10 under all three tested weights.",'Use stable candidates as interview priorities, not inventory recommendations.'),
 ('18_market_context','Market growth does not prove seller survival','External context: four-platform GMV grew 34.75% in 2025; active seller count declined 7.43%.','Test whether price intelligence addresses real seller pain; the macro trend is not causal evidence.'),
 ('19_cost_sensitivity','Data costs can change the break-even point','Illustrative scenarios vary monthly fixed cost and per-account servicing cost at a 99,000 VND subscription.','Obtain licensing and support quotes before committing to the business model.'),
 ('20_brand_shops','Brand presence spans multiple competitors',f"{E['brand_shop_leader'] or 'Unavailable'} has the most distinct observed shops ({fmt(E['brand_shop_leader_n'])}).",'Compare actual SKU portfolios and avoid interpreting this as market share.')

]
# Native editable slide elements, shared notebook charts (not manually rebuilt).
prs=Presentation(); prs.slide_width=I(13.333); prs.slide_height=I(7.5)
def color(s): return RGBColor.from_string(s)
def rect(sl,x,y,w,h,fill,round=False):
    sh=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round else MSO_SHAPE.RECTANGLE,I(x),I(y),I(w),I(h))
    sh.fill.solid();sh.fill.fore_color.rgb=color(fill);sh.line.fill.background()
    return sh
def txt(sl,x,y,w,h,s,size=20,fill=NAVY,bold=False,align=PP_ALIGN.LEFT):
    box=sl.shapes.add_textbox(I(x),I(y),I(w),I(h))
    tf=box.text_frame;tf.clear();tf.word_wrap=True
    tf.margin_left=tf.margin_right=I(.03);tf.margin_top=tf.margin_bottom=I(.02)
    for j,line in enumerate(str(s).split('\n')):
        p=tf.paragraphs[0] if j==0 else tf.add_paragraph()
        p.text=line;p.alignment=align;p.space_after=P(6)
        for r in p.runs:r.font.name='Aptos';r.font.size=P(size);r.font.bold=bold;r.font.color.rgb=color(fill)
    return box
def base(title,section,source='ShopScope | Proposed startup concept',dark=False):
    sl=prs.slides.add_slide(prs.slide_layouts[6])
    bg=sl.background.fill;bg.solid();bg.fore_color.rgb=color(NAVY if dark else WHITE)
    rect(sl,.52,.38,.10,.35,ORANGE)
    txt(sl,.73,.35,11.9,.35,section.upper(),12,ORANGE,True)
    txt(sl,.7,.88,12,1.03,title,33,WHITE if dark else NAVY,True)
    rect(sl,.7,7.07,11.9,.018,GRAY if dark else LIGHT)
    txt(sl,.7,7.13,11.4,.25,source+'  |  Evidence '+EVIDENCE_ID,9,'B8C5D2' if dark else GRAY)
    txt(sl,12,7.1,.6,.3,f'{len(prs.slides):02}',10,'B8C5D2' if dark else GRAY,align=PP_ALIGN.RIGHT)
    return sl
def cards(sl,items,top=2.18):
    gap=.24;w=(11.93-(len(items)-1)*gap)/len(items)
    for i,(k,v,b) in enumerate(items):
        x=.7+i*(w+gap);rect(sl,x,top,w,3.6,PALE,True)
        txt(sl,x+.22,top+.22,w-.44,.6,k,15,GRAY,True)
        txt(sl,x+.22,top+.97,w-.44,1.0,v,30 if len(v)<23 else 22,ORANGE,True)
        txt(sl,x+.22,top+2.05,w-.44,1.35,b,17,NAVY)
def narrative(sl,lines,top=2.1):
    for i,(k,v) in enumerate(lines):
        y=top+i*1.38
        rect(sl,.75,y,.12,.94,ORANGE)
        txt(sl,.98,y,3.12,.87,k,20,NAVY,True)
        txt(sl,4.15,y,8.1,1.12,v,19,NAVY)
def chart_slide(i,section='Evidence'):
    key,title,finding,action=INS[i]
    src='Illustrative assumptions | ShopScope executed notebook' if key in ('12_finance','19_cost_sensitivity') else ('Metric via VCCI, 19 Jan 2026 | external market context' if key=='18_market_context' else SOURCE)
    sl=base(title,section,src)
    img=FIG/(key+'.png')
    with Image.open(img) as im: w,h=im.size
    ww=min(7.55,4.55*w/h);hh=ww*h/w
    sl.shapes.add_picture(str(img),I(.75+(7.55-ww)/2),I(2.08+(4.55-hh)/2),width=I(ww),height=I(hh))
    rect(sl,8.58,2.18,4.02,4.43,PALE,True)
    txt(sl,8.82,2.4,3.54,.35,'WHAT THE DATA SAYS',12,ORANGE,True)
    txt(sl,8.82,2.86,3.54,1.55,finding,17,NAVY,True)
    txt(sl,8.82,4.56,3.54,.34,'SELLER ACTION',12,TEAL,True)
    txt(sl,8.82,5.02,3.54,1.35,action,15,NAVY)
    return sl
sl=base('See the market. Sell smarter.','SHOP SCOPE / 01',dark=True)
txt(sl,.8,2.1,8.9,1.15,'ShopScope',62,WHITE,True)
txt(sl,.85,3.35,7.6,1.65,'Pricing intelligence for small e-commerce sellers.\nVietnam first. Southeast Asia next.',26,'DDE5EB')
for i,(x,y,w,h) in enumerate([(9.3,4.55,.65,1.05),(10.15,3.75,.65,1.85),(11,2.9,.65,2.7),(11.85,2.25,.65,3.35)]):rect(sl,x,y,w,h,ORANGE if i==3 else TEAL)
txt(sl,.87,6.05,8,.48,'DATA ENTREPRENEURSHIP  •  PROOF OF CONCEPT',15,ORANGE,True)
sl=base('A small seller faces a big decision','Problem')
narrative(sl,[('What should I sell?','Thousands of fragmented listings make competitor research slow.'),('What is a fair price?','Pack size, diaper type and variants make raw price comparisons misleading.'),('Can I earn a margin?','Without a cost floor, a competitive price may be economically unsustainable.')])
sl=base('A growing market. A tougher game.','Market context','Metric, as reported by VCCI, 19 Jan 2026')
cards(sl,[('2025 FOUR-PLATFORM GMV','429.7T VND','Shopee, TikTok Shop, Lazada and Tiki'),('YEAR-ON-YEAR GMV','+34.75%','More opportunity, not a guarantee of seller success.'),('ACTIVE SELLERS','−7.43%','About 601,800 reported active sellers; pricing pain remains a hypothesis.')])
sl=base('Start with one customer and one decision','Beachhead')
narrative(sl,[('Customer','Small Vietnamese mother-and-baby seller, especially a new Shopee retailer.'),('Job to be done','Find comparable listings, assess historical price range and protect contribution margin.'),('Value proposition','Replace manual tab switching with explainable, confidence-aware decision support.')])
chart_slide(0,'Data foundation')
sl=base('From fragmented listings to a decision','Product architecture')
cards(sl,[('01 / INPUT','Raw listings','Clean keys, normalize fields, preserve uncertainty.'),('02 / INTELLIGENCE','Compare','Extract size and pack; rank similar titles within hard constraints.'),('03 / DECISION','Advise','Benchmark comparable shops; compare with a seller-specific cost floor.')])
chart_slide(1)
chart_slide(2)
chart_slide(4)
chart_slide(7)
sl=base('Find similar products. Admit uncertainty.','Matching engine',SOURCE)
m=E['matching']
cards(sl,[('ELIGIBLE POOL',fmt(m['eligible_pool']),'Attribute-constrained candidates; no claim of exact equivalence.'),('REVIEW QUEUE',fmt(m['candidate_pairs']),'Pairs produced for independent human labeling.'),('EVALUATION','Pending' if m['evaluation_status'].startswith('Not validated') else 'Reviewed','Exact title vs. char TF-IDF. '+m['evaluation_status'])])
chart_slide(12,'Trust and data quality')
chart_slide(9,'Opportunity discovery')
chart_slide(10,'Product demo')
sl=base('Experience the ShopScope proof of concept','Actual product interface',SOURCE)
ui=OUT/'mvp/overview.png'
with Image.open(ui) as im: uw,uh=im.size
uwidth=min(8.2,4.78*uw/uh);uheight=uwidth*uh/uw
sl.shapes.add_picture(str(ui),I(.75+(8.2-uwidth)/2),I(2.05+(4.78-uheight)/2),width=I(uwidth),height=I(uheight))
rect(sl,9.08,2.28,3.52,4.13,PALE,True)
txt(sl,9.3,2.55,3.06,.5,'LIVE PROTOTYPE',13,ORANGE,True)
txt(sl,9.3,3.03,3.06,2.0,'Six workspaces: overview, product search, competitor structure, price intelligence, opportunity finder and pricing advisor.',18,NAVY,True)
txt(sl,9.3,5.35,3.06,.9,'Actual historical dataset. No live feed or validated SKU equivalence claimed.',14,TEAL)
sl=base('A focused business, not another generic dashboard','Business model')
cards(sl,[('FREE','0 VND','Limited searches and educational benchmarks.'),('PRO','99k VND','Proposed monthly price: comparison and pricing advisor.'),('BUSINESS','299k VND','Future premium tier; not yet validated.')])
sl=base('Lean Canvas | a focused startup hypothesis','Business model')
canvas=[('PROBLEM','Manual research and variant ambiguity'),('CUSTOMER','Small online mother-and-baby sellers'),('VALUE','Actionable, margin-aware price intelligence'),('SOLUTION','Search, compare, check margin, abstain'),('CHANNELS','Seller communities and training partners'),('METRICS','Time saved, match precision, paid conversion'),('COSTS','Licensed data, hosting, support, development'),('REVENUE','Subscription and premium reports'),('ADVANTAGE','Potential localized reviewed matching labels')]
for i,(k,v) in enumerate(canvas):
    x=.7+(i%3)*4.02;y=2.12+(i//3)*1.44
    rect(sl,x,y,3.82,1.28,PALE,True)
    txt(sl,x+.16,y+.12,3.5,.32,k,12,ORANGE,True)
    txt(sl,x+.16,y+.49,3.5,.7,v,16,NAVY)
sl=base('Size the business in seller accounts, not GMV','Addressable market')
cards(sl,[('TAM CEILING','714.9B VND','Illustrative annualized ceiling: 601,800 reported seller accounts × 99k × 12; not a measured TAM.'),('SAM','To validate','Reachable small sellers in the initial category; no verified count.'),('SOM','Pilot first','Obtain 3 paid commitments, then measure acquisition and retention.')])
sl=base('Our position: simple, localized, decision-first','Competition','Metric pricing page | metric.vn/pricing | proposed ShopScope positioning')
narrative(sl,[('Metric / broad analytics','Established market and shop intelligence; Advanced list price is around 1.5M VND/month equivalent.'),('Seller Centre / sheets','Existing platform workflows and manual research; actual feature overlap requires user testing.'),('ShopScope / niche','Our proposed wedge is a lower-cost, SKU-level price workflow. Not proven differentiation yet.')])
sl=base('Test the business before scaling it','Lean startup')
cards(sl,[('PROBLEM','15 interviews','Target: 10/15 confirm repeated pricing pain. Owner: Business lead.'),('PRODUCT','10 paired tasks','Target: 50% faster median time with no quality loss. Owner: Product lead.'),('REVENUE','15 offers','Target: 3 paid-pilot commitments at 99k VND. Owner: Growth lead.')])
chart_slide(11,'Financial feasibility')
sl=base('A gated roadmap protects the startup','Execution')
narrative(sl,[('Now | classroom pilot','Run the historical proof of concept; complete seller interviews and reviewed product pairs.'),('Next | data rights & refresh','Negotiate licensed recurring data, validate unit economics and pilot with real sellers.'),('Later | expand','Add categories and countries only after matching, retention and recurring acquisition costs work.')])
sl=base('Build smarter. Sell better.','The ask',dark=True)
txt(sl,.85,2.1,11.3,1.2,'Join our first seller pilot.',46,WHITE,True)
txt(sl,.88,3.65,10.6,1.4,'We are seeking 15 small sellers to test the pricing workflow, plus a licensed data partner to validate recurring coverage.',27,'DDE5EB')
txt(sl,.9,5.65,10.8,.72,'ShopScope  /  Vietnam first. Evidence before scale.',21,ORANGE,True)
# Supplemental chart slides and source page.
for i in (3,5,6,8,13,14,15,16,17,18,19): chart_slide(i,'Appendix / analytical detail')
sl=base('Evidence and interpretation notes','Appendix / sources')
narrative(sl,[('Dataset','Easy Data, Shopee Diaper Listings: Six Markets, November 2025. Kaggle and publisher documentation; historical, filtered collection.'),('Market & competitor','VCCI (19 Jan 2026), Metric 2025 four-platform report; Metric public pricing page. See report for full URLs.'),('Status','No customer validation, licensed live feed or verified equivalent-SKU accuracy claimed. All financial assumptions are labeled.')])
# Speaker notes and a stand-alone rehearsal script, sourced from the same evidence.
core_notes=[
"Open with the seller decision: finding a price that is both competitive and sustainable. ShopScope turns marketplace information into an action, not just a report.",
"Imagine a small seller comparing diapers in multiple browser tabs. A lower package price may actually mean a higher price per diaper, and price without cost says nothing about margin. These pain points are hypotheses to validate.",
"External context: Metric reported 429.7 trillion VND of GMV across four platforms in 2025, up 34.75%, while active seller count fell 7.43%. This motivates research but does not prove our solution.",
"Start narrow: Vietnamese mother-and-baby sellers. The job is one recurring decision — compare offers and decide whether a proposed asking price is feasible.",
INS[0][2]+" "+INS[0][3],
"Explain the pipeline simply: clean listing keys, identify product attributes, retrieve candidates, and combine a price benchmark with a seller-specific cost floor.",
INS[1][2]+" "+INS[1][3],
INS[2][2]+" "+INS[2][3],
INS[4][2]+" "+INS[4][3],
INS[7][2]+" "+INS[7][3],
f"We generated {m['candidate_pairs']} candidate pairs; {m['exact_title_candidates']} have identical normalized titles. No verified precision or recall is reported until people review the actual products.",
INS[12][2]+" "+INS[12][3],
INS[9][2]+" "+INS[9][3],
INS[10][2]+" "+INS[10][3],
"Show the actual Streamlit interface. Start with market overview, explore a brand, then enter cost and margin in Pricing Advisor. The system abstains if it cannot find adequate evidence.",
"The proposed subscription price is 99,000 VND per month; free and future premium tiers are hypotheses. We do not claim existing paying users.",
"Walk through Lean Canvas. The key link is customer pain → useful decision → measurable seller value → recurring subscription. Data rights and acquisition cost are essential assumptions.",
"Market sizing should count potential customer accounts, not diaper GMV. The broad TAM ceiling is purely illustrative; SAM and SOM require verified eligible accounts and conversion evidence.",
"Existing tools are credible alternatives. Our differentiation is proposed focus and affordability, not a claim of superior breadth. Interviews must test this.",
"Three experiments: validate the problem with 15 interviews, test 10 paired tasks, and offer a paid pilot to 15 sellers. No results have been fabricated.",
INS[11][2]+" "+INS[11][3],
"Do not scale first. Complete reviewed matching pairs, seller experiments, and licensed data sourcing, then expand only if unit economics and retention support it.",
"Close with an evidence-led ask: recruit 15 sellers and a data partner. We are building a responsible price decision workflow, not promising profit."
]
notes=core_notes+[INS[i][2]+" "+INS[i][3] for i in (3,5,6,8,13,14,15,16,17,18,19)]+["Reference the original Kaggle release, publisher documentation, VCCI market context, and Metric pricing. All analytical charts share the notebook evidence bundle."]
assert len(notes)==len(prs.slides)
for slide,note in zip(prs.slides,notes):slide.notes_slide.notes_text_frame.text=note
(REPORT/'ShopScope_Pitch_Script.md').write_text('# ShopScope | English rehearsal script\n\n23 core slides; appendices for questions. Suggested timing: 12–15 minutes. Evidence ID: '+EVIDENCE_ID+'\n\n'+'\n\n'.join(f'## Slide {i+1:02d}\n\n{n}' for i,n in enumerate(notes)),encoding='utf-8')
ppt=REPORT/'ShopScope_Startup_Pitch.pptx';prs.save(ppt)

# Consulting-style Word report. Page-break controlled sections; charts share the notebook files.
doc=Document(); sec=doc.sections[0];sec.page_width=Inches(8.27);sec.page_height=Inches(11.69)
sec.top_margin=Inches(.72);sec.bottom_margin=Inches(.7);sec.left_margin=sec.right_margin=Inches(.75)
normal=doc.styles['Normal']; normal.font.name='Aptos';normal.font.size=Pt(12);normal.font.color.rgb=DColor.from_string(NAVY);normal.paragraph_format.space_after=Pt(9);normal.paragraph_format.line_spacing=1.16
for nm,sz,col in [('Title',38,NAVY),('Heading 1',25,NAVY),('Heading 2',15,TEAL),('Heading 3',12,ORANGE)]:
    style=doc.styles[nm];style.font.name='Aptos';style.font.size=Pt(sz);style.font.bold=True;style.font.color.rgb=DColor.from_string(col)
h=sec.header.paragraphs[0];h.alignment=WD_ALIGN_PARAGRAPH.RIGHT;r=h.add_run('SHOPSCOPE   /   DATA ENTREPRENEURSHIP');r.font.size=Pt(9);r.font.color.rgb=DColor.from_string(ORANGE)
foot=sec.footer.paragraphs[0];foot.alignment=WD_ALIGN_PARAGRAPH.RIGHT;r=foot.add_run('Historical proof of concept  •  '+EVIDENCE_ID+'  |  ');r.font.size=Pt(9);r.font.color.rgb=DColor.from_string(GRAY)
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');foot._p.append(field)
def para(s,style=None): return doc.add_paragraph(s,style)
def heading(s):doc.add_heading(s,level=1)
def sub(s):doc.add_heading(s,level=2)
def page(s):doc.add_page_break();heading(s)
def table(headers,rows):
    t=doc.add_table(rows=1,cols=len(headers));t.style='Light Shading Accent 1'
    for c,k in zip(t.rows[0].cells,headers):c.text=str(k)
    for row in rows:
        for c,v in zip(t.add_row().cells,row):c.text=str(v)
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                p.paragraph_format.space_after=Pt(4)
                for r in p.runs:r.font.size=Pt(10)
    return t
def figure(i):
    key,title,finding,action=INS[i]
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(FIG/(key+'.png')),width=Inches(6.55))
    p=para('Figure '+str(i+1)+'. '+title+' — '+('Illustrative financial assumptions.' if key in ('12_finance','19_cost_sensitivity') else ('Metric via VCCI, 19 Jan 2026; external context.' if key=='18_market_context' else SOURCE)));p.runs[0].font.size=Pt(9);p.runs[0].italic=True
    para(finding);sub('Business implication');para(action)
para('DATA ENTREPRENEURSHIP  /  STARTUP BUSINESS PLAN')
p=doc.add_heading('ShopScope',0); p.paragraph_format.space_before=Pt(70); p.paragraph_format.space_after=Pt(20)
p=para('See the market. Sell smarter.');p.runs[0].font.size=Pt(24);p.runs[0].font.color.rgb=DColor.from_string(ORANGE)
para('A data-driven market intelligence platform for small e-commerce sellers in Southeast Asia — Vietnam diaper category proof of concept.')
para('Business strategy • Data analytics • Decision support • Lean startup validation')
para('November 2026 | Source snapshot: November 18, 2025')
table(['Proof-of-concept scope','Computed evidence'],[['Raw observations',fmt(E['raw_observations'])],['Unique listing keys',fmt(E['unique_listings'])],['Vietnam listings / shops',f'{fmt(N)} / {fmt(S)}'],['Evidence ID',EVIDENCE_ID]])
para('Independent academic project. Not affiliated with or endorsed by Shopee. Customer research and commercial data rights remain open.')
page('Executive summary')
para('ShopScope proposes a focused subscription service that helps small sellers compare product offers and set a margin-aware asking price. Its starting point is the Vietnamese mother-and-baby category: a bounded use case where pack quantities, variants and brand labels complicate comparison. The commercial hypothesis is that sellers will value a faster, clearer decision workflow rather than an additional general-purpose dashboard.')
para(f"The executed notebook processed {fmt(E['raw_observations'])} historical observations across six markets, resolving them into {fmt(E['unique_listings'])} distinct listing keys. The Vietnam analysis covers {fmt(N)} listings and {fmt(S)} shop IDs. The median recorded asking price is {fmt(E['vn_price_median'])} VND, but it should not be interpreted as a comparable-SKU recommendation.")
para(f"Only {fmt(E['eligible_units'])} listings meet the conservative unit-price screen. This is a commercially relevant finding: a product that makes uncertainty explicit can avoid false comparisons. Candidate retrieval and the margin advisor are technical proof-of-concept components, not proven customer traction.")
para('The proposed Pro price is VND 99,000 per month. The next decision is not immediate scale; it is to recruit a seller pilot, independently review matching candidates, and determine the cost and permission for a refreshed data feed. The report separates computed dataset evidence, external market context and business assumptions.')
sub('Reading guide')
table(['Part','Coverage'],[['I. Strategy','Market, customer, product and competition'],['II. Evidence','Ingestion, quality, prices, brands, sellers and opportunity signals'],['III. Execution','MVP, revenue, financial feasibility, validation and risks']])
page('1. Market opportunity and customer')
para('Vietnam provides a practical first market because the team can recruit local sellers and interpret Vietnamese product titles. According to Metric as reported by VCCI on 19 January 2026, four major marketplaces recorded 429.7 trillion VND GMV in 2025 (+34.75% year-on-year), while reported active online sellers declined by 7.43% to approximately 601,800. This establishes market context, not a causal proof that pricing intelligence prevents seller exits.')
sub('Target customer and job to be done')
para('The early adopter is an owner-operated mother-and-baby online retailer who needs to evaluate a supplier offer, compare competing packs and decide whether an asking price can meet a margin target. An illustrative persona is Linh, a seller who manages sourcing, pricing and fulfillment herself. Her pain points are hypotheses that must be tested, not interview findings.')
table(['Problem hypothesis','Proposed decision value'],[['Fragmented competitor listings','Reduce time spent collecting prices'],['Inconsistent pack and variant information','Avoid incorrect unit-price comparisons'],['Uncertain costs and platform fees','Calculate minimum viable asking price'],['Limited analysis budget','Test affordable subscription economics']])
sub('Beachhead and expansion')
para('Vietnam is the beachhead, not the entire serviceable market. The five other workbooks support exploratory localization research. Expansion requires language-specific parsing, currency separation, current licensed data and new customer interviews.')
page('2. Product design and value proposition')
para('Unique value proposition: turn marketplace data into smarter selling decisions. The product is a decision workflow rather than a collection of unrelated charts.')
table(['Workflow stage','User action and output'],[['Find','Search by title, brand, size, diaper type and pack quantity.'],['Compare','Review constrained candidates and distinct-shop price range.'],['Check','Inspect data freshness, matching reliability and missing attributes.'],['Decide','Enter costs, variable fees and target contribution margin.'],['Act','Test a feasible asking price or reconsider sourcing and differentiation.']])
sub('Architecture')
para('Original workbooks → validation and deduplication → normalized product attributes → candidate retrieval → price benchmarking → margin-aware recommendation → Streamlit interface.')
sub('Why this is a data product')
para('The underlying value is not the raw marketplace file. The transformation from inconsistent listings into a constrained, explainable pricing decision can save effort and reduce avoidable mistakes. The system abstains when evidence is inadequate rather than inventing an answer.')
sub('Minimum viable scope')
para('The local MVP focuses on market overview, listing exploration and the pricing advisor. Live crawling, payments, automated repricing, and broader geographic expansion are deliberately excluded until rights and customer value are established.')
page('Product interface | Actual prototype')
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(str(OUT/'mvp/overview.png'),width=Inches(6.65))
p=para('Product screenshot. Actual local Streamlit Market Overview; generated from the executed notebook evidence.');p.runs[0].font.italic=True;p.runs[0].font.size=Pt(9)
sub('How the six workspaces support decisions')
table(['Workspace','Seller decision'],[['Market Overview','Orient to historical price and seller structure'],['Product Explorer','Search the observed catalog and inspect attributes'],['Competitor Analysis','Identify observed seller and brand concentration'],['Price Intelligence','Compare price ranges and variant risk'],['Opportunity Finder','Prioritize research by brand segments'],['Pricing Advisor','Check a margin-aware price floor; abstain when evidence is insufficient']])
para('The application is a working local prototype. It does not provide verified live prices or automated repricing; the commercial product requires data rights, updated feeds and user testing.')
page('3. Dataset and reproducibility')
para('Easy Data released six Excel workbooks containing a historical collection dated November 18, 2025. All files use the Multi-Modal Comparison worksheet; Indonesia has 46 source columns and the other five have 47. The source contains filtered and sales-sorted collection views, so coverage is not representative of complete national demand.')
table(['Market','Observations','Unique keys','Shop IDs'],[[r['market'],fmt(r['observations']),fmt(r['listings']),fmt(r['shops'])] for r in E['coverage']])
sub('Reproducibility contract')
para('The notebook validates expected counts, imports identifiers as text, preserves original values, maps source fields by name, and records SHA-256 hashes for all six workbooks. It exports charts, CSV tables and evidence.json. The report and deck are generated from that evidence bundle; no analytical numbers are copied manually.')
para('Raw files, listing-level exports and candidate review queues remain local because the publisher does not specify unrestricted reuse rights. The repository distributes analysis code and aggregate artifacts only.')
page('4. Regional coverage')
figure(0)
page('5. Data quality and deduplication')
figure(1)
para('Repeated listing keys are not physical product duplicates. For a conflicting field, the notebook retains the listing identity but excludes that field from the affected analysis. Missing attributes remain missing. No foreign currency is converted or compared directly.')
page('6. Vietnam pricing landscape')
figure(2)
para('The distribution uses positive, non-conflicting recorded asking prices, not checkout totals. Variant ranges, promotions and bundle composition may change the final unit purchased. The interquartile range is descriptive, not an optimal price interval.')
page('7. Recorded brand landscape')
figure(3)
para('Raw source brand labels may include inconsistent naming or product-line labels. The analysis preserves these limitations and does not report verified brand shares.')
page('8. Competitive seller structure')
figure(4)
para('Shop IDs are unique within a market. Listing concentration is based on distinct observed listing keys, not company-level revenue or sales share. Seller research should inspect relevant product catalogs rather than blindly copy the most visible shops.')
page('9. Price positioning by brand')
figure(5)
page('10. Popularity proxies')
figure(6)
para('The snapshot cannot establish a calendar-month transaction count, seasonality, sales velocity or causal price elasticity. No revenue estimate is computed from asking price multiplied by source counters.')
page('11. Product comparability and unit price')
figure(7)
para('An explicit quantity token, a unique size and diaper type, a single observed price and absence of detected bundles are required for automatic eligibility. This is a conservative heuristic and may still miss ambiguity; manual variant confirmation is required.')
page('12. Indicative unit price')
figure(8)
para('Unit price = recorded asking price / explicit pack quantity. The result is used only when the screening conditions are met; it is not a guarantee of selected-variant checkout price.')
page('13. Multimodal annotation reliability')
figure(12)
para('The image-based and text-based labels were generated by the data publisher. Exact normalized agreement is a useful consistency check but is not a measured classification accuracy. Future human review should include cases where the two sources agree as well as disagree.')
page('14. Matching experiment')
para('Exact normalized titles form a strict baseline. Character n-gram TF-IDF ranks candidates within identical recorded brand, type, size and pack quantity, excluding the same shop. These candidates are provisional; they may differ in product line or physical variant.')
table(['Measure','Computed result'],[['Eligible candidate pool',m['eligible_pool']],['Candidate pairs queued',m['candidate_pairs']],['Exact-title candidates',m['exact_title_candidates']],['Accuracy evaluation status',m['evaluation_status']]])
sub('Evaluation design')
para('Two reviewers should label up to 300 candidate pairs as equivalent, non-equivalent or unclear, using title and packaging evidence. Resolve disagreements before calculating precision, recall on reviewed candidates and F1. A candidate-only sample cannot estimate full-catalog retrieval recall; a separately labeled query set is necessary for that claim. Avoid leakage by keeping listing keys separate across evaluation and tuning.')
sub('Release gate')
para('Require at least 90% precision on a held-out reviewed subset, with coverage and abstention rate reported. This is a target, not an achieved metric. Until it is met, display candidates as review-required rather than verified equivalents.')
page('15. Opportunity discovery')
figure(9)
para('Segments are grouped by recorded source brand (minimum 20 listings and three distinct shops). The heuristic averages relative popularity rank and inverse observed competitor-count rank. The score is exploratory and depends on the sampling design, the minimum segment support and the selected weights. It should guide interviews and sourcing checks, not inventory purchase.')
page('16. Margin-aware pricing advisor')
figure(10)
sub('Decision rule')
para('Minimum viable price = fixed cost per selling unit / (1 − variable fee rate − target contribution margin). Round up to the nearest 1,000 VND. Compare the floor with the historical interquartile price band, require three distinct comparable shops, and abstain when there is insufficient evidence. Costs, fee rates and margin targets are user inputs, not inferred seller profits.')
page('17. Lean Canvas and competitive positioning')
table(['Canvas element','ShopScope hypothesis'],[['Problem','Manual research, misleading comparisons and uncertain margin'],['Customer segments','Small Vietnamese online sellers; initial mother-and-baby category'],['Unique value proposition','Actionable, confidence-aware pricing intelligence'],['Solution','Product candidate matching, benchmarks and cost floor'],['Channels','Seller groups, training partners and direct outreach'],['Revenue streams','Monthly subscriptions; optional advanced reports'],['Cost structure','Data acquisition, development, hosting, support and marketing'],['Key metrics','Time saved, match precision, activation, conversion, retention'],['Potential advantage','Localized labels and seller feedback accumulated with permission']])
sub('Alternatives and differentiation')
para('Metric and YouNet ECI provide established market intelligence; Seller Centre and spreadsheets are common workflow alternatives. Metric’s public Advanced plan lists around 1.5 million VND/month equivalent, though packages and prices vary. ShopScope proposes a narrower low-cost decision workflow, not feature parity. Interviews must establish whether the difference matters.')
page('18. Business model and addressable market')
para('The proposed freemium strategy offers limited educational searches, a 99,000 VND/month Pro tier and a future 299,000 VND/month Business tier. These are willingness-to-pay hypotheses, not confirmed prices.')
table(['Tier','Price hypothesis','Value'],[['Free','0 VND','Limited exploration'],['Pro','99,000 VND/month','Comparisons and pricing advisor'],['Business','299,000 VND/month','Future multi-category reports']])
sub('TAM, SAM and SOM')
para('Use customer accounts rather than diaper GMV. The reported 601,800 active marketplace sellers is an external upper-bound starting point, not a count of unique eligible businesses. A purely illustrative ceiling at 99,000 VND/month is approximately 714.9 billion VND annualized, before removing duplicate or ineligible accounts. SAM requires a validated count of reachable small mother-and-baby sellers; SOM requires acquisition and retention evidence. No precise SAM or SOM is asserted.')
sub('Go-to-market')
para('Recruit sellers through local seller communities and direct outreach. Offer a guided pricing task and a paid pilot. Track activation, pilot conversion, acquisition cost and repeat usage before committing to paid marketing.')
page('19. Financial feasibility')
figure(11)
table(['Scenario','Paid accounts','MRR (VND)','Monthly operating result'],[[r['scenario'],fmt(r['paid_accounts']),fmt(r['mrr']),fmt(r['monthly_operating_result'])] for r in finance['scenarios']])
para('Assumes constant accounts and costs; excludes taxes and financing. No CAC, churn or LTV is fabricated. Quote recurring data rights and delivery costs before using these scenarios for investment decisions.')
page('20. Test Cards and validation plan')
para('No customer interviews, paid pilots or task experiments have been completed. The following experiments define measurable success and decision gates.')
table(['Test','Recruit / method','Metric and threshold','Owner / review'],[['Problem','15 active sellers; interviews','10/15 report recurring pain','Business lead / Week 1'],['Product','10 sellers; counterbalanced manual vs. prototype task','Median time down ≥50%; no quality loss','Product lead / Week 3'],['Revenue','15 target sellers; paid pilot offer','≥3 actual paid commitments','Growth lead / Week 4']])
sub('Interview and experiment controls')
para('Recruit active sellers rather than classmates posing as customers. Ask about the most recent pricing decision, time spent, existing tools, fees and consequences. Avoid leading questions. Use the same comparable-product tasks in both conditions, counterbalance order and measure decision accuracy using a reviewed reference. Obtain consent and retain only anonymous respondent IDs.')
sub('Decision after review')
para('If the problem threshold fails, revisit the segment. If the product task fails, improve matching and explanation. If the paid-pilot threshold fails, revisit price, packaging or target customer. The test result matters more than an attractive pitch.')
page('21. Roadmap, risks and investment gate')
table(['Milestone','Evidence required'],[['Foundation','Repeatable dataset audit and provenance'],['Proof of concept','Executed notebook and cost-aware local MVP'],['Customer pilot','Completed tests and reviewed matching labels'],['Commercial readiness','Licensed recurring data feed, actual cost model and privacy review'],['Expansion','Retention and reliable localized matching in the initial category']])
sub('Key risks and mitigations')
para('Data freshness: all market evidence is historical; secure a lawful update path. Coverage bias: source filters and sales sorting limit generalization. Product ambiguity: show confidence and abstain. Commercial risk: validate paid demand and data acquisition cost before scale. Privacy: avoid collecting unnecessary customer identifiers and do not publish raw listing or survey data.')
sub('Recommendation')
para('Proceed with a controlled Vietnam pilot, not a full commercial launch. The proof of concept demonstrates a reproducible transformation of marketplace observations into decision-support signals. The next investment should buy evidence: verified product comparisons, real customer tasks and a sustainable data license.')
# Compact analytical appendix: two charts per page where possible.
def small_figure(i):
    key,title,finding,action=INS[i]
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(FIG/(key+'.png')),width=Inches(4.9))
    p=para('Figure '+str(i+1)+'. '+title+' — '+('Illustrative scenario.' if key=='19_cost_sensitivity' else ('External context: Metric via VCCI.' if key=='18_market_context' else SOURCE)))
    p.runs[0].font.size=Pt(9);p.runs[0].italic=True
    para(finding)
page('Appendix A. Collection and variant risk')
small_figure(13);small_figure(14)
page('Appendix B. Price dispersion and robustness')
small_figure(15);small_figure(16)
page('Appendix C. Market and cost sensitivity')
small_figure(17);small_figure(18)
page('Appendix D. Brand competition')
small_figure(19)
para('Use distinct shop counts as a second lens alongside listing counts. A brand with many observed shops may have broader distribution, but this snapshot cannot establish verified market penetration.')
page('References and evidence provenance')
for s in [f"Easy Data. (2025). Shopee Diaper Listings: Six Markets, November 2025. Kaggle. {E['source_url']}",f"Easy Data. Marketplace Datasets and Data Quality Guides. {E['publisher_url']}",f"VCCI. (2026, January 19). Online retail sales in Vietnam jump 35% to over $16 bln in 2025: report. {MARKET}",f"Metric. Public service pricing. {COMP}",'ShopScope. Executed Jupyter notebook, evidence.json and generated figures. Evidence ID: '+EVIDENCE_ID]:para(s)
sub('Source file checksums')
for f in E['files']:para(f["file"]+" | "+str(f["rows"])+" rows | SHA-256 "+f["sha256"])
docx=REPORT/'ShopScope_Business_Report.docx';doc.save(docx)
# Structural and evidence consistency checks. Rendering is performed separately in CI.
assert len(Presentation(ppt).slides)==35
assert len(Document(docx).inline_shapes)==21
assert len(E['figures'])==20
print(f'Created {ppt.name} ({len(prs.slides)} slides), {docx.name} (20 shared charts and actual MVP screenshot). Evidence {EVIDENCE_ID}')
