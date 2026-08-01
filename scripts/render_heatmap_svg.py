import os
import json
from datetime import datetime

def render_heatmap():
    data_path = 'data/contributions.json'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Run fetch_contributions.py first.")
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        days = json.load(f)

    # Calculate stats
    total_contributions = sum(day['count'] for day in days)
    
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    # Sort days chronologically just in case
    sorted_days = sorted(days, key=lambda x: x['date'])
    
    for day in sorted_days:
        if day['count'] > 0:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 0

    # Calculate current streak from the end backwards
    for day in reversed(sorted_days):
        if day['count'] > 0:
            current_streak += 1
        else:
            # Allow today to be 0 if no contributions yet
            if day == sorted_days[-1]:
                continue
            break

    # GitHub dark theme color map for levels
    colors = {
        0: '#161b22',
        1: '#0e4429',
        2: '#006d32',
        3: '#26a641',
        4: '#39d353'
    }

    # Group days by weeks (columns)
    weeks = []
    current_week = []
    for i, day in enumerate(sorted_days):
        current_week.append(day)
        if len(current_week) == 7 or i == len(sorted_days) - 1:
            weeks.append(current_week)
            current_week = []

    # SVG Dimensions
    cell_size = 11
    cell_gap = 4
    left_pad = 20
    top_pad = 20
    
    width = left_pad + len(weeks) * (cell_size + cell_gap) + 20
    height = 180

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '<style>',
        '  .bg { fill: #0d1117; }',
        '  .border { stroke: #30363d; stroke-width: 2; fill: none; }',
        '  .text { font: 12px monospace; fill: #8b949e; }',
        '  .bold { font-weight: bold; fill: #c9d1d9; }',
        '  @keyframes reveal {',
        '    0% { opacity: 0; transform: translateY(10px); }',
        '    100% { opacity: 1; transform: translateY(0); }',
        '  }',
        '  .animate-heatmap { animation: reveal 1s ease-out forwards; }',
        '</style>',
        f'<rect width="{width}" height="{height}" rx="10" class="bg" />',
        f'<rect width="{width}" height="{height}" rx="10" class="border" />',
        '<g class="animate-heatmap" transform="translate(20, 20)">'
    ]

    # Render grid cells
    for w_idx, week in enumerate(weeks):
        for d_idx, day in enumerate(week):
            x = w_idx * (cell_size + cell_gap)
            y = d_idx * (cell_size + cell_gap)
            color = colors.get(day['level'], colors[0])
            date_str = day['date']
            count = day['count']
            
            svg_parts.append(
                f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}">'
                f'<title>{count} contributions on {date_str}</title></rect>'
            )

    # Stats footer inside SVG
    stats_y = 7 * (cell_size + cell_gap) + 25
    svg_parts.extend([
        f'  <text x="0" y="{stats_y}" class="text">Total: <tspan class="bold">{total_contributions}</span</text>',
        f'  <text x="180" y="{stats_y}" class="text">Current Streak: <tspan class="bold">{current_streak}d</tspan></text>',
        f'  <text x="360" y="{stats_y}" class="text">Longest Streak: <tspan class="bold">{longest_streak}d</tspan></text>',
        '</g>',
        '</svg>'
    ] )

    os.makedirs('assets', exist_ok=True)
    output_path = 'contrib-heatmap.svg'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_parts))

    print(f"Successfully generated {output_path}")

if __name__ == '__main__':
    render_heatmap()