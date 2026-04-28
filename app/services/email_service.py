# app/services/email_service.py

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="rrs@cue.edu.ge",
    MAIL_PASSWORD="wwhlbtmrjmkgxptz",
    MAIL_FROM="rrs@cue.edu.ge",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_email(subject: str, email_to: str, body: str):
    try:
        message = MessageSchema(
            subject=subject,
            recipients=[email_to],
            body=body,
            subtype="html"
        )
        fm = FastMail(conf)
        await fm.send_message(message)
        print("✅ მეილი გაიგზავნა!")
    except Exception as e:
        print(f"❌ შეცდომა: {e}")