import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx

from .settings import settings
from .summarizer import summarize

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Text Summarizer API",
    version="1.0.0",
    description="Resúmenes vía Cloudflare Workers o RapidAPI",
)

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=5000)
    min_length: int = Field(50, ge=1)
    max_length: int = Field(200, ge=1)

class SummarizeResponse(BaseModel):
    summary: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/summarize", response_model=SummarizeResponse)
async def api_summarize(req: SummarizeRequest):
    try:
        return SummarizeResponse(summary=await summarize(req.text, req.min_length, req.max_length))
    except httpx.HTTPStatusError:
        logger.error("Error en servicio externo")
        raise HTTPException(status_code=502, detail="Error en servicio externo")
    except RuntimeError as e:
        logger.warning(f"Configuración inválida: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        log_level="info",
        workers=2,
    )
