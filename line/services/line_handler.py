from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    UserProfileResponse,
    ShowLoadingAnimationRequest
)
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LineService:
    def __init__(self):
        self.channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        self.configuration = Configuration(access_token=self.channel_access_token)
        
        # Configure Gemini
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            print("Warning: GEMINI_API_KEY not found in environment variables.")
            self.model = None

    def get_user_profile(self, user_id):
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            return line_bot_api.get_profile(user_id)

    def handle_text_message(self, event):
        """
        Logic for handling text messages.
        You can expand this to include AI, database lookups, etc.
        """
        user_message = event.message.text
        user_profile = self.get_user_profile(event.source.user_id)

        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            # 1. Show loading animation
            try:
                line_bot_api.show_loading_animation(
                    ShowLoadingAnimationRequest(chatId=event.source.user_id, loadingSeconds=20)
                )
            except Exception as e:
                print(f"Error showing loading animation: {e}")

            # 2. Get response from Gemini
            if self.model:
                try:
                    response = self.model.generate_content(user_message)
                    reply_text = response.text
                except Exception as e:
                    reply_text = f"Gemini Error: {str(e)}"
            else:
                # Fallback if Gemini is not configured
                if user_message.lower() == "hello":
                    reply_text = f"Hello {user_profile.display_name}"
                else:
                    reply_text = f"Service processed: {user_message} {user_profile.display_name}"

            # 3. Reply to user
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )
        
    def handle_beacon(self, event):
        """
        Logic for handling beacon messages.
        You can expand this to include AI, database lookups, etc.
        """
        reply_text = f"Service processed: {event.beacon.type}"
        
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )

# Create a singleton instance
line_service = LineService()
