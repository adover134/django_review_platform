# 프로젝트 소개
학교 주변의 원룸에 대해 리뷰를 공유할 수 있는 웹 플랫폼 서비스입니다.</br>
업로드된 리뷰들은 내부적으로 분석하여 저장돼 사용자에게 카테고리 별 키워드들을 강조해줍니다.</br>
Django 기반 풀스택 웹 서비스와 TensorFlow 기반 NLP 모델을 결합하였습니다.

---
# 프로젝트 구조
- DBs: Django 백엔드 앱
- customForms: 리뷰 작성 및 회원 정보 입력 용 form
- static: 프론트엔드 구성 파일
- templates: 웹 페이지 html
- webPages: Django 프론트엔드 앱
- webTests: 기능 테스트용 앱 (디버깅 전용)

---
# 주요 기술 스택
- 백엔드
  - Django
  - Django REST Framework
  - social_django
- 프론트엔드
  - Kakao Login API
  - Kakao Map API
  - Django
- AI 모델
  - NLP
  - TensorFlow

---
# 주요 기능
- 리뷰 데이터 수집 및 전처리
- 주소 기반 리뷰 지역 표시
- TensorFlow 기반 토큰 단위 키워드 별 점수 학습 모델
- 카테고리 별 키워드 강조
- 소셜 로그인 (Kakaotalk)

---
# 설계 문서
- 요구사항 명세서: https://docs.google.com/document/d/1Ej2ZvKu4Gu0gHX5RQ_zv7h7FmQk90vnGsOkXhbxdCFw/edit?usp=sharing
- 설계 명세서: https://docs.google.com/document/d/1IMb8-54zuHn9anj146vTcFd8iyg328LADCRjq4frqDY/edit?usp=sharing
