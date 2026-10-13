import io
import pandas as pd
import streamlit as st
from phishing_agent import analyze_email, normalize_email_row

st.set_page_config(page_title="Phishing Email Investigation Agent", page_icon="🛡️", layout="wide")
st.title("🛡️ Phishing Email Investigation Agent")
st.caption("A safe, explainable triage demo using synthetic examples. It does not open URLs or download attachments.")

with st.sidebar:
    st.header("About this demo")
    st.write("Rule-based risk scoring, safe URL defanging, evidence, and recommended actions.")
    st.warning("Demo only: do not treat this as a production security control.")
    st.write("All sample domains and URLs are reserved or synthetic. Links are displayed defanged.")

tab1, tab2, tab3 = st.tabs(["Analyze one email", "Analyze CSV", "Sample dataset"])

with tab1:
    st.subheader("Paste an email")
    default_subject = "Urgent: Verify your mailbox immediately"
    default_sender = "IT Support <support@account-security.example>"
    default_reply = "helpdesk@unrelated-mail.example"
    default_body = """Your mailbox will be suspended today. Verify your password immediately:
http://account-security.example/verify
Please act now to avoid losing access."""
    with st.form("single_email"):
        sender = st.text_input("From", value=default_sender)
        reply_to = st.text_input("Reply-To (optional)", value=default_reply)
        subject = st.text_input("Subject", value=default_subject)
        body = st.text_area("Body", value=default_body, height=180)
        auth = st.selectbox("Authentication results", ["Not provided", "SPF pass; DKIM pass; DMARC pass", "SPF fail; DKIM fail; DMARC fail", "SPF pass; DKIM fail; DMARC fail"])
        attachment = st.text_input("Attachment metadata (optional)", placeholder="e.g. invoice.html, macro-enabled document")
        submitted = st.form_submit_button("Analyze email", type="primary")
    if submitted:
        result = analyze_email({
            "sender": sender, "reply_to": reply_to, "subject": subject, "body": body,
            "auth_results": "" if auth == "Not provided" else auth,
            "attachment_metadata": attachment
        })
        c1, c2, c3 = st.columns(3)
        c1.metric("Risk label", result["risk_label"])
        c2.metric("Risk score", f'{result["risk_score"]}/100')
        c3.metric("URLs found", result["features"]["url_count"])
        st.progress(result["risk_score"] / 100)
        st.subheader("Analyst summary")
        st.write(result["summary"])
        st.subheader("Evidence and indicators")
        if result["evidence"]:
            for item in result["evidence"]:
                st.markdown(f"- {item}")
        else:
            st.write("No strong indicators found by the baseline rules.")
        st.subheader("Recommended actions")
        for item in result["recommended_actions"]:
            st.markdown(f"- {item}")
        with st.expander("Technical details (safe, structured output)"):
            st.json(result)

with tab2:
    st.subheader("Upload a CSV of emails")
    st.write("Expected columns: `subject`, `body`; optional columns: `sender`, `reply_to`, `auth_results`, `attachment_metadata`, `label`.")
    uploaded = st.file_uploader("Choose CSV", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded).fillna("")
            if not {"subject", "body"}.issubset(df.columns):
                st.error("CSV must include at least `subject` and `body` columns.")
            else:
                results = []
                for _, row in df.iterrows():
                    email = normalize_email_row(row.to_dict())
                    result = analyze_email(email)
                    results.append({
                        "subject": email.get("subject", ""),
                        "sender": email.get("sender", ""),
                        "risk_label": result["risk_label"],
                        "risk_score": result["risk_score"],
                        "url_count": result["features"]["url_count"],
                        "evidence": " | ".join(result["evidence"]),
                        "recommended_action": result["recommended_actions"][0] if result["recommended_actions"] else ""
                    })
                out = pd.DataFrame(results)
                st.dataframe(out, use_container_width=True, hide_index=True)
                counts = out["risk_label"].value_counts()
                st.bar_chart(counts)
                st.download_button("Download analysis CSV", out.to_csv(index=False).encode("utf-8"), "email_analysis_results.csv", "text/csv")
        except Exception as exc:
            st.error(f"Could not read this CSV: {exc}")

with tab3:
    st.subheader("Built-in synthetic dataset")
    data_path = "data/dummy_emails.csv"
    try:
        samples = pd.read_csv(data_path).fillna("")
        st.write(f"{len(samples)} synthetic examples included.")
        st.dataframe(samples.head(20), use_container_width=True, hide_index=True)
        st.download_button("Download sample dataset", samples.to_csv(index=False).encode("utf-8"), "dummy_emails.csv", "text/csv")
    except FileNotFoundError:
        st.info("Run `python create_dataset.py` to create the synthetic dataset.")
