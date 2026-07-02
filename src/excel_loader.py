"""ERP '실적통합관리' 화면에서 다운로드한 엑셀 파일을 대시보드 스키마로 변환한다."""

import pandas as pd

_COLUMN_MAP = {
    "배차작업일": "배차작업일",
    "청구영업소": "사무소",
    "영업담당자": "영업사원",
    "화주": "화주",
    "청구합계": "매출액",
}


def load_from_excel(path: str) -> pd.DataFrame:
    """실적통합관리 엑셀을 읽어 월/사무소/영업사원/화주/매출액 컬럼의 DataFrame으로 반환한다."""
    raw = pd.read_excel(path, sheet_name=0, usecols=list(_COLUMN_MAP), dtype=str)
    raw = raw.dropna(subset=["배차작업일"])

    df = raw.rename(columns=_COLUMN_MAP)
    df["배차작업일"] = pd.to_datetime(df["배차작업일"])
    df["월"] = df["배차작업일"].values.astype("datetime64[M]")
    df["매출액"] = (
        df["매출액"].str.replace(",", "", regex=False).astype(float).fillna(0)
    )

    return df[["월", "사무소", "영업사원", "화주", "매출액"]]
