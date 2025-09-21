#!/usr/bin/env python3
"""
Clean text extraction with comprehensive filtering
"""

import asyncio
import re
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator


def is_advertisement_content(line):
    """Check if line contains advertisement indicators"""
    ad_patterns = [
        r'\b(advertisement|ad|sponsored|promoted|partner content|brand content|paid content|native ad)\b',
        r'\b(subscribe|join|newsletter|email updates|daily digest|weekly digest|get premium|upgrade to|try premium)\b',
        r'\b(limited time|special offer|deal|discount|sale|buy now|shop now|order now|click here|learn more)\b',
        r'\b(affiliate|commission|earn money|make money|monetize|revenue)\b',
        r'\b(click to|tap to|swipe to|download|install|get started|sign up now)\b',
        r'\b(free trial|premium access|unlock|exclusive|bonus|gift)\b',
        r'\b(popup|modal|overlay|banner|promo|offer|deal)\b',
        r'\b(act now|don\'t miss|hurry|expires|ends soon|while supplies last)\b',
        r'\b(guaranteed|risk-free|money back|satisfaction guaranteed)\b'
    ]
    
    line_lower = line.lower()
    return any(re.search(pattern, line_lower) for pattern in ad_patterns)


def is_ui_element(line):
    """Check if line is a UI element"""
    ui_patterns = [
        r'\b(sign up|sign in|login|register|follow|share|like|comment|subscribe)\b',
        r'\b(open in app|download app|get the app|listen|watch|play|view|read more)\b',
        r'\b(sitemap|privacy policy|terms of service|cookie policy|contact us|help|support)\b',
        r'\b(about us|about|home|menu|navigation|skip to|jump to|back to top)\b',
        r'\b(previous|next|more|less|show more|show less|back to|return to|continue)\b',
        r'\b(search|filter|sort|category|tag|archive|rss|feed)\b',
        r'\b(facebook|twitter|instagram|linkedin|youtube|tiktok|pinterest|reddit|snapchat)\b',
        r'\b(tweet|retweet|pin|bookmark|save|favorite|react|emoji)\b',
        r'\b(share on|follow us|connect with|join us|stay connected)\b',
        r'\b(cookie consent|accept cookies|cookie settings|gdpr|privacy settings)\b',
        r'\b(writing is for everyone|medium|wordpress|blogger|tumblr|substack)\b',
        r'\b(recommended|trending|popular|featured|latest|breaking|news)\b'
    ]
    
    line_lower = line.lower()
    return any(re.search(pattern, line_lower) for pattern in ui_patterns)


def is_navigation_content(line):
    """Check if line is navigation or breadcrumb content"""
    nav_patterns = [
        r'^(home|about|contact|services|products|blog|news|support|help|faq|login|register|sign up|sign in)$',
        r'^(previous|next|back|forward|up|down|left|right|top|bottom)$',
        r'^(page \d+|page \d+ of \d+|showing \d+ of \d+|results \d+-\d+ of \d+)$',
        r'^(sort by|filter by|search|browse|explore|discover)$',
        r'^(categories|tags|topics|sections|chapters|parts)$'
    ]
    
    line_stripped = line.strip()
    return any(re.search(pattern, line_stripped, re.IGNORECASE) for pattern in nav_patterns)


def is_boilerplate_content(line):
    """Check if line is boilerplate content"""
    boilerplate_patterns = [
        r'\b(copyright|all rights reserved|©|®|™)\b',
        r'\b(privacy policy|terms of service|terms and conditions|disclaimer)\b',
        r'\b(cookie policy|gdpr|data protection|legal notice)\b',
        r'\b(accessibility|accessibility statement|wcag|ada)\b',
        r'\b(sitemap|rss|atom|feed|syndication)\b',
        r'\b(last updated|last modified|published|created|posted)\b',
        r'\b(version \d+\.\d+|v\d+\.\d+|build \d+)\b'
    ]
    
    line_lower = line.lower()
    return any(re.search(pattern, line_lower) for pattern in boilerplate_patterns)


def is_social_media_content(line):
    """Check if line is social media related content"""
    social_patterns = [
        r'\b(facebook|twitter|instagram|linkedin|youtube|tiktok|pinterest|reddit|snapchat|discord|telegram)\b',
        r'\b(tweet|retweet|like|share|comment|follow|unfollow|subscribe|unsubscribe)\b',
        r'\b(hashtag|mention|@|#|dm|direct message|story|post|reel|video)\b',
        r'\b(profile|bio|handle|username|display name|avatar|cover photo)\b',
        r'\b(engagement|reach|impressions|views|likes|shares|comments|followers|following)\b'
    ]
    
    line_lower = line.lower()
    return any(re.search(pattern, line_lower) for pattern in social_patterns)


