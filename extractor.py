from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

# 1. Provide correct paths
pdf_path = 'Istiak_Ahasan.pdf'
poppler_path = r'C:\Users\USER\Downloads\poppler-24.08.0\Library\bin'  # 👈 Replace this with the correct folder!




# 2. Convert PDF to images
images = convert_from_path(pdf_path, poppler_path=poppler_path)

# 3. Create output folder
os.makedirs("output_images", exist_ok=True)

# 4. OCR each page
all_text = ""
for i, image in enumerate(images):
    image_path = f"output_images/page_{i+1}.png"
    image.save(image_path, 'PNG')
    text = pytesseract.image_to_string(Image.open(image_path))
    all_text += f"\n\n--- Page {i+1} ---\n{text}"

# 5. Save the extracted text
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("✅ Text extraction complete. Saved to 'extracted_text.txt'.")









