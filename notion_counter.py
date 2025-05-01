import os
from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load .env
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATA_DB_ID = os.getenv("NOTION_DATABASE_ID")
TASK_DB_ID = os.getenv("NOTION_TASK_DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)

# Filters to Peloton Bike
filters = {
    "filter": {
        "property": "Tags",
        "multi_select": {
            "contains": "Peloton Bike"
        }
    }
}

def fetch_all_pages():
    pages = []
    start_cursor = None

    while True:
        response = notion.databases.query(
            database_id=DATA_DB_ID,
            start_cursor=start_cursor,
            **filters
        )
        pages.extend(response["results"])
        if not response.get("has_more"):
            break
        start_cursor = response.get("next_cursor")

    return pages

def create_task(message):
    due_time = (datetime.utcnow() + timedelta(minutes=5)).isoformat()

    notion.pages.create(
        parent={"database_id": TASK_DB_ID},
        properties={
            "Action Item": {
                "title": [{"text": {"content": f"🏆 {message} @{due_time}"}}]
            },
            "Do Date": {
                "date": {
                    "start": due_time
                }
            }
        }
    )
    print(f"🆕 Task created in Notion: 🏆 {message}")

def check_threshold(count):
    mod = count % 100
    if mod == 97:
        create_task("3 rides until milestone")
    elif mod == 98:
        create_task("2 rides until milestone")
    elif mod == 99:
        create_task("Next Ride is a Milestone!")
    else:
        print(f"✅ {count} rides — no task created.")

if __name__ == "__main__":
    # 👇 Manual test mode
    # check_threshold(397)

    # ✅ When ready for real data, comment out the line above and uncomment these:
    records = fetch_all_pages()
    count = len(records)
    check_threshold(count)