import streamlit as st
import pandas as pd
from datetime import date, datetime
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
OFFERS_FILE = 'offers.csv'

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

if not os.path.exists(OFFERS_FILE):
    offers_df = pd.DataFrame(columns=['offer_type', 'x_value', 'y_value'])
    offers_df.to_csv(OFFERS_FILE, index=False)

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

def log_transaction(order, discount):
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"Transaction at {timestamp}\n")
        for product in order:
            f.write(f"{product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {product['quantity'] * product['price']} $)\n")
        if discount > 0:
            f.write(f"Discount applied: -{discount:.2f} $\n")
        f.write("\n")

def create_receipt_pdf(order, total_price, discount):
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

    if discount > 0:
        c.line(5 * mm, (y_position - 10) * mm, 85 * mm, (y_position - 10) * mm)
        y_position -= 20
        c.setFont("Courier-Bold", 10)
        c.drawString(10 * mm, (y_position - 5) * mm, "DISCOUNT")
        c.drawRightString(82 * mm, (y_position - 5) * mm, f"-{discount:.2f} $")
        y_position -= 10
        c.line(5 * mm, (y_position - 10) * mm, 85 * mm, (y_position - 10) * mm)
        y_position -= 20
        final_total = total_price - discount
        c.setFont("Courier-Bold", 10)
        c.drawString(10 * mm, (y_position - 5) * mm, "FINAL TOTAL")
        c.drawRightString(82 * mm, (y_position - 5) * mm, f"{final_total:.2f} $")

    y_position -= 20
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
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80vh;
        }
        .stButton > button {
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title('Welcome Back')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Login'):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.page = 'command'
                st.session_state.username = username
            else:
                st.error("Incorrect username or password")
    with col2:
        if st.button('Sign Up'):
            st.session_state.page = 'signup'

def signup_page():
    st.markdown(
        """
        <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80vh;
        }
        .stButton > button {
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title('Sign Up')
    username = st.text_input('Username', key='signup_username')
    password = st.text_input('Password', type='password', key='signup_password')
    confirm_password = st.text_input('Confirm Password', type='password', key='confirm_password')
    loyalty = st.checkbox('Participate in Loyalty Program')
    phone = st.text_input('Phone Number') if loyalty else ''
    if password == confirm_password:
        if st.button('Register'):
            if signup(username, password, loyalty, phone):
                st.success("User registered successfully")
                st.session_state.page = 'login'
            else:
                st.error("Username already exists")
    else:
        st.error("Passwords do not match")

def command_page():
    st.title('Command')

    st.sidebar.header('Product Selection')
    product_selection = products + ['Other']
    name = st.sidebar.selectbox('Which product', product_selection, key='name')

    if name == 'Other':
        with st.sidebar.expander('Create a new product'):
            st.text_input('Enter new product name', key='custom_product_name')
            st.number_input('Enter new product price per kg', min_value=0.00, value=0.0, key='custom_product_price')

    st.sidebar.header('Admin Access')
    password = st.sidebar.text_input('Enter password', type='password')
    
    if st.sidebar.button('Go'):
        if password == 'wewe':
            st.session_state.is_admin = True

    if 'is_admin' in st.session_state and st.session_state.is_admin:
        st.sidebar.button('Admin Page', on_click=lambda: st.session_state.update(page='admin'))

    with st.form('Command'):
        st.header('Add a Product')

        col1, col2 = st.columns(2)
        with col1:
            how_many = st.number_input('How much (qt in kg)', min_value=0.00, max_value=10.00, value=0.0, key='how_many')
        with col2:
            date_input = st.date_input('Enter Date', value=date.today(), key='date')

            if name != 'Other':
                product_index = products.index(name)
                product_price = prices[product_index]
                st.write(f'Price per kg: {product_price} $')
            else:
                product_price = st.session_state.custom_product_price
                st.write(f'Price per kg: {product_price} $')

            if st.session_state.logged_in:
                users_df = pd.read_csv(USERS_FILE)
                user = users_df[users_df['username'] == st.session_state.username].iloc[0]
                if user['loyalty']:
                    st.write('**Loyalty Program Member**')
                    offer = get_current_offer()
                    if offer['offer_type'] == 'percentage':
                        st.write(f"**Offer: {offer['x_value']}% off on orders above {offer['y_value']} kg!**")
                    else:
                        st.write(f"**Offer: {offer['x_value']}$ off on orders above {offer['y_value']} kg!**")

        add_another = st.form_submit_button('Add Another Product', on_click=add_product)
        submit_button = st.form_submit_button('Submit Order')

    if st.session_state.order:
        st.subheader('Current Order')
        for i, product in enumerate(st.session_state.order):
            st.write(f"**Product {i + 1}:** {product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {round(product['quantity'] * product['price'], 2)} $)")

    if submit_button:
        st.subheader('Final Order')
        total_price = 0.0
        for i, product in enumerate(st.session_state.order):
            product_total = round(product['quantity'] * product['price'], 2)
            total_price += product_total
            st.write(f"**Product {i + 1}:** {product['name']} - {product['quantity']} kg on {product['date']} with price of {product['price']} $/kg (Total: {product_total} $)")

        users_df = pd.read_csv(USERS_FILE)
        user = users_df[users_df['username'] == st.session_state.username].iloc[0]
        discount = 0.0
        if user['loyalty']:
            offer = get_current_offer()
            if offer['offer_type'] == 'percentage' and total_price > offer['y_value']:
                discount = total_price * (offer['x_value'] / 100)
                st.write(f"**Discount ({offer['x_value']}% off):** -{round(discount, 2)} $")
            elif offer['offer_type'] == 'money' and total_price > offer['y_value']:
                discount = offer['x_value']
                st.write(f"**Discount ({offer['x_value']}$ off):** -{round(discount, 2)} $")
            total_price -= discount

        st.write(f"**Total Price:** {round(total_price, 2)} $")

        buffer = create_receipt_pdf(st.session_state.order, total_price, discount)
        st.download_button('Download Receipt PDF', buffer, file_name='receipt.pdf', mime='application/pdf')

        log_transaction(st.session_state.order, discount)
        st.session_state.order = []

def stock_management_page():
    st.title('Stock Management')

    st.subheader('Stock Database')
    st.table(stock_df)

    with st.form('Update Stock'):
        product = st.selectbox('Select Product', products)
        new_stock = st.number_input('Enter new stock quantity', min_value=0)
        update_button = st.form_submit_button('Update Stock')

    if update_button:
        stock_index = stock_df[stock_df['product'] == product].index[0]
        stock_df.at[stock_index, 'stock'] = new_stock
        save_stock()
        st.success(f"Stock updated for {product}")

def settings_page():
    st.title('Settings')
    users_df = pd.read_csv(USERS_FILE)
    user = users_df[users_df['username'] == st.session_state.username].iloc[0]

    st.subheader('Profile Information')
    new_username = st.text_input('Username', user['username'])
    loyalty = st.checkbox('Participate in Loyalty Program', user['loyalty'])
    phone = st.text_input('Phone Number', user['phone']) if loyalty else ''

    if st.button('Update Profile'):
        users_df.loc[users_df['username'] == user['username'], 'username'] = new_username
        users_df.loc[users_df['username'] == user['username'], 'loyalty'] = loyalty
        if loyalty:
            users_df.loc[users_df['username'] == user['username'], 'phone'] = phone
        users_df.to_csv(USERS_FILE, index=False)
        st.success("Profile updated successfully")

def admin_page():
    st.title("Admin Page")
    st.write("Welcome to the admin page!")

    st.sidebar.button('Exit Admin Page', on_click=lambda: st.session_state.update(page='command'))

    st.subheader("Modify Product Prices")
    product_to_update = st.selectbox("Select Product", products)
    new_price = st.number_input("Enter new price", min_value=0.0, value=prices[products.index(product_to_update)])
    if st.button("Update Price"):
        prices[products.index(product_to_update)] = new_price
        save_products()
        st.success(f"Price updated for {product_to_update}")

    st.subheader("Manage Offers")
    offer_type = st.selectbox("Offer Type", ['percentage', 'money'])
    x_value = st.number_input(f"Enter {'percentage' if offer_type == 'percentage' else 'amount'} value")
    y_value = st.number_input("Enter minimum quantity")
    if st.button("Create/Update Offer"):
        offers_df = pd.DataFrame({'offer_type': [offer_type], 'x_value': [x_value], 'y_value': [y_value]})
        offers_df.to_csv(OFFERS_FILE, index=False)
        st.success("Offer created/updated successfully")

def get_current_offer():
    if os.path.exists(OFFERS_FILE):
        offers_df = pd.read_csv(OFFERS_FILE)
        if not offers_df.empty:
            return offers_df.iloc[0]
    return {'offer_type': 'none', 'x_value': 0, 'y_value': 0}

def main():
    if not st.session_state.logged_in:
        if st.session_state.page == 'login':
            login_page()
        elif st.session_state.page == 'signup':
            signup_page()
    else:
        st.sidebar.header('Navigation')
        page = st.sidebar.radio('Go to', ['Command', 'Stock Management', 'Settings'])

        if st.session_state.page == 'admin':
            admin_page()
        elif page == 'Command':
            st.session_state.page = 'command'
            command_page()
        elif page == 'Stock Management':
            st.session_state.page = 'stock_management'
            stock_management_page()
        elif page == 'Settings':
            st.session_state.page = 'settings'
            settings_page()

if __name__ == '__main__':
    main()
