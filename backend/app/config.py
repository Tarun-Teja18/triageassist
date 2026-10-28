"""Application configuration, loaded from the environment.

Every tunable value and every secret enters the app through this one module.
Nothing else in the codebase reads os.environ directly — that way there is a
single place to look to answer "what can be configured?", and a single place
where a typo'd variable name can hide.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# .env lives at the repository root, one level above backend/.
# Resolving it from __file__ rather than the current working directory means
# the app finds it no matter which folder uvicorn was launched from.
#   __file__ = backend/app/config.py
#   parents[0] = backend/app   parents[1] = backend   parents[2] = repo root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """Typed application settings.

    Values are read from real environment variables first, then from .env.
    That precedence matters for deployment: on Hugging Face Spaces there is no
    .env file at all — the platform injects real environment variables, and
    this class picks them up with no code change.
    """

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",  # ignore unrelated variables rather than crashing
    )

    # Secret. Defaults to empty rather than being required, so the app can
    # still start and serve /health without a key — we fail at call time with
    # a clear message instead of refusing to boot.
    groq_api_key: str = ""

    # Groq retires models periodically; keeping this configurable means a
    # retirement is an .env edit, not a code change.
    groq_model: str = "llama-3.3-70b-versatile"

    # Fail a hung request rather than letting it pile up connections.
    llm_timeout_seconds: float = 30.0

    @property
    def groq_configured(self) -> bool:
        return bool(self.groq_api_key and self.groq_api_key.startswith("gsk_"))


@lru_cache
def get_settings() -> Settings:
    """Return the settings singleton.

    @lru_cache makes this run once per process; every later call gets the same
    object back. Without it, FastAPI would re-read and re-parse .env on every
    single request. This function is also the seam used for dependency
    injection — see the Depends(...) usage in main.py.
    """
    return Settings()
