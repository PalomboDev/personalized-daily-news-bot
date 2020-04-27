import smtplib
from email.message import EmailMessage


class EmailClient:

    def __init__(self, smtp_server, smtp_port, username, password, recipients):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.recipients = recipients

    def send_email(self, subject, body, body_alternative=None):
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
            smtp.login(self.username, self.password)

            for recipient in self.recipients:
                message = EmailMessage()

                message["Subject"] = subject
                message["From"] = self.username
                message["To"] = recipient

                message.set_content(body)

                if body_alternative is not None:
                    message.add_alternative(body_alternative, subtype="html")

                smtp.send_message(message)
