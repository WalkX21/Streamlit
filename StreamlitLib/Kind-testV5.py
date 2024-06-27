import streamlit as st
import pandas as pd
from datetime import date, datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO

st.title('Command 🍎')

# Paths to the files
PRODUCTS_FILE = 'products.csv'
LOG_FILE = 'transaction_log.txt'
STOCK_FILE = 'stock.csv'

# Load product data from CSV
if os.path.exists(PRODUCTS_FILE):
    products_df = pd.read_csv(PRODUCTS_FILE)
    products = products_df['product'].tolist()
    prices = products_df['price'].tolist()
else:
    # Predefined products and their prices
    products = ['Tomatoes 🍅', 'Potatoes 🥔', 'Carrots 🥕', 'Cucumber 🥒', 'Lettuce 🥬']
    prices = [1.5, 1.0, 0.8, 1.2, 0.9]

    products_df = pd.DataFrame({'product': products, 'price': prices})
    products_df.to_csv(PRODUCTS_FILE, index=False)

# Load stock data from CSV
if os.path.exists(STOCK_FILE):
    stock_df = pd.read_csv(STOCK_FILE)
    stock = stock_df.set_index('product')['stock'].to_dict()
else:
    stock = {product: 100 for product in products}  # Initial stock for each product
    stock_df = pd.DataFrame({'product': list(stock.keys()), 'stock': list(stock.values())})
    stock_df.to_csv(STOCK_FILE, index=False)

def save_products():
    df = pd.DataFrame({'product': products, 'price': prices})
    df.to_csv(PRODUCTS_FILE, index=False)

def save_stock():
    stock_df = pd.DataFrame({'product': list(stock.keys()), 'stock': list(stock.values())})
    stock_df.to_csv(STOCK_FILE, index=False)

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
            stock[product_name] = 100  # Initialize new product stock
            save_products()
            save_stock()
    else:
        product_name = st.session_state.name
        product_index = products.index(product_name)
        product_price = prices[product_index]

    if st.session_state.how_many > stock[product_name]:
        st.error(f"Cannot add {st.session_state.how_many} kg of {product_name}. Only {stock[product_name]} kg available in stock.")
        return

    product = {
        'name': product_name,
        'quantity': st.session_state.how_many,
        'date': st.session_state.date,
        'price': product_price
    }
    st.session_state.order.append(product)
    stock[product_name] -= st.session_state.how_many  # Update stock
    save_stock()

def log_transaction(order):
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H+1:%M:%S')
        f.write(f"Transaction at {timestamp}\n")
        for product in order:
            f.write(f"{product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {product['quantity'] * product['price']} $)\n")
        f.write("\n")

def create_receipt_pdf(order):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(90 * mm, 200 * mm))  # Receipt size in mm

    # Store details
    store_name = "MBMAGASIN"
    address = "01 place du Centre - 01234 MAVILLE "
    infos = "06 23 45 67 89 - contact@hiboutik.com"
    transaction_date = datetime.now().strftime("Le %d %B %Y  Ticket 001")

    c.setFont("Courier-Bold", 12)
    c.drawString(10 * mm, 190 * mm, store_name)
    c.setFont("Courier", 8)
    c.drawString(10 * mm, 185 * mm, address)
    c.drawString(10 * mm, 180 * mm, infos)

    c.drawString(10 * mm, 175 * mm, transaction_date)

    # Line separator
    c.line(5 * mm, 170 * mm, 85 * mm, 170 * mm)

    # Customer and server info
    c.drawString(10 * mm, 165 * mm, "Servi par: mohammed - #1")
    c.drawString(10 * mm, 160 * mm, "Client: mohammed - #2")

    # Line separator
    c.line(5 * mm, 155 * mm, 85 * mm, 155 * mm)

    y_position = 150  # Initial y position
    total_price = 0.0
    c.setFont("Courier", 8)
    for product in order:
        product_total = product['quantity'] * product['price']
        total_price += product_total
        text = f"{product['name']} - {product['quantity']} kg @ {product['price']} $/kg"
        c.drawString(10 * mm, y_position * mm, text)
        c.setFont('Courier-Bold', 10)
        c.drawRightString(82 * mm, y_position * mm, f"{product_total:.2f} $")
        c.setFont("Courier", 8)
        y_position -= 10  # Move to the next line
        if y_position < 10:  # Check if y_position is too low for the current page
            c.showPage()
            y_position = 190  # Reset y_position for the new page
            c.setFont("Courier", 8)

    # Line separator
    c.line(5 * mm, (y_position + 5) * mm, 85 * mm, (y_position + 5) * mm)

    # Total price
    c.setFont("Courier-Bold", 10)
    c.drawString(10 * mm, (y_position - 5) * mm, "TOTAL")
    c.drawRightString(82 * mm, (y_position - 5) * mm, f"{total_price:.2f} $")

    # Line separator
    c.line(5 * mm, (y_position - 10) * mm, 85 * mm, (y_position - 10) * mm)

    # Additional information
    y_position -= 20  # Ensure space between line and additional information
    c.setFont("Courier", 8)
    c.drawString(10 * mm, (y_position - 5) * mm, "Payé en ESP - TVA incluse")
    c.drawString(10 * mm, (y_position - 15) * mm, "Merci de votre visite. À bientôt!")

    # Footer
    y_position -= 20  # Ensure space between additional info and footer
    c.setFont("Courier", 6)
    footer_text = "Lun - Ven 11h00-14h00 / 15h00-19h00\nSamedi 11h00 - 19h30\nwww.mbm.com\nFR00123456789 - RCS PARIS B 123456789"
    for line in footer_text.split('\n'):
        y_position -= 5
        c.drawString(10 * mm, (y_position - 5) * mm, line)  # Adjust y_position for footer

    c.save()
    buffer.seek(0)
    return buffer

