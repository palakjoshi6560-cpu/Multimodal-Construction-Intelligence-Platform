# Manual Testing Checklist

- [ ] Install dependencies in a fresh virtual environment.
- [ ] Launch with `streamlit run app.py`.
- [ ] Confirm all four tabs render without an API key.
- [ ] Upload a JPG and PNG in the safety tab; confirm demo results are labelled as demo.
- [ ] Upload a JPG and PNG in the crack tab; confirm demo results are labelled as demo.
- [ ] Download both JSON reports and validate that they parse as JSON.
- [ ] Test all structure types, all location tiers, and completion slider values.
- [ ] Confirm estimate values update after pressing Calculate.
- [ ] Select each weather condition and verify the corresponding protocol.
- [ ] Send multiple chat messages without a key and confirm session history appears.
- [ ] If using Gemini, test a valid key and an invalid key; ensure failure is disclosed.
- [ ] Deploy from the correct repository and `app.py` entrypoint on Streamlit Community Cloud.
