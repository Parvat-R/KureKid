from fastapi import FastAPI
import database
from database import models, init_db
from tortoise import Tortoise, run_async

app = FastAPI()

# Startup event to initialize database
@app.on_event("startup")
async def startup_event():
    await init_db()

# Shutdown event to close database connections
@app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()

@app.get("/")
async def index():
    return {"Hello": "World"}
