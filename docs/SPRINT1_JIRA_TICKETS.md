# 📋 Sprint 1 Jira 티켓 상세 명세서

## 스프린트 개요
- **Sprint 이름**: Sprint 1 - The Foundation (기반 다지기)
- **기간**: 2주 (14일)
- **목표**: MVP를 위한 기본 대화 및 필터링 API 완성
- **팀 구성**: 리더 1명, Frontend 1명, Backend 1명

---

## 📊 Epic 정의

### [EPIC-01] 인프라 및 보안 가드레일 구축

**Epic 설명**:
청소년 안전을 위한 기술적 기반 구축. 서버 환경 세팅 및 유해성 필터링 로직 구현.

**비즈니스 가치**:
- 유해 콘텐츠로부터 청소년 보호
- 서비스의 핵심 안전 장치 확보
- 부모의 신뢰 확보

**성공 지표**:
- 유해 답변 차단율 99% 이상
- API 응답 시간 3초 이내
- 시스템 가동률 99% 이상

---

## 📝 Story 상세 명세

### Story 1: 사용자 인증 시스템 및 부모-자녀 계정 연동

**Story ID**: EDUGUARD-101
**Epic**: EPIC-01
**담당**: Backend 개발자
**Story Points**: 8
**우선순위**: Highest

#### 📖 사용자 스토리
```
As a 청소년 사용자
I want to 이메일로 회원가입하고 로그인할 수 있기를
So that 나만의 학습 이력을 저장하고 관리할 수 있다
```

```
As a 부모 사용자
I want to 내 자녀 계정과 연동할 수 있기를
So that 자녀의 AI 사용을 모니터링하고 관리할 수 있다
```

#### 📋 요구사항
1. 이메일 기반 회원가입/로그인 시스템
2. JWT 토큰 기반 인증
3. 부모-자녀 계정 연동 기능
4. 비밀번호 암호화 (bcrypt)
5. 회원 정보 수정/탈퇴 기능

#### ✅ Acceptance Criteria
- [ ] 사용자는 이메일과 비밀번호로 회원가입할 수 있다
- [ ] 비밀번호는 최소 8자 이상, 영문+숫자 조합이어야 한다
- [ ] 로그인 성공 시 JWT 토큰이 발급된다
- [ ] 토큰의 유효기간은 30분이다
- [ ] 부모는 자녀 계정을 최대 3개까지 연동할 수 있다
- [ ] 자녀 계정은 부모 동의 없이 독립적으로 생성할 수 없다
- [ ] 모든 비밀번호는 bcrypt로 해시되어 저장된다
- [ ] API 응답 시간은 1초 이내여야 한다

#### 🔧 Technical Details
**Database Schema**:
```sql
-- users 테이블
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL, -- 'parent' or 'child'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- parent_child_links 테이블
CREATE TABLE parent_child_links (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES users(id),
    child_id INTEGER REFERENCES users(id),
    linked_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(parent_id, child_id)
);
```

**API Endpoints**:
- `POST /api/v1/auth/signup` - 회원가입
- `POST /api/v1/auth/login` - 로그인
- `POST /api/v1/auth/link-child` - 자녀 계정 연동
- `GET /api/v1/auth/me` - 내 정보 조회
- `PUT /api/v1/auth/me` - 내 정보 수정
- `DELETE /api/v1/auth/me` - 회원 탈퇴

#### 🧪 테스트 시나리오
1. 유효한 이메일/비밀번호로 회원가입 성공
2. 중복 이메일로 회원가입 실패
3. 약한 비밀번호로 회원가입 실패
4. 정상 로그인 후 토큰 발급 확인
5. 잘못된 비밀번호로 로그인 실패
6. 부모-자녀 계정 연동 성공
7. 이미 연동된 자녀 재연동 시도 실패

---

### Story 2: 입력 프롬프트 유해성 검사 로직 구현 (Llama Guard)

**Story ID**: EDUGUARD-102
**Epic**: EPIC-01
**담당**: Backend 개발자
**Story Points**: 13
**우선순위**: Highest

