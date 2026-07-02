# 경평물류 영업 실적 대시보드

사무소별 매출, 영업사원별 매출, 신규/이탈 화주를 확인하는 Streamlit 대시보드.

## 실행 방법

```bash
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

기본 설정(`ERP_SOURCE=mock`)에서는 목업 데이터로 동작한다.

## 실적통합관리 엑셀로 실행하기

ERP의 "실적통합관리" 화면에서 배차작업일 기준으로 조회 후 다운로드한 엑셀 파일을 바로 쓸 수 있다.

1. `.env`에서 `ERP_SOURCE=excel`로 변경한다.
2. `ERP_EXCEL_PATH`에 다운로드한 파일의 절대경로를 채운다.

[src/excel_loader.py](src/excel_loader.py)가 배차작업일/청구영업소/영업담당자/화주/청구합계 컬럼을 대시보드가 쓰는 월/사무소/영업사원/화주/매출액으로 변환한다.

## 실제 ERP API 연동하기

1. `.env`에 `ERP_API_BASE_URL`, `ERP_API_KEY`를 채운다.
2. `ERP_SOURCE=api`로 변경한다.
3. [src/erp_client.py](src/erp_client.py)의 `_fetch_from_api` 함수를 실제 API 스펙에 맞게 수정한다.
