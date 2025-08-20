import qrcode

# Change phone number for testing
phone_number = "919090578737"

# Use your local IP and Flask port
url = f"http://192.168.1.12:5000/scan?phone={phone_number}"

qr = qrcode.make(url)
qr.save("qr_code.png")

print(f"✅ QR code generated for {phone_number} and saved as qr_code.png")
print(f"Scan the QR code to open: {url}")
