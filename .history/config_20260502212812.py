import os
with open('key.txt', 'r') as file:
    api_key = file.read().strip()
print(f"تم تحميل المفتاح بنجاح: {api_key[:5]}****")
OPENROUTER_KEY: str = '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'
APP_NAME: str = "Research Assistant Agent"
DATABASE_PATH: str = "database/conversations.db"
MAX_SEARCH_RESULTS: int = 5
os.environ["CHAINLIT_AUTH_SECRET"] = "wCgBz6L-Mz$fJyweuW4jS,%SogY4iloQzcdjVcmoc3q1m0J0KbZg,Sw9EZ54SVp9"
