# LINE Bot with Gemini 2.5 Flash & FastAPI

A modern, fast, and intelligent LINE Messaging API bot built with **FastAPI**, integrated with **Google Gemini 2.5 Flash**, and featuring automated local tunneling via **ngrok**.

## 🚀 Features

- **Gemini 2.5 Flash Integration**: Real-time AI-powered conversations.
- **Improved UX**: Automatic "Loading/Typing" animation in LINE while Gemini generates a response.
- **Automated Tunneling**: Built-in `pyngrok` support for instant local testing without manual ngrok setup.
- **Clean Architecture**: Uses FastAPI routers and a dedicated service layer for modular code.
- **Webhook Security**: Full signature verification for incoming LINE events.

## 📁 Project Structure

```text
.
├── main.py              # Application entry point & ngrok setup
├── routers/
│   ├── webhook.py        # Receives & handles LINE Webhook events
│   └── messaging.py      # Actions for pushing messages/getting profiles
├── services/
│   └── line_handler.py   # Core logic (Gemini & LINE SDK calls)
├── .env.example          # Template for environment variables
└── requirements.txt      # Python dependencies
```

## 🛠 Prerequisites

- **Python 3.12+**
- A **LINE Developers Account** and a Messaging API Channel.
- **Google AI Studio API Key** (for Gemini): Get it at [aistudio.google.com](https://aistudio.google.com/).
- **ngrok Auth Token**: Get it at [dashboard.ngrok.com](https://dashboard.ngrok.com/).

## ⚙️ Installation & Setup

1. **Clone the repository** (or navigate to the project folder).
2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   LINE_CHANNEL_ACCESS_TOKEN=your_token
   LINE_CHANNEL_SECRET=your_secret
   GEMINI_API_KEY=your_gemini_key
   NGROK_AUTH_TOKEN=your_ngrok_token
   ```

## 🏃 Running the Bot

Start the application using:

```bash
python main.py
```

Upon startup, the console will print your temporary **public ngrok URL**:
```text
 * ngrok tunnel available at https://xxxx-xxxx.ngrok-free.dev
 * LINE Webhook URL should be: https://xxxx-xxxx.ngrok-free.dev/webhook/callback
```

1. Copy the **Webhook URL** from the terminal.
2. Go to the **LINE Developers Console** > **Messaging API tab**.
3. Paste the URL into the **Webhook URL** field and click **Verify**.
4. Ensure **Use Webhook** is enabled.

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/webhook/callback` | Receives messages and beacon events from LINE. |
| `POST` | `/messaging/push` | Sends a push message to a specific User ID. |
| `GET` | `/messaging/profile/{id}` | Retrieves a user's display name and picture. |
| `GET` | `/docs` | Interactive Swagger API documentation. |

## 📝 License
MIT
