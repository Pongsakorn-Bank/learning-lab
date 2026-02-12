# FastAPI Tutorial: Hotel Bookings API

This tutorial demonstrates how to build a RESTful API using **FastAPI** and **Pydantic** for structured data handling. We use a CSV dataset of hotel bookings as our data source.

## Features
- **Structured Models**: Using Pydantic for request and response validation.
- **Router Pattern**: Organizing code using FastAPI `APIRouter`.
- **Advanced GET**: Supporting field selection, filtering, and pagination with `next_page_token`.
- **CRUD Operations**: Support for adding and updating booking records.

## Project Structure
```text
fastapi/
├── app/
│   ├── main.py          # Entry point and app configuration
│   ├── database.py      # CSV data handling (Mock DB)
│   ├── routers/         # API routes
│   │   └── bookings.py  # Hotel booking endpoints
│   └── schemas/         # Pydantic models
│       └── booking.py   # Data structures
├── data/
│   └── hotel_bookings.csv
└── requirements.txt
```

## Setup & Running

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Server**:
   ```bash
   cd fastapi
   python3 app/main.py
   ```
   The API will be available at `http://localhost:8080`.

## API Documentation
Once the server is running, visit:
- **Swagger UI**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc**: [http://localhost:8080/redoc](http://localhost:8080/redoc)

## Example Requests

### 1. Get Bookings with Filtering and Pagination
**GET** `/bookings/?page=1&size=5&hotel=Resort Hotel&fields=hotel,arrival_date_year,adr`

### 2. Add a New Booking
**POST** `/bookings/`
```json
{
  "hotel": "Resort Hotel",
  "is_canceled": 0,
  "lead_time": 10,
  "arrival_date_year": 2024,
  "arrival_date_month": "February",
  "arrival_date_week_number": 6,
  "arrival_date_day_of_month": 12,
  "stays_in_weekend_nights": 1,
  "stays_in_week_nights": 2,
  "adults": 2,
  "children": 0,
  "babies": 0,
  "meal": "BB",
  "country": "THA",
  "market_segment": "Direct",
  "distribution_channel": "Direct",
  "is_repeated_guest": 0,
  "previous_cancellations": 0,
  "previous_bookings_not_canceled": 0,
  "reserved_room_type": "A",
  "assigned_room_type": "A",
  "booking_changes": 0,
  "deposit_type": "No Deposit",
  "agent": "NULL",
  "company": "NULL",
  "days_in_waiting_list": 0,
  "customer_type": "Transient",
  "adr": 150.0,
  "required_car_parking_spaces": 1,
  "total_of_special_requests": 0,
  "reservation_status": "Check-Out",
  "reservation_status_date": "2024-02-15"
}
```

### 3. Update an Existing Booking
**PUT** `/bookings/{booking_id}`
```json
{
  "adr": 175.0,
  "booking_changes": 1
}
```
