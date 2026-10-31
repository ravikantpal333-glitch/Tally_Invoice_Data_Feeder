from google_drive import upload_pdf_to_drive

pdf_path = "uploads/1264 Singh Switchgear.pdf"

try:
    link = upload_pdf_to_drive(pdf_path, "TEST_1264 Singh Switchgear.pdf")
    print("Upload OK. Link:", link)
except Exception as e:
    print("Upload FAILED:", e)