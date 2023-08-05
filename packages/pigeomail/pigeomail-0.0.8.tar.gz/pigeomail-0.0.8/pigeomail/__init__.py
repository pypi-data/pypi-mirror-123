# *_*coding:utf-8 *_*
import mimetypes
import smtplib
import time
import uuid
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import doger

logger = doger.guru(level='INFO', name='pigeomail')


class Message(object):
    """
    Represents an email message.

    Set the To, From, Reply-To, Subject, and Body attributes as plain-text strings.
    Optionally, set the Html attribute to send an HTML email, or use the
    attach() method to attach files.

    Use the charset property to send messages using other than us-ascii

    If you specify an attachments argument, it should be a list of
    attachment filenames: ["file1.txt", "file2.txt"]

    `To` should be a string for a single address, and a sequence
    of strings for multiple recipients (castable to list)

    Send using the Mailer class.
    """
    def __init__(self, **kwargs):
        """Message contents
        To: the visible list of primary intended recipients.
        Cc: A visible list of secondary intended recipients.
        """

        # extract  parameters and convert names to lowercase
        params = {}
        for i in kwargs:
            params[i.lower()] = kwargs[i]

        # preprocess attachments
        self.attachments = params.get("attachments", [])

        self.To = params.get("to", [])
        self.Cc = params.get("cc", [])
        self.From = params.get("from", "Anonymous")  # string or iterable
        self.Subject = Header(params.get("subject", ""), "utf-8")  # string
        self.Body = params.get("body", None)
        self.Html = params.get("html", None)
        self.Date = params.get(
            "date", time.strftime("%a, %d %b %Y %H:%M:%S %z", time.gmtime()))
        self.Charset = params.get("charset", "utf-8")
        self.Headers = params.get("headers", {})

        self.message_id = self.make_key()

    def make_key(self):
        return str(uuid.uuid4())

    def header(self, key, value):
        self.Headers[key] = value

    def as_string(self):
        """Get the email as a string to send in the mailer"""

        if not self.attachments:
            return self._multipart()
        else:
            return self._multipart()

    def _set_info(self, msg):
        msg["Subject"] = self.Subject
        msg["From"] = self.From

        if isinstance(self.To, str):
            msg["To"] = self.To
        else:
            msg["To"] = ", ".join(list(set(self.To)))

        if self.Cc:
            if isinstance(self.Cc, str):
                msg["CC"] = self.Cc
            else:
                msg["CC"] = ", ".join(list(set(self.Cc)))

        if self.Headers:
            for key, value in list(self.Headers.items()):
                msg[key] = str(value).encode(self.Charset)

        msg["Date"] = self.Date
        return msg

    def _multipart(self):
        """The email has attachments"""
        msg = MIMEMultipart("related")
        if self.Html:
            msg.attach(MIMEText(self.Html, "html", "utf-8"))
        else:
            msg.attach(MIMEText(self.Body, "plain", "utf-8"))

        self._set_info(msg=msg)

        msg.preamble = self.Subject

        for filename in self.attachments:
            self._add_attachment(msg, filename)

        return msg.as_string().encode()

    def _add_attachment(self, outer, filename):
        """
        If mimetype is None, it will try to guess the mimetype
        """
        ctype, encoding = mimetypes.guess_type(filename)

        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)
        with open(filename, "rb") as fp:
            content = fp.read()

        if maintype == "text":
            # TODO: handle calculating the charset
            msg = MIMEText(_text=content.decode(), _subtype=subtype)
        elif maintype == "application":
            msg = MIMEApplication(_data=content)
        elif maintype == "image":
            msg = MIMEImage(_imagedata=content, _subtype=subtype)
        elif maintype == "audio":
            msg = MIMEAudio(_audiodata=content, _subtype=subtype)
        else:
            msg = MIMEBase(_maintype=maintype, _subtype=subtype)
            msg.set_payload(content)
            # Encode the payload using Base64
            encoders.encode_base64(msg)
        msg.add_header("content-disposition", "attachment", filename=filename)

        outer.attach(msg)


class Mailer:
    def __init__(self, **kwargs):
        # extract  parameters and convert names to lowercase
        params = {}
        for i in kwargs:
            params[i.lower()] = kwargs[i]

        self.host = params.get("host", None)
        self.port = int(params.get("port", None))
        self.user = params.get("user", None)
        self.pass_ = params.get("passwd", None) or params.get("pwd", None)
        self.smtp = self.login()

    def login(self):
        smtp = smtplib.SMTP()  # create an connection
        smtp.connect(self.host)  # connect to mail server
        smtp.login(self.user, self.pass_)  # login to mail server
        return smtp

    def send(self, msg):
        self.smtp.sendmail(from_addr=self.user,
                           to_addrs=msg.To + msg.Cc,
                           msg=msg.as_string())  # send message

        logger.info("Well done ✨")
        # self.smtp.quit()


from .__version__ import version, __version__
