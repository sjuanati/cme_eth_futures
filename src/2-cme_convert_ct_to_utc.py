import os
import csv
from datetime import datetime, timedelta
import pytz

def read_csv_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
    return rows

def write_csv_file(file_path, rows):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def process_files(output_dir):
    central = pytz.timezone('US/Central')
    utc = pytz.utc

    for filename in sorted(os.listdir(output_dir)):
        if filename.endswith('.csv'):
            file_path = os.path.join(output_dir, filename)
            rows = read_csv_file(file_path)
            
            # Add Entry Date UTC header
            headers = rows[0]
            headers.insert(1, 'Entry Date UTC')
            data_rows = rows[1:]

            updated_rows = [headers]

            for row in data_rows:
                entry_date_ct_str = row[0]
                entry_date_ct = datetime.strptime(entry_date_ct_str, '%Y%m%dT%H:%M:%S')
                # entry_date_ct = central.localize(entry_date_ct)
                entry_date_ct = central.localize(entry_date_ct, is_dst=False)
                # entry_date_ct = central.localize(entry_date_ct, is_dst=False) - timedelta(hours=1)
                entry_date_utc = entry_date_ct.astimezone(utc)
                entry_date_utc_str = entry_date_utc.strftime('%Y%m%dT%H:%M:%S')

                # Insert the Entry Date UTC in the correct position
                row.insert(1, entry_date_utc_str)
                updated_rows.append(row)

            write_csv_file(file_path, updated_rows)
            print(f"Processed {filename}")

# Base directory where the output CSV files are located
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_dir = os.path.join(main_dir, 'out')

process_files(output_dir)
