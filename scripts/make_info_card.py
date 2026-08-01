CARD = """<svg xmlns="http://www.w3.org/2000/svg"
width="520"
height="330">

<style>
text{
font-family:Consolas,monospace;
fill:#d0d0d0;
font-size:18px;
}

.title{
fill:#39d353;
font-size:22px;
font-weight:bold;
}

.line{
opacity:0;
animation:fade .4s forwards;
}

@keyframes fade{
from{opacity:0;transform:translateX(20px);}
to{opacity:1;transform:translateX(0);}
}
</style>

<rect width="100%" height="100%" fill="#0d1117"/>

<text x="20" y="35" class="title">jeevanth@github</text>
"""

rows = [
    ("Name", "B Jeevanth"),
    ("Role", "AI & Full Stack Developer"),
    ("College", "NEC Gudur"),
    ("Location", "Andhra Pradesh"),
    ("Projects", "SentinelEdu"),
    ("Projects", "Opportunity Radar"),
    ("OSS", "FOSSASIA Contributor"),
    ("Frontend", "React, Tailwind"),
    ("Backend", "FastAPI, Node.js"),
    ("Languages", "Python, JavaScript, C++"),
    ("Database", "PostgreSQL, Firebase"),
    ("AI/ML", "TensorFlow, OpenCV"),
    ("Dream", "Building AI for Millions")
]

y = 70

for i, (k, v) in enumerate(rows):
    CARD += f'''
<text
x="20"
y="{y}"
class="line"
style="animation-delay:{i*0.2}s">
{k:<12}: {v}
</text>
'''
    y += 22

CARD += "</svg>"

with open("info-card.svg", "w", encoding="utf-8") as f:
    f.write(CARD)

print("info-card.svg created")