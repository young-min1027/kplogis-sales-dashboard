"""매출 집계 및 신규/이탈 화주 판별 로직."""

import pandas as pd


def sales_by_salesperson(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("영업사원", as_index=False)["매출액"]
        .sum()
        .sort_values("매출액", ascending=False)
        .reset_index(drop=True)
    )


def new_and_churned_customers(df: pd.DataFrame, window_months: int = 1) -> tuple[pd.DataFrame, pd.DataFrame]:
    """최근 `window_months`개월 구간 기준 신규화주/이탈화주를 반환한다.

    신규화주: 최근 구간에 처음 등장한 화주.
    이탈화주: 그 이전 구간(같은 길이)에는 있었으나 최근 구간에는 없는 화주.
    """
    months = sorted(df["월"].unique())
    if len(months) < window_months * 2:
        empty = df.iloc[0:0][["화주", "영업사원", "매출액"]]
        return empty, empty

    latest_window = months[-window_months:]
    prev_window = months[-window_months * 2 : -window_months]

    customers_before_latest = set(df[df["월"] < latest_window[0]]["화주"])
    latest_df = df[df["월"].isin(latest_window)]
    prev_df = df[df["월"].isin(prev_window)]
    latest_customers = set(latest_df["화주"])
    prev_customers = set(prev_df["화주"])

    new_customers = latest_df[~latest_df["화주"].isin(customers_before_latest)]
    churned_names = prev_customers - latest_customers
    churned_customers = prev_df[prev_df["화주"].isin(churned_names)]

    new_cols = new_customers[["화주", "영업사원", "매출액"]].drop_duplicates("화주")
    churned_cols = churned_customers[["화주", "영업사원", "매출액"]].drop_duplicates("화주")
    return new_cols.reset_index(drop=True), churned_cols.reset_index(drop=True)
