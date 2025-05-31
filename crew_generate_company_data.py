import os
import sys
import json

# Fix Windows encoding - add this right here
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.append(os.path.abspath("."))  # Ensure tools and agents are importable

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.web_research_agent import create_web_research_agent
from agents.summarizer_agent import create_summarizer_agent
from agents.json_builder_agent import create_json_builder_agent
from tools.web_search_tool import scraperapi_search
from tools.json_writer_tool import write_json_to_file

def generate_company_data(company_name: str):
    print(f"Searching for company: {company_name}")
    web_agent = create_web_research_agent()
    summarizer = create_summarizer_agent()
    builder = create_json_builder_agent()

    # Step 1: Web search
    search_results = scraperapi_search(f"{company_name} company overview 2024")
    if not search_results:
        print("ERROR: No search results returned.")
        return

    print(f"🔍 Search results length: {len(search_results)} characters (~{len(search_results)//4} tokens)")
    print(f"🔍 First 500 chars: {search_results[:500]}")

    # Step 2: Summarize (no truncation needed with Gemini)
    print("Summarizing results...")
    summary_response = summarizer.generate_reply(
        messages=[{"role": "user", "content": search_results}]
    )

    # Handle different response types safely
    if isinstance(summary_response, str):
        summary_text = summary_response
    elif hasattr(summary_response, 'content'):
        summary_text = summary_response.content
    else:
        summary_text = str(summary_response)

    print(f"Summary completed: {summary_text[:500]} ...")

    # Step 3: Build and write JSON
    print("Building JSON file...")
    try:
        builder_reply = builder.generate_reply(messages=[{"role": "user", "content": summary_text}])

        # Handle the JSON response safely
        if isinstance(builder_reply, str):
            json_content = builder_reply
        elif hasattr(builder_reply, 'content'):
            json_content = builder_reply.content
        else:
            json_content = str(builder_reply)

        # Try to parse and validate the JSON
        json_data = json.loads(json_content)
        
        # Write to file manually
        result = write_json_to_file(json_content)
        print(f"✅ {result}")
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON returned: {e}")
        print(f"Raw response: {json_content[:500]}...")
        return
    except Exception as e:
        print(f"❌ Error during JSON building: {e}")
        return

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("company", help="Company name to research")
    args = parser.parse_args()
    generate_company_data(args.company)
