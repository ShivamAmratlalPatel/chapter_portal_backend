"""Main module for the backend FastAPI application."""
import logging
import os
import re
import tracemalloc

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse

from backend.chapters.chapters_routes import chapters_router

from .actions.actions_routes import actions_router
from .allocations.allocation_routes import allocations_router
from .committees.committee_routes import committee_router
from .config import CORS_ORIGINS
from .events.event_routes import event_router
from .health.health_routes import health_router
from .inventory.inventory_routes import inventory_router
from .meetings.meetings_routes import meetings_router
from .middleware import ContentSizeLimitMiddleware
from .updates.update_routes import update_router
from .users.users_routes import users_router
from .visits.visits_routes import visit_router

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)

app = FastAPI(
    title="NHSF Backend",
    version="0.1.0",
    description="Backend for the NHSF application.",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:  # pragma: no cover
    """
    Handle validation errors.

    Args:
        request: request
        exc: RequestValidationError object

    Returns:
        JSONResponse: response
    """
    _ = request
    logger.error(jsonable_encoder({"detail": exc.errors(), "body": exc.body}))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


cors_origins = CORS_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ContentSizeLimitMiddleware, max_content_size=10_000_000)

app.include_router(actions_router)
app.include_router(allocations_router)
app.include_router(chapters_router)
app.include_router(committee_router)
app.include_router(event_router)
app.include_router(health_router)
app.include_router(inventory_router)
app.include_router(meetings_router)
app.include_router(update_router)
app.include_router(users_router)
app.include_router(visit_router)


@app.get(
    "/health",
    tags=["health"],
    responses={
        status.HTTP_200_OK: {
            "description": "Health check",
            "content": {"application/json": {"example": {"status": "ok"}}},
        },
    },
)
async def health() -> str:
    """
    Health check.

    Returns
        str: "ok"
    """
    return "ok"


first_trace = None


@app.get("/tracemalloc", response_class=PlainTextResponse)
def trace(n: int = 10, filter_: str = ".*", v: bool = False) -> str:
    """
    Trace memory allocations.

    Args:
        n: number of top entries to show
        filter_: regex to filter entries by
        v: verbose

    Returns:
        str: trace
    """
    global first_trace

    # On first call: create reference point
    if not first_trace:
        tracemalloc.start()
        first_trace = tracemalloc.take_snapshot()
        return "First snapshot taken!\n"
    else:  # pragma: no cover
        # Subsequent calls: show changes
        top_stats = tracemalloc.take_snapshot().compare_to(first_trace, "lineno")
        top_stats = [t for t in top_stats if re.search(filter_, str(t))]
        if not v:
            return "\n".join([str(stat) for stat in top_stats[:n]])
        lines = []
        for stat in top_stats[:n]:
            lines.append(str(stat))
            lines.append(f"{stat.count} memory blocks: {stat.size / 1024:.1f} KiB")
            for line in stat.traceback.format():
                lines.append(line)
            lines.append("")
        return "\n".join(lines)


@app.get("/migrate_db", response_class=PlainTextResponse)
def migrate_db() -> str:
    """
    Migrate the database.

    Returns
        str: migration output
    """
    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    return "Database migrated!"


@app.get("/generate_migrations", response_class=PlainTextResponse)
def generate_migrations() -> str:
    """Generate new migrations"""
    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, "head", autogenerate=True)
    return "Migrations generated!"
