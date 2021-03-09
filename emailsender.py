import asyncio
import email
import mimetypes
import pathlib
import smtplib

import aiosmtplib

class EmailException(Exception):
    def __init__(self, message):
        self.message = message


class EmailSender():
    def __init__(self, login, password):
        self.login    = login
        self.password = password
        if not self.check_credentials():
            raise EmailException("Bad credentials \
                                  or you have not granted access\
                                  from side applications in mail settings")


    def check_credentials(self):
        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.login(self.login, self.password)
            return True
        except Exception as e:
            print(e)
            return False

    async def send_message(self, to_email:str, subject:str, message:str, attachments:list[pathlib.Path]):
        msg = email.message.EmailMessage()

        msg['Subject'] = subject
        msg['From']    = self.login
        msg['To']      = to_email

        msg.set_content(message)

        for attachment in attachments:
            with open(attachment, 'rb') as attachment_descriptor:
                attachment_data = attachment_descriptor.read()

                guessed_type = mimetypes.guess_type(attachment)[0]
                maintype, subtype = guessed_type.split('/')

                msg.add_attachment(attachment_data,
                                    filename  = attachment.name,
                                    maintype  = maintype,
                                    subtype   = subtype)

        return await aiosmtplib.send(msg,
                                    use_tls  = True,
                                    hostname = "smtp.gmail.com",
                                    port     = 465,
                                    username = self.login,
                                    password = self.password)
