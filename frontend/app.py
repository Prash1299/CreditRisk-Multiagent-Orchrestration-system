import os

import httpx
import streamlit as st

API_URL = os.getenv("CREDIT_API_URL", "http://127.0.0.1:8000")
EXAMPLE = (
    "I earn ₹85,000 per month, have an existing EMI of ₹15,000, a credit score of 720, "
    "and want a personal loan of ₹8 lakh for 4 years."
)

st.set_page_config(page_title="CreditRisk Multi-Agent", layout="wide")
st.title("Credit Risk & Loan Recommendation")
st.caption("LangGraph supervisor with research, analyst and reviewer agents. Decision support only.")

with st.sidebar:
    st.markdown("**Session memory**")
    session_id = st.text_input("Session ID", value="demo-user")
    async_mode = st.checkbox("Queue via Redis + Celery", value=False)
    st.markdown(
        "Use the same session ID to recall prior assessments from PostgreSQL + Chroma."
    )

request = st.text_area("Applicant request", value=EXAMPLE, height=120)
run = st.button("Run assessment", type="primary")

if run:
    try:
        response = httpx.post(
            f"{API_URL}/assess",
            json={
                "request": request,
                "session_id": session_id,
                "async_mode": async_mode,
            },
            timeout=120.0,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        st.error(f"Request failed: {exc}")
        st.stop()

    if async_mode or data.get("job_id") and data.get("status") != "completed":
        st.info(f"Queued job `{data.get('job_id')}`. Poll `/jobs/{data.get('job_id')}`.")
        st.json(data)
        st.stop()

    st.subheader(f"Disposition: {data.get('disposition')}")
    cols = st.columns(3)
    cols[0].metric("Risk score", data.get("risk_score"))
    cols[1].metric("Illustrative PD", data.get("probability_of_default"))
    cols[2].metric("Products scored", len(data.get("recommendations") or []))
    st.write(data.get("rationale"))
    st.caption(data.get("disclaimer"))

    st.markdown("### Loan options")
    st.dataframe(data.get("recommendations") or [], use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Research**")
        st.json(data.get("research") or {})
    with c2:
        st.markdown("**Analysis**")
        st.json(data.get("analysis") or {})
    with c3:
        st.markdown("**Review**")
        st.json(data.get("review") or {})
