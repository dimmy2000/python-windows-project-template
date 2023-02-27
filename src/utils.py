# Standard Library
import os

# Third Party Library
import pywintypes
import win32com.client
from tenacity import TryAgain, retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

# Local Modules
from src.loggers import logger


@retry(stop=stop_after_attempt(3), wait=wait_fixed(15))
def send_email(addrs, subject, msg_body=None, msg_html_body=None, attachment=None):
    logger.info("Trying to send e-mail")
    try:
        Application = win32com.client.Dispatch("Outlook.Application")
        mail = Application.CreateItem(0)
        mail.To = addrs
        mail.Subject = subject
        if msg_body is not None:
            mail.Body = msg_body
        if msg_html_body is not None:
            mail.HTMLBody = msg_html_body
        if attachment is not None:
            if isinstance(attachment, list):
                for item in attachment:
                    mail.Attachments.Add(item)
            else:
                mail.Attachments.Add(attachment)
        mail.Send()
        return True
    except pywintypes.com_error:
        logger.exception("Outlook doesn't respond. Restart")
        os.system("taskkill /im outlook.exe /f")
        os.system("start outlook")
        send_email(addrs, subject, msg_body, msg_html_body, attachment)
    except Exception:
        logger.exception("Sending e-mail failed. Retry")
        raise TryAgain
