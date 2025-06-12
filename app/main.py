from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .summarizer import summarize

api = FastAPI(title="Scientific Text Summarizer", version="0.1.0")


class SummarizeIn(BaseModel):
    text: str = Field(..., min_length=50)
    min_length: int | None = 50
    max_length: int | None = 200


class SummarizeOut(BaseModel):
    summary: str


@api.post("/summarize", response_model=SummarizeOut)
async def summarize_endpoint(body: SummarizeIn):
    try:
        summary = await summarize(body.text, body.min_length, body.max_length)
        return SummarizeOut(summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api.get("/health")
async def health():
    return {"status": "ok"}
