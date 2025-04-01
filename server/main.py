from fastapi import FastAPI, Request
import database
from database import models, init_db
from tortoise import Tortoise, run_async
import time

app = FastAPI()

# Startup event to initialize database
@app.on_event("startup")
async def startup_event():
    await init_db()

# Shutdown event to close database connections
@app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()


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
