import json
import os

notebook_path = r'd:\project\Customer Segmentation using RFM\notebooks\01_data_loading.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Find the cell defining data_path
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            if "data_path = 'data/raw/'" in source:
                # Fix the path to be relative to the notebook location
                cell['source'] = [line.replace("data_path = 'data/raw/'", "data_path = '../data/raw/'") for line in cell['source']]
                print("Fixed data_path.")
                break
    
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

except Exception as e:
    print(f"Error: {e}")
