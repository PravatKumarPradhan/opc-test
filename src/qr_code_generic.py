import qrcode

# URL of the form (no personal parameter)
form_url = "http://192.168.1.12:5000/scan"

qr = qrcode.make(form_url)
qr.save("qr_code_generic.png")

print("✅ Generic QR code generated for the form.")
print(f"Scan the QR code to open: {form_url}")
