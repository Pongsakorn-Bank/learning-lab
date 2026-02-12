from fastapi import FastAPI
from dotenv import load_dotenv
import os
import logging
from routers.facebook import router as facebook_router
from routers.google_sheet import router as google_sheet_router


logging.basicConfig(level=logging.INFO)
load_dotenv()

app = FastAPI(
    title="Simple Facebook Lead Gen API",
    description="""
    This API handles Facebook Lead Gen API webhooks and provides actions for interacting with Facebook users.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(facebook_router, prefix="/facebook", tags=["Facebook"])
app.include_router(google_sheet_router, prefix="/google_sheet", tags=["Google Sheet"])

@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "Simple Facebook Lead Gen API is running"}

if __name__ == "__main__":
    import uvicorn
    import os
    logging.info("Starting server...")
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8080)), log_level="info", reload=True)