# Multimodal Construction Intelligence Platform

An AI-powered construction platform for site safety, crack diagnostics, project planning, indicative valuation, and construction assistance.

## Modules

1. **Site Safety & PPE Audit** — identifies visible hazards and provides general safety suggestions.
2. **Crack Diagnostics** — reviews crack/defect images and offers cautious, preliminary observations.
3. **Project Planning & Valuation** — provides indicative construction budget, material quantities, and progress estimates.
4. **Site Assistant** — answers construction-related questions and provides weather-aware safety guidance based on the condition selected by the user.

## Features

- Optional Gemini multimodal image analysis with structured JSON output.
- Clearly labelled demonstration results when no API key is supplied or live analysis fails.
- PPE checklist, visible hazard findings, suggested remedies, and downloadable JSON.
- Preliminary crack/defect observations, possible causes, repair suggestions, and urgency guidance.
- Indicative INR construction budget, CAPEX, conceptual steel/cement quantities, and progress estimates.
- Weather-specific safety guidance and multi-turn assistant chat.
- No external database required.

## Run locally (Windows PowerShell)

Python 3.10 or newer is recommended.

Open PowerShell in the project folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Gemini API

Enter the Gemini API key in the sidebar for the current session. The app does not save the key to source files. If no key is entered, it uses clearly labelled sample/demo results. If a live request fails, the app labels the result as a demo fallback.

For deployment, use Streamlit Community Cloud's Secrets settings where supported. Never commit `.env`, `secrets.toml`, or API keys to GitHub.

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository you own.
2. Open https://share.streamlit.io/ and choose **Create app**.
3. Select the repository, branch, and `app.py` file.
4. Deploy; dependencies are installed from `requirements.txt`.
5. If using Gemini, configure the API key securely and never commit secrets.

## Important limitations

- This is a prototype decision-support tool, not a certified construction safety inspection, structural diagnosis, engineering design, quantity survey, or professional property valuation.
- A photo may not show boots, harnesses, or all site conditions. Unseen items should not be treated as confirmed absent.
- Crack width cannot be reliably measured from a photo without a scale reference and calibration. Do not rely on the model alone for structural decisions.
- OSHA and Indian requirements are context-dependent. IS 456 is primarily a concrete design code, not a comprehensive PPE regulation.
- Cost, steel, cement, and asset-value calculations use illustrative assumptions. Replace them with local rates, drawings, BOQ, actual land value, and market comparables before use.
- Architectural rendering currently prepares a prompt; it does not automatically call a paid or third-party image API.
- The app does not fetch live weather forecasts. The user selects the known or forecast condition manually.
