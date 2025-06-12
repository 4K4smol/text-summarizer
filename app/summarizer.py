import httpx
from .settings import settings

_httpx_client: httpx.AsyncClient | None = None

def _get_client() -> httpx.AsyncClient:
    global _httpx_client
    if _httpx_client is None:
        _httpx_client = httpx.AsyncClient(timeout=30.0)
    return _httpx_client

async def _summarize_workers(text: str, min_length: int, max_length: int) -> str:
    url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ACCOUNT_ID}/workers/summarize"
    headers = {
        "Authorization": f"Bearer {settings.CF_API_TOKEN}",
        "Content-Type": "application/json",
    }
    resp = await _get_client().post(
        url,
        json={"text": text, "min_length": min_length, "max_length": max_length},
    )
    resp.raise_for_status()
    return resp.json().get("summary", "")

async def _summarize_rapidapi(text: str, min_length: int, max_length: int) -> str:
    if not settings.RAPIDAPI_KEY or not settings.RAPIDAPI_HOST:
        raise RuntimeError("Faltan credenciales de RapidAPI")
    url = f"https://{settings.RAPIDAPI_HOST}/summarize"
    headers = {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": settings.RAPIDAPI_HOST,
        "Content-Type": "application/json",
    }
    resp = await _get_client().post(
        url,
        json={"text": text, "min_length": min_length, "max_length": max_length},
    )
    resp.raise_for_status()
    return resp.json().get("summary", "")

async def summarize(text: str, min_length: int, max_length: int) -> str:
    if settings.BACKEND == "workers":
        return await _summarize_workers(text, min_length, max_length)
    if settings.BACKEND == "rapidapi":
        return await _summarize_rapidapi(text, min_length, max_length)
    raise RuntimeError(f"Backend no soportado en Render Free: {settings.BACKEND}")
