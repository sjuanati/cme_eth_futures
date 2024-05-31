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

    # Process each file in the base directory
    for filename in sorted(os.listdir(base_dir)):
        if filename.startswith('steth_1m_') and filename.endswith('.csv'):
            file_path = os.path.join(base_dir, filename)
            data = read_csv_file(file_path)

            # Initialize data processing structures
            filtered_data = []

            # Filter data to every hour
            for entry in data:
                time_str, price = entry
                actual_date_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
                # Check if the minute is 00 (hourly data)
                if actual_date_time.minute == 0:
                    filtered_data.append(entry)

            # Prepare the new file name
            new_filename = filename.replace('1m', '1h')

            # Write to the output file
            output_file = os.path.join(output_dir, new_filename)
            with open(output_file, 'w', newline='') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(['Entry Date UTC', 'Price'])
                for data in filtered_data:
                    writer.writerow(data)

            print(f"Processed {filename}")

# Main execution setup
if __name__ == '__main__':
    # Base directory where the data files are located
    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.join(main_dir, 'data_steth')  # Adjust to your data folder

    # Directory where the output CSV files will be saved
    output_dir = os.path.join(main_dir, 'out')  # Adjust to your output folder

    process_files(base_dir, output_dir)
