import pytesseract
from PIL import Image
import os
import re
import time

# ---------------------------------------
# FOLDER where ShareX saves screenshots
# ---------------------------------------
FOLDER = "/mnt/c/Users/hr306/Downloads/ShareX-18.0.1-portable/ShareX/Screenshots/2025-12"

# WSL uses its own tesseract install, no need to set path!
# pytesseract will find /usr/bin/tesseract automatically.

OUTPUT_FILE = "emails.txt"
EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

seen = set()

print("Watching folder:", FOLDER)
print("Press CTRL+C to stop\n")

while True:
    try:
        for filename in os.listdir(FOLDER):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                fullpath = os.path.join(FOLDER, filename)

                # open screenshot
                try:
                    img = Image.open(fullpath)
                except:
                    continue

                # OCR
                text = pytesseract.image_to_string(img)

                # find emails
                emails = re.findall(EMAIL_REGEX, text)

                new = 0
                with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                    for email in emails:
                        email = email.lower().strip()
                        if email not in seen:
                            seen.add(email)
                            f.write(email + "\n")
                            new += 1

                if new > 0:
                    print("New emails found:", new)

                # delete processed screenshot
                os.remove(fullpath)

        time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopped by user. Unique emails:", len(seen))
        break

