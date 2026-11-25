"""Pydantic schemas for the demo request-validation endpoint.

This endpoint exists only to demonstrate Pydantic validation - the data is
validated and echoed back, never persisted.
"""

from pydantic import BaseModel, EmailStr, Field


class DemoValidationRequest(BaseModel):
    """Example request body demonstrating validation rules."""

    name: str = Field(..., min_length=2, max_length=50, description="Full name (2-50 chars)")
    email: EmailStr = Field(..., description="Valid email address")
    age: int = Field(..., ge=18, le=120, description="Age between 18 and 120")


class DemoValidationResponse(BaseModel):
    """Echo of the validated payload plus a confirmation message."""

    message: str
    received: DemoValidationRequest
