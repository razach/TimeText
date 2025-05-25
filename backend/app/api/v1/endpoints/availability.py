from fastapi import APIRouter, HTTPException
from app.schemas.availability import AvailabilityRequest, AvailabilityResponse
from app.services.availability_service import AvailabilityService
import pytz
from datetime import datetime

router = APIRouter()

@router.post("/generate", response_model=AvailabilityResponse)
async def generate_availability_text(request: AvailabilityRequest):
    """
    Generate formatted text output for selected availability slots.
    
    - **selected_slots**: List of time slots with start and end times
    - **user_timezone**: User's timezone in IANA format (e.g., 'America/New_York')
    - **recipient_timezone**: Optional recipient's timezone in IANA format
    - **output_format**: Either 'continuous' or 'chunks'
    - **slot_granularity_minutes**: Minutes per slot (used if output_format is 'chunks')
    """
    try:
        # Validate timezones
        try:
            pytz.timezone(request.user_timezone)
            if request.recipient_timezone:
                pytz.timezone(request.recipient_timezone)
        except pytz.exceptions.UnknownTimeZoneError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid timezone: {str(e)}"
            )

        # Validate output format
        if request.output_format not in ["continuous", "chunks"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid output_format. Must be either 'continuous' or 'chunks'"
            )

        # Validate time slots
        for slot in request.selected_slots:
            if slot.start >= slot.end:
                raise HTTPException(
                    status_code=400,
                    detail="Start time must be before end time for each slot"
                )

        # Generate output based on format
        if request.output_format == "continuous":
            text_output = AvailabilityService.generate_continuous_output(
                request.selected_slots,
                request.user_timezone,
                request.recipient_timezone
            )
        else:  # chunks
            text_output = AvailabilityService.generate_chunks_output(
                request.selected_slots,
                request.user_timezone,
                request.recipient_timezone,
                request.slot_granularity_minutes
            )

        return AvailabilityResponse(
            text_output=text_output,
            user_timezone=request.user_timezone,
            recipient_timezone=request.recipient_timezone
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        ) 