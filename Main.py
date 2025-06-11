import pandas as pd
from sqlalchemy import create_engine



engine = create_engine('postgresql+psycopg2://postgres:password123@localhost:5432/Ola_Raiders')
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


for col in ['Booking_Status', 'Vehicle_Type', 'Payment_Method']:
    df[col] = df[col].astype('string')
    #print(df[col].head())

BS = df['Booking_Status'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Booking_Status': {BS:.2f}%")
#df['Booking_Status'] = df['Booking_Status'].fillna('others')    

VT = df['Vehicle_Type'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Vehicle_Type': {VT:.2f}%")
# df['Vehicle_Type'] = df['Vehicle_Type'].fillna('others')
    
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

#print(df['Incomplete_Rides'])

BV = df['Booking_Value'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Booking_Value': {BV:.2f}%")

df['Booking_Value'] = pd.to_numeric(df['Booking_Value'], errors='coerce').fillna(0).astype('float64')
#print(df['Booking_Value'].head())

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

df[df.duplicated()]
print(f"Number of duplicate rows: {df.duplicated().sum()}")

print(df)