"""ERP API 연동 전까지 사용하는 개발/테스트용 더미 매출 데이터 생성기."""

import random
from datetime import date

import pandas as pd

OFFICES = ["서울사무소", "부산사무소", "인천사무소", "광주사무소"]
SALESPEOPLE = {
    "서울사무소": ["김민수", "이서연"],
    "부산사무소": ["박지훈", "최유진"],
    "인천사무소": ["정도현"],
    "광주사무소": ["강수빈", "한지우"],
}
CUSTOMERS = [f"화주-{i:03d}" for i in range(1, 41)]

_RNG = random.Random(2026)


def _add_months(d: date, n: int) -> date:
    total = d.month - 1 + n
    return date(d.year + total // 12, total % 12 + 1, 1)


def generate_sales_records(months_back: int = 6, today: date | None = None) -> pd.DataFrame:
    """지난 `months_back`개월치 매출 레코드를 생성한다.

    각 화주는 활동 시작월/종료월이 정해져 있어, 이를 통해
    최근 신규 진입 화주와 최근 거래가 끊긴(이탈) 화주가 자연스럽게 나타난다.
    """
    if today is None:
        today = date.today()

    start_month = _add_months(date(today.year, today.month, 1), -(months_back - 1))
    all_months = [_add_months(start_month, i) for i in range(months_back)]

    customer_lifespans = {}
    for customer in CUSTOMERS:
        start_idx = _RNG.randint(0, months_back - 1)
        # 70%는 최근까지 계속 거래, 나머지는 중간에 이탈
        if _RNG.random() < 0.7 or start_idx >= months_back - 1:
            end_idx = months_back - 1
        else:
            end_idx = _RNG.randint(start_idx, months_back - 2)
        customer_lifespans[customer] = (start_idx, end_idx)

    records = []
    for month_idx, month in enumerate(all_months):
        for customer, (start_idx, end_idx) in customer_lifespans.items():
            if not (start_idx <= month_idx <= end_idx):
                continue
            office = _RNG.choice(OFFICES)
            salesperson = _RNG.choice(SALESPEOPLE[office])
            amount = _RNG.randint(500, 8000) * 10_000  # 원 단위
            records.append(
                {
                    "월": month,
                    "사무소": office,
                    "영업사원": salesperson,
                    "화주": customer,
                    "매출액": amount,
                }
            )

    return pd.DataFrame.from_records(records)
