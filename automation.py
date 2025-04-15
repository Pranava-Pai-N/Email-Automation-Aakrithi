import smtplib
import os
from fastapi import FastAPI, UploadFile
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

sender_email = "teamparakram16@gmail.com"
app_password = os.getenv("APP_PASSWORD")

subject = "Prakrithi Analysis Final Report"

@app.get('/')
def read_root():
    return {"FastAPI is running"}

@app.post("/send-email")
async def send_email(recipient_name: str, recipient_email: str, file: UploadFile = None):
    receiver_email = recipient_email

    body = f"""
    Dear {recipient_name},

    I hope this message finds you well. Attached below, you will find the Prakrithi Analysis Final Report for your review. If you have any questions or require further assistance, 
    
    please don't hesitate to reach out. We are happy to help!

    Best regards,  
    Team Parakram
    """

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.set_content(body)

    if file:
        file_data = await file.read()
        message.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file.filename)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(message)
        return {"message": "Email sent successfully!"}
    except Exception as e:
        return {"message": f"Failed to send email. Error: {str(e)}"}
