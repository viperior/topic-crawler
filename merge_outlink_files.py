import csv
import glob
import json

output_directory = 'data/'
outlink_files = glob.glob(output_directory + 'outlinks_*.json')
output_file_semantic_name = 'merged_topic_links'
output_json_file_path = output_directory + output_file_semantic_name + '.json'
output_csv_file_path = output_directory + output_file_semantic_name + '.csv'

merged_json_data = {}

for index, path in enumerate(outlink_files):
    with open(path, 'r') as input_file:
        json_data = json.load(input_file)
        
    if index == 0:
        merged_json_data = json_data
    else:
        merged_json_data = {**merged_json_data, **json_data}
        
# Save as merged JSON file.
with open(output_json_file_path, 'w') as output_json_file:
    json.dump(merged_json_data, output_json_file)
    
# Save as flattened CSV file.
csv_row_data = []
link_dict_keys = merged_json_data.keys()

for key in link_dict_keys:
    csv_row_data.append(merged_json_data[key])

fieldnames = csv_row_data[0].keys()

with open(output_csv_file_path, 'w') as output_csv_file:
    csv_writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    
    for row in csv_row_data:
        csv_writer.writerow(row)
    
print(
    str(len(outlink_files)) + ' files containing ' + str(len(merged_json_data))\
        + ' links merged.'
)
