import json
import os
from datetime import datetime
from io import BytesIO
import streamlit as st
from PIL import Image
from construction_ai import (
    analyze_image, demo_safety_report, demo_crack_report, ask_gemini,
    budget_estimate, weather_advisory, architecture_prompt
)

st.set_page_config(page_title="Multimodal Construction Intelligence Platform",
                   page_icon="🏗️", layout="wide")

st.markdown("""
<style>
:root { --ink:#172033; --muted:#667085; --accent:#d97706; }
.block-container {padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1400px;}
.hero {padding:1.5rem 1.7rem; border-radius:18px; color:white;
background:linear-gradient(120deg,#172033,#334155 65%,#b45309); margin-bottom:1rem;}
.hero h1 {color:white; margin:0; font-size:2rem;}
.hero p {color:#e5e7eb; margin:.5rem 0 0 0;}
.pill {display:inline-block;padding:.25rem .65rem;border-radius:999px;
font-size:.82rem;font-weight:700;background:#fef3c7;color:#92400e;}
.small-note {color:#667085;font-size:.86rem;}
div[data-testid="stMetric"] {
    background: #f8fafc;
    color: #172033;
    padding: 14px;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricLabel"],
div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #172033 !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🏗️ Construction AI")
    st.caption("Skill Wallet Capstone · Project 1")

    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        api_key = st.text_input(
            "Gemini API key",
            type="password",
            help="Used only for requests during this session."
        )
    st.caption("No key? Demo mode remains available.")
    st.divider()
    st.subheader("Architecture")
    st.markdown("**Streamlit UI** → **AI service** → **validated JSON**")
    st.markdown("- Gemini multimodal analysis (optional)\n- Rule-based planning estimates\n- Weather protocol knowledge base\n- Session-only chat history")
    st.divider()
    st.caption("No external database required.")

st.markdown("""
<div class="hero">
<h1>Multimodal Construction Intelligence Platform</h1>
<p>Site safety · Crack diagnostics · Project valuation · Weather-aware site assistant</p>
</div>
""", unsafe_allow_html=True)

if api_key.strip():
    st.success("Gemini key entered for this session. Image and chat analysis can use the configured model.")
else:
    st.info("Demonstration mode is active. Sample image-analysis results are illustrative, not actual detection.")

tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Site Safety & PPE", "🧱 Crack Diagnostics",
    "📐 Planning & Valuation", "🌦️ Site Assistant"
])

def report_download(report, name):
    st.download_button("⬇️ Download JSON report",
        data=json.dumps(report, indent=2, ensure_ascii=False),
        file_name=name, mime="application/json")

with tab1:
    st.subheader("Site Safety & PPE Audit")
    st.write("Upload a construction-site photo to assess visible PPE and potential hazards.")
    photo = st.file_uploader("Construction site photo", type=["jpg","jpeg","png"], key="safety_photo")
    if photo:
        try:
            img = Image.open(photo).convert("RGB")
            st.image(img, caption="Uploaded site photo", use_container_width=True)
            if st.button("Run PPE safety audit", type="primary", key="run_safety"):
                with st.spinner("Reviewing visible safety conditions…"):
                    report = analyze_image(img, api_key, "safety")
                    st.session_state["safety_report"] = report
        except Exception as e:
            st.error(f"Could not read this image: {e}")
    report = st.session_state.get("safety_report")
    if report:
        c1,c2,c3 = st.columns(3)
        c1.metric("Safety score", f"{report.get('safety_score', 0)}/100")
        c2.metric("Overall status", report.get("overall_status","Review required"))
        c3.metric("Hazards found", len(report.get("hazards", [])))
        st.markdown("#### PPE detection checklist")
        st.json(report.get("ppe_detection", {}))
        st.markdown("#### Identified hazards and corrective remedies")
        if report.get("hazards"):
            for h in report["hazards"]:
                st.markdown(f"**{h.get('hazard','Hazard')}** · `{h.get('severity','Medium')}`")
                st.write(h.get("remedy","Arrange a competent site inspection."))
        else:
            st.write("No hazards were returned by the selected analysis mode.")
        st.warning("Visual AI is a screening aid, not a certified safety inspection. OSHA and Indian requirements depend on site context; IS 456 primarily concerns concrete design, not a complete PPE code.")
        report_download(report, "site_safety_report.json")

with tab2:
    st.subheader("Crack Diagnostics & Structural Integrity")
    st.write("Upload a clear concrete or wall-surface image. AI estimates are not a substitute for an engineer's site inspection.")
    crack_photo = st.file_uploader("Concrete / wall photo", type=["jpg","jpeg","png"], key="crack_photo")
    if crack_photo:
        try:
            img2 = Image.open(crack_photo).convert("RGB")
            st.image(img2, caption="Uploaded surface photo", use_container_width=True)
            if st.button("Analyze crack / defect", type="primary", key="run_crack"):
                with st.spinner("Assessing visible surface defects…"):
                    st.session_state["crack_report"] = analyze_image(img2, api_key, "crack")
        except Exception as e:
            st.error(f"Could not read this image: {e}")
    cr = st.session_state.get("crack_report")
    if cr:
        a,b,c = st.columns(3)
        a.metric("Defect type", cr.get("defect_type","Unknown"))
        b.metric("Estimated width", f"{cr.get('estimated_width_mm','Unknown')} mm")
        c.metric("Urgency", cr.get("urgency","Needs review"))
        st.markdown("#### Possible root causes")
        st.write(cr.get("root_causes", []))
        st.markdown("#### Recommended next steps")
        st.write(cr.get("recommended_repairs", []))
        st.info(cr.get("limitations","Image-based assessment is uncertain; consult a qualified structural engineer."))
        report_download(cr, "crack_diagnostics_report.json")

with tab3:
    st.subheader("Project Planning & Real Estate Valuation")
    st.caption("Indicative planning estimates only. Rates and quantities are assumptions that must be replaced with local BOQ, soil/design inputs and market evidence.")
    col1,col2 = st.columns(2)
    with col1:
        structure = st.selectbox("Structure type", ["Residential house","Apartment building","Commercial building","Warehouse / industrial"])
        area = st.number_input("Built-up area (sq ft)", min_value=100, max_value=2000000, value=1500, step=100)
        tier = st.selectbox("Location tier", ["Tier 1","Tier 2","Tier 3"])
    with col2:
        completion = st.slider("Construction completion (%)", 0, 100, 35)
        quality = st.selectbox("Construction quality", ["Standard","Premium","Economical"])
        land_value = st.number_input("Estimated land value (₹ lakh; optional)", min_value=0.0, value=0.0, step=5.0)
    if st.button("Calculate project estimates", type="primary"):
        st.session_state["budget"] = budget_estimate(structure, area, tier, completion, quality, land_value)
    b = st.session_state.get("budget")
    if b:
        x1,x2,x3 = st.columns(3)
        x1.metric("Estimated construction budget", f"₹{b['total_budget_lakh']:.2f} lakh")
        x2.metric("Expenditure incurred", f"₹{b['incurred_capex_lakh']:.2f} lakh")
        x3.metric("Indicative asset value", b["market_value_display"])
        st.progress(completion/100, text=f"Milestone progress · {completion}%")
        m1,m2 = st.columns(2)
        m1.metric("Indicative steel", f"{b['steel_tonnes']:.2f} tonnes")
        m2.metric("Indicative cement", f"{b['cement_bags']} bags (50 kg)")
        st.write("**Assumptions used**")
        st.json(b["assumptions"])
        st.download_button("⬇️ Download estimate JSON", json.dumps(b,indent=2), "project_estimate.json", "application/json")
    st.divider()
    st.markdown("#### Conceptual 3D architectural rendering")
    arch = st.text_area("Describe the building concept", value="Modern Indian two-storey residential house, sustainable materials, realistic daylight, architectural visualization")
    st.code(architecture_prompt(arch), language="text")
    st.caption("This generates a ready-to-use prompt. An image provider/API is not called automatically; connect an approved image-generation endpoint if you want live rendering.")

with tab4:
    st.subheader("Daily Site Assistant & Weather-Aware Advisory")
    weather = st.selectbox("Current / forecast condition", ["Normal","High Wind","Heavy Rain","Extreme Heat"])
    advice = weather_advisory(weather)
    st.markdown(f"### {advice['title']}")
    for item in advice["actions"]:
        st.markdown(f"- {item}")
    st.caption("Follow the site's approved safety plan, local weather alerts and competent-person directions.")
    st.divider()
    st.markdown("#### Construction engineering assistant")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    prompt = st.chat_input("Ask about construction planning, safety, concrete, or site protocols…")
    if prompt:
        st.session_state.chat_history.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Preparing guidance…"):
                answer = ask_gemini(prompt, api_key, st.session_state.chat_history)
                st.markdown(answer)
        st.session_state.chat_history.append({"role":"assistant","content":answer})
    if st.button("Clear chat history"):
        st.session_state.chat_history = []
        st.rerun()

st.divider()
st.caption("Decision-support prototype · Not a substitute for licensed structural engineering, quantity surveying, legal compliance, or professional valuation.")
