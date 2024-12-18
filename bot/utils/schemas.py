from pydantic import BaseModel


class Profile(BaseModel):
    balance: int
    available_messages_count: int
    sent_messages_count: int
