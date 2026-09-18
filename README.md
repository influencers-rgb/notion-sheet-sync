# Notion to Google Sheets Sync

A FastAPI service that receives Notion webhook events and synchronizes the affected page to Google Sheets.

## Requirements

- Python 3.10 or newer
- A Notion integration with access to the data source
- A Google service account with access to the target spreadsheet

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Copy your Google service-account JSON file to `credentials/google-service-account.json`.

4. Create a `.env` file with these values:

   ```env
   NOTION_TOKEN=your_notion_integration_token
   NOTION_DATA_SOURCE_ID=your_notion_data_source_id
   GOOGLE_SERVICE_ACCOUNT_FILE=credentials/google-service-account.json
   GOOGLE_SPREADSHEET_ID=your_google_spreadsheet_id
   GOOGLE_SHEET_NAME=TEST
   ```

The `.env` file and service-account credentials are intentionally excluded from Git.

## Run

Start the API with:

```powershell
uvicorn app.main:app --env-file .env --reload
```

The service provides:

- `GET /` for a service status response
- `GET /health` for a health check
- `POST /notion/webhook` for Notion webhook events

## Sync behavior

The webhook handler extracts a Notion page ID, reads the page properties, and inserts or updates the matching row in the configured Google Sheet. The sheet must include a `Notion Page ID` header.
