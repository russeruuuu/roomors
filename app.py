"""Local hotel analytics workspace. Run: streamlit run app.py."""
from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import streamlit as st
from dashboard_utils import wilson_interval, queue_summary
from sklearn.metrics import roc_curve, precision_recall_curve

ROOT = Path(__file__).resolve().parent
INK, BLUE = '#172B4D', '#3478F6'
HOTEL_COLORS = {'City Hotel': BLUE, 'Resort Hotel': INK}
st.set_page_config(page_title='Roomors · Hotel Booking Analytics', page_icon='▦', layout='wide')
st.markdown('''<style>
:root{--ink:#172B4D;--blue:#3478F6;--muted:#65748B;--line:#E5E9F0}
html,body,[class*="css"],.stApp,input,button,textarea,select{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
.stApp{background:#EDF2FA;color:var(--ink)}
.stApp p,.stApp h1,.stApp h2,.stApp h3,.stApp button,.stApp label,.stApp input,.stApp [data-baseweb="tab"]{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif!important}
[class*="st-key-panel-"]{background:#FFF!important;border-radius:16px!important;border-color:#E5E9F0!important}
.stMainBlockContainer{max-width:1600px;padding:4.5rem 2.5rem 3rem}
[data-testid="stHeader"]{background:rgba(245,246,248,.92);border-bottom:1px solid var(--line)}
[data-testid="stToolbar"]{visibility:hidden}
section[data-testid="stSidebar"]{background:#172B4D;border-right:0}
section[data-testid="stSidebar"] .stVerticalBlock{gap:.8rem}
h1,h2,h3,p,label{color:var(--ink)!important}
h1{font-size:2rem!important;letter-spacing:-.06rem;font-weight:650!important;padding:0!important}
h2{font-size:1.2rem!important;letter-spacing:-.02rem}
h3{font-size:1.05rem!important;font-weight:600!important;letter-spacing:-.01rem}
[data-testid="stCaptionContainer"] p{color:#52627A!important;opacity:1;font-size:.82rem;line-height:1.55}
[data-testid="stMetric"]{background:#FFFFFF;border:1px solid var(--line);padding:19px 20px;border-radius:14px;box-shadow:0 3px 10px rgba(23,43,77,.025)}
[data-testid="stMetricLabel"] p{font-size:.8rem!important;color:var(--muted)!important;font-weight:500}
[data-testid="stMetricValue"]{font-family:"SFMono-Regular",Consolas,monospace!important;font-size:1.65rem!important;letter-spacing:-.07rem;color:var(--ink);font-weight:500}
[data-testid="stVerticalBlockBorderWrapper"]>div{border-color:var(--line)!important;border-radius:16px!important;background:#FFF}
.stTabs [data-baseweb="tab-list"]{gap:6px;background:#E9EDF3;border-radius:11px;padding:4px;width:fit-content;margin:12px 0 20px;border-bottom:0}
.stTabs [data-baseweb="tab"]{height:36px;border-radius:8px;padding:0 20px;color:var(--muted);font-size:.88rem}
.stTabs [aria-selected="true"]{background:#FFF;color:var(--ink)!important;box-shadow:0 1px 5px rgba(23,43,77,.10)}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none}
[data-baseweb="select"]>div,[data-baseweb="input"],.stDateInput input{border-radius:9px!important}
[data-baseweb="tag"]{background:#DFE9FC!important;color:var(--ink)!important}
.stButton button,.stDownloadButton button{border-radius:9px;border:1px solid #DDE3EC;font-weight:500;font-size:.85rem}
.stButton button:hover,.stDownloadButton button:hover{border-color:var(--blue);color:var(--blue)}
.brand{display:flex;align-items:center;gap:10px;margin:6px 0 25px;font-size:15px;font-weight:650;letter-spacing:-.3px}
.brand-icon{display:grid;place-items:center;width:34px;height:34px;border-radius:10px;background:#3478F6;color:white;font-size:20px}
.eyebrow{font-size:10px;font-weight:650;letter-spacing:1.7px;color:#65748B;margin-bottom:8px}
.status{display:inline-block;border:1px solid #DFE6F1;background:#EDF3FF;color:#172B4D;border-radius:20px;padding:6px 11px;font-size:11px;font-weight:500}
.insight{padding:13px 16px;border-left:3px solid #3478F6;background:#EDF3FF;border-radius:0 9px 9px 0;color:#172B4D;font-size:13px;line-height:1.65;margin:8px 0 20px}
.footer{font-size:11px;color:#65748B;border-top:1px solid #E5E9F0;margin-top:28px;padding-top:15px}
@media(max-width:900px){.stMainBlockContainer{padding:4.5rem 1rem 2rem}h1{font-size:1.6rem!important}[data-testid="stMetric"]{padding:12px}[data-testid="stMetricValue"]{font-size:1.3rem!important}.stTabs [data-baseweb="tab"]{padding:0 12px}}

section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{padding-top:12px}
.st-key-filter-panel{background:#FFF;border:1px solid rgba(255,255,255,.2);border-radius:16px;padding:18px 16px 20px;box-shadow:0 10px 30px rgba(0,0,0,.10)}
.st-key-filter-panel [data-testid="stDateInput"] input{font-size:12px!important;padding-left:8px!important;padding-right:4px!important}
.st-key-filter-panel [data-testid="stCaptionContainer"] p{font-size:12px;color:#52627A!important}
.st-key-filter-panel [data-baseweb="select"]>div,.st-key-filter-panel [data-baseweb="input"]{background:#F3F6FC;border:1px solid #DCE4F0}
.st-key-segment-list .stVerticalBlock{gap:0!important}
.st-key-segment-list [data-testid="stCheckbox"] label p{font-size:13px!important}
.st-key-filter-panel [data-testid="stExpander"] .stButton button{background:#EDF3FF;border:1px solid #DCE4F0;color:#172B4D!important;min-height:34px;font-size:12px}
.st-key-filter-panel [data-testid="stExpander"] .stButton button p{color:#172B4D!important;font-size:12px}
.st-key-filter-panel .stButton button{background:#3478F6;border-color:#3478F6;color:white!important;min-height:40px}
.st-key-filter-panel .stButton button p{color:white!important}
.side-brand{display:flex;gap:12px;align-items:center;color:#FFF;margin:8px 2px 26px;font-size:19px;font-weight:650;letter-spacing:-.5px}
.side-brand small{display:block;color:#BDCCE3;font-size:11px;font-weight:400;letter-spacing:.2px;margin-top:4px}
.side-symbol{display:grid;place-items:center;background:#3478F6;border:1px solid #6C9DF9;border-radius:12px;width:42px;height:42px;font-size:24px}
.filter-title{font-size:16px;font-weight:650;color:#172B4D;margin:0 0 4px}
.filter-subtitle{font-size:12px;color:#52627A;line-height:1.5;margin-bottom:16px}
.sidebar-foot{padding:22px 6px;color:#BDCCE3;font-size:12px;line-height:1.8}
.sidebar-foot strong{color:white;font-weight:500}
.hero{background:linear-gradient(115deg,#172B4D 0%,#244B8A 58%,#3478F6 100%);border:1px solid #294F89;border-radius:20px;padding:30px 32px 26px;margin-bottom:22px;box-shadow:0 10px 30px rgba(23,43,77,.12);color:white}
.hero-top{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:20px}
.hero-eyebrow{font-size:10px;font-weight:600;letter-spacing:1.8px;color:#D4E1F7}
.hero-badge{font-size:11px;white-space:nowrap;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.24);padding:6px 10px;border-radius:20px;color:#FFF}
.hero h1{color:#FFF!important;font-size:30px!important;font-weight:650!important;letter-spacing:-1px;margin:0 0 10px!important}
.hero-description{color:#DFE9FA;font-size:14px;line-height:1.6;margin-bottom:24px}
.hero-scope{display:flex;flex-wrap:wrap;gap:10px;border-top:1px solid rgba(255,255,255,.17);padding-top:18px}
.hero-scope span{color:#FFF;font-size:12px;padding:5px 11px;background:rgba(255,255,255,.10);border-radius:7px}
[data-testid="stMetric"]{border-top:3px solid #3478F6}
.stTabs [aria-selected="true"]{background:#3478F6!important;color:#FFF!important}
.stTabs [aria-selected="true"] p{color:#FFF!important}
@media(max-width:900px){.hero{padding:24px 22px}.hero-top{align-items:flex-start}.hero h1{font-size:25px!important}.hero-description{font-size:13px}.hero-badge{font-size:10px}}


.st-key-headline-kpis [data-testid="stHorizontalBlock"]{flex-wrap:wrap!important}
.st-key-headline-kpis [data-testid="stColumn"]{flex:1 1 155px!important;min-width:155px!important}
[data-testid="stMetricLabel"] p{white-space:normal!important}
@media(max-width:1150px){
.stTabs [data-testid="stHorizontalBlock"]:has([class*="st-key-panel-"]){flex-wrap:wrap!important}
.stTabs [data-testid="stHorizontalBlock"]:has([class*="st-key-panel-"])>[data-testid="stColumn"]{flex:1 1 320px!important;min-width:0!important}
.hero{padding:24px!important}.hero-top{flex-wrap:wrap}.hero h1{font-size:25px!important}
}

</style>''', unsafe_allow_html=True)

