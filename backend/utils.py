import re
import smtplib
from datetime import datetime
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def extract_info(message: str, current_data: dict):
    updates = current_data.copy()

    name_match = re.search(r"(?:my name is|i am)\s+([a-zA-Z ]+)", message, re.I)
    if name_match:
        updates["name"] = name_match.group(1).strip()

    email_match = re.search(r"[\w\.-]+@[\w\.-]+", message)
    if email_match:
        updates["email"] = email_match.group(0)

    phone_match = re.search(r"(\+?\d[\d\s\-\(\)]{9,})", message)
    if phone_match:
        updates["phone"] = phone_match.group(0)

    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", message)
    if date_match:
        updates["move_in"] = date_match.group(1)

    bed_match = re.search(r"(\d+)\s*(?:bed|bedroom)", message, re.I)
    if bed_match:
        updates["beds"] = int(bed_match.group(1))
        updates["unit_id"] = check_inventory(updates["beds"])

    reply = "Thanks! Please continue by sharing your name, email, move-in date, and bedrooms needed."
    return reply, updates

def check_inventory(beds: int) -> str:
    return f"UNIT-{beds}A-101"  

def send_email(data):
    msg = EmailMessage()
    msg['Subject'] = "Tour Confirmation – Homewiz"
    msg['From'] = os.getenv("GMAIL_USER")
    msg['To'] = data['email']
    msg.set_content(f"""
Hello {data['name']},

Thanks for booking a tour with Homewiz!

Your requested unit: {data['unit_id']}
Suggested tour slot: Tomorrow at 3 PM
Address: 123 Homewiz Lane, Hometown

See you soon!
""")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
        smtp.send_message(msg)
