import os
import csv
from datetime import datetime, timedelta

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

    # Process each file in the base directory
    for filename in sorted(os.listdir(base_dir)):
        if filename.endswith('.csv'):
            file_path = os.path.join(base_dir, filename)
            data = read_csv_file(file_path)

            # Initialize data processing structures
            processed_data = {}
            last_price = None

            # Process the read data
            for entry in data:
                time_str, price = entry
                actual_date_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f %Z')
                actual_date_time = actual_date_time.replace(second=0, microsecond=0)
                actual_date_minute_str = actual_date_time.strftime('%Y-%m-%dT%H:%M')
                processed_data[actual_date_minute_str] = price
                last_price = price

            # Determine the time span of the data
            if data:
                first_entry_time = datetime.strptime(data[0][0], '%Y-%m-%d %H:%M:%S.%f %Z')
                first_entry_time = first_entry_time.replace(second=0, microsecond=0)
                last_entry_time = datetime.strptime(data[-1][0], '%Y-%m-%d %H:%M:%S.%f %Z')
                last_entry_time = last_entry_time.replace(second=0, microsecond=0)
                output_data = []
                current_time = first_entry_time

                while current_time <= last_entry_time:
                    current_time_str = current_time.strftime('%Y-%m-%dT%H:%M')
                    if current_time_str in processed_data:
                        last_price = processed_data[current_time_str]
                    if last_price is not None:
                        output_data.append([current_time_str + ':00', last_price])
                    current_time += timedelta(minutes=1)

            # Write to the output file
            output_file = os.path.join(output_dir, filename)
            with open(output_file, 'w', newline='') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(['Entry Date UTC', 'Price'])
                for data in output_data:
                    writer.writerow(data)

            print(f"Processed {filename}")

# Main execution setup
if __name__ == '__main__':
    # Base directory where the data files are located
    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.join(main_dir, 'data_steth')  # Adjust to your data folder

    # Directory where the output CSV files will be saved
    output_dir = os.path.join(main_dir, 'out')

    process_files(base_dir, output_dir)
