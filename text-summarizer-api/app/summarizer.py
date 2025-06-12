import json
import httpx
from .settings import settings

_httpx_client: httpx.AsyncClient | None = None

def _get_client() -> httpx.AsyncClient:
    global _httpx_client
    if _httpx_client is None:
        _httpx_client = httpx.AsyncClient(timeout=30.0)
    return _httpx_client

async def _summarize_workers(text: str, min_length: int, max_length: int) -> str:
    url = f"{settings.WORKER_URL}/summarize"
    headers = {
        "Authorization": f"Bearer {settings.CF_API_TOKEN}",  # si tu Worker lo exige
        "Content-Type": "application/json",
    }
    payload = {"text": text, "min_length": min_length, "max_length": max_length}
    client = _get_client()
    resp = await client.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data.get("summary", "")

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
    client = _get_client()
    resp = await client.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data.get("summary", "")

async def summarize(text: str, min_length: int, max_length: int) -> str:
    if settings.BACKEND == "workers":
        return await _summarize_workers(text, min_length, max_length)
    if settings.BACKEND == "rapidapi":
        return await _summarize_rapidapi(text, min_length, max_length)
    raise RuntimeError(f"Backend no soportado en Render Free: {settings.BACKEND}")
