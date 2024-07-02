import streamlit as st
import pandas as pd
from datetime import date, datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO

# st.set_page_config(page_title="Store Management", layout="wide")

# File paths
PRODUCTS_FILE = 'products.csv'
LOG_FILE = 'transaction_log.txt'
STOCK_FILE = 'stock.csv'
USERS_FILE = 'users.csv'

# Load product data from CSV
if os.path.exists(PRODUCTS_FILE):
    products_df = pd.read_csv(PRODUCTS_FILE)
    products = products_df['product'].tolist()
    prices = products_df['price'].tolist()
else:
    products = ['Tomatoes 🍅', 'Potatoes 🥔', 'Carrots 🥕', 'Cucumber 🥒', 'Lettuce 🥬']
    prices = [1.5, 1.0, 0.8, 1.2, 0.9]
    products_df = pd.DataFrame({'product': products, 'price': prices})
    products_df.to_csv(PRODUCTS_FILE, index=False)

if os.path.exists(STOCK_FILE):
    stock_df = pd.read_csv(STOCK_FILE)
else:
    stock_df = pd.DataFrame({'product': products, 'stock': [100] * len(products)})
    stock_df.to_csv(STOCK_FILE, index=False)

if not os.path.exists(USERS_FILE):
    users_df = pd.DataFrame(columns=['username', 'password', 'loyalty', 'phone'])
    users_df.to_csv(USERS_FILE, index=False)

def save_products():
    df = pd.DataFrame({'product': products, 'price': prices})
    df.to_csv(PRODUCTS_FILE, index=False)

def save_stock():
    stock_df.to_csv(STOCK_FILE, index=False)

# Initialize session state
if 'order' not in st.session_state:
    st.session_state.order = []

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = 'login'

if 'username' not in st.session_state:
    st.session_state.username = ''

def authenticate(username, password):
    users_df = pd.read_csv(USERS_FILE)
    user = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
    return not user.empty

def signup(username, password, loyalty, phone):
    users_df = pd.read_csv(USERS_FILE)
    if username in users_df['username'].values:
        return False
    new_user = pd.DataFrame({'username': [username], 'password': [password], 'loyalty': [loyalty], 'phone': [phone]})
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv(USERS_FILE, index=False)
    return True

def add_product():
    if st.session_state.name == 'Other':
        product_name = st.session_state.custom_product_name
        product_price = st.session_state.custom_product_price
        if product_name not in products:
            products.append(product_name)
            prices.append(product_price)
            save_products()
            stock_df.loc[len(stock_df)] = [product_name, 100]
            save_stock()
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
    stock_index = stock_df[stock_df['product'] == product_name].index[0]
    if product['quantity'] > stock_df.at[stock_index, 'stock']:
        st.error(f"Not enough stock for {product_name}")
    else:
        stock_df.at[stock_index, 'stock'] -= product['quantity']
        st.session_state.order.append(product)
        save_stock()

def log_transaction(order):
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"Transaction at {timestamp}\n")
        for product in order:
            f.write(f"{product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {product['quantity'] * product['price']} $)\n")
        f.write("\n")

