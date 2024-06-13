import csv
import os
from datetime import datetime

def read_and_process_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            data = []
            for row in reader:
                try:
                    # Parse date (no offset added)
                    date_utc = datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%SZ')
                    formatted_date = date_utc.strftime('%Y-%m-%d %H:%M:%S.000 UTC')
                    
                    # Extract the 'open' price from the second column
                    price = row[1]  # Changed from row[4] to row[1]
                    
                    # Append the formatted date and price to the data list
                    data.append((formatted_date, price))
                except ValueError as e:
                    print(f"Error processing row {row}: {e}")
        
        # Write processed data to the output file
        with open(output_file, 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(['Entry Date UTC', 'Price'])  # Write header
            writer.writerows(data)  # Write all processed data
        print(f"Processed file saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Define the base directory and input/output paths
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_dir = os.path.join(main_dir, 'data_steth')
output_dir = os.path.join(main_dir, 'out')
os.makedirs(output_dir, exist_ok=True)

input_file_path = os.path.join(input_dir, 'BYBIT_STETHUSDT, 5.csv')
output_file_path = os.path.join(output_dir, 'processed_data.csv')

# Process the file
read_and_process_file(input_file_path, output_file_path)
