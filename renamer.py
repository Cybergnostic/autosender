import os

# Set up folder path
folder_path = 'C:\\Users\\PC\\Downloads\\osiguranja20042023'

# Get list of files in folder
files = os.listdir(folder_path)

# Loop over files and rename them with serial number
serial_number = 1
for file in files:
    # Get file extension
    ext = os.path.splitext(file)[1]

    # Construct new file name with serial number
    new_name = os.path.splitext(file)[0] + '_' + str(serial_number) + ext

    # Rename file
    os.rename(os.path.join(folder_path, file),
              os.path.join(folder_path, new_name))

    # Increment serial number
    serial_number += 1
