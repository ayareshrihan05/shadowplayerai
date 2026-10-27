"""
ShadowPlayer AI — FastAPI Backend Entry Point & Production Static Server
All data served is synthetic and fictional.
"""
from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Load .env before importing anything that reads env vars
load_dotenv()

from api.routes import health, matches, players, sequences, reports  # noqa: E402
from database.db import init_db, is_seeded, populate_cache  # noqa: E402
from database.seed import run_seed  # noqa: E402

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("shadowplayer")

FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"
STATIC_DIR = Path(__file__).parent / "static"


# Initialize DB and populate in-memory cache on startup
init_db()
if not is_seeded():
    logger.info("Database empty — running synthetic match seed...")
    run_seed()
populate_cache()
logger.info("Cache ready. Serving synthetic match data.")


app = FastAPI(
    title="ShadowPlayer AI",
    description="Off-ball football analytics platform. All data is synthetic and fictional.",
    version="1.0.0",
)

cors_origins = [
    origin.strip()
    for origin in os.getenv("API_CORS_ORIGINS", "http://localhost:5173,http://localhost:8000,http://127.0.0.1:8000").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── API Routes (Precedence over static files) ──────────────────────────────
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(matches.router, prefix="/api", tags=["Matches"])
app.include_router(players.router, prefix="/api", tags=["Players"])
app.include_router(sequences.router, prefix="/api", tags=["Sequences"])
app.include_router(reports.router, prefix="/api", tags=["Reports"])


# ── Production Frontend SPA Serving ───────────────────────────────────────
# Locate the frontend dist directory (either local repo layout or Docker layout)
dist_path = FRONTEND_DIST if FRONTEND_DIST.exists() else (STATIC_DIR if STATIC_DIR.exists() else None)

if dist_path and dist_path.exists():
    logger.info("Mounting frontend SPA from: %s", dist_path)

    # Mount static assets if they exist (JS, CSS, images)
    assets_path = dist_path / "assets"
    if assets_path.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str, request: Request):
        # Prevent intercepting /api or /docs /openapi.json
        if full_path.startswith("api/") or full_path in ("docs", "redoc", "openapi.json"):
            return JSONResponse(status_code=404, content={"error": "Not Found"})

        # If a specific static file at dist root exists (e.g. vite.svg, favicon.ico), serve it
        candidate_file = dist_path / full_path
        if candidate_file.is_file():
            return FileResponse(candidate_file)

        # Fallback to index.html for SPA client-side routing (HTML5 history mode)
        index_file = dist_path / "index.html"
        if index_file.is_file():
            return FileResponse(index_file)

        return JSONResponse(status_code=404, content={"error": "Frontend build index.html not found"})
else:
    logger.warning("Frontend dist directory not found. Run `npm run build` in frontend/ to serve SPA.")

    @app.get("/", include_in_schema=False)
    async def root_fallback():
        return {
            "name": "ShadowPlayer AI API",
            "status": "online",
            "message": "Frontend not built yet. Run `cd frontend && npm run build` to enable UI.",
            "docs_url": "/docs",
        }
