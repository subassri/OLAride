import pandas as pd
import pyodbc
from sqlalchemy import create_engine

# Load the cleaned data
df = pd.read_csv(r'C:\Users\Administrator\Desktop\Miniproj\venv\pulse\ola\OLA_Data_Cleaned.csv')

# Ensure the data types of the columns match the table structure
df['Canceled_Rides_by_Customer'] = pd.to_numeric(df['Canceled_Rides_by_Customer'], errors='coerce').fillna(0).astype(int)
df['Canceled_Rides_by_Driver'] = pd.to_numeric(df['Canceled_Rides_by_Driver'], errors='coerce').fillna(0).astype(int)
df['Incomplete_Rides'] = pd.to_numeric(df['Incomplete_Rides'], errors='coerce').fillna(0).astype(int)

# Define the connection string
server = r"NEWJAIS-RSFVIR2\SQLEXPRESS"
database = "ola"
conn_str = f"mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

# Create a SQLAlchemy engine
engine = create_engine(conn_str)

# Insert the data into the table
df.to_sql('ola_data', engine, if_exists='append', index=False)
