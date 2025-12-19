# 🌿 Git 브랜치 전략 가이드

## 📋 개요

EduGuard AI 프로젝트는 **GitHub Flow 기반의 단순화된 브랜치 전략**을 사용합니다.
소규모 팀(3명)과 2주 스프린트에 최적화된 전략입니다.

## 🌳 브랜치 구조

```
main (프로덕션)
  └── develop (개발 통합)
       ├── feature/sprint1-user-auth
       ├── feature/sprint1-llama-guard
       ├── feature/sprint1-chat-ui
       ├── feature/sprint2-rag-system
       └── bugfix/login-error
```

## 📚 브랜치 종류

### 1. `main` - 프로덕션 브랜치
- **목적**: 항상 배포 가능한 안정적인 코드 유지
- **보호 규칙**:
  - 직접 push 금지
  - PR + Code Review 필수
  - CI/CD 테스트 통과 필수
- **병합 시점**: Sprint 종료 후 develop → main

### 2. `develop` - 개발 통합 브랜치
- **목적**: 개발 중인 기능들의 통합 및 테스트
- **업데이트**: 각 feature 브랜치 완료 시 병합
- **테스트**: 통합 테스트 수행 환경

### 3. `feature/*` - 기능 개발 브랜치
- **네이밍**: `feature/sprint번호-기능명`
  - 예시: `feature/sprint1-user-auth`
  - 예시: `feature/sprint2-rag-vector-db`
- **생성**: develop에서 분기
- **병합**: develop으로 PR

### 4. `bugfix/*` - 버그 수정 브랜치
- **네이밍**: `bugfix/이슈설명`
  - 예시: `bugfix/login-timeout-error`
- **생성**: develop 또는 main에서 분기
- **병합**: 원본 브랜치로 PR

### 5. `hotfix/*` - 긴급 수정 브랜치
- **네이밍**: `hotfix/심각한이슈`
  - 예시: `hotfix/security-vulnerability`
- **생성**: main에서 직접 분기
- **병합**: main과 develop 양쪽 모두

## 🔄 워크플로우

### 일반적인 개발 흐름

```bash
# 1. develop 브랜치로 이동 및 최신화
git checkout develop
git pull origin develop

# 2. 새 기능 브랜치 생성
git checkout -b feature/sprint1-user-auth

# 3. 개발 작업 수행
# ... 코딩 ...

# 4. 변경사항 커밋
git add .
git commit -m "feat: 사용자 인증 API 엔드포인트 구현"

# 5. 원격 저장소에 푸시
git push origin feature/sprint1-user-auth

# 6. GitHub에서 Pull Request 생성
# develop <- feature/sprint1-user-auth

# 7. Code Review 및 승인 대기

# 8. 병합 후 로컬 브랜치 정리
git checkout develop
git pull origin develop
git branch -d feature/sprint1-user-auth
```

## ✅ 커밋 메시지 규칙

### 커밋 메시지 포맷
```
<타입>: <제목>

<본문 (선택사항)>

<푸터 (선택사항)>
```

### 타입 종류
- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅 (기능 변경 없음)
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드 추가/수정
- `chore`: 빌드, 설정 파일 수정

### 예시
```bash
feat: Llama Guard 입력 필터링 기능 구현

- Llama Guard 3 모델 연동
- 유해성 점수 임계값 설정
- 차단 시 사용자 피드백 메시지 추가

Resolves: #42
```

## 🛡️ Pull Request (PR) 규칙

### PR 생성 시 체크리스트
- [ ] 브랜치명이 규칙에 맞는가?
- [ ] 커밋 메시지가 명확한가?
- [ ] 테스트가 모두 통과하는가?
- [ ] 코드 리뷰어를 지정했는가?
- [ ] Jira 티켓 번호를 연결했는가?

### PR 제목 형식
```
[SPRINT-1] feat: 사용자 인증 시스템 구현
```

### PR 설명 템플릿
```markdown
## 📝 변경 사항
- 구현한 기능 요약

## 🔗 관련 이슈
- Jira: EDUGUARD-123
- GitHub Issue: #42

## ✅ 테스트 완료
- [ ] 단위 테스트 통과
- [ ] 통합 테스트 통과
- [ ] 로컬 환경 테스트 완료

## 📸 스크린샷 (UI 변경 시)
(이미지 첨부)

## 💬 리뷰 요청 사항
- 특별히 확인이 필요한 부분
```

## 🚀 Sprint 종료 시 병합 프로세스

### Sprint 완료 후 develop → main 병합

```bash
# 1. develop 브랜치 최신화
git checkout develop
git pull origin develop

# 2. 모든 기능 테스트 확인
# - 단위 테스트
# - 통합 테스트
# - QA 테스트

# 3. main으로 병합 PR 생성
# GitHub에서 main <- develop PR 생성

# 4. 팀 전체 승인 후 병합

# 5. 릴리즈 태그 생성
git checkout main
git pull origin main
git tag -a v0.1.0 -m "Sprint 1 Release"
git push origin v0.1.0
```

## ⚠️ 주의사항

### DO ✅
- 작은 단위로 자주 커밋하기
- PR은 가능한 작게 유지하기 (400줄 이하 권장)
- 코드 리뷰는 24시간 내 완료하기
- 브랜치는 최신 develop 기준으로 업데이트하기

### DON'T ❌
- main 브랜치에 직접 push 하지 않기
- 리뷰 없이 병합하지 않기
- 테스트 실패 상태에서 PR 하지 않기
- 의미 없는 커밋 메시지 사용 ("수정", "test" 등)

## 🔧 충돌 해결 프로세스

```bash
# 1. develop 최신 변경사항 가져오기
git checkout develop
git pull origin develop

# 2. 작업 중인 브랜치로 이동
git checkout feature/my-feature

# 3. develop 변경사항 병합
git merge develop

# 4. 충돌 해결
# ... 충돌 파일 수정 ...

# 5. 해결 후 커밋
git add .
git commit -m "chore: develop 브랜치 변경사항 병합 및 충돌 해결"

# 6. 푸시
git push origin feature/my-feature
```

## 📊 브랜치 관리 도구

### 유용한 Git 명령어

```bash
# 현재 브랜치 확인
git branch

# 원격 브랜치 목록 확인
git branch -r

# 병합된 브랜치 삭제
git branch -d feature/completed-feature

# 브랜치 강제 삭제 (병합되지 않은 경우)
git branch -D feature/abandoned-feature

# 원격 브랜치 삭제
git push origin --delete feature/old-feature

# 브랜치 이름 변경
git branch -m old-name new-name
```

## 🎯 팀 협업 규칙

1. **코드 리뷰는 필수**
   - 최소 1명의 승인 필요
   - 리더(이형구님)는 주요 기능 리뷰

2. **브랜치는 최신 상태 유지**
   - 매일 아침 develop pull
   - PR 전 develop 병합 확인

3. **충돌 발생 시**
   - 즉시 팀에 알림
   - 함께 해결 방안 논의

4. **브랜치 정리**
   - 병합 완료된 브랜치는 즉시 삭제
   - 주 1회 원격 브랜치 정리

---

**질문이 있다면 팀 채널에 공유해주세요!**
