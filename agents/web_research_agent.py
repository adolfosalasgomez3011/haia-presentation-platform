import os
from autogen import AssistantAgent


def create_web_research_agent():
    return AssistantAgent(
        name="WebResearchAgent",
        system_message=(
            "You are a web research specialist. You analyze search results and extract "
            "relevant company information for business analysis presentations.\n\n"
            "Focus on:\n"
            "- Company overview and business model\n"
            "- Financial performance and metrics\n"
            "- Market position and competitive advantages\n"
            "- Leadership and management team\n"
            "- Recent developments and news\n"
            "- ESG (Environmental, Social, Governance) factors\n\n"
            "Provide clear, factual summaries suitable for executive presentations."
        ),
        llm_config={
            "config_list": [{
                "model": "gemini-1.5-pro",
                "api_key": os.getenv("GEMINI_API_KEY"),  # Changed from GOOGLE_API_KEY
                "api_type": "google"
            }],
            "temperature": 0.2
        },
        human_input_mode="NEVER"
    )
