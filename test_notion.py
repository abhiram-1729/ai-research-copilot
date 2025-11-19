#!/usr/bin/env python3
"""
Test script to verify Notion integration is working.
Run this after sharing the database with your integration.
"""

import os
from dotenv import load_dotenv
from notion_client import Client

# Load environment variables
load_dotenv()

token = os.getenv('NOTION_TOKEN')
db_id = os.getenv('NOTION_DATABASE_ID')

print("🧪 Notion Integration Test")
print("=" * 60)

if not token or not db_id:
    print("❌ Missing credentials in .env file")
    exit(1)

try:
    client = Client(auth=token)
    print("✅ Notion client connected")
    
    # Try to access database
    db = client.databases.retrieve(db_id)
    print("✅ Database accessible!")
    
    # Try to create a test page
    page = client.pages.create(
        parent={"database_id": db_id},
        properties={
            "Name": {
                "title": [{"text": {"content": "✅ Test Page - Python Integration Works!"}}]
            }
        }
    )
    print("✅ Test page created successfully!")
    print(f"   Page URL: https://notion.so/{page['id']}")
    
    # Archive the test page
    client.pages.update(page['id'], archived=True)
    print("✅ Test page archived")
    
    print("\n" + "=" * 60)
    print("✅ NOTION IS FULLY OPERATIONAL!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n📝 SETUP INSTRUCTIONS:")
    print("1. Go to your Notion database:")
    print(f"   https://www.notion.so/{db_id}")
    print("2. Click Share (top-right)")
    print("3. Find and invite your integration")
    print("4. Make sure it has Edit permissions")
    print("5. Run this test again")
