import csv
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Function to select files
def select_files():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames()
    return list(file_paths)

# Function to select a directory
def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    directory_path = filedialog.askdirectory()
    return directory_path

# Confirm overwrite dialog
def confirm_overwrite(file_path):
    return messagebox.askyesno("Confirm Overwrite", f"The file {file_path} already exists. Do you want to overwrite it?")

# Check if a line contains valid data (assuming numeric data)
def is_valid_data_line(line):
    try:
        # Check if at least the first cell can be converted to a float
        float(line[0])
        return True
    except ValueError:
        return False

# Get the list of selected files
selected_files = select_files()

# Get the output directory
output_directory = select_directory()

for file_path in selected_files:
    base_name = os.path.basename(file_path)
    output_file_path = os.path.join(output_directory, os.path.splitext(base_name)[0] + '.csv')

    # Check if file exists and ask for overwrite permission
    if os.path.exists(output_file_path) and not confirm_overwrite(output_file_path):
        print(f"Skipped {output_file_path} as it already exists.")
        continue

    # Read the input file
    with open(file_path, 'r') as input_file:
        lines = input_file.readlines()
        # Remove empty lines and process non-empty lines
        output_data = [line.split() for line in lines if line.strip() and is_valid_data_line(line.split())]

    # Add headers
    headers = ['E/V', 'I/uA']
    output_data.insert(0, headers)  # Prepend headers to the data

    # Write the processed data to the output CSV file
    with open(output_file_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerows(output_data)

    print(f"Processed {file_path} and saved as {output_file_path}")

print("CSV processing complete for all files.")
