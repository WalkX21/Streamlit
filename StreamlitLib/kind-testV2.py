
import streamlit as st
import pandas as pd
from datetime import date, datetime
import os

st.title('Command')

# Paths to the files
PRODUCTS_FILE = 'products.csv'
LOG_FILE = 'transaction_log.txt'

# Load product data from CSV
if os.path.exists(PRODUCTS_FILE):
    products_df = pd.read_csv(PRODUCTS_FILE)
    products = products_df['product'].tolist()
    prices = products_df['price'].tolist()
else:
    # Predefined products and their prices
    products = ['Tomatoes 🍅', 'Potatoes 🥔', 'Carrots 🥕', 'Cucumber 🥒', 'Lettuce 🥬']
    prices = [1.5, 1.0, 0.8, 1.2, 0.9]

    # Save predefined products to CSV
    products_df = pd.DataFrame({'product': products, 'price': prices})
    products_df.to_csv(PRODUCTS_FILE, index=False)

# Function to save products to CSV
def save_products():
    df = pd.DataFrame({'product': products, 'price': prices})
    df.to_csv(PRODUCTS_FILE, index=False)

# Initialize session state to store order
if 'order' not in st.session_state:
    st.session_state.order = []

# Function to add a product to the order
def add_product():
    if st.session_state.name == 'Other':
        product_name = st.session_state.custom_product_name
        product_price = st.session_state.custom_product_price
        if product_name not in products:
            products.append(product_name)
            prices.append(product_price)
            save_products()
    else:
        product_name = st.session_state.name
        product_index = products.index(product_name)
        product_price = prices[product_index]

    product = {
        'name': product_name,
        'quantity': st.session_state.how_many,
        'date': st.session_state.date,
        'price': product_price
    }
    st.session_state.order.append(product)

# Function to log transaction
def log_transaction(order):
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H+1:%M:%S')
        f.write(f"Transaction at {timestamp}\n")
        for product in order:
            f.write(f"{product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {product['quantity'] * product['price']} $)\n")
        f.write("\n")

# Function to create receipt
def create_receipt(order):
    receipt = "Receipt\n"
    total_price = 0.0
    for product in order:
        product_total = product['quantity'] * product['price']
        total_price += product_total
        receipt += f"{product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {product_total} $)\n"
    receipt += f"Total Price: {total_price} $\n"
    return receipt

# Sidebar product selection
st.sidebar.header('Product Selection')
product_selection = products + ['Other']
name = st.sidebar.selectbox('Which product', product_selection, key='name')

# If 'Other' is selected, show inputs for new product creation
if name == 'Other':
    with st.sidebar.expander('Create a new product'):
        st.text_input('Enter new product name', key='custom_product_name')
        st.number_input('Enter new product price per kg', min_value=0.00, value=0.0, key='custom_product_price')

# Access to transaction log
st.sidebar.header('Admin Access')
password = st.sidebar.text_input('Enter password', type='password')
if st.sidebar.button('Download Transaction Log') and password == 'wewe':
    with open(LOG_FILE, 'rb') as file:
        st.sidebar.download_button('Download Log File', file, file_name='transaction_log.txt')

# Feedback Form
with st.form('Command'):
    st.header('Add a Product')

    col1, col2 = st.columns(2)
    with col1:
        how_many = st.number_input('How much (qt in kg)', min_value=0.00, max_value=10.00, value=0.0, key='how_many')
    with col2:
        date = st.date_input('Enter Date', value=date.today(), key='date')

        if name != 'Other':
            product_index = products.index(name)
            product_price = prices[product_index]
            st.write(f'Price per kg: {product_price} $')
        else:
            product_price = st.session_state.custom_product_price
            st.write(f'Price per kg: {product_price} $')

    add_another = st.form_submit_button('Add Another Product', on_click=add_product)
    submit_button = st.form_submit_button('Submit Order')

# Display current order
if st.session_state.order:
    st.subheader('Current Order')
    for i, product in enumerate(st.session_state.order):
        st.write(f"**Product {i + 1}:** {product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {product['quantity'] * product['price']} $)")

# Submit order
if submit_button:
    st.subheader('Final Order')
    total_price = 0.0
    for i, product in enumerate(st.session_state.order):
        product_total = product['quantity'] * product['price']
        total_price += product_total
        st.write(f"**Product {i + 1}:** {product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {product_total} $)")
    st.write(f"**Total Price:** {total_price} $")

    # Log the transaction
    log_transaction(st.session_state.order)

    # Create receipt
    receipt = create_receipt(st.session_state.order)
    st.download_button('Download Receipt', receipt, file_name=f'receipt_{datetime.now().strftime("%Y%m%d%H%M%S")}.txt')

    # Reset the order list after submission
    st.session_state.order = []
