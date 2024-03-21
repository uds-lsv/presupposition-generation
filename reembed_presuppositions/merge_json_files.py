import json

def merge_json_files(file1_path, file2_path, output_file_path):
    # Load data from file1
    with open(file1_path, 'r') as file1:
        data1 = json.load(file1)

    # Load data from file2
    with open(file2_path, 'r') as file2:
        data2 = json.load(file2)

    # Merge the data and remove duplicates
    merged_data = data1 + [item for item in data2 if item not in data1]

    # Write the merged data to the output file
    with open(output_file_path, 'w') as output_file:
        json.dump(merged_data, output_file, indent=4)

# Example usage
file1_path = 'pspnli_1107.json'  # Replace with the path to your first input file
file2_path = 'pspnli_1307.json'  # Replace with the path to your second input file
output_file_path = 'pspnli_1307_merged.json'  # Replace with the desired path for the output file

merge_json_files(file1_path, file2_path, output_file_path)
