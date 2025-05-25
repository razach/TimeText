from fastapi import APIRouter, HTTPException, Depends, Request, Header
from app.schemas.availability import AvailabilityRequest, AvailabilityResponse
from app.services.availability_service import AvailabilityService
from app.core.config import settings
import pytz
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def get_api_key(api_key: str = Header(..., alias="X-API-Key")):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

async def get_request_body(request: Request) -> AvailabilityRequest:
    try:
        body = await request.json()
        return AvailabilityRequest(**body)
    except Exception as e:
        logger.error(f"Error parsing request body: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid request body: {str(e)}")

@router.post("/", response_model=AvailabilityResponse)
async def generate_availability_text(
    request: Request,
    body: AvailabilityRequest = Depends(get_request_body),
    api_key: str = Depends(get_api_key)
):
    """
    Generate formatted text output for selected availability slots.
    
    - **selected_slots**: List of time slots with start and end times
    - **user_timezone**: User's timezone in IANA format (e.g., 'America/New_York')
    - **recipient_timezone**: Optional recipient's timezone in IANA format
    - **output_format**: Either 'continuous' or 'chunks'
    - **slot_granularity_minutes**: Minutes per slot (used if output_format is 'chunks')
    """
    try:
        logger.info(f"Received request: {await request.json()}")
        
        # Validate timezones
        try:
            pytz.timezone(body.user_timezone)
            if body.recipient_timezone:
                pytz.timezone(body.recipient_timezone)
        except pytz.exceptions.UnknownTimeZoneError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid timezone: {str(e)}"
            )

        # Validate output format
        if body.output_format not in ["continuous", "chunks"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid output_format. Must be either 'continuous' or 'chunks'"
            )

        # Validate time slots
        for slot in body.selected_slots:
            if slot.start >= slot.end:
                raise HTTPException(
                    status_code=400,
                    detail="Start time must be before end time for each slot"
                )

        # Generate output based on format
        if body.output_format == "continuous":
            text_output = AvailabilityService.generate_continuous_output(
                body.selected_slots,
                body.user_timezone,
                body.recipient_timezone
            )
        else:  # chunks
            text_output = AvailabilityService.generate_chunks_output(
                body.selected_slots,
                body.user_timezone,
                body.recipient_timezone,
                body.slot_granularity_minutes
            )

        return AvailabilityResponse(
            text_output=text_output,
            user_timezone=body.user_timezone,
            recipient_timezone=body.recipient_timezone
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        ) 