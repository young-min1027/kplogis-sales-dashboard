"""매출 집계 및 신규/이탈 화주 판별 로직."""

import pandas as pd


def sales_by_office(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("사무소", as_index=False)["매출액"]
        .sum()
        .sort_values("매출액", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_salesperson(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["사무소", "영업사원"], as_index=False)["매출액"]
        .sum()
        .sort_values("매출액", ascending=False)
        .reset_index(drop=True)
    )


def new_and_churned_customers(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """최신월 기준 신규화주(최신월에 처음 등장)와 이탈화주(직전월에는 있었으나 최신월에 없음)를 반환한다."""
    months = sorted(df["월"].unique())
    if len(months) < 2:
        empty = df.iloc[0:0][["화주", "사무소", "영업사원"]]
        return empty, empty

    latest_month, prev_month = months[-1], months[-2]
    customers_before_latest = set(df[df["월"] < latest_month]["화주"])
    customers_latest = df[df["월"] == latest_month]
    customers_prev = set(df[df["월"] == prev_month]["화주"])
    latest_customers = set(customers_latest["화주"])

    new_customers = customers_latest[~customers_latest["화주"].isin(customers_before_latest)]
    churned_names = customers_prev - latest_customers
    churned_customers = df[(df["월"] == prev_month) & (df["화주"].isin(churned_names))]

    new_cols = new_customers[["화주", "사무소", "영업사원", "매출액"]].drop_duplicates("화주")
    churned_cols = churned_customers[["화주", "사무소", "영업사원", "매출액"]].drop_duplicates("화주")
    return new_cols.reset_index(drop=True), churned_cols.reset_index(drop=True)
