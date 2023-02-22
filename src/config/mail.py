from fastapi_mail import ConnectionConfig

from .settings import Settings


class MailConfig:
    def __init__(self, mail_from: str, settings=Settings()) -> None:
        self.mail_from = mail_from
        self.settings = settings

    def set_mail_configuration(self):
        conf = ConnectionConfig(
            MAIL_USERNAME=self.settings.EMAIL_HOST_USER,
            MAIL_PASSWORD=self.settings.EMAIL_HOST_PASSWORD,
            MAIL_FROM=self.mail_from,
            MAIL_PORT=self.settings.EMAIL_PORT,
            MAIL_SERVER=self.settings.EMAIL_HOST,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
        )
        return conf
