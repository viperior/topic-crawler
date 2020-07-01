import glob
import os

outbound_link_files = glob.glob('data/outbound_links_*.json')
file_count = len(outbound_link_files)

for path in outbound_link_files:
    os.remove(path)
    
print(str(file_count) + ' files deleted.')
