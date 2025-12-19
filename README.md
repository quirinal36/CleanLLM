# 🛡️ EduGuard AI - 청소년 안전 LLM 서비스

> 미성년자가 AI의 위험(할루시네이션, 편향성, 유해물) 없이 잠재력을 탐색할 수 있는 **안전한 디지털 운동장**

## 📋 프로젝트 개요

EduGuard AI는 청소년을 위한 안전한 AI 학습 플랫폼입니다. 기술적 샌드박스와 가드레일을 통해 위험을 원천 차단하며, 교육적 가치를 극대화합니다.

### 핵심 원칙
- ✅ **Safety First**: Llama Guard 3 + Perspective API 기반 다층 안전 필터
- 📚 **RAG-based Learning**: 검증된 교육 데이터 기반 답변 생성
- 🔒 **Privacy Protection**: PII 자동 마스킹 및 개인정보 보호
- 👨‍👩‍👧 **Guardian Dashboard**: 부모 모니터링 및 제어 시스템

## 🏗️ 프로젝트 구조

```
CleanLLM/
├── backend/                 # Python FastAPI 백엔드
│   ├── app/
│   │   ├── api/            # API 라우터
│   │   ├── core/           # 핵심 설정 및 보안
│   │   ├── models/         # 데이터 모델
│   │   ├── services/       # 비즈니스 로직
│   │   └── utils/          # 유틸리티 함수
│   ├── tests/              # 테스트 코드
│   ├── requirements.txt    # Python 의존성
│   └── .env.example        # 환경변수 템플릿
│
├── frontend/               # React Native 프론트엔드
│   ├── src/
│   │   ├── components/     # 재사용 가능 컴포넌트
│   │   ├── screens/        # 화면 컴포넌트
│   │   ├── services/       # API 통신
│   │   ├── utils/          # 유틸리티
│   │   └── assets/         # 이미지, 폰트 등
│   ├── __tests__/          # 테스트 코드
│   ├── package.json        # Node.js 의존성
│   └── .env.example        # 환경변수 템플릿
│
├── docs/                   # 프로젝트 문서
├── PRD.md                  # 제품 요구사항 문서
├── Agile.md                # 애자일 개발 가이드
└── README.md               # 프로젝트 소개 (현재 파일)
```

## 🚀 빠른 시작 가이드

### 사전 요구사항
- Python 3.13+
- Node.js 18+
- Git

### 1️⃣ Backend 설정

```bash
# Backend 디렉토리로 이동
cd backend

# Python 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
copy .env.example .env
# .env 파일을 열어 API 키 등을 설정하세요

# 서버 실행
python app/main.py
```

서버가 `http://localhost:8000`에서 실행됩니다.

### 2️⃣ Frontend 설정

```bash
# Frontend 디렉토리로 이동
cd frontend

# 의존성 설치
npm install

# 환경변수 설정
copy .env.example .env
# .env 파일을 열어 API 엔드포인트를 설정하세요

# 앱 실행
npm start

# 플랫폼별 실행
npm run android  # Android
npm run ios      # iOS
npm run web      # Web
```

## 🛠️ 기술 스택

### Backend
- **Framework**: FastAPI (Python)
- **AI/LLM**: Azure OpenAI (GPT-4o), LangGraph
- **Vector DB**: Pinecone
- **Safety**: Llama Guard 3, Google Perspective API
- **Database**: PostgreSQL (SQLAlchemy)

### Frontend
- **Framework**: React Native (Expo)
- **Navigation**: React Navigation
- **State Management**: React Query
- **HTTP Client**: Axios

### Infrastructure
- **Cloud**: AWS EC2
- **CI/CD**: GitHub Actions (예정)
- **Monitoring**: CloudWatch (예정)

## 📊 개발 로드맵

### Sprint 1: The Foundation (2주)
- [ ] 사용자 인증 시스템
- [ ] 입력 프롬프트 유해성 검사 (Llama Guard)
- [ ] 기본 대화형 UI 및 PII 마스킹

### Sprint 2: Knowledge Integration (2주)
- [ ] RAG 시스템 구축
- [ ] 교과서 데이터 임베딩
- [ ] 출처 표기 기능

### Sprint 3: Creation Tools (2주)
- [ ] 안전한 이미지 생성
- [ ] 실시간 협업 에디터
- [ ] 파일 업로드 스캔 시스템

### Sprint 4: Guardian & Launch (2주)
- [ ] 부모 대시보드
- [ ] 실시간 알림 시스템
- [ ] QA 및 배포

자세한 내용은 [Agile.md](Agile.md)를 참조하세요.

## 🔐 환경 변수 설정

### Backend 필수 환경변수
```env
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
PINECONE_API_KEY=your_key_here
GOOGLE_PERSPECTIVE_API_KEY=your_key_here
SECRET_KEY=your_secret_key_here
```

### Frontend 필수 환경변수
```env
API_BASE_URL=http://localhost:8000
```

자세한 설정은 각 디렉토리의 `.env.example` 파일을 참조하세요.

## 🧪 테스트 실행

### Backend 테스트
```bash
cd backend
pytest
pytest --cov=app tests/  # 커버리지 포함
```

### Frontend 테스트
```bash
cd frontend
npm test
```

## 📚 문서

- [PRD.md](PRD.md) - 제품 요구사항 문서
- [Agile.md](Agile.md) - 스프린트 계획 및 Jira 가이드
- [docs/](docs/) - 추가 기술 문서

## 🤝 팀 구성

- **프로젝트 리더**: 이형구
- **Frontend 개발**: 1명
- **Backend 개발**: 1명

## 📝 Git 브랜치 전략

```
main (production)
  └── develop (integration)
       ├── feature/user-auth
       ├── feature/llama-guard
       └── feature/chat-ui
```

- `main`: 프로덕션 배포 브랜치
- `develop`: 개발 통합 브랜치
- `feature/*`: 기능별 개발 브랜치

자세한 내용은 [docs/GIT_STRATEGY.md](docs/GIT_STRATEGY.md)를 참조하세요.

## 🎯 성공 지표 (KPI)

1. **유해 답변 차단율**: 99.9% 이상
2. **할루시네이션 발생률**: 5% 미만 (RAG 적용 기준)
3. **사용자 유지율**: 주간 활성 사용자(WAU) 대비 40% 이상

## 📄 라이선스

MIT License

## 🆘 도움이 필요하신가요?

- 이슈 제기: [GitHub Issues](../../issues)
- 팀 채널: [프로젝트 Slack/Discord]
- 문서: [docs/](docs/)

---

**Built with ❤️ by EduGuard Team**
