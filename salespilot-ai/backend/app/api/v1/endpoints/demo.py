"""Demo endpoint teaching request validation (no data persisted)."""

from fastapi import APIRouter, status

from app.schemas.demo import DemoValidationRequest, DemoValidationResponse

router = APIRouter(tags=["demo"])


@router.post(
    "/demo/validate",
    response_model=DemoValidationResponse,
    status_code=status.HTTP_200_OK,
    summary="Demo: validate a request payload",
    description=(
        "Validates name, email and age with Pydantic and echoes them back. "
        "For teaching purposes only - nothing is saved."
    ),
    responses={
        422: {"description": "Invalid input"},
    },
)
async def validate_demo(payload: DemoValidationRequest) -> DemoValidationResponse:
    """Validate the payload and return a structured confirmation."""
    return DemoValidationResponse(
        message=f"Validation passed for {payload.name}",
        received=payload,
    )
