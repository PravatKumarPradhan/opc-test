from flask import Blueprint, request, render_template, flash
from twilio.rest import Client
from src.database import save_number, SessionLocal, Scan
import qrcode
import io
from flask import send_file

# Define single blueprint
bp = Blueprint("main", __name__)

# Twilio config (replace with your credentials)
TWILIO_SID = 'ACbf4cab149c7f09ad56d21b12bfe3be6f'
TWILIO_AUTH_TOKEN = 'e89fab27e11c023162d4d0b786e277f2'
TWILIO_WHATSAPP ='whatsapp:+14155238886'  # Twilio sandbox number

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


@bp.route("/")
def index():
    return render_template("index.html")





@bp.route("/qr")
def qr():
    wa_link = "https://wa.me/14155238886?text=join%20cute-panda"
    img = qrcode.make(wa_link)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@bp.route("/scan", methods=["GET", "POST"])
def scan():
    if request.method == "POST":
        phone = request.form.get("phone")
        if phone:
            save_number(phone)

            try:
                client.messages.create(
                    from_=TWILIO_WHATSAPP,
                    body="🙏 Enjoy your Puja! 🎉",
                    to=f"whatsapp:+{phone}"
                )
                flash("✅ WhatsApp message sent!")
            except Exception as e:
                flash(f"⚠️ Failed to send WhatsApp message: {e}")

            return render_template("thankyou.html", phone=phone)

    return render_template("scan_form.html")


@bp.route("/admin/scans")
def admin_scans():
    session = SessionLocal()
    try:
        scans = session.query(Scan).order_by(Scan.timestamp.desc()).all()
        return render_template("admin_scans.html", scans=scans)
    finally:
        session.close()
