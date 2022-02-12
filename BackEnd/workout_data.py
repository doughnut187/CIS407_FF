"""
Filename: workout_data.py

Purpose: Loads the workout data into the database from a csv file

Authors: Jordan Smith
Group: Wholesome as Heck Programmers (WaHP)
Last modified: 11/13/21
"""
from db_manager import db_mgr
import csv

# Boolean to delete data from the workouts table
# Useful for debugging and initially setting up
DELETE_DATA = True

# The workout table's column names
data_keys = ['type', 'name', 'equipment', 'difficulty', 'is_priority']

data_to_insert = []

# Load the csv file and convert it into a list of dictionaries so it 
#   can be inserted into the database
with open("workout_data.csv", newline="") as csv_data:
    # Initialize the spamreader to read from the csv file
    spamreader = csv.reader(csv_data, delimiter=',', quotechar='|')
    
    for row in spamreader:
        new_row = {}
        count = 0

        # Make a dictionary for the current row (column name, value)
        for key in data_keys:
            value_data = row[count + 1]

            # Weird case for commas in csv column, need to grab two values
            if '"' in value_data:
                value_data += ',' + row[count + 2]
                value_data = value_data.strip('"')
                count += 1

            if value_data == "TRUE":
                value_data = True
            elif value_data == "FALSE":
                value_data = False

            new_row[key] = value_data

            count += 1

        # Add the dictionary row to the list
        data_to_insert.append(new_row)

        print(f"Converted data from row {len(data_to_insert)}")

# For debugging, deletes all rows from the workouts table
if DELETE_DATA:
    db_mgr.delete_rows('workouts')

# Insert the data into the workouts table 
res = db_mgr.add_many_rows('workouts', data_to_insert)
if res:
    print("Inserted data into database successfully!")