def create_receipt_pdf(order, loyalty_discount):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(90 * mm, 200 * mm))
    c.translate(mm, mm)

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

    c.line(5 * mm, 170 * mm, 85 * mm, 170 * mm)

    c.drawString(10 * mm, 165 * mm, "Servi par: mohammed - #1")
    c.drawString(10 * mm, 160 * mm, "Client: mohammed - #2")

    c.line(5 * mm, 155 * mm, 85 * mm, 155 * mm)

    y_position = 150
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
        y_position -= 10
        if y_position < 10:
            c.showPage()
            y_position = 190
            c.setFont("Courier", 8)

    if loyalty_discount:
        discount_amount = total_price * 0.2
        total_price -= discount_amount
        c.line(5 * mm, (y_position + 5) * mm, 85 * mm, (y_position + 5) * mm)
        c.setFont("Courier-Bold", 10)
        c.drawString(10 * mm, (y_position - 5) * mm, "LOYALTY DISCOUNT")
        c.drawRightString(82 * mm, (y_position - 5) * mm, f"-{discount_amount:.2f} $")
        y_position -= 20

    c.line(5 * mm, (y_position + 5) * mm, 85 * mm, (y_position + 5) * mm)

    c.setFont("Courier-Bold", 10)
    c.drawString(10 * mm, (y_position - 5) * mm, "TOTAL")
    c.drawRightString(82 * mm, (y_position - 5) * mm, f"{total_price:.2f} $")

    c.line(5 * mm, (y_position - 10) * mm, 85 * mm, (y_position - 10) * mm)

    y_position -= 20
    c.setFont("Courier", 8)
    c.drawString(10 * mm, (y_position - 5) * mm, "Payé en ESP - TVA incluse")
    c.drawString(10 * mm, (y_position - 15) * mm, "Merci de votre visite. À bientôt!")

    y_position -= 20
    c.setFont("Courier", 6)
    footer_text = "Lun - Ven 11h00-14h00 / 15h00-19h00\nSamedi 11h00 - 19h30\nwww.mbm.com\nFR00123456789 - RCS PARIS B 123456789"
    for line in footer_text.split('\n'):
        y_position -= 5
        c.drawString(10 * mm, (y_position - 5) * mm, line)

    c.save()
    buffer.seek(0)
    return buffer

def login_page():
    st.markdown(
        """
        <style>
        .login-page {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            width: 400px;
            margin: auto;
            margin-top: 100px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        .login-page h2 {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="login-page"><h2>Login</h2></div>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = 'main'
        else:
            st.error("Invalid username or password")
    st.markdown("Don't have an account? [Sign Up](#signup)", unsafe_allow_html=True)

def signup_page():
    st.markdown(
        """
        <style>
        .signup-page {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            width: 400px;
            margin: auto;
            margin-top: 100px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        .signup-page h2 {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="signup-page"><h2>Sign Up</h2></div>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    loyalty = st.checkbox("Join Loyalty Program")
    phone = st.text_input("Phone Number")
    if st.button("Sign Up"):
        if signup(username, password, loyalty, phone):
            st.success("Account created successfully! You can now log in.")
            st.session_state.page = 'login'
        else:
            st.error("Username already exists. Please choose a different username.")

def main_page():
    st.header("Store Management")
    st.subheader("Select Product and Quantity")
    product_name = st.selectbox("Product Name", options=products + ["Other"], key='name')
    if product_name == 'Other':
        custom_product_name = st.text_input("Enter custom product name", key='custom_product_name')
        custom_product_price = st.number_input("Enter custom product price", key='custom_product_price')
    how_many = st.number_input("How many kg?", min_value=0, key='how_many')
    order_date = st.date_input("Order Date", value=date.today(), key='date')
    if st.button("Add to Order"):
        add_product()
        st.session_state.how_many = 0

    st.subheader("Order Summary")
    total = 0.0
    for product in st.session_state.order:
        st.write(f"{product['name']} - {product['quantity']} kg @ {product['price']} $/kg on {product['date']}")
        total += product['quantity'] * product['price']
    st.write(f"Total: {total} $")

    users_df = pd.read_csv(USERS_FILE)
    current_user = users_df[users_df['username'] == st.session_state.username].iloc[0]
    loyalty_discount = False
    if current_user['loyalty']:
        st.write("Loyalty discount applied (20% off)")
        loyalty_discount = True
        total *= 0.8

    if st.button("Complete Order"):
        log_transaction(st.session_state.order)
        receipt_buffer = create_receipt_pdf(st.session_state.order, loyalty_discount)
        st.download_button(
            label="Download Receipt",
            data=receipt_buffer,
            file_name="receipt.pdf",
            mime="application/pdf"
        )
        st.session_state.order = []

if st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'signup':
    signup_page()
else:
    main_page()
