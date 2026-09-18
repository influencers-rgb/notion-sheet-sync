import os
import requests


NOTION_TOKEN = os.environ["NOTION_TOKEN"]

NOTION_VERSION = "2025-09-03"


def notion_headers():

    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }


def get_page(page_id):

    url = f"https://api.notion.com/v1/pages/{page_id}"

    response = requests.get(
        url,
        headers=notion_headers(),
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def query_data_source():

    data_source_id = os.environ[
        "NOTION_DATA_SOURCE_ID"
    ]

    url = (
        "https://api.notion.com/v1/data_sources/"
        f"{data_source_id}/query"
    )

    response = requests.post(
        url,
        headers=notion_headers(),
        json={},
        timeout=30
    )

    response.raise_for_status()

    return response.json()