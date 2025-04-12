from fastapi import FastAPI, Request
import database
from database import models, init_db
from tortoise import Tortoise, run_async
import time
from endpoints import auth, scenario

app = FastAPI()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database
    await init_db()
    yield
    # Shutdown: close database connections
    await Tortoise.close_connections()

app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def index():
    return {"Hello": "World"}

# Include routers
app.include_router(auth.router, prefix="/auth")
app.include_router(scenario.router, prefix="/scenario")

