from PIL import Image, ImageOps
import os

# Paths
INPUT_IMAGE = "assets/profile.jpg"
OUTPUT_IMAGE = "assets/source-prepped.png"

# Load image
img = Image.open(INPUT_IMAGE).convert("L")  # Convert to grayscale

# Improve contrast automatically
img = ImageOps.autocontrast(img)

# Resize while keeping aspect ratio
WIDTH = 100
aspect_ratio = img.height / img.width
HEIGHT = int(WIDTH * aspect_ratio * 0.55)  # Character height correction

img = img.resize((WIDTH, HEIGHT))

# Create output directory if needed
os.makedirs("assets", exist_ok=True)

# Save
img.save(OUTPUT_IMAGE)

print(f"Saved preprocessed image to {OUTPUT_IMAGE}")