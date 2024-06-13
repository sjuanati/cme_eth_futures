import os
import csv
import gzip
from datetime import datetime
import pytz

def read_csv_file(file_path):
    encodings = ['utf-8', 'latin-1']
    for encoding in encodings:
        try:
            if file_path.endswith('.gz'):
                with gzip.open(file_path, 'rt', encoding=encoding) as file:
                    reader = csv.reader(file)
                    return list(reader)
            else:
                with open(file_path, 'r', encoding=encoding) as file:
                    reader = csv.reader(file)
                    return list(reader)
        except (UnicodeDecodeError, csv.Error):
            continue
    raise ValueError(f"Failed to decode file {file_path} with available encodings.")

def process_files(base_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    central = pytz.timezone('US/Central')

    for year in sorted(os.listdir(base_dir)):
        year_dir = os.path.join(base_dir, year)
        if os.path.isdir(year_dir):
            for month in sorted(os.listdir(year_dir)):
                month_dir = os.path.join(year_dir, month)
                if os.path.isdir(month_dir):
                    month_data = {}
                    for day in sorted(os.listdir(month_dir)):
                        day_dir = os.path.join(month_dir, day, 'TICK', 'XCME')
                        if os.path.isdir(day_dir):
                            for filename in sorted(os.listdir(day_dir)):
                                file_path = os.path.join(day_dir, filename)
                                try:
                                    rows = read_csv_file(file_path)
                                    # Initialize the contract_month filter with the first row's value
                                    contract_month_filter = None
                                    for row in rows:
                                        if len(row) > 9:
                                            if contract_month_filter is None:
                                                contract_month_filter = row[6]  # Set the filter from the first valid row
                                            if row[6] != contract_month_filter:
                                                continue  # Skip rows that do not match the filter
                                            try:
                                                actual_date_str = row[-2]
                                                time_str = row[1]
                                                actual_date_time = datetime.strptime(f"{actual_date_str} {time_str}", '%Y%m%d %H:%M:%S')
                                                # actual_date_time = central.localize(actual_date_time).replace(second=0)
                                                actual_date_time = central.localize(actual_date_time, is_dst=False).replace(second=0)
                                                actual_date_minute_str = actual_date_time.strftime('%Y%m%dT%H:%M')
                                                price = row[9]
                                                month_data[actual_date_minute_str] = price  # Always store the latest price per minute
                                            except ValueError as e:
                                                print(f"Error parsing date/time in {file_path}: {e}")
                                except ValueError as e:
                                    print(f"Error reading {file_path}: {e}")

                    # Write the data to CSV
                    output_file = os.path.join(output_dir, f"{year}{month}.csv")
                    with open(output_file, 'w', newline='') as out_file:
                        writer = csv.writer(out_file)
                        writer.writerow(['Entry Date CT', 'Price'])
                        for time_stamp, price in sorted(month_data.items()):
                            writer.writerow([time_stamp + ':00', price])

                    print(f"Processed {year}-{month}")

# Base directory where the data files are located
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_dir = os.path.join(main_dir, 'data_cme')

# Directory where the output CSV files will be saved
output_dir = os.path.join(main_dir, 'out')

process_files(base_dir, output_dir)
