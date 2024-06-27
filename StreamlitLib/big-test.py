import streamlit as st
import pandas as pd
import os
from datetime import date

# File paths
USERS_FILE = 'users.csv'
LOG_FILE = 'transaction_log.txt'
STOCK_FILE = 'stock.csv'

# Initial stock data
if not os.path.exists(STOCK_FILE):
    stock_df = pd.DataFrame({
        'product': ['Apples', 'Bananas', 'Oranges'],
        'stock': [100, 150, 200]
    })
    stock_df.to_csv(STOCK_FILE, index=False)
else:
    stock_df = pd.read_csv(STOCK_FILE)

# Load users data from CSV
if not os.path.exists(USERS_FILE):
    users_df = pd.DataFrame(columns=['username', 'password'])
    users_df.to_csv(USERS_FILE, index=False)

# Authentication functions
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

# Login and Signup pages
def login_page():
    st.markdown(
        """
        <style>
            .container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px;
            }
            .login-container, .signup-container {
                width: 48%;
                padding: 20px;
                background: #f9f9f9;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .login-container h2, .signup-container h2 {
                text-align: center;
                margin-bottom: 20px;
            }
            .login-container button, .signup-container button {
                width: 100%;
                padding: 10px;
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 10px;
            }
            .login-container button:hover, .signup-container button:hover {
                background: #45a049;
            }
        </style>
        <div class="container">
            <div class="login-container">
                <h2>Login</h2>
                <form action="" method="post">
                    <label for="username">Username</label>
                    <input type="text" id="login-username" name="username" placeholder="Your username..">
                    <label for="password">Password</label>
                    <input type="password" id="login-password" name="password" placeholder="Your password..">
                    <button type="button" onclick="login()">Login</button>
                </form>
            </div>
            <div class="signup-container">
                <h2>Sign Up</h2>
                <form action="" method="post">
                    <label for="username">Username</label>
                    <input type="text" id="signup-username" name="username" placeholder="Your username..">
                    <label for="password">Password</label>
                    <input type="password" id="signup-password" name="password" placeholder="Your password..">
                    <button type="button" onclick="signup()">Sign Up</button>
                </form>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Login'):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
            else:
                st.error("Incorrect username or password")
    with col2:
        if st.button('Sign Up'):
            if signup(username, password):
                st.success("User registered successfully")
            else:
                st.error("Username already exists")

# Command and Stock Management pages
def command_page():
    st.title('Command Page')

    products = ['Apples', 'Bananas', 'Oranges', 'Other']
    prices = [2.0, 1.5, 3.0]

    if 'order' not in st.session_state:
        st.session_state.order = []

    def add_product():
        if name == 'Other':
            product_name = st.session_state.custom_product_name
        else:
            product_name = name

        st.session_state.order.append({
            'name': product_name,
            'quantity': how_many,
            'date': date_input,
            'price': product_price
        })

    st.sidebar.header('Product Selection')
    name = st.sidebar.selectbox('Select a product', products, key='product_name')

    if name == 'Other':
        with st.sidebar.expander('Create a new product'):
            st.text_input('Enter new product name', key='custom_product_name')
            st.number_input('Enter new product price per kg', min_value=0.00, value=0.0, key='custom_product_price')

    st.sidebar.header('Admin Access')
    password = st.sidebar.text_input('Enter password', type='password')
    if st.sidebar.button('Download Transaction Log') and password == 'wewe':
        with open(LOG_FILE, 'rb') as file:
            st.sidebar.download_button('Download Log File', file, file_name='transaction_log.txt')

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
        st.write(f"**Total Price:** {total_price} $")

        buffer = create_receipt_pdf(st.session_state.order)
        st.download_button('Download Receipt PDF', buffer, file_name='receipt.pdf', mime='application/pdf')

        log_transaction(st.session_state.order)
        st.session_state.order = []

def stock_management_page():
    st.title('Stock Management')

    st.subheader('Stock Database')
    st.dataframe(stock_df)

    with st.form('Update Stock'):
        product = st.selectbox('Select Product', stock_df['product'].tolist())
        new_stock = st.number_input('Enter new stock quantity', min_value=0)
        update_button = st.form_submit_button('Update Stock')

    if update_button:
        stock_index = stock_df[stock_df['product'] == product].index[0]
        stock_df.at[stock_index, 'stock'] = new_stock
        stock_df.to_csv(STOCK_FILE, index=False)
        st.success(f"Stock updated for {product}")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    if not st.session_state.logged_in:
        login_page()
    else:
        st.sidebar.header('Navigation')
        page = st.sidebar.radio('Go to', ['Command', 'Stock Management'])
        if page == 'Command':
            command_page()
        elif page == 'Stock Management':
            stock_management_page()

if __name__ == '__main__':
    main()
