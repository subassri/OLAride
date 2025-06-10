OLA Dashboard

Overview
This project is a Streamlit-based dashboard for visualizing OLA ride data. It connects to a SQL Server database and executes various queries to display insights on ride data, vehicle types, cancellations, revenue, customer behavior, and ratings.

Features
- Interactive sidebar with category selection
- Displays various metrics and insights for each category
- Uses icons for vehicle types
- Customizable styling using Streamlit's markdown feature

Requirements
- Python 3.x
- Streamlit
- pandas
- pyodbc
- SQL Server database with OLA ride data

Installation
1. Clone the repository: git clone https://github.com/subassri/OLAride.git
2. Install required packages: pip install streamlit pandas pyodbc
3. Update the database connection string in the DatabaseConnector class in olaapps.py

Usage
1. Run the application: streamlit run olaapps.py
2. Open a web browser and navigate to http://localhost:8501
3. Select a category from the sidebar to view insights

Database Schema
The project assumes a SQL Server database with a table named ola_data containing columns such as:

- Booking_Status
- Vehicle_Type
- Ride_Distance
- Customer_Rating
- Payment_Method
- Booking_Value
