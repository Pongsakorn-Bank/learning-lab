from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage
)
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
configuration = Configuration(access_token=channel_access_token)

class PushMessage(BaseModel):
    user_id: str
    text: str

@router.post("/push")
async def push_message(payload: PushMessage):
    """
    Send a Push Message to a specific User ID.
    
    - **user_id**: The unique ID of the LINE user.
    - **text**: The message content you want to send.
    """
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        try:
            line_bot_api.push_message(
                PushMessageRequest(
                    to=payload.user_id,
                    messages=[TextMessage(text=payload.text)]
                )
            )
            return {"status": "success", "message": "Push message sent"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/profile/{user_id}")
async def get_profile(user_id: str):
    """
    Retrieve user profile information.
    
    - **user_id**: The unique ID of the LINE user.
    """
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        try:
            profile = line_bot_api.get_profile(user_id)
            return {
                "display_name": profile.display_name,
                "user_id": profile.user_id,
                "picture_url": profile.picture_url,
                "status_message": profile.status_message
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
