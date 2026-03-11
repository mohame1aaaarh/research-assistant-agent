import bcrypt
import sys 
from pathlib import Path
from database.memory import create_user,get_user

project_root= Path(__file__).parent.parent
sys.path.insert(0,str(project_root))

def hash_password(password: str)->str:
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes,bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(password : str,hashed_password:str)->bool :
    password_bytes=password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes,hashed_bytes)

def register_user(username:str,password:str)->dict :
    existing= get_user(username)
    if existing:
        return {"success":False,"error":"this user name is existed"}
    if len(password) < 8:
        return {"success":False,"error":"the length of must be greater than 8 charcter"}
    hashed = hash_password(password)
    user_id=create_user(username,hashed)
    return {"success":True,"user_id":user_id}

def login_user(username:str,password:str)->dict:
    user = get_user(username)
    if not user :
        return {"success":False,"error":"user name is incorrect or not exist"}
    if not verify_password(password,user["password"]):
        return {"success":False,"error":"incorrect password"}
    return {"success":True,"user":user}
