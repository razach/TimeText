from datetime import datetime, timedelta
import pytz
import pytest
from app.schemas.availability import TimeSlot
from app.services.availability_service import AvailabilityService

@pytest.fixture
def sample_time_slots():
    # Create sample time slots in America/New_York timezone
    ny_tz = pytz.timezone('America/New_York')
    base_time = ny_tz.localize(datetime(2024, 3, 20, 9, 0))  # March 20, 2024, 9:00 AM
    
    return [
        TimeSlot(
            start=base_time,
            end=base_time + timedelta(hours=2)
        ),
        TimeSlot(
            start=base_time + timedelta(days=1),
            end=base_time + timedelta(days=1, hours=1)
        )
    ]

def test_convert_timezone():
    # Test timezone conversion
    ny_tz = pytz.timezone('America/New_York')
    la_tz = pytz.timezone('America/Los_Angeles')
    
    # Create a time in New York
    ny_time = ny_tz.localize(datetime(2024, 3, 20, 9, 0))
    
    # Convert to Los Angeles
    la_time = AvailabilityService.convert_timezone(ny_time, 'America/New_York', 'America/Los_Angeles')
    
    # LA should be 3 hours behind NY
    assert la_time.hour == 6
    assert la_time.minute == 0

def test_format_time():
    # Test time formatting
    ny_tz = pytz.timezone('America/New_York')
    time = ny_tz.localize(datetime(2024, 3, 20, 9, 0))
    
    formatted = AvailabilityService.format_time(time)
    assert formatted == "9:00 AM"

def test_format_date():
    # Test date formatting
    ny_tz = pytz.timezone('America/New_York')
    time = ny_tz.localize(datetime(2024, 3, 20, 9, 0))
    
    formatted = AvailabilityService.format_date(time)
    assert formatted == "Wed, Mar 20"

def test_generate_continuous_output(sample_time_slots):
    # Test continuous output generation
    output = AvailabilityService.generate_continuous_output(
        sample_time_slots,
        'America/New_York',
        'America/Los_Angeles'
    )
    
    # Check that the output contains expected elements
    assert "Here's my availability:" in output
    assert "America/New_York" in output
    assert "America/Los_Angeles" in output
    assert "Wed, Mar 20" in output
    assert "Thu, Mar 21" in output

def test_generate_chunks_output(sample_time_slots):
    # Test chunks output generation
    output = AvailabilityService.generate_chunks_output(
        sample_time_slots,
        'America/New_York',
        'America/Los_Angeles',
        granularity_minutes=30
    )
    
    # Check that the output contains expected elements
    assert "Here's my availability:" in output
    assert "America/New_York" in output
    assert "America/Los_Angeles" in output
    assert "Wed, Mar 20" in output
    assert "Thu, Mar 21" in output
    
    # Should have multiple 30-minute chunks
    assert output.count("9:00 AM") > 0
    assert output.count("9:30 AM") > 0 