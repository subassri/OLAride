import pandas as pd
import os

# Define the file path
file_path = r'C:\Users\Administrator\Desktop\Miniproj\venv\pulse\ola\OLA_DataSet.xlsx'

# Load your data into a Pandas DataFrame
df = pd.read_excel(file_path)

# Print the original number of rows
print("Original number of rows:", len(df))

# Impute missing values in numerical columns with mean
numerical_columns = ['V_TAT', 'C_TAT', 'Driver_Ratings', 'Customer_Rating', 'Ride_Distance', 'Booking_Value']
for column in numerical_columns:
    df[column] = df[column].fillna(df[column].mean())

# Impute missing values in categorical columns with most frequent category
categorical_columns = ['Payment_Method', 'Incomplete_Rides_Reason']
for column in categorical_columns:
    df[column] = df[column].fillna(df[column].mode()[0])

# Handle specific columns differently
df['Canceled_Rides_by_Customer'] = df['Canceled_Rides_by_Customer'].fillna("Unknown")
df['Canceled_Rides_by_Driver'] = df['Canceled_Rides_by_Driver'].fillna("Unknown")
df['Incomplete_Rides'] = df['Incomplete_Rides'].fillna("Unknown")

# Get the directory path of the Excel file
dir_path = os.path.dirname(file_path)

# Save the cleaned data to a new CSV file in the same directory
df.to_csv(os.path.join(dir_path, 'OLA_Data_Cleaned.csv'), index=False)
print("Cleaned data saved to:", os.path.join(dir_path, 'OLA_Data_Cleaned.csv'))
