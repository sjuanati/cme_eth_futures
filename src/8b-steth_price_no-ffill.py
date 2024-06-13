import os
import csv
from datetime import datetime

def read_csv_file(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            data.append(row)
    return data

def process_files(base_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in sorted(os.listdir(base_dir)):
        if filename.endswith('.csv'):
            file_path = os.path.join(base_dir, filename)
            data = read_csv_file(file_path)

            output_data = []

            for entry in data:
                time_str, price = entry
                actual_date_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f UTC')
                actual_date_minute_str = actual_date_time.strftime('%Y-%m-%dT%H:%M:%S.000 UTC')
                output_data.append([actual_date_minute_str, price])

            output_file = os.path.join(output_dir, filename)
            with open(output_file, 'w', newline='') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(['Entry Date UTC', 'Price'])
                writer.writerows(output_data)

            print(f"Processed {filename}")

# Main execution setup
if __name__ == '__main__':
    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.join(main_dir, 'data_steth')
    output_dir = os.path.join(main_dir, 'out')

    process_files(base_dir, output_dir)
