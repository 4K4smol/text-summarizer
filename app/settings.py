from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BACKEND: str = "workers"          # "workers" o "hf"
    MAX_TOKENS: int = 1024

    HF_MODEL: str = "facebook/bart-large-cnn"

    CF_ACCOUNT_ID: str | None = None
    CF_API_TOKEN: str | None = None
    CF_MODEL: str = "@hf/thebloke/distilbart-cnn-6-6"

    class Config:
        env_file = ".env"


settings = Settings()
