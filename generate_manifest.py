import os
import json
import re

def main():
    files = [f for f in os.listdir('.') if f.endswith('.json') and 'wag_gold_scene' in f]
    
    # Filter out potential dupes or tests if needed, matching the JS logic
    # JS: !href.includes('(1)') && !href.includes('test-')
    valid_files = [f for f in files if '(1)' not in f and 'test-' not in f]
    
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
