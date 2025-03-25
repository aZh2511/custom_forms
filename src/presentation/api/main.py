from fastapi import FastAPI

app = FastAPI(
    title="Custom Forms",
    description="Welcome to Custom Form's API documentation!",
    root_path="/api/v1",
)


@app.get('/healthcheck')
def healthcheck() -> dict:
    return {'status': 'ok'}
