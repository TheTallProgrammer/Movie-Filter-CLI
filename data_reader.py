import csv

def read_csv(input_file):
    # csv dictReader auto interprets the first row as the header columns (keys) for the csv. 
    # The rows beneath are data rows (the values) for the header keys based on its position
    # use reference to open file to parse csv efficiently by changing the args namespace object to a dictionary
    reader = csv.DictReader(input_file)
    return reader