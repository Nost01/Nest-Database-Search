import pandas as pd
import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from .env file
load_dotenv("variables.env")

# Load the Excel file
df = pd.read_excel(r"C:\Users\nost_\OneDrive\Desktop\General Work\StaffParkingManagement.xlsx")

# df['StallNumber'] Selects the column 'StallNumber'.
# .astype(str) Converts all values in the column to string type.
# .str.strip() Removes any leading or trailing whitespace from the string values.
df['StallNumber'] = df['StallNumber'].astype(str).str.strip()

# .replace({...}) Replaces specific values in the 'StallNumber' column.
# {'nan': None, 'NaN': None} Specifies that any occurrence of the string 'nan' or 'NaN' should be replaced with None (which represents a null value in Python).
df['StallNumber'] = df['StallNumber'].replace({'nan': None, 'NaN': None})

# Columns needed
columns_needed = [
    'StaffID',
    'FirstName',
    'LastName',
    'Department',
    'VehiclePlate',
    'VehicleDescription',
    'VehicleColour',
    'VehicleMake',
    'VehicleModel',
    'StallNumber',
    'NumberOfVehicles'
]

# df.columns Lists of all column names.
# .str.strip() Removes any whitespace at the start or end of column names.
df.columns = df.columns.str.strip()

# Selects only the columns that are needed.
df = df[columns_needed]

# pd.notnull(df) Checks each cell to see if it's not NULL.
# df.where(pd.notnull(df), None) Replaces NULL values with None.
df = df.where(pd.notnull(df), None)

# Connect to the Employees database
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Curser object
cursor = conn.cursor()

# Insert data into the Employees table row by row
for _, row in df.iterrows():
    cursor.execute("""
            INSERT INTO Employees (StaffID, FirstName, LastName, Department, VehiclePlate, VehicleDescription, VehicleColour, VehicleMake, VehicleModel, StallNumber, NumberOfVehicles)  
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  
        """, tuple(row))      
                    
# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

# Print a success message
print("Data imported successfully into the Employees table!")