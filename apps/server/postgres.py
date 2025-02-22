import json
import logging
from typing import List, Optional, Dict
import uuid
from datetime import datetime
from langchain.schema.messages import AIMessage, HumanMessage
from models.chat_message import ChatMessage
from fastapi_sqlalchemy import db
from typings.user import UserOutput

from langchain.schema import (
    BaseChatMessageHistory,
    BaseMessage,
    _message_to_dict,
    messages_from_dict,
)

logger = logging.getLogger(__name__)


class ChatMessageJSONEncoder(json.JSONEncoder):
    def default(self, obj: object):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        if isinstance(obj, datetime):
            # for datetime objects, convert to string in your preferred format
            return obj.isoformat()
        return super().default(obj)


class PostgresChatMessageHistory(BaseChatMessageHistory):
    def __init__(
            self,
            account_id: str,
            user_id: str,
            user: UserOutput,
            session_id: str,
            parent_id: Optional[str] = None,
            version: Optional[str] = None,
    ):
        self.account_id = account_id
        self.user_id = user_id
        self.user = user
        self.version = version
        self.session_id = session_id
        self.parent_id = parent_id

    def fetch_messages(self):
        try:
            chat_messages = (db.session.query(ChatMessage)
                         .filter(ChatMessage.session_id == self.session_id)
                        #  .options(joinedload(ChatMessage.parent))
                         .order_by(ChatMessage.created_on.desc())
                         .limit(50)
                         .all())

            result = []
            for chat_message in chat_messages:
                chat_message_dict = chat_message.to_dict()
                if chat_message.parent:
                    parent_dict = chat_message.parent.to_dict()
                    chat_message_dict['parent'] = parent_dict
                result.append(chat_message_dict)

            result.reverse()
          
            return result
        except Exception as e:
            print(f"Error fetching messages: {e}")
        return []

    @property
    def messages(self) -> List[BaseMessage]:  # type: ignore
        """Retrieve the messages from PostgreSQL"""
        items = [record["message"] for record in self.fetch_messages()]

        # We add user message before calling agent. When agent gets message history we remove user's current question.
        items.pop()

        messages = messages_from_dict(items)
        return messages

    def get_messages(self):
        """Retrieve the messages from PostgreSQL"""
        return self.fetch_messages()

    def create_message(self, message, parent_id):
        # Append the message to the record in PostgreSQL
        chat_message = ChatMessage(
            user_id=self.user_id,
            account_id=self.account_id,
            message=_message_to_dict(message),
            version=self.version,
            session_id=self.session_id,
            parent_id=parent_id
        )

        db.session.add(chat_message)
        db.session.commit()
        db.session.refresh(chat_message)


        # Serialize the model instance's data dictionary
        data_dict = chat_message.to_dict()
        if chat_message.parent:
            parent_dict = chat_message.parent.to_dict()
            data_dict['parent'] = parent_dict
      
        data_json = json.dumps(data_dict, cls=ChatMessageJSONEncoder)  # Use default=str to handle UUID and datetime
        # print("the result", json.loads(data_json))
        return json.loads(data_json)

    def create_ai_message(self, message: str, parent_id: str):
        return self.create_message(AIMessage(content=message), parent_id)

    def create_human_message(self, message: str):
        print("human parent id", self.parent_id)
        return self.create_message(HumanMessage(content=message, additional_kwargs={
            "name": self.user.name,
        }), parent_id=self.parent_id)

    def add_message(self, message: BaseMessage) -> str:
        """Append the message to the record in PostgreSQL"""
        return ""

    def update_thoughts(self, message_id: str, thoughts: List[Dict]):
        chat_message: ChatMessage = db.session.query(ChatMessage).get(message_id)
        chat_message.thoughts = thoughts
        db.session.commit()

        updated_message_json = json.dumps(chat_message.to_dict(), cls=ChatMessageJSONEncoder)
        return json.loads(updated_message_json)

    def delete_message(self, message_id: str):
        chat_message: ChatMessage = db.session.query(ChatMessage).get(message_id)
        db.session.delete(chat_message)
        db.session.commit()

    def clear(self) -> None:
        """Clear session memory from PostgreSQL"""
        return None

    def __del__(self) -> None:
        return None
