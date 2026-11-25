"""Health and readiness endpoints.

- /health       -> liveness: the process is up and serving requests.
- /health/ready -> readiness: the app can accept real work. Database
                   connectivity is intentionally NOT reported yet because
                   PostgreSQL is integrated in a later module.
"""

from fastapi import APIRouter, status

from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness check",
    description="Returns service health. Used by the frontend to verify backend reachability.",
)
async def health_check() -> HealthResponse:
    """Return service health status."""
    return HealthResponse(status="healthy", application="SalesPilot AI")


@router.get(
    "/health/ready",
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness check",
    description="Returns application readiness and the list of dependencies currently checked.",
)
async def readiness_check() -> ReadinessResponse:
    """Return readiness. Only lists dependencies implemented so far."""
    return ReadinessResponse(
        status="ready",
        application="SalesPilot AI",
        checks=[
            # PostgreSQL is integrated in a later module; reported as not_configured.
            {"name": "database", "status": "not_configured"},
        ],
    )
