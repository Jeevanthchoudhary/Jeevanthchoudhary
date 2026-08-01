import subprocess
import sys

def run_script(script_path):
    print(f"Running {script_path}...")
    result = subprocess.run([sys.executable, script_path])
    if result.returncode != 0:
        print(f"Error: {script_path} failed.")
        sys.exit(result.returncode)

def main():
    print("Starting GitHub Profile Build Process...")
    
    # 1. Generate Info Card
    run_script("scripts/make_info_card.py")
    
    # 2. Fetch Contributions Data
    run_script("scripts/fetch_contributions.py")
    
    # 3. Render Heatmap SVG
    run_script("scripts/render_heatmap_svg.py")
    
    print("Build complete! All SVGs and data files are up to date.")

if __name__ == "__main__":
    main()