from pathlib import Path
import math,json
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parents[1]; out=ROOT/'outputs'
st.set_page_config(page_title='ShopScope',layout='wide')
st.title('ShopScope | See the market. Sell smarter.')
st.caption('Historical proof of concept • 18 November 2025 • Not current market prices')
if not (out/'private/vietnam_analysis.csv').exists():
    st.error('Run python scripts/download_data.py and python scripts/run_notebook.py locally first.');st.stop()
d=pd.read_csv(out/'private/vietnam_analysis.csv',dtype={'shop_id':str,'product_id':str})
e=json.loads((out/'evidence.json').read_text())
view=st.sidebar.radio('Workspace',['Market overview','Product explorer','Pricing advisor'])
if view=='Market overview':
    a,b,c=st.columns(3);a.metric('Unique Vietnam listings',f"{e['vn_listings']:,}");b.metric('Observed shops',f"{e['vn_shops']:,}");c.metric('Historical median asking price',f"{e['vn_price_median']:,.0f} VND")
    st.image(str(out/'figures/03_price.png'));st.image(str(out/'figures/05_concentration.png'));st.info('Listing counts are not market share. Prices are historical.')
elif view=='Product explorer':
    q=st.text_input('Search listing title');brands=sorted(d.brand.dropna().unique())
    selected=st.multiselect('Recorded brand',brands)
    rows=d[d.title.fillna('').str.contains(q,case=False,regex=False)]
    if selected:rows=rows[rows.brand.isin(selected)]
    st.write(f'{len(rows):,} observed listings')
    st.dataframe(rows[['title','brand','price','quantity','size','type','unit_eligible']].head(200),hide_index=True)
else:
    st.subheader('Cost-aware pricing advisor')
    pool=d[d.unit_eligible & d.brand.notna() & d.title.notna()].copy()
    if pool.empty:st.warning('No eligible benchmark candidates.');st.stop()
    key=st.selectbox('Select a provisional product cohort',pool.title.drop_duplicates().sort_values())
    r=pool[pool.title.eq(key)]
    row=r.iloc[0]
    for col in ['brand','size','type','quantity']:r=r[r[col].eq(row[col])]
    prices=r.groupby('shop_id').price.median()
    cost=st.number_input('Total fixed cost per selling unit (VND)',min_value=1000,value=150000,step=1000)
    fee=st.slider('Variable fee (%)',0,40,12)/100; margin=st.slider('Target contribution margin (%)',0,50,20)/100
    floor=math.ceil(cost/(1-fee-margin)/1000)*1000
    st.metric('Minimum viable asking price',f'{floor:,} VND')
    st.caption('Candidate cohort requires human verification of product line, variant and pack.')
    if len(prices)<3:st.warning('ABSTAIN: fewer than three distinct comparable shops.')
    else:
        lo,med,hi=prices.quantile([.25,.5,.75]);st.write(f'{len(prices)} shops | historical IQR: {lo:,.0f}–{hi:,.0f} VND | median {med:,.0f} VND')
        p=math.ceil(max(floor,lo)/1000)*1000
        if p<=hi:st.success(f'Provisional test price: {p:,} VND. Verify SKU and refresh prices first.')
        else:st.warning('Cost floor exceeds feasible price band. Reduce costs or differentiate.')
