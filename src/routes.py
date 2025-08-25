import json
import logging
import os

from flask import Blueprint, request, render_template, flash
from twilio.rest import Client
from src.database import save_number, SessionLocal, Scan, get_next_serial
import qrcode
import io
from flask import send_file

# Setup logging (put this once in your app.py or main entry point)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)
# Define single blueprint
bp = Blueprint("main", __name__)

# Twilio config (replace with your credentials)
#TWILIO_SID = 'ACbf4cab149c7f09ad56d21b12bfe3be6f'
#TWILIO_AUTH_TOKEN = 'a8b7feceb43ac8b9934a7b787a57ab2'
# Load Twilio credentials from environment variables
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
#TWILIO_WHATSAPP ='whatsapp:+14155238886'  # Twilio sandbox number
TWILIO_WHATSAPP ='whatsapp:+917064578737'  # Twilio sandbox number

client = Client(account_sid, auth_token)


@bp.route("/")
def index():
    return render_template("index.html")





@bp.route("/qr")
def qr():
   ## wa_link = "https://wa.me/14155238886?text=join%20cute-panda"
    #wa_link = "http://172.20.10.4:5000/scan"
    wa_link = "https://opc-test.onrender.com/scan"
    img = qrcode.make(wa_link)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


def generate_unique_code( serial_num):
    return f"OPC_FC:{serial_num:04d}"

@bp.route("/scan", methods=["GET", "POST"])
def scan():
    if request.method == "POST":
        phone = request.form.get("phone")
        name = request.form.get("name")
        if phone:
            # Example: get_next_serial() fetches and increments serial from DB
            serial_num = get_next_serial()  # implement this based on your DB
            unique_code = generate_unique_code(serial_num)

            # Save user data with unique code as needed
            save_number(phone, name, unique_code)

            # Send WhatsApp message including the unique code
            try:
                client.messages.create(
                    from_=TWILIO_WHATSAPP,
                    to=f"whatsapp:+91{phone}",
                    content_sid='HXd86f798c23cc09882f161d75d5d53814',
                    content_variables=json.dumps({
                        "1": name
                    })
                )

                flash("✅ WhatsApp message sent!")
            except Exception as e:
                logger.error("Error while sending WhatsApp message", exc_info=True)
                flash(f"⚠️ Failed to send WhatsApp message: {e}")

            return render_template("thankyou.html", phone=phone, unique_code=unique_code)

    return render_template("scan_form.html")


@bp.route("/admin/scans")
def admin_scans():
    session = SessionLocal()
    try:
        scans = session.query(Scan).order_by(Scan.timestamp.desc()).all()
        return render_template("admin_scans.html", scans=scans)
    finally:
        session.close()
