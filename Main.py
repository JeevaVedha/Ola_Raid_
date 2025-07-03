import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# DB Connection
engine = create_engine('postgresql+psycopg2://postgres:password123@localhost:5432/Ola_Raiders')

# Function to get query based on selection
def get_query(option: int) -> str:
    match option:
        case 1:
            return 'SELECT * FROM july WHERE "Booking_Status" = \'Success\';'
        case 2: 
            return '''
                SELECT "Vehicle_Type", AVG("Ride_Distance") AS "Avg_Ride_Distance"
                FROM july
                GROUP BY "Vehicle_Type";
            '''
        case 3:
            return '''
                SELECT "Customer_ID", COUNT(*) AS "Total_Cancellations"
                FROM july
                WHERE "Booking_Status" = 'Canceled by Customer'
                GROUP BY "Customer_ID"
                ORDER BY "Total_Cancellations" DESC;
            '''
        case 4:
            return '''
                SELECT "Customer_ID", COUNT(*) AS "Total_Rides"
                FROM july
                WHERE "Booking_Status" = 'Success'
                GROUP BY "Customer_ID"
                ORDER BY "Total_Rides" DESC
                LIMIT 5;
            '''
        case 5:
            return '''
                SELECT "Customer_ID", COUNT(*) AS "Total_Cancellations"
                FROM july
                WHERE "Booking_Status" = 'Canceled by Driver'
                GROUP BY "Customer_ID"
                ORDER BY "Total_Cancellations" DESC;
            '''
        case 6:
            return '''
                SELECT 
                    "Customer_ID", 
                    MAX("Driver_Ratings") AS "Max_Driver_Rating", 
                    MIN("Driver_Ratings") AS "Min_Driver_Rating"
                FROM july
                WHERE "Vehicle_Type" = 'Prime Sedan'
                GROUP BY "Customer_ID";
            '''
        case 7:
            return '''
                SELECT * 
                FROM july 
                WHERE "Payment_Method" = 'UPI' AND "Booking_Status" = 'Success';
            '''
        case 8:
            return '''
              SELECT 
                    "Vehicle_Type", 
                    AVG("Customer_Rating") AS "Avg_Customer_Rating"
                FROM july
                WHERE "Booking_Status" = 'Success'
                GROUP BY "Vehicle_Type";
            '''
        case 9:
            return '''
                SELECT 
                    SUM("Booking_Value") AS "Total_Booking_Value"
                FROM july
                WHERE "Booking_Status" = 'Success';
            '''
        case 10:
            return '''
                SELECT "Customer_ID", COUNT(*) AS "Incomplete_Rides"
                FROM july
                WHERE "Booking_Status" = 'Success'
                GROUP BY "Customer_ID";
            '''
        case _:
            return ""

# App UI
st.set_page_config("Ola SQL Dashboard", layout="wide")
st.title("📊 Ola Riders SQL Dashboard (Enhanced Edition)")

option = st.selectbox(
    "Choose query to run:",
    list(range(1, 11)),
    format_func=lambda x: {
        1: "1. All successful bookings",
        2: "2. Avg ride distance by vehicle type",
        3: "3. Total cancellations by customers",
        4: "4. Top 5 customers by rides",
        5: "5. Driver cancellations",
        6: "6. Max/min driver ratings (Prime Sedan)",
        7: "7. Rides paid via UPI",
        8: "8. Avg customer rating by vehicle type",
        9: "9. Total booking value (successful)",
        10: "10. Incomplete rides count"
    }.get(x, "")
)

sql = get_query(option)
if not sql:
    st.error("Invalid selection!")
