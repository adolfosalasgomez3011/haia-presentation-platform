import json
import os
import shutil
from datetime import datetime
import sys
import io

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def get_company_config(company_name):
    """Get company-specific configuration"""
    print(f"DEBUG: get_company_config called with: '{company_name}'")
    
    company_configs = {
        "SunCoke Energy": {
            "slug": "suncoke",
            "image": "suncoke_plant.jpg",
            "industry": "cokemaking",
            "summary_cards": [
                {"label": "Total Sales", "field": "Revenue", "color": "#d72638", "icon": "$"},
                {"label": "Cokemaking Facilities", "field": "facilities", "color": "#0e2f44", "icon": "F"},
                {"label": "Adj. EBITDA", "field": "EBITDA", "color": "#f8961e", "icon": "E"},
                {"label": "Tons handled", "field": "logistics_volume", "color": "#2a9d8f", "icon": "L"},
                {"label": "Tons produced", "field": "production_volume", "color": "#264653", "icon": "P"},
            ],
            "description": [
                "<li><strong>Integrated operations:</strong> Includes both cokemaking and coal logistics terminals.</li>",
                "<li><strong>Global reach:</strong> Serving steel manufacturers in the US and Brazil.</li>",
                "<li><strong>Strategic contracts:</strong> Long-term, take-or-pay agreements ensure stability.</li>"
            ]
        },
        "Teine Energy": {
            "slug": "teine",
            "image": "teine_facility.jpg",
            "industry": "energy",
            "summary_cards": [
                {"label": "Total Revenue", "field": "Revenue", "color": "#1e40af", "icon": "$"},
                {"label": "Energy Assets", "field": "assets", "color": "#0e2f44", "icon": "A"},
                {"label": "EBITDA", "field": "EBITDA", "color": "#f59e0b", "icon": "E"},
                {"label": "MW Capacity", "field": "capacity", "color": "#059669", "icon": "M"},
                {"label": "Projects", "field": "projects", "color": "#dc2626", "icon": "P"},
            ],
            "description": [
                "<li><strong>Diversified portfolio:</strong> Multi-energy platform with renewable and conventional assets.</li>",
                "<li><strong>Growth focus:</strong> Expanding renewable energy capabilities and storage solutions.</li>",
                "<li><strong>Strategic positioning:</strong> Well-positioned for energy transition opportunities.</li>"
            ]
        }
    }
    
    print(f"DEBUG: Available companies: {list(company_configs.keys())}")
    
    if company_name in company_configs:
        print(f"DEBUG: Found exact match for '{company_name}'")
        return company_configs[company_name]
    else:
        print(f"DEBUG: No match found for '{company_name}', defaulting to SunCoke Energy")
        return company_configs["SunCoke Energy"]

