import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
COMMASPACE = ','


def Sendemails():
    logging.info('Start preparing email notification.')
    sender = 'xxx@healthedge.com'
    pwd = ''
    recipients = ['xxx@healthedge.com']

    # Create the enclosing(outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'VPN Alert'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    body = "Please check attachment for failure VPN information!"
    outer.attach(MIMEText(body, 'plain'))
    # List of attachment
    attachments = [".\\no_response_servers.txt", "downvpn.log"]

    # Add the attachment to the message
    for file in attachments:
        try:
            with open(file, 'r') as fhr:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fhr.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise
    composed = outer.as_string()
    # # Send the mail
    # server = smtplib.SMTP('smtp.office365.com', '587')
    # server.starttls()
    # server.login(sender, pwd)
    # server.sendmail(sender, recipients, composed)
    try:
        with smtplib.SMTP('smtp.office365.com', '587') as s:
            # s.ehlo()
            s.starttls()
            # s.ehlo()
            s.login(sender, pwd)
            s.sendmail(sender, recipients, composed)
            s.close()
        #print("EMAIL sent")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise
    logging.info('Email notification has been sent.')

