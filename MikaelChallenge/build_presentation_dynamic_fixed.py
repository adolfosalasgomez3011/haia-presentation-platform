
import json
import os
import shutil
from datetime import datetime

def build_markdown(data):
    slides = []

    # Cover Slide
    company_name = data.get("company", "Unnamed Company")
    slides.append(
    f"""<!-- .slide: data-background-color='#ffffff' style='height: 100vh; display: flex; flex-direction: column; justify-content: flex-start; align-items: center;' -->

<div style="margin-top: 160px; background-color: rgba(14, 47, 68, 0.05); padding: 40px 80px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
  <h1 style="font-size: 84px; letter-spacing: 2px; color: #0e2f44; margin-bottom: 20px;">
    <strong>{company_name.upper()}</strong>
  </h1>
  <p style="font-size: 34px; font-style: italic; color: #333; margin-top: 0;">
    Company Overview – {datetime.now().year}
  </p>
</div>
    """)

    # Executive Summary (dynamic)
    financials = data.get("financials", {})
    summary_cards = [
        {"label": "Total Sales", "value": financials.get("Revenue", "N/A"), "color": "#d72638", "icon": "💰"},
        {"label": "Cokemaking Facilities", "value": str(data.get("facilities", "N/A")), "color": "#0e2f44", "icon": "🏭"},
        {"label": "Adj. EBITDA", "value": financials.get("EBITDA", "N/A"), "color": "#f8961e", "icon": "📊"},
        {"label": "Tons handled", "value": data.get("logistics_volume", "N/A"), "color": "#2a9d8f", "icon": "🚢"},
        {"label": "Tons produced", "value": data.get("production_volume", "N/A"), "color": "#264653", "icon": "🔥"},
    ]

    summary_html = '''
<!-- .slide: data-background-color="#ffffff" style="text-align: center;" -->
<h2 style="color: #0e2f44; font-size: 48px; margin-bottom: 40px;">📌 Executive Summary</h2>
<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 30px;">
'''

    for item in summary_cards:
        summary_html += f'''
  <div style="background-color: #efefef; padding: 20px 30px; border-radius: 12px; width: 220px;">
    <div style="font-size: 32px; margin-bottom: 5px; color: {item["color"]}">{item["icon"]} <strong>{item["value"]}</strong></div>
    <p style="font-size: 16px; color: #333;">{item["label"]}</p>
  </div>
'''

    summary_html += "</div>"
    slides.append(summary_html)

    return "\n---\n\n".join(slides)

# Load and generate
if __name__ == "__main__":
    json_path = os.path.join(os.path.dirname(__file__), "company_data_enriched.json")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    markdown = build_markdown(data)

    company_slug = data.get("company", "company").lower().replace(" ", "_").replace(",", "")
    output_path = "F:/revealJS/FirstPresentation/slides_" + company_slug + ".md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    default_path = "F:/revealJS/FirstPresentation/slides.md"
    shutil.copyfile(output_path, default_path)

    print(f"✅ Markdown written to {output_path}")
    print(f"✅ Also copied to {default_path} for live Reveal.js preview")
