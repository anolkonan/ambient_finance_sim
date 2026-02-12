import streamlit as st
from agent import ambient_agent
from banking_data import dashboard_metrics
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import streamlit.components.v1 as components

# MUST be first
st.set_page_config(layout="wide")

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
        height=300
    )

    return fig


# ---------------- Sidebar ----------------
st.sidebar.title("🛰 Navigation")
page = st.sidebar.radio(
    "Select View",
    ["Dashboard", "AI Assistant", "Analytics", "Settings"]
)

risk_mode = st.sidebar.selectbox(
    "AI Risk Personality",
    ["Conservative", "Balanced", "Aggressive"]
)

# ---------------- Theme Toggle ----------------
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

.glass-card {
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 0 30px rgba(0,255,255,0.1);
}

.flag-alert {
    padding: 8px;
    border-radius: 10px;
    margin-bottom: 8px;
    font-weight: bold;
}

.red-glow {
    background: rgba(255,0,0,0.15);
    box-shadow: 0 0 10px rgba(255,0,0,0.8);
}

.yellow-glow {
    background: rgba(255,255,0,0.15);
    box-shadow: 0 0 10px rgba(255,255,0,0.8);
}

.metric-value {{
    font-size: 32px;
    font-weight: bold;
    color: #00ffff;
}}

.metric-title {{
    opacity: 0.7;
    font-size: 14px;
}}

.title {{
    font-size: 38px;
    text-align: center;
    margin-bottom: 30px;
    text-shadow: 0 0 10px #00ffff;
}}

.pulse {
    height: 80px;
    width: 80px;
    border-radius: 50%;
    margin: auto;
    animation: pulse-animation 2s infinite;
}

@keyframes pulse-animation {
    0% { box-shadow: 0 0 0 0 rgba(0,255,200, 0.7); }
    70% { box-shadow: 0 0 0 20px rgba(0,255,200, 0); }
    100% { box-shadow: 0 0 0 0 rgba(0,255,200, 0); }
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# ================== DASHBOARD =========================
# ======================================================

if page == "Dashboard":

    st.markdown('<div class="title">Ambient Finance Control Center</div>', unsafe_allow_html=True)

    dashboard = dashboard_metrics()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">Savings Rate</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{dashboard["savings_rate"]}%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">Daily Burn Rate</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">${dashboard["burn_rate_daily"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">Runway (Months)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{dashboard["runway_months"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------- AI + Chart Section --------
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🧠 AI Decision Engine")

        user_input = st.text_input("Ask your financial assistant:")

        if st.button("Run Simulation"):
            with st.spinner("Analyzing financial signals..."):
                time.sleep(1)
                response = ambient_agent(user_input, risk_mode=risk_mode)
                st.json(response)

        if "recommendation_score" in response:
           st.plotly_chart(render_recommendation_gauge(response["recommendation_score"]),width="stretch")

        if "recommendation_score" in response and "confidence_level" in response:heat_label = decision_heat(
        response["recommendation_score"],
        response["confidence_level"]
    )

    st.markdown(
        f"""
        <div class="glass-card">
            <h2 style='text-align:center;'>{heat_label}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Financial Trend")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=[4000, 4500, 4200, 4800, 5000, 5200],
            mode='lines',
            line=dict(width=3)
        ))

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(showgrid=False, visible=False)
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# ================= AI ASSISTANT =======================
# ======================================================

elif page == "AI Assistant":

    st.markdown('<div class="title">AI Decision Cockpit</div>', unsafe_allow_html=True)

    user_input = st.text_input("Enter your financial question:")

    response = None

    if st.button("Run AI"):
        with st.spinner("Processing financial intelligence..."):
            time.sleep(1)
            response = ambient_agent(user_input, risk_mode=risk_mode)

if response:
    st.json(response)

    if "recommendation_score" in response:
        st.plotly_chart(
            render_recommendation_gauge(response["recommendation_score"]),
            width="stretch"
        )

    if "recommendation_score" in response and "confidence_level" in response:
        heat_label = decision_heat(
            response["recommendation_score"],
            response["confidence_level"]
        )

        st.markdown(
            f"""
            <div class="glass-card">
                <h2 style='text-align:center;'>{heat_label}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )


        # Layout for futuristic cockpit
        col_left, col_right = st.columns([2, 1])

        # ---------------- LEFT PANEL ----------------
        with col_left:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🧠 AI Financial Assessment")
            st.json(response)
            st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- RIGHT PANEL ----------------
        with col_right:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            # Radial Gauge
            if "recommendation_score" in response:
                st.plotly_chart(
                    render_recommendation_gauge(response["recommendation_score"]),
                    width="stretch"
                )

            # Heat Level
            if "recommendation_score" in response and "confidence_level" in response:
                heat_label = decision_heat(
                    response["recommendation_score"],
                    response["confidence_level"]
                )

                st.markdown(
                    f"<h3 style='text-align:center;'>{heat_label}</h3>",
                    unsafe_allow_html=True
                )

            # Confidence Pulse
            if "confidence_level" in response:
                st.markdown("<div class='pulse'></div>", unsafe_allow_html=True)
                st.markdown(
                    f"<p style='text-align:center;'>Confidence: {response['confidence_level']}</p>",
                    unsafe_allow_html=True
                )

            st.markdown('</div>', unsafe_allow_html=True)



# ======================================================
# ================= ANALYTICS ==========================
# ======================================================

elif page == "Analytics":

    st.title("📊 Financial Forecast")

    months = np.arange(1, 13)
    forecast = 5000 - months * 300

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=forecast,
        mode="lines+markers"
    ))

    fig.update_layout(
        title="Projected Cash Runway",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, width="stretch")

    st.subheader("Transaction History")

    data = pd.DataFrame({
        "Date": ["Jan 1", "Jan 3", "Jan 5", "Jan 8"],
        "Category": ["Food", "Rent", "Transport", "Shopping"],
        "Amount": [-500, -12000, -800, -2500]
    })

    st.dataframe(data, use_container_width=True)

# ======================================================
# ================= SETTINGS ===========================
# ======================================================

elif page == "Settings":

    st.title("⚙️ System Settings")
    st.info("Future: automation rules, AI temperature control, portfolio logic, etc.")