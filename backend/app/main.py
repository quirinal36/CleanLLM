"""
EduGuard AI - Main Application Entry Point
청소년 안전 LLM 서비스 백엔드 메인 파일
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title=os.getenv("APP_NAME", "EduGuard AI"),
    version=os.getenv("APP_VERSION", "0.1.0"),
    description="청소년을 위한 안전한 AI 학습 플랫폼",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Production에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "EduGuard AI Backend",
        "version": os.getenv("APP_VERSION", "0.1.0"),
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "ok",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "debug": os.getenv("DEBUG", "False"),
    }


# Import and include API routers
from app.api import auth_router

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
# TODO: Add other routers
# from app.api import chat, safety
# app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
# app.include_router(safety.router, prefix="/api/v1/safety", tags=["safety"])


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True if os.getenv("DEBUG", "False") == "True" else False,
    )
