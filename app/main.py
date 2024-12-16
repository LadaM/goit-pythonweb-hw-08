"""
Main module for the FastAPI application.

Includes routers for authentication, contacts, and user management.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import contacts, auth, user
from redis import asyncio as aioredis
from app.config import Config

# Global Redis client
redis_client = aioredis.from_url(Config.REDIS_URL, decode_responses=True)

app = FastAPI()
@app.on_event("startup")
async def startup_event():
    await redis_client.ping()
    print("Connected to Redis!")

@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.close()
    print("Disconnected from Redis!")

# for now allow all origins
allowed_origins = ["*"]

# Healthcheck
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # all methods allowed
    allow_headers=["*"],  # all HTTP headers allowed
)

# Include routers
app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(user.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)