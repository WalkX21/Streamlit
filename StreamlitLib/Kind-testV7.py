import streamlit as st
import pandas as pd
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO

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
    users_df = pd.DataFrame(columns=['username', 'password'])
    users_df.to_csv(USERS_FILE, index=False)

def save_products():
    df = pd.DataFrame({'product': products, 'price': prices})
    df.to_csv(PRODUCTS_FILE, index=False)

def save_stock():
    stock_df.to_csv(STOCK_FILE, index=False)

if 'order' not in st.session_state:
    st.session_state.order = []

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = 'login'

def authenticate(username, password):
    users_df = pd.read_csv(USERS_FILE)
    user = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
    return not user.empty

def signup(username, password):
    users_df = pd.read_csv(USERS_FILE)
    if username in users_df['username'].values:
        return False
    new_user = pd.DataFrame({'username': [username], 'password': [password]})
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

def create_receipt_pdf(order):
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
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80vh;
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 20px;
        }
        .login-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .login-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .login-input {
            margin-bottom: 10px;
            width: 100%;
        }
        .login-button {
            width: 100%;
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        .login-button:hover {
            background-color: #0056b3;
        }
        .signup-link {
            margin-top: 10px;
            font-size: 14px;
            color: #007bff;
            cursor: pointer;
        }
        </style>
        """, unsafe_allow_html=True
    )
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Login</div>', unsafe_allow_html=True)
    username = st.text_input("Username", key="login_username", value="", help="Enter your username")
    password = st.text_input("Password", type="password", key="login_password", value="", help="Enter your password")
    login_button = st.button("Login", key="login_button", class_="login-button")

    if login_button:
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.page = 'home'
        else:
            st.error("Invalid username or password")
    
    st.markdown('<div class="signup-link" onClick="window.location.reload();">Sign up</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

def signup_page():
    st.markdown(
        """
        <style>
        .signup-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80vh;
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 20px;
        }
        .signup-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .signup-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .signup-input {
            margin-bottom: 10px;
            width: 100%;
        }
        .signup-button {
            width: 100%;
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        .signup-button:hover {
            background-color: #218838;
        }
        .login-link {
            margin-top: 10px;
            font-size: 14px;
            color: #007bff;
            cursor: pointer;
        }
        </style>
        """, unsafe_allow_html=True
    )
    st.markdown('<div class="signup-container">', unsafe_allow_html=True)
    st.markdown('<div class="signup-box">', unsafe_allow_html=True)
    st.markdown('<div class="signup-title">Sign Up</div>', unsafe_allow_html=True)
    username = st.text_input("Username", key="signup_username", value="", help="Choose a username")
    password = st.text_input("Password", type="password", key="signup_password", value="", help="Choose a password")
    signup_button = st.button("Sign Up", key="signup_button", class_="signup-button")

    if signup_button:
        if signup(username, password):
            st.success("User registered successfully! Please log in.")
            st.session_state.page = 'login'
        else:
            st.error("Username already exists")
    
    st.markdown('<div class="login-link" onClick="window.location.reload();">Log in</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

if st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'signup':
    signup_page()
else:
    st.sidebar.title("MBMAGASIN")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = 'login'

    st.title("Order Entry")

    col1, col2 = st.columns(2)

    with col1:
        st.date_input("Delivery Date", key="date")
        st.selectbox("Product", options=products + ["Other"], key="name")

        if st.session_state.name == 'Other':
            st.text_input("Enter Product Name", key="custom_product_name")
            st.number_input("Enter Product Price ($/kg)", key="custom_product_price")

        st.number_input("Quantity (kg)", min_value=0.0, step=0.1, key="how_many")

    with col2:
        st.button("Add Product to Order", on_click=add_product)
        st.button("Reset Order", on_click=lambda: st.session_state.update(order=[]))

        st.subheader("Current Order")
        total_cost = 0.0
        for item in st.session_state.order:
            st.write(f"{item['name']}: {item['quantity']} kg @ ${item['price']} $/kg on {item['date']}")
            total_cost += item['quantity'] * item['price']
        st.write(f"**Total Cost: ${total_cost}**")

        if st.button("Log Transaction and Create Receipt"):
            log_transaction(st.session_state.order)
            pdf_buffer = create_receipt_pdf(st.session_state.order)
            st.session_state.order = []

            st.success("Transaction logged and receipt created.")
            st.download_button(
                label="Download Receipt",
                data=pdf_buffer,
                file_name="receipt.pdf",
                mime="application/pdf"
            )

   
