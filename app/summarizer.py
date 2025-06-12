import asyncio
from functools import lru_cache
from typing import Optional

import httpx

from .settings import settings


@lru_cache()
def _load_local_pipeline():
    # Importar transformers solo si se usa el backend "hf"
    from transformers import pipeline
    return pipeline(
        "summarization",
        model=settings.HF_MODEL,
        device_map="auto",
        cache_dir=settings.HF_CACHE_DIR,
    )


async def _summarize_hf(text: str, min_length: int, max_length: int) -> str:
    pipe = _load_local_pipeline()
    # Ejecutar la inferencia en un thread pool
    result = await asyncio.to_thread(
        lambda: pipe(
            text,
            min_length=min_length,
            max_length=max_length,
        )[0]["summary_text"]
    )
    return result.strip()


_httpx_client: Optional[httpx.AsyncClient] = None


def _get_httpx_client() -> httpx.AsyncClient:
    global _httpx_client
    if _httpx_client is None:
        _httpx_client = httpx.AsyncClient(timeout=30.0)
    return _httpx_client


async def _summarize_workers(text: str, min_length: int, max_length: int) -> str:
    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{settings.CF_ACCOUNT_ID}/workers/summarize"
    )
    headers = {
        "Authorization": f"Bearer {settings.CF_API_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"text": text, "min_length": min_length, "max_length": max_length}
    client = _get_httpx_client()
    resp = await client.post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data.get("summary") or data.get("result") or ""


async def _summarize_rapidapi(text: str, min_length: int, max_length: int) -> str:
    if not settings.RAPIDAPI_KEY or not settings.RAPIDAPI_HOST:
        raise RuntimeError("Faltan credenciales de RapidAPI")
    url = f"https://{settings.RAPIDAPI_HOST}/summarize"
    headers = {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": settings.RAPIDAPI_HOST,
        "Content-Type": "application/json",
    }
    payload = {"text": text, "min_length": min_length, "max_length": max_length}
    client = _get_httpx_client()
    resp = await client.post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data.get("summary") or data.get("result") or ""


async def summarize(text: str, min_length: int, max_length: int) -> str:
    match settings.BACKEND:
        case "hf":
            return await _summarize_hf(text, min_length, max_length)
        case "workers":
            return await _summarize_workers(text, min_length, max_length)
        case "rapidapi":
            return await _summarize_rapidapi(text, min_length, max_length)
        case other:
            raise ValueError(f"BACKEND no válido: {other}")
