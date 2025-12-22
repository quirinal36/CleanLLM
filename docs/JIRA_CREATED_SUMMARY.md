# ✅ Jira 티켓 생성 완료 요약

## 🎯 생성 완료 현황

**프로젝트**: CleanLLM (CLEAN)
**Jira URL**: https://letscoding.atlassian.net/jira/software/projects/CLEAN
**생성일**: 2025-12-20

---

## 📊 생성된 티켓 통계

### 총 티켓 수: **33개**

- **Epic**: 1개
- **Story**: 3개 (총 29 Story Points)
- **Task**: 29개

---

## 🏗️ Epic

### CLEAN-1: [EPIC-01] 인프라 및 보안 가드레일 구축

**설명**: 청소년 안전을 위한 기술적 기반 구축. 서버 환경 세팅 및 유해성 필터링 로직 구현.

**성공 지표**:
- 유해 답변 차단율 99% 이상
- API 응답 시간 3초 이내
- 시스템 가동률 99% 이상

**포함된 Story**: CLEAN-2, CLEAN-3, CLEAN-4

---

## 📝 Story 목록

### CLEAN-2: [STORY-101] 사용자 인증 시스템 및 부모-자녀 계정 연동

**Story Points**: 8
**우선순위**: Highest
**담당**: Backend 개발자

**하위 Task (10개)**:
1. CLEAN-5: Database Schema 설계 및 생성
2. CLEAN-6: User Model 및 Pydantic Schema 작성
3. CLEAN-7: 회원가입 API 엔드포인트 구현
4. CLEAN-8: 로그인 API 엔드포인트 구현
5. CLEAN-9: 부모-자녀 연동 API 구현
6. CLEAN-10: 인증 API 단위 테스트 작성
7. ✅ CLEAN-11: 회원가입 화면 UI 구현 (Frontend) - **완료**
8. CLEAN-12: 로그인 화면 UI 구현 (Frontend)
9. CLEAN-13: Auth API Service 구현 (Frontend)
10. CLEAN-14: 토큰 저장 및 관리 로직 (Frontend)

**Acceptance Criteria**:
- ✅ 이메일/비밀번호 회원가입 (최소 8자, 영문+숫자)
- ✅ JWT 토큰 기반 로그인 (30분 유효)
- ✅ 부모-자녀 계정 연동 (최대 3개)
- ✅ API 응답 시간 1초 이내

---

### CLEAN-3: [STORY-102] 입력 프롬프트 유해성 검사 로직 구현 (Llama Guard)

**Story Points**: 13
**우선순위**: Highest
**담당**: Backend 개발자

**하위 Task (6개)**:
1. CLEAN-15: Llama Guard 3 라이브러리 설치 및 설정
2. CLEAN-16: Safety Service 클래스 구현
3. CLEAN-17: Google Perspective API 연동
4. CLEAN-18: 유해 요청 로그 DB 스키마 생성
5. CLEAN-19: Safety Check API 엔드포인트 구현
6. CLEAN-20: 유해성 검사 단위 테스트 작성

**Acceptance Criteria**:
- ✅ 유해성 점수 0.8 이상 차단
- ✅ 5개 카테고리 검사 (폭력, 성적, 혐오, 자해, 불법)
- ✅ Llama Guard 실패 시 Perspective API 대체
- ✅ 모든 유해 요청 DB 로그 저장
- ✅ 검사 응답 시간 2초 이내

---

### CLEAN-4: [STORY-103] 기본 대화형 UI 및 개인정보 마스킹 처리

**Story Points**: 8
**우선순위**: High
**담당**: Frontend + Backend 협업

**하위 Task (13개)**:

**Frontend (6개)**:
1. CLEAN-21: 채팅 화면 레이아웃 구현
2. CLEAN-22: ChatMessage 컴포넌트 구현
3. CLEAN-23: ChatInput 컴포넌트 구현
4. CLEAN-24: TypingIndicator 컴포넌트 구현
5. CLEAN-25: Chat API Service 구현
6. CLEAN-26: 에러 처리 및 사용자 피드백

**Backend (7개)**:
7. CLEAN-27: Azure OpenAI GPT-4o 연동
8. CLEAN-28: PII Detection 및 Masking 로직 구현
9. CLEAN-29: Chat History DB 스키마 생성
10. CLEAN-30: Chat API 엔드포인트 구현
11. CLEAN-31: 대화 컨텍스트 관리 로직
12. CLEAN-32: PII 마스킹 단위 테스트
13. CLEAN-33: 채팅 API 통합 테스트

**Acceptance Criteria**:

**Frontend**:
- ✅ 텍스트 입력창 및 전송 버튼
- ✅ 대화 히스토리 스크롤 리스트
- ✅ "생각 중..." 로딩 표시
- ✅ 에러 메시지 표시
- ✅ 좌(사용자)/우(AI) 메시지 구분

**Backend**:
- ✅ GPT-4o API 정상 연동
- ✅ 전화번호: `010-****-****`
- ✅ 이메일: `u***@example.com`
- ✅ 주민등록번호: `******-*******`
- ✅ 최대 10개 대화 컨텍스트 유지
- ✅ 모든 대화 DB 저장
- ✅ API 응답 시간 5초 이내

