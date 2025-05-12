import pandas as pd
import re

def normalize_columns(df):
    """
    Normalize column names by:
    - Converting to lowercase
    - Removing spaces and replacing with underscores
    - Removing special characters
    """
    df.columns = df.columns.str.strip().str.lower()
    df.columns = df.columns.str.replace(' ', '_', regex=True)
    df.columns = df.columns.str.replace(r'[^a-z0-9_]', '_', regex=True)
    return df

def process_excel(file):
    """
    Process an Excel file:
    - Read the file using pandas
    - Normalize column names
    - Return data as a list of dictionaries
    """
    df = pd.read_excel(file)
    df = normalize_columns(df)
    return df.to_dict(orient="records") 