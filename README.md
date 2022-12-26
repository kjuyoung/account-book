Contents
========

```
1. 요구사항
2. 구현 기능 요약
3. 구현 기능
4. 미구현 기능
5. 구현 API
6. 서버 실행 방법 설명

```

## 1. 요구사항
---------
>1. 고객은 이메일과 비밀번호 입력을 통해서 회원 가입을 할 수 있습니다. 
>2. 고객은 회원 가입이후, 로그인과 로그아웃을 할 수 있습니다. 
>3. 고객은 로그인 이후 가계부 관련 아래의 행동을 할 수 있습니다. 
>    1. 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다. 
>    2. 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다. 
>    3. 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다. 
>    4. 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다. 
>    5. 가계부에서 상세한 세부 내역을 볼 수 있습니다. 
>    6. 가계부의 세부 내역을 복제할 수 있습니다.
>    7. 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
>    (단축 URL은 특정 시간 뒤에 만료되어야 합니다.)
>
>4. 로그인하지 않은 고객은 가계부 내역에 대한 접근 제한 처리가 되어야 합니다.

<br/>

## 2. 구현 기능 요약
-------------
>+ 회원가입 / 로그인 / 로그아웃  
>+ 로그인 고객  
>   + 가계부 내용(금액, 메모) 생성 / 수정 / 삭제 / 조회(리스트, 상세내역) / 복제 / 단축 URL
>+ 로그인하지 않은 고객  
>   + 접근 제한

<br/>

## 3. 구현 기능
-------------
>+ 회원가입 (password를 2번 입력받아 정확히 입력했는지 확인, 비밀번호 암호화하여 저장)
>+ 로그인 (Access token 발행)
>+ 로그아웃 (Frontend에서 처리하면 된다고 생각하여 별다른 기능구현은 하지 않았습니다.)
>+ 가계부 생성
>+ 가게부 수정
>+ 가계부 삭제
>+ 가계부 리스트 조회 (간략한 리스트가 아닌 내용 전부에 대한 리스트 반환)
>   + pagination (offset, limit)
>+ 가계부 조회
>+ 가계부 내용 복제 (세부 내역 복제의 뜻을 정확히 이해하지 못해 조회된 데이터를 반환하도록 구현)
>+ 가계부 단축 URL 반환 (만료 기능은 미구현)
>+ 로그인하지 않은 고객에 대한 접근 제한 (JWT를 통한 인증 제어)
>+ REST API 구조
>+ Docker를 이용한 실행 (App, MySQL 5.7)

<br/>

## 4. 미구현 기능
-------------
>+ 단축 URL 만료 기능
>+ RESTful API (HATEOAS)
>+ 테스트 케이스 작성

<br/>

## 5. 구현 API
-------------
>+ 회원가입 / 로그인 / 로그아웃
>   + /api/v1/users/create
>   + /api/v1/users/login
>   + /api/v1/users/logout
>+ 가계부 생성 / 수정 / 삭제 / 조회 / 복제 / 단축URL
>   + POST  /api/v1/accountbooks
>   + PATCH /api/v1/accountbooks/{account_book_id}
>   + DELETE    /api/v1/accountbooks/{account_book_id}
>   + GET   /api/v1/accountbooks
>   + GET   /api/v1/accountbooks/{account_book_id}
>   + GET   /api/v1/accountbooks/{account_book_id}/copy
>   + GET   /api/v1/accountbooks/{account_book_id}/shareurl

<br/>

## 6. 서버 실행 방법 설명
-------------
>+ 가상환경 만들기
>+ [필요 패키지 설치]
>   + pip install -r requirements.txt
>+ [Docker를 이용한 빌드 및 실행 - App & Mysql]
>   + docker-compose -f docker-compose.yml up -d --build
>   + 또는 uvicorn main:app --reload --port 8080
>+ [Swagger를 활용한 API 기능 문서화 & TEST]
>   + http://0.0.0.0:8080/docs

<br/>