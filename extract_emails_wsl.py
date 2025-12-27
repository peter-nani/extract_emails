import pytesseract
from PIL import Image
import os
import time
import regex
import phonenumbers

# ---------------------------------------
# CONFIGURATION
# ---------------------------------------

# ShareX Screenshot Folder (mounted from Windows)
FOLDER = "/mnt/c/Users/hr306/Downloads/ShareX-18.0.1-portable/ShareX/Screenshots/2025-12"

# Output file (stored in WSL or mount to Windows)
OUTPUT_FILE = "emails_phones.txt"


# ---------------------------------------
# EMAIL EXTRACTION (regex module)
# ---------------------------------------
EMAIL_PATTERN = regex.compile(
    r"(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+"
    r"(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,15})"
)

def extract_emails(text: str):
    """
    Extracts email addresses from OCR text using RFC-compliant regex.
    No validators used — pattern matching only.
    """
    return EMAIL_PATTERN.findall(text)


# ---------------------------------------
# PHONE NUMBER EXTRACTION (phonenumbers)
# ---------------------------------------
def extract_phone_numbers(text: str, region="IN"):
    """
    Extracts phone numbers using Google's phonenumbers library.
    Returns numbers in +E164 international format.
    """
    results = []
    for match in phonenumbers.PhoneNumberMatcher(text, region):
        formatted = phonenumbers.format_number(
            match.number, phonenumbers.PhoneNumberFormat.E164
        )
        results.append(formatted)
    return results


# ---------------------------------------
# MAIN OCR PROCESSING LOOP
# ---------------------------------------
seen_emails = set()
seen_phones = set()

print("========================================")
print("  OCR Email + Phone Extractor Running")
print("  Watching folder:", FOLDER)
print("  Press CTRL+C to stop")
print("========================================\n")

while True:
    try:
        for filename in os.listdir(FOLDER):
            if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            fullpath = os.path.join(FOLDER, filename)

            # Open screenshot image
            try:
                img = Image.open(fullpath)
            except:
                continue

            # OCR text extraction
            text = pytesseract.image_to_string(img)

            # Extract data
            found_emails = extract_emails(text)
            found_phones = extract_phone_numbers(text)

            new_items = []

            # Save new emails
            for email in found_emails:
                email = email.lower().strip()
                if email not in seen_emails:
                    seen_emails.add(email)
                    new_items.append(("EMAIL", email))

            # Save new phone numbers
            for phone in found_phones:
                if phone not in seen_phones:
                    seen_phones.add(phone)
                    new_items.append(("PHONE", phone))

            # Write new items to output file
            if new_items:
                with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                    for item_type, value in new_items:
                        f.write(f"{item_type}: {value}\n")

                print("New data found:+1")

            # Remove screenshot after processing
            os.remove(fullpath)

        time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopped by user.")
        print("Total unique emails:", len(seen_emails))
        print("Total unique phone numbers:", len(seen_phones))
        break

