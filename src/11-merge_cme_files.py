''' merge all files in /out into a single file names merged.csv '''

import os
import csv

def merge_csv_files(output_dir, merged_file_name):
    merged_file_path = os.path.join(output_dir, merged_file_name)
    all_data = []

    # Iterate through all files in the output directory
    for filename in sorted(os.listdir(output_dir)):
        if filename.endswith('.csv') and filename != merged_file_name:
            file_path = os.path.join(output_dir, filename)
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header
                for row in reader:
                    all_data.append(row)

    # Write all data to the merged file
    with open(merged_file_path, 'w', newline='', encoding='utf-8') as merged_file:
        writer = csv.writer(merged_file)
        writer.writerow(['Entry Date UTC', 'Price'])  # Write header
        for data in all_data:
            writer.writerow(data)

    print(f"All files have been merged into {merged_file_name}")

# Main execution setup
if __name__ == '__main__':
    # Base directory where the data files are located
    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(main_dir, 'out')  # Adjust to your output folder

    # Call the function to merge CSV files
    merge_csv_files(output_dir, 'merged.csv')
