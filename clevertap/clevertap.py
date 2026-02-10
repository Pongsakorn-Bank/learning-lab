import requests
import os
import json
from pydantic import BaseModel, ValidationError, TypeAdapter
from datetime import datetime, timezone, timedelta
from typing import Optional, List

class CleverTapProfile(BaseModel):
    type: str = "profile"
    identity: Optional[str] = None
    objectId: Optional[str] = None
    FBID: Optional[str] = None
    profileData: dict

class CleverTapEvent(BaseModel):
    type: str = "event"
    evtName: str
    ts: int
    identity: Optional[str] = None
    objectId: Optional[str] = None
    FBID: Optional[str] = None
    GPID: Optional[str] = None
    evtData: dict

class CleverTap:
    def __init__(self, clevertap_account_id:str=None, clevertap_passcode:str=None):
        self.account_id = os.environ.get("CLEVERTAP_ACCOUNT_ID") if clevertap_account_id == None else clevertap_account_id
        self.passcode = os.environ.get("CLEVERTAP_PASSCODE") if clevertap_passcode == None else clevertap_passcode
        self.base_url = "https://sg1.api.clevertap.com/1"
        self.headers = {
            "X-CleverTap-Account-Id": self.account_id,
            "X-CleverTap-Passcode": self.passcode
        }

    def upload_user_profile(self, profiles):
        try:
            profile = CleverTapProfile(**profiles)
        except ValidationError as e:
            return e.json()
        headers = self.headers
        headers['Content-Type'] = "application/json; charset=utf-8"
        url = f"{self.base_url}/upload"
        data = {
            "d": [profiles]
        }
        respones = requests.post(url, headers=headers, data=json.dumps(data))
        res_data = json.loads(respones.content)
        return res_data
    
    def upload_user_profiles(self, profiles):
        try:
            profile = TypeAdapter(List[CleverTapProfile]).validate_python(profiles)
        except ValidationError as e:
            return e.json()
        headers = self.headers
        headers['Content-Type'] = "application/json; charset=utf-8"
        url = f"{self.base_url}/upload"
        data = {
            "d": profiles
        }
        respones = requests.post(url, headers=headers, data=json.dumps(data))
        res_data = json.loads(respones.content)
        return res_data
    
    def upload_event(self, event):
        try:
            event = CleverTapEvent(**event)
        except ValidationError as e:
            return e.json()
        headers = self.headers
        headers['Content-Type'] = "application/json; charset=utf-8"
        url = f"{self.base_url}/upload"
        data = {
            "d": [event]
        }
        respones = requests.post(url, headers=headers, data=json.dumps(data))
        res_data = json.loads(respones.content)
        return res_data
    
    def upload_events(self, event_pack):
        try:
            events = TypeAdapter(List[CleverTapEvent]).validate_python(event_pack)
        except ValidationError as e:
            return {"status": "error", "message": "Invalid event payload", "details": e.errors()}

        headers = self.headers
        headers['Content-Type'] = "application/json; charset=utf-8"
        url = f"{self.base_url}/upload"
        data = {
            "d": event_pack
        }
        respones = requests.post(url, headers=headers, data=json.dumps(data))
        res_data = json.loads(respones.content)
        return res_data
    
    def _to_unix(self, dt_str, tz_offset_hours=0):
        tz = timezone(timedelta(hours=tz_offset_hours))
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo=tz)
        return int(dt.timestamp())