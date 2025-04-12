import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from src.auth.router import router as auth_router
from src.secrets.router import router as secret_router
from logging.config import fileConfig
from src.logging_config import setup_logging
from src.redis import RedisClient
from redis.asyncio import Redis
from src.config import settings


app = FastAPI(
    title="Referral System API",
    description="API для управления реферальной системой",
    version="1.0.0",
)


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(secret_router, prefix="/secret", tags=["secrets"])

@app.on_event("startup")
async def startup_event():
    fileConfig("logging.ini", disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    setup_logging(test_mode=False)
    logger.info("Application starting up")
    
    await RedisClient.init(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD
    )
    
@app.on_event("shutdown")
async def shutdown_event():
    await RedisClient.close()
    
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger = logging.getLogger(__name__)
    logger.error(f"Internal Server Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )