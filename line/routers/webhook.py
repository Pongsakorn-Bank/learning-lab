from fastapi import APIRouter, Request, HTTPException, Header
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    BeaconEvent,
    TextMessageContent,
    ImageMessageContent
)
from services.line_handler import line_service
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Get credentials from environment variables
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# Initialize Line Bot SDK V3
configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)

@router.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    """
    Webhook callback endpoint for LINE.
    
    - **LINE sends its messages here.**
    - **Signature verification**: Ensures the message really came from LINE.
    """
    if x_line_signature is None:
        raise HTTPException(status_code=400, detail="Missing Signature")

    body = await request.body()
    
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
        print(body.decode("utf-8"))
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid Signature")

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    """
    This function handles Text Messages sent by users.
    It delegates the logic to LineService.
    """
    line_service.handle_text_message(event)

@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    """
    This function handles Image Messages sent by users.
    It delegates the logic to LineService.
    """
    line_service.handle_image_message(event)

@handler.add(BeaconEvent)
def handle_beacon(event):
    """
    This function handles Beacon Events sent by users.
    It delegates the logic to LineService.
    """
    line_service.handle_beacon(event)
