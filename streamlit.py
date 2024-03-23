import streamlit as st
from openai import OpenAI
import pandas as pd
import re

# Streamlit app layout
st.title("Synthetic Data Generator")

# Initialize OpenAI client with API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Regular expression to match lines starting with a number and a dot
line_pattern = re.compile(r'^\d+\.\s+\[.*\]$')

# Function to generate synthetic data
def generate_synthetic_data_with_chat_model(domain, columns_format, n_records=10):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate {n_records} synthetic records for {domain} with the following format: {list(columns_format.keys())}. This will be used in a MySQL database."}
        ])
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}")
        return None

# Sidebar for user inputs
st.sidebar.title("Settings")
domain = st.sidebar.text_input("Domain", value="Healthcare patient records")
columns_format_str = st.sidebar.text_area("Columns Format", value="First Name: varchar(20), Last Name: varchar(20), Age: int(3), DOB: datetime, Diagnosis: varchar(200), Gender: boolean, BloodType: varchar(3), Allergies: varchar(200), LastVisitDate: datetime, Medications: varchar(200)")
n_records = st.sidebar.number_input("Number of Records", min_value=1, value=10)

# Button in the sidebar
if st.sidebar.button("Generate Synthetic Data"):
    columns_format = {}
    try:
        for item in columns_format_str.split(','):
            key, value = item.split(':')
            columns_format[key.strip()] = value.strip()
    except Exception as e:
        st.sidebar.error("Invalid columns format. Please use the format: Column Name: data_type")
    else:
        synthetic_data = generate_synthetic_data_with_chat_model(domain, columns_format, n_records)
        if synthetic_data:
            # Parsing the synthetic data into a list of lists
            data_list = []
            for line in synthetic_data.split('\n'):
                if line_pattern.match(line):
                    # Extracting the list from the string
                    record = line.split('. ')[1]
                    # Evaluating the string representation of the list to a list
                    record_list = eval(record)
                    data_list.append(record_list)

                    # Use the keys from columns_format as your columns
                    columns = list(columns_format.keys())
                    # columns = ['First Name', 'Last Name', 'Age', 'DOB', 'Diagnosis', 'Gender', 'BloodType', 'Allergies', 'LastVisitDate', 'Medications']

                    # Creating a DataFrame
                    df = pd.DataFrame(data_list, columns=columns)
                    df

            # Display synthetic data in the main area
            st.write("Generated Synthetic Data:")
            st.dataframe(df, width=1000)

