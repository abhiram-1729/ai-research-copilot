# 🔧 Notion Database Property Fix

## Problem
```
⚠️ Database property mismatch. Ensure database has 'Name' property.
```

Your Notion database doesn't have a "Name" property, which is required for storing research data.

## Solution

### Step 1: Add the "Name" Property to Your Database

**Option A: Manual Setup (Recommended if integration lacks permissions)**
1. Go to your Notion database in your browser
2. Look at the top row where you see property names
3. Click the **`+`** button to add a new property
4. Name it: **`Name`**
5. Set type to: **`Title`**
6. Click "Done"

**Option B: Auto-Setup (If you have integration edit permissions)**
```bash
python3 setup_notion_database.py
```

### Step 2: Grant Integration Database Access (If Auto-Setup Fails)

If the auto-setup script fails, your integration needs explicit access:

1. **Open your Notion database** in a browser
2. Click **Share** (top right corner)
3. Scroll down to **"Connections"** section
4. Click **"+ Invite"**
5. Search for and select **"AI Research Copilot"** (or your integration name)
6. Confirm the invitation
7. Close the dialog

### Step 3: Verify the Setup

```bash
python3 check_notion_database.py
```

You should see:
```
📋 Available Properties:
  • Name: title
  • Type: select
  • Timestamp: created_time
```

### Step 4: Test It Works

Now go to your deployed Streamlit app:
1. Go to the **Search** tab
2. Enter a query (e.g., "AI")
3. **Check the "Auto-save to Notion" checkbox**
4. Click "Search"
5. Check your Notion database - the result should appear!

## Database Schema

Your app needs these properties (created automatically or manually):

| Property | Type | Purpose |
|----------|------|---------|
| **Name** | Title | Main heading (e.g., search query or topic) |
| **Type** | Select | Content type (Search, News, Summary, Comparison, Trend) |
| **Timestamp** | Created Time | Auto-generated timestamp |

## Troubleshooting

**Q: I added the Name property but data still doesn't save**
- Verify "Auto-save to Notion" checkbox is checked before running actions
- Check sidebar "Debug Info" - confirm Notion: ✅ appears

**Q: The setup script says it worked but properties don't appear**
- Your integration needs database access (see Step 2)
- Go to Notion database → Share → + Invite → select your integration

**Q: I don't see my integration in the Connections list**
- Create a new internal integration in Notion settings
- Or check that you're using the correct token in Streamlit secrets