#### 📖 사용자 스토리
```
As a 시스템
I want to 사용자가 입력한 프롬프트의 유해성을 사전 검사하기를
So that 부적절한 요청을 차단하고 안전한 대화를 유지할 수 있다
```

#### 📋 요구사항
1. Llama Guard 3 모델 연동
2. 유해성 카테고리별 점수 계산
3. 임계값 기반 차단 로직
4. 차단 시 사용자 친화적 메시지 반환
5. 유해 요청 로그 저장
6. Google Perspective API 보조 검사

#### ✅ Acceptance Criteria
- [ ] 사용자 입력 프롬프트를 Llama Guard로 검사한다
- [ ] 유해성 점수가 0.8 이상일 경우 차단한다
- [ ] 차단 시 "이 질문은 안전하지 않아 답변할 수 없어요" 메시지를 반환한다
- [ ] 유해 카테고리: 폭력, 성적 콘텐츠, 혐오 표현, 자해, 불법 활동
- [ ] Llama Guard 실패 시 Perspective API로 대체 검사한다
- [ ] 모든 유해 요청은 DB에 로그로 저장된다
- [ ] 검사 응답 시간은 2초 이내여야 한다

#### 🔧 Technical Details
**Safety Categories**:
```python
SAFETY_CATEGORIES = {
    "violence": {"threshold": 0.8, "severity": "high"},
    "sexual": {"threshold": 0.8, "severity": "high"},
    "hate": {"threshold": 0.7, "severity": "medium"},
    "self_harm": {"threshold": 0.9, "severity": "critical"},
    "illegal": {"threshold": 0.8, "severity": "high"},
}
```

**API Flow**:
```
User Input → Llama Guard → Score Check →
  → If Safe: Continue to LLM
  → If Unsafe: Block + Log + User Message
```

**API Endpoints**:
- `POST /api/v1/safety/check-prompt` - 프롬프트 검사
- `GET /api/v1/safety/logs` - 유해 요청 로그 조회 (부모용)

#### 🧪 테스트 시나리오
1. 안전한 프롬프트: "수학 숙제 도와줘" → 통과
2. 폭력적 프롬프트: "사람을 어떻게 해치나요?" → 차단
3. 성적 프롬프트: [부적절 내용] → 차단
4. 경계선 프롬프트: "게임에서 적을 물리치는 방법" → 통과
5. Llama Guard 오류 시 Perspective API 대체 확인

#### 📦 Dependencies
- `llama-guard` 라이브러리
- `google-cloud-perspective` 라이브러리
- Azure/AWS 인프라 (모델 호스팅)

---

### Story 3: 기본 대화형 UI 및 개인정보 마스킹 처리

**Story ID**: EDUGUARD-103
**Epic**: EPIC-01
**담당**: Frontend 개발자, Backend 개발자 (협업)
**Story Points**: 8
**우선순위**: High

#### 📖 사용자 스토리
```
As a 청소년 사용자
I want to AI와 채팅할 수 있는 직관적인 인터페이스를
So that 쉽게 질문하고 답변을 받을 수 있다
```

```
As a 시스템
I want to 대화 중 개인정보를 자동으로 감지하고 마스킹하기를
So that 사용자의 프라이버시를 보호할 수 있다
```

#### 📋 요구사항

**Frontend**:
1. 채팅 인터페이스 (메시지 입력창, 대화 히스토리)
2. 메시지 전송/수신 애니메이션
3. 로딩 인디케이터
4. 에러 메시지 표시
5. 반응형 디자인 (모바일 최적화)

**Backend**:
1. Azure OpenAI GPT-4o 연동
2. 대화 컨텍스트 관리
3. PII 자동 감지 및 마스킹
4. 대화 이력 저장

#### ✅ Acceptance Criteria

