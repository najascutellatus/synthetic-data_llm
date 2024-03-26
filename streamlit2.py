import openai as OpenAI
import pandas as pd
import numpy as np
import streamlit as st
import os

# Set your OpenAI API key 
#OpenAI.api_key = os.getenv('OPENAI_API_KEY')

OpenAI.api_key=st.secrets["OPENAI_API_KEY"]

def generate_synthetic_data(domain, formatted_column_names, num_rows):
    
    try:
        response = OpenAI.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate {num_rows} synthetic records for {domain} with the following format: {formatted_column_names}. Please give output in a form that can be copied and pasted to create a csv file. This will be used in a MySQL database."}
        ])
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}")
        return None

st.title('Synthetic Data Generator')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
num_rows = st.number_input("Enter the number of rows for synthetic data", min_value=1, value=5)

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display the heading columns
    st.write("Heading Columns:", df.columns.tolist())
    
    st.title('Domain')
    domain = st.text_input("What is the domain?")

    if st.button('Generate Synthetic Data'):
        # Generate synthetic data based on column names
        
        column_names_list = df.columns.tolist()
        formatted_column_names = ", ".join(column_names_list) 
        
        synthetic_df = generate_synthetic_data(domain, formatted_column_names, num_rows)
        
        # Display the synthetic data table
        #st.write(synthetic_df)        
        st.markdown(synthetic_df)

        # following will show interactive table but it's not working for me
        #st.dataframe(synthetic_df)
        #st.table(synthetic_df)
        