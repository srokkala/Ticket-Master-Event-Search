from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from app.models.events import EventResponse
from app.services.events_service import EventsService

router = APIRouter()

@router.get("/events", response_model=EventResponse, tags=["events"])
async def search_events(
    keyword: Optional[str] = Query(None, description="Keyword to search for in event name"),
    location: Optional[str] = Query(None, description="Location (city) of the event"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    category: Optional[str] = Query(None, description="Event category (e.g., Sports, Music, Arts)"),
    events_service: EventsService = Depends(lambda: EventsService())
):
    """
    Search for events based on search criteria.
    This endpoint maps parameters directly to Ticketmaster API parameters.
    """
    if not any([keyword, location, start_date, end_date, category]):
        raise HTTPException(status_code=400, detail="At least one search parameter is required")
    
    search_params = {}
    if keyword:
        search_params["keyword"] = keyword
    if location:
        search_params["location"] = location
    if start_date:
        search_params["start_date"] = start_date
    if end_date:
        search_params["end_date"] = end_date
    if category:
        search_params["category"] = category
    
    try:
        events = await events_service.search_events(search_params)
        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search events: {str(e)}")