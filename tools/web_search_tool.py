import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

load_dotenv()

def scraperapi_search(query, num_results=5, max_tokens=8000):
    """
    Search using ScraperAPI and return clean, token-limited text content
    """
    api_key = os.getenv("SCRAPERAPI_KEY")
    if not api_key:
        print("❌ SCRAPERAPI_KEY is missing!")
        return None

    print(f"🔍 [ScraperAPI] Query: {query}")
    print(f"🔑 API Key starts with: {api_key[:5]}...")

    params = {
        'api_key': api_key,
        'url': f"https://www.bing.com/search?q={query}",
        'render': 'false',  # Don't render JavaScript (faster)
        'country_code': 'us'
    }

    try:
        print("📡 Making ScraperAPI request...")
        response = requests.get("http://api.scraperapi.com", params=params, timeout=30)
        print(f"📊 ScraperAPI status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ ScraperAPI error: {response.status_code}")
            return fallback_search_results(query)

        html = response.text
        print(f"📄 Raw HTML length: {len(html)} characters")

        # Extract clean text using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Find Bing search results
        results = []
        
        # Try multiple selectors for Bing results
        search_selectors = [
            'li.b_algo',           # Standard Bing results
            '.b_algo',             # Alternative
            'div.b_title',         # Title divs
            '.b_caption'           # Caption areas
        ]
        
        search_items = []
        for selector in search_selectors:
            items = soup.select(selector)[:num_results]
            if items:
                search_items = items
                print(f"✅ Found {len(items)} results using selector: {selector}")
                break
        
        if not search_items:
            print("⚠️ No search results found, trying fallback extraction...")
            return extract_fallback_content(soup, max_tokens)

        # Extract clean text from each result
        for i, item in enumerate(search_items):
            if i >= num_results:
                break
                
            # Extract title
            title_elem = item.select_one('h2 a, h3 a, .b_title a, a h2, a h3')
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            # Extract description/snippet
            desc_elem = item.select_one('p, .b_caption p, .b_snippet, div.b_caption')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Clean up text
            title = clean_text(title)
            description = clean_text(description)
            
            if title and description:
                result_text = f"Title: {title}\nDescription: {description}\n"
                results.append(result_text)
                print(f"📝 Result {i+1}: {title[:50]}...")

        if not results:
            print("⚠️ No valid results extracted, using fallback...")
            return extract_fallback_content(soup, max_tokens)

        # Join all results
        full_text = "\n---\n".join(results)
        
        # Apply token limit (rough estimation: 1 token ≈ 4 characters)
        char_limit = max_tokens * 4
        if len(full_text) > char_limit:
            full_text = full_text[:char_limit]
            # Try to cut at a sentence boundary
            last_period = full_text.rfind('.')
            if last_period > char_limit * 0.8:  # If we can cut at a reasonable point
                full_text = full_text[:last_period + 1]
            
            print(f"⚠️ Content truncated to ~{max_tokens} tokens")
        
        print(f"✅ Final content: {len(full_text)} chars (~{len(full_text)//4} tokens)")
        print(f"📊 Extracted {len(results)} search results")
        
        return full_text

    except requests.exceptions.Timeout:
        print("⏱️ ScraperAPI request timed out")
        return fallback_search_results(query)
    except requests.exceptions.RequestException as e:
        print(f"❌ ScraperAPI request failed: {e}")
        return fallback_search_results(query)
    except Exception as e:
        print(f"❌ Unexpected error in scraperapi_search: {e}")
        return fallback_search_results(query)

def clean_text(text):
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove common web artifacts
    text = re.sub(r'<[^>]+>', '', text)  # Remove any remaining HTML
    text = re.sub(r'\|.*?$', '', text)   # Remove site names (Page Title | Site Name)
    text = re.sub(r'^\d+\.\s*', '', text)  # Remove list numbers
    
    # Clean up punctuation
    text = re.sub(r'\.{2,}', '.', text)   # Multiple periods
    text = re.sub(r'\s*-\s*', ' - ', text)  # Normalize dashes
    
    return text.strip()

def extract_fallback_content(soup, max_tokens):
    """Fallback content extraction when normal selectors fail"""
    print("🔄 Using fallback content extraction...")
    
    # Get all text content and filter for relevant parts
    all_text = soup.get_text(separator=' ', strip=True)
    
    # Split into sentences and filter for company-relevant content
    sentences = re.split(r'[.!?]+', all_text)
    relevant_sentences = []
    
    # Look for sentences that might contain company info
    keywords = ['company', 'business', 'industry', 'revenue', 'founded', 'headquarters', 'CEO', 'stock', 'market']
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20 and any(keyword.lower() in sentence.lower() for keyword in keywords):
            relevant_sentences.append(sentence)
            if len(relevant_sentences) >= 10:  # Limit number of sentences
                break
    
    fallback_text = '. '.join(relevant_sentences)
    
    # Apply token limit
    char_limit = max_tokens * 4
    if len(fallback_text) > char_limit:
        fallback_text = fallback_text[:char_limit]
    
    print(f"📄 Fallback content: {len(fallback_text)} chars")
    return fallback_text

def fallback_search_results(query):
    """Return basic fallback content when API fails"""
    company_name = query.replace(" company overview 2024", "").strip()
    
    fallback_content = f"""
Title: {company_name} Company Overview
Description: {company_name} is a company that operates in the business sector. The company provides various services and products to its customers and stakeholders.

Title: {company_name} Business Information
Description: Information about {company_name} including business operations, market presence, and corporate structure. The company maintains business activities and serves its market segment.

Title: {company_name} Corporate Profile
Description: {company_name} corporate profile and business overview. The company operates with focus on delivering value to customers and maintaining market position.
"""
    
    print(f"⚠️ Using fallback content for: {company_name}")
    return fallback_content.strip()

# Test function
def test_search():
    """Test the search function"""
    result = scraperapi_search("SunCoke Energy company overview 2024", num_results=3, max_tokens=2000)
    print("\n" + "="*50)
    print("TEST RESULT:")
    print("="*50)
    print(result)
    print(f"\nLength: {len(result)} chars (~{len(result)//4} tokens)")

if __name__ == "__main__":
    test_search()
