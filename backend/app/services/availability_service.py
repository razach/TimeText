from datetime import datetime, timedelta
from typing import List, Optional
import pytz
from app.schemas.availability import TimeSlot

class AvailabilityService:
    @staticmethod
    def convert_timezone(
        dt: datetime,
        from_tz: str,
        to_tz: str
    ) -> datetime:
        """Convert datetime from one timezone to another."""
        from_zone = pytz.timezone(from_tz)
        to_zone = pytz.timezone(to_tz)
        
        # If datetime is naive, localize it
        if dt.tzinfo is None:
            dt = from_zone.localize(dt)
        # If datetime is already localized, convert it
        else:
            dt = dt.astimezone(from_zone)
        
        # Convert to target timezone
        return dt.astimezone(to_zone)

    @staticmethod
    def format_time(dt: datetime) -> str:
        """Format datetime to a readable time string."""
        return dt.strftime("%I:%M %p").lstrip("0")

    @staticmethod
    def format_date(dt: datetime) -> str:
        """Format datetime to a readable date string."""
        return dt.strftime("%a, %b %d")

    @staticmethod
    def _get_tz_name(dt: datetime) -> str:
        # Helper to get the timezone name from a datetime or fallback to 'UTC'
        if dt.tzinfo is not None:
            # For pytz, tzinfo.zone gives the string name
            return getattr(dt.tzinfo, 'zone', 'UTC')
        return 'UTC'

    @staticmethod
    def generate_continuous_output(
        slots: List[TimeSlot],
        user_tz: str,
        recipient_tz: Optional[str] = None
    ) -> str:
        """Generate continuous format output."""
        output = ["Here's my availability:\n"]
        
        # Add header
        header = "Date        | My Timezone"
        if recipient_tz:
            header += f" ({user_tz}) | Recipient's Timezone ({recipient_tz})"
        else:
            header += f" ({user_tz})"
        output.append(header)
        output.append("-" * len(header))

        # Group slots by date
        slots_by_date = {}
        for slot in slots:
            # Ensure the datetime is in the user's timezone
            start_time = AvailabilityService.convert_timezone(
                slot.start, AvailabilityService._get_tz_name(slot.start), user_tz
            )
            end_time = AvailabilityService.convert_timezone(
                slot.end, AvailabilityService._get_tz_name(slot.end), user_tz
            )
            
            date_key = start_time.date()
            if date_key not in slots_by_date:
                slots_by_date[date_key] = []
            slots_by_date[date_key].append((start_time, end_time))

        # Generate output for each date
        for date in sorted(slots_by_date.keys()):
            for start_time, end_time in slots_by_date[date]:
                date_str = AvailabilityService.format_date(start_time)
                time_str = f"{AvailabilityService.format_time(start_time)} - {AvailabilityService.format_time(end_time)}"
                
                if recipient_tz:
                    recipient_start = AvailabilityService.convert_timezone(start_time, user_tz, recipient_tz)
                    recipient_end = AvailabilityService.convert_timezone(end_time, user_tz, recipient_tz)
                    recipient_time = f"{AvailabilityService.format_time(recipient_start)} - {AvailabilityService.format_time(recipient_end)}"
                    output.append(f"{date_str} | {time_str} | {recipient_time}")
                else:
                    output.append(f"{date_str} | {time_str}")

        return "\n".join(output)

    @staticmethod
    def generate_chunks_output(
        slots: List[TimeSlot],
        user_tz: str,
        recipient_tz: Optional[str] = None,
        granularity_minutes: int = 30
    ) -> str:
        """Generate chunks format output."""
        output = ["Here's my availability:\n"]
        
        # Add header
        header = "Date        | My Timezone"
        if recipient_tz:
            header += f" ({user_tz}) | Recipient's Timezone ({recipient_tz})"
        else:
            header += f" ({user_tz})"
        output.append(header)
        output.append("-" * len(header))

        # Generate chunks for each slot
        for slot in slots:
            # Ensure the datetime is in the user's timezone
            current = AvailabilityService.convert_timezone(
                slot.start, AvailabilityService._get_tz_name(slot.start), user_tz
            )
            end_time = AvailabilityService.convert_timezone(
                slot.end, AvailabilityService._get_tz_name(slot.end), user_tz
            )
            
            while current < end_time:
                date_str = AvailabilityService.format_date(current)
                time_str = AvailabilityService.format_time(current)
                
                if recipient_tz:
                    recipient_time = AvailabilityService.convert_timezone(current, user_tz, recipient_tz)
                    recipient_time_str = AvailabilityService.format_time(recipient_time)
                    output.append(f"{date_str} | {time_str} | {recipient_time_str}")
                else:
                    output.append(f"{date_str} | {time_str}")
                
                current += timedelta(minutes=granularity_minutes)

        return "\n".join(output) 