from fastapi import FastAPI
from dotenv import load_dotenv
import os
from routers import webhook, messaging

# Load environment variables
load_dotenv()

app = FastAPI(
    title="LINE Webhook API",
    description="""
    This API handles LINE Messaging API webhooks and provides actions for interacting with LINE users.
    
    ### For Non-Technical Users:
    - **Webhook**: This is the endpoint where LINE sends events (like when someone sends a message to your bot).
    - **Messaging**: Use these endpoints to send messages to users, reply to messages, etc.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include Routers
app.include_router(webhook.router, prefix="/webhook", tags=["Webhook"])
app.include_router(messaging.router, prefix="/messaging", tags=["Messaging Actions"])

@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "LINE Webhook API is running"}

# add this to your main.py
if __name__ == "__main__":
    import uvicorn
    from pyngrok import ngrok
    import os

    # Set your auth token if you have one (optional but recommended)
    ngrok.set_auth_token(os.environ.get("NGROK_AUTH_TOKEN"))

    # Open a tunnel to port 8080
    public_url = ngrok.connect(8080).public_url
    print(f" * ngrok tunnel available at {public_url}")
    print(f" * LINE Webhook URL should be: {public_url}/webhook/callback")

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
