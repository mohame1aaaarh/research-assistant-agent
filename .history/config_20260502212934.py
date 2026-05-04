import os
with open(r'key.txt', 'r') as file:
    api_key = file.read()
    
OPENROUTER_KEY: str = api_key
APP_NAME: str = "Research Assistant Agent"
DATABASE_PATH: str = "database/conversations.db"
MAX_SEARCH_RESULTS: int = 5
os.environ["CHAINLIT_AUTH_SECRET"] = "wCgBz6L-Mz$fJyweuW4jS,%SogY4iloQzcdjVcmoc3q1m0J0KbZg,Sw9EZ54SVp9"
