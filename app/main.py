from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import contacts, auth, user

app = FastAPI()

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