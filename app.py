
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 SALES ANALYSIS DASHBOARD")
st.markdown("### Business Insights | Sales Performance | Customer Analysis")
st.divider()

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    orders = pd.read_csv("clean_orders.csv")
    customers = pd.read_csv("clean_customers.csv")

    orders.columns = orders.columns.str.strip()
    customers.columns = customers.columns.str.strip()

    # Convert numerical columns
    orders["Sales"] = pd.to_numeric(
        orders["Sales"], errors="coerce"
    )
    orders["Quantity"] = pd.to_numeric(
        orders["Quantity"], errors="coerce"
    )

    # Remove invalid sales records
    orders = orders.dropna(
        subset=["Sales", "Quantity", "Product", "Region"]
    )

    orders = orders[
        (orders["Sales"] > 0) &
        (orders["Quantity"] > 0)
    ].copy()

    # Merge sales and customer information
    data = orders.merge(
        customers,
        on="Customer_ID",
        how="left",
        suffixes=("", "_Customer")
    )

    return data, customers


try:
    df, customers = load_data()
except Exception as e:
    st.error(f"Error loading CSV files: {e}")
    st.stop()

if df.empty:
    st.warning("No valid sales records found.")
    st.stop()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Dashboard Filters")

regions = sorted(df["Region"].dropna().unique())
products = sorted(df["Product"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)

selected_products = st.sidebar.multiselect(
    "Select Product",
    products,
    default=products
)

filtered_df = df[
    df["Region"].isin(selected_regions) &
    df["Product"].isin(selected_products)
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ---------------- KPI CALCULATIONS ----------------
total_sales = filtered_df["Sales"].sum()
total_orders = filtered_df["Order_ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()
average_order = total_sales / total_orders if total_orders else 0

# ---------------- KPI CARDS ----------------
st.subheader("📌 Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Sales", f"₹{total_sales:,.2f}")
c2.metric("📦 Total Orders", f"{total_orders:,}")
c3.metric("🛒 Quantity Sold", f"{total_quantity:,.0f}")
c4.metric("📈 Average Order Value", f"₹{average_order:,.2f}")

st.divider()

# ---------------- SALES BY PRODUCT ----------------
st.subheader("📦 Product Analysis")

product_sales = (
    filtered_df.groupby("Product", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        product_sales,
        x="Product",
        y="Sales",
        color="Product",
        title="Sales by Product",
        text_auto=".2s"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(
        product_sales,
        names="Product",
        values="Sales",
        title="Product-wise Sales Distribution",
        hole=0.4
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- REGION ANALYSIS ----------------
st.subheader("🌍 Regional Sales Analysis")

region_sales = (
    filtered_df.groupby("Region", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

fig3 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    color="Region",
    title="Sales Performance by Region",
    text_auto=".2s"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- QUANTITY ANALYSIS ----------------
st.subheader("🛒 Quantity Analysis")

quantity_data = (
    filtered_df.groupby("Product", as_index=False)["Quantity"]
    .sum()
)

fig4 = px.bar(
    quantity_data,
    x="Product",
    y="Quantity",
    color="Product",
    title="Quantity Sold by Product"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- CUSTOMER ANALYSIS ----------------
st.subheader("👥 Customer Analysis")

customer_sales = (
    filtered_df.groupby("Customer_ID", as_index=False)
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Orders=("Order_ID", "nunique")
    )
)

customer_sales = customer_sales.merge(
    customers[["Customer_ID", "Customer_Name"]],
    on="Customer_ID",
    how="left"
)

customer_sales = customer_sales.sort_values(
    "Total_Sales", ascending=False
)

st.dataframe(
    customer_sales,
    use_container_width=True,
    hide_index=True
)

# ---------------- COMPLETE SALES DATA ----------------
st.subheader("📋 Sales Details")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# ---------------- DOWNLOAD REPORT ----------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Sales Report",
    data=csv,
    file_name="sales_analysis_report.csv",
    mime="text/csv"
)

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "Developed using Python | Pandas | Streamlit | Plotly"
)
