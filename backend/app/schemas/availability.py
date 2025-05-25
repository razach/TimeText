from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class TimeSlot(BaseModel):
    start: str = Field(..., description="Start time of the availability slot in ISO format")
    end: str = Field(..., description="End time of the availability slot in ISO format")

    @field_validator('start', 'end')
    @classmethod
    def validate_datetime(cls, v: str) -> datetime:
        try:
            return datetime.fromisoformat(v)
        except ValueError:
            raise ValueError("Invalid datetime format. Must be in ISO format.")

class AvailabilityRequest(BaseModel):
    selected_slots: List[TimeSlot] = Field(..., description="List of selected time slots")
    user_timezone: str = Field(..., description="User's timezone (IANA format)")
    recipient_timezone: Optional[str] = Field(None, description="Recipient's timezone (IANA format)")
    output_format: str = Field(
        default="continuous",
        description="Format of output: 'continuous' or 'chunks'"
    )
    slot_granularity_minutes: int = Field(
        default=30,
        description="Granularity of time slots in minutes (used if output_format is 'chunks')"
    )

class AvailabilityResponse(BaseModel):
    text_output: str = Field(..., description="Formatted text output of availability")
    user_timezone: str = Field(..., description="User's timezone")
    recipient_timezone: Optional[str] = Field(None, description="Recipient's timezone") 