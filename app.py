import streamlit as st
from agent import ambient_agent
from banking_data import dashboard_metrics
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import base64
import json

# ======================================================
#                   PAGE CONFIG
# ======================================================

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
                    url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .block-container {
        max-width: 900px;
        margin: auto;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }

    .title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
    }

    section[data-testid="stSidebar"] {
        background: rgba(20, 20, 30, 0.85);
        backdrop-filter: blur(15px);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
#                   UTILITY FUNCTIONS
# ======================================================

def decision_heat(score, confidence):
    if score > 75 and confidence == "High":
        return "🔥 HIGH DECISION MOMENT"
    elif score > 50:
        return "⚡ Moderate Opportunity"
    else:
        return "🧊 Low Urgency"


def render_recommendation_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Recommendation Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"thickness": 0.3},
            "steps": [
                {"range": [0, 40], "color": "#ff4b4b"},
                {"range": [40, 70], "color": "#f4c430"},
                {"range": [70, 100], "color": "#00ffcc"},
            ],
        },
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
        height=280
    )

    return fig


# ======================================================
#                   SIDEBAR
# ======================================================

st.sidebar.title("🛰 Navigation")
page = st.sidebar.radio(
    "Select View",
    ["Dashboard", "AI Assistant", "Analytics", "Settings"]
)

risk_mode = st.sidebar.selectbox(
    "AI Risk Personality",
    ["Conservative", "Balanced", "Aggressive"]
)

# ======================================================
#                   THEME
# ======================================================

theme = st.sidebar.toggle("🌗 Light Mode")

if theme:
    bg = "linear-gradient(135deg, #f0f0f0, #d9d9d9)"
    text_color = "black"
else:
    bg = "linear-gradient(135deg, #0f2027, #203a43, #2c5364)"
    text_color = "white"

st.markdown(f"""
<style>
html, body {{
    background: {bg};
    color: {text_color};
    font-family: 'Segoe UI', sans-serif;
}}

.glass-card {{
    backdrop-filter: blur(25px);
    background: rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 0 40px rgba(0,255,255,0.15);
}}

.title {{
    font-size: 42px;
    text-align: center;
    margin-bottom: 30px;
    background: linear-gradient(90deg, #00ffff, #00ffcc, #00ffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(0,255,255,0.6);
         }}


.pulse {{
    height: 80px;
    width: 80px;
    border-radius: 50%;
    margin: auto;
    animation: pulse-animation 2s infinite;
}}

body {{
    overflow-x: hidden;
}}

.particles {{
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: -1;
    background: radial-gradient(circle at 20% 30%, rgba(0,255,255,0.08), transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(0,255,200,0.08), transparent 40%);
    animation: moveParticles 20s linear infinite alternate;
}}

.confidence-ring {{
    height: 120px;
    width: 120px;
    border-radius: 50%;
    border: 4px solid rgba(0,255,255,0.4);
    box-shadow: 0 0 20px #00ffff;
    margin: auto;
    animation: rotateRing 4s linear infinite;
}}

.glass-card:hover {{
    box-shadow: 0 0 40px #00ffff;
    transition: 0.3s ease-in-out;
}}

@keyframes rotateRing {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

@keyframes moveParticles {{
    0% {{ transform: translateY(0px); }}
    100% {{ transform: translateY(-50px); }}
}}

@keyframes pulse-animation {{
    0% {{ box-shadow: 0 0 0 0 rgba(0,255,200, 0.7); }}
    70% {{ box-shadow: 0 0 0 20px rgba(0,255,200, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(0,255,200, 0); }}
}}

</style>

<div class="particles"></div>

""", unsafe_allow_html=True)
st.markdown("<div class='pulse'></div>", unsafe_allow_html=True)


# ======================================================
#                   DASHBOARD
# ======================================================

if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = True

# if st.session_state.auto_refresh:
#    time.sleep(5)
#    st.rerun()

