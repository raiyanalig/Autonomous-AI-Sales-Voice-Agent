"""Application settings loaded from environment variables (.env).

Uses pydantic-settings so configuration is typed, validated and fail-fast.
Development and production differ through APP_ENV and per-environment .env files.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration.

    All values can be overridden with environment variables or a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "SalesPilot AI"
    app_env: str = "development"  # development | staging | production
    api_version: str = "v1"
    app_version: str = "0.1.0"
    debug: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS - comma separated list of allowed frontend origins
    backend_cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Logging
    log_level: str = "INFO"

    @property
    def cors_origin_list(self) -> list[str]:
        """Return CORS origins as a cleaned list."""
        return [o.strip() for o in self.backend_cors_origins.split(",") if o.strip()]

    def validate_runtime(self) -> None:
        """Validate critical configuration at startup (fail fast)."""
        if self.app_env == "production" and self.debug:
            raise ValueError("DEBUG must be False when APP_ENV=production")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (parsed once per process)."""
    return Settings()


settings = get_settings()
