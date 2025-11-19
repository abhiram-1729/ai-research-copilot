import os
import json
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
notion_token = os.getenv('NOTION_TOKEN')
database_id = os.getenv('NOTION_DATABASE_ID')

if not notion_token:
    raise SystemExit('Missing NOTION_TOKEN')

notion = Client(auth=notion_token)

page_id = '2b0aed9c-062a-8112-9966-e2481572f411'
print('Retrieving page:', page_id)
try:
    p = notion.pages.retrieve(page_id)
    print(json.dumps(p, indent=2)[:4000])
    print('\nParent:', p.get('parent'))
    print('\nProperties keys:', list(p.get('properties', {}).keys()))
except Exception as e:
    print('Error retrieving page:', repr(e))
