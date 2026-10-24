# Multimodal Construction Intelligence Platform

**Skill Wallet Capstone Project 1**  
Category: Generative AI · Real Estate Decision Support  
Platform ID: `6ac4c98d1dcde6d7857c1642`

A Streamlit decision-support prototype with four modules:
1. Site Safety & PPE Audit
2. Crack Diagnostics & Structural Integrity
3. Project Planning & Real Estate Valuation
4. Daily Site Assistant & Weather-Aware Advisory

## Features

- Optional Gemini multimodal image analysis with structured JSON output.
- Explicit demonstration mode when no API key is supplied, or if live analysis fails.
- PPE checklist, visible hazard findings, remedies and downloadable JSON.
- Crack/defect classification, cautious width estimate, possible causes, repair suggestions and urgency.
- Indicative INR construction budget, incurred CAPEX, conceptual steel/cement quantities and progress.
- Weather-specific safety protocols and multi-turn assistant chat.
- No external database.

## Run locally

Python 3.10+ is recommended for current package compatibility.

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

macOS/Linux:
```bash
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Gemini API

Enter the API key in the sidebar during the current session. The app does not save it to source files. If no key is entered, it uses clearly labelled sample/demo results. If a live request fails, the app labels the result as a demo fallback.

For deployment, use Streamlit Community Cloud's Secrets settings rather than committing keys. This app currently accepts a key in the sidebar; do not commit `secrets.toml`, `.env`, or API keys to GitHub.

## Deploy on Streamlit Community Cloud

1. Push this folder to a repository you own.
2. Go to https://share.streamlit.io/ and choose **Create app**.
3. Select your repository, branch and `app.py`.
4. Deploy. Dependencies are installed from `requirements.txt`.
5. If using Gemini, enter the key in the sidebar. Never commit secrets.

## Important limitations

- This is a prototype decision-support tool, not a certified construction safety inspection, structural diagnosis, engineering design, quantity survey, or professional property valuation.
- A photo may not show boots, harnesses, or all site conditions. The model must not treat unseen items as confirmed absent.
- Crack width cannot be reliably measured from a photo without a scale reference and calibration. Do not rely on the model alone for structural decisions.
- OSHA and Indian requirements are context-dependent. IS 456 is primarily a concrete design code, not a comprehensive PPE regulation.
- Cost, steel, cement and asset-value calculations use explicit illustrative assumptions. Replace them with local rates, drawings, BOQ, actual land value and market comparables before use.
- Architectural rendering currently prepares a prompt; it does not call a paid or third-party image API automatically.
- The app does not fetch live weather forecasts. The user selects the known/forecast condition manually.

## Project structure

```text
Multimodal_Construction_Intelligence_Platform/
├── app.py
├── construction_ai.py
├── requirements.txt
├── README.md
└── .gitignore
```
