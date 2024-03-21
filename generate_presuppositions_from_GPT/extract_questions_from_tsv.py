import csv

"""
This file preprocesses a .tsv file containing cross-examinations in the same format as 'cross_examinations.tsv'.
It removes any lines that do not contain questions (i.e. do not start with 'Q:'), and removes the question-tag 'Q:' from the start
of every question line.
"""

def preprocess(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        rows = list(reader)

    filtered_rows = []
    for row in rows:
        filtered_row = [value.replace('Q:', '') for value in row if value.startswith('Q')]
        if filtered_row:  # Only add non-empty rows
            filtered_rows.append(filtered_row)

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(filtered_rows)


