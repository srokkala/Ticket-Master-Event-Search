import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.models.events import Event

client = TestClient(app)

@pytest.fixture
def mock_search():
    with patch("app.api.events.EventsService") as mock_class:
        search_mock = AsyncMock()
        mock_class.return_value.search_events = search_mock
        yield search_mock

def test_validation_requires_parameters():
    """Test API requires at least one parameter."""
    response = client.get("/api/events")
    assert response.status_code == 400
    assert "At least one search parameter is required" in response.json()["detail"]

def test_successful_search(mock_search):
    """Test successful event search with parameters."""
    mock_search.return_value = [
        Event(
            id="event1", name="Test Event", date="2025-04-15", time="19:00:00",
            venue="Test Venue", city="Test City", state="TS",
            image_url="https://example.com/image.jpg", url="#", category="Music"
        )
    ]
    
    response = client.get("/api/events?keyword=test&location=NY")
    
    assert response.status_code == 200
    events = response.json()["events"]
    assert len(events) == 1
    assert events[0]["name"] == "Test Event"

def test_parameter_passing(mock_search):
    """Test parameters are correctly passed to service."""
    mock_search.return_value = []
    
    response = client.get("/api/events?keyword=test&location=NY&category=Music")
    
    assert response.status_code == 200
    call_args = mock_search.call_args[0][0]
    assert call_args["keyword"] == "test"
    assert call_args["location"] == "NY"
    assert call_args["category"] == "Music"

def test_error_handling(mock_search):
    """Test error handling when service throws exception."""
    mock_search.side_effect = Exception("API error")
    
    response = client.get("/api/events?keyword=test")
    
    assert response.status_code == 500
    assert "Failed to search events" in response.json()["detail"]