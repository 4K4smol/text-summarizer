import asyncio, httpx
from functools import lru_cache
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from .settings import settings


@lru_cache(maxsize=1)
def _load_local_pipeline():
    model = AutoModelForSeq2SeqLM.from_pretrained(settings.HF_MODEL)
    tok = AutoTokenizer.from_pretrained(settings.HF_MODEL)
    return pipeline("summarization", model=model, tokenizer=tok)


async def summarize(text: str, min_length: int = 50, max_length: int | None = None) -> str:
    max_length = max_length or settings.MAX_TOKENS

    if settings.BACKEND == "hf":
        pipe = _load_local_pipeline()
        summaries = await asyncio.to_thread(
            pipe,
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
        )
        return summaries[0]["summary_text"]

    if settings.BACKEND == "workers":
        base = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ACCOUNT_ID}/ai/run/{settings.CF_MODEL}"
        headers = {"Authorization": f"Bearer {settings.CF_API_TOKEN}"}
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(base, json={"text": text}, headers=headers)
            res.raise_for_status()
            return res.json()["result"]["summary"]

    raise RuntimeError("BACKEND must be 'hf' or 'workers'")
