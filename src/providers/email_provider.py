from fastapi import BackgroundTasks, Depends
from fastapi_mail import FastMail, MessageSchema, MessageType

from src.config.mail import MailConfig


class EmailProvider:
    def __init__(self):
        self.conf = MailConfig(mail_from="solid_fast_api@example.com").set_mail_configuration()
        self.fm = FastMail(self.conf)

    async def _send_email(self, recipients: list, subject: str, body: str, subtype: MessageType):
        print(body)
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
        background_tasks: BackgroundTasks = Depends(),
    ):
        background_tasks.add_task(self._send_email, recipients, subject, body, subtype)
