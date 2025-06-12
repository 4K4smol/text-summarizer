from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    BACKEND: str = Field("workers", env="BACKEND")
    HF_MODEL: str = Field("facebook/bart-large-cnn", env="HF_MODEL")
    HF_CACHE_DIR: str = Field("/models", env="HF_CACHE_DIR")
    CF_API_TOKEN: str = Field(..., env="CF_API_TOKEN")
    CF_ACCOUNT_ID: str = Field(..., env="CF_ACCOUNT_ID")
    RAPIDAPI_KEY: str | None = Field(None, env="RAPIDAPI_KEY")
    RAPIDAPI_HOST: str | None = Field(None, env="RAPIDAPI_HOST")
    PORT: int = Field(8080, env="PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
