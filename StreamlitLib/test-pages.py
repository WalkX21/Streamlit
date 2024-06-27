import streamlit as st
import pandas as pd

# Define each page as a function
def main_page():
    st.title("Main Page")
    st.write("Welcome to the main page!")

    # Add any main page specific content here

def products_page():
    st.title("Products Page")
    st.write("Here you can manage your products.")

    # Example table
    data = {
        "Product": ["Tomatoes", "Potatoes", "Carrots"],
        "Price": [1.5, 1.0, 0.8]
    }
    df = pd.DataFrame(data)
    st.table(df)

    # Add any product page specific content here

def order_page():
    st.title("Order Page")
    st.write("Place your orders here.")

    # Add order form or other content here

def log_page():
    st.title("Transaction Log Page")
    st.write("View your transaction logs here.")

    # Example transaction log
    log_data = {
        "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "Transaction": ["Order 1", "Order 2", "Order 3"]
    }
    log_df = pd.DataFrame(log_data)
    st.table(log_df)

    # Add any log page specific content here

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main Page", "Products Page", "Order Page", "Transaction Log Page"])

# Display the selected page
if page == "Main Page":
    main_page()
elif page == "Products Page":
    products_page()
elif page == "Order Page":
    order_page()
elif page == "Transaction Log Page":
    log_page()
