import streamlit as st
from pathlib import Path
from src.pipeline import analyze_document
from src.report import build_reference_list, build_csv_rows
from src.llm_agent import llm_available

st.set_page_config(page_title="CiteWise", page_icon="📚", layout="wide")

st.title("📚 CiteWise")
st.caption("AI Citation Management Agent — detect claims, find supporting academic sources, and generate citations.")

with st.sidebar:
    st.header("Settings")
    style = st.selectbox("Citation style", ["IEEE", "APA"])
    st.markdown("---")
    if llm_available():
        st.success("🤖 LLM agent active (Groq)")
    else:
        st.warning("Rule-based mode — add GROQ_API_KEY in .env for AI-powered detection")
    st.markdown("---")
    st.info("Demo mode works with the included dataset. For live academic search, add an API key in `.env`.")

uploaded = st.file_uploader("Upload a research paper", type=["pdf", "txt"])

if "result" not in st.session_state:
    st.session_state.result = None

if st.button("🔎 Analyze Paper", type="primary", disabled=uploaded is None):
    with st.spinner("CiteWise agent is analyzing the document..."):
        data = uploaded.getvalue()
        st.session_state.result = analyze_document(data, uploaded.name, style)

result = st.session_state.result

if result:
    st.success("Analysis completed.")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Claims detected", len(result["claims"]))
    m2.metric("Potential citations", len(result["citation_candidates"]))
    m3.metric("Sources matched", len(result["matches"]))
    m4.metric("Citation coverage", f'{result["coverage"]:.0f}%')

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🤖 Agent Activity", "🔍 Claims & Sources", "📚 References", "⬇️ Export"]
    )

    with tab1:
        for step in result["activity"]:
            st.write(step)

    with tab2:
        for item in result["claims"]:
            st.subheader(item["claim_id"] + " — " + item["text"])
            if item["needs_citation"]:
                match = next((x for x in result["matches"] if x["claim_id"] == item["claim_id"]), None)
                if match:
                    st.success(
                        f'Suggested source: {match["title"]} | '
                        f'confidence {match["score"]:.0%}'
                    )
                    st.caption(match["reason"])
                else:
                    st.warning("No sufficiently relevant source found.")
            else:
                st.info("Likely self-contained statement; citation not automatically required.")
            st.caption(f'Detection method: {item["detection_method"]}')

    with tab3:
        st.code(build_reference_list(result["matches"], style), language="text")

    with tab4:
        csv_text = build_csv_rows(result["matches"])
        st.download_button(
            "Download citation matches CSV",
            data=csv_text,
            file_name="citewise_matches.csv",
            mime="text/csv",
        )
        st.download_button(
            "Download generated references",
            data=build_reference_list(result["matches"], style),
            file_name=f"references_{style.lower()}.txt",
            mime="text/plain",
        )
else:
    st.info("Upload the included demo paper or your own PDF/TXT file, then click Analyze Paper.")
