# FastAPI

> FastAPI를 사용한 간단한 로그인 RestAPI 서버 입니다.


---


# 라이브러리 설치

```bash
pip install fastapi
pip install pydantic-settings
pip install "pydantic[dotenv]"
pip install "pydantic[email]"
pip install python-multipart

# db
pip install sqlalchemy
# async sqlite
pip install aiosqlite
pip install greenlet

# 비동기 서버 실행
pip install uvicorn

# jwt
pip install python-jose
pip install "passlib[bcrypt]"

# test
pip install pytest
pip install requests
```


---

# DB 설정

- 설정 파일 위치
```
/.credentials/.env
```


---

# 실행

## 1. FastAPI 서버 실행

```bash
# one execute
uvicorn app.main:app

# loop execute
uvicorn app.main:app --reload

# cumtom execute
uvicorn app.main:app --port 8000 --workers 1
```

## 2. Swagger 접속

웹브라우저에서 `http://localhost:8000/docs` 주소로 접속


---

## 3. FastAPI 서버 테스트 실행

```bash
pytest app/
```
