from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import date

class BookingBase(BaseModel):
    hotel: str
    is_canceled: int
    lead_time: int
    arrival_date_year: int
    arrival_date_month: str
    arrival_date_week_number: int
    arrival_date_day_of_month: int
    stays_in_weekend_nights: int
    stays_in_week_nights: int
    adults: int
    children: Optional[float] = 0.0
    babies: int
    meal: str
    country: Optional[str] = None
    market_segment: str
    distribution_channel: str
    is_repeated_guest: int
    previous_cancellations: int
    previous_bookings_not_canceled: int
    reserved_room_type: str
    assigned_room_type: str
    booking_changes: int
    deposit_type: str
    agent: Optional[str] = "NULL"
    company: Optional[str] = "NULL"
    days_in_waiting_list: int
    customer_type: str
    adr: float
    required_car_parking_spaces: int
    total_of_special_requests: int
    reservation_status: str
    reservation_status_date: str

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    hotel: Optional[str] = None
    is_canceled: Optional[int] = None
    lead_time: Optional[int] = None
    arrival_date_year: Optional[int] = None
    arrival_date_month: Optional[str] = None
    arrival_date_week_number: Optional[int] = None
    arrival_date_day_of_month: Optional[int] = None
    stays_in_weekend_nights: Optional[int] = None
    stays_in_week_nights: Optional[int] = None
    adults: Optional[int] = None
    children: Optional[float] = None
    babies: Optional[int] = None
    meal: Optional[str] = None
    country: Optional[str] = None
    market_segment: Optional[str] = None
    distribution_channel: Optional[str] = None
    is_repeated_guest: Optional[int] = None
    previous_cancellations: Optional[int] = None
    previous_bookings_not_canceled: Optional[int] = None
    reserved_room_type: Optional[str] = None
    assigned_room_type: Optional[str] = None
    booking_changes: Optional[int] = None
    deposit_type: Optional[str] = None
    agent: Optional[str] = None
    company: Optional[str] = None
    days_in_waiting_list: Optional[int] = None
    customer_type: Optional[str] = None
    adr: Optional[float] = None
    required_car_parking_spaces: Optional[int] = None
    total_of_special_requests: Optional[int] = None
    reservation_status: Optional[str] = None
    reservation_status_date: Optional[str] = None

class Booking(BookingBase):
    id: int

    class Config:
        from_attributes = True

class PaginatedBookingResponse(BaseModel):
    data: List[dict]
    total: int
    page: int
    size: int
    next_page_token: Optional[str] = None
