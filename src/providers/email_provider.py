from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, MessageType

from src.config.mail import MailConfig

from .interfaces.iemail_provider import IEmailProvider


class EmailProvider(IEmailProvider):
    """
    Email provider implementation for sending emails using FastMail.

    Attributes:
        conf (MailConfig): Configuration object for FastMail.
        fm (FastMail): FastMail instance for sending emails.
    """

    def __init__(self):
        """
        Constructs a new instance of the EmailProvider class.
        """
        self.conf = MailConfig(mail_from="solid_fast_api@example.com").set_mail_configuration()
        self.fm = FastMail(self.conf)

    async def _send_email(self, recipients: list, subject: str, body: str, subtype: MessageType):
        """
        Sends an email using the FastMail instance.

        Args:
            recipients (list): List of email recipients.
            subject (str): Email subject.
            body (str): Email body.
            subtype (MessageType): Email subtype.

        Returns:
            None.
        """
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
        """
        Sends an email in the background.

        Args:
            recipients (list): List of email recipients.
            subject (str): Email subject.
            body (str): Email body.
            subtype (MessageType): Email subtype.
            background_tasks (BackgroundTasks): FastAPI background tasks.

        Returns:
            None.
        """
        background_tasks.add_task(self._send_email, recipients, subject, body, subtype)
