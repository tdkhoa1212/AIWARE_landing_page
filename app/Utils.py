# app/utils.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
from .models.User import User

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.check_password(password):
        return None
    return user

def send_verification_email(email: str, verification_link: str):
    from_email = "AIWARE.ai.tech@gmail.com"
    from_password = "xmaf glwn ndls qokw"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = email
    msg['Subject'] = "Account Verification"

    body = f"Please click the following link to verify your account: {verification_link}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(from_email, email, msg.as_string())
    server.quit()