@st.cache_data
def load():
    return (pd.read_csv(ROOT/'data/hotel_bookings_analysis.csv',parse_dates=['arrival_date','booking_date']),
            pd.read_csv(ROOT/'results/heldout_predictions.csv',parse_dates=['arrival_date','booking_date']),
            json.loads((ROOT/'results/summary.json').read_text()))
try:
    df, pred, summary = load()
    pred['review_reference'] = ['R-' + str(i+1).zfill(6) for i in range(len(pred))]
except FileNotFoundError:
    st.error('Data is not ready. Run python analysis.py, then reopen the dashboard.'); st.stop()

SEGMENTS = sorted(df.market_segment.unique())

def set_segments(selected):
    for name in SEGMENTS:
        st.session_state[f'segment::{name}'] = selected

def reset_filters():
    st.session_state['hotels'] = sorted(df.hotel.unique())
    set_segments(True)
    st.session_state['dates'] = (df.arrival_date.min().date(),df.arrival_date.max().date())

with st.sidebar:
    st.markdown('<div class="side-brand"><span class="side-symbol">▦</span><div>Roomors<small>HOTEL ANALYTICS</small></div></div>',unsafe_allow_html=True)
    with st.container(key='filter-panel'):
        st.markdown('<div class="filter-title">Filter bookings</div><div class="filter-subtitle">Choose the records you want to explore. Your view updates automatically.</div>',unsafe_allow_html=True)
        hotels = st.multiselect('Hotel properties', sorted(df.hotel.unique()), default=sorted(df.hotel.unique()),key='hotels',format_func=lambda name:name.replace(' Hotel',''))
        dates = st.date_input('Arrival period',value=(df.arrival_date.min().date(),df.arrival_date.max().date()),min_value=df.arrival_date.min().date(),max_value=df.arrival_date.max().date(),key='dates',format='DD/MM/YYYY')
        for name in SEGMENTS:
            st.session_state.setdefault(f'segment::{name}', True)
        selected_count = sum(st.session_state[f'segment::{name}'] for name in SEGMENTS)
        with st.expander('Market segments',expanded=False):
            st.caption('Choose segments to include.')
            select_all, clear = st.columns(2)
            select_all.button('All',help='Select all market segments',key='segments-all',on_click=set_segments,args=(True,),use_container_width=True)
            clear.button('Clear',key='segments-clear',on_click=set_segments,args=(False,),use_container_width=True)
            with st.container(height=300,border=False,key='segment-list'):
                for name in SEGMENTS:
                    st.checkbox(name,key=f'segment::{name}')
            segments = [name for name in SEGMENTS if st.session_state[f'segment::{name}']]
        st.caption('All market segments included' if len(segments)==df.market_segment.nunique() else f'{len(segments)} of {df.market_segment.nunique()} segments included')
        st.button('Reset all filters',on_click=reset_filters,use_container_width=True)
    st.markdown('<div class="sidebar-foot"><strong>Your analysis workspace</strong><br>Filters apply to the overview and follow-up queue. Model evaluation uses a fixed test set.<br><br>Group 4.2 · Enriquez &amp; Patron</div>',unsafe_allow_html=True)

