# ⚡ Quick Setup for Streamlit Cloud

Your app is now deployed! Follow these steps to add your API keys and get it working.

## Step 1: Get Your API Keys

Before configuring secrets, you need API keys from:

1. **Google Gemini** (Required)
   - Go to: https://ai.google.dev/
   - Click "Get API Key"
   - Create a new key → Copy it

2. **SerpAPI** (Required for web search)
   - Go to: https://serpapi.com/
   - Sign up and get your API key from dashboard

3. **Notion** (Optional, for saving to Notion)
   - Go to: https://www.notion.so/my-integrations
   - Create a new integration
   - Copy the token
   - Find your database ID from the database URL: `https://notion.so/workspace/[DATABASE_ID]?v=...`

## Step 2: Add Secrets to Streamlit Cloud

1. Go to your deployed app on Streamlit Cloud
2. Click the **⚙️ Settings** button (top-right corner)
3. Click **Secrets** in the left sidebar
4. Paste this template and fill in your actual keys:

```toml
GEMINI_API_KEY = "paste-your-gemini-key-here"
SERPAPI_KEY = "paste-your-serpapi-key-here"
NOTION_TOKEN = "paste-your-notion-token-here"
NOTION_DATABASE_ID = "paste-your-notion-database-id-here"
```

5. Click **Save**
6. Streamlit will automatically reboot your app

## Step 3: Verify It Works

1. Wait 30-60 seconds for the app to reboot
2. Refresh the page (⌘+R or Ctrl+R)
3. Check the sidebar "Debug Info" section — all 4 keys should show ✅
4. Try running a search or summarize

## Troubleshooting

**App still showing "Copilot not initialized"?**
- Check the sidebar Debug Info section to see which keys are missing
- Go back to Settings → Secrets and verify the format is correct
- Make sure there are spaces around the `=` sign
- Try clicking "Reload Copilot" button

**Keys not loading?**
- Copy-paste from the `.env.example` file to ensure correct format
- Don't include quotes inside the quotes (just paste the raw key)
- If you get an error, check the format matches exactly:
  ```
  KEY_NAME = "value-without-extra-quotes"
  ```

## That's It! 🎉

Your app should now be fully functional. You can:
- ✅ Search the web in real-time
- ✅ Fetch latest news
- ✅ Summarize text with AI
- ✅ Compare concepts
- ✅ Analyze trends
- ✅ Save everything to Notion (if configured)

Happy researching! 🚀
