# Import python packages
import streamlit as st
import snowflake.snowpark.context
import requests
import pandas as pd

# Write directly to the app
st.title("🥤 Customize Your Smoothie!")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

# Text input for the customer's name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get the Snowflake session
session = snowflake.snowpark.context.get_active_session()

# Fetch fruits data from Snowflake
my_dataframe = session.sql("select FRUIT_NAME, FRUIT_ID from FRUITS_OPTIONS").to_pandas()
# st.dataframe(data=my_dataframe, use_container_width=True)

# Multiselect for choosing fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe['FRUIT_NAME']
    , max_selections=5
)

if ingredients_list:m
    st.write("You selected:", ingredients_list)
    st.text(ingredients_list)
    
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        search_on=my_dataframe.loc[my_dataframe['FRUIT_NAME'] == fruit_chosen, 'FRUIT_ID'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        
        # Call the Fruityvice API to get nutrition info
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com" + search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # Insert button
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
