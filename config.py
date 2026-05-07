import os
OPENROUTER_KEY: str = os.getenv("OPENROUTER_KEY", "your_openrouter_api_key_here")
APP_NAME: str = "Research Assistant Agent"
DATABASE_PATH: str = "database/conversations.db"
MAX_SEARCH_RESULTS: int = 5
os.environ["CHAINLIT_AUTH_SECRET"] = os.getenv("CHAINLIT_AUTH_SECRET", "your_chainlit_auth_secret_here")