# Navigation
st.sidebar.header('Navigation')
page = st.sidebar.radio("Go to", ["Command", "Stock Management"])

if page == "Command":
    # Product selection
    st.sidebar.header('Product Selection')
    product_selection = products + ['Other']
    name = st.sidebar.selectbox('Which product', product_selection, key='name')

    # Other ==> let you create a new product
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

    # Frontend
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
            st.write(f"**Product {i + 1}:** {product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {round(product['quantity'] * product['price'], 2)} $)")

    # Submit the order
    if submit_button:
        st.subheader('Final Order')
        total_price = 0.0
        for i, product in enumerate(st.session_state.order):
            product_total = round(product['quantity'] * product['price'], 2)
            total_price += product_total
            st.write(f"**Product {i + 1}:** {product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {product_total} $)")
        st.write(f"**Total Price:** {total_price} $")

        buffer = create_receipt_pdf(st.session_state.order)
        st.download_button('Download Receipt PDF', buffer, file_name='receipt.pdf', mime='application/pdf')

        log_transaction(st.session_state.order)
        st.session_state.order = []

elif page == "Stock Management":
    st.header('Stock Management')

    # Display stock table
    stock_df = pd.DataFrame({'product': list(stock.keys()), 'price': prices, 'stock': list(stock.values())})
    st.table(stock_df)

    st.subheader('Add Stock')
    with st.form('Add Stock'):
        product_selection = products
        product_name = st.selectbox('Select product to add stock', product_selection, key='stock_product_name')
        add_stock_quantity = st.number_input('Add quantity to stock (kg)', min_value=0.00, value=0.0, key='add_stock_quantity')
        add_stock_button = st.form_submit_button('Add Stock')

    if add_stock_button:
        stock[product_name] += add_stock_quantity
        save_stock()
        st.success(f"Added {add_stock_quantity} kg to the stock of {product_name}. New stock: {stock[product_name]} kg")

    st.subheader('Reduce Stock')
    with st.form('Reduce Stock'):
        product_selection = products
        product_name = st.selectbox('Select product to reduce stock', product_selection, key='reduce_stock_product_name')
        reduce_stock_quantity = st.number_input('Reduce quantity from stock (kg)', min_value=0.00, value=0.0, key='reduce_stock_quantity')
        reduce_stock_button = st.form_submit_button('Reduce Stock')

    if reduce_stock_button:
        if reduce_stock_quantity <= stock[product_name]:
            stock[product_name] -= reduce_stock_quantity
            save_stock()
            st.success(f"Reduced {reduce_stock_quantity} kg from the stock of {product_name}. New stock: {stock[product_name]} kg")
        else:
            st.error(f"Cannot reduce {reduce_stock_quantity} kg from the stock of {product_name}. Only {stock[product_name]} kg available in stock.")
