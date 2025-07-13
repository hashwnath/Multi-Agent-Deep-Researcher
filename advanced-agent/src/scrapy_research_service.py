import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy.signalmanager import dispatcher
import requests
import json
import time
import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
from urllib.parse import urljoin, urlparse
import re
from bs4 import BeautifulSoup
import newspaper3k
from concurrent.futures import ThreadPoolExecutor
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ScrapedContent:
    """Structured content from web scraping"""
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]
    source_type: str
    scraped_at: datetime
    relevance_score: float = 0.0

class ResearchSpider(scrapy.Spider):
    """Scrapy spider for comprehensive research content extraction"""
    
    name = 'research_spider'
    
    def __init__(self, query: str, max_pages: int = 10, *args, **kwargs):
        super(ResearchSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.max_pages = max_pages
        self.scraped_count = 0
        self.start_urls = []
        self.search_results = []
        self.lock = threading.Lock()
        
        # Progress tracking
        self.current_url = ""
        self.progress_callback = None
        
    def start_requests(self):
        """Generate initial requests from search results"""
        logger.info(f"🔍 Starting research spider for query: '{self.query}'")
        
        # Get search results from multiple sources
        search_urls = self.get_search_urls()
        
        for i, url in enumerate(search_urls[:self.max_pages]):
            self.current_url = url
            if self.progress_callback:
                self.progress_callback(f"🌐 Analyzing: {url}")
            
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'source_index': i},
                errback=self.handle_error,
                dont_filter=True
            )
    
    def get_search_urls(self) -> List[str]:
        """Get URLs from multiple search sources"""
        urls = []
        
        # 1. DuckDuckGo search
        logger.info("🔍 Searching DuckDuckGo...")
        ddg_urls = self.search_duckduckgo()
        urls.extend(ddg_urls)
        
        # 2. Google search (using serpapi or similar)
        logger.info("🔍 Searching Google...")
        google_urls = self.search_google()
        urls.extend(google_urls)
        
        # 3. Bing search
        logger.info("🔍 Searching Bing...")
        bing_urls = self.search_bing()
        urls.extend(bing_urls)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        
        logger.info(f"📊 Found {len(unique_urls)} unique URLs from search")
        return unique_urls
    
    def search_duckduckgo(self) -> List[str]:
        """Search DuckDuckGo for relevant URLs"""
        try:
            # DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {
                'q': self.query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                urls = []
                
                # Extract URLs from various sources
                if 'AbstractURL' in data:
                    urls.append(data['AbstractURL'])
                if 'RelatedTopics' in data:
                    for topic in data['RelatedTopics'][:5]:
                        if 'FirstURL' in topic:
                            urls.append(topic['FirstURL'])
                
                return urls
        except Exception as e:
            logger.warning(f"⚠️ DuckDuckGo search failed: {e}")
        
        return []
    
    def search_google(self) -> List[str]:
        """Search Google for relevant URLs (using free alternatives)"""
        try:
            # Using a free search API or scraping Google search results
            # Note: This is a simplified version - you might want to use a proper search API
            search_url = f"https://www.google.com/search?q={self.query.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                urls = []
                
                # Extract URLs from search results
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('/url?q='):
                        url = href.split('/url?q=')[1].split('&')[0]
                        if url.startswith('http'):
                            urls.append(url)
                
                return urls[:5]  # Limit to first 5 results
        except Exception as e:
            logger.warning(f"⚠️ Google search failed: {e}")
        
        return []
    
    def search_bing(self) -> List[str]:
        """Search Bing for relevant URLs"""
        try:
            # Similar to Google search but for Bing
            search_url = f"https://www.bing.com/search?q={self.query.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                urls = []
                
                # Extract URLs from Bing search results
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('http') and 'bing.com' not in href:
                        urls.append(href)
                
                return urls[:5]  # Limit to first 5 results
        except Exception as e:
            logger.warning(f"⚠️ Bing search failed: {e}")
        
        return []
    
    def parse(self, response):
        """Parse individual pages and extract content"""
        try:
            with self.lock:
                self.scraped_count += 1
            
            url = response.url
            domain = urlparse(url).netloc
            
            logger.info(f"📄 Scraping {self.scraped_count}/{self.max_pages}: {domain}")
            
            # Extract content using multiple methods
            content_data = self.extract_content(response)
            
            if content_data['content']:
                scraped_content = ScrapedContent(
                    url=url,
                    title=content_data['title'],
                    content=content_data['content'],
                    metadata=content_data['metadata'],
                    source_type=content_data['source_type'],
                    scraped_at=datetime.now(),
                    relevance_score=self.calculate_relevance(content_data['content'])
                )
                
                self.search_results.append(scraped_content)
                
                logger.info(f"✅ Extracted {len(content_data['content'])} chars from {domain}")
            
        except Exception as e:
            logger.error(f"❌ Error parsing {url}: {e}")
    
    def extract_content(self, response) -> Dict[str, Any]:
        """Extract content using multiple methods"""
        url = response.url
        html_content = response.text
        
        # Method 1: Newspaper3k for article content
        try:
            article = newspaper3k.Article(url)
            article.download(input_html=html_content)
            article.parse()
            
            if article.text:
                return {
                    'title': article.title or '',
                    'content': article.text,
                    'metadata': {
                        'authors': article.authors,
                        'publish_date': str(article.publish_date),
                        'top_image': article.top_image,
                        'summary': article.summary
                    },
                    'source_type': 'article'
                }
        except Exception as e:
            logger.debug(f"Newspaper3k failed for {url}: {e}")
        
        # Method 2: BeautifulSoup for general content
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text() if title else ''
            
            # Extract metadata
            metadata = {}
            meta_tags = soup.find_all('meta')
            for tag in meta_tags:
                name = tag.get('name') or tag.get('property')
                content = tag.get('content')
                if name and content:
                    metadata[name] = content
            
            return {
                'title': title_text,
                'content': text,
                'metadata': metadata,
                'source_type': 'general'
            }
            
        except Exception as e:
            logger.debug(f"BeautifulSoup failed for {url}: {e}")
        
        # Fallback: Return minimal content
        return {
            'title': '',
            'content': html_content[:1000],  # First 1000 chars
            'metadata': {},
            'source_type': 'fallback'
        }
    
    def calculate_relevance(self, content: str) -> float:
        """Calculate relevance score based on query keywords"""
        if not content or not self.query:
            return 0.0
        
        query_words = set(self.query.lower().split())
        content_words = set(content.lower().split())
        
        # Simple relevance calculation
        matches = len(query_words.intersection(content_words))
        relevance = matches / len(query_words) if query_words else 0.0
        
        return min(relevance, 1.0)
    
    def handle_error(self, failure):
        """Handle request errors"""
        url = failure.request.url
        logger.warning(f"⚠️ Failed to scrape {url}: {failure.value}")
    
    def closed(self, reason):
        """Called when spider is closed"""
        logger.info(f"🔄 Spider finished. Scraped {len(self.search_results)} pages")
        logger.info(f"📊 Total content extracted: {sum(len(r.content) for r in self.search_results)} characters")

