import os
import sys
from dotenv import load_dotenv

# Load from .env
load_dotenv()

print("Testing Notion connection...")
print(f"NOTION_TOKEN: {'✅ Found' if os.getenv('NOTION_TOKEN') else '❌ Missing'}")
print(f"NOTION_DATABASE_ID: {'✅ Found' if os.getenv('NOTION_DATABASE_ID') else '❌ Missing'}")

if not os.getenv('NOTION_TOKEN') or not os.getenv('NOTION_DATABASE_ID'):
    print("\n⚠️ Missing Notion credentials. Skipping test.")
    sys.exit(1)

try:
    from notion_client import Client
    notion = Client(auth=os.getenv('NOTION_TOKEN'))
    
    # Test database access
    db_id = os.getenv('NOTION_DATABASE_ID')
    result = notion.databases.retrieve(db_id)
    print(f"\n✅ Successfully connected to Notion database")
    print(f"Database title: {result.get('title', 'Unknown')}")
    
    # Try to create a test page
    test_page = notion.pages.create(
        parent={"database_id": db_id},
        properties={
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": "[TEST] AI Research Copilot"
                        }
                    }
                ]
            }
        }
    )
    print(f"✅ Test page created: {test_page['id']}")
    
    # Try to add content
    notion.blocks.children.append(
        block_id=test_page['id'],
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "This is a test page from AI Research Copilot"
                            }
                        }
                    ]
                }
            }
        ]
    )
    print(f"✅ Content added to test page")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    sys.exit(1)
