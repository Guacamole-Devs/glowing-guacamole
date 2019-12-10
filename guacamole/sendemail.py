
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import url_for
import base64
import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from random import randint
from guacamole.db import get_db,close_db

def sendmail(toaddrs,code,username):
    fromaddr = "soerem98@zedat.fu-berlin.de"
    message = MIMEMultipart()
    message["From"] = fromaddr
    message["To"] = toaddrs
    message["Subject"] = f"DEIN CODE: {code}"
    message["Bcc"] = "receiver_email"
    z = url_for("auth.validate", code=code,username=username)
    x = f"DEIN CODE: {code}\n LINK: {"http://127.0.0.1:5000"+ z}"
    message.attach(MIMEText(x, 'plain'))


    server = smtplib.SMTP('mail.zedat.fu-berlin.de',port=587)

    server.starttls()
    server.ehlo()
    server.login("soerem98",base64.b64decode(b'UXh6MTA4MjMhIg==').decode("utf-8"))

    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, message.as_string())
    server.quit()