---

## 📅 Sprint 1 일정 (2주)

### Week 1 (Day 1-7)
- **Day 1-2**: 환경 설정 + Story 101 시작
- **Day 3-4**: Story 101 핵심 기능 구현
- **Day 5**: Story 101 완료 및 통합 테스트
- **Day 6-7**: Story 102 시작

### Week 2 (Day 8-14)
- **Day 8-9**: Story 102 완료
- **Day 10-11**: Story 103 시작
- **Day 12-13**: Story 103 완료
- **Day 14**: Sprint Review & Retrospective

---

## 👥 역할별 작업 분배

### Backend 개발자 (19개 Task)
**Story 101 (6개)**:
- CLEAN-5: DB Schema
- CLEAN-6: User Model
- CLEAN-7: 회원가입 API
- CLEAN-8: 로그인 API
- CLEAN-9: 부모-자녀 연동 API
- CLEAN-10: 단위 테스트

**Story 102 (6개)**:
- CLEAN-15: Llama Guard 설치
- CLEAN-16: Safety Service
- CLEAN-17: Perspective API
- CLEAN-18: 로그 DB
- CLEAN-19: Safety API
- CLEAN-20: 단위 테스트

**Story 103 (7개)**:
- CLEAN-27: OpenAI 연동
- CLEAN-28: PII 마스킹
- CLEAN-29: Chat DB
- CLEAN-30: Chat API
- CLEAN-31: 컨텍스트 관리
- CLEAN-32: PII 테스트
- CLEAN-33: 통합 테스트

### Frontend 개발자 (10개 Task)
**Story 101 (4개)**:
- ✅ CLEAN-11: 회원가입 UI - **완료 (2025-12-22)**
- CLEAN-12: 로그인 UI
- CLEAN-13: Auth API Service
- CLEAN-14: 토큰 관리

**Story 103 (6개)**:
- CLEAN-21: 채팅 화면
- CLEAN-22: ChatMessage 컴포넌트
- CLEAN-23: ChatInput 컴포넌트
- CLEAN-24: TypingIndicator 컴포넌트
- CLEAN-25: Chat API Service
- CLEAN-26: 에러 처리

---

## 🔗 Jira 바로가기 링크

### Epic & Stories
- [CLEAN-1: Epic - 인프라 및 보안](https://letscoding.atlassian.net/browse/CLEAN-1)
- [CLEAN-2: Story 101 - 사용자 인증](https://letscoding.atlassian.net/browse/CLEAN-2)
- [CLEAN-3: Story 102 - 유해성 검사](https://letscoding.atlassian.net/browse/CLEAN-3)
- [CLEAN-4: Story 103 - 채팅 UI](https://letscoding.atlassian.net/browse/CLEAN-4)

### 백로그 & 보드
- [프로젝트 백로그](https://letscoding.atlassian.net/jira/software/projects/CLEAN/boards)
- [칸반 보드](https://letscoding.atlassian.net/jira/software/projects/CLEAN/board)

---

## ✅ 다음 단계

### 1. Sprint 생성
```
Sprint 이름: Sprint 1 - The Foundation
기간: 2주 (예: 2025-12-23 ~ 2026-01-05)
목표: MVP를 위한 기본 대화 및 필터링 API 완성
```

### 2. Story를 Sprint에 추가
- Jira 백로그 화면에서
- CLEAN-2, CLEAN-3, CLEAN-4를 드래그하여 Sprint 1에 추가

### 3. Sprint 시작
- Sprint 영역 우측 상단 "Sprint 시작" 클릭

### 4. Task 배정
- 각 Task를 팀원에게 할당
- Backend 개발자: 19개 Task
- Frontend 개발자: 10개 Task

### 5. 작업 시작
- 팀원들이 To Do → In Progress로 상태 변경
- 매일 Daily Stand-up 진행

---

## 📝 주요 문서 참고

- [SPRINT1_JIRA_TICKETS.md](SPRINT1_JIRA_TICKETS.md) - 상세 티켓 명세서
- [JIRA_QUICKSTART.md](JIRA_QUICKSTART.md) - Jira 사용 가이드
- [GIT_STRATEGY.md](GIT_STRATEGY.md) - Git 브랜치 전략
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 개발 환경 설정

---

## 🎯 Sprint 1 성공 기준

### 기능적 목표
- ✅ 사용자 회원가입/로그인 가능
- ✅ 유해 프롬프트 99% 이상 차단
- ✅ AI와 안전한 대화 가능
- ✅ 개인정보 자동 마스킹

### 기술적 목표
- ✅ 모든 API 응답 시간 기준 충족
- ✅ 단위 테스트 커버리지 80% 이상
- ✅ 코드 리뷰 100% 완료
- ✅ develop 브랜치 병합 완료

### 팀 목표
- ✅ Daily Stand-up 100% 참여
- ✅ Sprint Review 데모 준비
- ✅ Retrospective 액션 아이템 도출

---

**생성 완료일**: 2025-12-20
**생성자**: EduGuard AI Team (with Claude Code)
**버전**: 1.0
