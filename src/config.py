from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URI: str
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES: int = 3600
    LOKI_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )

settings = Settings()
