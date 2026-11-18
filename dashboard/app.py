
import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

import os

API_URL = os.getenv(
    "API_URL",
    "https://retail-sales-analytics-api.onrender.com"
)


# --------------------------------------------------
# 2. API DATA FETCHING FUNCTION
# --------------------------------------------------

def fetch_data(endpoint):
    """
    Fetch data from the FastAPI backend.
    """

    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI. "
            "Please start the backend server."
        )
        st.stop()

    except requests.exceptions.RequestException as error:
        st.error(f"API request failed: {error}")
        st.stop()

    except ValueError:
        st.error(f"Invalid JSON response from {endpoint}")
        st.stop()


# --------------------------------------------------
# 3. LOAD ALL DASHBOARD DATA
# --------------------------------------------------

def load_dashboard_data():

    sales = fetch_data("/sales/summary")

    monthly_sales = pd.DataFrame(
        fetch_data("/sales/monthly")
    )

    top_products = pd.DataFrame(
        fetch_data("/products/top?limit=10")
    )

    categories = pd.DataFrame(
        fetch_data("/categories")
    )

    states = pd.DataFrame(
        fetch_data("/states")
    )

    payments = pd.DataFrame(
        fetch_data("/payments")
    )

    delivery = fetch_data("/delivery")

    order_status_data = fetch_data("/orders/status")

    order_status = pd.DataFrame(order_status_data)

    return (
        sales,
        monthly_sales,
        top_products,
        categories,
        states,
        payments,
        delivery,
        order_status
    )


# --------------------------------------------------
# 4. DASHBOARD HEADER
# --------------------------------------------------

st.title("📊 Retail Sales Analytics Dashboard")

st.markdown(
    """
    Analyze sales performance, product trends,
    customer locations, payment methods and delivery.
    """
)

st.divider()


# --------------------------------------------------
# 5. SIDEBAR
# --------------------------------------------------

st.sidebar.title("Dashboard Controls")

st.sidebar.write("Data Source: FastAPI")

if st.sidebar.button("🔄 Refresh Dashboard"):
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.caption(
    "Brazilian E-Commerce Public Dataset (Olist)"
)


# --------------------------------------------------
# 6. FETCH DATA
# --------------------------------------------------

(
    sales,
    monthly_sales,
    top_products,
    categories,
    states,
    payments,
    delivery,
    order_status
) = load_dashboard_data()


# --------------------------------------------------
# 7. VALIDATE ORDER STATUS DATA
# --------------------------------------------------

required_columns = [
    "order_status",
    "total_orders"
]

if order_status.empty:
    st.error(
        "Order status data is empty. "
        "Check the /orders/status API response."
    )
    st.stop()

missing_columns = [
    column for column in required_columns
    if column not in order_status.columns
]

if missing_columns:
    st.error(
        f"Missing columns in order status data: {missing_columns}"
    )

    st.write("Received columns:", order_status.columns.tolist())
    st.write("Received data:", order_status)

    st.stop()


# --------------------------------------------------
# 8. BUSINESS OVERVIEW
# --------------------------------------------------

st.subheader("Business Overview")

delivered_orders = int(
    order_status.loc[
        order_status["order_status"] == "delivered",
        "total_orders"
    ].sum()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Product Sales",
    f"R$ {sales['product_sales'] / 1_000_000:.2f}M",
    help=f"Exact value: R$ {sales['product_sales']:,.2f}"
)

col2.metric(
    "Freight Value",
    f"R$ {sales['freight_value'] / 1_000_000:.2f}M",
    help=f"Exact value: R$ {sales['freight_value']:,.2f}"
)

col3.metric(
    "Delivered Orders",
    f"{delivered_orders:,}"
)

col4.metric(
    "Average Delivery",
    f"{delivery['average_delivery_days']:.2f} days"
)

# --------------------------------------------------
# 9. MONTHLY SALES PERFORMANCE
# --------------------------------------------------

st.subheader("Monthly Sales Performance")

