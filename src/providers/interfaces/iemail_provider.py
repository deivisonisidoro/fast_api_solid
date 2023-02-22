from abc import ABC, abstractmethod
from typing import List

from fastapi import BackgroundTasks, Depends
from fastapi_mail import MessageType


class IEmailProvider(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def _send_email(self, recipients: List[str], subject: str, body: str, subtype: MessageType):
        pass

    @abstractmethod
    async def send_email(
        self,
        recipients: List[str],
        subject: str,
        body: str,
        subtype: MessageType,
        background_tasks: BackgroundTasks = Depends(),
    ):
        pass