**Frontend**:
- [ ] 사용자는 텍스트 입력창에 메시지를 입력할 수 있다
- [ ] 전송 버튼 클릭 시 메시지가 전송된다
- [ ] 대화 히스토리는 스크롤 가능한 리스트로 표시된다
- [ ] AI 응답 대기 중에는 "생각 중..." 로딩 표시가 나타난다
- [ ] 에러 발생 시 사용자 친화적인 메시지가 표시된다
- [ ] 메시지는 좌(사용자)/우(AI)로 구분되어 표시된다

**Backend**:
- [ ] GPT-4o API 연동이 정상 작동한다
- [ ] 전화번호는 `010-****-****` 형식으로 마스킹된다
- [ ] 이메일은 `u***@example.com` 형식으로 마스킹된다
- [ ] 주민등호번호는 `******-*******` 형식으로 마스킹된다
- [ ] 대화 이력은 최대 10개까지 컨텍스트로 유지된다
- [ ] 모든 대화는 DB에 저장된다
- [ ] API 응답 시간은 5초 이내여야 한다

#### 🔧 Technical Details

**Frontend Components**:
```
src/screens/
  └── ChatScreen.tsx
src/components/
  ├── ChatMessage.tsx
  ├── ChatInput.tsx
  └── TypingIndicator.tsx
src/services/
  └── chatApi.ts
```

**Backend PII Detection**:
```python
PII_PATTERNS = {
    "phone": r"01[0-9]-\d{3,4}-\d{4}",
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "ssn": r"\d{6}-\d{7}",
    "address": r"[가-힣]+시 [가-힣]+구 [가-힣]+동",
}
```

**API Endpoints**:
- `POST /api/v1/chat/send` - 메시지 전송
- `GET /api/v1/chat/history/{user_id}` - 대화 이력 조회
- `DELETE /api/v1/chat/history/{chat_id}` - 대화 삭제

#### 🎨 UI/UX 요구사항
- 색상: 밝고 친근한 파스텔 톤
- 폰트: 가독성 높은 산세리프
- 버튼: 큰 터치 영역 (최소 44x44px)
- 애니메이션: 부드러운 페이드인/아웃

#### 🧪 테스트 시나리오

**Frontend**:
1. 메시지 입력 및 전송 성공
2. 빈 메시지 전송 시도 차단
3. 긴 메시지 자동 줄바꿈
4. 네트워크 오류 시 에러 메시지 표시
5. 대화 이력 스크롤 동작 확인

**Backend**:
1. 일반 대화: "안녕하세요" → "안녕하세요! 무엇을 도와드릴까요?"
2. PII 포함: "내 번호는 010-1234-5678이야" → "내 번호는 010-****-****이야"
3. 컨텍스트 유지: 이전 대화 기억 확인
4. 토큰 한도 초과 시 처리

---

## 📊 Task 분해 및 역할 배정

### Story 1 Tasks (사용자 인증)

#### Backend Tasks:

**TASK-101-1**: Database Schema 설계 및 생성
- **담당**: Backend
- **예상 시간**: 2시간
- **설명**: users, parent_child_links 테이블 생성
```sql
-- 실행할 SQL 스크립트 작성
```

**TASK-101-2**: User Model 및 Pydantic Schema 작성
- **담당**: Backend
- **예상 시간**: 2시간
- **파일**: `backend/app/models/user.py`

**TASK-101-3**: 회원가입 API 엔드포인트 구현
- **담당**: Backend
- **예상 시간**: 4시간
- **파일**: `backend/app/api/auth.py`
- **기능**: 이메일 중복 체크, 비밀번호 해싱, DB 저장

**TASK-101-4**: 로그인 API 엔드포인트 구현
- **담당**: Backend
- **예상 시간**: 4시간
- **기능**: 인증 확인, JWT 토큰 발급

**TASK-101-5**: 부모-자녀 연동 API 구현
- **담당**: Backend
- **예상 시간**: 3시간
- **기능**: 관계 생성, 중복 체크

**TASK-101-6**: 단위 테스트 작성
- **담당**: Backend
- **예상 시간**: 3시간
- **파일**: `backend/tests/test_auth.py`

