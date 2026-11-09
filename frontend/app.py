import os

import httpx
import streamlit as st

API_URL = os.getenv("CREDIT_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="CreditRisk Multi-Agent", layout="wide")
st.title("CreditRisk Multi-Agent")
st.caption("Research → Analyst → Reviewer workflow")

with st.form("assess"):
    borrower_id = st.text_input("Borrower ID", value="B001")
    product_id = st.text_input("Product ID", value="P200")
    request = st.text_area("Request", value="Assess this credit application.")
    submitted = st.form_submit_button("Run assessment")

if submitted:
    try:
        response = httpx.post(
            f"{API_URL}/assess",
            json={
                "borrower_id": borrower_id,
                "product_id": product_id,
                "request": request,
            },
            timeout=60.0,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        st.error(f"Assessment failed: {exc}")
    else:
        st.subheader(f"Recommendation: {data.get('recommendation')}")
        st.metric("Risk score", data.get("risk_score"))
        st.write(data.get("rationale"))
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Research**")
            st.json(data.get("research") or {})
        with col2:
            st.markdown("**Analysis**")
            st.json(data.get("analysis") or {})
        with col3:
            st.markdown("**Review**")
            st.json(data.get("review") or {})
