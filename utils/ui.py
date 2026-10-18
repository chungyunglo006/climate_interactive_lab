"""
UI helper module for beautiful styling, banners, metrics, and Plotly templates.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

CUSTOM_CSS = """
<style>
/* Global Modern Typography & Polish */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

code, kbd, samp, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Glassmorphism Hero Banner */
.hero-container {
    background: linear-gradient(135deg, rgba(21, 28, 44, 0.85) 0%, rgba(11, 15, 25, 0.95) 100%);
    border: 1px solid rgba(0, 229, 255, 0.2);
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px -10px rgba(0, 229, 255, 0.15);
    backdrop-filter: blur(10px);
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ffffff 0%, #00e5ff 60%, #7c4dff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #94a3b8;
    line-height: 1.5;
}

.tag-badge {
    display: inline-block;
    padding: 3px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 9999px;
    background: rgba(0, 229, 255, 0.12);
    color: #00e5ff;
    border: 1px solid rgba(0, 229, 255, 0.3);
    margin-right: 8px;
}

/* Custom Card Container */
.stat-card {
    background: rgba(21, 28, 44, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    transition: all 0.2s ease-in-out;
}

.stat-card:hover {
    border-color: rgba(0, 229, 255, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.stat-label {
    font-size: 0.85rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

.stat-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 4px;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #0d121f !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

/* Button & Slider Accents */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s;
}

.stButton > button:hover {
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
}
</style>
"""


def apply_custom_styles():
    """Injects custom CSS styling."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero(title, subtitle, badges=None):
    """Renders a sleek hero banner."""
    apply_custom_styles()
    badge_html = ""
    if badges:
        for b in badges:
            badge_html += f'<span class="tag-badge">{b}</span>'

    html = f"""
    <div class="hero-container">
        <div>{badge_html}</div>
        <div class="hero-title">{title}</div>
        <div class="hero-subtitle">{subtitle}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_stat_card(label, value, subtext=""):
    """Renders an interactive metric card."""
    sub_html = f'<div style="font-size: 0.8rem; color: #64748b; margin-top: 2px;">{subtext}</div>' if subtext else ''
    html = f"""
    <div class="stat-card">
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        {sub_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def get_plotly_layout(title="", xaxis_title="", yaxis_title="", height=480):
    """Returns a unified, ultra-clean dark Plotly layout."""
    return dict(
        title=dict(text=title, font=dict(family="Plus Jakarta Sans", size=16, color="#f8fafc")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.45)",
        font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
        xaxis=dict(
            title=xaxis_title,
            gridcolor="rgba(255,255,255,0.07)",
            zerolinecolor="rgba(255,255,255,0.15)",
            showline=True,
            linecolor="rgba(255,255,255,0.1)"
        ),
        yaxis=dict(
            title=yaxis_title,
            gridcolor="rgba(255,255,255,0.07)",
            zerolinecolor="rgba(255,255,255,0.15)",
            showline=True,
            linecolor="rgba(255,255,255,0.1)"
        ),
        legend=dict(
            bgcolor="rgba(15, 23, 42, 0.6)",
            bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1,
            font=dict(size=12, color="#cbd5e1")
        ),
        margin=dict(l=50, r=30, t=50, b=50),
        height=height,
        hovermode="x unified"
    )
