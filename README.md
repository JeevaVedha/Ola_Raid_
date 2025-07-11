
# 🚖 Ola Riders SQL Dashboard

A fully interactive, visually rich Streamlit dashboard for analyzing Ola ride booking data from a PostgreSQL database. This dashboard provides key performance metrics, booking trends, cancellation patterns, ratings, payment methods, and more – all in a single-page layout with expandable sections and a modern UI theme.

![Dashboard Preview](https://i.cdn.newsbytesapp.com/images/l86520231130161501.jpeg?tr=w-720)

---

## 📦 Features

- ✅ **Total Successful Bookings**
- 🚗 **Average Ride Distance by Vehicle Type**
- 🙅 **Cancellations by Customers & Drivers**
- ⭐ **Driver & Customer Ratings**
- 💰 **Total Booking Value**
- 🔝 **Top Customers by Ride Count**
- 📱 **UPI-Based Booking Analysis**
- ⚠️ **Incomplete Rides Overview**
- 📊 Fully interactive Plotly charts and metrics

---

## 🗃️ Data Source

The app connects to a local PostgreSQL database `Ola_Raiders` and uses a table named `july` with the following columns:

- `Date`, `Time`, `Booking_ID`, `Booking_Status`, `Customer_ID`, `Vehicle_Type`, `Pickup_Location`, `Drop_Location`, `V_TAT`, `C_TAT`, `Canceled_Rides_by_Customer`, `Canceled_Rides_by_Driver`, `Incomplete_Rides`, `Booking_Value`, `Payment_Method`, `Ride_Distance`, `Driver_Ratings`, `Customer_Rating`, `Vehicle Images`

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/JeevaVedha/Ola_Raid_.git
cd ola-sql-dashboard
```

### 2. Install Requirements

Make sure Python is installed. Then, install the dependencies:

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```
streamlit
pandas
sqlalchemy
psycopg2-binary
plotly
requests
```

### 3. Configure PostgreSQL Connection

In your Streamlit app, ensure this line is updated based on your local credentials:

```python
engine = create_engine('postgresql+psycopg2://postgres:password123@localhost:5432/Ola_Raiders')
```

> You must have a running PostgreSQL server and a database called `Ola_Raiders` with the `july` table loaded.

---

## 🚀 Run the App

```bash
streamlit run Main.py
```
---

## 📷 Screenshots

- Interactive dashboard layout with Plotly graphs
- Ola branding and modern UI styling with custom backgrounds
- Expandable sections to reduce visual clutter

---

## 📌 Credits

- Dashboard developed using **Streamlit**, **Plotly**, and **PostgreSQL**
- Ola logo from [Wikipedia](https://en.wikipedia.org/wiki/Ola_Cabs)
- Background images from [Unsplash](https://unsplash.com)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
