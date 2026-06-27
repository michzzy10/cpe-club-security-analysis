import requests
import pandas as pd
import json

def fetch_data(save_path):
    print("Attempting to log in and download ACLED data...")
    session = requests.Session()
    login_url = "https://acleddata.com/user/login?_format=json"
    
    # Using your credentials
    credentials = {
        "name": "ubaezuonuchinonso.20241429893@futo.edu.ng",
        "pass": "a6F!gVaernuD@7_"
    }
    
    try:
        login_response = session.post(login_url, json=credentials)
        
        if login_response.status_code == 200:
            print("Login Successful! Session created.")
            
            # We accept the JSON response now!
            data_url = "https://acleddata.com/api/acled/read?limit=1000&country=Nigeria"
            
            data_response = session.get(data_url)
            
            if data_response.status_code == 200:
                # 1. Parse the JSON response
                raw_json = data_response.json()
                
                # 2. Extract the actual records (ACLED usually stores rows inside a "data" or "data" key)
                # If it's directly a list, we use that. If it's a dictionary, we pull out the "data" part.
                if isinstance(raw_json, dict) and "data" in raw_json:
                    records = raw_json["data"]
                else:
                    records = raw_json
                
                # 3. Use Pandas to instantly convert that JSON list into a proper CSV format!
                temp_df = pd.DataFrame(records)
                temp_df.to_csv(save_path, index=False)
                
                print("Success: JSON translated to CSV and saved locally!")
                return True
            else:
                print(f"Error fetching data: {data_response.status_code}")
                return False
        else:
            print(f"Login Failed: Status {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def clean_data(file_path):
    print("\n--- Initializing Pandas Cleaning Pipeline ---")
    
    # 1. Load the freshly downloaded (and now properly translated) CSV data
    df = pd.read_csv(file_path)
    
    # Force column headers to lowercase
    df.columns = df.columns.str.lower()
    print("Available columns:", list(df.columns))
    
    # 2. Map ACLED's standard headers (admin1, admin2) to our context
    # If the API gave us 'state' directly, we map it too just to be safe
    df = df.rename(columns={
        'admin1': 'State',
        'admin2': 'LGA',
        'state': 'State',
        'lga': 'LGA'
    })
    
    print("Standardized column names...")

    # 3. Drop rows that don't have State or LGA data
    # (We use a list comprehension to only drop if the columns exist to prevent KeyError)
    check_cols = [col for col in ['State', 'LGA'] if col in df.columns]
    if len(check_cols) == 2:
        df = df.dropna(subset=['State', 'LGA'])
    else:
        print(f"Warning: Could not find State or LGA columns. Current columns are: {df.columns}")
        return
    
    # 4. Fix the fatalities column
    if 'fatalities' in df.columns:
        df['fatalities'] = pd.to_numeric(df['fatalities'], errors='coerce').fillna(0).astype(int)
    
    # 5. Standardize Date format
    if 'event_date' in df.columns:
        df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce')
    
    # 6. Clean the State names uniformity
    df['State'] = df['State'].astype(str).str.lower().str.replace(' state', '').str.title()
    
    # Preview the clean data
    print("\nData Cleaning Complete! Here is a preview:")
    columns_to_show = [col for col in ['event_date', 'State', 'LGA', 'fatalities'] if col in df.columns]
    print(df[columns_to_show].head())
    
    # Save the output file
    cleaned_path = 'cleaned_conflict_data.csv'
    df.to_csv(cleaned_path, index=False)
    print(f"\nCleaned dataset saved as: {cleaned_path}")

# ---------------------------------------------------------
# EXECUTION TRIGGER
# ---------------------------------------------------------
if __name__ == "__main__":
    RAW_FILE = "raw_conflict_data.csv"
    
    if fetch_data(RAW_FILE):
        clean_data(RAW_FILE)