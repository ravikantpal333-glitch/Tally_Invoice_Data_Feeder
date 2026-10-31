
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

credentials = Credentials.from_service_account_file(
    "credentials/service_account.json",
    scopes=SCOPES
)

client = gspread.authorize(credentials)

spreadsheet = client.open_by_key(
    "1m0ojOjsw1gseERRl-ESIPuTSlQRD6iPM1wfjIgeH2Rk"
)

worksheet = spreadsheet.worksheet("Invoice_Data")

print("Google Sheet connected successfully!")

# Check column headers
print("Headers:", worksheet.row_values(1))