def build_markdown(data):
    slides = []
    
    # Get company-specific configuration - ADD DEBUG INFO
    company_name = data.get("company", "SunCoke Energy")
    print(f"DEBUG: company_name from data: '{company_name}'")
    print(f"DEBUG: company_name type: {type(company_name)}")
    
    config = get_company_config(company_name)
    print(f"DEBUG: config slug: '{config['slug']}'")
    print(f"DEBUG: config industry: '{config['industry']}'")

    # Cover Slide
    slides.append(
        f"""<!-- .slide: data-background-color='#ffffff' style='height: 100vh; display: flex; flex-direction: column; justify-content: flex-start; align-items: center;' -->

<div style="margin-top: 120px; background-color: rgba(14, 47, 68, 0.05); padding: 40px 80px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
  <h1 style="font-size: 84px; letter-spacing: 2px; color: #0e2f44; margin-bottom: 20px;">
    <strong>{company_name.upper()}</strong>
  </h1>
  <p style="font-size: 34px; font-style: italic; color: #333; margin-top: 0;">
    Company Overview – {datetime.now().year}
  </p>
</div>
        """
    )

    # Executive Summary - Now Dynamic
    financials = data.get("financials", {})
    
    # Build dynamic summary cards based on company
    summary_cards = []
    for card_config in config["summary_cards"]:
        value = "N/A"
        if card_config["field"] in financials:
            value = financials[card_config["field"]]
        elif card_config["field"] in data:
            value = str(data[card_config["field"]])
        
        summary_cards.append({
            "label": card_config["label"],
            "value": value,
            "color": card_config["color"],
            "icon": card_config["icon"]
        })

    # Dynamic image path
    plant_image_path = f"img/{config['slug']}/{config['image']}"

    summary_html = f"""<!-- .slide: data-background-color="#ffffff" style="text-align: center;" -->
<h2 style="color: #0e2f44; font-size: 48px; margin-bottom: 40px; text-align: center;">Executive Summary</h2>

<div style="display: flex; justify-content: center; align-items: flex-start; gap: 40px; padding: 0 60px;">

  <div style="flex: 1; max-width: 45%;">
    <img src="{plant_image_path}" 
         style="width: 100%; border-radius: 10px; box-shadow: 0 0 8px rgba(0,0,0,0.15);">
  </div>

  <div style="flex: 1; text-align: left; font-size: 18px; color: #333;">
    <div style="display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 30px;">
"""
    
    # Add dynamic summary cards
    for item in summary_cards:
        summary_html += f"""
      <div style="background-color: #efefef; padding: 16px 20px; border-radius: 10px; width: 180px;">
        <div style="font-size: 28px; color: {item["color"]}">{item["icon"]} <strong>{item["value"]}</strong></div>
        <p style="font-size: 14px; color: #333; margin: 6px 0 0;">{item["label"]}</p>
      </div>
"""

    # Add dynamic company description
    summary_html += f"""
    </div>

    <ul style="line-height: 1.8;">
      {"".join(config["description"])}
    </ul>

    <p style="margin-top: 20px; font-size: 16px; color: #666; font-style: italic;">
      Company Overview – {datetime.now().year}
    </p>
  </div>
</div>
"""
    slides.append(summary_html)

    # Business Segments - Dynamic
    segments = data.get("business_segments", ["Segment information not available"])
    segments_text = "\n".join([f"- {segment}" for segment in segments])
    slides.append(f"""## Business Segments

{segments_text}""")

    # Financials vs. Risks - Dynamic
    revenue = financials.get("Revenue", "N/A")
    risks = data.get("risks", ["Market volatility", "Regulatory changes"])
    risks_text = "\n".join([f"- {risk}" for risk in risks[:2]])
    
    slides.append(f"""## Financials vs. Risks

**Financial Highlights:**
- Revenue: {revenue}
- EBITDA: {financials.get("EBITDA", "N/A")}

**Key Risks:**
{risks_text}
""")

    # Charts - Dynamic based on company
    chart_slug = config["slug"]
    slides.append(f"""## Market Trends

<img src='img/{chart_slug}_price_1y.png'>
<img src='img/{chart_slug}_revenue_bars.png'>""")

    # Rest of slides remain the same
    slides.append("""## Leadership Snapshot

- CEO: {}
- Background: {}""".format(
        data.get("leadership", {}).get("name", "N/A"),
        data.get("leadership", {}).get("background", "N/A")
    ))

    slides.append("""## Strategic Insights

- Placeholder quote""")

    slides.append("""## Operational Flow

```mermaid
graph TD
A --> B --> C
```""")

    slides.append("""## Recent News

- Placeholder news item""")

    slides.append("""## Thank You

Email: {}
Phone: {}
""".format(
        data.get("email", "N/A"),
        data.get("phone", "N/A")
    ))

    return "\n---\n\n".join(slides)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("company", help="Company name")
    args = parser.parse_args()
    
    # Read the JSON file
    json_path = os.path.join(os.path.dirname(__file__), "company_data_enriched.json")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # FORCE the company name from the argument
    data["company"] = args.company
    print(f"Building presentation for: {args.company}")

    markdown = build_markdown(data)

    company_slug = args.company.lower().replace(" ", "_").replace(",", "")
    output_path = f"F:/revealJS/FirstPresentation/slides_{company_slug}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    default_path = "F:/revealJS/FirstPresentation/slides.md"
    shutil.copyfile(output_path, default_path)

    print(f"SUCCESS: Markdown written to {output_path}")
    print(f"SUCCESS: Also copied to {default_path} for live Reveal.js preview")