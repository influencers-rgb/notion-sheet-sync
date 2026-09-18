from datetime import datetime, timezone

from app.notion import get_page
from app.google_sheets import (
    get_rows,
    insert_row,
    update_row
)


def text_value(prop):

    items = prop.get("title", [])

    if not items:
        items = prop.get("rich_text", [])

    return "".join(
        item.get("plain_text", "")
        for item in items
    )


def select_value(prop):

    value = prop.get("select")

    if value:
        return value.get("name", "")

    return ""


def status_value(prop):

    value = prop.get("status")

    if value:
        return value.get("name", "")

    return ""


def people_value(prop):

    people = prop.get("people", [])

    return ", ".join(
        person.get("name", "")
        for person in people
        if person.get("name")
    )


def multi_select_value(prop):

    values = prop.get("multi_select", [])

    return " → ".join(
        item.get("name", "")
        for item in values
        if item.get("name")
    )


def date_value(prop):

    value = prop.get("date")

    if value:
        return value.get("start", "")

    return ""


def email_value(prop):

    return prop.get("email") or ""


def url_value(prop):

    return prop.get("url") or ""


def get_prop(properties, name):

    return properties.get(name, {})


def build_row(page):

    properties = page.get(
        "properties",
        {}
    )

    return [

        text_value(
            get_prop(
                properties,
                "Lead / Company"
            )
        ),

        status_value(
            get_prop(
                properties,
                "Sales Stage"
            )
        ),

        select_value(
            get_prop(
                properties,
                "Priority"
            )
        ),

        people_value(
            get_prop(
                properties,
                "Sales Owner"
            )
        ),

        date_value(
            get_prop(
                properties,
                "Call Date"
            )
        ),

        select_value(
            get_prop(
                properties,
                "Call Status"
            )
        ),

        text_value(
            get_prop(
                properties,
                "Next Action"
            )
        ),

        text_value(
            get_prop(
                properties,
                "Blocked / Missing"
            )
        ),

        people_value(
            get_prop(
                properties,
                "Next Action Owner"
            )
        ),

        multi_select_value(
            get_prop(
                properties,
                "Stage History - New"
            )
        ),

        select_value(
            get_prop(
                properties,
                "Source"
            )
        ),

        people_value(
            get_prop(
                properties,
                "Call Owner"
            )
        ),

        text_value(
            get_prop(
                properties,
                "Contact"
            )
        ),

        email_value(
            get_prop(
                properties,
                "Contact Email"
            )
        ),

        url_value(
            get_prop(
                properties,
                "Granola Notes"
            )
        ),

        date_value(
            get_prop(
                properties,
                "Last Contact"
            )
        ),

        text_value(
            get_prop(
                properties,
                "Notes"
            )
        ),

        date_value(
            get_prop(
                properties,
                "Next Follow-up"
            )
        ),

        select_value(
            get_prop(
                properties,
                "Service"
            )
        ),

        date_value(
            get_prop(
                properties,
                "Next Action Due"
            )
        ),

        page.get(
            "id",
            ""
        ),

        page.get(
            "created_time",
            ""
        ),

        page.get(
            "last_edited_time",
            ""
        ),

        "SUCCESS",

        datetime.now(
            timezone.utc
        ).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        ),

        ""

    ]


def sync_page(page_id):

    page = get_page(page_id)

    row = build_row(page)

    notion_page_id = row[20]

    if not row[0]:

        return {
            "action": "skipped",
            "reason": "empty page",
            "page_id": notion_page_id
        }


    rows = get_rows()

    if not rows:

        raise Exception(
            "TEST sheet has no header row"
        )


    headers = rows[0]

    notion_id_column = headers.index(
        "Notion Page ID"
    )


    existing_row = None

    for row_number, sheet_row in enumerate(
        rows[1:],
        start=2
    ):

        if len(sheet_row) > notion_id_column:

            if (
                sheet_row[notion_id_column]
                == notion_page_id
            ):

                existing_row = row_number

                break


    if existing_row:

        update_row(
            existing_row,
            row
        )

        return {
            "action": "updated",
            "row": existing_row,
            "lead": row[0],
            "page_id": notion_page_id
        }


    insert_row(row)

    return {
        "action": "inserted",
        "lead": row[0],
        "page_id": notion_page_id
    }