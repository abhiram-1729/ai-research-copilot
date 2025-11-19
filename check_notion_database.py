import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

notion_token = os.getenv('NOTION_TOKEN')
database_id = os.getenv('NOTION_DATABASE_ID')

if not notion_token or not database_id:
    print("Missing Notion credentials")
    exit(1)

notion = Client(auth=notion_token)

try:
    db = notion.databases.retrieve(database_id)
    print(f"\n📚 Database: {database_id}")
    print(f"\n📋 Available Properties:")
    print("-" * 50)
    
    properties = db.get('properties', {})
    for prop_name, prop_config in properties.items():
        prop_type = prop_config.get('type', 'unknown')
        print(f"  • {prop_name}: {prop_type}")
    
    print("\n" + "-" * 50)
    print(f"\nTotal properties: {len(properties)}")
    print(f"\nTitle/Name property types typically are: 'title', 'rich_text'")
    
except Exception as e:
    print(f"❌ Error: {e}")
