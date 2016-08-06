import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# TODO: Make this class more general


class Emailer:

    def __init__(self, destination, me, subject):
        self.destination = destination
        self.me = me
        self.subject = subject

    def format_html_link(self, video_id, title):
        link = "http://youtube.com/watch?v=" + video_id
        if not title:
            html = """\
                <html>
                <head></head>
                <body>
                    <p>Hi!<br>
                    A new episode is out!<br>
                    Here is the <a href="{link}">link</a>.
                    </p>
                </body>
                </html>
                """.format(link=link)
        else:
            html = """\
            <html>
            <head></head>
            <body>
                <p>Hi!<br>
                A new episode is out!<br>
                {title} <br>
                Here is the <a href="{link}">link</a>.
                </p>
            </body>
            </html>
            """.format(link=link, title=title)
        return html

    def format_text_link(self, video_id):
        link = "http://youtube.com/watch?v=" + video_id
        text = "New episode of Zero Time Dilemma!\n" + link
        return text

    def send_email(self, video_id, title=""):

        # Format the body of the email
        html = self.format_html_link(video_id, title)
        text = self.format_text_link(video_id)

        # Create the message type - will contain html with text backup
        message = MIMEMultipart('alternative')
        message['Subject'] = "New Episode of Zero Time Dilemma!"
        message['From'] = self.me
        message['To'] = self.destination

        # Set the MIME types, plain text as a fallback, and ideally HTML
        text_part = MIMEText(text, 'plain')
        html_part = MIMEText(html, 'html')
        message.attach(text_part)
        message.attach(html_part)

        # Send the message via local SMTP server - in practice Postfix send-only server
        server = smtplib.SMTP('localhost')
        server.sendmail(self.me, self.destination, message.as_string())
        server.quit()
