import asyncio
import logging

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

from .settings import settings
from .summarizer import summarize

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Text Summarizer API",
    version="1.0.0",
    description="Un microservicio para resumir texto, con backends HF, Workers o RapidAPI",
)


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=5000)
    min_length: int = Field(50, ge=1)
    max_length: int = Field(200, ge=1)


class SummarizeResponse(BaseModel):
    summary: str


@app.on_event("startup")
async def on_startup():
    # Precarga del modelo local para evitar latencia en la primera petición
    if settings.BACKEND == "hf":
        logger.info("Precargando pipeline HF...")
        await asyncio.to_thread(_load := __import__("app.summarizer", fromlist=["_load_local_pipeline"])._load_local_pipeline)


@app.get("/health", response_model=dict)
async def health():
    return {"status": "ok"}


@app.post("/summarize", response_model=SummarizeResponse)
async def api_summarize(req: SummarizeRequest):
    try:
        summary = await summarize(req.text, req.min_length, req.max_length)
        return SummarizeResponse(summary=summary)
    except httpx.HTTPStatusError as e:
        logger.error(f"Error en servicio externo: {e}")
        raise HTTPException(status_code=502, detail="Error en servicio externo")
    except (ValidationError, ValueError, RuntimeError) as e:
        logger.warning(f"Error de entrada o configuración: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        log_level="info",
        # Si usas HF local, 1 worker para ahorrar RAM; si es workers/rapidapi, más concurrencia
        workers=1 if settings.BACKEND == "hf" else 2,
    )