period = f'{dates[0]:%d %b %Y} - {dates[1]:%d %b %Y}' if len(dates)==2 else 'Choose an arrival period'
hotel_scope = 'Both properties' if len(hotels)==2 else (hotels[0] if hotels else 'No properties selected')
segment_scope = 'All market segments' if len(segments)==df.market_segment.nunique() else f'{len(segments)} market segments'
st.markdown(f'''<div class="hero"><div class="hero-top"><span class="hero-eyebrow">RESERVATION INTELLIGENCE</span><span class="hero-badge">Historical analysis · 2015-2017</span></div><h1>Roomors</h1><div class="hero-description">Every booking tells a story.<br>Hotel booking analytics and cancellation risk prioritization.</div><div class="hero-scope"><span>{period}</span><span>{hotel_scope}</span><span>{segment_scope}</span></div></div>''',unsafe_allow_html=True)
if len(dates)!=2:
    st.info('Choose a start and end date to view bookings.');st.stop()
d = df[df.hotel.isin(hotels)&df.market_segment.isin(segments)&df.arrival_date.between(pd.Timestamp(dates[0]),pd.Timestamp(dates[1]))].copy()
if d.empty:
    st.info('No bookings match your filters. Select another hotel or segment, or reset the filters.');st.stop()
with st.container(key='headline-kpis'):
    for col,label,value in zip(st.columns(5),['Bookings','Canceled bookings','Cancellation rate','Median lead time','Median daily rate'],[f'{len(d):,}',f'{d.is_canceled.sum():,}',f'{d.is_canceled.mean():.1%}',f'{d.lead_time.median():.0f} days',f'{d.adr.median():.2f}']):
        col.metric(label,value)
