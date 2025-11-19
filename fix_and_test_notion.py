import os
import json
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
notion_token = os.getenv('NOTION_TOKEN')
database_id = os.getenv('NOTION_DATABASE_ID')

print('NOTION_TOKEN present:', bool(notion_token))
print('NOTION_DATABASE_ID present:', bool(database_id))

if not notion_token or not database_id:
    print('Missing token or database id, aborting')
    raise SystemExit(1)

notion = Client(auth=notion_token)

# Retrieve DB
print('\n--- Retrieve DB ---')
try:
    db = notion.databases.retrieve(database_id)
    print('DB id:', db.get('id'))
    props = db.get('properties', {})
    print('Properties before update:', list(props.keys()), 'count=', len(props))
except Exception as e:
    print('Error retrieving DB:', repr(e))

# Attempt update and print response
print('\n--- Update DB properties ---')
try:
    resp = notion.databases.update(
        database_id,
        properties={
            "Name": {"title": {}},
            "Type": {"select": {"options": [{"name":"Search","color":"blue"}, {"name":"News","color":"green"}] }},
            "Timestamp": {"created_time": {}}
        }
    )
    print('Update response (truncated):')
    print(json.dumps(resp, indent=2)[:3000])
except Exception as e:
    print('Error updating DB:', repr(e))

# Retrieve again
print('\n--- Retrieve DB after update ---')
try:
    db2 = notion.databases.retrieve(database_id)
    props2 = db2.get('properties', {})
    print('Properties after update:', list(props2.keys()), 'count=', len(props2))
except Exception as e:
    print('Error retrieving DB after update:', repr(e))

# Attempt to create page with correct paragraph.rich_text
print('\n--- Create test page ---')
try:
    test_page = notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {"title": [{"text": {"content": "Fix-test page from script"}}]}
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Diagnostic content."}}
                    ]
                }
            }
        ]
    )
    print('Created page id:', test_page.get('id'))
except Exception as e:
    print('Error creating page:', repr(e))

# Search for pages using notion.search (filter pages and match parent.database_id)
print('\n--- Search pages via notion.search ---')
try:
    search_resp = notion.search(filter={"property":"object","value":"page"}, page_size=50)
    results = search_resp.get('results', [])
    print('Total pages found by search:', len(results))
    matched = 0
    for p in results:
        parent = p.get('parent', {})
        if parent.get('database_id') == database_id:
            matched += 1
            title = None
            props = p.get('properties', {})
            if 'Name' in props and props['Name'].get('type') == 'title':
                title_arr = props['Name'].get('title', [])
                if title_arr:
                    title = ''.join([t.get('plain_text','') for t in title_arr])
            print(' - Found page id:', p.get('id'), 'title:', title)
    print('Pages matched to DB:', matched)
except Exception as e:
    print('Error searching pages:', repr(e))

print('\n--- Debug run complete ---')
