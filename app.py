"""경평물류 영업 실적 대시보드."""

import streamlit as st

from src.erp_client import ERP_SOURCE, fetch_sales_records
from src.metrics import new_and_churned_customers, sales_by_salesperson

ALLOWED_SALESPEOPLE = ["정영민", "김현훈", "백주홍", "박성훈", "가주형", "양희헌"]
CHURN_WINDOW_MONTHS = 3


def format_won(df):
    df = df.copy()
    df["매출액"] = df["매출액"].map(lambda x: f"{x:,.0f}원")
    return df

st.set_page_config(page_title="경평물류 영업 실적", layout="wide")
st.title("경평물류 영업 실적 대시보드")

if ERP_SOURCE == "mock":
    st.info("ERP 연동 정보가 아직 설정되지 않아 목업 데이터로 표시 중입니다. (.env의 ERP_SOURCE 참고)")
elif ERP_SOURCE == "csv":
    st.caption("실적통합관리 2026-01~06 다운로드 기준 데이터입니다. 실시간 데이터가 아닙니다.")

months_back = 6
if ERP_SOURCE == "mock":
    months_back = st.sidebar.slider("조회 기간(개월)", min_value=2, max_value=12, value=6)
df = fetch_sales_records(months_back=months_back)
df = df[df["영업사원"].isin(ALLOWED_SALESPEOPLE)]

tab_salesperson, tab_customers = st.tabs(["영업사원별 매출", "신규·이탈 화주"])

with tab_salesperson:
    salesperson_df = sales_by_salesperson(df)
    st.dataframe(format_won(salesperson_df), width="stretch")

with tab_customers:
    st.caption(f"최근 {CHURN_WINDOW_MONTHS}개월 구간 vs 그 이전 {CHURN_WINDOW_MONTHS}개월 구간 기준")
    new_customers, churned_customers = new_and_churned_customers(df, window_months=CHURN_WINDOW_MONTHS)

    col_new, col_churned = st.columns(2)
    with col_new:
        st.subheader(f"신규화주 ({len(new_customers)}개사)")
        st.dataframe(format_won(new_customers), width="stretch")
    with col_churned:
        st.subheader(f"이탈화주 ({len(churned_customers)}개사)")
        st.dataframe(format_won(churned_customers), width="stretch")
