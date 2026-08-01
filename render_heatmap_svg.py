import json
import os

LEVEL_COLORS = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353"
}

def render_heatmap(json_path: str, output_svg_path: str):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Contributions data not found at {json_path}")
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    days = data.get("days", [])
    total = data.get("total", 0)
    
    box_size = 11
    box_gap = 4
    step = box_size + box_gap
    
    svg_width = 860
    svg_height = 160
    
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%" style="background-color: #0d1117;">',
        '<style>',
        '  text { font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, monospace; fill: #8b949e; font-size: 10px; }',
        '  .heat-box { rx: 2px; ry: 2px; transition: fill 0.2s; }',
        '  .reveal { animation: slideDown 1s ease-out forwards; opacity: 0; }',
        '@keyframes slideDown {',
        '  0% { transform: translateY(-10px); opacity: 0; }',
        '  100% { transform: translateY(0); opacity: 1; }',
        '}',
        '</style>',
        f'<rect width="100%" height="100%" fill="#0d1117" rx="6" stroke="#30363d" stroke-width="1"/>',
        '<g class="reveal" transform="translate(20, 25)">'
    ]
    
    weeks = []
    current_week = []
    for day in days:
        current_week.append(day)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week)
        
    for w_idx, week in enumerate(weeks):
        x = w_idx * step
        for d_idx, day in enumerate(week):
            y = d_idx * step
            color = LEVEL_COLORS.get(day["level"], "#161b22")
            date_str = day["date"]
            count_str = day["count"]
            svg_parts.append(
                f'  <rect class="heat-box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}">'
                f'<title>{count_str} contributions on {date_str}</title></rect>'
            )
            
    footer_y = 7 * step + 20
    svg_parts.append(f'<text x="0" y="{footer_y}">{total:,} contributions in the last year</text>')
    
    legend_x = svg_width - 180
    svg_parts.append(f'<text x="{legend_x - 30}" y="{footer_y}">Less</text>')
    for idx in range(5):
        lx = legend_x + (idx * (box_size + 3))
        lcolor = LEVEL_COLORS[idx]
        svg_parts.append(f'<rect x="{lx}" y="{footer_y - 9}" width="{box_size}" height="{box_size}" fill="{lcolor}" rx="2"/>')
    svg_parts.append(f'<text x="{legend_x + 5 * (box_size + 3) + 5}" y="{footer_y}">More</text>')
    
    svg_parts.append('</g>')
    svg_parts.append('</svg>')
    
    with open(output_svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
    print(f"Heatmap SVG rendered successfully at {output_svg_path}")

if __name__ == "__main__":
    render_heatmap("data/contributions.json", "contrib-heatmap.svg")