import httpx
from typing import Dict, List, Any
from app.models.events import Event

class EventsService:
    """Service for interacting with the Ticketmaster API."""
    
    def __init__(self):
        # Public demo key
        self.base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
        self.api_key = "pLOeuGq2JL05uEGrZG7DuGWu6sh2OnMz"  
    
    async def search_events(self, search_params: Dict[str, str]) -> List[Event]:
        """Search for events using provided parameters."""
        api_params = {
            "apikey": self.api_key,
            "size": "20",
        }
        
        # Complete mapping of our parameters to Ticketmaster parameters
        mappings = {
            "keyword": "keyword",
            "location": "city",
            "category": "classificationName",
            "start_date": "startDateTime", 
            "end_date": "endDateTime"       
        }
        
        # Appling all mappings
        for our_param, ticket_master_param in mappings.items():
            if our_param in search_params:
                api_params[ticket_master_param] = search_params[our_param]
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=api_params, timeout=10.0)
                if response.status_code != 200:
                    response.raise_for_status()
                data =  response.json()
                            
            if "_embedded" not in data or "events" not in data["_embedded"]:
                return []
            
            # Transforming the API response to our model
            return [self._parse_event(event) for event in data["_embedded"]["events"]]
                
        except Exception as e:
            print(f"Error fetching events: {str(e)}")
            return []
            
    def _parse_event(self, event_data: Dict[str, Any]) -> Event:
        """Parse event data from Ticketmaster response."""
        # Extracting the venue data
        venue_data = event_data.get("_embedded", {}).get("venues", [{}])[0]
        
        # Getting the first image URL if available
        image_url = ""
        if event_data.get("images"):
            image_url = event_data["images"][0].get("url", "")
            
        # Getting the event time and checking for TBA flag
        time = "TBD"
        start_data = event_data.get("dates", {}).get("start", {})
        if start_data.get("localTime") and not start_data.get("timeTBA", False):
            time = start_data["localTime"]
            
        # Getting the category
        category = "Other"
        if event_data.get("classifications"):
            segment = event_data["classifications"][0].get("segment", {})
            category = segment.get("name", "Other")
                
        return Event(
            id=event_data.get("id", ""),
            name=event_data.get("name", "Unknown Event"),
            date=event_data.get("dates", {}).get("start", {}).get("localDate", "TBD"),
            time=time,
            venue=venue_data.get("name", "TBD"),
            city=venue_data.get("city", {}).get("name", "TBD"),
            state=venue_data.get("state", {}).get("stateCode", ""),
            image_url=image_url,
            url=event_data.get("url", "#"),
            category=category
        )