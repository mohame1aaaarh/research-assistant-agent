import os

path_to_key = os.path.expanduser(r"C:\Users\LENOVO\Desktop\Api Key.txt")

try:
    with open(path_to_key, "r") as file:
        API_KEY = file.read().strip()
except FileNotFoundError:
    print("خطأ: لم يتم العثور على ملف المفتاح في سطح المكتب!")
    API_KEY = None

GEMINI_API_KEY = API_KEY
APP_NAME = "Research Assistant Agent"
DATABASE_PATH = "database/conversations.db"
MAX_SEARCH_RESULTS = 5

