import smtplib

class EmailClient:

    def __init__(self, smtp_server, smtp_port, username, password, recipients):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.recipients = recipients

    def send_email(self, subject, body):
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(self.username, self.password)

            message = f"Subject: {subject}\n\n{body}"

            smtp.sendmail(self.username, self.recipients, message)
