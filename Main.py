import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import seaborn as sns
import plotly.express as px



engine = create_engine('postgresql+psycopg2://postgres:password123@localhost:5432/Ola_Raiders')
conn = engine.connect()

df = pd.read_sql('SELECT * FROM july', engine) 

# Display the first few rows of the dataframe
# print(df.head())
#df.info()
#df.describe() 
#df = df.convert_dtypes()


# Columns 1 & 2 to datetime conversion
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce').dt.date
# df['Month'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce').dt.month
#df['Year'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce').dt.year
#df['Week']= pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce').dt.isocalendar().week

df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.time

#print(df['Date'].head())
#print(df['Time'].head())
#print(df['Month'].head())
#print(df['Year'].head()) 
#print(df['Week'].head())   


for col in ['Booking_Status', 'vehicle_type', 'Payment_Method']:
    df[col] = df[col].astype('string')
    #print(df[col].head())

BS = df['Booking_Status'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Booking_Status': {BS:.2f}%")
#df['Booking_Status'] = df['booking_status'].fillna('others')    

VT = df['vehicle_type'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'vehicle_type': {VT:.2f}%")
# df['vehicle_type'] = df['vehicle_type'].fillna('others')
    
CRBC = df['Canceled_Rides_by_Customer'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Canceled_Rides_by_Customer': {CRBC:.2f}%")
CRBD = df['Canceled_Rides_by_Driver'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Canceled_Rides_by_Driver': {CRBD:.2f}%")

#df['Canceled_Rides_by_Customer'] = pd.to_numeric(df['Canceled_Rides_by_Customer'], errors='coerce').fillna(0).astype('Int64')
#df['Canceled_Rides_by_Driver'] = pd.to_numeric(df['Canceled_Rides_by_Driver'], errors='coerce').fillna(0).astype('Int64')
df['Canceled_Rides_by_Customer'].dropna(inplace=True)
df['Canceled_Rides_by_Driver'].dropna(inplace=True)

 
#print(df['Canceled_Rides_by_Customer'].tail())
##print(df['Incomplete_Rides'].head())

ICR = df['Incomplete_Rides'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Incomplete_Rides': {ICR:.2f}%")
df['Incomplete_Rides'] = pd.to_numeric(df['Incomplete_Rides'], errors='coerce').fillna(0).astype('Int64')
df['Incomplete_Rides'].dropna(inplace=True)

#print(df['Incomplete_Rides'])

BV = df['booking_values'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Booking_Value': {BV:.2f}%")

df['booking_values'] = pd.to_numeric(df['booking_values'], errors='coerce').fillna(0).astype('float64')
#print(df['booking_values'].head())

pm = df['Payment_Method'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Payment_Method': {pm:.2f}%")
df['Payment_Method'] = df['Payment_Method'].fillna('others')

#df['Payment_Method'] = df['Payment_Method'].astype('string')
#df['Payment_Method'] = df['Payment_Method'].fillna('Others')
 
#print(df['Payment_Method'])
RD = df['Ride_Distance'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Ride_Distance': {RD:.2f}%")

df['Ride_Distance'] = pd.to_numeric(df['Ride_Distance'], errors='coerce').astype('float64')
#print(df['Ride_Distance'].head())

DR = df['Driver_Ratings'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Driver_Ratings': {DR:.2f}%")

df['Driver_Ratings'] = pd.to_numeric(df['Driver_Ratings'], errors='coerce').astype('float64')
mean_rating = df['Driver_Ratings'].mean()
df['Driver_Ratings'] = df['Driver_Ratings'].fillna(mean_rating).round(1)
#print(df['Driver_Ratings'])

CR = df['Customer_Rating'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Customer_Rating': {CR:.2f}%")

df['Customer_Rating']  = pd.to_numeric(df['Customer_Rating'], errors='coerce').astype('float64')
#print(df['Customer_Rating'])
mean_customer_rating = df['Customer_Rating'].mean() 
#df['Customer_Rating'] = df['Customer_Rating'].fillna(mean_customer_rating).round(1)
#print(df['Customer_Rating'])

#print(df)

#------------------------------------------------------------------------------------------------------#
 

def get_query(option: int) -> str:
    match option:
        case 1:
            return "SELECT * FROM july WHERE booking_status = 'Success';"
        
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
    st.success("Query completed!")


    # --- Donut chart via Plotly ---
    fig = px.pie(
        df,
        names='vehicle_type',
        values='booking_values',
        hole=0.5,
        title=f"Successfull Booking Status by Vehicle Type",
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')

    # Display chart
    st.plotly_chart(fig, use_container_width=True)

     # Display results
    st.subheader(f"Results for: {option}")
    st.dataframe(df, use_container_width=True)
    st.title("📊 Booking Status by Vehicle Type")

    value_count = df['booking_status'].value_counts().reset_index()
    value_count.columns = ['booking_status', 'value_count']
    # Display the value counts as a dataframe
    st.dataframe(value_count, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Booking Status Distribution")
        st.metric("✅ Successful Bookings", df['booking_status'].value_counts().get('Success', 0))

         
    with col2:
        st.subheader("Booking Status by Vehicle Type")
        st.metric("✅ Successful Bookings", df['booking_status'].value_counts().get('Success', 0))
 
    
    # Apply card styling
    style_metric_cards(
        background_color="#f0f9f5",
        border_color="#a6d7c0",
        border_size_px=2,
        border_left_color="#34a853",
        border_radius_px=8,
        box_shadow=True,
    )
    # For aggregated numeric results (#3,5,9), display a metric
    if option in {3, 5, 9} and not df.empty:
        val = df.iloc[0, 0]
        st.metric(label="Result", value=int(val))
 
 