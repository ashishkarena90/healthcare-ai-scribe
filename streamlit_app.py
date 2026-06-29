import json
import requests
import streamlit as st

# ==================================================
# Page Config
# ==================================================

st.set_page_config(
    page_title="Healthcare AI Scribe",
    page_icon="🩺",
    layout="wide"
)

# ==================================================
# Sidebar
# ==================================================

with st.sidebar:

    st.title("🩺 Healthcare AI Scribe")

    st.markdown("---")

    st.write("### Human-in-the-Loop Dashboard")

    st.info(
        """
        AI Powered Medical Documentation

        ✅ Whisper ASR

        ✅ Speaker Diarization

        ✅ SOAP Generation

        ✅ ICD-10 Recommendation
        """
    )

    st.markdown("---")

    st.caption("Version 1.0")

    st.caption("Developed by Ashish Karena")

# ==================================================
# Header
# ==================================================

st.title("🩺 Healthcare AI Scribe")

st.write(
    "Upload a doctor-patient audio conversation and review the generated SOAP note before finalizing."
)

st.divider()

# ==================================================
# Upload
# ==================================================

uploaded_file = st.file_uploader(
    "🎤 Upload Doctor-Patient Audio",
    type=["mp3", "wav", "m4a"]
)

# ==================================================
# Process Button
# ==================================================

if uploaded_file is not None:

    st.success(f"Selected File : {uploaded_file.name}")

    if st.button(
        "🚀 Generate SOAP Note",
        use_container_width=True
    ):

        with st.spinner("Processing audio..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/upload-audio",
                    files=files
                )

                if response.status_code != 200:

                    st.error(
                        f"API Error : {response.status_code}"
                    )

                    st.stop()

                data = response.json()

            except Exception as e:

                st.error(e)

                st.stop()

        st.success("SOAP Note Generated Successfully!")

        # ==========================================
        # Summary Cards
        # ==========================================

        st.subheader("📊 Summary")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Language",
                data["language"].upper()
            )

        with col2:

            st.metric(
                "ICD Codes",
                len(data["icd_codes"])
            )

        with col3:

            st.metric(
                "Speakers",
                len(
                    set(
                        item["speaker"]
                        for item in data["conversation"]
                    )
                )
            )

        # ==========================================
        # Tabs
        # ==========================================

        soap = data["soap_note"]

        tab1, tab2 = st.tabs(
            [
                "📝 Transcript",
                "📋 SOAP Note"
            ]
        )

        # ==========================================
        # Transcript Tab
        # ==========================================

        with tab1:

            st.subheader("Conversation Transcript")

            st.text_area(
                "Transcript",
                value=data["transcript"],
                height=300,
                disabled=True
            )

            st.markdown("---")

            with st.expander(
                "👥 View Speaker Conversation"
            ):

                for item in data["conversation"]:

                    if item["speaker"] == "Doctor":

                        st.success(
                            f"👨‍⚕️ Doctor : {item['text']}"
                        )

                    else:

                        st.info(
                            f"🧑 Patient : {item['text']}"
                        )

        # ==========================================
        # SOAP Note Tab
        # ==========================================

        with tab2:

            st.subheader(
                "Human-in-the-Loop SOAP Editor"
            )

            subjective = st.text_area(
                "Subjective",
                value="\n".join(
                    soap["subjective"]
                ),
                height=120
            )

            objective = st.text_area(
                "Objective",
                value="\n".join(
                    soap["objective"]
                ),
                height=120
            )

            assessment = st.text_area(
                "Assessment",
                value="\n".join(
                    soap["assessment"]
                ),
                height=120
            )

            plan = st.text_area(
                "Plan",
                value="\n".join(
                    soap["plan"]
                ),
                height=120
            )

        st.divider()

        # ==========================================
        # ICD Recommendation
        # ==========================================

        st.subheader("💊 Suggested ICD-10 Codes")

        for item in data["icd_codes"]:

            with st.container(border=True):

                c1, c2 = st.columns([1,5])

                with c1:

                    st.markdown(
                        f"### {item['code']}"
                    )

                with c2:

                    st.write(
                        item["description"]
                    )
                    
        # ==========================================
        # Final SOAP Note
        # ==========================================

        final_note = {
            "subjective": [
                line.strip()
                for line in subjective.split("\n")
                if line.strip()
            ],
            "objective": [
                line.strip()
                for line in objective.split("\n")
                if line.strip()
            ],
            "assessment": [
                line.strip()
                for line in assessment.split("\n")
                if line.strip()
            ],
            "plan": [
                line.strip()
                for line in plan.split("\n")
                if line.strip()
            ]
        }

        st.divider()

        st.subheader("📄 Final Review")

        with st.expander("Preview Final SOAP Note", expanded=False):
            st.json(final_note)

        st.divider()

        # ==========================================
        # Action Buttons
        # ==========================================

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                label="⬇ Download SOAP Note (JSON)",
                data=json.dumps(
                    final_note,
                    indent=4
                ),
                file_name="soap_note.json",
                mime="application/json",
                use_container_width=True
            )

        with col2:

            if st.button(
                "✅ Finalize SOAP Note",
                use_container_width=True
            ):

                st.success(
                    "SOAP Note Finalized Successfully!"
                )

                st.balloons()

        st.divider()

        # ==========================================
        # Footer
        # ==========================================

        st.caption(
            "🩺 Healthcare AI Scribe | Human-in-the-Loop Dashboard | Version 1.0"
        )