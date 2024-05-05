import datetime
import os
import csv
import sys

def log(*args,file_path=None,suf=''):
    """
    Logs the provided arguments into a CSV file along with a current timestamp.

    Parameters:
    - file_path: str, the path to the CSV file where data should be logged. Defaults to 'log.csv' in the current directory.
    - *args: variable length argument list, the data to log in the CSV.
    """

    # Get the current timestamp
    now = datetime.datetime.utcnow()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    if file_path is None:
        script_name = os.path.basename(sys.argv[0])
        if script_name.endswith('.py'):
            script_name = script_name[:-3]  # Remove .py extension
        file_path = f"/logs/{script_name}_{suf}_log.csv"

    # Open the CSV file and append the new row
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Add the timestamp as the first item in the row, followed by the provided arguments
        writer.writerow([timestamp] + list(args))

    print([timestamp] + list(args))
    
