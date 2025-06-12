from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    BACKEND: str = Field("workers", env="BACKEND")
    # Solo backends I/O-bound:
    CF_ACCOUNT_ID: str = Field(..., env="CF_ACCOUNT_ID")
    CF_API_TOKEN: str = Field(..., env="CF_API_TOKEN")
    RAPIDAPI_KEY: str | None = Field(None, env="RAPIDAPI_KEY")
    RAPIDAPI_HOST: str | None = Field(None, env="RAPIDAPI_HOST")
    PORT: int = Field(8080, env="PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
