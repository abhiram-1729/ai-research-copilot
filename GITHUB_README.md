# 🔬 AI Research Copilot

> A futuristic, multi-agent AI research assistant with real-time web search, Notion integration, and intelligent summarization powered by Google Gemini.

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features ✨

- **🌐 Real-Time Web Search** — Powered by SerpAPI for live, up-to-date search results
- **🤖 AI-Powered Analysis** — Google Gemini 2.0 Flash for intelligent content generation and summarization
- **📚 Notion Integration** — Auto-save research, summaries, and insights directly to your Notion database
- **🔍 Advanced Comparison** — Compare concepts, analyze trends, and extract key differences
- **📝 Smart Summarization** — Condense long-form content into actionable summaries
- **💾 Session History** — Track all research activities with timestamps and save status
- **🎨 Futuristic UI** — Modern glassmorphism design with neon accents and Orbitron typography
- **🚀 Multi-Tab Workflow** — Organize research by task (Search, News, Summarize, Compare, Trends)

## Architecture 🏗️

The project consists of two main components:

```
ai-research-copilot/
├── research_copilot.py       # Core logic (ResearchCopilot base class + AdvancedResearchCopilot)
├── app.py                    # Streamlit web UI with futuristic styling
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

### Core Classes

- **`ResearchCopilot`** — Base class with:
  - Gemini API integration (text generation)
  - SerpAPI web search (live data)
  - Notion client setup and page creation
  - Search result parsing and formatting
  - CLI-based interactive mode

- **`AdvancedResearchCopilot`** (extends `ResearchCopilot`) — Advanced features:
  - `compare_concepts()` — Compare two topics with real-time data
  - `analyze_research_trends()` — Trend analysis and future predictions
  - Inherits all base functionality

## Getting Started 🚀

### Prerequisites

- Python 3.9+
- API keys for:
  - [Google Gemini API](https://ai.google.dev/)
  - [SerpAPI](https://serpapi.com/) (for real-time web search)
  - [Notion](https://www.notion.so/integrations) (optional, for Notion integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-research-copilot.git
   cd ai-research-copilot
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` with your API keys:
   ```env
   GEMINI_API_KEY=sk-...
   SERPAPI_KEY=...
   NOTION_TOKEN=ntn_...
   NOTION_DATABASE_ID=your_database_id
   ```

### Running the App

**Web UI (Streamlit)**
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`

**CLI Mode (Interactive)**
```bash
python3 research_copilot.py
```

## Usage 📖

### Web UI Workflow

1. **Research Tab** — Full end-to-end research workflow:
   - Enter a topic
   - Toggle real-time search and auto-save to Notion
   - Get existing research + new findings + AI summary

2. **Search Tab** — Web search with optional Notion save:
   - Search the web in real-time
   - View results and analysis
   - Save to Notion with one click

3. **News Tab** — Latest news on a topic:
   - Fetch timely news articles
   - Auto-save headlines and summaries

4. **Summarize Tab** — Condense long text:
   - Paste text or content
   - Get AI-powered summary
   - Save to Notion

5. **Compare Tab** — Analyze two concepts:
   - Enter two topics
   - Get detailed comparison with real-time data
   - Optional Notion save

6. **Trends Tab** — Future-focused analysis:
   - Analyze research trends for a topic
   - Get predictions and emerging areas
   - Optional Notion save

7. **Notion Tab** — Direct Notion tools:
   - Search your Notion database
   - Manually create Notion pages

8. **History Tab** — Session tracking:
   - View all research activities
   - See timestamps and Notion save status
   - Clear session history

### CLI Commands

```
research [topic]              # Complete research workflow
search [query]                # Web search only
news [query]                  # Search latest news
summarize [content]           # Summarize text
compare [c1] vs [c2]          # Compare concepts
trends [topic]                # Analyze trends
notion search [query]         # Search Notion
notion create [title] | [content]  # Create Notion page
history                       # Show session history
status                        # Show API status
quit                          # Exit
```

## Configuration 🔧

### Environment Variables (`.env`)

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | ✅ Yes |
| `SERPAPI_KEY` | SerpAPI key for web search | ✅ Yes |
| `NOTION_TOKEN` | Notion integration token | ❌ Optional |
| `NOTION_DATABASE_ID` | Notion database ID | ❌ Optional |

### Notion Setup

1. Create a [Notion Integration](https://www.notion.so/my-integrations)
2. Create or duplicate a Notion database
3. Share the database with your integration
4. Copy the database ID from the database URL:
   ```
   https://notion.so/workspace/DATABASE_ID?v=...
   ```
5. Add credentials to `.env`

## Project Structure 📁

```
ai-research-copilot/
├── research_copilot.py          # Core application (700+ lines)
│   ├── ResearchCopilot          # Base class
│   │   ├── __init__()
│   │   ├── web_search_tool()
│   │   ├── search_news_only()
│   │   ├── summarize_research()
│   │   ├── create_notion_page()
│   │   ├── search_notion()
│   │   ├── research_workflow()
│   │   └── interactive_mode()
│   └── AdvancedResearchCopilot  # Extended class
│       ├── compare_concepts()
│       └── analyze_research_trends()
├── app.py                       # Streamlit UI (400+ lines)
│   ├── Futuristic CSS injection
│   ├── Sidebar with API status
│   ├── 8 main tabs (Research, Search, News, etc.)
│   └── Session state management
├── requirements.txt             # Python dependencies
├── .env.example                 # Template for environment variables
└── README.md                    # Documentation
```

## Dependencies 📦

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `google-generativeai` | Gemini API client |
| `notion-client` | Notion API integration |
| `requests` | HTTP client for SerpAPI |
| `serpapi` | Real-time search API |
| `python-dotenv` | Environment variable management |

See `requirements.txt` for pinned versions.

## Key Features in Detail 🎯

### Auto-Save to Notion
Every search, news fetch, summary, comparison, and trend analysis can auto-save to Notion. Each entry includes:
- Title
- Full content/results
- Timestamp
- Tags (for filtering)

### Real-Time Data
- SerpAPI provides live search results, news, and related searches
- No cached or simulated results (unless SerpAPI is unavailable)
- Full URLs, snippets, and metadata for each result

### AI Analysis
- Google Gemini 2.0 Flash model for:
  - Structured search result analysis
  - Content summarization
  - Concept comparison
  - Trend prediction
- Context-aware prompts for high-quality outputs

### Session Tracking
- All activities logged in `conversation_history`
- Timestamps, Notion save status, query details
- History viewable and clearable from UI

## Performance Tips ⚡

- **Disable real-time search** if SerpAPI quota is low (uses Gemini simulation)
- **Batch Notion saves** — limit auto-save to important items
- **Use summarize** on large documents to reduce processing time
- **Clear history** periodically to keep the session lightweight

## Troubleshooting 🔧

### "Notion integration unavailable"
- Verify `NOTION_TOKEN` and `NOTION_DATABASE_ID` in `.env`
- Check that the integration has access to the database (Notion settings → Connections)
- Ensure the database has a `Name` property (used as page title)

### "SerpAPI not configured"
- Add `SERPAPI_KEY` to `.env`
- App will fall back to Gemini simulation if SerpAPI is unavailable

### "Streamlit DuplicateElementId" error
- Clear Streamlit cache: `streamlit cache clear`
- Restart the app: `Ctrl+C` then re-run `streamlit run app.py`

### "Import errors" on startup
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt --upgrade`

