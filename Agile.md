1) Jira 프로젝트 설정
프로젝트 유형: 소프트웨어 개발 (Scrum)

이슈 계층 구조: Epic > Story > Task > Sub-task

2) 에픽(Epic) 구성 (Backlog의 큰 줄기)
Jira에서 아래와 같이 에픽을 먼저 생성하세요.

[EPIC-01] 인프라 및 보안 가드레일 구축: 서버 환경 세팅 및 필터링 로직 구현.

[EPIC-02] 지능형 교육 엔진 (RAG): 교육 데이터 수집 및 벡터 DB 연동.

[EPIC-03] 확장 기능 개발 (Canvas/Drive): 편집 공간 및 외부 API 연동.

[EPIC-04] 가디언 대시보드 및 알림 시스템: 부모용 앱 기능 구현.

[EPIC-05] UI/UX 고도화 및 품질 검증: 디자인 시스템 적용 및 베타 테스트.

3) 로드맵 (Sprint Planning)
Sprint 1: 기반 다지기 (The Foundation)
목표: MVP를 위한 기본 대화 및 필터링 API 완성.

주요 티켓(Story):

[STORY] 사용자 인증 시스템 및 부모-자녀 계정 연동.

[STORY] 입력 프롬프트 유해성 검사 로직 구현 (Llama Guard).

[STORY] 기본 대화형 UI 및 개인정보 마스킹 처리.

Sprint 2: 스마트 지식 통합 (Knowledge Integration)
목표: 할루시네이션 방지를 위한 RAG 시스템 구축.

주요 티켓(Story):

[STORY] 초중등 교과서 데이터 임베딩 및 Vector DB 적재.

[STORY] 답변 시 출처(Source) 표기 기능 구현.

[STORY] 구글 드라이브 연동 및 문서 텍스트 추출 엔진 개발.

Sprint 3: 창의적 도구 및 안전한 생성 (Creation)
목표: 이미지 생성 및 협업 캔버스 구현.

주요 티켓(Story):

[STORY] 이미지 생성 프롬프트 자동 순화 엔진 개발.

[STORY] 실시간 협업 에디터(Canvas) 프로토타입.

[STORY] 파일 업로드 시 유해 콘텐츠 스캔 시스템.

Sprint 4: 가디언 연결 및 런칭 준비 (Guardian & Launch)
목표: 부모 모니터링 시스템 완성 및 최종 배포.

주요 티켓(Story):

[STORY] 위험 키워드 감지 시 실시간 푸시 알림 서버 구축.

[STORY] 주간 대화 요약 및 관심사 분석 리포트 생성 로직.

[STORY] 최종 QA 및 스토어 등록 준비.

3. 팀 협업 Rule
Daily Stand-up: 매일 아침 15분간 (1) 어제 한 일, (2) 오늘 할 일, (3) 장애물을 공유합니다.

Jira Status: 작업 시작 시 To Do -> In Progress로, 완료 시 Review -> Done으로 즉시 변경합니다.

Definition of Done (DoD): 모든 기능은 유해성 테스트 케이스를 통과해야만 '완료'로 간주합니다.