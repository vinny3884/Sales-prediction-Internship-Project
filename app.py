# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import pickle
import streamlit as st
import pandas as pd

# Load the saved ML model
with open("best_model.pkl", 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Function to make predictions
def predict_sales(data):
    return loaded_model.predict(data)

# Streamlit App
def main():
    st.title('Sales Prediction App')

    # Create input fields for user to enter data
    st.header('Enter Input Data:')
    product_name = st.text_input('Product Name')
    sub_category = st.selectbox('Select Sub-Category', ['Art', 'Bookcases', 'Binders','Copiers','Storage','Accessories','Supplies','Chairs','Labels','Phones','Envelopes'])
    country = st.selectbox('Select Country', ['Netherlands', 'Germany', 'France', 'Italy','United Kingdom','Belgium'])  
    ship_mode = st.selectbox('Select Ship Mode', ['Priority', 'Economy','Economy Plus'])  
    days_to_ship = st.number_input('Days to Ship', min_value=2, value=7)
    discount = st.number_input('Discount', min_value=0.0, max_value=0.5, step=0.05, value=0.5)
    actual_discount = st.number_input('Actual Discount', min_value=0.0, max_value=114.5, step=0.1, value=22.0)
    quantity = st.number_input('Quantity', min_value=1, max_value=8, value=3)
    
    
    # Add date input fields for Ship Date and Order Date
    st.write("Enter Ship Date and Order Date (YYYY-MM-DD):")
    ship_date_input = st.text_input("Ship Date")
    order_date_input = st.text_input("Order Date")

    # Function to extract datetime features from date strings
    def extract_datetime_features(date_str):
        if '-' in date_str:
           date = pd.to_datetime(date_str, format='%Y-%m-%d', errors='coerce')
           if not pd.isna(date):
               year = date.year
               day_of_year = date.dayofyear
               day_of_week = date.dayofweek
               return year, day_of_year, day_of_week
        return None, None, None

    # Extract datetime features for Ship Date and Order Date
    ship_year, ship_day_of_year, ship_day_of_week = extract_datetime_features(ship_date_input)
    order_year, order_day_of_year, order_day_of_week = extract_datetime_features(order_date_input)

    

    # Create a dataframe with user input
    input_data = pd.DataFrame({
        'Product Name': product_name,
        'Sub-Category': sub_category,
        'Country': [country],
        'Ship Mode': [ship_mode],
        'Days to Ship': [days_to_ship],
        'Discount': [discount],
        'Actual Discount': [actual_discount],
        'Quantity': [quantity],
        'Ship Year': [ship_year],
        'Ship Day of Year': [ship_day_of_year],
        'Ship Day of Week': [ship_day_of_week],
        'Order Year': [order_year],
        'Order Day of Year': [order_day_of_year],
        'Order Day of Week': [order_day_of_week]
    })

    # Make a prediction when the 'Predict' button is clicked
    if st.button('Predict'):
        prediction = predict_sales(input_data)
        st.success(f'Predicted Sales: {prediction[0]:.2f}')

if __name__ == '__main__':
    main()
