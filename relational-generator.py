import streamlit as st
import openai as OpenAI
import pandas as pd
import numpy as np
import json
import re
import zipfile
from io import BytesIO
import base64
import random

# Function to reset session state
def reset_state():
    for key in st.session_state.keys():
        del st.session_state[key]

# Initialize session state variables if they are not already initialized
if 'schema' not in st.session_state:
    st.session_state.schema = ""
if 'uploaded' not in st.session_state:
    st.session_state.uploaded = False
if 'tables_detected' not in st.session_state:
    st.session_state.tables_detected = False
if 'table_rows' not in st.session_state:
    st.session_state.table_rows = {}
if 'output_text' not in st.session_state:
    st.session_state.output_text = ""
    
# Function to decode the SQL or JSON file
def fileparser(definition_schema):
    content = definition_schema.getvalue().decode("utf-8")
    return content

# Function to detect tables in the schema
def detect_tables(schema):
    pattern = re.compile(r"CREATE TABLE\s+([a-zA-Z_][a-zA-Z0-9_]*)", re.IGNORECASE)
    tables = pattern.findall(schema)
    return tables

# # Function to call OpenAI API and generate synthetic data
# def openai_generator(schema, table_and_rows):
#     MAX_TOKENS = 4096
#     try:
#         response = OpenAI.chat.completions.create(model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful data analyst expert at generating synthetic data."},
#             {"role": "user", "content": f"Analyze the following schema - {schema}. The following are the specification for the number of rows for each table - {table_and_rows}. Generate only csv entries to populate the tables. Separate each csv file with --- and add name of csv file before the entries. Include a heading row. Do not include any additional text"}
#         ])
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#         return None
from io import StringIO
def openai_generator(schema, table_and_rows, chunk_size=100):
    MAX_TOKENS = 4096
    final_output = ""
    
    # Split table_and_rows into a dictionary
    table_rows_dict = {table.split(':')[0]: int(table.split(':')[1]) for table in table_and_rows.split(", ")}
    
    for table, rows_requested in table_rows_dict.items():
        rows_generated = 0
        table_tmp = []
        while rows_generated < rows_requested:
            # Determine how many rows to request in this chunk
            rows_to_generate = min(chunk_size, rows_requested - rows_generated)
            try:
                response = OpenAI.chat.completions.create(
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    top_p=0.9,
                    messages=[
                        {"role": "system", "content": "You are a helpful data analyst expert at generating synthetic data."},
                        {"role": "user", "content": f"Generating unique dataset {random.randint(1, 100000)}. Analyze the following schema - {schema}. Please generate {rows_to_generate} entries to populate the {table} table in valid CSV format with the correct header for each column. The data generated needs to be consistent with the foreign and primary keys. Do not include any additional text like 'certainly... here you go' or unnecessary characters, only response with the requested data."}
                    ]
                    )
                table_tmp.append(pd.read_csv(StringIO(response.choices[0].message.content)))
                # final_output += f"---\n{table}.csv\n" + chunk_output if final_output else chunk_output
                rows_generated += rows_to_generate
            except Exception as e:
                st.error(f"An error occurred: {e}")
                return None
        table_rows_dict[table] = pd.concat(table_tmp, ignore_index=True)
    
    return table_rows_dict

# Function to download generated data as a ZIP file
# def download_zip(output_text):
#     sections = [section.strip() for section in output_text.strip().split('---') if section]
#     zip_buffer = BytesIO()
#     with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
#         for section in sections:
#             title, *data = section.split('\n')
#             csv_content = '\n'.join(data)
#             zip_file.writestr(title, csv_content)
#     zip_buffer.seek(0)
#     return zip_buffer.getvalue()

import pandas as pd
from io import BytesIO
import zipfile

def download_zip(dataframes_dict):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for title, df in dataframes_dict.items():
            # Convert DataFrame to CSV format
            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_content = csv_buffer.getvalue().decode()
            # Write the CSV content to the ZIP file
            zip_file.writestr(f"{title}.csv", csv_content)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


# Streamlit app title
st.title("Relational Database Generator")
st.text("This webapp accepts a SQL schema and generates a synthetic database")

# Streamlit sidebar for file upload and reset functionality
with st.sidebar:
    uploaded_schema = st.file_uploader("Upload a SQL file", type=["sql", "json"])

    if uploaded_schema is not None:
        schema = fileparser(uploaded_schema)
        st.session_state.schema = schema
        st.session_state.uploaded = True

    if st.session_state.tables_detected:
        # chunks = st.number_input("Chunk size for data generation:", min_value=1, value=100, step=1)
        st.write("Detected tables and row configurations:")
        for table in st.session_state.tables:
            st.session_state.table_rows[table] = st.number_input(f"Number of rows for {table}:", min_value=0, value=st.session_state.table_rows[table], step=1, key=table)

    if st.session_state.tables_detected and st.button('Confirm Row Numbers'):
        table_and_rows = ", ".join([f"{table}: {st.session_state.table_rows[table]}" for table in st.session_state.tables])
        output_text = openai_generator(st.session_state.schema, table_and_rows)
        if output_text:
            st.session_state.output_text = output_text

    # Reset button
    if st.button("Reset"):
        reset_state()

if st.session_state.uploaded:
    st.text_area("Uploaded SQL Schema", value=st.session_state.schema, height=200, help="The SQL schema from your uploaded file.")

if st.session_state.uploaded and st.button("Detect Tables"):
    st.session_state.tables = detect_tables(st.session_state.schema)
    st.session_state.tables_detected = True
    for table in st.session_state.tables:
        st.session_state.table_rows[table] = 10
        
# Display generated data and download button
if st.session_state.get('output_text', ''):
    st.text_area("Synthetic Generated Database", value=st.session_state.output_text, height=400, help="Generated Database based on provided configuration.")
    zip_file = download_zip(st.session_state.output_text)
    st.download_button(
        label="Download Database as ZIP",
        data=zip_file,
        file_name="database.zip",
        mime='application/zip'
    )
