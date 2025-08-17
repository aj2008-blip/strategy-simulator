import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# --- PAGE CONFIG ---
st.set_page_config(page_title="Business Strategy Simulator", layout="centered")

# --- INTRO PAGE ---
st.title("📊 Business Strategy Simulator")
st.markdown("Welcome to the **Business Strategy Simulator**. "
            "Use this tool to plan strategies, simulate decisions, and download insights.")

# --- NAVIGATION ---
pages = ["📋 Inputs", "📈 Simulation", "📑 Summary & Download"]
choice = st.sidebar.radio("Navigate", pages)

# --- PAGE 1: INPUTS ---
if choice == "📋 Inputs":
    st.header("Step 1: Define Your Business Inputs")
    st.markdown("Fill in the parameters below to set up your strategy simulation.")

    market_size = st.number_input("Market Size (in $M)", min_value=10, max_value=10000, value=500)
    growth_rate = st.slider("Expected Annual Growth Rate (%)", 0, 50, 10)
    competition = st.selectbox("Competition Level", ["Low", "Medium", "High"])
    budget = st.number_input("Available Budget (in $M)", min_value=1, max_value=5000, value=100)

    st.session_state["inputs"] = {
        "Market Size": market_size,
        "Growth Rate": growth_rate,
        "Competition": competition,
        "Budget": budget
    }

    st.success("✅ Inputs saved! Continue to the Simulation page.")

# --- PAGE 2: SIMULATION ---
elif choice == "📈 Simulation":
    st.header("Step 2: Run Simulation")
    if "inputs" not in st.session_state:
        st.warning("⚠️ Please fill inputs first.")
    else:
        inputs = st.session_state["inputs"]

        # Simple scoring logic
        base_score = inputs["Market Size"] * (inputs["Growth Rate"] / 100)
        if inputs["Competition"] == "High":
            base_score *= 0.6
        elif inputs["Competition"] == "Medium":
            base_score *= 0.8
        else:
            base_score *= 1.1

        budget_effect = np.log1p(inputs["Budget"])
        success_score = round(base_score * budget_effect, 2)

        st.metric("📊 Predicted Success Potential", f"${success_score}M")

        st.session_state["simulation_result"] = {
            "Success Score": success_score
        }

        st.success("✅ Simulation complete! Go to the Summary page.")

# --- PAGE 3: SUMMARY ---
elif choice == "📑 Summary & Download":
    st.header("Step 3: Strategy Summary")

    if "inputs" not in st.session_state or "simulation_result" not in st.session_state:
        st.warning("⚠️ Please complete the inputs and simulation first.")
    else:
        inputs = st.session_state["inputs"]
        results = st.session_state["simulation_result"]

        st.subheader("📋 Your Inputs")
        st.write(inputs)

        st.subheader("📊 Simulation Result")
        st.write(results)

        # PDF Export
        def generate_pdf(inputs, results):
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("Business Strategy Simulator - Report", styles["Title"]))
            story.append(Spacer(1, 12))

            story.append(Paragraph("Inputs:", styles["Heading2"]))
            for key, val in inputs.items():
                story.append(Paragraph(f"{key}: {val}", styles["Normal"]))

            story.append(Spacer(1, 12))
            story.append(Paragraph("Results:", styles["Heading2"]))
            for key, val in results.items():
                story.append(Paragraph(f"{key}: {val}", styles["Normal"]))

            doc.build(story)
            buffer.seek(0)
            return buffer

        pdf_buffer = generate_pdf(inputs, results)

        st.download_button(
            label="📥 Download Strategy Report (PDF)",
            data=pdf_buffer,
            file_name="strategy_report.pdf",
            mime="application/pdf"
        )
