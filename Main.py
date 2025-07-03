import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine

# PostgreSQL Connection
engine = create_engine('postgresql+psycopg2://postgres:password123@localhost:5432/Ola_Raiders')
conn = engine.connect()
df = pd.read_sql('SELECT * FROM july LIMIT 1', engine)
print(df.columns.tolist())
# Title
st.title("📊 Ola Riders SQL Dashboard (10 Dynamic Insights)")

# Query Selector
option = st.selectbox(
    "Choose a query to run:",
    list(range(1, 11)),
    format_func=lambda x: {
        1: "1. Retrieve all successful bookings",
        2: "2. Average ride distance by vehicle type",
        3: "3. Total customer-cancelled rides",
        4: "4. Top 5 customers by booking count",
        5: "5. Driver cancellations by reason",
        6: "6. Max/Min driver ratings (Prime Sedan)",
        7: "7. All rides paid via UPI",
        8: "8. Average customer rating per vehicle type",
        9: "9. Total booking value (successful)",
        10: "10. Incomplete rides with reasons"
    }.get(x, "Invalid")
)

# SQL Logic
def get_query(option: int) -> str:
    match option:
        case 1:
            return 'SELECT * FROM july WHERE "Booking_Status" = \'Success\';'
        case 2:
            return 'SELECT "Vehicle_Type", ROUND(AVG("Ride_Distance")::NUMERIC, 2) AS "Avg_Ride_Distance" FROM july GROUP BY "Vehicle_Type";'
        
        case 3:
            return 'SELECT SUM("Canceled_Rides_by_Customer") AS "Total_Customer_Cancellations" FROM july;'
        case 4:
            return 'SELECT "Customer_ID", COUNT(*) AS "Total_Rides" FROM july GROUP BY "Customer_ID" ORDER BY "Total_Rides" DESC LIMIT 5;'
        case 5:
            return 'SELECT "Cancel_Reason", COUNT(*) AS "Total_Cancellations" FROM july WHERE "Cancelled_By" = \'Driver\' GROUP BY "Cancel_Reason";'
        case 6:
            return 'SELECT MAX("Driver_Rating") AS "Max_Rating", MIN("Driver_Rating") AS "Min_Rating" FROM july WHERE "Vehicle_Type" = \'Prime Sedan\';'
        case 7:
            return 'SELECT * FROM july WHERE "Payment_Method" = \'UPI\';'
        case 8:
            return 'SELECT "Vehicle_Type", ROUND(AVG("Customer_Rating"), 2) AS "Avg_Customer_Rating" FROM july GROUP BY "Vehicle_Type";'
        case 9:
            return 'SELECT SUM("Booking_Value") AS "Total_Successful_Booking_Value" FROM july WHERE "Booking_Status" = \'Success\';'
        case 10:
            return 'SELECT "Ride_Status", COUNT(*) AS "Count" FROM july WHERE "Ride_Status" != \'Completed\' GROUP BY "Ride_Status";'
        case _:
            return ""

# Run Query
sql = get_query(option)
if sql:
    try:
        df = pd.read_sql(sql, conn)

        if df.empty:
            st.warning("⚠️ No data found for this query.")
        else:
            # Shared Output
            st.subheader("📋 Query Result")
            if option == 1:
                st.metric("Total Successful Bookings", df.shape[0])
             # Visualizations per query
            elif option == 2:
                fig = px.bar(df, x="Vehicle_Type", y="Avg_Ride_Distance", text="Avg_Ride_Distance",
                             title="Average Ride Distance by Vehicle Type", color="Vehicle_Type")
                st.plotly_chart(fig, use_container_width=True)

            elif option == 3:
                st.metric("Total Customer Cancellations", df.iloc[0, 0])

            elif option == 4:
                fig = px.bar(df, x="Total_Rides", y="Customer_ID", orientation='h', text="Total_Rides",
                             title="Top 5 Customers by Number of Rides", color="Total_Rides")
                st.plotly_chart(fig, use_container_width=True)

            elif option == 5:
                fig = px.pie(df, names="Cancel_Reason", values="Total_Cancellations", hole=0.4,
                             title="Driver Cancellations by Reason")
                fig.update_traces(textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

            elif option == 6:
                col1, col2 = st.columns(2)
                col1.metric("Max Driver Rating", df['Max_Rating'][0])
                col2.metric("Min Driver Rating", df['Min_Rating'][0])

            elif option == 8:
                fig = px.bar(df, x="Vehicle_Type", y="Avg_Customer_Rating", text="Avg_Customer_Rating",
                             title="Average Customer Rating by Vehicle Type", color="Vehicle_Type")
                st.plotly_chart(fig, use_container_width=True)

            elif option == 9:
                st.metric("Total Booking Value (Successful)", f"₹{df['Total_Successful_Booking_Value'][0]:,.2f}")

            elif option == 10:
                fig = px.pie(df, names="Ride_Status", values="Count", hole=0.4,
                             title="Incomplete Ride Reasons")
                fig.update_traces(textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error executing query: {e}")
else:
    st.error("❌ Invalid query selected.")
