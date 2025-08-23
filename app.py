import streamlit as st
import pandas as pd

# --------------------------
# PAGE CONFIGURATION
# --------------------------
st.set_page_config(page_title="Strategy Simulator", page_icon="📊", layout="wide")

# --------------------------
# SIDEBAR NAVIGATION
# --------------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Introduction", "Strategy Builder", "Risk Analysis", "Market Scenarios", "Summary & Download"]
)

# --------------------------
# INTRO PAGE
# --------------------------
if page == "Introduction":
    st.title("📊 Strategy Simulator")
    st.write("""
    Welcome to the **Strategy Simulator**!  
    This tool helps you design, test, and analyze strategies for **business, personal projects, or investments**.  

    ✅ Build strategies step by step  
    ✅ Analyze risks and predictions  
    ✅ Simulate real-world scenarios  
    ✅ Export your results for later use  

    Use the left-hand sidebar to navigate between sections.
    """)

# --------------------------
# STRATEGY BUILDER PAGE
# --------------------------
elif page == "Strategy Builder":
    st.title("📝 Strategy Builder")
    st.write("Define the core elements of your strategy below:")

    with st.form("strategy_form"):
        goal = st.text_input("🎯 Goal", "Increase revenue / Improve efficiency / Expand reach")
        timeline = st.selectbox("⏳ Timeline", ["1 Month", "3 Months", "6 Months", "1 Year", "3+ Years"])
        budget = st.number_input("💰 Budget (in USD)", min_value=0, value=1000, step=100)
        resources = st.text_area("🛠️ Resources Needed", "Team, tools, marketing, etc.")
        submit = st.form_submit_button("Save Strategy")

    if submit:
        st.success("✅ Strategy saved successfully!")
        st.session_state["strategy"] = {
            "Goal": goal,
            "Timeline": timeline,
            "Budget": budget,
            "Resources": resources
        }

# --------------------------
# RISK ANALYSIS PAGE
# --------------------------
elif page == "Risk Analysis":
    st.title("⚠️ Risk Analysis")
    st.write("Evaluate risks and potential challenges.")

    market_risk = st.slider("📉 Market Risk", 0, 100, 30)
    financial_risk = st.slider("💵 Financial Risk", 0, 100, 40)
    execution_risk = st.slider("⚙️ Execution Risk", 0, 100, 20)

    total_risk = (market_risk + financial_risk + execution_risk) / 3
    st.metric("Overall Risk Level", f"{total_risk:.1f}%")

    st.session_state["risks"] = {
        "Market Risk": market_risk,
        "Financial Risk": financial_risk,
        "Execution Risk": execution_risk,
        "Total Risk": total_risk
    }

# --------------------------
# MARKET SCENARIOS PAGE
# --------------------------
elif page == "Market Scenarios":
    st.title("🌍 Market Scenarios")
    st.write("Simulate how your strategy performs under different conditions.")

    scenario = st.selectbox("Choose a scenario", ["Optimistic", "Neutral", "Pessimistic"])
    impact = {"Optimistic": 1.2, "Neutral": 1.0, "Pessimistic": 0.7}[scenario]

    if "strategy" in st.session_state:
        budget = st.session_state["strategy"]["Budget"]
        adjusted_budget = budget * impact
        st.metric("Adjusted Budget", f"${adjusted_budget:,.2f}")

        st.session_state["scenario"] = {
            "Scenario": scenario,
            "Impact Factor": impact,
            "Adjusted Budget": adjusted_budget
        }
    else:
        st.warning("⚠️ Please set up a strategy first in the Strategy Builder.")

# --------------------------
# SUMMARY & DOWNLOAD PAGE
# --------------------------
elif page == "Summary & Download":
    st.title("📑 Strategy Summary & Download")

    if "strategy" in st.session_state and "risks" in st.session_state and "scenario" in st.session_state:
        strategy_df = pd.DataFrame([st.session_state["strategy"]])
        risks_df = pd.DataFrame([st.session_state["risks"]])
        scenario_df = pd.DataFrame([st.session_state["scenario"]])

        st.subheader("🎯 Strategy")
        st.table(strategy_df)

        st.subheader("⚠️ Risks")
        st.table(risks_df)

        st.subheader("🌍 Scenario")
        st.table(scenario_df)

        # Combine into one Excel file
        output = pd.ExcelWriter("strategy_summary.xlsx", engine="xlsxwriter")
        strategy_df.to_excel(output, sheet_name="Strategy", index=False)
        risks_df.to_excel(output, sheet_name="Risks", index=False)
        scenario_df.to_excel(output, sheet_name="Scenario", index=False)
        output.close()

        with open("strategy_summary.xlsx", "rb") as file:
            st.download_button(
                label="⬇️ Download Summary (Excel)",
                data=file,
                file_name="strategy_summary.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    else:
        st.warning("⚠️ Please complete all sections before viewing the summary.")