#### Frontend Tasks:

**✅ TASK-101-7**: 회원가입 화면 UI 구현 - **완료 (2025-12-22)**
- **담당**: Frontend
- **예상 시간**: 4시간
- **파일**: `frontend/src/screens/SignupScreen.tsx`
- **상태**: ✅ 구현 완료
- **구현 내용**:
  - 가입 유형 선택 (학생/부모)
  - 이메일 입력 및 검증
  - 비밀번호 입력 및 검증 (최소 8자, 영문+숫자)
  - 실시간 폼 검증 및 에러 표시
  - 파스텔 톤 색상 테마 적용
  - 반응형 레이아웃 (KeyboardAvoidingView)

**TASK-101-8**: 로그인 화면 UI 구현
- **담당**: Frontend
- **예상 시간**: 3시간
- **파일**: `frontend/src/screens/LoginScreen.tsx`

**TASK-101-9**: Auth API Service 구현
- **담당**: Frontend
- **예상 시간**: 2시간
- **파일**: `frontend/src/services/authApi.ts`

**TASK-101-10**: 토큰 저장 및 관리 로직
- **담당**: Frontend
- **예상 시간**: 2시간
- **기능**: AsyncStorage 사용

---

### Story 2 Tasks (유해성 검사)

#### Backend Tasks:

**TASK-102-1**: Llama Guard 3 라이브러리 설치 및 설정
- **담당**: Backend
- **예상 시간**: 3시간
- **설명**: 모델 다운로드, 환경 설정

**TASK-102-2**: Safety Service 클래스 구현
- **담당**: Backend
- **예상 시간**: 5시간
- **파일**: `backend/app/services/safety_service.py`
- **기능**: 유해성 점수 계산, 카테고리별 검사

**TASK-102-3**: Google Perspective API 연동
- **담당**: Backend
- **예상 시간**: 3시간
- **설명**: 백업 검사 시스템

**TASK-102-4**: 유해 요청 로그 DB 스키마 생성
- **담당**: Backend
- **예상 시간**: 1시간
```sql
CREATE TABLE safety_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    prompt TEXT NOT NULL,
    safety_score FLOAT NOT NULL,
    category VARCHAR(50),
    blocked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**TASK-102-5**: Safety Check API 엔드포인트 구현
- **담당**: Backend
- **예상 시간**: 4시간
- **파일**: `backend/app/api/safety.py`

**TASK-102-6**: 유해성 검사 단위 테스트 작성
- **담당**: Backend
- **예상 시간**: 4시간
- **파일**: `backend/tests/test_safety.py`

---

### Story 3 Tasks (채팅 UI 및 PII 마스킹)

#### Frontend Tasks:

**TASK-103-1**: 채팅 화면 레이아웃 구현
- **담당**: Frontend
- **예상 시간**: 4시간
- **파일**: `frontend/src/screens/ChatScreen.tsx`

**TASK-103-2**: ChatMessage 컴포넌트 구현
- **담당**: Frontend
- **예상 시간**: 3시간
- **파일**: `frontend/src/components/ChatMessage.tsx`
- **기능**: 말풍선, 시간 표시, 좌우 정렬

**TASK-103-3**: ChatInput 컴포넌트 구현
- **담당**: Frontend
- **예상 시간**: 2시간
- **파일**: `frontend/src/components/ChatInput.tsx`
- **기능**: TextInput, 전송 버튼

**TASK-103-4**: TypingIndicator 컴포넌트 구현
- **담당**: Frontend
- **예상 시간**: 2시간
- **파일**: `frontend/src/components/TypingIndicator.tsx`
- **기능**: 애니메이션 "..."

**TASK-103-5**: Chat API Service 구현
- **담당**: Frontend
- **예상 시간**: 3시간
- **파일**: `frontend/src/services/chatApi.ts`

**TASK-103-6**: 에러 처리 및 사용자 피드백
- **담당**: Frontend
- **예상 시간**: 2시간

#### Backend Tasks:

**TASK-103-7**: Azure OpenAI GPT-4o 연동
- **담당**: Backend
- **예상 시간**: 4시간
- **파일**: `backend/app/services/llm_service.py`

**TASK-103-8**: PII Detection 및 Masking 로직 구현
- **담당**: Backend
- **예상 시간**: 5시간
- **파일**: `backend/app/services/pii_service.py`
- **기능**: 정규식 기반 패턴 매칭

**TASK-103-9**: Chat History DB 스키마 생성
- **담당**: Backend
- **예상 시간**: 1시간
```sql
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    masked_content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**TASK-103-10**: Chat API 엔드포인트 구현
- **담당**: Backend
- **예상 시간**: 4시간
- **파일**: `backend/app/api/chat.py`

