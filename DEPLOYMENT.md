# 🚀 Deployment Checklist for Streamlit Cloud

## Before Deploying

- [ ] Code is committed and pushed to GitHub (`main` branch)
- [ ] All dependencies are in `requirements.txt`
- [ ] `.env` file is **NOT** in `.gitignore` (secrets will be added in Streamlit Cloud instead)
- [ ] `streamlit.toml` is configured correctly

## Streamlit Cloud Setup

### Step 1: Connect to GitHub
1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click "New app" → Select your repo and branch (`main`)
4. Set main file path: `app.py`

### Step 2: Add Secrets
1. Click the ⚙️ gear icon (Settings) in the top-right
2. Click "Secrets"
3. **Paste these secrets exactly** (use the format below):

```toml
GEMINI_API_KEY = "sk-your-actual-key-here"
SERPAPI_KEY = "your-actual-key-here"
NOTION_TOKEN = "ntn_your-actual-token-here"
NOTION_DATABASE_ID = "your-actual-database-id-here"
```

### Step 3: Deploy
1. Click "Deploy" button
2. Wait for the app to initialize (typically 2-5 minutes on first load)

## If App is Still Loading/Stuck

### Quick Fixes
1. **Hard refresh the page** — `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
2. **Check app status** — Look for error messages in the sidebar
3. **Check Secrets** — Go to Settings → Secrets and verify all keys are present
4. **Reboot the app** — Click the "Reload Copilot" button in the sidebar

### Debug Steps
1. Open **Streamlit logs**:
   - Click "⋮" (three dots) in top-right
   - Select "Manage app" → "View logs"
2. Look for these messages:
   - ✅ `Initialization error` — Check your secrets
   - ✅ `GEMINI_API_KEY not configured` — Add the key to secrets
   - ✅ `SerpAPI not configured` — Add SERPAPI_KEY to secrets

### Common Issues

| Issue | Fix |
|-------|-----|
| App loads forever | Check secrets in Settings → verify all keys are present |
| "Copilot not initialized" error | Secrets are missing or incorrectly formatted |
| "Search" button not working | SerpAPI key missing or invalid |
| "Notion save" fails | Check NOTION_TOKEN and NOTION_DATABASE_ID format |

## Environment Variables Reference

| Variable | Where to Get | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | [ai.google.dev](https://ai.google.dev/) | ✅ Yes |
| `SERPAPI_KEY` | [serpapi.com](https://serpapi.com/) | ✅ Yes |
| `NOTION_TOKEN` | [notion.so/my-integrations](https://www.notion.so/my-integrations) | ❌ Optional |
| `NOTION_DATABASE_ID` | Your Notion database URL | ❌ Optional |

## Testing After Deployment

1. **Search Tab** — Try a search query (e.g., "Python programming")
2. **News Tab** — Try fetching news (e.g., "AI breakthroughs")
3. **Summarize Tab** — Paste some text and summarize
4. **History Tab** — Check that activities are recorded

## Performance Tips

- First load takes 20-30 seconds (Gemini model initialization)
- Subsequent requests are faster (cached)
- Each search/news query takes 3-5 seconds (SerpAPI latency)

## Still Having Issues?

1. **Check Streamlit Cloud status** — [status.streamlit.io](https://status.streamlit.io)
2. **Restart the app** — "Manage app" → "Reboot app"
3. **Check GitHub repo** — Ensure latest code is pushed to main branch
4. **Delete and redeploy** — Sometimes a clean deploy helps

---

**Need help?** Check the main [GITHUB_README.md](../GITHUB_README.md) for more details.
