from fastapi_mail import ConnectionConfig

from .settings import Settings


class MailConfig:
    """Class responsible for configuring email settings."""

    def __init__(self, mail_from: str, settings=Settings()) -> None:
        """
        Initialize a new instance of `MailConfig`.

        Args:
            mail_from (str): The email address to use as the default `from` address.
            settings (Settings, optional): An instance of `Settings` containing the email settings. Defaults to the default `Settings` instance.

        Returns:
            None
        """
        self.mail_from = mail_from
        self.settings = settings

    def set_mail_configuration(self):
        """
        Set the email configuration.

        Returns:
            ConnectionConfig: A `ConnectionConfig` object with the email configuration.
        """
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