## Deployment 🌐

### Streamlit Cloud
1. Push repo to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo
4. Add secrets in the app settings:
   - `GEMINI_API_KEY`
   - `SERPAPI_KEY`
   - `NOTION_TOKEN`
   - `NOTION_DATABASE_ID`
5. Deploy!

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t ai-research-copilot .
docker run -e GEMINI_API_KEY=$GEMINI_API_KEY -p 8501:8501 ai-research-copilot
```

## Contributing 🤝

Contributions are welcome! Here's how to help:

1. **Fork** the repository
2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```
3. **Make your changes**
   - Follow PEP 8 style guide
   - Add docstrings to new functions
   - Update `README.md` if adding features
4. **Test your changes**
   ```bash
   python3 -m pytest tests/
   ```
5. **Commit with clear messages**
   ```bash
   git commit -m "feat: add new feature"
   ```
6. **Push and open a Pull Request**

### Areas for Contribution
- [ ] Add support for additional LLMs (OpenAI, Anthropic)
- [ ] Implement vector databases for semantic search
- [ ] Add export formats (PDF, Markdown, CSV)
- [ ] Create mobile-friendly responsive UI
- [ ] Build advanced filtering/tagging in History
- [ ] Add test suite (unit + integration tests)
- [ ] Optimize SerpAPI queries for cost savings
- [ ] Implement multi-language support

## Roadmap 🗺️

- [ ] **v1.1** — PDF/Markdown export, custom Notion templates
- [ ] **v1.2** — Vector embeddings and semantic comparison
- [ ] **v1.3** — Multi-user collaboration with session sharing
- [ ] **v2.0** — Mobile app, offline mode, advanced analytics

## License 📄

MIT License — See [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- [Google Gemini API](https://ai.google.dev/) for powerful LLM capabilities
- [SerpAPI](https://serpapi.com/) for real-time search
- [Notion API](https://developers.notion.com/) for seamless database integration
- [Streamlit](https://streamlit.io/) for beautiful web UI

## Support & Feedback 💬

- **Issues** — Report bugs via [GitHub Issues](https://github.com/yourusername/ai-research-copilot/issues)
- **Discussions** — Ask questions in [GitHub Discussions](https://github.com/yourusername/ai-research-copilot/discussions)
- **Email** — Contact via your-email@example.com

---

**Made with ❤️ by Abhiram Rangoon**

*Last Updated: November 2025*
