# 📄 PRD: EduGuard AI (청소년 안전 LLM 서비스)

## 1. 프로젝트 개요
- **비전**: 미성년자가 AI의 위험(할루시네이션, 편향성, 유해물) 없이 잠재력을 탐색할 수 있는 '안전한 디지털 운동장' 구축.
- **핵심 원칙 (제1 사고원칙)**: AI 모델에 의존하는 것이 아니라, 기술적 샌드박스와 가드레일을 통해 위험을 원천 차단한다.

## 2. 주요 기능 (Core Features)
### [Phase 1: Foundation]
- **Safety Guardrails**: Llama Guard 3 및 Perspective API를 이용한 입출력 필터링.
- **RAG Core**: 검증된 교육 데이터(교과서, 백과사전) 기반의 근거 있는 답변 생성.
- **PII Masking**: 개인정보 자동 식별 및 마스킹 처리.

### [Phase 2: Power Tools]
- **Safe Image Gen**: 실사 인물 제외, 교육적 삽화 위주의 이미지 생성 및 프롬프트 순화.
- **Edu Canvas**: AI와 협업하는 실시간 에세이/코딩 에디터.
- **File & Drive Integration**: 구글 드라이브 및 문서(PDF/Docx) 안전 스캔 및 요약.

### [Phase 3: Guardian]
- **Parent Dashboard**: 위험 키워드 알림, 관심사 분석 리포트, 기능 제어 토글.

## 3. 기술 스택 (Tech Stack)
- **Frontend**: React Native (Cross-platform)
- **Backend**: Python (FastAPI), LangGraph
- **AI/LLM**: Azure OpenAI (GPT-4o), Pinecone (Vector DB)
- **Safety**: Llama Guard 3, Google Perspective API
- **Infra**: AWS or Azure

## 4. 성공 지표 (KPI)
1. 유해 답변 차단율: 99.9% 이상
2. 할루시네이션 발생률: 5% 미만 (RAG 적용 기준)
3. 사용자 유지율(Retention): 주간 활성 사용자(WAU) 대비 40% 이상