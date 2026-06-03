from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, preferences, categories, seeds

app = FastAPI(
    title="TikTok Title Optimizer",
    description="AI-powered title optimization for Douyin (TikTok) content creators",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1 import optimize, history, dashboard

app.include_router(auth.router, prefix="/api/v1")
app.include_router(preferences.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(optimize.router, prefix="/api/v1")
app.include_router(history.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(seeds.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
