# EduGuard AI - Frontend

청소년을 위한 안전한 AI 학습 플랫폼 프론트엔드

## 📱 기술 스택

- **Framework**: React Native + Expo
- **Language**: TypeScript
- **UI**: React Native Components
- **State Management**: React Hooks
- **Navigation**: React Navigation (예정)
- **HTTP Client**: Axios
- **Data Fetching**: TanStack Query (React Query)

## 🗂️ 프로젝트 구조

```
frontend/
├── src/
│   ├── screens/         # 화면 컴포넌트
│   │   └── SignupScreen.tsx  # 회원가입 화면 ✅
│   ├── components/      # 재사용 가능한 컴포넌트
│   ├── services/        # API 서비스
│   ├── types/           # TypeScript 타입 정의
│   │   └── auth.ts      # 인증 관련 타입 ✅
│   ├── utils/           # 유틸리티 함수
│   │   └── validation.ts # 폼 검증 유틸리티 ✅
│   └── styles/          # 스타일 및 테마
│       └── colors.ts    # 색상 테마 ✅
├── App.tsx              # 앱 진입점
└── package.json         # 의존성 관리
```

## 🎨 디자인 시스템

### 색상 테마
- **Primary**: 파스텔 블루 (`#6B9BD1`) - 청소년 친화적
- **Secondary**: 부드러운 핑크 (`#F0B8D8`)
- **Accent**: 따뜻한 옐로우 (`#FFD88C`)
- **Background**: 밝은 회색 (`#F8F9FA`)

### UI/UX 원칙
- ✅ 밝고 친근한 파스텔 톤 색상
- ✅ 가독성 높은 산세리프 폰트
- ✅ 큰 터치 영역 (최소 50x50px, 권장 44x44px 초과)
- ✅ 부드러운 애니메이션 (페이드인/아웃)
- ✅ 반응형 디자인 (모바일 최적화)

## ✅ 구현 완료 기능 (CLEAN-11)

### 회원가입 화면 (SignupScreen.tsx)

**주요 기능**:
1. ✅ 가입 유형 선택 (학생/부모)
2. ✅ 이메일 입력 및 검증
   - 이메일 형식 확인
   - 실시간 에러 표시
3. ✅ 비밀번호 입력 및 검증
   - 최소 8자 이상
   - 영문 + 숫자 조합 필수
   - 비밀번호 확인 일치 검사
4. ✅ 입력 필드 에러 처리
   - 실시간 검증
   - 사용자 친화적 에러 메시지
5. ✅ 로딩 상태 처리
   - ActivityIndicator 표시
   - 버튼 비활성화
6. ✅ 키보드 처리
   - KeyboardAvoidingView (iOS/Android 대응)
   - 스크롤 가능한 레이아웃

**검증 규칙** (src/utils/validation.ts):
```typescript
// 이메일 검증
- 빈 값 체크
- 이메일 형식 확인 (정규식)

// 비밀번호 검증
- 최소 8자 이상
- 영문 포함 확인
- 숫자 포함 확인

// 비밀번호 확인 검증
- 원본 비밀번호와 일치 확인
```

## 🚀 실행 방법

### 1. 의존성 설치
```bash
cd frontend
npm install
```

### 2. 개발 서버 실행
```bash
# Expo 개발 서버 시작
npm start

# iOS 시뮬레이터
npm run ios

# Android 에뮬레이터
npm run android

# 웹 브라우저
npm run web
```

### 3. 테스트
```bash
npm test
```

## 📋 다음 작업 (예정)

- [ ] **CLEAN-12**: 로그인 화면 UI 구현
- [ ] **CLEAN-13**: Auth API Service 구현
- [ ] **CLEAN-14**: 토큰 저장 및 관리 로직
- [ ] Navigation 설정 (React Navigation)
- [ ] API 연동 (Backend 완료 후)

## 🧪 테스트 시나리오

### 회원가입 화면 테스트
1. ✅ 빈 이메일 입력 시도 → "이메일을 입력해주세요" 에러
2. ✅ 잘못된 이메일 형식 → "올바른 이메일 형식이 아닙니다" 에러
3. ✅ 짧은 비밀번호 (8자 미만) → "최소 8자 이상" 에러
4. ✅ 영문만 or 숫자만 비밀번호 → "영문과 숫자 포함" 에러
5. ✅ 비밀번호 불일치 → "비밀번호가 일치하지 않습니다" 에러
6. ✅ 올바른 입력 → 검증 통과, API 호출 준비

## 📝 Acceptance Criteria 충족 여부

**CLEAN-11 요구사항**:
- ✅ 이메일과 비밀번호 입력 필드
- ✅ 비밀번호 검증 (최소 8자, 영문+숫자)
- ✅ 이메일 검증 (정규식)
- ✅ 회원가입 버튼 (50x50px, 터치 영역 충분)
- ✅ 밝고 친근한 파스텔 톤 색상
- ✅ 가독성 높은 산세리프 폰트
- ✅ 큰 터치 영역 (모든 버튼 50px 이상)
- ✅ 부드러운 애니메이션 (ActivityIndicator)
- ✅ 에러 메시지 표시
- ⏳ API 연동 (CLEAN-13에서 구현 예정)

## 📚 참고 문서

- [Sprint 1 Jira 티켓 명세서](../docs/SPRINT1_JIRA_TICKETS.md)
- [Jira 티켓 생성 요약](../docs/JIRA_CREATED_SUMMARY.md)
- [React Native 공식 문서](https://reactnative.dev/)
- [Expo 공식 문서](https://docs.expo.dev/)

## 🔗 관련 Jira 티켓

- **CLEAN-11**: 회원가입 화면 UI 구현 (Frontend) ✅ 완료
- **CLEAN-2**: [STORY-101] 사용자 인증 시스템 및 부모-자녀 계정 연동

---

**작성일**: 2025-12-22
**담당**: Frontend 개발자
**상태**: ✅ CLEAN-11 구현 완료
