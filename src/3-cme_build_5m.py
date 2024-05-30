import os
import csv
from datetime import datetime

def read_csv_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return list(reader)

def write_csv_file(file_path, rows):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def process_files(data_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    
    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith('.csv'):
            input_file_path = os.path.join(data_dir, filename)
            output_file_path = os.path.join(output_dir, filename)  # Keep the same filename in the output directory
            
            rows = read_csv_file(input_file_path)
            headers = rows[0]
            data_rows = rows[1:]
            updated_rows = [headers]

            for row in data_rows:
                utc_date_str = row[1]  # Assuming 'Entry Date UTC' is the second column
                utc_date = datetime.strptime(utc_date_str, '%Y%m%dT%H:%M:%S')

                # Check if the minute is a multiple of 5
                if utc_date.minute % 5 == 0:
                    updated_rows.append(row)

            write_csv_file(output_file_path, updated_rows)
            print(f"Processed {filename} and created in {output_dir}")

# Base directory where the data files are located
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_dir = os.path.join(main_dir, 'data_cme')

# Directory where the output CSV files will be saved
output_dir = os.path.join(main_dir, 'out')

process_files(base_dir, output_dir)
