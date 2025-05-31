import os
from autogen import AssistantAgent

def create_json_builder_agent():
    return AssistantAgent(
        name="JSONBuilderAgent",
        system_message=(
            "You are a JSON formatter. You receive structured data from a summarizer "
            "and must output valid JSON following the company_data.json format. "
            "Use keys like: 'company', 'summary', 'financials', 'leadership', 'strategy', etc.\n"
            "Return ONLY valid JSON - no other text or explanations. Do not call any functions."
        ),
        llm_config={
            "config_list": [{
                "model": "gemini-1.5-pro",
                "api_key": os.getenv("GEMINI_API_KEY"),
                "api_type": "google"
            }],
            "temperature": 0.3
        },
        human_input_mode="NEVER"
    )
