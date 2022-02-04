from . import create_app

app = create_app()


@app.get("/health")
async def health():
    return {"message": "ok"}
