
from app.pdf_reader import extract_pages, identify_page, parse_invoice

pdf_path = "uploads/1276_U_S_ENTERPRISES_1.pdf"

# Step 1: Read all PDF pages
pages = extract_pages(pdf_path)

invoice_pages = []

for number, text in enumerate(pages, start=1):
    page_type = identify_page(text)
    print(f"Page {number}: {page_type}")

    # Include Tax Invoice pages only
    if page_type == "TAX INVOICE":
        invoice_pages.append(text)

# Step 2: Combine invoice pages
combined_text = "\n".join(invoice_pages)

# Step 3: Print item-related OCR lines
print("\n--- ITEM ROWS FROM OCR ---")

for line in combined_text.splitlines():
    if "85362030" in line:
        print(repr(line))

# Step 4: Extract invoice data
invoice = parse_invoice(combined_text)

print("\n--- INVOICE DATA ---")
print("Invoice No:", invoice["invoice_no"])
print("Invoice Date:", invoice["invoice_date"])
print("Buyer:", invoice["buyer_name"])
print("State:", invoice["state"])

# Step 5: Print extracted items
print("\n--- ITEMS ---")

for item in invoice["items"]:
    print(item)

print("\nTotal Items Extracted:", len(invoice["items"]))

# Step 6: Check important OCR lines
print("\n--- CHECK OCR TEXT ---")

for line in combined_text.splitlines():
    if any(word in line.lower() for word in [
        "asg",
        "state name",
        "buyer (bill to)",
        "invoice no"
    ]):
        print(repr(line))
