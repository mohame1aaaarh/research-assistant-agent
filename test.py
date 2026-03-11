from database.auth import register_user, login_user

register_user("ahmed", "ahmed123")
result = login_user("ahmed", "ahmed123")
print(result)