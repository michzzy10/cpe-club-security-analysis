import requests
import pandas as pd

# ---------------------------------------------------------
# PHASE 1: DATA GATHERING (Using the requests module)
# ---------------------------------------------------------
def fetch_data(url, save_path):
    print(f"Attempting to download data from: {url}...")
    
    try:
        # We send a GET request to the URL
        response = requests.get(url)
        
        # Check if the download was successful (HTTP 200 OK)
        if response.status_code == 200:
            # We open a new local file in 'write binary' (wb) mode and save the data
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print("Success: Data downloaded and saved locally!")
            return True
        else:
            print(f"Error: Server returned status code {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        # This catches network errors (like if FUTO's Wi-Fi drops out during the download)
        print(f"Network Error occurred: {e}")
        return False

# ---------------------------------------------------------
# PHASE 2: DATA CLEANING (Using Pandas)
# ---------------------------------------------------------
def clean_data(file_path):
    print("\n--- Initializing Pandas Cleaning Pipeline ---")
    
    try:
        # Load the CSV into a Pandas DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("Error: Could not find the raw CSV file to clean.")
        return

    # 1. Drop rows that don't have State or LGA data (they are useless for our spatial analysis)
    df = df.dropna(subset=['State', 'LGA'])
    
    # 2. Fix the fatalities column (Fill blanks with 0, then convert to whole numbers)
    df['fatalities'] = df['fatalities'].fillna(0).astype(int)
    
    # 3. Standardize Date format (Turns "12-May-2023" text into actual time data)
    df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce')
    
    # 4. Clean the State names (Makes everything lowercase, then Capitalizes the first letters)
    # This fixes issues where some entries say "lagos" and others say "Lagos State"
    df['State'] = df['State'].str.lower().str.replace(' state', '').str.title()
    
    # Check our work by printing the first 5 rows and the new data info
    print("\nData Cleaning Complete! Here is a preview:")
    print(df[['event_date', 'State', 'LGA', 'fatalities']].head())
    
    # Save the cleaned data to a new file so Matplotlib can use it next week!
    cleaned_path = 'cleaned_conflict_data.csv'
    df.to_csv(cleaned_path, index=False)
    print(f"\nCleaned dataset saved as: {cleaned_path}")

# ---------------------------------------------------------
# EXECUTION TRIGGER
# ---------------------------------------------------------
if __name__ == "__main__":
    # Note: Replace this dummy URL with the actual API link the CPE Club gave you!
    API_URL = "https://raw.githubusercontent.com/datasets/dummy-acled-data/main/data.csv"
    RAW_FILE = "raw_conflict_data.csv"
    
    # Run the download
    download_success = fetch_data(API_URL, RAW_FILE)
    
    # If the download worked, immediately run the cleaning pipeline
    if download_success:
        clean_data(RAW_FILE)