if page == "Dashboard":

    # Outer centered glass container
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="title">Ambient Finance Control Center</div>',
        unsafe_allow_html=True
    )

    dashboard = dashboard_metrics()

    col1, col2, col3 = st.columns(3)

    metrics = [
        ("Savings Rate", f"{dashboard['savings_rate']}%"),
        ("Daily Burn Rate", f"${dashboard['burn_rate_daily']}"),
        ("Runway (Months)", dashboard['runway_months'])
    ]

    for col, (label, value) in zip([col1, col2, col3], metrics):
        with col:
            st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.06);
                    backdrop-filter: blur(15px);
                    border-radius: 16px;
                    padding: 25px;
                    text-align: center;
                    border: 1px solid rgba(255,255,255,0.1);
                ">
                    <div style="font-size:14px; opacity:0.6;">
                        {label}
                    </div>
                    <div style="font-size:36px; font-weight:700; color:#00ffff;">
                        {value}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


    # AI SECTION

    st.markdown("<div class='confidence-ring'></div>", unsafe_allow_html=True)

    st.markdown("""
      <hr style="
      border: none;
      height: 1px;
      background: linear-gradient(to right, transparent, #00ffff, transparent);
      box-shadow: 0 0 15px #00ffff;
      margin: 40px 0;">
""", unsafe_allow_html=True)

    st.subheader("🧠 AI Decision Engine")

    user_input = st.text_input("Ask your financial assistant:")

    if st.button("Run Simulation"):
        with st.spinner("Analyzing financial signals..."):
            time.sleep(1)
            response = ambient_agent(user_input, risk_mode=risk_mode)

            response_text = json.dumps(response, indent=2)
            typing_placeholder = st.empty()
            display_text = ""

            for char in response_text:
                display_text += char
                typing_placeholder.code(display_text, language="json")
                time.sleep(0.01)

            if "recommendation_score" in response:
                st.plotly_chart(
                    render_recommendation_gauge(response["recommendation_score"]),
                    use_container_width=True
                )

            if "recommendation_score" in response and "confidence_level" in response:
                heat_label = decision_heat(
                    response["recommendation_score"],
                    response["confidence_level"]
                )

                st.markdown("""
                    <div style="text-align:center; font-size:12px; opacity:0.6;">AI signal processing complete ✔</div>
                    </div>
                     """, unsafe_allow_html=True)
                
                st.button("🎙 Activate Voice Mode")
                st.info("Voice processing coming in next phase integration.")


                st.success(heat_label)


# ======================================================
#                    AI ASSISTANT
# ======================================================

elif page == "AI Assistant":

    st.markdown('<div class="title">AI Decision Cockpit</div>', unsafe_allow_html=True)

    st.markdown("### Ask anything about your financial situation")

    user_input = st.text_input(
        "Your Question",
        placeholder="e.g. Should I invest more this month?"
    )

    run_ai = st.button("🚀 Run AI Analysis")

    if run_ai:

        if not user_input.strip():
            st.warning("Please enter a question before running the AI.")
        else:
            progress = st.progress(0)
            for percent in range(100):
                time.sleep(0.01)
                progress.progress(percent + 1)

            with st.spinner("Analyzing financial signals..."):
                time.sleep(1)
                response = ambient_agent(user_input, risk_mode=risk_mode)

                progress.empty()


                try:
                    response = ambient_agent(user_input, risk_mode=risk_mode)
                except Exception as e:
                    st.error(f"Agent Error: {e}")
                    st.stop()

            col_left, col_right = st.columns([2, 1])

            # LEFT SIDE
            with col_left:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("AI Financial Assessment")

                st.markdown("### 📊 AI Strategic Insight")

                st.write(response.get("analysis", "No analysis provided."))

                if "recommendation" in response:
                    st.success(response["recommendation"])

                if "reasoning" in response:
                    st.markdown(f"**AI Reasoning:** {response['reasoning']}")
                    st.markdown('</div>', unsafe_allow_html=True)

            # RIGHT SIDE
            with col_right:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)

                if "recommendation_score" in response:
                    st.plotly_chart(
                        render_recommendation_gauge(response["recommendation_score"]),
                        width="stretch"
                    )

                if "confidence_level" in response:
                    st.markdown(f"### Confidence: {response['confidence_level']}")

                st.markdown('</div>', unsafe_allow_html=True)



# ======================================================
#                   ANALYTICS
# ======================================================

elif page == "Analytics":

    st.markdown('<div class="title">Financial Forecast Lab</div>', unsafe_allow_html=True)

    dashboard = dashboard_metrics()

    # Forecast Simulation
    months = np.arange(1, 13)
    projected_balance = dashboard["runway_months"] * 1000 - months * dashboard["burn_rate_daily"] * 30

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=months,
        y=projected_balance,
        mode="lines+markers",
        name="Projected Balance"
    ))

    fig.update_layout(
        title="12-Month Financial Projection",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Month",
        yaxis_title="Balance"
    )

    st.plotly_chart(fig, width="stretch")

    # Risk Simulation Slider
    st.subheader("📊 Scenario Simulator")

    expense_shock = st.slider(
        "Simulate Unexpected Expense ($)",
        min_value=0,
        max_value=10000,
        value=2000,
        step=500
    )

    impact_runway = max(
        0,
        dashboard["runway_months"] - (expense_shock / 1000)
    )

    st.metric(
        "Runway After Shock (Months)",
        round(impact_runway, 2)
    )

    # Transaction Table
    st.subheader("Recent Transactions")

    data = pd.DataFrame({
        "Date": ["Jan 1", "Jan 3", "Jan 5", "Jan 8"],
        "Category": ["Food", "Rent", "Transport", "Shopping"],
        "Amount": [-500, -12000, -800, -2500]
    })

    st.dataframe(data, width="stretch")


# ======================================================
#                       SETTINGS
# ======================================================

elif page == "Settings":

    st.markdown('<div class="title">System Settings</div>', unsafe_allow_html=True)
    st.info("Future: automation rules, AI temperature control, portfolio logic, etc.")