st.caption('Rates are in dataset units. Booking volume includes cancellations and does not measure occupancy or realized revenue.')
overview, performance, queue_tab=st.tabs(['Overview','Model performance','Follow-up queue'])

def grouped(column):
    g=d.groupby(column,observed=True).is_canceled.agg(Bookings='size',Canceled='sum',Rate='mean').reset_index()
    g['Cancellation rate (%)']=g.Rate*100
    low, high = wilson_interval(g.Canceled, g.Bookings)
    g['Lower 95% (%)'] = low*100
    g['Upper 95% (%)'] = high*100
    return g

def chart(fig,height=300):
    fig.update_layout(template='plotly_white',height=height,paper_bgcolor='white',plot_bgcolor='white',
                      font=dict(family='-apple-system, BlinkMacSystemFont, Segoe UI, Arial, sans-serif',size=12,color=INK),
                      margin=dict(l=12,r=18,t=18,b=15),colorway=[BLUE,INK],
                      legend=dict(orientation='h',y=1.12,x=0,title_text=''),hoverlabel=dict(bgcolor='white',font_color=INK),
                      modebar=dict(bgcolor='white',color=INK,activecolor=BLUE))
    fig.update_xaxes(showgrid=False,zeroline=False,title_font_size=11,tickfont_size=11,automargin=True)
    fig.update_yaxes(gridcolor='#EDF0F5',zeroline=False,title_font_size=11,tickfont_size=11,automargin=True)
    st.plotly_chart(fig,use_container_width=True,theme=None,config={'displayModeBar':False})

def card_title(title,subtitle):
    st.subheader(title);st.caption(subtitle)

