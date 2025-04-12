import pytest
import httpx
from unittest.mock import patch
from app.services.events_service import EventsService

@pytest.fixture
def service():
    return EventsService()

def test_parse_event_complete(service):
    """Test parsing complete event data."""
    event_data = {
        "id": "event1",
        "name": "Test Event",
        "dates": {"start": {"localDate": "2025-04-15", "localTime": "19:00:00"}},
        "_embedded": {
            "venues": [{"name": "Test Venue", "city": {"name": "Test City"}, "state": {"stateCode": "TS"}}]
        },
        "images": [{"url": "https://example.com/image.jpg"}],
        "url": "https://example.com/event",
        "classifications": [{"segment": {"name": "Music"}}]
    }
    
    event = service._parse_event(event_data)
    
    assert event.id == "event1"
    assert event.name == "Test Event"
    assert event.date == "2025-04-15"
    assert event.venue == "Test Venue"
    assert event.category == "Music"

def test_parse_event_missing_data(service):
    """Test parsing with missing data."""
    event = service._parse_event({"id": "event1", "name": "Test Event"})
    
    assert event.id == "event1"
    assert event.name == "Test Event" 
    assert event.date == "TBD"
    assert event.category == "Other"


@pytest.mark.asyncio
async def test_http_error_handling(service):
    """Test handling of HTTP errors."""
    with patch("httpx.AsyncClient.get", side_effect=httpx.HTTPError("HTTP Error")):
        result = await service.search_events({"keyword": "test"})
        assert result == []

@pytest.mark.asyncio
async def test_empty_response_handling(service):
    """Test handling empty API responses."""
    class MockResponse:
        def __init__(self):
            self.status_code = 200

        def json(self):
            return {}

    async def mock_get(self, *args, **kwargs):
        return MockResponse()

    with patch("httpx.AsyncClient.get", side_effect=mock_get):
        result = await service.search_events({"keyword": "test"})
        assert result == []