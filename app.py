"""파리크라상 회계·수익성·해외투자 진단 (분할 이전 감사보고서 기반)."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='파리크라상 | 회계 관점 경영진단', page_icon='📊', layout='wide')
st.markdown('''<style>.block-container{padding-top:1.5rem;max-width:1250px}div[data-testid="stMetric"]{background:#f5f7fb;padding:17px;border-radius:12px;border:1px solid #e6ebf3}h1,h2,h3{color:#182c49}.stTabs [data-baseweb="tab"]{font-weight:650}</style>''', unsafe_allow_html=True)

# 자료: 상미당홀딩스(구 파리크라상) 2025 별도감사보고서 재무제표 및 주석 4, 8, 17~19.
# 2024·2025년은 분할 이전 구 법인 기준. 금액 단위: 억 원 (원본 원 ÷ 1e8, 천원 ÷ 1e5).
D = {
 2024:dict(sales=19307.06299002,cogs=10432.41776703,gross=8874.64522299,sga=8651.28321160,op=223.36201139,net=319.47085,ar=810.30627368,ocf=970.87475647,inventory=454.83501,prod_sales=9852.09542,goods_sales=9255.66114,other_sales=199.30643,prod_cogs=5271.13558,goods_cogs=5161.28218,prod_make=4239.07622,prod_transfer=1020.01473,goods_purchase=3135.64973,goods_transfer=2014.35601),
 2025:dict(sales=19780.01066837,cogs=10945.35390340,gross=8834.65676497,sga=8574.34696214,op=260.30980283,net=-423.23423,ar=1005.30335633,ocf=735.53501486,inventory=540.43002,prod_sales=9820.17212,goods_sales=9393.99433,other_sales=565.84422,prod_cogs=5995.57388,goods_cogs=4949.78002,prod_make=4265.83342,prod_transfer=1747.79160,goods_purchase=3731.68477,goods_transfer=1200.22986)
}
# 별도감사보고서 주석 8, 법인별 지분법손익, 억원.
INV = pd.DataFrame([
 ('SPC INVESTMENT LIMITED COMPANY',-77.58047,-170.55184,'중국 투자사업 관련 법인'),
 ('PARIS BAGUETTE BON DOUX, INC.',-20.08666,-54.41053,'미국 투자법인'),
 ('PARIS BAGUETTE SINGAPORE PTE. LTD.',-76.11316,-182.93475,'싱가포르 법인'),
 ('PARIS BAGUETTE VIETNAM CO., LTD.',-15.94250,-15.66599,'베트남 법인'),
 ('SPC SAM LIP',375.08014,59.93922,'국내 관계회사'),
 ('SPL',32.78876,-64.11685,'국내 관계회사'),
 ('SPC',-134.77133,-94.42095,'국내 관계회사'),
 ('Big Bite',-14.67357,-34.60193,'투자법인')
],columns=['법인','2024','2025','분류'])
INV['변화']=INV['2025']-INV['2024']
CON = {2024:dict(sales=56244.25,op=869.57,sga=15167.19,advert=781.43711,fees=3480.59346),2025:dict(sales=55692.52,op=305.98,sga=17060.61,advert=1477.28619,fees=4772.21907)}

def won(x):return f'{x:,.1f}억 원'
def pct(a,b):return (a/b*100) if b else 0
def delta(k):return D[2025][k]-D[2024][k]
def metrics(items):
 cols=st.columns(len(items))
 for col,(label,value,change) in zip(cols,items):col.metric(label,value,change)
def table(df,fmt='{:.1f}'):
 st.dataframe(df,hide_index=True,use_container_width=True)

def note(text):st.caption('자료: '+text)

st.title('파리크라상 | 회계 관점 경영진단')
st.write('사업구조 이해 → 국내 수익성 → 해외 투자성과 → 실행 가능한 관리 제안')
st.warning('비교 범위 주의: 2024~2025년 수치는 2026년 1월 회사 분할 이전의 구 파리크라상(현 상미당홀딩스) 별도재무제표입니다. 2026년 신설 파리크라상의 현재 실적이나 가격 조정 효과로 직접 해석할 수 없습니다.',icon='⚠️')

t1,t2,t3,t4=st.tabs(['① 사업·성과 진단','② 국내 수익성·운전자본','③ 해외 투자성과','④ 회계 개선 실행안'])
with t1:
 st.subheader('사업의 숫자가 어디서 발생하는가')
 a,b,c=st.columns(3)
 a.info('국내 가맹점 공급\n\n본부의 제품 공급매출과 가맹점의 소비자 판매액은 구분해서 보아야 합니다.')
 b.info('해외 생산거점 확대\n\n공장 투자·가동 준비비용과 기존 투자법인의 손익을 혼동하지 않아야 합니다.')
 c.info('법인 분할·ERP 전환\n\n분할 전후 회계주체, 계정과목, 내부거래 및 비교 기준의 일관성을 확인해야 합니다.')
 st.subheader('2025년 별도 재무성과')
 metrics([('매출액',won(D[2025]['sales']),f'{delta("sales"):+,.1f}억'),('매출총이익',won(D[2025]['gross']),f'{delta("gross"):+,.1f}억'),('영업이익',won(D[2025]['op']),f'{delta("op"):+,.1f}억'),('영업현금흐름',won(D[2025]['ocf']),f'{delta("ocf"):+,.1f}억')])
 trend=pd.DataFrame([{'연도':str(y),'매출액':D[y]['sales'],'매출총이익':D[y]['gross'],'영업이익':D[y]['op']} for y in (2024,2025)])
 left,right=st.columns([1.4,1])
 with left:
  fig=go.Figure()
  for k in ['매출액','매출총이익','영업이익']:fig.add_trace(go.Bar(name=k,x=trend['연도'],y=trend[k],text=[f'{v:,.0f}' for v in trend[k]],textposition='auto'))
  fig.update_layout(barmode='group',height=350,yaxis_title='억 원',legend_orientation='h',margin=dict(t=25,b=25))
  st.plotly_chart(fig,use_container_width=True)
 with right:
  st.markdown('발견한 과제')
  st.write(f'• 매출액은 {delta("sales"):+,.1f}억 원 증가했지만 매출총이익은 {delta("gross"):+,.1f}억 원 변동했습니다.')
  st.write(f'• 매출총이익률은 {pct(D[2024]["gross"],D[2024]["sales"]):.2f}% → {pct(D[2025]["gross"],D[2025]["sales"]):.2f}%로 낮아졌습니다.')
  st.write(f'• 영업현금흐름은 {delta("ocf"):+,.1f}억 원 변동해, 이익뿐 아니라 현금 회수도 살펴야 합니다.')
  st.info('진단의 초점: 매출 성장 자체보다 수익성·현금창출력으로 연결됐는지 확인합니다.')
 st.divider()
 st.subheader('연결 기준 비용 증가: 별도 실적과 분리해서 확인')
 ca,cb=CON[2024],CON[2025]
 metrics([('연결 광고선전비',won(cb['advert']),f'{cb["advert"]-ca["advert"]:+,.1f}억'),('연결 지급수수료',won(cb['fees']),f'{cb["fees"]-ca["fees"]:+,.1f}억'),('연결 영업이익',won(cb['op']),f'{cb["op"]-ca["op"]:+,.1f}억')])
 st.caption('광고선전비·지급수수료의 증가 원인이 어느 법인·사업에 귀속되는지는 연결감사보고서만으로 확정할 수 없습니다. 국내 신설 사업회사의 비용 증가로 단정하지 않습니다.')
 note('2025년 별도감사보고서 손익계산서·현금흐름표, 2025년 연결감사보고서 손익계산서 및 판관비 주석')

with t2:
 st.subheader('국내 수익성: 매출은 증가했는데 왜 매출총이익은 감소했을까?')
 metrics([('매출 증가',won(delta('sales')),'2024 → 2025'),('매출원가 증가',won(delta('cogs')),'2024 → 2025'),('매출총이익 변화',won(delta('gross')),'2024 → 2025')])
 df=pd.DataFrame([{'항목':x,'2024년':D[2024][k],'2025년':D[2025][k],'증감':delta(k)} for x,k in [('제품매출액','prod_sales'),('상품매출액','goods_sales'),('기타매출액','other_sales'),('제품매출원가','prod_cogs'),('상품매출원가','goods_cogs'),('당기제품제조원가','prod_make'),('제품 타계정 대체','prod_transfer'),('당기상품매입액','goods_purchase'),('상품 타계정 대체','goods_transfer')]])
 st.dataframe(df.style.format({'2024년':'{:,.1f}','2025년':'{:,.1f}','증감':'{:+,.1f}'}),hide_index=True,use_container_width=True)
 st.info('해석: 제품매출원가 증가액 대부분이 「타계정에서 대체」 항목의 증가와 수치상 연관되지만, 상품의 같은 항목은 반대로 감소했습니다. 이 항목을 실제 제조비용 상승이나 절감 가능액으로 해석해서는 안 됩니다. 제품·상품 간 분류 및 대체 상대계정을 확인해야 합니다.')
 st.markdown('회계 담당자의 실제 확인사항')
 st.write('제품군별 공급단가·판매량·재료비·노무비 자료를 같은 기준으로 비교해 가격 효과와 수량·원가 효과를 구분합니다. 공개 감사보고서만으로 제품군별 원가율이나 2026년 가격 인상의 수익성 효과를 계산할 수는 없습니다.')
 st.divider()
 st.subheader('운전자본: 매출 증가보다 빠른 매출채권 증가')
 metrics([('기말 매출채권(순액)',won(D[2025]['ar']),f'{delta("ar"):+,.1f}억'),('기말 재고자산',won(D[2025]['inventory']),f'{delta("inventory"):+,.1f}억'),('영업현금흐름',won(D[2025]['ocf']),f'{delta("ocf"):+,.1f}억')])
 ar_growth=pct(delta('ar'),D[2024]['ar']);sales_growth=pct(delta('sales'),D[2024]['sales'])
 st.write(f'2024~2025년 매출 증가율은 {sales_growth:.1f}%, 기말 매출채권(순액) 증가율은 {ar_growth:.1f}%입니다. 이 차이는 회수 조건이나 거래처 구성 변화의 점검 신호이지, 연체가 입증됐다는 뜻은 아닙니다.')
 st.markdown('공개자료 기반 회전일수 참고치')
 dso=pct((D[2024]['ar']+D[2025]['ar'])/2,D[2025]['sales'])*365/100
 st.metric('2025년 매출채권 회전일수(근사)',f'{dso:.1f}일',help='2024·2025 기말 매출채권 평균 / 2025년 매출액 × 365. 연말 잔액과 매출액의 범위 차이, 계절성 등에 주의하세요.')
 st.caption('전년 회전일수와의 정확한 비교에는 2023년 말 매출채권 잔액이 추가로 필요합니다. 회수 지연 판단에는 거래처별 연령분석·연체내역·계약조건이 필요합니다.')
 note('2025년 별도감사보고서 재무상태표, 현금흐름표, 주석 4·5·17·18')

with t3:
 st.subheader('해외 투자성과: 손실 규모보다 변화 원인')
 st.write('별도재무제표 지분법손익 기준입니다. 지분법손실은 해당 연도의 현금 유출액이나 특정 해외 공장의 영업손실과 같지 않습니다.')
 view=st.radio('표시 대상',['전체 주요 투자법인','해외 투자법인 4곳'],horizontal=True)
 dd=INV if view=='전체 주요 투자법인' else INV.iloc[:4]
 metrics([('표시 법인 2025년 손익 합계',won(dd['2025'].sum()),'지분법손익 합계'),('전년 대비 손익 변화',won(dd['변화'].sum()),'표시 법인 기준')])
 fig=px.bar(dd.sort_values('변화'),x='변화',y='법인',orientation='h',color='변화',color_continuous_scale=['#bb4556','#e8eaf1','#167e70'],labels={'변화':'지분법손익 증감(억 원)','법인':''},height=max(320,len(dd)*54))
 fig.update_layout(coloraxis_showscale=False,margin=dict(t=20,b=20))
 st.plotly_chart(fig,use_container_width=True)
 st.dataframe(dd[['법인','분류','2024','2025','변화']].style.format({'2024':'{:,.1f}','2025':'{:,.1f}','변화':'{:+,.1f}'}),hide_index=True,use_container_width=True)
 st.warning('분석 범위: 위 표는 선정된 투자법인만 보여줍니다. 전체 지분법손익 총계와 일치하지 않을 수 있으며, SPC INVESTMENT·싱가포르·미국 투자법인의 손실을 말레이시아 공장 또는 텍사스 공장 손실로 연결할 근거는 없습니다.')
 st.markdown('회계 담당자의 후속 점검: 손실 악화 법인의 예산 대비 실적, 영업·비영업손익, 초기투자 비용, 현금흐름, 투자장부금액 및 손상 징후를 법인별로 확인합니다.')
 note('2025년 별도감사보고서 주석 8 「지분법적용투자주식」')

with t4:
 st.subheader('발견한 문제를 실제 관리 업무로 연결하기')
 tasks=[
 ('1 · 국내 수익성','매출 +473억 원에도 매출총이익 약 40억 원 감소','제품군별 공급단가·판매수량·재료비·노무비·제품/상품 계정 대체 내역','가격·수량·제품구성·원가 요인을 분해하고 수익성 악화 제품군의 공급·생산조건 점검','제품군별 매출총이익률, 단위원가, 원가 차이'),
 ('2 · 현금 회수','매출 +2.4% 대비 기말 매출채권 약 +24.1%','거래처별 채권 연령표, 계약 회수기일, 입금 이력, 특수관계자 거래','회수기일 초과 채권부터 원인 확인, 거래처별 회수조건·한도 재검토','연체율, 30/60/90일 이상 채권, 회전일수'),
 ('3 · 연결 비용','연결 광고선전비·지급수수료 증가','법인별·계정별 판관비 명세, 계약서, 캠페인 성과 및 수수료 산정 기준','증가 비용의 귀속 법인과 비용 효과를 확인하고 재계약·예산배분 검토','매출 대비 비용률, 계약별 수수료율, 집행 대비 성과'),
 ('4 · 해외 투자','일부 해외 투자법인 지분법손실 확대','법인별 예산/실적, 손익 세부내역, 투자집행, 현금흐름, 자산가치 자료','손실 확대 법인을 우선 점검하고 일회성 투자비와 반복 손실 구분','법인별 손익 편차, 투자집행률, 가동률, 손상 징후'),
 ('5 · 분할·ERP','2026년 회사 분할과 신규 ERP 운영에 따른 비교·집계 기준 점검 필요','분할 재무제표, 계정 매핑표, 내부거래 명세, 마스터 데이터, 전표 승인기록','분할 전후 비교가능성 검증 및 계정·법인·거래별 대사 절차 표준화','대사 불일치 건수, 수정분개, 결산 마감 소요일')]
 for title,signal,needed,action,kpi in tasks:
  with st.expander(title+' | '+signal,expanded=title.startswith('1')):
   st.markdown(f'공개자료에서 발견한 신호  \n{signal}')
   st.markdown(f'추가 확보할 내부자료  \n{needed}')
   st.markdown(f'실행 제안  \n{action}')
   st.markdown(f'관리 지표  \n{kpi}')
 st.divider()
 st.subheader('면접·자소서용 핵심 설명')
 st.success('"국내에서는 매출 증가에도 매출총이익이 감소하고 매출채권이 빠르게 늘어난 점에 주목했습니다. 해외에서는 투자법인별 지분법손익을 비교해 점검 우선순위를 설정했습니다. 공개자료로 원인을 단정하기보다, 회계 담당자가 추가로 확인할 자료와 관리 지표까지 연결하도록 프로그램을 설계했습니다."')
 st.caption('본 프로그램은 공개 감사보고서 기반 교육·취업 준비용 분석입니다. 실무상 개선 효과와 인과관계는 내부 원가·거래·계약 자료로 검증해야 합니다.')
