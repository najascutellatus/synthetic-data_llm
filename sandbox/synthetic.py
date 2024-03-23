# %%
from openai import OpenAI
import pandas as pd
import streamlit as st

# %%
# Your OpenAI API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# %%
def generate_synthetic_data_with_chat_model(domain, columns_format, n_records=10):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Ensure this is a chat model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate {n_records} synthetic records for {domain} with the following format: {list(columns_format.keys())}. This will be used in a MySQL database."}
        ])
        # Extracting and returning the generated text
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# %%
# Example usage
# Define the domain and columns format for the synthetic data generation
domain = "Healthcare patient records"
columns_format = {
    "First Name": "varchar(20)",
    "Last Name": "varchar(20)",
    "Age": "int(3)", 
    "DOB": "datetime", 
    "Diagnosis": "varchar(200)",
    "Gender": "boolean",
    "BloodType": "varchar(3)",
    "Allergies": "varchar(200)",
    "LastVisitDate": "datetime",
    "Medications": "varchar(200)"
}

# Generate synthetic data (ensure to replace 'your_openai_api_key_here' with your actual API key)
synthetic_data = generate_synthetic_data_with_chat_model(domain, columns_format, 10)

# Optionally, print or further process the synthetic data
print(synthetic_data)


# %%
# Function to convert generated data to pandas DataFrame
def convert_to_dataframe(raw_data, columns_format):
    # Split the raw data into lines and then into fields
    lines = raw_data.split('\n')
    data = [line.split(',') for line in lines if line.strip() != '']  # Assuming comma-separated values
    
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=columns_format.keys())
    
    # Convert types
    for column, dtype in columns_format.items():
        if dtype == 'int':
            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0).astype(int)
        elif dtype == 'datetime':
            df[column] = pd.to_datetime(df[column], errors='coerce')
        # Add more type conversions as needed
    
    return df

# %%
# Convert to DataFrame and adjust types
df = convert_to_dataframe(synthetic_data, columns_format)

# Save to CSV
df.to_csv('synthetic_healthcare_data.csv', index=False)

print("Synthetic data generated and saved to synthetic_healthcare_data.csv.")
