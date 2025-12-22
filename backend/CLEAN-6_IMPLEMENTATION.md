# CLEAN-6: User Model 및 Pydantic Schema 작성 완료

## 작업 요약

**Task**: CLEAN-6 - User Model 및 Pydantic Schema 작성
**담당**: Backend 개발자
**예상 시간**: 2시간
**완료 일시**: 2025-12-22

---

## 구현 내용

### 1. 프로젝트 구조 생성

```
backend/app/
├── __init__.py
├── main.py
├── core/
│   ├── __init__.py
│   ├── config.py          # 환경 변수 설정
│   └── database.py        # SQLAlchemy 데이터베이스 설정
├── models/
│   ├── __init__.py
│   └── user.py            # User 및 ParentChildLink 모델
└── schemas/
    ├── __init__.py
    └── user.py            # Pydantic 요청/응답 스키마
```

---

## 구현 상세

### 📁 core/config.py

**목적**: Pydantic Settings를 사용한 환경 변수 관리

**주요 기능**:
- `.env` 파일에서 환경 변수 자동 로드
- 타입 안전한 설정 값 관리
- 데이터베이스, JWT, API 키 등 모든 설정 통합 관리

**주요 설정**:
```python
- DATABASE_URL: PostgreSQL 연결 문자열
- SECRET_KEY: JWT 토큰 서명용 키
- ACCESS_TOKEN_EXPIRE_MINUTES: 토큰 만료 시간 (30분)
- AZURE_OPENAI_API_KEY: Azure OpenAI API 키
- LLAMA_GUARD_THRESHOLD: 유해성 검사 임계값 (0.8)
```

---

### 📁 core/database.py

**목적**: SQLAlchemy 2.0 기반 데이터베이스 연결 및 세션 관리

**주요 구성 요소**:
- `engine`: 데이터베이스 엔진 (Connection Pool 포함)
- `SessionLocal`: 세션 팩토리
- `Base`: SQLAlchemy 모델 베이스 클래스
- `get_db()`: FastAPI 의존성 주입용 세션 제공 함수

**특징**:
- Connection Pool 설정 (size: 10, max_overflow: 20)
- Health check 활성화 (`pool_pre_ping=True`)
- 디버그 모드에서 SQL 쿼리 로깅

---

### 📁 models/user.py

**목적**: 사용자 및 부모-자녀 연동 데이터베이스 모델

#### User 모델

**테이블**: `users`

**컬럼**:
| 컬럼명 | 타입 | 제약 조건 | 설명 |
|--------|------|-----------|------|
| id | Integer | PK, Auto Increment | 사용자 ID |
| email | String(255) | Unique, Not Null, Indexed | 이메일 주소 |
| password_hash | String(255) | Not Null | Bcrypt 해시된 비밀번호 |
| role | String(20) | Not Null | 역할 ('parent' or 'child') |
| created_at | DateTime | Not Null, Default: NOW() | 생성 시각 |
| updated_at | DateTime | Not Null, Default: NOW() | 수정 시각 |

**Relationships**:
- `children`: 부모에게 연동된 자녀 목록 (Many-to-Many)
- `parents`: 자녀에게 연동된 부모 목록 (Many-to-Many)

**메서드**:
- `to_dict()`: 모델을 딕셔너리로 변환 (password_hash 제외)

#### ParentChildLink 모델

**테이블**: `parent_child_links`

**컬럼**:
| 컬럼명 | 타입 | 제약 조건 | 설명 |
|--------|------|-----------|------|
| id | Integer | PK, Auto Increment | 링크 ID |
| parent_id | Integer | FK (users.id), Not Null | 부모 사용자 ID |
| child_id | Integer | FK (users.id), Not Null | 자녀 사용자 ID |
| linked_at | DateTime | Not Null, Default: NOW() | 연동 시각 |

**제약 조건**:
- `UNIQUE(parent_id, child_id)`: 중복 연동 방지
- `CASCADE DELETE`: 사용자 삭제 시 연동 정보도 삭제

---

### 📁 schemas/user.py

**목적**: Pydantic을 사용한 요청/응답 검증 스키마

#### 스키마 목록

| 스키마 | 용도 | 주요 필드 |
|--------|------|-----------|
| `UserBase` | 기본 사용자 스키마 | email, role |
| `UserCreate` | 회원가입 요청 | email, password, role |
| `UserLogin` | 로그인 요청 | email, password |
| `UserUpdate` | 사용자 정보 수정 | email?, password? |
| `UserResponse` | 사용자 정보 응답 | id, email, role, created_at, updated_at |
| `TokenResponse` | JWT 토큰 응답 | access_token, token_type, expires_in, user |
| `ParentChildLinkCreate` | 자녀 연동 요청 | child_id |
| `ParentChildLinkResponse` | 연동 정보 응답 | id, parent_id, child_id, linked_at |

#### 유효성 검증

**UserCreate 비밀번호 검증**:
```python
✓ 최소 8자 이상
✓ 최소 1개의 영문자 포함
✓ 최소 1개의 숫자 포함
```

**이메일 검증**:
```python
✓ EmailStr 타입 사용 (RFC 5322 준수)
✓ 자동 형식 검증
```

---

## 추가된 의존성

`requirements.txt`에 다음 패키지 추가:

```
pydantic-settings==2.6.1   # 환경 변수 관리
email-validator==2.2.0     # 이메일 검증
psycopg2-binary==2.9.10    # PostgreSQL 드라이버
```

---

## Acceptance Criteria 달성 여부

### Story 101 요구사항 충족

