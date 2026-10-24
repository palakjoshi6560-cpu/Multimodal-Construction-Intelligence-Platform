import json
from PIL import Image
from io import BytesIO

MODEL_NAME = "gemini-3.5-flash-lite"

def _gemini_client(api_key):
    if not api_key or not api_key.strip():
        return None
    try:
        from google import genai
        return genai.Client(api_key=api_key.strip())
    except Exception:
        return None

def _extract_json(text):
    text = (text or "").strip()
    if text.startswith("```"):
        text = text.split("\n",1)[-1]
        if text.endswith("```"):
            text = text[:-3]
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("AI response did not contain a JSON object.")
    return json.loads(text[start:end+1])

def analyze_image(image, api_key, mode):
    client = _gemini_client(api_key)
    if client is None:
        return demo_safety_report() if mode == "safety" else demo_crack_report()
    try:
        from google.genai import types
        import io
        buf = io.BytesIO()
        image.save(buf, format="JPEG", quality=90)
        image_part = types.Part.from_bytes(data=buf.getvalue(), mime_type="image/jpeg")
        if mode == "safety":
            prompt = """Act as a cautious construction safety visual screening assistant. Analyze only visible evidence; mark unseen/uncertain PPE as 'not_visible' rather than assuming. Return ONLY valid JSON with keys safety_score (integer 0-100), overall_status (Safe/Needs Improvement/High Risk), ppe_detection (object with helmet, high_visibility_vest, steel_toe_boots, safety_harness; each value should be Present/Absent/Not visible/Not applicable), hazards (array of objects with hazard, severity (Low/Medium/High/Critical), evidence, remedy). Give practical corrective actions. This is a preliminary visual review, not a formal OSHA/Indian compliance certification. IS 456 primarily concerns plain and reinforced concrete, not PPE rules."""
        else:
            prompt = """Act as a cautious concrete surface visual screening assistant. Return ONLY valid JSON with keys defect_type (Hairline/Settlement/Structural Shear/Thermal Expansion/Spalling/Unclear), estimated_width_mm (number or null), severity (Low/Medium/High/Critical/Unclear), root_causes (array), recommended_repairs (array), urgency (Routine/Prompt/Immediate engineer inspection), limitations (string). Do not claim precise crack width from a photo without a scale reference. Never certify structural safety. Recommend a qualified structural engineer for concerning cracks."""
        response = client.models.generate_content(model=MODEL_NAME, contents=[prompt, image_part],
            config={"response_mime_type":"application/json"})
        data = _extract_json(response.text)
        if mode == "safety":
            data.setdefault("safety_score", 0)
            data.setdefault("overall_status", "Needs Improvement")
            data.setdefault("ppe_detection", {})
            data.setdefault("hazards", [])
        else:
            data.setdefault("defect_type", "Unclear")
            data.setdefault("estimated_width_mm", None)
            data.setdefault("root_causes", [])
            data.setdefault("recommended_repairs", [])
            data.setdefault("urgency", "Prompt engineer review")
            data.setdefault("limitations", "Image-based estimate; no scale reference may be available.")
        data["analysis_mode"] = "gemini"
        return data
    except Exception as exc:
        # Explicitly disclose fallback; never disguise failed live analysis as AI output.
        report = demo_safety_report() if mode == "safety" else demo_crack_report()
        report["analysis_mode"] = "demo_fallback"
        report["fallback_reason"] = f"Gemini request failed: {type(exc).__name__}. Check key, model access, and connectivity."
        return report

def demo_safety_report():
    return {
        "analysis_mode":"demo",
        "safety_score":72,
        "overall_status":"Needs Improvement",
        "ppe_detection":{"helmet":"Not visible — verify on site","high_visibility_vest":"Not visible — verify on site",
                         "steel_toe_boots":"Not assessable from image","safety_harness":"Not assessable from image"},
        "hazards":[{"hazard":"Demonstration hazard example — unprotected edge","severity":"High",
                    "evidence":"Illustrative sample only; not detected from your uploaded photo.",
                    "remedy":"Inspect edges, install compliant guardrails or fall-arrest systems, and restrict access until corrected."}],
        "notice":"Demo data only. No actual image inference was performed."
    }

def demo_crack_report():
    return {
        "analysis_mode":"demo",
        "defect_type":"Unclear",
        "estimated_width_mm":None,
        "severity":"Unclear",
        "root_causes":["Cannot infer from an image without actual model analysis and site context."],
        "recommended_repairs":["Photograph with a scale reference; map and monitor the crack; request a qualified structural engineer's assessment before selecting a repair."],
        "urgency":"Engineer review required if widening, diagonal, through-wall, leaking, or associated with movement.",
        "limitations":"Demo data only. No actual image inference was performed; crack width cannot reliably be estimated without scale."
    }