**TASK-103-11**: 대화 컨텍스트 관리 로직
- **담당**: Backend
- **예상 시간**: 3시간
- **설명**: 최근 10개 메시지 유지

**TASK-103-12**: PII 마스킹 단위 테스트
- **담당**: Backend
- **예상 시간**: 3시간
- **파일**: `backend/tests/test_pii.py`

---

## 📅 Sprint 1 일정 계획 (2주)

### Week 1 (1일~7일)

**Day 1-2: 환경 설정 및 Story 1 시작**
- 팀 전체: 개발 환경 설정 (Python, Node.js, API 키 발급)
- Backend: TASK-101-1, TASK-101-2 (DB 및 Model)
- Frontend: ✅ TASK-101-7 (회원가입 UI - 완료), TASK-101-8 (로그인 UI)

**Day 3-4: Story 1 핵심 기능 구현**
- Backend: TASK-101-3, TASK-101-4 (회원가입/로그인 API)
- Frontend: TASK-101-9, TASK-101-10 (API 연동)

**Day 5: Story 1 완료 및 통합 테스트**
- Backend: TASK-101-5, TASK-101-6 (자녀 연동, 테스트)
- Frontend: 통합 테스트 및 버그 수정
- 팀 전체: 데모 및 리뷰

**Day 6-7: Story 2 시작 (유해성 검사)**
- Backend: TASK-102-1, TASK-102-2 (Llama Guard 설정 및 Service)
- Frontend: 휴식 또는 디자인 개선

### Week 2 (8일~14일)

**Day 8-9: Story 2 완료**
- Backend: TASK-102-3, TASK-102-4, TASK-102-5 (Perspective API, DB, 엔드포인트)
- Backend: TASK-102-6 (테스트)

**Day 10-11: Story 3 시작 (채팅 UI)**
- Frontend: TASK-103-1, TASK-103-2, TASK-103-3, TASK-103-4 (채팅 UI 컴포넌트)
- Backend: TASK-103-7, TASK-103-8, TASK-103-9 (LLM 연동, PII, DB)

**Day 12-13: Story 3 완료**
- Frontend: TASK-103-5, TASK-103-6 (API 연동, 에러 처리)
- Backend: TASK-103-10, TASK-103-11, TASK-103-12 (Chat API, 컨텍스트, 테스트)

**Day 14: Sprint Review & Retrospective**
- 전체 통합 테스트
- 데모 준비
- Sprint Review 미팅
- Retrospective (회고)

---

## 📝 Jira 티켓 입력 템플릿

### Epic 템플릿

```
Epic Name: [EPIC-01] 인프라 및 보안 가드레일 구축

Summary:
청소년 안전을 위한 기술적 기반 구축. 서버 환경 세팅 및 유해성 필터링 로직 구현.

Description:
청소년이 안전하게 AI를 사용할 수 있도록 다층 보안 시스템을 구축합니다.
- Llama Guard 3 기반 유해성 검사
- PII 자동 마스킹
- 사용자 인증 및 권한 관리

Business Value:
- 유해 콘텐츠로부터 청소년 보호
- 서비스의 핵심 안전 장치 확보
- 부모의 신뢰 확보

Success Metrics:
- 유해 답변 차단율 99% 이상
- API 응답 시간 3초 이내
- 시스템 가동률 99% 이상

Sprint: Sprint 1
```

