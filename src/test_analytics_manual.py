from src.analytics import (
    get_total_sales,
    get_top_products,
    get_category_sales,
    get_monthly_sales
)

# Test total sales
sales = get_total_sales()

print("\nTotal sales:")
print(sales)

# Test top 5 products
products = get_top_products(5)

print("\nTop 5 products:")
print(products)

# Test top 5 categories
categories = get_category_sales(5)

print("\nTop 5 categories:")
print(categories)

# Test monthly sales
monthly = get_monthly_sales()

print("\nMonthly sales:")
print(monthly)

print("\nManual analytics testing completed!")