from fastapi import BackgroundTasks, Depends
from fastapi_mail import FastMail, MessageSchema, MessageType

from src.config.mail import MailConfig

from .interfaces.iemail_provider import IEmailProvider


class EmailProvider(IEmailProvider):
    def __init__(self):
        self.conf = MailConfig(mail_from="solid_fast_api@example.com").set_mail_configuration()
        self.fm = FastMail(self.conf)

    async def _send_email(self, recipients: list, subject: str, body: str, subtype: MessageType):
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=subtype,
        )

        await self.fm.send_message(message)

    async def send_email(
        self,
        recipients: list,
        subject: str,
        body: str,
        subtype: MessageType,
        background_tasks: BackgroundTasks,
    ):
        background_tasks.add_task(self._send_email, recipients, subject, body, subtype)
