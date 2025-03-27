from fastapi import FastAPI
from presentation.api import forms


app = FastAPI(
    title="Custom Forms",
    description="Welcome to Custom Form's API documentation!",
    root_path="/api/v1",
)


@app.get("/healthcheck")
def healthcheck() -> dict:
    return {"status": "ok"}


app.include_router(forms.router)
