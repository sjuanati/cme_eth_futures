# import csv
# import os
# from datetime import datetime, timedelta

# def read_and_process_file(input_file, output_file):
#     encodings = ['utf-8', 'latin-1', 'cp1252']  # List of encodings to try
#     data_processed = False

#     for encoding in encodings:
#         try:
#             with open(input_file, 'r', encoding=encoding) as file:
#                 reader = csv.reader(file)
#                 next(reader)  # Skip header if present
#                 data = []
#                 for index, row in enumerate(reader, start=1):  # Start indexing from 1 for better readability in errors
#                     if len(row) >= 5:  # Ensure there are enough columns to process
#                         try:
#                             # Attempt to parse date and adjust it according to the requirement
#                             date_utc = datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%SZ')
#                             date_utc_plus_one_hour = date_utc + timedelta(hours=1)
#                             formatted_date = date_utc_plus_one_hour.strftime('%Y-%m-%d %H:%M:%S.000 UTC')
#                             price = row[4]
#                             data.append((formatted_date, price))
#                         except ValueError as e:
#                             print(f"Skipping row {index} due to error: {e}. Data: {row}")
#                             continue
#                     else:
#                         print(f"Row {index} skipped because it doesn't have enough columns. Data: {row}")
#                 if data:
#                     with open(output_file, 'w', newline='') as file:
#                         writer = csv.writer(file)
#                         writer.writerow(['Entry Date UTC', 'Price'])
#                         writer.writerows(data)
#                     data_processed = True
#                     print(f"Processed file saved to {output_file_path}")
#                     break
#         except UnicodeDecodeError:
#             print(f"Failed with encoding {encoding}, trying next...")
#             continue
#         except Exception as e:
#             print(f"Unhandled exception for encoding {encoding}: {e}")
#             break

#     if not data_processed:
#         print("Failed to process any data. Check file content and format.")

# # Base directory where the data files are located
# main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# input_dir = os.path.join(main_dir, 'data_eth')

# # Directory where the output CSV files will be saved
# output_dir = os.path.join(main_dir, 'out')

# # Ensure the output directory exists
# os.makedirs(output_dir, exist_ok=True)

# # Find the first file in the input directory
# file_name = None
# for root, dirs, files in os.walk(input_dir):
#     if files:
#         file_name = files[0]
#         break

# if file_name:
#     input_file_path = os.path.join(root, file_name)
#     output_file_path = os.path.join(output_dir, 'processed_data.csv')

#     # Process the file
#     read_and_process_file(input_file_path, output_file_path)
# else:
#     print("No files found in the specified directory.")

import csv
import os
from datetime import datetime, timedelta

def read_and_process_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            data = []
            for row in reader:
                try:
                    # Parse date and add one hour to the UTC time
                    date_utc = datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%SZ')
                    date_utc_plus_one_hour = date_utc + timedelta(hours=1) # if hourly sourcing, get open of next instead of close of current
                    formatted_date = date_utc_plus_one_hour.strftime('%Y-%m-%d %H:%M:%S.000 UTC')
                    
                    # Extract the 'close' price
                    price = row[4]
                    
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
input_dir = os.path.join(main_dir, 'data_eth')
output_dir = os.path.join(main_dir, 'out')
os.makedirs(output_dir, exist_ok=True)

input_file_path = os.path.join(input_dir, 'steth_1h_tv.csv')
output_file_path = os.path.join(output_dir, 'processed_data.csv')

# Process the file
read_and_process_file(input_file_path, output_file_path)