with overview:
    st.markdown(f'<div class="insight"><b>At a glance</b> · {int(d.is_canceled.sum()):,} of {len(d):,} selected bookings were canceled ({d.is_canceled.mean():.1%}). Use the comparisons below to decide where to focus reservation reviews.</div>',unsafe_allow_html=True)
    a,b=st.columns(2,gap='medium')
    with a,st.container(border=True,key="panel-0"):
        card_title('Cancellation by hotel','Which property has higher cancellation exposure?')
        g=grouped('hotel')
        fig=px.bar(g,x='hotel',y='Cancellation rate (%)',color='hotel',color_discrete_map=HOTEL_COLORS,hover_data=['Bookings','Canceled'],text=g['Cancellation rate (%)'].map(lambda v:f'{v:.1f}%'))
        fig.update_layout(showlegend=False);fig.update_traces(textposition='outside',cliponaxis=False,width=.46);fig.update_xaxes(title=None);fig.update_yaxes(range=[0,max(10,g['Cancellation rate (%)'].max()*1.2)])
        chart(fig)
        row=g.sort_values('Rate',ascending=False).iloc[0]
        st.caption(f'{row.hotel}: {row.Rate:.1%} canceled across {int(row.Bookings):,} records. Compare volume before assigning follow-up capacity.')
    with b,st.container(border=True,key="panel-1"):
        card_title('Cancellation by segment','Which booking channels need a closer look?')
        all_segments=grouped('market_segment').sort_values('Rate')
        small_segments=all_segments[all_segments.Bookings<30]
        g=all_segments[all_segments.Bookings>=30].copy()
        if not g.empty:
            fig=px.bar(g,x='Cancellation rate (%)',y='market_segment',orientation='h',color_discrete_sequence=[BLUE],hover_data={'Bookings':True,'Canceled':True,'Lower 95% (%)':':.1f','Upper 95% (%)':':.1f'},text=g['Cancellation rate (%)'].map(lambda v:f'{v:.1f}%'))
            fig.update_traces(textposition='outside',cliponaxis=False);fig.update_yaxes(title=None);fig.update_xaxes(range=[0,max(10,g['Cancellation rate (%)'].max()*1.2) if not g.empty else 10])
            chart(fig)
        else:
            st.info('No selected segment has at least 30 records. See the small-sample table below; these groups still count toward the KPIs.')
        if not small_segments.empty:
            st.caption('Groups with fewer than 30 records are listed separately to avoid unstable rankings. Hover over bars for counts and 95% intervals.')
            with st.expander('Small-sample groups'):
                st.dataframe(small_segments[['market_segment','Bookings','Canceled','Cancellation rate (%)']],hide_index=True,width='stretch')
        named=g[(g.market_segment!='Undefined')&(g.Bookings>=30)]
        if not named.empty:
            row=named.iloc[-1];st.caption(f'{row.market_segment} leads among named segments with 30+ records ({row.Rate:.1%}; n={int(row.Bookings):,}). Investigate the booking mix before changing channel policy.')
        else:st.caption('Selected groups have fewer than 30 records. Treat their cancellation rates cautiously.')
    a,b=st.columns(2,gap='medium')
    with a,st.container(border=True,key="panel-2"):
        card_title('Booking activity','How does recorded arrival demand change over time?')
        x=d.assign(month=d.arrival_date.dt.to_period('M').dt.to_timestamp()).groupby('month').is_canceled.agg(Bookings='size',Rate='mean').reset_index();x['Cancellation rate (%)']=x.Rate*100
        fig=px.area(x,x='month',y='Bookings',color_discrete_sequence=[BLUE],hover_data=['Cancellation rate (%)'])
        fig.update_traces(line_width=2,fillcolor='rgba(52,120,246,.10)');fig.update_xaxes(title=None);chart(fig)
        row=x.loc[x.Bookings.idxmax()];st.caption(f'{row.month:%b %Y} has the most selected records ({int(row.Bookings):,}). Review staffing and confirmation workload around busy arrival periods. These counts are not occupancy; partial years limit seasonal conclusions.')
    with b,st.container(border=True,key="panel-3"):
        card_title('Booking lead time','Does advance notice relate to cancellation?')
        d['Lead-time group']=pd.cut(d.lead_time,[-1,7,30,90,180,365,float('inf')],labels=['0-7','8-30','31-90','91-180','181-365','366+'])
        g=grouped('Lead-time group')
        fig=px.bar(g,x='Lead-time group',y='Cancellation rate (%)',hover_data=['Bookings','Canceled'],color_discrete_sequence=[INK],text=g['Cancellation rate (%)'].map(lambda v:f'{v:.1f}%'))
        fig.update_traces(textposition='outside',cliponaxis=False);fig.update_xaxes(title='Days before arrival');fig.update_yaxes(range=[0,max(10,g['Cancellation rate (%)'].max()*1.2)]);chart(fig)
        if len(g):
            high_row=g.loc[g.Rate.idxmax()];low_row=g.loc[g.Rate.idxmin()]
            st.caption(f'{high_row["Lead-time group"]} days has the highest selected cancellation rate ({high_row.Rate:.1%}; n={int(high_row.Bookings):,}), compared with {low_row.Rate:.1%} for {low_row["Lead-time group"]} days. Prioritize confirmation review, while comparing group sizes. This is association, not causation.')
    a,b=st.columns(2,gap='medium')
    with a,st.container(border=True,key="panel-4"):
        card_title('Daily rate distribution','How do typical rates compare across properties?')
        high=d.adr.quantile(.99);view=d[d.adr.between(0,high)]
        fig=px.box(view,x='hotel',y='adr',points=False,color='hotel',color_discrete_map=HOTEL_COLORS,labels={'adr':'Daily rate · dataset units'})
        fig.update_layout(showlegend=False);fig.update_xaxes(title=None);chart(fig)
        st.caption(f'The selected median daily rate is {d.adr.median():.2f}. Use medians to compare typical rates and investigate extremes before financial estimates. The display shows 0-{high:.2f}; {len(d)-len(view):,} records are hidden only in this plot. KPIs retain all rows.')
    with b,st.container(border=True,key="panel-5"):
        card_title('Cancellation over time','When do property-level patterns differ?')
        h=d.assign(Month=d.arrival_date.dt.to_period('M').astype(str)).groupby(['hotel','Month']).is_canceled.mean().unstack()*100
        fig=px.imshow(h,aspect='auto',color_continuous_scale=['#EDF3FF',BLUE,INK],labels={'color':'Cancellation (%)'})
        monthly_counts=d.assign(Month=d.arrival_date.dt.to_period('M').astype(str)).groupby(['hotel','Month']).size().unstack().reindex(index=h.index,columns=h.columns)
        fig.update_traces(customdata=monthly_counts.to_numpy(),hovertemplate='Hotel: %{y}<br>Arrival month: %{x}<br>Cancellation rate: %{z:.1f}%<br>Bookings: %{customdata:,.0f}<extra></extra>')
        fig.update_xaxes(title=None,tickangle=-45);fig.update_yaxes(title=None);fig.update_layout(coloraxis_colorbar=dict(thickness=10,len=.8));chart(fig)
        highest=h.stack().idxmax();st.caption(f'{highest[0]} in {highest[1]} has the highest selected monthly rate ({h.loc[highest]:.1f}%; n={int(monthly_counts.loc[highest]):,}). Review this period and hover for counts before acting; small groups can be unstable. Blank cells have no records.')
    st.download_button('Export filtered bookings',d.drop(columns=['Lead-time group'],errors='ignore').to_csv(index=False),'selected_bookings.csv','text/csv')

