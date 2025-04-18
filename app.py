import smtplib
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sender_email = os.getenv("SENDER_EMAIL")
app_password = os.getenv("APP_PASSWORD")

subject = "Prakrithi Analysis Final Report"

@app.get('/')
def read_root():
    return {"FastAPI is running"}

@app.post("/send_email")
async def send_email(
    recipient_name: str = Form(...),
    recipient_email: str = Form(...),
    file: UploadFile = File(None)
):
    body = f"""
    Dear {recipient_name},

    I hope this message finds you well. Attached below, you will find the Prakrithi Analysis Final Report for your review. If you have any questions or require further assistance, 
    
    please don't hesitate to reach out. We are happy to help!

    Best regards,  
    Team Parakram
    """

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.set_content(body)

    if file:
        file_data = await file.read()
        message.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file.filename)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(message)
        return {"message": 1}
    except Exception as e:
        return {"message": 0}
