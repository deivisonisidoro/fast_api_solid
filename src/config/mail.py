from fastapi_mail import ConnectionConfig


class MailConfig:
    def __init__(self, mail_from: str) -> None:
        self.mail_from = mail_from

    def set_mail_configuration(self):
        conf = ConnectionConfig(
            MAIL_USERNAME="93b18c8f2ae5c7",
            MAIL_PASSWORD="2a9ef42df82451",
            MAIL_FROM=self.mail_from,
            MAIL_PORT=2525,
            MAIL_SERVER="sandbox.smtp.mailtrap.io",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
        )
        return conf
