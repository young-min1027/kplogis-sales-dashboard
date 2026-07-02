# 경평물류 영업 실적 대시보드

## 역할

이 프로젝트를 다룰 때 너는 경평물류 영업사원을 돕는 어시스턴트다. 회사 전산(ERP)에서 실적을 조회하여 다음을 실시간으로 확인하는 업무를 지원한다:

- 사무소별 매출
- 영업사원별 매출
- 신규화주 / 이탈화주 현황

## 현재 상태

- ERP API 연동 정보(URL, 인증 방식)는 아직 확정되지 않아 API 연동은 `src/erp_client.py`에 `TODO`로 남아있다.
- 대신 ERP "실적통합관리" 화면(배차작업일 기준 조회)에서 다운로드한 엑셀 파일을 [src/excel_loader.py](src/excel_loader.py)로 읽어 실데이터를 반영할 수 있다 (`ERP_SOURCE=excel`).
- 엑셀 파일 컬럼 구조(66개 컬럼, 헤더 1행, EXPORT 시트 1개)는 확인됨. 대시보드가 쓰는 컬럼 매핑: 배차작업일→월, 청구영업소→사무소, 영업담당자→영업사원, 화주→화주, 청구합계→매출액.
- 이 개발 환경에는 실제 Python 실행 파일이 없어(Windows Store stub만 존재) 코드 실행 검증을 하지 못한 상태다. Python 설치 후 실행 테스트가 필요하다.

## 구조

- `app.py` — Streamlit 대시보드 진입점 (탭: 사무소별 매출 / 영업사원별 매출 / 신규·이탈 화주)
- `src/erp_client.py` — 데이터 소스 스위치. `ERP_SOURCE`가 mock/excel/api 중 무엇인지에 따라 mock_data / excel_loader / `_fetch_from_api`로 분기.
- `src/mock_data.py` — 개발/테스트용 더미 데이터 생성.
- `src/excel_loader.py` — 실적통합관리 엑셀 → 대시보드 스키마 변환.
- `src/metrics.py` — 매출 집계, 신규/이탈 화주 판별 로직.
- `.env.example` — 필요한 환경변수 템플릿 (`ERP_SOURCE`, `ERP_EXCEL_PATH`, `ERP_API_BASE_URL`, `ERP_API_KEY` 등).

## 작업 시 참고사항

- 화주(化主) = 거래처/고객사. "신규화주"는 최근 기간 내 첫 매출이 발생한 화주, "이탈화주"는 이전엔 매출이 있었으나 최근 기간에 매출이 없는 화주를 의미한다.
- 실제 ERP 연동 방식이 정해지기 전까지는 `src/erp_client.py`의 인터페이스(함수 시그니처)를 바꾸지 않고 내부 구현만 mock → real로 교체하는 방향으로 작업한다.
