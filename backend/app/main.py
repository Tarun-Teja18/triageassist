"""TriageAssist API — application entry point.

Step 1: a single health endpoint, so we can confirm the web layer works before
adding the agent, retrieval, and LLM calls on top of it.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

# Single source of truth for the version, reused in the app metadata and the
# health response so the two can never drift apart.
VERSION = "0.1.0"

# The application object. uvicorn is pointed at this variable by name
# ("app.main:app"), the way you'd point a servlet container at a WAR.
# The metadata below is not decoration: FastAPI feeds it into the generated
# OpenAPI schema that powers the interactive docs at /docs.
app = FastAPI(
    title="TriageAssist API",
    description=(
        "Clinical-intake triage assistant. Educational portfolio project — "
        "does not provide medical diagnosis."
    ),
    version=VERSION,
)


class HealthResponse(BaseModel):
    """The shape of a successful /health response.

    A Pydantic model is a Java DTO, Bean Validation constraints, and Jackson
    serialization collapsed into one declaration. Each attribute's type
    annotation is enforced at runtime, not merely documented.
    """

    status: str = Field(description="'ok' when the service is running.")
    service: str = Field(description="Which service answered — useful once deployed.")
    version: str = Field(description="Running API version.")


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Liveness check",
    tags=["system"],
)
def health() -> HealthResponse:
    """Report that the service is up.

    Deliberately does no real work — no database, no LLM call. A health check
    that depends on a slow external service will time out and get your
    container killed, so it stays trivial on purpose.
    """
    return HealthResponse(status="ok", service="triageassist-api", version=VERSION)
