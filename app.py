import streamlit as st
from train import AadhaarRiskEngine

st.set_page_config(page_title="Aadhaar Risk Engine", layout="wide")

st.title("🛡 Aadhaar Risk Engine Dashboard")

engine = AadhaarRiskEngine()

st.sidebar.header("Upload CSV Files")

enrol_files = st.sidebar.file_uploader(
    "Upload Enrolment CSVs",
    accept_multiple_files=True,
    type="csv"
)

demo_files = st.sidebar.file_uploader(
    "Upload Demographic CSVs",
    accept_multiple_files=True,
    type="csv"
)

bio_files = st.sidebar.file_uploader(
    "Upload Biometric CSVs",
    accept_multiple_files=True,
    type="csv"
)

if enrol_files and demo_files and bio_files:
    with st.spinner("Processing data..."):
        enrol_df = engine.load_enrolment(enrol_files)
        demo_df = engine.load_demographic(demo_files)
        bio_df = engine.load_biometric(bio_files)

        merged_df = engine.merge_all(enrol_df, demo_df, bio_df)
        final_df = engine.compute_risk(merged_df)

    st.success("Risk engine successfully executed!")

    st.subheader("📊 High Risk Cases")
    high_risk = final_df[final_df["risk_level"] == "HIGH"]
    st.dataframe(high_risk.sort_values("final_risk_score", ascending=False).head(50))

    st.subheader("📈 Risk Score Distribution")
    st.bar_chart(final_df["risk_level"].value_counts())

    st.subheader("🔍 Filter by Pincode")
    pincode = st.text_input("Enter Pincode")
    if pincode:
        st.dataframe(final_df[final_df["pincode"].astype(str) == pincode])

    st.download_button(
        "⬇ Download Full Risk Output",
        data=final_df.to_csv(index=False),
        file_name="aadhaar_risk_output.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload all three datasets to run the risk engine.")