if not monthly_sales.empty:

    monthly_sales["sales_month"] = pd.to_datetime(
        monthly_sales["sales_month"],
        format="%Y-%m"
    )

    fig_monthly = px.line(
        monthly_sales,
        x="sales_month",
        y="monthly_product_sales",
        markers=True,
        title="Monthly Product Sales",
        labels={
            "sales_month": "Month",
            "monthly_product_sales": "Product Sales (R$)"
        }
    )

    fig_monthly.update_layout(
        hovermode="x unified",
        xaxis_title="Month",
        yaxis_title="Sales (R$)"
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

else:
    st.info("No monthly sales data available.")

st.divider()


# --------------------------------------------------
# 10. PRODUCT ANALYSIS
# --------------------------------------------------

st.subheader("Product Analysis")

col1, col2 = st.columns(2)

with col1:

    if not top_products.empty:

        fig_products = px.bar(
            top_products.sort_values(
                "total_product_sales",
                ascending=True
            ),
            x="total_product_sales",
            y="product_id",
            orientation="h",
            title="Top 10 Products by Sales",
            labels={
                "total_product_sales": "Sales (R$)",
                "product_id": "Product ID"
            }
        )

        st.plotly_chart(
            fig_products,
            use_container_width=True
        )

    else:
        st.info("No product data available.")


with col2:

    if not categories.empty:

        fig_categories = px.bar(
            categories.sort_values(
                "total_product_sales",
                ascending=True
            ),
            x="total_product_sales",
            y="category",
            orientation="h",
            title="Top Product Categories",
            labels={
                "total_product_sales": "Sales (R$)",
                "category": "Category"
            }
        )

        st.plotly_chart(
            fig_categories,
            use_container_width=True
        )

    else:
        st.info("No category data available.")

st.divider()


# --------------------------------------------------
# 11. GEOGRAPHICAL SALES ANALYSIS
# --------------------------------------------------

st.subheader("Geographical Sales Analysis")

if not states.empty:

    fig_states = px.bar(
        states.sort_values(
            "total_product_sales",
            ascending=False
        ),
        x="customer_state",
        y="total_product_sales",
        title="Sales by Customer State",
        labels={
            "customer_state": "State",
            "total_product_sales": "Product Sales (R$)"
        }
    )

    st.plotly_chart(
        fig_states,
        use_container_width=True
    )

else:
    st.info("No geographical sales data available.")

st.divider()


# --------------------------------------------------
# 12. PAYMENT ANALYSIS
# --------------------------------------------------

st.subheader("Payment Analysis")

col1, col2 = st.columns(2)

if not payments.empty:

    with col1:

        fig_payment = px.pie(
            payments,
            names="payment_type",
            values="total_payment_value",
            title="Payment Value by Payment Method",
            hole=0.4
        )

        st.plotly_chart(
            fig_payment,
            use_container_width=True
        )

    with col2:

        fig_payment_orders = px.bar(
            payments,
            x="payment_type",
            y="unique_orders",
            title="Unique Orders by Payment Method",
            labels={
                "payment_type": "Payment Method",
                "unique_orders": "Unique Orders"
            }
        )

        st.plotly_chart(
            fig_payment_orders,
            use_container_width=True
        )

else:
    st.info("No payment data available.")

st.divider()


# --------------------------------------------------
# 13. ORDER STATUS DISTRIBUTION
# --------------------------------------------------

st.subheader("Order Status Distribution")

fig_status = px.bar(
    order_status.sort_values(
        "total_orders",
        ascending=True
    ),
    x="total_orders",
    y="order_status",
    orientation="h",
    text="total_orders",
    title="Number of Orders by Status",
    labels={
        "order_status": "Order Status",
        "total_orders": "Number of Orders"
    }
)

fig_status.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_status.update_layout(
    xaxis_title="Number of Orders",
    yaxis_title="Order Status"
)

st.plotly_chart(
    fig_status,
    use_container_width=True
)

st.dataframe(
    order_status,
    use_container_width=True,
    hide_index=True
)

st.divider()

# --------------------------------------------------
# 14. DELIVERY PERFORMANCE
# --------------------------------------------------

st.subheader("Delivery Performance")

col1, col2 = st.columns(2)

col1.metric(
    "Average Delivery Time",
    f"{delivery['average_delivery_days']:.2f} days"
)

col2.metric(
    "Average Days vs Estimated",
    f"{delivery['average_days_vs_estimate']:.2f} days"
)

st.caption(
    "A negative average difference means orders "
    "were delivered earlier than estimated."
)

st.divider()


# --------------------------------------------------
# 15. DETAILED DATA TABLES
# --------------------------------------------------

st.subheader("Detailed Analytics Data")

with st.expander("View Monthly Sales Data"):

    st.dataframe(
        monthly_sales,
        use_container_width=True,
        hide_index=True
    )


with st.expander("View Top Products Data"):

    st.dataframe(
        top_products,
        use_container_width=True,
        hide_index=True
    )


with st.expander("View Category Sales Data"):

    st.dataframe(
        categories,
        use_container_width=True,
        hide_index=True
    )


with st.expander("View State Sales Data"):

    st.dataframe(
        states,
        use_container_width=True,
        hide_index=True
    )


with st.expander("View Payment Data"):

    st.dataframe(
        payments,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# 16. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Retail Sales Analytics Dashboard | "
    "Built using Python, Pandas, Plotly, "
    "Streamlit, FastAPI and SQLite"
)
