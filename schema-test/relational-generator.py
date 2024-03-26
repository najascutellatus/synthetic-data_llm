import streamlit as st
import openai as OpenAI
import pandas as pd
import numpy as np

OpenAI.api_key=st.secrets["OPENAI_API_KEY"]

def fileparser(definition_schema):
    # this method decodes the sql file
    content = definition_schema.getvalue().decode("utf-8")
    return content

def generate_sql_populator(sql_schema):
    #returns an sql file for populating
    try:
        response = OpenAI.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful data analyst expert at SQL."},
            {"role": "user", "content": f"Given the following SQL schema, generate SQL INSERT statements to populate the tables with synthetic data:\n\n{sql_schema}\n\n"}
        ])
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.write(f"An error occurred: {e}")



# Streamlit Webapp
st.title("Relational Database Generator")
st.text("this webapp accepts a SQL schema and generates a synthetic database")

definition_schema = st.file_uploader("Upload a SQL file", type="sql")

if definition_schema is not None:
    sql_schema = fileparser(definition_schema)
    st.text_area("Uploaded SQL Schema", value=sql_schema, height=200, help="The SQL schema from your uploaded file.")
    if st.button("Generate Synthetic Data"):
        sql_populator = generate_sql_populator(sql_schema)
        st.text_area("Synthetic SQL Data", value=sql_populator, height=400, help="Synthetic SQL INSERT statements generated based on the schema.")
