#!/usr/bin/env python3
"""
Comprehensive Research System - DuckDuckGo Search + Content Scraping
"""

import requests
from bs4 import BeautifulSoup
import asyncio
import json
import os
from datetime import datetime
from urllib.parse import urljoin, urlparse
import re
from typing import List, Dict, Tuple
from crawler import extract_markdown


class ComprehensiveResearcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
    
    def ddg_search(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search DuckDuckGo and return results with metadata"""
        print(f"Searching DuckDuckGo for: {query}")
        
        url = "https://html.duckduckgo.com/html/"
        data = {"q": query}
        
        try:
            resp = self.session.post(url, data=data, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            
            results = []
            links = soup.find_all('a', href=True)
            
            for link in links[:max_results * 2]:
                try:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    
                    if not href.startswith('http') or len(text) < 10:
                        continue
                    
                    # Skip internal DuckDuckGo links
                    if 'duckduckgo.com' in href or 'duck.co' in href:
                        continue
                    
                    # Skip common non-content links
                    skip_domains = ['youtube.com', 'facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com']
                    if any(domain in href for domain in skip_domains):
                        continue
                    
                    results.append({
                        'title': text,
                        'url': href,
                        'snippet': text[:200] + '...' if len(text) > 200 else text
                    })
                    
                    if len(results) >= max_results:
                        break
                        
                except Exception as e:
                    continue
            
            print(f"Found {len(results)} results")
            return results
            
        except Exception as e:
            print(f"Search failed: {e}")
            return []
    
    def evaluate_relevance(self, result: Dict, query: str) -> float:
        """Evaluate relevance of a search result"""
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        query_terms = query.lower().split()
        
        score = 0.0
        
        # Title relevance (higher weight)
        title_matches = sum(1 for term in query_terms if term in title)
        score += title_matches * 2.0
        
        # Snippet relevance
        snippet_matches = sum(1 for term in query_terms if term in snippet)
        score += snippet_matches * 1.0
        
        # URL domain authority (basic)
        url = result.get('url', '')
        if any(domain in url for domain in ['nytimes.com', 'washingtonpost.com', 'bbc.com', 'reuters.com', 'cnn.com']):
            score += 1.0
        
        return score
    
    def select_top_urls(self, results: List[Dict], query: str, top_n: int = 6) -> List[Dict]:
        """Select top N most relevant URLs"""
        if not results:
            return []
        
        # Score all results
        scored_results = []
        for result in results:
            score = self.evaluate_relevance(result, query)
            scored_results.append((result, score))
        
        # Sort by score (descending)
        scored_results.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N
        top_results = [result for result, score in scored_results[:top_n]]
        print(f"Selected top {len(top_results)} most relevant URLs")
        
        return top_results
    
    async def scrape_urls(self, urls: List[Dict]) -> List[Dict]:
        """Scrape content from URLs using crawl4ai"""
        print(f"Scraping content from {len(urls)} URLs...")
        
        scraped_content = []
        
        for i, url_info in enumerate(urls):
            try:
                url = url_info['url']
                print(f"Scraping {i+1}/{len(urls)}: {url}")
                
                # Use crawl4ai for robust content extraction
                content = await extract_markdown(url)
                
                if content and len(content.strip()) > 100:
                    scraped_content.append({
                        'url': url,
                        'title': url_info.get('title', ''),
                        'content': content,
                        'length': len(content)
                    })
                    print(f"Successfully scraped {len(content)} characters")
                else:
                    print(f"Failed to extract meaningful content")
                    
            except Exception as e:
                print(f"Error scraping {url_info['url']}: {e}")
                continue
        
        print(f"Successfully scraped {len(scraped_content)} URLs")
        return scraped_content
    
    def consolidate_content(self, scraped_content: List[Dict], query: str) -> str:
        """Consolidate all scraped content into a single text"""
        print("Consolidating scraped content...")
        
        consolidated = f"RESEARCH RESULTS FOR: {query}\n"
        consolidated += "=" * 80 + "\n\n"
        
        for i, item in enumerate(scraped_content, 1):
            consolidated += f"SOURCE {i}: {item['title']}\n"
            consolidated += f"URL: {item['url']}\n"
            consolidated += f"CONTENT LENGTH: {item['length']} characters\n"
            consolidated += "-" * 40 + "\n"
            consolidated += item['content']
            consolidated += "\n\n" + "=" * 80 + "\n\n"
        
        return consolidated
    
    async def comprehensive_research(self, query: str, max_results: int = 10, top_urls: int = 6) -> Dict:
        """Perform comprehensive research on a query"""
        print(f"Starting comprehensive research for: {query}")
        
        # Step 1: Search DuckDuckGo
        search_results = self.ddg_search(query, max_results)
        
        if not search_results:
            return {
                'query': query,
                'error': 'No search results found',
                'content': '',
                'sources': []
            }
        
        # Step 2: Select most relevant URLs
        top_urls_list = self.select_top_urls(search_results, query, top_urls)
        
        if not top_urls_list:
            return {
                'query': query,
                'error': 'No relevant URLs found',
                'content': '',
                'sources': []
            }
        
        # Step 3: Scrape content from selected URLs
        scraped_content = await self.scrape_urls(top_urls_list)
        
        if not scraped_content:
            return {
                'query': query,
                'error': 'Failed to scrape content from URLs',
                'content': '',
                'sources': []
            }
        
        # Step 4: Consolidate content
        consolidated_content = self.consolidate_content(scraped_content, query)
        
        # Step 5: Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_query = re.sub(r'[^\w\s-]', '', query).strip()
        safe_query = re.sub(r'[-\s]+', '_', safe_query)
        
        # Save JSON
        json_filename = f"research_{safe_query}_{timestamp}.json"
        research_data = {
            'query': query,
            'timestamp': timestamp,
            'sources': scraped_content,
            'total_sources': len(scraped_content),
            'total_content_length': sum(item['length'] for item in scraped_content)
        }
        
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(research_data, f, indent=2)
        
        # Save text
        txt_filename = f"research_{safe_query}_{timestamp}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write(consolidated_content)
        
        print(f"Research completed and saved to {json_filename} and {txt_filename}")
        
        return {
            'query': query,
            'content': consolidated_content,
            'sources': scraped_content,
            'json_file': json_filename,
            'txt_file': txt_filename
        }


async def main():
    """Example usage"""
    researcher = ComprehensiveResearcher()
    
    query = "artificial intelligence trends 2024"
    result = await researcher.comprehensive_research(query)
    
    if 'error' in result:
        print(f"Research failed: {result['error']}")
    else:
        print(f"Research completed successfully!")
        print(f"Found {len(result['sources'])} sources")
        print(f"Total content length: {len(result['content'])} characters")


if __name__ == "__main__":
    asyncio.run(main())