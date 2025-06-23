import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from io import StringIO
import plotly.express as px

# ---------------- PostgreSQL connection settings ----------------
db_user = 'postgres'
db_password = 'password123'
db_host = 'localhost'
db_port = '5432'
db_name = 'Ola_Raiders'
EXCEL_FILE = 'Data/OLA_DataSet.xlsx'

# ---------------- Step 1: Connect to default postgres db ----------------
# First connect to the 'postgres' database (built-in) to check/create your target db
default_conn = psycopg2.connect(
    dbname='postgres',
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)
default_conn.autocommit = True
cursor = default_conn.cursor()

# Check if the target database exists
cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
exists = cursor.fetchone()

if not exists:
    print(f"🔨 Database '{db_name}' does not exist. Creating...")
    cursor.execute(f'CREATE DATABASE "{db_name}";')
    print(f"✅ Database '{db_name}' created.")
else:
    print(f"✅ Database '{db_name}' already exists.")

cursor.close()
default_conn.close()

# ---------------- Step 2: Connect to the target database ----------------
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
# Test the connection
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1;"))
        print("✅ Connection to the database is successful.")
except Exception as e:
    print(f"❌ Connection failed: {e}")

# 2️⃣ Read all sheets from Excel
df = pd.read_excel(EXCEL_FILE, sheet_name='July', engine='openpyxl')

#print(df)
#df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce').dt.date
print(f"✅ Converted 'Date' column to datetime format.")
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce').dt.date
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.time
#print(df['Time'].head())

VTAT = df['V_TAT'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'V_TAT': {VTAT:.2f}%")
df['V_TAT'] = pd.to_numeric(df['V_TAT'], errors='coerce').fillna(0).astype('float64')

CTAT = df['C_TAT'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'C_TAT': {CTAT:.2f}%")
df['C_TAT'] = pd.to_numeric(df['C_TAT'], errors='coerce').fillna(0).astype('float64')

for col in ['Booking_Status', 'Vehicle_Type', 'Payment_Method']:
    df[col] = df[col].astype('string')
    #print(df[col].head())

BS = df['Booking_Status'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Booking_Status': {BS:.2f}%")
df['Booking_Status'] = df['Booking_Status'].fillna('others')    

VT = df['Vehicle_Type'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Vehicle_Type': {VT:.2f}%")
df['Vehicle_Type'] = df['Vehicle_Type'].fillna('others')

PM = df['Payment_Method'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Payment_Method': {PM:.2f}%")
df['Payment_Method'] = df['Payment_Method'].fillna('others')

CRBC = df['Canceled_Rides_by_Customer'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Canceled_Rides_by_Customer': {CRBC:.2f}%")
#df['Canceled_Rides_by_Customer'] = df['Canceled_Rides_by_Customer'].fillna('Not Mentioned')
df.drop('Canceled_Rides_by_Customer', axis=1, inplace=True)


CRBD = df['Canceled_Rides_by_Driver'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Canceled_Rides_by_Driver': {CRBD:.2f}%")
df['Canceled_Rides_by_Driver'] = df['Canceled_Rides_by_Driver'].fillna('Not Mentioned')
df.drop('Canceled_Rides_by_Driver', axis=1, inplace=True)

#df['Canceled_Rides_by_Customer'] = pd.to_numeric(df['Canceled_Rides_by_Customer'], errors='coerce').fillna(0).astype('Int64')
#df['Canceled_Rides_by_Driver'] = pd.to_numeric(df['Canceled_Rides_by_Driver'], errors='coerce').fillna(0).astype('Int64')
 
 
 
#print(df['Canceled_Rides_by_Customer'].tail())
##print(df['Incomplete_Rides'].head())

ICR = df['Incomplete_Rides'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Incomplete_Rides': {ICR:.2f}%")
df['Incomplete_Rides'] = pd.to_numeric(df['Incomplete_Rides'], errors='coerce').fillna(0).astype('Int64')
df['Incomplete_Rides'] = df['Incomplete_Rides'].fillna('Not Mentioned')

ICRR = df['Incomplete_Rides_Reason'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Incomplete_Rides_Reason': {ICRR:.2f}%")
df.drop('Incomplete_Rides_Reason', axis=1, inplace=True) 
#print(df['Incomplete_Rides'])

BV = df['Booking_Value'].isnull().sum() / len(df) * 100
print(f"Percentage of null values in 'Booking_Value': {BV:.2f}%")

df['Booking_Value'] = pd.to_numeric(df['Booking_Value'], errors='coerce').fillna(0).astype('float64')
#print(df['Booking_Value'].head())

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
df['Customer_Rating'] = df['Customer_Rating'].fillna(mean_customer_rating).round(1)
#print(df['Customer_Rating'])
 
# a) Create empty table schema
df.head(0).to_sql('july', con=engine, if_exists='replace', index=False)

# b) Bulk load via COPY

buf = StringIO()
df.to_csv(buf, index=False, header=False)
buf.seek(0)

conn = engine.raw_connection()
cur = conn.cursor()
cur.copy_expert("COPY july FROM STDIN WITH CSV", buf)
conn.commit()
cur.close()
conn.close()

print(f"✅ Loaded {len(df)} rows via COPY")