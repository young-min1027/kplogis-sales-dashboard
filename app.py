"""경평물류 영업 실적 대시보드."""

import streamlit as st

from src.erp_client import ERP_SOURCE, fetch_sales_records
from src.metrics import new_and_churned_customers, sales_by_office, sales_by_salesperson

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

tab_office, tab_salesperson, tab_customers = st.tabs(
    ["사무소별 매출", "영업사원별 매출", "신규·이탈 화주"]
)

with tab_office:
    office_df = sales_by_office(df)
    st.bar_chart(office_df.set_index("사무소")["매출액"])
    st.dataframe(office_df, width="stretch")

with tab_salesperson:
    salesperson_df = sales_by_salesperson(df)
    st.dataframe(salesperson_df, width="stretch")

with tab_customers:
    new_customers, churned_customers = new_and_churned_customers(df)

    col_new, col_churned = st.columns(2)
    with col_new:
        st.subheader(f"신규화주 ({len(new_customers)}개사)")
        st.dataframe(new_customers, width="stretch")
    with col_churned:
        st.subheader(f"이탈화주 ({len(churned_customers)}개사)")
        st.dataframe(churned_customers, width="stretch")
