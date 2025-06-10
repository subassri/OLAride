import streamlit as st
import pandas as pd
import pyodbc
import os

class DatabaseConnector:
    def __init__(self, server, database):
        self.server = server
        self.database = database
        self.conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes"

    def execute_query(self, query):
        try:
            with pyodbc.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    columns = [column[0] for column in cursor.description]
                    df = pd.DataFrame.from_records(rows, columns=columns)
                    return df
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None

def main():
    db_connector = DatabaseConnector("NEWJAIS-RSFVIR2\\SQLEXPRESS", "ola")

    queries = {
        "Overall": {
            "Total Successful Bookings": "SELECT TOP 100 * FROM ola_data WHERE Booking_Status = 'Success'",
            "Total Booking Value": "SELECT TOP 100 * FROM ola_data WHERE Booking_Status = 'Success'"
        },
        "Vehicle Type": {
            "Average Ride Distance": "SELECT TOP 100 Vehicle_Type, AVG(Ride_Distance) AS Average_Ride_Distance FROM ola_data GROUP BY Vehicle_Type",
            "Average Customer Rating": "SELECT TOP 100 Vehicle_Type, AVG(Customer_Rating) AS Average_Customer_Rating FROM ola_data GROUP BY Vehicle_Type"
        },
        "Cancellation": {
            "Total Cancelled Rides": "SELECT Canceled_Rides_by_Customer, COUNT(*) AS Total_Cancelled_Rides FROM ola_data WHERE Canceled_Rides_by_Customer <> 'Unknown' GROUP BY Canceled_Rides_by_Customer",
            "Rides Cancelled by Drivers": "SELECT COUNT(*) AS Total_Cancelled_Rides FROM ola_data WHERE Canceled_Rides_by_Driver IS NOT NULL AND Canceled_Rides_by_Driver <> ''"
        },
        "Revenue": {
            "Total Booking Value": "SELECT SUM(Booking_Value) AS Total_Booking_Value FROM ola_data WHERE Booking_Status = 'Success'",
            "Rides by UPI": "SELECT TOP 100 * FROM ola_data WHERE Payment_Method = 'UPI'"
        },
        "Customer": {
            "Top 5 Customers": "SELECT TOP 5 Customer_ID, COUNT(*) AS Total_Rides FROM ola_data GROUP BY Customer_ID ORDER BY Total_Rides DESC"
        },
        "Ratings": {
            "Average Customer Rating": "SELECT TOP 100 Vehicle_Type, AVG(Customer_Rating) AS Average_Customer_Rating FROM ola_data GROUP BY Vehicle_Type",
            "Max and Min Driver Ratings for Prime Sedan": "SELECT MAX(Driver_Ratings) AS Max_Driver_Rating, MIN(Driver_Ratings) AS Min_Driver_Rating FROM ola_data WHERE Vehicle_Type = 'Prime Sedan'"
        }
    }

    vehicle_icons_map = {
        "Prime Sedan": "https://cdn-icons-png.flaticon.com/128/14183/14183770.png",
        "Bike": "https://cdn-icons-png.flaticon.com/128/9983/9983173.png",
        "Prime SUV": "https://cdn-icons-png.flaticon.com/128/9983/9983204.png",
        "eBike": "https://cdn-icons-png.flaticon.com/128/6839/6839867.png",
        "Mini": "https://cdn-icons-png.flaticon.com/128/3202/3202926.png",
        "Prime Plus": "https://cdn-icons-png.flaticon.com/128/11409/11409716.png",
        "Auto": "https://cdn-icons-png.flaticon.com/128/16526/16526595.png"
    }

    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background-color: #000000;
            }
            [data-testid="stSidebar"] label {
                color: #ffffff;
            }
            div.stSelectbox > div > div > div {
                background-color: #000000;
                color: #ffffff;
            }
            div.stSelectbox > div > div > div:hover {
                background-color: #32CD32 !important;
                color: #ffffff;
            }
            div.block-container {
                background-color: #f0f0f0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
     st.image("olaicon.png", width=200)
     st.markdown("<h2 style='font-family: Arial; color: #ffffff;'>OLA Dashboard</h2>", unsafe_allow_html=True)
     categories = list(queries.keys())
     selected_category = st.selectbox("Select Category", categories)

    if selected_category:
     st.subheader(f"Category: {selected_category}")
    for query_name, query in queries[selected_category].items():
        st.subheader(query_name)
        df = db_connector.execute_query(query)
        if df is not None and not df.empty:
            if selected_category in ["Vehicle Type", "Ratings"] and "Vehicle_Type" in df.columns:
                df['Vehicle_Type'] = df['Vehicle_Type'].apply(lambda x: f"<img src='{vehicle_icons_map.get(x, '')}' width='20'> {x}")
                st.write(df.to_html(escape=False), unsafe_allow_html=True)
            else:
                st.dataframe(df)
        else:
            st.write("No results found.")

if __name__ == "__main__":
    main()
