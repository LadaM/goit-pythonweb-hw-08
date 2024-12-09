from fastapi import FastAPI
from app.api.routers import contacts

app = FastAPI()

# Healthcheck
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}

# Include a router to contacts
app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)