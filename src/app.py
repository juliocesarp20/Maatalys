from fastapi import FastAPI, Request
from src.logger import configure_logging
from src.auth.routers import router as auth_router
from src.user.routers import router as user_router
from src.investigation.routers import router as investigation_router
import logging
from pydantic_settings import BaseSettings
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.middleware.db_middleware import DBSessionMiddleware
from src.db.base import Base
from src.db.session import engine

class AppSettings(BaseSettings):
    LOG_LEVEL: str = "INFO"

settings = AppSettings()

configure_logging(log_level=settings.LOG_LEVEL)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid input"},
    )

logger = logging.getLogger(__name__)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(investigation_router, prefix="/investigation", tags=["Investigation"])
app.include_router(investigation_router, prefix="/investigation", tags=["Investigation"])
app.add_middleware(DBSessionMiddleware)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the API"}
