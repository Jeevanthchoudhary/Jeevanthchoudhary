import os
import cv2

# Density ramp from sparse to dense
RAMP = " .:-=+*#%@"

def generate_ascii_svg(image_path: str, output_svg_path: str, cols: int = 90):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Prepped image not found at '{image_path}'. Run prep_photo.py first!")

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Failed to load image at '{image_path}'. Ensure it's a valid image file.")
    
    h, w = img.shape
    # Calculate rows maintaining aspect ratio (characters are taller than wide, approx 2:1 ratio)
    rows = int(cols * (h / w) * 0.55)
    
    resized = cv2.resize(img, (cols, rows))
    
    # Build ASCII grid matrix
    lines = []
    for y in range(rows):
        line_chars = []
        for x in range(cols):
            pixel_val = resized[y, x]
            idx = int((pixel_val / 255.0) * (len(RAMP) - 1))
            line_chars.append(RAMP[idx])
        lines.append("".join(line_chars))
        
    char_width = 7.2
    char_height = 14
    svg_width = cols * char_width
    svg_height = rows * char_height
    
    # SVG Template with row-by-row clipping reveal animation
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%" style="background-color: #0d1117;">',
        '<style>',
        '  text { font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace; font-size: 12px; fill: #c9d1d9; }',
        '  .row-clip { animation: wipe 0.8s ease-in-out forwards; opacity: 0; }',
    ]
    
    # Generate staggered delays for each row
    for i in range(rows):
        delay = i * 0.02
        svg_parts.append(f'  #row-{i} {{ animation-delay: {delay:.2f}s; }}')
        
    svg_parts.extend([
        '@keyframes wipe {',
        '  0% { clip-path: inset(0 100% 0 0); opacity: 1; }',
        '  100% { clip-path: inset(0 0% 0 0); opacity: 1; }',
        '}',
        '</style>',
        f'<rect width="100%" height="100%" fill="#0d1117" rx="6"/>',
        '<g transform="translate(10, 20)">'
    ])
    
    for i, line in enumerate(lines):
        # Escape special XML characters
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        svg_parts.append(f'  <text id="row-{i}" class="row-clip" x="0" y="{i * char_height}">{escaped_line}</text>')
        
    svg_parts.append('</g>')
    svg_parts.append('</svg>')
    
    # Save output to root directory so README can read it easily
    with open(output_svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
    print(f"ASCII SVG generated successfully at {output_svg_path}")

if __name__ == "__main__":
    # Point directly to the assets folder where prep_photo.py saves it
    input_img = "assets/source-prepped.png"
    output_svg = "avi-ascii.svg"
    generate_ascii_svg(input_img, output_svg)