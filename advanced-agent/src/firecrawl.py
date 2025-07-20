import os
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv

load_dotenv()


class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self.app = FirecrawlApp(api_key=api_key)
        self._last_search_results = []

    def search_companies(self, query: str, num_results: int = 5):
        try:
            result = self.app.search(
                query=f"{query} company pricing",
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            return result
        except Exception as e:
            print(e)
            return []

    def scrape_company_pages(self, url: str):
        try:
            result = self.app.scrape_url(
                url,
                formats=["markdown"]
            )
            return result
        except Exception as e:
            print(e)
            return None

    def extract_tools(self, query: str):
        # Search for companies/products/tools
        search_results = self.search_companies(query, num_results=5)
        self._last_search_results = []
        tools = set()
        if hasattr(search_results, 'data'):
            for result in search_results.data:
                url = result.get("url", "")
                scraped = self.scrape_company_pages(url)
                if scraped and hasattr(scraped, 'markdown'):
                    content = scraped.markdown
                    # Simple keyword-based extraction
                    for keyword in ["api", "sdk", "framework", "tool", "platform", "service", "software", "application", "system"]:
                        if keyword in content.lower():
                            tools.add(keyword)
                    self._last_search_results.append({
                        'url': url,
                        'title': result.get('title', ''),
                        'content': content
                    })
        return list(tools)

    def get_search_results(self):
        return self._last_search_results

