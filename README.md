# TicketMaster Event Search API

A basic FastAPI backend to search for events using the Ticketmaster API.

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run server: `uvicorn app.main:app --reload`
6. API available at: [http://localhost:8000](http://localhost:8000)
7. API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoint

`GET /api/events` - Search for events with these query parameters:
- `keyword`: Search term
- `location`: City name
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `category`: Event category (e.g., "Sports", "Music", "Arts")

- Full TicketMaster Documentation is here: https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#search-events-v2

## Assumptions & Shortcuts

- Using a public Ticketmaster API key to avoid authentication requirements
- Direct mapping to Ticketmaster parameters for efficient filtering
- Limited to 5 search parameters per project requirements
- Minimal error handling focused on common API failures

## Testing
- Run tests with: `pytest --cov=app`
- This will also show test coverage statistics.
