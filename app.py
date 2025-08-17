import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Strategy Simulator",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# HELPER FUNCTIONS
# -------------------------
@st.cache_data
def run_simulation(strategy_factor, market_volatility, iterations=100):
    """Simulate strategy performance with randomness."""
    results = []
    for _ in range(iterations):
        actual_factor = strategy_factor * (0.9 + 0.2 * np.random.rand())
        volatility_effect = (1 - market_volatility * np.random.rand())
        results.append(actual_factor * volatility_effect * 100)
    return results

def generate_summary(results):
    """Generate a dataframe summary."""
    df = pd.DataFrame(results, columns=["Performance"])
    return df.describe()

def convert_df(df):
    """Convert DataFrame to CSV for download."""
    return df.to_csv(index=False).encode("utf-8")

# -------------------------
# SIDEBAR (Inputs)
# -------------------------
st.sidebar.title("⚙️ Simulation Settings")
strategy_factor = st.sidebar.slider("Strategy Effectiveness", 0.5, 2.0, 1.0, 0.1)
market_volatility = st.sidebar.slider("Market Volatility", 0.0, 1.0, 0.3, 0.05)
iterations = st.sidebar.number_input("Iterations", min_value=50, max_value=1000, value=200, step=50)

# -------------------------
# MAIN PAGE
# -------------------------
st.title("📊 Business Strategy Simulator")
st.markdown(
    """
    Welcome to the **Strategy Simulator**.  
    Use the sidebar to adjust **strategy effectiveness, market volatility, and iterations**.  
    The simulator will run scenarios and provide a **summary, visualization, and downloadable report**.
    """
)

try:
    # Run simulation
    results = run_simulation(strategy_factor, market_volatility, iterations)
    summary_df = generate_summary(results)

    # Show summary
    st.subheader("📈 Simulation Results Summary")
    st.dataframe(summary_df.style.highlight_max(axis=0))

    # Plot results
    st.subheader("📉 Performance Distribution")
    fig, ax = plt.subplots()
    ax.hist(results, bins=20, color="skyblue", edgecolor="black")
    ax.set_title("Strategy Performance Distribution")
    ax.set_xlabel("Performance")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Download section
    st.subheader("⬇️ Download Data")
    csv = convert_df(pd.DataFrame(results, columns=["Performance"]))
    st.download_button(
        "Download Results as CSV",
        data=csv,
        file_name="strategy_results.csv",
        mime="text/csv"
    )

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>© 2025 Strategy Simulator | Built for Business Insights</p>",
        unsafe_allow_html=True
    )

except Exception as e:
    st.error(f"❌ An error occurred during the simulation: {e}")

