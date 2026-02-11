from fastapi import Query
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from typing import Optional, List
import logging
import time
import json
from datetime import datetime, timedelta, timezone
import gspread
from google.oauth2.service_account import Credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

router = APIRouter()

def get_gspread_client() -> gspread.Client:
    # Define the scope
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # Get credentials from environment variable
    creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    
    if not creds_json:
        raise ValueError("GOOGLE_SHEETS_CREDENTIALS environment variable NOT found.")
    
    # If the env var is a path to a file, load it directly
    if os.path.isfile(creds_json):
        creds = Credentials.from_service_account_file(creds_json, scopes=scope)
    else:
        # Otherwise, assume it's the JSON content itself
        info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(info, scopes=scope)
        
    client = gspread.authorize(creds)
    return client

@router.post("/{google_sheet_id}/{work_sheet_id}")
def append_data(
    google_sheet_id: str,
    work_sheet_id: str,
    data: List[List[str]],
):
    try:
        try:
            gc = get_gspread_client()
            logger.info("Authenticated successfully!")
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
        try:
            spreadsheet = gc.open_by_key(google_sheet_id)
            worksheet = spreadsheet.get_worksheet_by_id(work_sheet_id)
            worksheet.append_rows(values=data)
            logger.info("Data appended successfully!")
            return JSONResponse(content={"message": "Data appended successfully!"})
        except Exception as e:
            logger.error(f"Error appending data to Google Sheet: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error appending data to Google Sheet: {e}")
        raise HTTPException(status_code=500, detail=str(e))