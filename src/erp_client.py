"""회사 전산(ERP) API에서 매출 데이터를 가져오는 래퍼.

실제 API 정보(URL, 인증 방식)가 확정되기 전까지는 ERP_USE_MOCK=true(기본값)일 때
mock_data 모듈이 생성한 더미 데이터를 반환한다. API 정보가 확보되면
`_fetch_from_api`만 채우면 되고, 호출부(app.py, metrics.py)는 수정할 필요가 없다.
"""

import os
from datetime import date
from pathlib import Path

import pandas as pd
import requests

from src.excel_loader import load_from_excel
from src.mock_data import generate_sales_records

DEFAULT_CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "sales_2026_h1.csv"

ERP_API_BASE_URL = os.environ.get("ERP_API_BASE_URL", "")
ERP_API_KEY = os.environ.get("ERP_API_KEY", "")
ERP_EXCEL_PATH = os.environ.get("ERP_EXCEL_PATH", "")
ERP_CSV_PATH = os.environ.get("ERP_CSV_PATH", str(DEFAULT_CSV_PATH))
# mock | csv | excel | api
ERP_SOURCE = os.environ.get("ERP_SOURCE", "csv")


def fetch_sales_records(months_back: int = 6, today: date | None = None) -> pd.DataFrame:
    """매출 레코드를 DataFrame으로 반환한다.

    컬럼: 월(date, 각 월 1일), 사무소, 영업사원, 화주, 매출액
    """
    if ERP_SOURCE == "csv":
        return pd.read_csv(ERP_CSV_PATH, parse_dates=["월"])
    if ERP_SOURCE == "excel":
        return load_from_excel(ERP_EXCEL_PATH)
    if ERP_SOURCE == "api":
        return _fetch_from_api(months_back=months_back, today=today)
    return generate_sales_records(months_back=months_back, today=today)


def _fetch_from_api(months_back: int, today: date | None) -> pd.DataFrame:
    if not ERP_API_BASE_URL:
        raise RuntimeError(
            "ERP_API_BASE_URL이 설정되지 않았습니다. .env 파일을 설정하거나 "
            "ERP_USE_MOCK=true로 목업 데이터를 사용하세요."
        )

    # TODO: 실제 ERP API 스펙이 확정되면 아래 요청을 맞게 수정한다.
    response = requests.get(
        f"{ERP_API_BASE_URL}/sales",
        headers={"Authorization": f"Bearer {ERP_API_KEY}"},
        params={"months_back": months_back},
        timeout=10,
    )
    response.raise_for_status()
    return pd.DataFrame(response.json())
