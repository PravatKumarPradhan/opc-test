from flask import Blueprint, request, render_template, redirect
from database import save_number, SessionLocal, Scan

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/scan")
def scan():
    phone_number = request.args.get("phone")
    if phone_number:
        save_number(phone_number)
        return redirect(f"https://wa.me/{phone_number}?text=Welcome%20to%20OPC!")
    return "No phone number provided", 400

@bp.route("/admin/scans")
def admin_scans():
    session = SessionLocal()
    try:
        scans = session.query(Scan).order_by(Scan.timestamp.desc()).all()
        return render_template("admin_scans.html", scans=scans)
    finally:
        session.close()
