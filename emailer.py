#!/usr/bin/env python

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

    def format_text_link(self, videoId):
        link = "http://youtube.com/watch?v=" + videoId
        text = "New episode of Zero Time Dilemma!\n" + link
        return text

    def send_email(self, videoId, title=""):

        # Format the body of the email
        html = self.format_html_link(videoId, title)
        text = self.format_text_link(videoId)

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "New Episode of Zero Time Dilemma!"
        msg['From'] = self.me
        msg['To'] = self.destination

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via local SMTP server.
        s = smtplib.SMTP('localhost')
        s.sendmail(self.me, self.destination, msg.as_string())
        s.quit()
