# 🚀 Jira 프로젝트 빠른 시작 가이드

## 📋 목차
1. [Jira 프로젝트 생성](#jira-프로젝트-생성)
2. [Epic 생성](#epic-생성)
3. [Story 생성](#story-생성)
4. [Task 생성](#task-생성)
5. [Sprint 설정](#sprint-설정)
6. [보드 설정](#보드-설정)

---

## Jira 프로젝트 생성

### 1단계: Jira 계정 및 워크스페이스 생성

1. **Jira 접속**: https://www.atlassian.com/software/jira
2. **무료 시작하기** 클릭
3. **이메일 입력** 및 계정 생성
4. **워크스페이스 이름**: `EduGuard-AI` 입력

### 2단계: 프로젝트 생성

1. **프로젝트 만들기** 버튼 클릭
2. **프로젝트 유형 선택**:
   - ✅ **Scrum** 선택 (스프린트 기반 개발)
3. **프로젝트 이름**: `EduGuard AI`
4. **프로젝트 키**: `EDUGUARD` (자동 생성됨)
5. **만들기** 클릭

### 3단계: 팀원 초대

1. 프로젝트 설정 → **사람** 메뉴
2. **사람 추가** 클릭
3. 팀원 이메일 입력:
   - Frontend 개발자 이메일
   - Backend 개발자 이메일
4. 역할 선택: **Member**
5. **초대** 클릭

---

## Epic 생성

### Epic 만들기

1. 왼쪽 사이드바 → **백로그** 클릭
2. 상단 **만들기** 버튼 → **Epic** 선택
3. Epic 정보 입력:

```
Epic 이름: [EPIC-01] 인프라 및 보안 가드레일 구축

요약:
청소년 안전을 위한 기술적 기반 구축

설명:
청소년이 안전하게 AI를 사용할 수 있도록 다층 보안 시스템을 구축합니다.

비즈니스 가치:
- 유해 콘텐츠로부터 청소년 보호
- 서비스의 핵심 안전 장치 확보
- 부모의 신뢰 확보

성공 지표:
- 유해 답변 차단율 99% 이상
- API 응답 시간 3초 이내
- 시스템 가동률 99% 이상
```

4. **만들기** 클릭

### Epic 색상 지정 (선택사항)

- EPIC-01: 🔴 빨강 (보안/안전)
- EPIC-02: 🟢 초록 (지식/RAG)
- EPIC-03: 🔵 파랑 (기능 확장)
- EPIC-04: 🟡 노랑 (부모 기능)

---

## Story 생성

### Story 만들기

1. 백로그 화면에서 **만들기** 버튼 클릭
2. **이슈 유형**: Story 선택
3. Story 정보 입력:

#### Story 1 예시:

```
제목: [STORY] 사용자 인증 시스템 및 부모-자녀 계정 연동

이슈 유형: Story
Epic 링크: EPIC-01 선택
담당자: Backend 개발자 선택
Story Points: 8
우선순위: Highest

설명:
이메일 기반 회원가입/로그인 시스템 구현

사용자 스토리:
As a 청소년 사용자
I want to 이메일로 회원가입하고 로그인할 수 있기를
So that 나만의 학습 이력을 저장하고 관리할 수 있다

인수 기준 (Acceptance Criteria):
☐ 사용자는 이메일과 비밀번호로 회원가입할 수 있다
☐ 비밀번호는 최소 8자 이상, 영문+숫자 조합이어야 한다
☐ 로그인 성공 시 JWT 토큰이 발급된다
☐ 토큰의 유효기간은 30분이다
☐ 부모는 자녀 계정을 최대 3개까지 연동할 수 있다

기술 노트:
API Endpoints:
- POST /api/v1/auth/signup
- POST /api/v1/auth/login
- POST /api/v1/auth/link-child
```

4. **만들기** 클릭

### Story Points 설정

Jira에서 Story Points는 작업의 복잡도를 나타냅니다:

- **1-2 Points**: 매우 간단 (1-2시간)
- **3-5 Points**: 보통 (반나절)
- **8 Points**: 복잡 (1일)
- **13 Points**: 매우 복잡 (2일)
- **21+ Points**: 너무 큼, 분해 필요

---

## Task 생성

### Task 만들기 (Story의 하위 작업)

1. Story를 클릭하여 상세 화면 열기
2. **하위 작업 만들기** 클릭
3. Task 정보 입력:

#### Task 예시:

```
제목: [TASK-101-1] Database Schema 설계 및 생성

담당자: Backend 개발자
예상 시간: 2시간

설명:
users 및 parent_child_links 테이블 생성

체크리스트:
☐ users 테이블 스키마 작성
☐ parent_child_links 테이블 스키마 작성
☐ 인덱스 추가
☐ 마이그레이션 파일 생성
☐ 로컬 DB에 적용 테스트

기술 상세:
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```
```

4. **만들기** 클릭

---

## Sprint 설정

### Sprint 1 생성 및 설정

1. **백로그** 화면으로 이동
2. 우측 상단 **Sprint 만들기** 클릭
3. Sprint 이름: `Sprint 1 - The Foundation`
4. Sprint 기간 설정:
   - 시작일: 2025-12-23 (예시)
   - 종료일: 2026-01-05 (2주)
5. Sprint 목표 입력:
   ```
   MVP를 위한 기본 대화 및 필터링 API 완성
   - 사용자 인증 시스템
   - 유해성 검사 로직
   - 기본 채팅 UI
   ```

### Story를 Sprint에 추가

1. 백로그에서 Story를 드래그
2. Sprint 1 영역에 드롭
3. 모든 관련 Story 추가:
   - STORY-101: 사용자 인증
   - STORY-102: 유해성 검사
   - STORY-103: 채팅 UI

### Sprint 시작

1. Sprint 영역 우측 상단 **Sprint 시작** 클릭
2. 확인 다이얼로그에서 **시작** 클릭

---

## 보드 설정

### 칸반 보드 컬럼 설정

1. **보드** 메뉴 → 보드 설정 (⚙️ 아이콘)
2. **컬럼** 탭 선택
3. 다음 컬럼 추가/수정:

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│   To Do     │ In Progress │   Review    │    Done     │
│   (해야 할 일)│   (진행 중)  │   (리뷰 중)  │   (완료)     │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### 워크플로우 설정

기본 워크플로우:
1. **To Do**: 아직 시작하지 않음
2. **In Progress**: 작업 진행 중
3. **Review**: 코드 리뷰 대기/진행
4. **Done**: 완료 및 develop 병합

### 스윔레인 설정 (선택사항)

보드를 역할별로 구분:
- **Frontend**: Frontend 개발자 작업
- **Backend**: Backend 개발자 작업
- **Blocked**: 차단된 작업

설정 방법:
1. 보드 설정 → **스윔레인** 탭
2. **담당자별로 그룹화** 선택

---

## 작업 흐름 (Workflow)

### 개발자가 작업을 시작할 때

1. **백로그** 또는 **보드**에서 Task 선택
2. Task 클릭 → 상세 화면
3. 우측 상단 **진행 중** 버튼 클릭
4. Task가 **In Progress** 컬럼으로 이동

### 작업 완료 후

1. Task 상세 화면에서 **리뷰** 버튼 클릭
2. GitHub에 PR 링크 첨부:
   ```
   PR 링크: https://github.com/quirinal36/CleanLLM/pull/1
   ```
3. 코드 리뷰 완료 후 **완료** 버튼 클릭

### Sprint 완료 시

1. **보드** → 우측 상단 **Sprint 완료** 클릭
2. 완료되지 않은 이슈 처리:
   - 다음 Sprint로 이동
   - 백로그로 반환
3. **완료** 클릭

---

## 유용한 Jira 기능

### 1. 필터 사용

**내가 담당한 작업만 보기**:
1. 보드 화면 상단 **필터** 클릭
2. **담당자** → 내 이름 선택

**우선순위 높은 작업만 보기**:
1. 필터 → **우선순위** → Highest, High 선택

### 2. 빠른 이슈 생성

키보드 단축키: `C` (Create)
- 어디서든 `C` 키를 누르면 이슈 생성 다이얼로그 열림

### 3. 이슈 링크

관련 이슈 연결:
1. 이슈 상세 화면 → **링크** 클릭
2. 링크 유형 선택:
   - **차단됨** (is blocked by)
   - **관련됨** (relates to)
   - **복제됨** (duplicates)

### 4. 댓글 및 멘션

팀원에게 알림:
```
@팀원이름 이 부분 확인 부탁드립니다.
```

### 5. 작업 시간 추적

1. 이슈 상세 화면 → **로그 작업** 클릭
2. 소요 시간 입력: `2h 30m`
3. 날짜 및 설명 입력

---

## Sprint 1 티켓 일괄 생성 체크리스트

### Epic 생성
- [ ] EPIC-01: 인프라 및 보안 가드레일 구축

### Story 생성
- [ ] STORY-101: 사용자 인증 시스템
- [ ] STORY-102: 입력 프롬프트 유해성 검사
- [ ] STORY-103: 기본 대화형 UI 및 PII 마스킹

### Story 101 Tasks
- [ ] TASK-101-1: Database Schema 설계
- [ ] TASK-101-2: User Model 작성
- [ ] TASK-101-3: 회원가입 API
- [ ] TASK-101-4: 로그인 API
- [ ] TASK-101-5: 부모-자녀 연동 API
- [ ] TASK-101-6: 단위 테스트
- [ ] TASK-101-7: 회원가입 화면 UI
- [ ] TASK-101-8: 로그인 화면 UI
- [ ] TASK-101-9: Auth API Service
- [ ] TASK-101-10: 토큰 관리 로직

### Story 102 Tasks
- [ ] TASK-102-1: Llama Guard 설치 및 설정
- [ ] TASK-102-2: Safety Service 구현
- [ ] TASK-102-3: Perspective API 연동
- [ ] TASK-102-4: 유해 요청 로그 DB
- [ ] TASK-102-5: Safety Check API
- [ ] TASK-102-6: 단위 테스트

### Story 103 Tasks
- [ ] TASK-103-1: 채팅 화면 레이아웃
- [ ] TASK-103-2: ChatMessage 컴포넌트
- [ ] TASK-103-3: ChatInput 컴포넌트
- [ ] TASK-103-4: TypingIndicator 컴포넌트
- [ ] TASK-103-5: Chat API Service
- [ ] TASK-103-6: 에러 처리
- [ ] TASK-103-7: Azure OpenAI 연동
- [ ] TASK-103-8: PII Detection 로직
- [ ] TASK-103-9: Chat History DB
- [ ] TASK-103-10: Chat API 엔드포인트
- [ ] TASK-103-11: 대화 컨텍스트 관리
- [ ] TASK-103-12: PII 마스킹 테스트

### Sprint 설정
- [ ] Sprint 1 생성
- [ ] 모든 Story를 Sprint 1에 추가
- [ ] Sprint 시작

---

## 📊 Jira 보고서

### Burndown Chart (번다운 차트)

Sprint 진행 상황 확인:
1. **보고서** → **번다운 차트** 선택
2. 이상적인 진행선과 실제 진행선 비교
3. Sprint 목표 달성 가능 여부 판단

### Velocity Chart (속도 차트)

팀의 평균 생산성 확인:
1. **보고서** → **속도 차트** 선택
2. 지난 Sprint들의 완료된 Story Points 확인
3. 다음 Sprint 계획에 활용

---

## 💡 팁 & 모범 사례

### DO ✅
- 매일 Jira 보드 업데이트하기
- Task를 작은 단위로 분해하기
- 댓글로 진행 상황 공유하기
- PR 링크를 Task에 첨부하기
- Sprint Review 전에 모든 Task 상태 정리하기

### DON'T ❌
- 오래된 Task를 방치하지 않기
- 너무 큰 Story 만들지 않기 (13 Points 이상)
- 담당자 없는 Task 만들지 않기
- Sprint 중간에 Story 추가하지 않기 (긴급한 경우 제외)

---

## 🆘 도움말 및 리소스

- **Jira 공식 문서**: https://support.atlassian.com/jira-software-cloud/
- **Jira 튜토리얼 비디오**: https://www.youtube.com/c/Atlassian
- **팀 문의**: 프로젝트 리더(이형구)

---

**문서 작성일**: 2025-12-20
**버전**: 1.0
