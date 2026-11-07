"""Verify study integrity and dashboard interactions without starting a server."""
from pathlib import Path
import json
import pandas as pd
from streamlit.testing.v1 import AppTest
from sklearn.metrics import roc_auc_score, average_precision_score
from dashboard_utils import wilson_interval, queue_summary
root=Path(__file__).resolve().parent
s=json.loads((root/'results/summary.json').read_text());d=pd.read_csv(root/'data/hotel_bookings_analysis.csv');p=pd.read_csv(root/'results/heldout_predictions.csv');m=pd.read_csv(root/'results/model_metrics.csv')
assert len(d)==s['analysis_rows']==87396
assert int(d.is_canceled.sum())==s['cancellations']==24025
assert len(p)==s['splits']['test']['n']==17561
assert not {'reservation_status','reservation_status_date','assigned_room_type','booking_changes'}&set(s['features'])
assert p.predicted_cancellation_risk.between(0,1).all()
for _,row in m.iterrows():assert row.tn+row.fp+row.fn+row.tp==row.n
app=AppTest.from_file(str(root/'app.py'),default_timeout=45).run();assert not app.exception
assert app.metric[0].value=='87,396'
app.sidebar.multiselect[0].set_value(['Resort Hotel']).run();assert not app.exception;assert app.metric[0].value=='33,968'
app.sidebar.multiselect[0].set_value(['City Hotel','Resort Hotel']).run()
next(b for b in app.sidebar.button if b.label=='Clear').click().run()
next(c for c in app.sidebar.checkbox if c.label=='Online TA').check().run();assert not app.exception;assert app.metric[0].value=='51,618'
next(b for b in app.sidebar.button if b.label=='Reset all filters').click().run();assert app.metric[0].value=='87,396'
app.sidebar.multiselect[0].set_value([]).run();assert not app.exception
print('PASS: data totals, prediction range, feature exclusions, confusion totals, hotel/segment filters, and empty-state handling.')

selected=m[(m.model==s['selected_model'])&(m.split=='test')].iloc[0]
assert abs(roc_auc_score(p.is_canceled,p.predicted_cancellation_risk)-selected.roc_auc)<1e-10
assert abs(average_precision_score(p.is_canceled,p.predicted_cancellation_risk)-selected.average_precision)<1e-10
queue,stats=queue_summary(p,10)
assert len(queue)==s['ranking']['flagged'] and int(queue.is_canceled.sum())==s['ranking']['canceled']
assert abs(stats['lift']-s['ranking']['lift'])<1e-10
lo,hi=wilson_interval([50,0,2],[100,10,2])
assert abs(lo[0]-.4038)<.001 and abs(hi[0]-.5962)<.001 and lo[2]<.35
_,zero=queue_summary(pd.DataFrame({'is_canceled':[0,0],'predicted_cancellation_risk':[.5,.1]}),10)
assert zero['lift'] is None and zero['capture'] is None
next(b for b in app.sidebar.button if b.label=='Reset all filters').click().run()
assert app.metric[0].value=='87,396'
assert any(e.label=='ROC & precision-recall curves' for e in app.expander)
app.radio[0].set_value('All models · saved comparison').run();assert not app.exception
next(b for b in app.sidebar.button if b.label=='Clear').click().run()
next(c for c in app.sidebar.checkbox if c.label=='Undefined').check().run();assert not app.exception
assert app.metric[0].value=='2'
print('PASS: saved-score consistency, queue enrichment, Wilson intervals, zero-event handling, curve views, reset, and small-sample rendering.')
from datetime import date
next(b for b in app.sidebar.button if b.label=='Reset all filters').click().run()
app.sidebar.date_input[0].set_value((date(2015,7,1),date(2015,7,31))).run()
assert not app.exception and app.metric[0].value=='1,674'
next(b for b in app.sidebar.button if b.label=='Reset all filters').click().run()
app.slider[0].set_value(20).run()
assert not app.exception
assert any(v.label=='Bookings to contact' and v.value=='3,513' for v in app.metric)
print('PASS: arrival-period filtering, no-heldout-cohort handling, and 20% queue capacity.')
