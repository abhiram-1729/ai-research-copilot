import streamlit as st
from datetime import datetime
import time
import os
import sys

# Import the copilot classes
from research_copilot import AdvancedResearchCopilot

st.set_page_config(page_title="AI Research Copilot", layout="wide")

# Load environment variables from st.secrets (Streamlit Cloud) or .env (local)
def load_env_vars():
    """Load environment variables from secrets or .env file"""
    try:
        # Try to get from Streamlit secrets first (Cloud deployment)
        if hasattr(st, 'secrets') and len(st.secrets) > 0:
            os.environ['GEMINI_API_KEY'] = st.secrets.get('GEMINI_API_KEY', '')
            os.environ['SERPAPI_KEY'] = st.secrets.get('SERPAPI_KEY', '')
            os.environ['NOTION_TOKEN'] = st.secrets.get('NOTION_TOKEN', '')
            os.environ['NOTION_DATABASE_ID'] = st.secrets.get('NOTION_DATABASE_ID', '')
            print(f"Loaded secrets from Streamlit", file=sys.stderr)
        else:
            # Fall back to .env file (local development)
            from dotenv import load_dotenv
            load_dotenv()
            print(f"Loaded from .env file", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Could not load environment variables: {e}", file=sys.stderr)

load_env_vars()

# Verify environment variables are loaded
print(f"GEMINI_API_KEY loaded: {bool(os.getenv('GEMINI_API_KEY'))}", file=sys.stderr)
print(f"SERPAPI_KEY loaded: {bool(os.getenv('SERPAPI_KEY'))}", file=sys.stderr)
print(f"NOTION_TOKEN loaded: {bool(os.getenv('NOTION_TOKEN'))}", file=sys.stderr)
print(f"NOTION_DATABASE_ID loaded: {bool(os.getenv('NOTION_DATABASE_ID'))}", file=sys.stderr)

# Initialize copilot and store in session state (with timeout protection)
if 'copilot' not in st.session_state:
    with st.spinner('Initializing AI Research Copilot...'):
        try:
            # Check if required API keys exist before initializing
            gemini_key = os.getenv('GEMINI_API_KEY', '').strip()
            if not gemini_key:
                st.session_state.copilot = None
                st.session_state.init_error = "GEMINI_API_KEY not configured. Please add it to Streamlit Secrets."
            else:
                st.session_state.copilot = AdvancedResearchCopilot()
                st.session_state.init_error = None
        except Exception as e:
            st.session_state.copilot = None
            st.session_state.init_error = f"Initialization error: {str(e)[:200]}"

copilot = st.session_state.copilot

# Futuristic CSS
FUTURISTIC_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;700&display=swap');
html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
.neon-header {
    font-family: 'Orbitron', sans-serif;
    font-weight: 800;
    font-size: 42px;
    letter-spacing: 1px;
    background: linear-gradient(90deg,#7B61FF,#00E5FF,#7BFFB2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 8px rgba(123,97,255,0.45), 0 0 24px rgba(0,229,255,0.12);
}
.subtle { color: #9aa7b2; }
.glass {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(6px) saturate(140%);
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 8px 30px rgba(2,6,23,0.6) inset;
}
.neon-badge {
    display:inline-block;padding:6px 10px;border-radius:999px;background:linear-gradient(90deg,#00E5FF22,#7B61FF22);color:#bfefff;border:1px solid rgba(255,255,255,0.04);font-weight:600;font-size:12px;
}
.card {
    padding:14px;border-radius:10px;background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));border:1px solid rgba(255,255,255,0.04);
}
.accent {
    color: #7B61FF;
}
.footer { color:#6b7280;font-size:12px }
</style>
"""

def neon_header(title: str, subtitle: str = None):
        st.markdown(f"<div class='neon-header'>{title}</div>", unsafe_allow_html=True)
        if subtitle:
                st.markdown(f"<div class='subtle'>{subtitle}</div>", unsafe_allow_html=True)

def render_card(title: str, body: str):
        st.markdown(f"<div class='card'>\n<h4 style='margin:0;color:#e6eef8'>{title}</h4>\n<p style='color:#9aa7b2;margin-top:6px'>{body}</p>\n</div>", unsafe_allow_html=True)

# Inject CSS
st.markdown(FUTURISTIC_CSS, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("AI Research Copilot")
    st.caption("Research assistant with real-time search & Notion integration")
    st.markdown("---")
    
    # Debug info (show which keys are loaded)
    with st.expander("🔍 Debug Info"):
        gemini_loaded = bool(os.getenv('GEMINI_API_KEY', '').strip())
        serpapi_loaded = bool(os.getenv('SERPAPI_KEY', '').strip())
        notion_token = bool(os.getenv('NOTION_TOKEN', '').strip())
        notion_db = bool(os.getenv('NOTION_DATABASE_ID', '').strip())
        
        st.write("**Environment Variables:**")
        st.write(f"- GEMINI_API_KEY: {'✅ Loaded' if gemini_loaded else '❌ Missing'}")
        st.write(f"- SERPAPI_KEY: {'✅ Loaded' if serpapi_loaded else '❌ Missing'}")
        st.write(f"- NOTION_TOKEN: {'✅ Loaded' if notion_token else '❌ Missing'}")
        st.write(f"- NOTION_DATABASE_ID: {'✅ Loaded' if notion_db else '❌ Missing'}")
    
    st.subheader("API Status")
    if copilot:
        st.write("- Gemini: ✅" if copilot.gemini_api_key else "- Gemini: ❌ Not configured")
        st.write("- SerpAPI: ✅" if copilot.serpapi_available else "- SerpAPI: ❌ Not configured")
        st.write("- Notion: ✅" if copilot.notion_available else "- Notion: ❌ Not configured")
        st.success("✅ Ready to use")
    else:
        st.error("⚠️ Initialization Failed")
        if st.session_state.init_error:
            st.error(st.session_state.init_error)
    st.markdown("---")
    st.caption("Tips: enter queries and press the action button. Results auto-save to Notion when configured.")
    st.markdown("---")
    if st.button('Reload Copilot'):
        st.rerun()

# Main layout
neon_header("🔬 AI Research Copilot", "A futuristic assistant for searching, summarizing and saving research to Notion.")

# Show prominent error if not initialized
if not copilot:
    st.error("🚨 **Copilot not initialized - Please configure API keys**")
    st.stop()  # Prevent the rest of the app from running

cols_banner = st.columns([1,3,1])
with cols_banner[0]:
    st.markdown("<div class='neon-badge'>LIVE</div>", unsafe_allow_html=True)
with cols_banner[1]:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
with cols_banner[2]:
    st.markdown("<div class='subtle'>Status: <span class='accent'>Optimized</span></div>", unsafe_allow_html=True)

tabs = st.tabs(["Research", "Search", "News", "Summarize", "Compare", "Trends", "Notion", "History"])

# ------------------ Research Tab ------------------
with tabs[0]:
    st.header("End-to-end Research")
    topic = st.text_input("Research topic", value="artificial intelligence")
    cols = st.columns([1, 1, 1, 1])
    use_real_time = cols[0].checkbox("Use real-time web (SerpAPI)", value=True, key="use_real_time_research")
    auto_save = cols[1].checkbox("Auto-save to Notion (Research)", value=True, key="auto_save_research")
    run_btn = cols[2].button("Run Research")
    clear_history = cols[3].button("Clear History")
    if clear_history:
        try:
            copilot.conversation_history.clear()
            st.success("History cleared")
        except Exception:
            st.error("Failed to clear history")
    if run_btn:
        if not copilot:
            st.error("Copilot not initialized")
        elif not topic.strip():
            st.error("Please enter a topic")
        else:
            with st.spinner('Running research workflow...'):
                result = copilot.research_workflow(topic, save_to_notion=auto_save, use_real_time=use_real_time)
            st.success("Research completed")
            st.subheader("Summary")
            st.markdown(result['summary'])
            st.subheader("Notion Result")
            st.write(result['notion_result'])
            st.subheader("Search Results (truncated)")
            st.code(result['search_results'])
            # record history (research_workflow already appends)

# ------------------ Search Tab ------------------
with tabs[1]:
    st.header("Real-time Web Search")
    query = st.text_input("Search query", key='search_query')
    search_cols = st.columns([3, 1])
    search_auto_save = search_cols[1].checkbox("Auto-save to Notion (Search)", value=True, key="auto_save_search")
    if search_cols[0].button('Search'):
        if not copilot:
            st.error("Copilot not initialized")
        elif not query.strip():
            st.error("Please enter a search query")
        else:
            with st.spinner('Searching the web...'):
                results = copilot.web_search_tool(query, use_serpapi=True)
            st.subheader("Results")
            st.text_area("Search Output", value=results, height=400)
            # Optionally save to Notion
            saved_to_notion = False
            notion_result = None
            if search_auto_save and copilot.notion_available:
                try:
                    st.info("Saving search to Notion...")
                    title = f"Search: {query}"
                    notion_result = copilot.create_notion_page(title, results)
                    st.success(notion_result)
                    saved_to_notion = True
                except Exception as e:
                    st.error(f"Notion save failed: {e}")
                    print(f"Notion save failed (Search): {e}", file=sys.stderr)

            # Record history for UI searches
            try:
                copilot.conversation_history.append({
                    "type": "search",
                    "query": query,
                    "results": results[:200] if isinstance(results, str) else str(results)[:200],
                    "saved_to_notion": saved_to_notion,
                    "notion_result": notion_result,
                    "timestamp": datetime.now().astimezone().isoformat()
                })
            except Exception:
                pass

# ------------------ News Tab ------------------
with tabs[2]:
    st.header("Latest News")
    news_q = st.text_input("News query", key='news_query')
    news_cols = st.columns([3, 1])
    news_auto_save = news_cols[1].checkbox("Auto-save to Notion (News)", value=True, key="auto_save_news")
    if news_cols[0].button('Fetch News'):
        if not copilot:
            st.error("Copilot not initialized")
        elif not news_q.strip():
            st.error("Please enter a news query")
        else:
            with st.spinner('Fetching news...'):
                news_results = copilot.search_news_only(news_q)
            st.text_area("News Output", value=news_results, height=400)
            # Optionally save to Notion
            saved_to_notion = False
            notion_result = None
            if news_auto_save and copilot.notion_available:
                try:
                    st.info("Saving news to Notion...")
                    title = f"News: {news_q}"
                    notion_result = copilot.create_notion_page(title, news_results)
                    st.success(notion_result)
                    saved_to_notion = True
                except Exception as e:
                    st.error(f"Notion save failed: {e}")
                    print(f"Notion save failed (News): {e}", file=sys.stderr)

            # Record history for UI news
            try:
                copilot.conversation_history.append({
                    "type": "news",
                    "query": news_q,
                    "results": news_results[:200] if isinstance(news_results, str) else str(news_results)[:200],
                    "saved_to_notion": saved_to_notion,
                    "notion_result": notion_result,
                    "timestamp": datetime.now().astimezone().isoformat()
                })
            except Exception:
                pass

# ------------------ Summarize Tab ------------------
with tabs[3]:
    st.header("Summarize Text")
    content = st.text_area("Paste text to summarize", height=250)
    topic_for_summary = st.text_input("Topic (optional)")
    summarize_cols = st.columns([3, 1])
    summarize_auto_save = summarize_cols[1].checkbox("Auto-save to Notion (Summarize)", value=True, key="auto_save_summarize")
    if summarize_cols[0].button('Summarize'):
        if not copilot:
            st.error("Copilot not initialized")
        elif not content.strip():
            st.error("Please enter text to summarize")
        else:
            with st.spinner('Generating summary...'):
                summary = copilot.summarize_research(content, topic_for_summary or "General")
            st.subheader("Summary")
            st.markdown(summary)
            # Optionally save summary to Notion
            saved_to_notion = False
            notion_result = None
            if summarize_auto_save and copilot.notion_available:
                try:
                    st.info("Saving summary to Notion...")
                    title = f"Summary: { (topic_for_summary or 'General') }"
                    notion_result = copilot.create_notion_page(title, summary)
                    st.success(notion_result)
                    saved_to_notion = True
                except Exception as e:
                    st.error(f"Notion save failed: {e}")
                    print(f"Notion save failed (Summarize): {e}", file=sys.stderr)

            # Record history for summaries
            try:
                copilot.conversation_history.append({
                    "type": "summarize",
                    "content": content[:200],
                    "summary": summary[:300] if isinstance(summary, str) else str(summary)[:300],
                    "saved_to_notion": saved_to_notion,
                    "notion_result": notion_result,
                    "timestamp": datetime.now().astimezone().isoformat()
                })
            except Exception:
                pass

# ------------------ Compare Tab ------------------
with tabs[4]:
    st.header("Compare Concepts")
    c1 = st.text_input("Concept A", key='c1')
    c2 = st.text_input("Concept B", key='c2')
    compare_cols = st.columns([3, 1])
    compare_auto_save = compare_cols[1].checkbox("Auto-save to Notion (Compare)", value=False, key="auto_save_compare")
    if compare_cols[0].button('Compare'):
        if not copilot:
            st.error("Copilot not initialized")
        elif not c1.strip() or not c2.strip():
            st.error("Please enter both concepts")
        else:
            with st.spinner('Comparing...'):
                cmp = copilot.compare_concepts(c1, c2)
            st.markdown(cmp)
            # Optionally save compare result to Notion
            saved_to_notion = False
            notion_result = None
            if compare_auto_save and copilot.notion_available:
                try:
                    title = f"Compare: {c1} vs {c2}"
                    notion_result = copilot.create_notion_page(title, cmp)
                    st.success(notion_result)
                    saved_to_notion = True
                except Exception as e:
                    st.error(f"Notion save failed: {e}")
                    print(f"Notion save failed (Compare): {e}", file=sys.stderr)

            # Record history for comparisons
            try:
                copilot.conversation_history.append({
                    "type": "compare",
                    "concept_a": c1,
                    "concept_b": c2,
                    "result": cmp[:300] if isinstance(cmp, str) else str(cmp)[:300],
                    "saved_to_notion": saved_to_notion,
                    "notion_result": notion_result,
                    "timestamp": datetime.now().astimezone().isoformat()
                })
            except Exception:
                pass

# ------------------ Trends Tab ------------------
with tabs[5]:
    st.header("Analyze Research Trends")
    trend_topic = st.text_input("Topic for trends", key='trend_topic')
    trends_cols = st.columns([3, 1])
    trends_auto_save = trends_cols[1].checkbox("Auto-save to Notion (Trends)", value=False, key="auto_save_trends")
    if trends_cols[0].button('Analyze Trends'):
        if not copilot:
            st.error("Copilot not initialized")
        elif not trend_topic.strip():
            st.error("Please enter a topic")
        else:
            with st.spinner('Analyzing trends...'):
                trends = copilot.analyze_research_trends(trend_topic)
            st.markdown(trends)
            # Optionally save trends to Notion
            saved_to_notion = False
            notion_result = None
            if trends_auto_save and copilot.notion_available:
                try:
                    title = f"Trends: {trend_topic}"
                    notion_result = copilot.create_notion_page(title, trends)
                    st.success(notion_result)
                    saved_to_notion = True
                except Exception as e:
                    st.error(f"Notion save failed: {e}")
                    print(f"Notion save failed (Trends): {e}", file=sys.stderr)

            # Record history for trend analysis
            try:
                copilot.conversation_history.append({
                    "type": "trends",
                    "topic": trend_topic,
                    "result": trends[:300] if isinstance(trends, str) else str(trends)[:300],
                    "saved_to_notion": saved_to_notion,
                    "notion_result": notion_result,
                    "timestamp": datetime.now().astimezone().isoformat()
                })
            except Exception:
                pass

# ------------------ Notion Tab ------------------
with tabs[6]:
    st.header("Notion Tools")
    st.markdown("**Notion Diagnostics**")
    st.write(f"- Notion integration available: {'✅' if copilot and copilot.notion_available else '❌'}")
    if st.button('Run Notion Test'):
        if not copilot:
            st.error("Copilot not initialized")
        else:
            try:
                test_title = f"TEST Save from App {datetime.utcnow().isoformat()}"
                test_content = "This is a diagnostic test created by the deployed app to verify Notion saving and permissions."
                with st.spinner('Running Notion test...'):
                    res = copilot.create_notion_page(test_title, test_content)
                st.success("Notion test succeeded")
                st.write(res)
                print(f"Notion test succeeded: {res}", file=sys.stderr)
            except Exception as e:
                st.error(f"Notion test failed: {e}")
                print(f"Notion test failed: {e}", file=sys.stderr)
                st.info("If this fails: invite the Notion integration to the database (Share -> Connections -> + Invite), and verify Streamlit Secrets contain NOTION_TOKEN and NOTION_DATABASE_ID.")
    st.markdown("---")
    notion_query = st.text_input("Search Notion", key='notion_query')
    if st.button('Search Notion'):
        if not copilot:
            st.error("Copilot not initialized")
        elif not notion_query.strip():
            st.error("Please enter a query")
        else:
            with st.spinner('Searching Notion...'):
                nres = copilot.search_notion(notion_query)
            st.text_area("Notion Search", value=nres, height=250)

    st.markdown("---")
    st.subheader("Create Notion Page")
    new_title = st.text_input("Page title", key='new_title')
    new_content = st.text_area("Page content", key='new_content')
    if st.button('Create Page'):
        if not copilot:
            st.error("Copilot not initialized")
        elif not new_title.strip():
            st.error("Please enter a page title")
        else:
            with st.spinner('Creating Notion page...'):
                res = copilot.create_notion_page(new_title, new_content)
            st.success(res)
            # Record history for manual Notion page creation
            try:
                copilot.conversation_history.append({
                    "type": "notion_create",
                    "title": new_title,
                    "content": new_content[:200],
                    "notion_result": res,
                    "timestamp": datetime.utcnow().isoformat(),
                    "saved_to_notion": copilot.notion_available
                })
            except Exception:
                pass

# ------------------ History Tab ------------------
with tabs[7]:
    st.header("Session History")
    if copilot and copilot.conversation_history:
        for i, item in enumerate(reversed(copilot.conversation_history[-20:]), 1):
            st.markdown(f"**{i}.** {item.get('topic', item.get('query', item.get('type', 'Unknown')))}")
            st.write(item)
            st.markdown("---")
    else:
        st.info("No history yet. Run a search or research first.")

# Footer
st.markdown("---")
st.caption(f"{datetime.utcnow().isoformat()} UTC — Powered by Gemini & Notion")
