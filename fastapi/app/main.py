from fastapi import FastAPI
import uvicorn
import os
import sys

# Add the current directory to sys.path to allow running from within the 'app' folder or the 'fastapi' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routers import bookings

app = FastAPI(
    title="Hotel Booking API Tutorial",
    description="A simple FastAPI using Pydantic models to structure request and response",
    version="1.0.0"
)

# Include routers
app.include_router(bookings.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Hotel Booking API Tutorial. Go to /docs for API documentation."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
