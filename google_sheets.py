import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def setup_google_sheets(credentials_file="credentials.json"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(credentials)
    return client

def fetch_and_clean_data(sheet):
    data = pd.DataFrame(sheet.get_all_records())
    grouped_data = data.groupby("Country", as_index=False).agg({
        "Visits": "sum",
        "Places": lambda x: ", ".join(sorted(set(", ".join(x).split(", ")))),
        "Total Number of Days": "sum"
    })
    result = grouped_data.merge(data[["Country", "Country Code", "Country Code 2"]].drop_duplicates(), on="Country", how="left")
    return result
