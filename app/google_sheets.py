import os

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]


def get_google_service():

    credentials = (
        Credentials
        .from_service_account_file(
            os.environ[
                "GOOGLE_SERVICE_ACCOUNT_FILE"
            ],
            scopes=SCOPES
        )
    )

    return build(
        "sheets",
        "v4",
        credentials=credentials
    )


def get_rows():

    service = get_google_service()

    spreadsheet_id = os.environ[
        "GOOGLE_SPREADSHEET_ID"
    ]

    sheet_name = os.environ[
        "GOOGLE_SHEET_NAME"
    ]

    result = (
        service
        .spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A:Z"
        )
        .execute()
    )

    return result.get("values", [])


def insert_row(row):

    service = get_google_service()

    spreadsheet_id = os.environ[
        "GOOGLE_SPREADSHEET_ID"
    ]

    sheet_name = os.environ[
        "GOOGLE_SHEET_NAME"
    ]

    return (
        service
        .spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A:Z",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={
                "values": [row]
            }
        )
        .execute()
    )


def update_row(row_number, row):

    service = get_google_service()

    spreadsheet_id = os.environ[
        "GOOGLE_SPREADSHEET_ID"
    ]

    sheet_name = os.environ[
        "GOOGLE_SHEET_NAME"
    ]

    return (
        service
        .spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=(
                f"{sheet_name}!"
                f"A{row_number}:Z{row_number}"
            ),
            valueInputOption="USER_ENTERED",
            body={
                "values": [row]
            }
        )
        .execute()
    )