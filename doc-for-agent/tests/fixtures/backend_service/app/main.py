from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/events")
def ingest_event() -> dict[str, str]:
    return {"accepted": "true"}
