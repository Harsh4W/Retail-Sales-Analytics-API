from fastapi import FastAPI, Query
from src.analytics import (
    get_total_sales,
    get_monthly_sales,
    get_top_products,
    get_category_sales,
    get_state_sales,
    get_payment_analysis,
    get_delivery_performance,
    get_order_status
)

app = FastAPI(
    title="Retail Sales Analytics API",
    description="API for analyzing Brazilian E-Commerce sales data",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Retail Sales Analytics API",
        "status": "Running"
    }


@app.get("/sales/summary")
def sales_summary():
    return get_total_sales()


@app.get("/sales/monthly")
def monthly_sales():
    df = get_monthly_sales()
    return df.to_dict(orient="records")


@app.get("/products/top")
def top_products(
    limit: int = Query(default=10, ge=1, le=100)
):
    df = get_top_products(limit=limit)
    return df.to_dict(orient="records")


@app.get("/categories")
def category_sales(
    limit: int = Query(default=10, ge=1, le=100)
):
    df = get_category_sales(limit=limit)
    return df.to_dict(orient="records")


@app.get("/states")
def state_sales():
    df = get_state_sales()
    return df.to_dict(orient="records")


@app.get("/payments")
def payment_analysis():
    df = get_payment_analysis()
    return df.to_dict(orient="records")


@app.get("/delivery")
def delivery_performance():
    return get_delivery_performance()


@app.get("/orders/status")
def order_status():
    df = get_order_status()
    return df.to_dict(orient="records")