### Story 템플릿 (예시: Story 1)

```
Story Name: [STORY] 사용자 인증 시스템 및 부모-자녀 계정 연동

Story Points: 8
Priority: Highest
Epic Link: EPIC-01
Assignee: Backend 개발자 이름
Sprint: Sprint 1

User Story:
As a 청소년 사용자
I want to 이메일로 회원가입하고 로그인할 수 있기를
So that 나만의 학습 이력을 저장하고 관리할 수 있다

Description:
이메일 기반 회원가입/로그인 시스템 구현
- JWT 토큰 인증
- 부모-자녀 계정 연동
- 비밀번호 암호화

Acceptance Criteria:
□ 사용자는 이메일과 비밀번호로 회원가입할 수 있다
□ 비밀번호는 최소 8자 이상, 영문+숫자 조합이어야 한다
□ 로그인 성공 시 JWT 토큰이 발급된다
□ 토큰의 유효기간은 30분이다
□ 부모는 자녀 계정을 최대 3개까지 연동할 수 있다
□ 자녀 계정은 부모 동의 없이 독립적으로 생성할 수 없다
□ 모든 비밀번호는 bcrypt로 해시되어 저장된다
□ API 응답 시간은 1초 이내여야 한다

Technical Notes:
API Endpoints:
- POST /api/v1/auth/signup
- POST /api/v1/auth/login
- POST /api/v1/auth/link-child
- GET /api/v1/auth/me

Definition of Done:
□ 코드 작성 완료
□ 단위 테스트 통과
□ 코드 리뷰 완료
□ API 문서 업데이트
□ develop 브랜치에 병합
```

### Task 템플릿 (예시: Task)

```
Task Name: [TASK-101-1] Database Schema 설계 및 생성

Story Link: EDUGUARD-101
Assignee: Backend 개발자
Estimated Time: 2시간
Sprint: Sprint 1

Description:
users 및 parent_child_links 테이블 생성

Subtasks:
□ users 테이블 스키마 작성
□ parent_child_links 테이블 스키마 작성
□ 인덱스 추가 (email, parent_id, child_id)
□ 마이그레이션 파일 생성
□ 로컬 DB에 적용 테스트

SQL Script:
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

Files to Create:
- backend/alembic/versions/001_create_users_table.py
```

---

## 🎯 Definition of Done (DoD)

모든 Story는 다음 조건을 충족해야 "완료"로 간주됩니다:

### 코드 품질
- [ ] 코드 작성 완료
- [ ] 코드 리뷰 승인 (최소 1명)
- [ ] Linting 통과 (flake8, ESLint)
- [ ] 타입 체크 통과 (mypy, TypeScript)

### 테스트
- [ ] 단위 테스트 작성 및 통과 (커버리지 80% 이상)
- [ ] 통합 테스트 통과
- [ ] 안전성 테스트 통과 (유해성 차단 확인)

### 문서화
- [ ] API 문서 업데이트 (Swagger)
- [ ] README 업데이트 (필요 시)
- [ ] 코드 주석 작성

### 배포
- [ ] develop 브랜치에 병합
- [ ] CI/CD 파이프라인 통과
- [ ] 스테이징 환경 배포 및 테스트

---

## 📞 커뮤니케이션

### Daily Stand-up (매일 아침 9:00, 15분)
1. 어제 한 일
2. 오늘 할 일
3. 장애물 (Blocker)

### Sprint Planning (Sprint 시작일)
- Epic & Story 리뷰
- Task 배정
- 목표 설정

### Sprint Review (Sprint 마지막날 오후)
- 완료된 기능 데모
- 이해관계자 피드백

### Retrospective (Sprint 마지막날 저녁)
- 잘한 점 (Keep)
- 개선할 점 (Improve)
- 시도할 것 (Try)

---

**문서 작성일**: 2025-12-20
**작성자**: EduGuard AI 팀
**버전**: 1.0
