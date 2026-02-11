from fastapi import Query
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, ConfigDict
import os
from dotenv import load_dotenv
from typing import Optional, List
from enum import Enum
import logging
import time
import re
import hashlib
import json
from datetime import datetime, timedelta, timezone
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.leadgenform import LeadgenForm
from facebook_business.adobjects.lead import Lead
from facebook_business.adobjects.adspixel import AdsPixel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class FormDataItem(BaseModel):
    """Represents a single answer in a form (e.g., Name: John)"""
    key: Optional[str] = Field(None, description="The field name, like 'phone_number'")
    value: Optional[str] = Field(None, description="The actual answer from the user")

class FormSubmission(BaseModel):
    """Represents the entire lead submission"""
    form_submission_id: str = Field(..., description="Unique ID for this lead (starts with l:)")
    form_type: str = Field("fb_lead_gen", description="Source type (always 'fb_lead_gen' here)")
    timestamp: Optional[str] = Field(None, description="Date and time the lead was created")
    ad_id: Optional[str] = Field(None, description="The ID of the Facebook Ad that generated this lead")
    data: List[FormDataItem] = Field(default_factory=list, description="The list of answers from the form")

class RequestLeadGen(BaseModel):
    """Represents the response from the /get_lead_gen endpoint"""
    form_id: str = Field(..., description="The ID of the form")
    start_time: Optional[str] = Field(None, description="The start time of the lead gen, example: 2025-01-01 00:00:00")
    end_time: Optional[str] = Field(None, description="The end time of the lead gen, example: 2025-01-01 23:59:59")

class ActionSource(str, Enum):
    EMAIL = "email"
    WEBSITE = "website"
    APP = "app"
    PHONE_CALL = "phone_call"
    CHAT = "chat"
    PHYSICAL_STORE = "physical_store"
    SYSTEM_GENERATED = "system_generated"
    OTHER = "other"

class UserData(BaseModel):
    # Meta requires these to be hashed (SHA256)
    em: Optional[List[str]] = None  # Email
    ph: Optional[List[str]] = None  # Phone
    fn: Optional[List[str]] = None  # First Name
    ln: Optional[List[str]] = None  # Last Name
    lead_id: Optional[List[str]] = None  # Lead ID
    
    # These should NOT be hashed
    client_ip_address: Optional[str] = None
    client_user_agent: Optional[str] = None
    fbc: Optional[str] = None  # Facebook Click ID
    fbp: Optional[str] = None  # Facebook Browser ID

    @field_validator("em", "ph", "fn", "ln", mode="before")
    @classmethod
    def hash_sensitive_data(cls, v):
        if v is None:
            return v
        
        hashed_list = []
        for item in v:
            item = item.strip().lower()
            # Only hash if it's not already a 64-char hex string (already hashed)
            if len(item) == 64 and all(c in "0123456789abcdef" for c in item):
                hashed_list.append(item)
            else:
                hashed_list.append(hashlib.sha256(item.encode()).hexdigest())
        return hashed_list

class CustomData(BaseModel):
    value: Optional[float] = None
    currency: Optional[str] = None
    content_name: Optional[str] = None
    content_ids: Optional[List[str]] = None
    content_type: Optional[str] = None
    order_id: Optional[str] = None

class ServerEvent(BaseModel):
    event_name: str
    event_time: int = Field(default_factory=lambda: int(time.time()))
    action_source: ActionSource = ActionSource.WEBSITE
    event_id: Optional[str] = None
    event_source_url: Optional[str] = None
    user_data: UserData
    custom_data: Optional[CustomData] = None

class FacebookCAPIPayload(BaseModel):
    data: List[ServerEvent]
    test_event_code: Optional[str] = None

router = APIRouter()

#def zone
def hash_data(value):
    if pd.isna(value) or value == "":
        return None
    return hashlib.sha256(str(value).strip().lower().encode('utf-8')).hexdigest()

def prepare_fb_payload(row):
    # Normalize and hash phone
    # Remove all symbols and non-numeric characters using regex
    clean_phone = re.sub(r'\D', '', str(row['phone']))
    hashed_phone = hash_data(clean_phone)
    
    payload = {
        "event_name": row['event_name'],
        "event_time": int(row['event_time']),
        "action_source": "system_generated", # or "physical_store" for offline
        "user_data": {
            "ph": [hashed_phone],
            "lead_id": row['lead_id'] # lead_id does NOT need hashing
        },
        "custom_data": {
            "currency": row['currency'],
            "value": float(row['value'])
        }
    }
    return payload

#set up env
access_token = os.environ.get("FB_TOKEN")

@router.get("/leadgen/{form_id}")
def leadgen(
    form_id: str,
    start_time: Optional[str] = Query(None, description="The start time of the lead gen, example: 2025-01-01 00:00:00"),
    end_time: Optional[str] = Query(None, description="The end time of the lead gen, example: 2025-01-01 23:59:59"),
    limit: Optional[int] = Query(100, description="The number of leads to return"),
):
    logger.info("Leadgen endpoint called")

    fields = ['created_time', 'field_data', 'ad_id', 'form_id']
    #transform start_time and end_time to timestamp
    start_time = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S")))
    end_time = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S")))
    params = {
        'limit': limit,
        'filtering': [
            {'field': 'time_created', 'operator': 'GREATER_THAN', 'value': start_time},
            {'field': 'time_created', 'operator': 'LESS_THAN', 'value': end_time}
        ]
    }
    if access_token:
        FacebookAdsApi.init(access_token=access_token)
        logger.info("Facebook API Initialized.")
    else:
        logger.error("Facebook API not initialized.")
        raise HTTPException(status_code=500, detail="Facebook API not initialized")
    try:
        leadgen_form = LeadgenForm(form_id)
        leads = leadgen_form.get_leads(fields=fields, params=params)
        all_cleaned_leads = []
        for lead in leads:
            dt_utc = datetime.strptime(lead['created_time'], "%Y-%m-%dT%H:%M:%S%z")
            bangkok_time = dt_utc.astimezone(timezone(timedelta(hours=7))).strftime("%Y-%m-%d %H:%M:%S")
            cleaned_lead = {
                'created_time': bangkok_time,
                'ad_id': lead.get('ad_id', None),
                'form_id': lead.get('form_id', None),
                'field_data': lead.get('field_data', None)
            }
            all_cleaned_leads.append(cleaned_lead)
            
        return JSONResponse(content=all_cleaned_leads)
    except Exception as e:
        logger.error(f"Error getting leads: {e}")
        raise HTTPException(status_code=500, detail="Error getting leads")


@router.get("/conversion_api/{pixel_id}/events")
def conversion_api(
    pixel_id: str,
    events: List[ServerEvent]
):
    FB_ACCESS_TOKEN = os.getenv('FB_TOKEN')
    if FB_ACCESS_TOKEN:
        FacebookAdsApi.init(access_token=FB_ACCESS_TOKEN)
        logger.info("Facebook API Initialized.")
    else:
        logger.error("Facebook API not initialized.")
        raise HTTPException(status_code=500, detail="Facebook API not initialized")
    try:
        pixel = AdsPixel(pixel_id)
        pixel.create_event(
            fields=[],
            params={
                'data': events,
                'test_event_code': 'TEST_CODE'
            }
        )
        logger.info("Events created successfully!")
        return JSONResponse(content={"message": "Events created successfully!"})
    except Exception as e:
        logger.error(f"Error creating events: {e}")
        raise HTTPException(status_code=500, detail="Error creating events")