else:
    df = pd.read_sql(sql, engine)
    st.success("Query executed successfully!")

    if option == 1:
        st.subheader("📅 Daily Booking Trend")
        col1, col2 = st.columns(2)
        col1.metric("Total Bookings", df.shape[0])
        col2.metric("Unique Customers", df['Customer_ID'].nunique())
        
        df['Date'] = pd.to_datetime(df['Date'])
        daily_counts = df.groupby('Date')['Booking_ID'].count()
        st.area_chart(daily_counts)

    elif option == 2:
        st.subheader("🚗 Avg Ride Distance by Vehicle Type")
        fig = px.bar(df, x='Vehicle_Type', y='Avg_Ride_Distance', color='Vehicle_Type',
                     title="Average Ride Distance", labels={'Avg_Ride_Distance': 'Avg Distance (km)'})
        st.plotly_chart(fig, use_container_width=True)

    elif option == 3:
        st.subheader("❌ Cancellations by Customers")
        st.metric("Total Cancellations", df['Total_Cancellations'].sum())
        fig = px.bar(df.head(20), x='Customer_ID', y='Total_Cancellations', title="Top 20 Cancelers")
        st.plotly_chart(fig)

    elif option == 4:
        st.subheader("🏅 Top 5 Customers by Ride Count")
        st.metric("Total Rides (Top 5)", df['Total_Rides'].sum())
        fig = px.bar(df, x='Customer_ID', y='Total_Rides', color='Total_Rides', title="Top 5 Riders")
        st.plotly_chart(fig)

    elif option == 5:
        st.subheader("🚫 Driver Cancellations")
        st.metric("Driver Cancellations", df['Total_Cancellations'].sum())
        fig = px.treemap(df, path=['Customer_ID'], values='Total_Cancellations',
                         title="Cancellations by Drivers per Customer")
        st.plotly_chart(fig)

    elif option == 6:
        st.subheader("⭐ Driver Ratings for Prime Sedan")
        df['Max_Driver_Rating'] = df['Max_Driver_Rating'].round(2)
        df['Min_Driver_Rating'] = df['Min_Driver_Rating'].round(2)

        st.metric("Max Rating", df['Max_Driver_Rating'].max())
        st.metric("Min Rating", df['Min_Driver_Rating'].min())

        fig = px.scatter(df, x='Customer_ID', y='Max_Driver_Rating', color='Max_Driver_Rating',
                         title="Max Ratings per Customer (Prime Sedan)")
        st.plotly_chart(fig)

    elif option == 7:
        st.subheader("💸 UPI-Based Successful Rides")
        st.metric("Total Rides via UPI", df.shape[0])
        fig = px.sunburst(df, path=['Vehicle_Type', 'Pickup_Location'], values='Booking_Value',
                          title="UPI Bookings by Vehicle & Location")
        st.plotly_chart(fig)

    elif option == 8:
        st.subheader("⭐ Avg Customer Ratings by Vehicle Type")
        df['Avg_Customer_Rating'] = df['Avg_Customer_Rating'].round(2)
        st.metric("Overall Avg Rating", df['Avg_Customer_Rating'].mean().round(2))

        fig = go.Figure(data=go.Scatterpolar(
            r=df['Avg_Customer_Rating'],
            theta=df['Vehicle_Type'],
            fill='toself',
            name='Avg Rating'
        ))
        fig.update_layout(title="Radar Chart: Avg Ratings by Vehicle Type", polar=dict(radialaxis=dict(visible=True)))
        st.plotly_chart(fig)

    elif option == 9:
        st.subheader("💰 Total Booking Value (Success Only)")
        total_value = df['Total_Booking_Value'].iloc[0]
        st.metric("Total Booking Value", f"₹{total_value:,.2f}")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total_value,
            title={'text': "Booking Value Gauge"},
            gauge={'axis': {'range': [None, total_value * 1.5]}}
        ))
        st.plotly_chart(fig)

    elif option == 10:
        st.subheader("🔁 Incomplete Ride Count")
        st.metric("Total Incomplete Rides", df['Incomplete_Rides'].sum())
        fig = px.bar(df.head(20), x='Customer_ID', y='Incomplete_Rides', title="Top 20 Customers with Incomplete Rides")
        st.plotly_chart(fig)
