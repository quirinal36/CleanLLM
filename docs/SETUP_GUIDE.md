# 🚀 EduGuard AI - 개발 환경 셋업 가이드

## 📋 목차
1. [사전 요구사항](#사전-요구사항)
2. [Backend 설정](#backend-설정)
3. [Frontend 설정](#frontend-설정)
4. [외부 API 설정](#외부-api-설정)
5. [데이터베이스 설정](#데이터베이스-설정)
6. [테스트 실행](#테스트-실행)
7. [문제 해결](#문제-해결)

---

## 사전 요구사항

### 필수 소프트웨어 설치

#### 1. Python 3.13+
```bash
# Windows
# Python 공식 사이트에서 설치: https://www.python.org/downloads/
# 설치 시 "Add Python to PATH" 체크 필수

# 설치 확인
python --version
# 출력: Python 3.13.x
```

#### 2. Node.js 18+
```bash
# Windows
# Node.js 공식 사이트에서 LTS 버전 설치: https://nodejs.org/

# 설치 확인
node --version
npm --version
```

#### 3. Git
```bash
# Windows
# Git 공식 사이트에서 설치: https://git-scm.com/

# 설치 확인
git --version
```

#### 4. 코드 에디터 (선택)
- **VS Code** (권장): https://code.visualstudio.com/
- 추천 확장 프로그램:
  - Python
  - Pylance
  - React Native Tools
  - ESLint
  - Prettier

---

## Backend 설정

### 1단계: 가상환경 생성 및 활성화

```bash
# 프로젝트 루트로 이동
cd CleanLLM/backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# Mac/Linux
source venv/bin/activate

# 활성화 확인 (프롬프트에 (venv) 표시됨)
```

### 2단계: 의존성 설치

```bash
# Python 패키지 업그레이드
python -m pip install --upgrade pip

# 프로젝트 의존성 설치
pip install -r requirements.txt

# 설치 확인
pip list
```

### 3단계: 환경변수 설정

```bash
# .env 파일 생성 (Windows)
copy .env.example .env

# .env 파일 생성 (Mac/Linux)
cp .env.example .env

# .env 파일 편집 (VS Code)
code .env
```

**최소 필수 환경변수:**
```env
# .env 파일 내용
APP_NAME=EduGuard AI
ENVIRONMENT=development
DEBUG=True
API_PORT=8000

# 나중에 설정할 항목 (일단 placeholder)
AZURE_OPENAI_API_KEY=temporary_placeholder
PINECONE_API_KEY=temporary_placeholder
SECRET_KEY=temporary_secret_key_for_development_only
```

### 4단계: 서버 실행

```bash
# 개발 서버 실행
python app/main.py

# 또는
uvicorn app.main:app --reload --port 8000

# 성공 시 출력:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete.
```

### 5단계: API 테스트

브라우저에서 다음 URL 접속:
- Health Check: http://localhost:8000/health
- API 문서: http://localhost:8000/docs (Swagger UI)

---

## Frontend 설정

### 1단계: 의존성 설치

```bash
# Frontend 디렉토리로 이동
cd ../frontend

# Node.js 패키지 설치
npm install

# 설치 확인
npm list --depth=0
```

### 2단계: 환경변수 설정

```bash
# .env 파일 생성 (Windows)
copy .env.example .env

# .env 파일 생성 (Mac/Linux)
cp .env.example .env

# .env 파일 편집
code .env
```

**필수 환경변수:**
```env
API_BASE_URL=http://localhost:8000
API_VERSION=v1
ENVIRONMENT=development
DEBUG_MODE=true
```

### 3단계: Expo 설정 (React Native)

```bash
# Expo CLI 전역 설치
npm install -g expo-cli

# 프로젝트 초기화 (이미 설정된 경우 생략)
# expo init은 package.json이 있으므로 생략 가능

# Expo 앱 설치 (모바일 기기에)
# iOS: App Store에서 "Expo Go" 설치
# Android: Google Play에서 "Expo Go" 설치
```

### 4단계: 앱 실행

```bash
# 개발 서버 시작
npm start

# 플랫폼별 실행
npm run android  # Android 에뮬레이터 또는 실제 기기
npm run ios      # iOS 시뮬레이터 (Mac만 가능)
npm run web      # 웹 브라우저

# QR 코드 스캔하여 모바일 기기에서 테스트
```

---

## 외부 API 설정

### 1. Azure OpenAI API

#### 가입 및 키 발급
1. Azure Portal 접속: https://portal.azure.com/
2. "Azure OpenAI" 서비스 생성
3. 리소스 배포 후 "Keys and Endpoint" 메뉴 접속
4. API Key와 Endpoint 복사

#### 환경변수 설정
```env
AZURE_OPENAI_API_KEY=your_actual_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

#### 예상 비용
- GPT-4o: $0.03/1K tokens (입력), $0.06/1K tokens (출력)
- 월 예상: 테스트 단계 $10~$50

### 2. Pinecone Vector DB

#### 가입 및 설정
1. Pinecone 가입: https://www.pinecone.io/
2. "Create Index" 클릭
   - Index Name: `eduguard-knowledge`
   - Dimensions: `1536` (OpenAI embedding 크기)
   - Metric: `cosine`
3. API Key 복사

#### 환경변수 설정
```env
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_ENVIRONMENT=us-west1-gcp
PINECONE_INDEX_NAME=eduguard-knowledge
```

#### 예상 비용
- Free Tier: 1 index, 100K vectors 무료
- 개발 단계에서는 무료 사용 가능

### 3. Google Perspective API

#### 가입 및 키 발급
1. Google Cloud Console: https://console.cloud.google.com/
2. 새 프로젝트 생성: "EduGuard-AI"
3. Perspective API 활성화
4. API Key 생성 (APIs & Services → Credentials)

#### 환경변수 설정
```env
GOOGLE_PERSPECTIVE_API_KEY=your_google_key_here
```

#### 예상 비용
- 무료 Quota: 1 QPS (초당 1 요청)
- 개발 단계 무료 사용 가능

### 4. Llama Guard 3 설정 (선택)

#### Hugging Face 토큰 발급
1. Hugging Face 가입: https://huggingface.co/
2. Settings → Access Tokens → New token
3. Read 권한으로 토큰 생성

```env
HUGGINGFACE_TOKEN=your_hf_token_here
LLAMA_GUARD_MODEL_PATH=meta-llama/Llama-Guard-3-8B
```

**참고**: Llama Guard는 로컬 실행 시 GPU 필요 (8GB+ VRAM)

---

## 데이터베이스 설정

### PostgreSQL 설치 및 설정

#### 1. PostgreSQL 설치 (Windows)
1. PostgreSQL 다운로드: https://www.postgresql.org/download/
2. 설치 시 비밀번호 설정 (예: `postgres`)
3. Port: 기본값 `5432` 사용

#### 2. 데이터베이스 생성
```bash
# PostgreSQL 명령줄 접속 (Windows)
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE eduguard_db;

# 사용자 생성 (선택)
CREATE USER eduguard_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE eduguard_db TO eduguard_user;

# 종료
\q
```

#### 3. 환경변수 설정
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/eduguard_db
```

#### 4. 마이그레이션 실행 (추후)
```bash
# Alembic 초기화
alembic init alembic

# 마이그레이션 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 적용
alembic upgrade head
```

---

## 테스트 실행

### Backend 테스트

```bash
cd backend

# 모든 테스트 실행
pytest

# 커버리지와 함께 실행
pytest --cov=app tests/

# 특정 파일만 테스트
pytest tests/test_safety.py

# 상세 출력
pytest -v
```

### Frontend 테스트

```bash
cd frontend

# 모든 테스트 실행
npm test

# 커버리지 확인
npm test -- --coverage

# Watch 모드
npm test -- --watch
```

---

## 문제 해결

### Backend 관련

#### 문제: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# 해결: 가상환경 활성화 확인 및 재설치
venv\Scripts\activate
pip install -r requirements.txt
```

#### 문제: `Port 8000 is already in use`
```bash
# 해결: 포트 사용 중인 프로세스 종료
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# 또는 다른 포트 사용
uvicorn app.main:app --port 8001
```

#### 문제: `Connection to database failed`
```bash
# 해결: PostgreSQL 서비스 실행 확인
# Windows: services.msc 실행 → postgresql 서비스 시작
```

### Frontend 관련

#### 문제: `npm install` 실패
```bash
# 해결: 캐시 정리 후 재시도
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### 문제: `Metro bundler` 오류
```bash
# 해결: 캐시 정리
npx expo start --clear
```

#### 문제: `Unable to resolve module`
```bash
# 해결: Watchman 설치 (Mac/Linux)
brew install watchman

# 또는 개발 서버 재시작
npm start -- --reset-cache
```

### API 연동 관련

#### 문제: `CORS error`
```python
# backend/app/main.py 확인
# allow_origins=["*"] 설정 되어있는지 확인
```

#### 문제: `API 응답 없음`
```bash
# Backend 서버 실행 확인
curl http://localhost:8000/health

# Frontend .env 파일 확인
# API_BASE_URL이 올바른지 확인
```

---

## 🎯 다음 단계

환경 설정이 완료되었다면:

1. [Git 브랜치 전략 문서](GIT_STRATEGY.md) 읽기
2. Sprint 1 티켓 확인 ([Agile.md](../Agile.md))
3. 첫 번째 기능 개발 시작
4. 팀 Daily Stand-up 참여

---

## 📞 도움이 필요하신가요?

- 팀 리더(이형구): [연락처]
- 팀 Slack/Discord: [채널 링크]
- GitHub Issues: [프로젝트 이슈 페이지]

---

**Happy Coding! 🚀**
