import os
import google.generativeai as genai
from dotenv import load_dotenv
from notion_client import Client
import requests
import json
from typing import List, Dict, Any
import re
from datetime import datetime

# Load environment variables
load_dotenv()

class ResearchCopilot:
    def __init__(self):
        # Configure Gemini
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Configure SerpAPI
        self.serpapi_key = os.getenv("SERPAPI_KEY")
        self.serpapi_available = bool(self.serpapi_key)
        
        # Configure Notion
        self.notion_token = os.getenv("NOTION_TOKEN")
        self.notion_database_id = os.getenv("NOTION_DATABASE_ID")
        self.notion = None
        self.notion_available = False
        
        # Try to initialize Notion if credentials are available
        if self.notion_token and self.notion_database_id:
            try:
                self.notion = Client(auth=self.notion_token)
                # Test connection by trying to retrieve the database
                self.notion.databases.retrieve(self.notion_database_id)
                self.notion_available = True
            except Exception as e:
                print(f"⚠️  Notion integration unavailable: {str(e)[:80]}")
                self.notion = None
                self.notion_available = False
        
        # Memory for conversation
        self.conversation_history = []
    
    def gemini_generate(self, prompt: str, context: str = "") -> str:
        """Generate response using Gemini API with context"""
        try:
            full_prompt = f"""
            {context}
            
            Current task: {prompt}
            
            Please provide a comprehensive, well-structured response.
            """
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def serpapi_search(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """Perform real-time web search using SerpAPI"""
        if not self.serpapi_available:
            return {"error": "SerpAPI not configured", "results": []}
        
        try:
            params = {
                'q': query,
                'api_key': self.serpapi_key,
                'engine': 'google',
                'num': num_results,
                'hl': 'en',
                'gl': 'us'
            }
            
            response = requests.get('https://serpapi.com/search', params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_serpapi_results(data)
            
        except Exception as e:
            return {"error": f"SerpAPI search error: {str(e)}", "results": []}
    
    def _parse_serpapi_results(self, data: Dict) -> Dict[str, Any]:
        """Parse SerpAPI results into structured format"""
        results = {
            "search_information": {},
            "organic_results": [],
            "news_results": [],
            "related_searches": []
        }
        
        # Extract search metadata
        if "search_information" in data:
            results["search_information"] = {
                "total_results": data["search_information"].get("total_results", 0),
                "query_displayed": data["search_information"].get("query_displayed", ""),
                "time_taken": data["search_information"].get("time_taken_displayed", "")
            }
        
        # Extract organic results
        if "organic_results" in data:
            for item in data["organic_results"][:10]:  # Limit to top 10
                organic_result = {
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "displayed_link": item.get("displayed_link", ""),
                    "date": item.get("date", "")
                }
                results["organic_results"].append(organic_result)
        
        # Extract news results if available
        if "news_results" in data:
            for item in data["news_results"][:5]:  # Limit to top 5 news
                news_result = {
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": item.get("source", ""),
                    "date": item.get("date", ""),
                    "thumbnail": item.get("thumbnail", "")
                }
                results["news_results"].append(news_result)
        
        # Extract related searches
        if "related_searches" in data:
            for item in data["related_searches"][:5]:
                results["related_searches"].append(item.get("query", ""))
        
        return results
    
    def format_search_results(self, search_data: Dict[str, Any]) -> str:
        """Format SerpAPI results into readable text"""
        if "error" in search_data and search_data["error"]:
            return f"Search error: {search_data['error']}"
        
        formatted = []
        
        # Search information
        info = search_data.get("search_information", {})
        formatted.append(f"🔍 Search Results ({info.get('total_results', 0)} results found)")
        formatted.append(f"Query: {info.get('query_displayed', '')}")
        formatted.append(f"Search time: {info.get('time_taken', '')}")
        formatted.append("")
        
        # News results (most timely)
        news_results = search_data.get("news_results", [])
        if news_results:
            formatted.append("📰 LATEST NEWS:")
            formatted.append("-" * 40)
            for i, news in enumerate(news_results, 1):
                formatted.append(f"{i}. {news['title']}")
                formatted.append(f"   Source: {news.get('source', 'Unknown')}")
                formatted.append(f"   Date: {news.get('date', 'Unknown date')}")
                formatted.append(f"   Summary: {news.get('snippet', 'No summary available')}")
                formatted.append(f"   Link: {news.get('link', '')}")
                formatted.append("")
        
        # Organic results
        organic_results = search_data.get("organic_results", [])
        if organic_results:
            formatted.append("🌐 TOP SEARCH RESULTS:")
            formatted.append("-" * 40)
            for i, result in enumerate(organic_results, 1):
                formatted.append(f"{i}. {result['title']}")
                formatted.append(f"   URL: {result.get('displayed_link', result.get('link', ''))}")
                formatted.append(f"   Date: {result.get('date', 'Unknown date')}")
                formatted.append(f"   Summary: {result.get('snippet', 'No summary available')}")
                formatted.append("")
        
        # Related searches
        related_searches = search_data.get("related_searches", [])
        if related_searches:
            formatted.append("🔗 RELATED SEARCHES:")
            formatted.append(", ".join(related_searches))
        
        return "\n".join(formatted)
    
    def web_search_tool(self, query: str, use_serpapi: bool = True) -> str:
        """Perform web search using SerpAPI or fallback to Gemini"""
        try:
            if use_serpapi and self.serpapi_available:
                print(f"🌐 Searching real-time web for: {query}")
                search_data = self.serpapi_search(query)
                formatted_results = self.format_search_results(search_data)
                
                # Enhance with Gemini analysis if we have good results
                if search_data.get("organic_results") or search_data.get("news_results"):
                    analysis_prompt = f"""
                    Based on the following real-time search results for "{query}", provide a comprehensive analysis:
                    
                    {formatted_results}
                    
                    Please analyze and structure this information into:
                    1. Key findings and main points
                    2. Recent developments (if any news)
                    3. Important statistics or facts
                    4. Authoritative sources mentioned
                    5. Overall summary of current state
                    
                    Focus on providing insights beyond just repeating the search results.
                    """
                    
                    analysis = self.gemini_generate(analysis_prompt)
                    final_output = f"REAL-TIME SEARCH RESULTS:\n{formatted_results}\n\nAI ANALYSIS:\n{analysis}"
                    return final_output
                else:
                    return formatted_results
            else:
                # Fallback to Gemini simulation
                print("⚠️  Using Gemini simulation (no real-time data)")
                search_prompt = f"""
                Simulate comprehensive web search results for: "{query}"
                
                Provide realistic search results including:
                1. Key articles and their summaries
                2. Recent developments
                3. Important facts and statistics
                4. Authoritative sources
                
                Format as a structured research summary.
                """
                
                return self.gemini_generate(search_prompt)
                
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def search_news_only(self, query: str) -> str:
        """Search specifically for recent news"""
        if not self.serpapi_available:
            return "SerpAPI not configured for news search"
        
        try:
            params = {
                'q': query,
                'api_key': self.serpapi_key,
                'engine': 'google',
                'tbm': 'nws',  # News search
                'num': 10,
                'hl': 'en',
                'gl': 'us'
            }
            
            response = requests.get('https://serpapi.com/search', params=params)
            response.raise_for_status()
            
            data = response.json()
            search_data = self._parse_serpapi_results(data)
            return self.format_search_results(search_data)
            
        except Exception as e:
            return f"News search error: {str(e)}"
    
    def summarize_research(self, content: str, topic: str) -> str:
        """Summarize research findings using Gemini"""
        summarize_prompt = f"""
        Summarize the following research content about '{topic}':
        
        {content}
        
        Create a well-structured summary with:
        - Key findings
        - Important statistics
        - Main concepts
        - Practical applications
        - Future trends
        
        Make it comprehensive but concise.
        """
        
        return self.gemini_generate(summarize_prompt)
    
    def create_notion_page(self, title: str, content: str, tags: List[str] = None) -> str:
        """Create a new research page in Notion"""
        if not self.notion:
            return "⚠️  Notion integration not configured"
        
        if not self.notion_database_id:
            return "⚠️  Notion database ID not configured"
        
        try:
            # Prepare properties for Notion
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": title[:100]
                            }
                        }
                    ]
                }
            }
            
            # Add tags if provided
            if tags:
                properties["Tags"] = {
                    "multi_select": [{"name": tag} for tag in tags[:5]]
                }
            
            # Create the page
            response = self.notion.pages.create(
                parent={"database_id": self.notion_database_id},
                properties=properties
            )
            
            # Add content as a child block
            if content:
                try:
                    self.notion.blocks.children.append(
                        block_id=response['id'],
                        children=[
                            {
                                "object": "block",
                                "type": "paragraph",
                                "paragraph": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": content[:2000],
                                                "link": None
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    )
                except Exception as e:
                    # Content adding failed, but page was created
                    pass
            
            return f"✅ Successfully created Notion page: '{title}'"
            
        except Exception as e:
            error_msg = str(e)
            if "Could not find database" in error_msg:
                return f"⚠️  Notion database not found. Please ensure the integration has access."
            elif "is not a property that exists" in error_msg:
                return f"⚠️  Database property mismatch. Ensure database has 'Name' property."
            else:
                return f"❌ Notion error: {error_msg}"
    
    def search_notion(self, query: str) -> str:
        """Search existing research in Notion"""
        if not self.notion:
            return "Notion integration not configured"
        
        try:
            response = self.notion.search(query=query)
            pages = response.get("results", [])
            
            if not pages:
                return "No existing research found on this topic."
            
            # Format results
            results = []
            for i, page in enumerate(pages[:5], 1):
                title = "Untitled"
                if 'properties' in page and 'Name' in page['properties']:
                    title_prop = page['properties']['Name']
                    if 'title' in title_prop and len(title_prop['title']) > 0:
                        title = title_prop['title'][0]['text']['content']
                elif 'properties' in page and 'Title' in page['properties']:
                    title_prop = page['properties']['Title']
                    if 'title' in title_prop and len(title_prop['title']) > 0:
                        title = title_prop['title'][0]['text']['content']
                
                results.append(f"{i}. {title}")
            
            return f"Found {len(pages)} relevant pages:\n" + "\n".join(results)
            
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def research_workflow(self, topic: str, save_to_notion: bool = True, use_real_time: bool = True) -> Dict[str, Any]:
        """Complete research workflow: search → summarize → save"""
        print(f"🔍 Starting research on: {topic}")
        
        # Step 1: Check existing research
        if self.notion_available:
            print("📚 Checking existing research in Notion...")
            existing_research = self.search_notion(topic)
        else:
            existing_research = "Notion not available"
        
        # Step 2: Conduct new research
        print("🌐 Searching for new information...")
        search_results = self.web_search_tool(topic, use_serpapi=use_real_time)
        
        # Step 3: Summarize findings
        print("📝 Summarizing research findings...")
        summary = self.summarize_research(search_results, topic)
        
        # Step 4: Save to Notion if requested and available
        notion_result = ""
        if save_to_notion and self.notion_available:
            print("💾 Saving to Notion...")
            title = f"Research: {topic}"
            notion_result = self.create_notion_page(title, summary, tags=[topic, "research"])
        elif save_to_notion and not self.notion_available:
            notion_result = "⚠️  Notion not available for saving"
        
        # Update conversation history
        self.conversation_history.append({
            "topic": topic,
            "summary": summary,
            "saved_to_notion": save_to_notion and self.notion_available,
            "used_real_time": use_real_time,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "topic": topic,
            "existing_research": existing_research,
            "search_results": search_results[:500] + "..." if len(search_results) > 500 else search_results,
            "summary": summary,
            "notion_result": notion_result,
            "conversation_history": len(self.conversation_history),
            "used_real_time_search": use_real_time
        }
    
    def interactive_mode(self):
        """Run the copilot in interactive mode"""
        print("🤖 AI Research Copilot with Real-Time Search Activated!")
        print("=" * 60)
        print("Available commands:")
        print("- 'research [topic]' - Complete research workflow")
        print("- 'search [query]' - Just search web")
        print("- 'news [query]' - Search latest news")
        print("- 'summarize [content]' - Summarize text")
        print("- 'notion search [query]' - Search Notion")
        print("- 'notion create [title] | [content]' - Create Notion page")
        print("- 'history' - Show research history")
        print("- 'status' - Show API status")
        print("- 'quit' - Exit")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n🎯 Your research request: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Happy researching!")
                    break
                
                elif user_input.lower() == 'history':
                    self.show_history()
                
                elif user_input.lower() == 'status':
                    self.show_status()
                
                elif user_input.startswith('research '):
                    topic = user_input[9:].strip()
                    if topic:
                        result = self.research_workflow(topic, use_real_time=True)
                        self.display_results(result)
                    else:
                        print("❌ Please provide a research topic.")
                
                elif user_input.startswith('search '):
                    query = user_input[7:].strip()
                    if query:
                        results = self.web_search_tool(query, use_serpapi=True)
                        print(f"\n🔍 Real-Time Search Results for '{query}':")
                        print("=" * 50)
                        print(results)
                        
                        # Auto-save to Notion if available
                        saved_to_notion = False
                        if self.notion_available:
                            print("\n💾 Saving to Notion...")
                            title = f"Search: {query}"
                            save_result = self.create_notion_page(title, results)
                            print(save_result)
                            saved_to_notion = True
                        
                        # Update history
                        self.conversation_history.append({
                            "type": "search",
                            "query": query,
                            "results": results[:200],
                            "saved_to_notion": saved_to_notion,
                            "timestamp": datetime.now().isoformat() if 'datetime' in dir() else ""
                        })
                    else:
                        print("❌ Please provide a search query.")
                
                elif user_input.startswith('news '):
                    query = user_input[5:].strip()
                    if query:
                        results = self.search_news_only(query)
                        print(f"\n📰 Latest News for '{query}':")
                        print("=" * 50)
                        print(results)
                        
                        # Auto-save to Notion if available
                        saved_to_notion = False
                        if self.notion_available:
                            print("\n💾 Saving to Notion...")
                            title = f"News: {query}"
                            save_result = self.create_notion_page(title, results)
                            print(save_result)
                            saved_to_notion = True
                        
                        # Update history
                        self.conversation_history.append({
                            "type": "news",
                            "query": query,
                            "results": results[:200],
                            "saved_to_notion": saved_to_notion,
                            "timestamp": datetime.now().isoformat()
                        })
                    else:
                        print("❌ Please provide a news query.")
                
                elif user_input.startswith('summarize '):
                    content = user_input[10:].strip()
                    if content:
                        summary = self.gemini_generate(f"Summarize this content: {content}")
                        print(f"\n📄 Summary:")
                        print("=" * 40)
                        print(summary)
                        
                        # Auto-save to Notion if available
                        saved_to_notion = False
                        if self.notion_available:
                            print("\n💾 Saving to Notion...")
                            title = f"Summary: {content[:50]}..."
                            save_result = self.create_notion_page(title, summary)
                            print(save_result)
                            saved_to_notion = True
                        
                        # Update history
                        self.conversation_history.append({
                            "type": "summarize",
                            "content": content[:100],
                            "summary": summary[:200],
                            "saved_to_notion": saved_to_notion,
                            "timestamp": datetime.now().isoformat()
                        })
                    else:
                        print("❌ Please provide content to summarize.")
                
                elif user_input.startswith('notion search '):
                    query = user_input[14:].strip()
                    if query:
                        results = self.search_notion(query)
                        print(f"\n📚 Notion Search Results:")
                        print("=" * 40)
                        print(results)
                    else:
                        print("❌ Please provide a search query.")
                
                elif user_input.startswith('notion create '):
                    parts = user_input[14:].split('|', 1)
                    if len(parts) == 2:
                        title = parts[0].strip()
                        content = parts[1].strip()
                        result = self.create_notion_page(title, content)
                        print(f"\n{result}")
                    else:
                        print("❌ Format: 'notion create Title | Content'")
                
                elif user_input.lower() == 'help':
                    self.show_help()
                
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
                    
            except EOFError:
                print("\n👋 Goodbye!")
                break
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def show_help(self):
        """Show help information"""
        print("\n📖 HELP GUIDE:")
        print("research machine learning - Complete research with real-time data")
        print("search python programming - Real-time web search")
        print("news artificial intelligence - Search latest news")
        print("summarize long text here - Summarize the provided text")
        print("notion search AI - Search Notion for AI content")
        print("notion create My Title | My content - Create Notion page")
        print("history - Show research history")
        print("status - Show API connectivity status")
        print("quit - Exit the program")
    
    def show_status(self):
        """Show API connectivity status"""
        print("\n🔌 API STATUS:")
        print(f"✅ Gemini API: Configured" if self.gemini_api_key else "❌ Gemini API: Not configured")
        print(f"✅ SerpAPI: Configured" if self.serpapi_available else "❌ SerpAPI: Not configured")
        print(f"✅ Notion: Configured" if self.notion_available else "❌ Notion: Not configured")
        print(f"📊 Research history: {len(self.conversation_history)} items")
    
    def display_results(self, result: Dict[str, Any]):
        """Display research results in a formatted way"""
        print("\n" + "=" * 60)
        print(f"📊 RESEARCH REPORT: {result['topic']}")
        print("=" * 60)
        
        print(f"\n📚 EXISTING RESEARCH:")
        print(result['existing_research'])
        
        print(f"\n🌐 NEW FINDINGS ({'REAL-TIME' if result['used_real_time_search'] else 'SIMULATED'}):")
        print(result['search_results'])
        
        print(f"\n📝 EXECUTIVE SUMMARY:")
        print(result['summary'])
        
        if result['notion_result']:
            print(f"\n💾 NOTION RESULT:")
            print(result['notion_result'])
        
        print(f"\n📈 SESSION: {result['conversation_history']} research tasks completed")
        print("=" * 60)
    
    def show_history(self):
        """Show research history"""
        if not self.conversation_history:
            print("No research history yet.")
            return
        
        print(f"\n📖 RESEARCH HISTORY ({len(self.conversation_history)} items):")
        for i, item in enumerate(self.conversation_history, 1):
            topic = item.get('topic', item.get('query', item.get('type', 'Unknown')))
            real_time = "🔴" if not item.get('used_real_time', True) else "🟢"
            saved = "💾" if item.get('saved_to_notion') else "📄"
            timestamp = item.get('timestamp', 'Unknown time')
            print(f"{i}. {real_time} {saved} {topic} - {timestamp}")

# Advanced version with better tool integration
class AdvancedResearchCopilot(ResearchCopilot):
    def __init__(self):
        super().__init__()
        self.research_topics = {}
    
    def analyze_research_trends(self, topic: str) -> str:
        """Analyze trends and future directions using real-time data"""
        # First get real-time data
        search_data = self.serpapi_search(f"{topic} trends 2024", num_results=15)
        formatted_results = self.format_search_results(search_data)
        
        trend_prompt = f"""
        Based on the following real-time search results about "{topic}", analyze research trends and future directions:
        
        {formatted_results}
        
        Provide:
        1. Current state of research
        2. Emerging trends
        3. Key challenges
        4. Future predictions
        5. Recommended research areas
        
        Be insightful and forward-looking based on the latest information available.
        """
        
        return self.gemini_generate(trend_prompt)
    
    def compare_concepts(self, concept1: str, concept2: str) -> str:
        """Compare two research concepts using real-time data"""
        # Get real-time data for both concepts
        search1 = self.serpapi_search(concept1, num_results=8)
        search2 = self.serpapi_search(concept2, num_results=8)
        
        formatted1 = self.format_search_results(search1)
        formatted2 = self.format_search_results(search2)
        
        compare_prompt = f"""
        Compare and contrast these two concepts using real-time information:
        
        CONCEPT A: {concept1}
        {formatted1}
        
        CONCEPT B: {concept2}
        {formatted2}
        
        Provide:
        - Similarities
        - Differences
        - Use cases for each
        - When to choose one over the other
        - Current popularity and trends
        """
        
        return self.gemini_generate(compare_prompt)

    # Keep the rest of the AdvancedResearchCopilot methods the same as before
    # but they will automatically inherit the real-time search capabilities

if __name__ == "__main__":
    copilot = AdvancedResearchCopilot()
    copilot.interactive_mode()