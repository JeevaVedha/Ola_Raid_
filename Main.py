import streamlit as st
import os
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import base64
import requests 

st.set_page_config(page_title="Ola Riders Dashboard", layout="wide")

# ✅ Function to convert image URL to base64
def get_image_base64_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode("utf-8")
    else:
        st.error(f"Failed to fetch image. Status code: {response.status_code}")
        return ""

# ✅ Load Ola logo (SVG)
logo_url = "https://upload.wikimedia.org/wikipedia/en/0/0f/Ola_Cabs_logo.svg"
logo_base64 = get_image_base64_from_url(logo_url)

# ✅ Background image (example, replace with your preferred one)
background_url = "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf"  # Change this to your own
bg_base64 = get_image_base64_from_url(background_url)

# ✅ HTML + CSS
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(90deg, rgba(222, 232, 35, 1) 0%, rgba(31, 29, 11, 1) 100%);;
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    }}

    .header {{
        display: flex;
        align-items: center;
        background-color: transparent; /* Purple semi-transparent */
        padding: 10px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}

    .header img {{
        height: 60px;
        margin-right: 20px;
    }}

    .menu {{
        display: flex;
        gap: 20px;
    }}

    .menu a {{
        font-weight: bold;
        color: white;
        text-decoration: none;
        font-size: 16px;
        padding-bottom: 2px;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }}

    .menu a:hover {{
        color: #e0d3f5;
        border-bottom: 2px solid white;
    }}
    </style>

    <div class="header">
        <img src="data:image/svg+xml;base64,{logo_base64}" alt="Ola Logo">
            <div class="menu">
            <h1>Ola Riders SQL Dashboard</h1>
        </div>
    </div>
""", unsafe_allow_html=True)
# Database Connection
engine = create_engine('postgresql+psycopg2://postgres:password123@localhost:5432/Ola_Raiders')

 
# Set Streamlit page config
#st.title("🚖 Ola Riders SQL Dashboard – Single Page View")
 
# --------- Query 1: All successful bookings --------- #
col1, col2 = st.columns([1, 1])
with col1:
    with st.expander("1️⃣ All Successful Bookings", expanded=False):
        
        df1 = pd.read_sql('SELECT * FROM july WHERE "Booking_Status" = \'Success\';', engine)
        a, b = st.columns(2)
        with a:
            st.metric("✅ Total Successful Bookings", df1.shape[0])
        with b:
            st.metric("👤 Unique Customers", df1['Customer_ID'].nunique())

        df1['Date'] = pd.to_datetime(df1['Date'])
        daily_counts = df1.groupby('Date')['Booking_ID'].count().reset_index()

        fig = px.area(
            daily_counts,
            x='Date',
            y='Booking_ID',
            title='Daily Successful Bookings',
            template='plotly_white'  # Use 'plotly_dark' for dark background
        )

        # Customize background
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',  # Outside plot area
            plot_bgcolor='rgba(0,0,0,0)',   # Inside plot area
            font=dict(color='white')        # Optional: for dark background
        )

        st.plotly_chart(fig, use_container_width=True)

    # --------- Query 2: Avg ride distance by vehicle type --------- #
    with st.expander("2️⃣ Avg Ride Distance by Vehicle Type", expanded=False):
        df2 = pd.read_sql('''
            SELECT "Vehicle_Type", AVG("Ride_Distance") AS "Avg_Ride_Distance"
            FROM july
            GROUP BY "Vehicle_Type";
        ''', engine)
        fig = px.bar(df2, x='Vehicle_Type', y='Avg_Ride_Distance', color='Vehicle_Type',
                     title="Avg Ride Distance (km)")
        st.plotly_chart(fig, use_container_width=True)

    # --------- Query 3: Cancellations by customers --------- #
    with st.expander("3️⃣ Cancellations by Customers", expanded=False):
        df3 = pd.read_sql('''
            SELECT "Customer_ID", COUNT(*) AS "Total_Cancellations"
            FROM july
            WHERE "Booking_Status" = 'Canceled by Customer'
            GROUP BY "Customer_ID"
            ORDER BY "Total_Cancellations" DESC;
        ''', engine)
        st.metric("Total Cancellations", df3['Total_Cancellations'].sum())
        st.dataframe(df3.head(10), use_container_width=True)

    # --------- Query 4: Top 5 customers by rides --------- #
    with st.expander("4️⃣ Top 5 Customers by Rides", expanded=False):
        df4 = pd.read_sql('''
            SELECT "Customer_ID", COUNT(*) AS "Total_Rides"
            FROM july
            WHERE "Booking_Status" = 'Success'
            GROUP BY "Customer_ID"
            ORDER BY "Total_Rides" DESC
            LIMIT 5;
        ''', engine)
        st.metric("Rides (Top 5 Customers)", df4['Total_Rides'].sum())
        st.bar_chart(df4.set_index('Customer_ID'))

    # --------- Query 5: Cancellations by drivers --------- #
    with st.expander("5️⃣ Driver Cancellations", expanded=False):
        df5 = pd.read_sql('''
            SELECT "Customer_ID", COUNT(*) AS "Total_Cancellations"
            FROM july
            WHERE "Booking_Status" = 'Canceled by Driver'
            GROUP BY "Customer_ID"
            ORDER BY "Total_Cancellations" DESC;
        ''', engine)
        st.metric("Total Driver Cancellations", df5['Total_Cancellations'].sum())
        st.dataframe(df5.head(10), use_container_width=True)

    # --------- Query 6: Max/min driver rating (Prime Sedan) --------- #
    with st.expander("6️⃣ Driver Ratings (Prime Sedan)", expanded=False):
        df6 = pd.read_sql('''
            SELECT 
                "Customer_ID", 
                MAX("Driver_Ratings") AS "Max_Driver_Rating", 
                MIN("Driver_Ratings") AS "Min_Driver_Rating"
            FROM july
            WHERE "Vehicle_Type" = 'Prime Sedan'
            GROUP BY "Customer_ID";
        ''', engine)
        st.metric("Max Rating", df6['Max_Driver_Rating'].max())
        st.metric("Min Rating", df6['Min_Driver_Rating'].min())
        st.dataframe(df6.head(10))

    # --------- Query 7: UPI Payments --------- #
    with st.expander("7️⃣ UPI-Based Successful Bookings", expanded=False):
        df7 = pd.read_sql('''
            SELECT * 
            FROM july 
            WHERE "Payment_Method" = 'UPI' AND "Booking_Status" = 'Success';
        ''', engine)
        st.metric("Total UPI Rides", df7.shape[0])
        fig = px.pie(df7, values='Booking_Value', names='Vehicle_Type',
                     title='Booking Value by Vehicle Type (UPI)', hole=0.5)
        st.plotly_chart(fig, use_container_width=True)

    # --------- Query 8: Avg customer rating by vehicle type --------- #
    with st.expander("8️⃣ Avg Customer Ratings by Vehicle Type", expanded=False):
        df8 = pd.read_sql('''
            SELECT 
                "Vehicle_Type", 
                AVG("Customer_Rating") AS "Avg_Customer_Rating"
            FROM july
            WHERE "Booking_Status" = 'Success'
            GROUP BY "Vehicle_Type";
        ''', engine)
        df8['Avg_Customer_Rating'] = df8['Avg_Customer_Rating'].round(2)
        st.metric("Avg Rating", df8['Avg_Customer_Rating'].mean().round(2))
        st.bar_chart(df8.set_index('Vehicle_Type'))

    # --------- Query 9: Total booking value --------- #
    with st.expander("9️⃣ Total Booking Value (Success Only)", expanded=False):
        df9 = pd.read_sql('''
            SELECT SUM("Booking_Value") AS "Total_Booking_Value"
            FROM july
            WHERE "Booking_Status" = 'Success';
        ''', engine)
        total_val = df9['Total_Booking_Value'].iloc[0]
        st.metric("Total Booking Value", f"₹{total_val:,.2f}")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total_val,
            title={'text': "Booking Value Gauge"},
            gauge={'axis': {'range': [None, total_val * 1.2]}}
        ))
        st.plotly_chart(fig)

    # --------- Query 10: Incomplete rides --------- #
    with st.expander("🔟 Incomplete Rides per Customer", expanded=False):
        df10 = pd.read_sql('''
            SELECT "Customer_ID", COUNT(*) AS "Incomplete_Rides"
            FROM july
            WHERE "Booking_Status" = 'Success'
            GROUP BY "Customer_ID";
        ''', engine)

        st.metric("Total Incomplete Rides", df10['Incomplete_Rides'].sum())

        # Top 15 customers with most incomplete rides
        top_incomplete = df10.sort_values(by='Incomplete_Rides', ascending=False).head(15)

        fig_bar = px.bar(
            top_incomplete,
            x='Incomplete_Rides',
            y='Customer_ID',
            orientation='h',
            title='Top 15 Customers by Incomplete Rides',
            labels={'Incomplete_Rides': 'Incomplete Rides', 'Customer_ID': 'Customer ID'},
            color='Incomplete_Rides',
            color_continuous_scale='Reds'
        )

        fig_bar.update_layout(yaxis=dict(autorange="reversed"))  # Ensure highest at top

        st.plotly_chart(fig_bar, use_container_width=True)

        #st.dataframe(top_incomplete, use_container_width=True)
with col2:
        st.image("https://i.cdn.newsbytesapp.com/images/l86520231130161501.jpeg?tr=w-720", use_container_width=True)