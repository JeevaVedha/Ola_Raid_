import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import seaborn as sns
import plotly.express as px



engine = create_engine('postgresql+psycopg2://postgres:password123@localhost:5432/Ola_Raiders')
conn = engine.connect()

df = pd.read_sql('SELECT * FROM july', engine) 

#------------------------------------------------------------------------------------------------------#
 

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
                SELECT 
                    "Customer_ID", 
                    COUNT(*) AS "Incomplete_Rides"
                FROM july
                WHERE "Booking_Status" = 'Success'
                GROUP BY "Customer_ID";
            '''
        case _:
            return ""  # default case
        
st.title("📊 Ola Riders SQL Dashboard (via switch–case)")
option = st.selectbox(
    "Choose query to run:",
    list(range(1, 11)),
    format_func=lambda x: {
        1: "1. All successful bookings",
        2: "2. Avg ride distance by vehicle type",
        3: "3. Total cancellations by customers",
        4: "4. Top 5 customers by rides",
        5: "5. Driver cancellations (personal/car)",
        6: "6. Max/min driver ratings (Prime Sedan)",
        7: "7. Rides paid via UPI",
        8: "8. Avg customer rating by vehicle type",
        9: "9. Total booking value (successful)",
        10: "10. Incomplete rides & reasons"
    }.get(x, "")
)

sql = get_query(option)
if not sql:
    st.error("Invalid selection!")
else:
    with st.spinner("Running query..."):
        df = pd.read_sql(sql, engine)
    st.success("Query executed successfully!")

    if option == 1:
        
        #st.dataframe(df, use_container_width=True)
        a,b = st.columns(2)
        a.metric(
            label="Total Successful Bookings",
            value=df.shape[0],
            delta="",
            border=True,
            help="Total number of successful bookings in July"
        )
        b.metric(
            label="Total Unique Customers",
            value=df['Customer_ID'].nunique(),
            delta="",
            border=True,
            help="Total number of unique customers in July"
        )

        st.line_chart(
            df.groupby('Date')['Booking_Value'].count(),
            use_container_width=True
        )
    elif option == 2:
        
        pip_Chart = px.pie(
            df,
            values='Avg_Ride_Distance',
            names='Vehicle_Type',
            title='Average Ride Distance by Vehicle Type',
            labels={'Avg_Ride_Distance': 'Average Ride Distance (km)'},
            color='Vehicle_Type'
        )
        st.plotly_chart(pip_Chart, use_container_width=True)
    elif option == 3:
        df = df.groupby('Customer_ID').size().reset_index(name='Total_Cancellations')
        st.metric(
            label="Total Cancellations by Customers",
            value=df['Total_Cancellations'].sum(),
            delta="",
            border=True,
            help="Total number of cancellations made by customers"
        )
        st.dataframe(df, use_container_width=True)
    elif option == 4:      
        df = df.groupby('Customer_ID').size().reset_index(name='Total_Rides')
        
        df = df.sort_values(by='Total_Rides', ascending=False).head(5)
        st.metric(
            label="Top 5 Customers by Rides",
            value=df['Total_Rides'].sum(),
            delta="",
            border=True,
            help="Total number of rides taken by top 5 customers"
        )
        st.dataframe(df, use_container_width=True)
    elif option == 5:
        df = df.groupby('Customer_ID').size().reset_index(name='Total_Cancellations')
        st.metric(
            label="Total Cancellations by Drivers",
            value=df['Total_Cancellations'].sum(),
            delta="",
            border=True,
            help="Total number of cancellations made by drivers"
        )
        st.dataframe(df, use_container_width=True)
    elif option == 6:
        df['Max_Driver_Rating'] = df['Max_Driver_Rating'].round(2)
        df['Min_Driver_Rating'] = df['Min_Driver_Rating'].round(2)
        
        st.metric(
            label="Max Driver Rating (Prime Sedan)",
            value=df['Max_Driver_Rating'].max(),
            delta="",
            border=True,
            help="Maximum driver rating for Prime Sedan vehicles"
        )
        st.metric(
            label="Min Driver Rating (Prime Sedan)",
            value=df['Min_Driver_Rating'].min(),
            delta="",
            border=True,
            help="Minimum driver rating for Prime Sedan vehicles"
        )
        st.dataframe(df, use_container_width=True)

    elif option == 7:
        st.metric(
            label="Total Successful UPI Payments",
            value=df.shape[0],
            delta="",
            border=True,
            help="Total number of successful bookings paid via UPI"
        )
        fig_donut = px.pie(
            df,
            values='Booking_Value',
            names='Vehicle_Type',
            title='Total Booking Value by Vehicle Type (UPI)',
            labels={'Booking_Value': 'Total Booking Value'},
            color='Vehicle_Type',
            hole=0.5  # 👈 This creates the donut hole
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)
    elif option == 8:
        df = df.groupby('Vehicle_Type')['Avg_Customer_Rating'].mean().reset_index()
        st.metric(
            label="Average Customer Rating by Vehicle Type",
            value=df['Avg_Customer_Rating'].mean().round(2),
            delta="",
            border=True,
            help="Average customer rating for all vehicle types"
        )
        fig_bar = px.bar(
            df,
            x='Vehicle_Type',
            y='Avg_Customer_Rating',
            title='Average Customer Rating by Vehicle Type',
            labels={'Avg_Customer_Rating': 'Average Customer Rating'},
            color='Vehicle_Type'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    elif option == 9:
        total_booking_value = df['Total_Booking_Value'].sum()
        st.metric(
            label="Total Booking Value (Successful)",
            value=f"₹{total_booking_value:,.2f}",
            delta="",
            border=True,
            help="Total booking value for all successful rides"
        )   

    elif option == 10:
        df = df.groupby('Customer_ID')['Incomplete_Rides'].count().reset_index()
        st.metric(
            label="Total Incomplete Rides",
            value=df['Incomplete_Rides'].sum(),
            delta="",
            border=True,
            help="Total number of incomplete rides in July"
        )
        st.dataframe(df, use_container_width=True)     


