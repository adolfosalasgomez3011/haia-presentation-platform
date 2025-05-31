import json
import os

OUTPUT_PATH = os.path.abspath("F:/revealJS/FirstPresentation/MikaelChallenge/company_data.json")


def write_json_to_file(json_string: str) -> str:
    try:
        parsed = json.loads(json_string)
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON: {e}"

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2)

    return f"✅ JSON saved to {OUTPUT_PATH}"
