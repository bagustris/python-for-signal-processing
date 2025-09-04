import json

valid_keys = ['cell_type', 'metadata', 'source']
filename = 'notebook/Compressive_Sampling.ipynb'

with open(filename) as f:
    data = json.load(f)

for index, cell in enumerate(data['cells'], 1):
    if cell['cell_type'] == 'markdown':
        extra_keys = [key for key in cell.keys() if key not in valid_keys]
        if extra_keys:    
            print(f'Cell {index} has the following keys which are invalid for a markdown cell: {extra_keys}')

# if no output, all good!
print('Done checking notebook.')