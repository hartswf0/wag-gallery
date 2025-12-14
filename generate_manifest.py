import os
import json
import re

def main():
    files = [f for f in os.listdir('.') if f.endswith('.json') and 'wag_gold_scene' in f]
    
    valid_files = []
    for f in files:
        if '(1)' in f or 'test-' in f:
            continue
        
        # Check if corresponding PNG exists
        png_file = f.replace('.json', '.png')
        if os.path.exists(png_file):
            valid_files.append(f)
        else:
            print(f"Skipping {f} - missing image {png_file}")
    
    # Sort by date extracted from filename (matching JS logic roughly)
    # Filename format: wag_gold_scene_N_YYYY-MM-DD_...
    def get_date(f):
        m = re.search(r'(\d{4}-\d{2}-\d{2})', f)
        return m.group(1) if m else '0000-00-00'
        
    valid_files.sort(key=get_date)
    
    with open('scenes_manifest.json', 'w') as f:
        json.dump(valid_files, f, indent=2)
        
    print(f"Generated scenes_manifest.json with {len(valid_files)} scenes.")

if __name__ == '__main__':
    main()
