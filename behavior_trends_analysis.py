import pandas as pd

def import_data(filename: str) -> pd.DataFrame:
    """Import dataset from Excel or CSV file."""
    if filename.endswith('.xlsx'):
        return pd.read_excel(filename)
    elif filename.endswith('.csv'):
        return pd.read_csv(filename)
    else:
        raise ValueError("File format not supported. Please use Excel (.xlsx) or CSV (.csv)")

def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filter data to remove missing CustomerID and negative values."""
    return df[
        (df['CustomerID'].notna()) & 
        (df['Quantity'] > 0) & 
        (df['UnitPrice'] > 0)
    ].copy()

def loyalty_customers(df: pd.DataFrame, min_purchases: int) -> pd.DataFrame:
    """Identify loyal customers based on minimum purchase threshold."""
    purchase_counts = df.groupby('CustomerID').size().reset_index(name='purchase_count')
    loyal_customers = purchase_counts[purchase_counts['purchase_count'] >= min_purchases]
    return loyal_customers.sort_values('purchase_count', ascending=False)

def quarterly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate total revenue per quarter."""
    # Add revenue column
    df['revenue'] = df['Quantity'] * df['UnitPrice']
    # Extract quarter from InvoiceDate
    df['quarter'] = df['InvoiceDate'].dt.quarter
    # Group by quarter and sum revenue
    quarterly = df.groupby('quarter')['revenue'].sum().reset_index()
    return quarterly

def high_demand_products(df: pd.DataFrame, top_n: int) -> pd.DataFrame:
    """Identify top N products with highest total quantity sold."""
    product_demand = df.groupby('Description')['Quantity'].sum().reset_index()
    return product_demand.nlargest(top_n, 'Quantity')

def purchase_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """Create summary of average quantity and unit price per product."""
    patterns = df.groupby('Description').agg({
        'Quantity': 'mean',
        'UnitPrice': 'mean'
    }).reset_index()
    
    patterns.columns = ['product', 'avg_quantity', 'avg_unit_price']
    return patterns

def answer_conceptual_questions() -> dict:
    """Return answers to conceptual questions."""
    return {
        "Q1": {"A"},  # Data entry errors affect calculations
        "Q2": {"B"},  # Quarterly aggregation reveals seasonal trends
        "Q3": {"C"},  # Loyal customers are easier to retain
        "Q4": {"A"},  # Optimize pricing strategies based on demand
        "Q5": {"A"}   # Total quantity sold best shows demand trends
    }





import pandas as pd

# 1. First, import the data
df = import_data("Online Retail.xlsx")
print("Raw data shape:", df.shape)

# 2. Clean the data
clean_df = filter_data(df)
print("\nCleaned data shape:", clean_df.shape)

# 3. Find loyal customers (e.g., with at least 100 purchases)
loyal = loyalty_customers(clean_df, min_purchases=100)
print("\nTop 5 loyal customers:")
print(loyal.head())

# 4. Calculate quarterly revenue
revenue = quarterly_revenue(clean_df)
print("\nQuarterly revenue:")
print(revenue)

# 5. Find top 10 products in demand
top_products = high_demand_products(clean_df, top_n=10)
print("\nTop 10 products by demand:")
print(top_products)

# 6. Get purchase patterns
patterns = purchase_patterns(clean_df)
print("\nPurchase patterns (first 5 products):")
print(patterns.head())

# 7. Get answers to conceptual questions
answers = answer_conceptual_questions()
print("\nConceptual question answers:")
print(answers)
