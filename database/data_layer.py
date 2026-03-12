from chainlit.data.base import BaseDataLayer
from chainlit.types import PageInfo, ThreadDict, PaginatedResponse
import chainlit as cl
from database.memory import get_user_sessions, get_session_messages, get_user_by_id, get_thread_author as get_author
from database.auth import get_user
import sqlite3 as sq
import sys
sys.path.insert(0, ".")
from config import DATABASE_PATH
from database.memory import get_thread_author as get_author, get_user_by_id


class SQLiteDataLayer(BaseDataLayer):

    async def get_user(self, identifier: str):
        user = get_user(identifier)
        if user:
            return cl.PersistedUser(
                id=str(user["id"]),
                identifier=identifier,
                createdAt=user.get("created_at", "")
            )
        return None

    async def create_user(self, user: cl.User):
        return user

    async def list_threads(self, pagination, filters):
        user_id = filters.userId
        db_user = get_user_by_id(int(user_id))

        if not db_user:
            return PaginatedResponse(
                pageInfo=PageInfo(hasNextPage=False, startCursor=None, endCursor=None),
                data=[]
            )

        sessions = get_user_sessions(db_user["id"])
        threads = []
        for session in sessions:
            threads.append(ThreadDict(
                id=str(session["id"]),
                name=session["title"],
                createdAt=session["start_time"],
                userId=str(db_user["id"]),
                userIdentifier=db_user["username"],
                metadata={},
                steps=[],
                elements=[]
            ))

        return PaginatedResponse(
            pageInfo=PageInfo(hasNextPage=False, startCursor=None, endCursor=None),
            data=threads
        )

    async def get_thread(self, thread_id: str):


    # جيب الـ username صاحب الـ thread
     author = get_author(int(thread_id))

     messages = get_session_messages(int(thread_id))
     steps = []
     for msg in messages:
        if msg["role"] in ("user", "assistant"):
            steps.append({
                "id": msg["created_at"],
                "threadId": thread_id,
                "type": "user_message" if msg["role"] == "user" else "assistant_message",
                "output": msg["content"],
                "createdAt": msg["created_at"]
            })

    # جيب الـ user_id
     from database.auth import get_user
     db_user = get_user(author)
     user_id = str(db_user["id"]) if db_user else ""

     print(f"get_thread: thread_id={thread_id}, author={author}, user_id={user_id}")  # مؤقت

     return ThreadDict(
        id=thread_id,
        name="محادثة",
        createdAt="",
        userId=user_id,           # ← مش فاضي
        userIdentifier=author,    # ← مش فاضي
        metadata={},
        steps=steps,
        elements=[]
     )

    async def update_thread(self, thread_id, name=None, user_id=None,
                            metadata=None, tags=None):
        pass

    async def delete_thread(self, thread_id):
        pass

    async def create_step(self, step_dict):
        pass

    async def update_step(self, step_dict):
        pass

    async def delete_step(self, step_id):
        pass

    async def get_thread_author(self, thread_id: str):
        try:
            author = get_author(int(thread_id))
            print(f"thread_id: {thread_id}, author: {author}")  # ← مؤقت
            return author
        except Exception as e:
            print(f"get_thread_author error: {e}")
            return ""

    async def upsert_feedback(self, feedback):
        pass

    async def create_element(self, element):
        pass

    async def get_element(self, thread_id, element_id):
        pass

    async def delete_element(self, element_id):
        pass

    async def build_debug_url(self) -> str:
        return ""

    async def close(self):
        pass

    async def delete_feedback(self, feedback_id: str):
        pass

    async def get_favorite_steps(self, user_id: str):
        return []