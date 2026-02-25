import os

path_to_key = os.path.expanduser(r"C:\Users\LENOVO\Desktop\Api Key.txt")

try:
    with open(path_to_key, "r") as file:
        API_KEY = file.read().strip()
except FileNotFoundError:
    print("خطأ: لم يتم العثور على ملف المفتاح في سطح المكتب!")
    API_KEY = None

GEMINI_API_KEY: str = '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'
APP_NAME: str = "Research Assistant Agent"
DATABASE_PATH: str = "database/conversations.db"
MAX_SEARCH_RESULTS: int = 5

