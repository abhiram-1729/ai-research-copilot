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

print('\n--- Retrieving database object ---')
try:
    db = notion.databases.retrieve(database_id)
    print('Database raw object (truncated):')
    print(json.dumps(db, indent=2)[:4000])
    print('\nDatabase id:', db.get('id'))
    print('Database title:', db.get('title'))
    print('Database parent:', db.get('parent'))
    props = db.get('properties', {})
    print('\nProperties count:', len(props))
    for k, v in props.items():
        print(' -', k, '->', v.get('type'))
except Exception as e:
    print('Error retrieving database:', repr(e))

print('\n--- Querying pages in database (first 10) ---')
try:
    res = notion.databases.query(database_id=database_id, page_size=10)
    results = res.get('results', [])
    print('Found pages:', len(results))
    for i, page in enumerate(results):
        pid = page.get('id')
        props = page.get('properties', {})
        title = None
        # attempt to extract title from common title property names
        for name in ['Name', 'name', 'Title', 'title']:
            if name in props:
                p = props[name]
                if p.get('type') == 'title':
                    title_arr = p.get('title', [])
                    if title_arr:
                        title = ''.join([t.get('plain_text','') for t in title_arr])
                        break
        print(i+1, pid, 'title:', title)
except Exception as e:
    print('Error querying database:', repr(e))

print('\n--- Attempting to create a test page in database ---')
try:
    test_page = notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {"title": [{"text": {"content": "Debug test page from script"}}]},
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"text": [{"type": "text", "text": {"content": "Diagnostic content."}}]}
            }
        ]
    )
    print('Created page id:', test_page.get('id'))
    print('Created page raw (truncated):')
    print(json.dumps(test_page, indent=2)[:2000])
except Exception as e:
    print('Error creating page:', repr(e))

print('\n--- Done ---')