| 요구사항 | 상태 | 비고 |
|----------|------|------|
| ✅ 이메일 기반 회원가입/로그인 모델 | 완료 | User 모델 + UserCreate/Login 스키마 |
| ✅ 비밀번호 최소 8자, 영문+숫자 조합 | 완료 | Pydantic validator 구현 |
| ✅ JWT 토큰 응답 구조 | 완료 | TokenResponse 스키마 |
| ✅ 부모-자녀 연동 모델 | 완료 | ParentChildLink 모델 |
| ✅ 최대 3개 자녀 연동 (로직은 API에서 구현) | 준비 완료 | 스키마에 max_allowed=3 명시 |
| ✅ 비밀번호 해시 저장 (password_hash 컬럼) | 완료 | User 모델 |

---

## 데이터베이스 스키마 (SQL)

```sql
-- users 테이블
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_users_email ON users(email);

-- parent_child_links 테이블
CREATE TABLE parent_child_links (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    child_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    linked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    UNIQUE(parent_id, child_id)
);

CREATE INDEX idx_parent_child_parent_id ON parent_child_links(parent_id);
CREATE INDEX idx_parent_child_child_id ON parent_child_links(child_id);
```

---

## 다음 단계 (CLEAN-7 ~ CLEAN-10)

### 1. Alembic 마이그레이션 초기화

```bash
cd backend
alembic init alembic
```

### 2. 첫 마이그레이션 생성

```bash
alembic revision --autogenerate -m "Create users and parent_child_links tables"
```

### 3. 마이그레이션 적용

```bash
alembic upgrade head
```

### 4. API 엔드포인트 구현 (CLEAN-7, CLEAN-8, CLEAN-9)

다음 파일 생성 필요:
- `backend/app/api/auth.py` - 인증 API 라우터
- `backend/app/services/auth_service.py` - 비즈니스 로직
- `backend/app/utils/security.py` - 비밀번호 해싱, JWT 토큰 생성

### 5. 단위 테스트 작성 (CLEAN-10)

- `backend/tests/test_auth.py`

---

## 테스트 방법

### 임포트 검증 테스트 실행

```bash
cd backend
python test_models.py
```

**예상 출력**:
```
✓ Core modules imported successfully
✓ Models imported successfully
✓ Schemas imported successfully
✓ Valid user created successfully
✓ Password validation working
✓ Password length validation working
✓ Database metadata created successfully
```

---

## 파일 목록

**생성된 파일**:
1. `backend/app/core/__init__.py`
2. `backend/app/core/config.py` (95줄)
3. `backend/app/core/database.py` (70줄)
4. `backend/app/models/__init__.py`
5. `backend/app/models/user.py` (112줄)
6. `backend/app/schemas/__init__.py`
7. `backend/app/schemas/user.py` (157줄)
8. `backend/test_models.py` (테스트 스크립트)

**수정된 파일**:
- `backend/requirements.txt` (3개 패키지 추가)

**총 라인 수**: ~450줄

---

## 기술 스택

- **Framework**: FastAPI 0.115.5
- **ORM**: SQLAlchemy 2.0.36
- **Validation**: Pydantic 2.10.3
- **Database**: PostgreSQL (psycopg2-binary 2.9.10)
- **Migration**: Alembic 1.14.0

---

## 주요 특징

### 1. 타입 안전성
- Pydantic을 사용한 런타임 타입 검증
- SQLAlchemy 2.0의 타입 힌트 지원

### 2. 보안
- 비밀번호는 평문 저장 절대 불가 (password_hash만 저장)
- 강력한 비밀번호 정책 (8자 이상, 영문+숫자)
- 이메일 형식 자동 검증

### 3. 확장성
- 명확한 계층 구조 (core/models/schemas)
- 쉬운 스키마 확장 (BaseModel 상속)
- 재사용 가능한 설정 관리

### 4. 유지보수성
- 명확한 문서화 (docstring)
- 일관된 네이밍 컨벤션
- 모듈화된 구조

---

## 성능 고려사항

- **Connection Pooling**: 10개 연결 + 20개 오버플로우
- **인덱스**: email, parent_id, child_id 인덱싱
- **Cascading Delete**: 사용자 삭제 시 자동 정리

---

## 보안 고려사항

- ✅ 비밀번호 평문 저장 금지 (password_hash 사용)
- ✅ SQL Injection 방지 (SQLAlchemy ORM 사용)
- ✅ 이메일 중복 방지 (UNIQUE 제약)
- ✅ 부모-자녀 중복 연동 방지 (UNIQUE 제약)

---

## 문제 해결

### Q: 모델을 수정했는데 DB에 반영되지 않아요
A: Alembic 마이그레이션을 사용하세요
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Q: pydantic-settings를 찾을 수 없어요
A: 의존성을 설치하세요
```bash
pip install -r requirements.txt
```

### Q: PostgreSQL 연결 오류가 발생해요
A: `.env` 파일에서 DATABASE_URL을 확인하세요
```
DATABASE_URL=postgresql://user:password@localhost:5432/eduguard_db
```

---

## 완료 체크리스트

- ✅ User 모델 작성
- ✅ ParentChildLink 모델 작성
- ✅ Pydantic 스키마 작성 (UserCreate, UserLogin, UserResponse 등)
- ✅ 데이터베이스 설정 (config.py, database.py)
- ✅ 비밀번호 검증 로직 구현
- ✅ 이메일 검증 (EmailStr)
- ✅ 필요한 의존성 추가 (requirements.txt)
- ✅ 임포트 검증 테스트 스크립트 작성

---

**작성자**: EduGuard AI Backend Team
**작성일**: 2025-12-22
**버전**: 1.0
**Jira 티켓**: [CLEAN-6](https://letscoding.atlassian.net/browse/CLEAN-6)