class ScrapyResearchService:
    """Service for comprehensive web research using Scrapy"""
    
    def __init__(self):
        self.settings = get_project_settings()
        self.settings.set('USER_AGENT', 'Research Agent Bot 1.0')
        self.settings.set('ROBOTSTXT_OBEY', True)
        self.settings.set('DOWNLOAD_DELAY', 1)  # 1 second delay
        self.settings.set('CONCURRENT_REQUESTS', 5)  # Limit concurrent requests
        self.settings.set('CONCURRENT_REQUESTS_PER_DOMAIN', 2)
        self.settings.set('AUTOTHROTTLE_ENABLED', True)
        self.settings.set('AUTOTHROTTLE_START_DELAY', 1)
        self.settings.set('AUTOTHROTTLE_MAX_DELAY', 3)
        
        # Progress tracking
        self.progress_callback = None
        self.current_status = ""
    
    def set_progress_callback(self, callback):
        """Set callback for progress updates"""
        self.progress_callback = callback
    
    def update_progress(self, message: str):
        """Update progress status"""
        self.current_status = message
        if self.progress_callback:
            self.progress_callback(message)
        logger.info(f"📊 {message}")
    
    def extract_content(self, query: str, max_pages: int = 10) -> List[ScrapedContent]:
        """Extract content from multiple sources using Scrapy"""
        
        self.update_progress(f"🚀 Starting comprehensive research for: '{query}'")
        
        # Create spider instance
        spider = ResearchSpider(query=query, max_pages=max_pages)
        spider.progress_callback = self.progress_callback
        
        # Create crawler process
        process = CrawlerProcess(self.settings)
        
        # Add spider to process
        process.crawl(spider)
        
        self.update_progress("🕷️ Initializing Scrapy spider...")
        
        # Start crawling
        process.start()
        
        # Get results from spider
        results = spider.search_results
        
        # Sort by relevance
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        self.update_progress(f"✅ Research complete! Extracted {len(results)} sources")
        
        return results
    
    def get_search_statistics(self, results: List[ScrapedContent]) -> Dict[str, Any]:
        """Get statistics about the search results"""
        if not results:
            return {}
        
        total_content = sum(len(r.content) for r in results)
        avg_content_length = total_content / len(results)
        
        # Group by source type
        source_types = {}
        for result in results:
            source_type = result.source_type
            if source_type not in source_types:
                source_types[source_type] = []
            source_types[source_type].append(result)
        
        # Get top domains
        domains = {}
        for result in results:
            domain = urlparse(result.url).netloc
            domains[domain] = domains.get(domain, 0) + 1
        
        top_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_sources': len(results),
            'total_content_chars': total_content,
            'avg_content_length': avg_content_length,
            'source_types': {k: len(v) for k, v in source_types.items()},
            'top_domains': top_domains,
            'relevance_scores': [r.relevance_score for r in results]
        } 