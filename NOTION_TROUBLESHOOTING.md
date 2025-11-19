# 🐛 Troubleshooting Notion Data Storage

## ✅ Your Notion Connection is Working!

I just verified locally that:
- ✅ Notion token is valid
- ✅ Notion database is accessible
- ✅ Pages can be created successfully
- ✅ Content can be added to pages

## 🔍 Why Data Might Not Be Saving on Streamlit Cloud

### Common Issues & Fixes

#### 1. **Auto-save Checkbox Not Checked** (Most Common)
- Open each tab (Search, News, Summarize, Compare, Trends)
- Make sure the "Auto-save to Notion (...)" checkbox is **checked** (✅)
- Run your action again

#### 2. **Notion Not Fully Initialized on Cloud**
The app shows "Notion: ❌ Not configured" in the sidebar
- Go to **Settings → Secrets** on your Streamlit app
- Make sure you have **ALL 4** keys:
  ```toml
  GEMINI_API_KEY = "..."
  SERPAPI_KEY = "..."
  NOTION_TOKEN = "..."
  NOTION_DATABASE_ID = "..."
  ```
- Click "Save" and wait for auto-reboot
- Check sidebar "Debug Info" - all 4 should show ✅

#### 3. **Check the Debug Info Panel**
Click "🔍 Debug Info" in the sidebar and verify:
- `GEMINI_API_KEY: ✅ Loaded`
- `SERPAPI_KEY: ✅ Loaded`
- `NOTION_TOKEN: ✅ Loaded`
- `NOTION_DATABASE_ID: ✅ Loaded`

If any show ❌, the secrets aren't being loaded properly.

#### 4. **Verify Notion Database Access**
The integration needs **explicit access** to the database:

1. Open your Notion database
2. Go to **Settings** (⚙️ icon)
3. Look for "Connections" or "Integrations"
4. Make sure "AI Research Copilot" integration is listed
5. If not listed, click "Connect to" and search for "AI Research Copilot"

#### 5. **Check the Database Has a "Name" Property**
The app creates pages with a "Name" property:

1. Open your Notion database
2. Click the database settings
3. Check that there's a "Name" property (this is usually the title field)
4. If missing, add it or rename an existing property to "Name"

### 🧪 Test Locally to Verify

```bash
# Run the test locally
python3 test_notion_connection.py
```

If this works locally, it confirms:
- Your credentials are valid
- The database is accessible
- The integration has permission
- Content can be created

### 📊 Monitor Streamlit Cloud Logs

1. Go to your Streamlit Cloud app
2. Click **⋮** (three dots) in top-right
3. Select **"Manage app"**
4. Click **"View logs"**
5. Look for messages like:
   - ✅ "Loaded secrets from Streamlit"
   - ❌ "NOTION_TOKEN loaded: False"
   - Error messages from Notion API

### 🔄 If Still Not Working

Try these steps in order:

1. **Hard refresh** — `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
2. **Check sidebar Debug Info** — Verify all keys are loaded
3. **Verify checkbox is checked** — Each tab has an "Auto-save" checkbox
4. **Check Notion database permissions** — Integration must have access
5. **Check Notion database has "Name" property** — Property structure matters
6. **Reboot the app** — Click "Reload Copilot" in sidebar
7. **View Streamlit logs** — Look for errors or confirmation messages

### 📝 What Gets Saved to Notion

When auto-save is enabled:
- **Title** — e.g., "Search: Python Programming"
- **Content** — Full search results, summary, or analysis
- **Timestamp** — When the page was created
- **Type** — search, news, summarize, compare, or trends

All saved to your configured Notion database.

### 💡 Pro Tips

- The first save might take 5-10 seconds (Notion initialization)
- Subsequent saves are faster (1-2 seconds)
- You can search your Notion database with the "Notion → Search" tab
- Pages are created immediately - check Notion app or web

---

**Still stuck?** Try running this locally to confirm everything works:
```bash
python3 test_notion_connection.py
```

Then check the Streamlit Cloud logs for any error messages.
