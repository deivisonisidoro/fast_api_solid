from typing import List

from pydantic import BaseModel


class MessageSchema(BaseModel):
    subject: str
    recipients: List[str]
    body: str
