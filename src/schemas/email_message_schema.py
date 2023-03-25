from typing import List

from pydantic import BaseModel


class MessageSchema(BaseModel):
    """
    Pydantic schema for an email message.

    Attributes:
        subject (str): The subject of the email.
        recipients (List[str]): List of email addresses of the recipients.
        body (str): The body of the email.
    """

    subject: str
    recipients: List[str]
    body: str
