from PIL import Image
import html

RAMP = "@%#*+=-:. "

INPUT = "assets/source-prepped.png"
OUTPUT = "avi-ascii.svg"

img = Image.open(INPUT).convert("L")

pixels = img.load()
w, h = img.size

FONT_SIZE = 8
CHAR_W = 6
CHAR_H = 9

lines = []

for y in range(h):
    row = ""
    for x in range(w):
        p = pixels[x, y]

        # Invert brightness
        idx = int((255 - p) / 255 * (len(RAMP) - 1))
        row += RAMP[idx]

    lines.append(row)

svg_height = h * CHAR_H + 20
svg_width = w * CHAR_W + 20

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{svg_width}"
height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}"
style="background:black">

<style>
text {{
font-family: Consolas, monospace;
font-size:{FONT_SIZE}px;
fill:#d0d0d0;
}}

@keyframes typing {{
from {{opacity:0;transform:translateX(-20px);}}
to {{opacity:1;transform:translateX(0);}}
}}
</style>
'''

for i, line in enumerate(lines):
    delay = i * 0.03

    svg += f'''
<text
x="10"
y="{15+i*CHAR_H}"
style="opacity:0;
animation:typing .3s forwards;
animation-delay:{delay}s;">
{html.escape(line)}
</text>
'''

svg += "</svg>"

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(svg)

print("Created avi-ascii.svg")