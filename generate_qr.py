import qrcode


# Your chatbot URL
website_url = "https://switch41-chatbot.onrender.com/"

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(website_url)
qr.make(fit=True)

# Save QR code in S:\bot
save_path = r"S:\bot\chatbot_qr_code.png"
qr_img = qr.make_image(fill="black", back_color="white")
qr_img.save(save_path)

print(f" QR Code generated and saved at: {save_path}")
