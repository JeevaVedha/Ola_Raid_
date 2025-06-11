import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from io import StringIO

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
sheets = pd.read_excel(EXCEL_FILE, sheet_name=None, engine='openpyxl')

for sheet_name, df in sheets.items():
    table = sheet_name.strip().lower().replace(' ', '_')
    print(f"➡ Processing '{sheet_name}' → table '{table}' ({len(df)} rows)")

    # a) Create table schema using empty dataframe
    df.head(0).to_sql(name=table, con=engine, if_exists='replace', index=False)

    # b) Convert dataframe to CSV in memory
    buf = StringIO()
    df.to_csv(buf, index=False, header=False)
    buf.seek(0)

    # c) Bulk load using psycopg2 COPY
    conn = engine.raw_connection()
    cur = conn.cursor()
    cur.copy_from(buf, table, sep=',', null='')
    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Loaded {len(df)} rows into '{table}'\n")
