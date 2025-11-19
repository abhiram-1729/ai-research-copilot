# AI Research Copilot

A futuristic, multi-agent AI research assistant with real-time web search, Notion integration, and intelligent summarization powered by Google Gemini.

## Quick Start

1. **Clone & Setup**
   ```bash
   git clone <repo-url>
   cd ai-research-copilot
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure API Keys**
   ```bash
   cp .env.example .env
   # Edit .env with your GEMINI_API_KEY, SERPAPI_KEY, and optionally NOTION_TOKEN
   ```

3. **Run the App**
   ```bash
   streamlit run app.py
   ```
   Open http://localhost:8501](https://ai-research-copilot-x7q6g2yqupmztiqyu4q3sg.streamlit.app/

## Features

- 🌐 Real-time web search (SerpAPI)
- 🤖 AI-powered analysis (Gemini 2.0)
- 📚 Notion integration with auto-save
- 🔍 Concept comparison & trend analysis
- 📝 Smart summarization
- 🎨 Futuristic UI with glassmorphism
- 💾 Session history & tracking

## Full Documentation

For complete setup, features, deployment, and contribution guidelines, see [GITHUB_README.md](GITHUB_README.md).

## License

MIT License

