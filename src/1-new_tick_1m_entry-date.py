import os
import csv
import gzip
from datetime import datetime, timedelta
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
    last_price = None

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
                                    for row in rows:
                                        if len(row) > 9:
                                            try:
                                                actual_date_str = row[-2]
                                                time_str = row[1]
                                                actual_date_time = datetime.strptime(f"{actual_date_str} {time_str}", '%Y%m%d %H:%M:%S')
                                                if 16 <= actual_date_time.hour < 17:
                                                    continue
                                                actual_date_time = central.localize(actual_date_time).replace(second=0)
                                                actual_date_minute_str = actual_date_time.strftime('%Y%m%dT%H:%M')
                                                price = row[9]
                                                if actual_date_minute_str not in month_data:
                                                    month_data[actual_date_minute_str] = price
                                            except ValueError as e:
                                                print(f"Error parsing date/time in {file_path}: {e}")
                                except ValueError as e:
                                    print(f"Error reading {file_path}: {e}")

                    # Sort the data by time and fill in the gaps with the last known price
                    sorted_times = sorted(month_data.keys())
                    if sorted_times:
                        start_time = datetime.strptime(f"{year}{month}01T00:00", '%Y%m%dT%H:%M')
                        end_time = (start_time + timedelta(days=32)).replace(day=1)

                        current_time = start_time
                        output_data = []

                        while current_time < end_time:
                            current_time_str = current_time.strftime('%Y%m%dT%H:%M')
                            if current_time_str in month_data:
                                last_price = month_data[current_time_str]
                            if last_price is not None and not (16 <= current_time.hour < 17):
                                output_data.append([current_time_str + ':00', last_price])
                            current_time += timedelta(minutes=1)

                    output_file = os.path.join(output_dir, f"{year}{month}.csv")
                    with open(output_file, 'w', newline='') as out_file:
                        writer = csv.writer(out_file)
                        writer.writerow(['Entry Date CT', 'Price'])
                        for data in output_data:
                            writer.writerow(data)

                    print(f"Processed {year}-{month}")

# Base directory where the data files are located
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_dir = os.path.join(main_dir, 'data')

# Directory where the output CSV files will be saved
output_dir = os.path.join(main_dir, 'out')

process_files(base_dir, output_dir)