def is_technical_content(line):
    """Check if line is technical/system content"""
    technical_patterns = [
        r'\b(api|endpoint|request|response|status|code|error|exception|debug|log)\b',
        r'\b(database|table|query|sql|nosql|mongodb|mysql|postgresql)\b',
        r'\b(server|client|host|domain|subdomain|ip|address|port|protocol)\b',
        r'\b(html|css|javascript|js|php|python|java|c\+\+|c#|ruby|go|rust)\b',
        r'\b(framework|library|package|module|dependency|import|export)\b',
        r'\b(git|github|gitlab|bitbucket|repository|commit|branch|merge|pull request)\b',
        r'\b(docker|kubernetes|container|microservice|deployment|ci/cd|pipeline)\b'
    ]
    
    line_lower = line.lower()
    return any(re.search(pattern, line_lower) for pattern in technical_patterns)


def clean_text(text):
    """Clean and filter text content"""
    if not text:
        return ""
    
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Skip very short lines (likely not content)
        if len(line) < 10:
            continue
        
        # Skip lines that are mostly punctuation or numbers
        if len(re.sub(r'[^\w\s]', '', line)) < 5:
            continue
        
        # Skip advertisement content
        if is_advertisement_content(line):
            continue
        
        # Skip UI elements
        if is_ui_element(line):
            continue
        
        # Skip navigation content
        if is_navigation_content(line):
            continue
        
        # Skip boilerplate content
        if is_boilerplate_content(line):
            continue
        
        # Skip social media content
        if is_social_media_content(line):
            continue
        
        # Skip technical content (unless it's the main topic)
        if is_technical_content(line):
            continue
        
        # Skip lines that are mostly URLs
        if re.match(r'^https?://', line):
            continue
        
        # Skip lines that are mostly email addresses
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', line):
            continue
        
        # Skip lines that are mostly phone numbers
        if re.match(r'^[\+]?[1-9][\d]{0,15}$', line):
            continue
        
        # Skip lines that are mostly dates
        if re.match(r'^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$', line):
            continue
        
        # Skip lines that are mostly times
        if re.match(r'^\d{1,2}:\d{2}(:\d{2})?(\s?[AP]M)?$', line):
            continue
        
        # Skip lines that are mostly numbers
        if re.match(r'^\d+$', line):
            continue
        
        # Skip lines that are mostly special characters
        if len(re.sub(r'[^\w\s]', '', line)) < len(line) * 0.3:
            continue
        
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


async def extract_markdown(url: str) -> str:
    """Extract clean markdown content from a URL using crawl4ai"""
    try:
        async with AsyncWebCrawler(
            browser_config=BrowserConfig(
                headless=True,
                browser_type="chromium"
            )
        ) as crawler:
            
            # Configure the crawler
            run_config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                content_filter=PruningContentFilter(
                    remove_ads=True,
                    remove_forms=True,
                    remove_scripts=True,
                    remove_styles=True,
                    remove_comments=True,
                    remove_meta=True,
                    remove_links=True,
                    remove_images=True,
                    remove_videos=True,
                    remove_audio=True,
                    remove_iframes=True,
                    remove_embeds=True,
                    remove_tables=True,
                    remove_lists=True,
                    remove_quotes=True,
                    remove_code=True,
                    remove_pre=True,
                    remove_blockquotes=True,
                    remove_divs=True,
                    remove_spans=True,
                    remove_paragraphs=True,
                    remove_headers=True,
                    remove_sections=True,
                    remove_articles=True,
                    remove_asides=True,
                    remove_navs=True,
                    remove_footers=True,
                    remove_headers=True,
                    remove_menus=True,
                    remove_sidebars=True,
                    remove_ads=True,
                    remove_forms=True,
                    remove_scripts=True,
                    remove_styles=True,
                    remove_comments=True,
                    remove_meta=True,
                    remove_links=True,
                    remove_images=True,
                    remove_videos=True,
                    remove_audio=True,
                    remove_iframes=True,
                    remove_embeds=True,
                    remove_tables=True,
                    remove_lists=True,
                    remove_quotes=True,
                    remove_code=True,
                    remove_pre=True,
                    remove_blockquotes=True,
                    remove_divs=True,
                    remove_spans=True,
                    remove_paragraphs=True,
                    remove_headers=True,
                    remove_sections=True,
                    remove_articles=True,
                    remove_asides=True,
                    remove_navs=True,
                    remove_footers=True,
                    remove_headers=True,
                    remove_menus=True,
                    remove_sidebars=True
                ),
                markdown_generator=DefaultMarkdownGenerator()
            )
            
            # Crawl the URL
            result = await crawler.arun(url, config=run_config)
            
            if result.success and result.markdown:
                # Clean the extracted content
                cleaned_content = clean_text(result.markdown)
                return cleaned_content
            else:
                print(f"Failed to extract content from {url}")
                return ""
                
    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return ""


async def main():
    """Example usage"""
    url = "https://example.com"
    content = await extract_markdown(url)
    print(f"Extracted content length: {len(content)}")
    print(f"Content preview: {content[:500]}...")


if __name__ == "__main__":
    asyncio.run(main())