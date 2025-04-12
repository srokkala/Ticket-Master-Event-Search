from pydantic import BaseModel
from typing import List, Optional

class Event(BaseModel):
    """Model for a single event."""
    id: str
    name: str
    date: str
    time: Optional[str] = "TBD"
    venue: str
    city: str
    state: Optional[str] = ""
    image_url: Optional[str] = ""
    url: str
    category: Optional[str] = "Other"

class EventResponse(BaseModel):
    """Model for an event search endpoint."""
    events: List[Event]