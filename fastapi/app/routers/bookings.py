from fastapi import APIRouter, Query, HTTPException, Body
from typing import List, Optional, Dict, Any
from schemas.booking import Booking, BookingCreate, BookingUpdate, PaginatedBookingResponse
from database import db

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)

@router.get("/", response_model=PaginatedBookingResponse)
async def get_bookings(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    hotel: Optional[str] = None,
    is_canceled: Optional[int] = None,
    fields: Optional[str] = Query(None, description="Comma separated list of fields to return")
):
    filters = {}
    if hotel:
        filters["hotel"] = hotel
    if is_canceled is not None:
        filters["is_canceled"] = is_canceled
        
    requested_fields = fields.split(",") if fields else None
    
    result = db.get_bookings(filters=filters, fields=requested_fields, page=page, size=size)
    return result

@router.post("/", response_model=Booking)
async def create_booking(booking: BookingCreate):
    new_booking = db.add_booking(booking.model_dump())
    return new_booking

@router.put("/{booking_id}", response_model=Booking)
async def update_booking(booking_id: int, booking: BookingUpdate):
    updated_booking = db.update_booking(booking_id, booking.model_dump(exclude_unset=True))
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking

@router.get("/{booking_id}", response_model=Booking)
async def get_booking(booking_id: int):
    # This is a bit inefficient with our simple DB but works for the tutorial
    result = db.get_bookings(filters={"id": booking_id}, size=1)
    if not result["data"]:
        raise HTTPException(status_code=404, detail="Booking not found")
    return result["data"][0]
