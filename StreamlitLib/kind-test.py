
import streamlit as st
from datetime import date

st.title('Commandes 🍎🍆')

# Initialize session state to store products and custom product entries
if 'products' not in st.session_state:
    st.session_state.products = []
if 'custom_products' not in st.session_state:
    st.session_state.custom_products = []

# Function to add a product
def add_product():
    if st.session_state.name == 'Other':
        product_name = st.session_state.custom_product_name
    else:
        product_name = st.session_state.name

    product = {
        'name': product_name,
        'quantity': st.session_state.how_many,
        'date': st.session_state.date,
        'time': st.session_state.time
    }
    st.session_state.products.append(product)

# Function to add a custom product to the custom products list
def add_custom_product():
    st.session_state.custom_products.append(st.session_state.new_custom_product)
    st.session_state.new_custom_product = ''  # Reset the input field

# Sidebar product selection
st.sidebar.header('Product Selection')
name = st.sidebar.selectbox(
    'Which product',
    ('Tomatoes 🍅', 'Potatoes 🥔', 'Carrots 🥕', 'Cucumber 🥒', 'Lettuce 🥬', 'Other'),
    key='name'
)

# If 'Other' is selected, show the expander for custom product creation
if name == 'Other':
    with st.sidebar.expander('Create a new product'):
        st.text_input('Enter new product name', key='new_custom_product')
        st.button('Add Product', on_click=add_custom_product)

    # Update the name selectbox to include custom products
    name = st.sidebar.selectbox(
        'Select a product',
        st.session_state.custom_products,
        key='custom_product_name'
    )

# Feedback Form
with st.form('Feedback_Form'):
    st.header('Add a Product')

    col1, col2 = st.columns(2)
    with col1:
        how_many = st.number_input('How much (qt in kg)', min_value=0.00, max_value=10.00, value=0.0, key='how_many')
    with col2:
        date = st.date_input('Enter Date', value=date.today(), key='date')
        time = st.radio('Select time to nearest label time', ('7.30', '7.45', '8.00', '8.10', '8.15'), key='time')

    add_another = st.form_submit_button('Add Another Product', on_click=add_product)
    submit_button = st.form_submit_button('Submit Order')

# Display current products added
if st.session_state.products:
    st.subheader('Current Order')
    for i, product in enumerate(st.session_state.products):
        st.write(f"**Product {i + 1}:** {product['name']} - {product['quantity']} kg on {product['date']} at {product['time']}")

# Submit order
if submit_button:
    st.subheader('Final Order')
    for i, product in enumerate(st.session_state.products):
        st.write(f"**Product {i + 1}:** {product['name']} - {product['quantity']} kg on {product['date']} at {product['time']}")
    # Reset the products list after submission
    st.session_state.products = []
