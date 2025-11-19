import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

notion_token = os.getenv('NOTION_TOKEN')
database_id = os.getenv('NOTION_DATABASE_ID')

if not notion_token or not database_id:
    print("❌ Missing Notion credentials")
    exit(1)

notion = Client(auth=notion_token)

try:
    print("🔧 Setting up Notion database schema...")
    
    # Update database with required properties
    notion.databases.update(
        database_id,
        properties={
            "Name": {
                "title": {}
            },
            "Type": {
                "select": {
                    "options": [
                        {"name": "Search", "color": "blue"},
                        {"name": "News", "color": "green"},
                        {"name": "Summary", "color": "purple"},
                        {"name": "Comparison", "color": "orange"},
                        {"name": "Trend", "color": "red"},
                        {"name": "Research", "color": "pink"}
                    ]
                }
            },
            "Timestamp": {
                "created_time": {}
            }
        }
    )
    
    print("✅ Database schema updated successfully!")
    print("\n📋 Properties created:")
    print("  • Name (Title) - Main title/heading")
    print("  • Type (Select) - Content type (Search, News, Summary, etc.)")
    print("  • Timestamp (Created Time) - Auto timestamp")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Make sure your Notion integration has:")
    print("   1. Database access (in Notion settings)")
    print("   2. Edit permissions on the database")