with performance:
    st.subheader('Model performance')
    st.caption('Fixed chronological test set · Classification threshold 0.50 · Sidebar filters do not change these results')
    m=pd.read_csv(ROOT/'results/model_metrics.csv');test=m[m.split=='test'].copy();selected=test[test.model==summary['selected_model']].iloc[0]
    st.markdown(f'<div class="insight"><b>{summary["selected_model"]}</b> was selected on validation average precision. The test period starts {summary["cutoff_test"]}. These results describe historical performance.</div>',unsafe_allow_html=True)
    for c,k,label in zip(st.columns(4),['roc_auc','average_precision','precision','recall'],['ROC-AUC','Average precision','Precision','Recall']):c.metric(label,f'{selected[k]:.3f}')
    st.info(f'At the fixed threshold, the selected model identifies {int(selected.tp):,} of {int(selected.tp+selected.fn):,} test cancellations and misses {int(selected.fn):,}. It also flags {int(selected.fp):,} bookings that did not cancel. Use this as a prioritization aid, not an automatic cancellation decision.')
    a,b=st.columns(2)
    with a,st.container(border=True,key="panel-6"):
        card_title('Compare models','Test ranking quality · higher is better')
        v=test.melt(id_vars='model',value_vars=['roc_auc','average_precision'],var_name='Metric',value_name='Score');v.Metric=v.Metric.map({'roc_auc':'ROC-AUC','average_precision':'Average precision'})
        fig=px.bar(v,x='Score',y='model',color='Metric',orientation='h',barmode='group',color_discrete_sequence=[INK,BLUE]);fig.update_yaxes(title=None);fig.update_xaxes(range=[0,1]);chart(fig,330)
    with b,st.container(border=True,key="panel-7"):
        card_title('What influences the ranking?','Validation permutation importance · predictive association')
        im=pd.read_csv(ROOT/'results/feature_importance.csv').head(7).iloc[::-1];fig=px.bar(im,x='importance_mean',y='feature',orientation='h',color_discrete_sequence=[BLUE],error_x='importance_sd');fig.update_yaxes(title=None);fig.update_xaxes(title='Decrease in average precision');chart(fig,330)
    display=test[['model','accuracy','precision','recall','f1','roc_auc','average_precision']].rename(columns={'model':'Model','accuracy':'Accuracy','precision':'Precision','recall':'Recall','f1':'F1','roc_auc':'ROC-AUC','average_precision':'Average precision'})
    st.dataframe(display,hide_index=True,use_container_width=True,column_config={c:st.column_config.NumberColumn(format='%.3f') for c in display.columns if c!='Model'})
    with st.expander('ROC & precision-recall curves',expanded=False):
        st.caption('Final chronological test set · Thresholds are visualized, not tuned using these outcomes.')
        curve_view=st.radio('Curve view',['Selected model · interactive','All models · saved comparison'],horizontal=True,label_visibility='collapsed')
        if curve_view=='Selected model · interactive':
            fpr,tpr,_=roc_curve(pred.is_canceled,pred.predicted_cancellation_risk)
            precision,recall,_=precision_recall_curve(pred.is_canceled,pred.predicted_cancellation_risk)
            roc=px.line(x=fpr,y=tpr,render_mode='svg',labels={'x':'False-positive rate','y':'True-positive rate'},color_discrete_sequence=[BLUE])
            roc.add_scatter(x=[0,1],y=[0,1],mode='lines',name='Chance reference',line=dict(color=INK,dash='dot'),showlegend=False)
            roc.update_traces(name='Logistic regression',selector=dict(line_color=BLUE))
            pr=px.line(x=recall,y=precision,render_mode='svg',labels={'x':'Recall','y':'Precision'},color_discrete_sequence=[BLUE])
            pr.add_hline(y=pred.is_canceled.mean(),line_dash='dot',line_color=INK)
            for fig in [roc,pr]:
                fig.update_xaxes(range=[0,1]);fig.update_yaxes(range=[0,1.02]);fig.update_layout(showlegend=False)
            left,right=st.columns(2)
            with left:
                st.markdown('**ROC curve · AUC 0.718**');chart(roc,280)
            with right:
                st.markdown('**Precision-recall · AP 0.469**');chart(pr,280)
            st.caption('Blue = logistic regression. Dotted navy references show chance discrimination (ROC) and the test cancellation prevalence (precision-recall).')
        else:
            st.image(str(ROOT/'results/model_curves.png'),caption='Original comparison: logistic regression is orange; baseline and random forest are also shown.',use_container_width=True)
        st.write('ROC compares the true-positive and false-positive rates. Precision-recall shows the trade-off between finding cancellations and making accurate flags. Average precision is a ranking metric, not accuracy.')
        st.caption('Logistic regression was selected on validation results. Neither this display nor the capacity slider changes the fitted model or the fixed 0.50 classification threshold.')
    with st.expander('Evaluation method and limitations'):
        st.write('Training and validation exclude reservations whose outcomes had not resolved before the next scoring origin. Imputation, scaling, and encoding fit only the training set. The test set never selects the model or tunes the threshold.')
        st.write('The source contains reservation snapshots rather than an audited booking-time event log. Performance declines in the later period. Results do not establish cancellation reduction or financial benefit.')
        st.dataframe(m,hide_index=True,use_container_width=True)

