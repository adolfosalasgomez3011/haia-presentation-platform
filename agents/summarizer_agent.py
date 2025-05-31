import os
from autogen import AssistantAgent

def create_summarizer_agent():
    return AssistantAgent(
        name="SummarizerAgent",
        system_message=(
            "You are an AI that takes raw search results about a company and converts them "
            "into structured company data blocks for a presentation generator.\n\n"
            "Your output must include:\n"
            "- Executive summary (2-3 sentences)\n"
            "- Business segments (name + description)\n"
            "- Financials (revenue, EBITDA, valuation, etc.)\n"
            "- Key assets or regions of operation\n"
            "- Leadership (name, role, brief background)\n"
            "- Sustainability/ESG themes\n"
            "- Key market risks\n"
            "- Quotes (if any from executives)\n"
            "- News highlights\n\n"
            "Be accurate, use markdown-style formatting in lists, and write concisely."
        ),
        llm_config={
            "config_list": [{
                "model": "gemini-1.5-pro",
                "api_key": os.getenv("GEMINI_API_KEY"),  # Changed from GOOGLE_API_KEY
                "api_type": "google"
            }],
            "temperature": 0.3
        },
        human_input_mode="NEVER"
    )
