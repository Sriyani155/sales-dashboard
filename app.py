
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

st.title("📊 Sales Analytics Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Total_Sales'] = df['Quantity'] * df['Price']
    df.dropna(inplace=True)
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter")
categories = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())
regions = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
start_date, end_date = st.sidebar.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])

# Apply Filters
filtered_df = df[
    (df['Category'].isin(categories)) &
    (df['Region'].isin(regions)) &
    (df['Date'] >= pd.to_datetime(start_date)) &
    (df['Date'] <= pd.to_datetime(end_date))
]

# KPIs
total_sales = filtered_df['Total_Sales'].sum()
total_orders = filtered_df['Order_ID'].nunique()
avg_order_value = filtered_df['Total_Sales'].mean()

st.metric("💰 Total Sales", f"${total_sales:,.2f}")
st.metric("📦 Total Orders", total_orders)
st.metric("📈 Avg Order Value", f"${avg_order_value:,.2f}")

# Revenue by Category
st.subheader("💼 Revenue by Category")
rev_by_category = filtered_df.groupby('Category')['Total_Sales'].sum().reset_index().sort_values(by='Total_Sales', ascending=False)
fig1, ax1 = plt.subplots()
sns.barplot(data=rev_by_category, x='Category', y='Total_Sales', ax=ax1)
ax1.set_title("Revenue by Category")
ax1.set_ylabel("Total Sales")
ax1.set_xlabel("Category")
plt.xticks(rotation=45)
st.pyplot(fig1)

# Daily Sales Trend
st.subheader("📅 Daily Sales Trend")
daily_sales = filtered_df.groupby('Date')['Total_Sales'].sum().reset_index()
fig2, ax2 = plt.subplots()
ax2.plot(daily_sales['Date'], daily_sales['Total_Sales'], marker='o')
ax2.set_title("Daily Sales Trend")
ax2.set_xlabel("Date")
ax2.set_ylabel("Total Sales")
plt.xticks(rotation=45)
st.pyplot(fig2)

# Region-wise Revenue
st.subheader("🌍 Revenue by Region")
region_sales = filtered_df.groupby('Region')['Total_Sales'].sum().reset_index().sort_values(by='Total_Sales', ascending=False)
fig3, ax3 = plt.subplots()
sns.barplot(data=region_sales, x='Region', y='Total_Sales', ax=ax3)
ax3.set_title("Revenue by Region")
ax3.set_ylabel("Total Sales")
ax3.set_xlabel("Region")
plt.xticks(rotation=45)
st.pyplot(fig3)

st.success("✅ Dashboard loaded successfully.")