with queue_tab:
    st.subheader('Follow-up queue')
    st.caption('Prioritize confirmation activity using historical held-out bookings matching your filters.')
    q=pred[pred.hotel.isin(hotels)&pred.market_segment.isin(segments)&pred.arrival_date.between(pd.Timestamp(dates[0]),pd.Timestamp(dates[1]))].copy()
    if q.empty:st.info('No held-out bookings match this selection. Try a later arrival range or reset the filters.')
    else:
        with st.container(border=True,key="panel-8"):
            fraction=st.slider('Review capacity · share of matching bookings (%)',5,30,10,5)
            queue,queue_stats=queue_summary(q,fraction);n=queue_stats['n']
            for c,label,val in zip(st.columns(3),['Bookings to contact','Historical cancellations','Queue cancellation rate'],[f'{n:,}',f'{queue.is_canceled.sum():,}',f'{queue.is_canceled.mean():.1%}']):c.metric(label,val)
        st.caption('Historical outcomes are shown for evaluation. Staff would not know them at contact time. Capacity changes the queue size, not the trained model.')
        capture_text=f"{queue_stats['capture']:.1%}" if queue_stats['capture'] is not None else 'not applicable (no cancellations in selection)'
        lift_text=f"{queue_stats['lift']:.2f}x" if queue_stats['lift'] is not None else 'not applicable'
        st.info(f"Queue rate: {queue_stats['rate']:.1%}, compared with {queue_stats['baseline']:.1%} in the matching test cohort. Enrichment: {lift_text}. Share of matching cancellations captured: {capture_text}. This is retrospective concentration, not prevented cancellations.")
        columns=['review_reference','hotel','arrival_date','market_segment','lead_time','predicted_cancellation_risk']
        st.dataframe(queue[columns],hide_index=True,use_container_width=True,column_config={'review_reference':'Review reference','hotel':'Hotel','arrival_date':st.column_config.DatetimeColumn('Arrival',format='DD MMM YYYY'),'market_segment':'Segment','lead_time':st.column_config.NumberColumn('Lead time (days)'),'predicted_cancellation_risk':st.column_config.ProgressColumn('Risk score',min_value=0,max_value=1,format='%.2f')})
        st.download_button('Export follow-up queue',queue[columns].to_csv(index=False),'follow_up_queue.csv','text/csv')
        st.caption('Review references identify rows in this historical test extract; they are not real property-management reservation IDs. Exported queues exclude eventual cancellation outcomes.')
        with st.expander('Recommended next steps'):
            st.write('Confirm arrival intent and booking details politely. Offer modifications consistent with existing policy. A risk score alone should never trigger a penalty or cancellation. Use a randomized pilot before claiming business impact.')
st.markdown('<div class="footer">Roomors · Group 4.2 &nbsp; / &nbsp; Local analytics workspace &nbsp; / &nbsp; Historical data, not a live reservations feed</div>',unsafe_allow_html=True)