def ask_gemini(prompt, api_key, history):
    client = _gemini_client(api_key)
    if client is None:
        return ("Demo assistant: I can provide general construction planning and safety guidance, but live Gemini is not configured. "
                "For a real site decision, follow the approved method statement and consult the responsible engineer. "
                "Add a Gemini API key in the sidebar to enable model responses.")
    try:
        transcript = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in history[-8:])
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=("You are a cautious construction engineering assistant. Give clear, practical general guidance. "
                      "Do not certify structural safety or replace a licensed engineer. Distinguish assumptions from facts.\n\n"
                      + transcript + "\nASSISTANT:")
        )
        return response.text or "I couldn't produce a response. Please try again."
    except Exception as exc:
        return f"Gemini is unavailable ({type(exc).__name__}). Please verify the API key and connection. General site decisions should follow your approved safety plan."

def budget_estimate(structure, area, tier, completion, quality, land_value_lakh=0):
    # Editable illustrative planning assumptions, not a professional quantity survey.
    base = {"Economical": 1550, "Standard": 1950, "Premium": 2700}[quality]
    tier_factor = {"Tier 1":1.18, "Tier 2":1.0, "Tier 3":0.88}[tier]
    type_factor = {"Residential house":1.0, "Apartment building":1.12,
                   "Commercial building":1.25, "Warehouse / industrial":0.82}[structure]
    rate = base * tier_factor * type_factor
    total_rupees = area * rate
    total_lakh = total_rupees / 100000
    incurred = total_lakh * completion / 100
    # Broad conceptual material thumb-rules only; project design/BOQ must govern.
    steel_kg_per_sqft = 3.5 if structure in ("Residential house","Apartment building") else 4.2
    cement_bags_per_sqft = 0.40 if structure != "Warehouse / industrial" else 0.28
    steel_tonnes = area * steel_kg_per_sqft / 1000
    cement_bags = round(area * cement_bags_per_sqft)
    asset_lakh = total_lakh * 1.12 + land_value_lakh
    display = f"₹{asset_lakh/100:.2f} crore" if asset_lakh >= 100 else f"₹{asset_lakh:.2f} lakh"
    return {
        "structure_type":structure,"built_up_sqft":area,"location_tier":tier,
        "completion_percent":completion,"quality":quality,
        "total_budget_lakh":round(total_lakh,2),"incurred_capex_lakh":round(incurred,2),
        "indicative_market_asset_value_lakh":round(asset_lakh,2),"market_value_display":display,
        "steel_tonnes":round(steel_tonnes,2),"cement_bags":cement_bags,
        "assumptions":{"construction_rate_inr_per_sqft":round(rate,2),
            "market_value_method":"Construction estimate × 1.12 + user-provided land value (rough proxy, not a market valuation)",
            "steel_rule":"Conceptual kg/sqft allowance; replace with structural drawings and BOQ",
            "cement_rule":"Conceptual bags/sqft allowance; replace with design mix and BOQ",
            "warning":"All estimates are illustrative and vary by city, soil, specifications, taxes, design, approvals and market evidence."}
    }

def weather_advisory(condition):
    items = {
        "Normal":{"title":"Normal conditions — routine controls","actions":[
            "Conduct the daily toolbox talk and pre-start equipment inspections.",
            "Keep access routes clear, use required PPE, and verify permits and lifting plans.",
            "Follow approved concrete placement, finishing and curing specifications."]},
        "High Wind":{"title":"High wind — lifting and work-at-height precautions","actions":[
            "Suspend crane, hoist and suspended-load operations when wind exceeds equipment/manufacturer or site-plan limits.",
            "Secure loose materials, formwork, sheets and temporary structures; restrict exposed-edge work as needed.",
            "Check official local wind alerts and resume only after the competent person authorizes it."]},
        "Heavy Rain":{"title":"Heavy rain — water, access and electrical hazards","actions":[
            "Stop work in flooded or unstable areas; isolate electrical equipment where safe and have a qualified person inspect it.",
            "Check excavation stability, dewatering, access roads and slope/retaining conditions before entry.",
            "Protect cement and aggregates from water; review concrete placement and curing plans with the site engineer."]},
        "Extreme Heat":{"title":"Extreme heat — heat-stress controls","actions":[
            "Provide potable water, shaded rest, acclimatization and work/rest cycles appropriate to conditions.",
            "Use a buddy system and train workers to report dizziness, confusion, cramps or fainting immediately.",
            "Protect fresh concrete from rapid moisture loss and follow the specified curing method; adjust pour timing only under the approved plan."]}
    }
    return items.get(condition, items["Normal"])

def architecture_prompt(description):
    return ("Architectural visualization prompt: " + description.strip() +
            ". High-quality conceptual 3D render, realistic construction materials, clear massing, natural lighting, "
            "professional architectural presentation. Concept only; not an approved construction drawing.")
