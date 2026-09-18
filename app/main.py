from fastapi import FastAPI, Request

from app.sync import sync_page


app = FastAPI(
    title="Notion → Google Sheets Sync"
)


@app.get("/")
async def root():

    return {
        "service": "Notion → Google Sheets Sync",
        "status": "running"
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }


@app.post("/notion/webhook")
async def notion_webhook(
    request: Request
):

    body = await request.json()

    print("\n================================")
    print("NOTION WEBHOOK")
    print("================================")

    print(body)


    # Notion webhook payload structure can
    # contain the affected page information.
    #
    # We'll inspect the actual payload during
    # the first webhook test.

    page_id = None


    if body.get("data"):

        data = body["data"]

        page_id = data.get("page_id")


        if not page_id:

            entity = data.get(
                "entity",
                {}
            )

            page_id = entity.get(
                "id"
            )


    if page_id:

        try:

            result = sync_page(
                page_id
            )

            print(
                "SYNC RESULT:",
                result
            )

            return {
                "status": "success",
                "result": result
            }

        except Exception as error:

            print(
                "SYNC ERROR:",
                str(error)
            )

            return {
                "status": "error",
                "message": str(error)
            }


    return {
        "status": "received",
        "message": "No page ID in webhook payload"
    }