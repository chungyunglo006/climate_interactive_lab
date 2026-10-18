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


def set_param_value(key, new_val):
    """Programmatically updates parameter across session state safely before widgets instantiate."""
    st.session_state[key] = new_val
    st.session_state[f"{key}_pending"] = new_val


def render_sync_input(label, key, min_val, max_val, default_val, step,
                      format="%.2f", is_int=False, container=None):
    """
    Renders synchronized slider and number_input allowing users to either
    drag the slider or directly type numeric values.
    Works inside expanders, sidebars, or main containers.
    """
    c = container if container is not None else st

    slider_key = f"{key}_slider"
    num_key = f"{key}_num"
    pending_key = f"{key}_pending"

    if key not in st.session_state:
        st.session_state[key] = default_val

    # Apply any pending external updates before widget instantiation
    if pending_key in st.session_state:
        st.session_state[key] = st.session_state.pop(pending_key)
        val = int(st.session_state[key]) if is_int else float(st.session_state[key])
        st.session_state[slider_key] = val
        st.session_state[num_key] = val

    # Ensure in bounds
    current_val = int(st.session_state[key]) if is_int else float(st.session_state[key])
    if current_val < min_val:
        current_val = int(min_val) if is_int else float(min_val)
        st.session_state[key] = current_val
    elif current_val > max_val:
        current_val = int(max_val) if is_int else float(max_val)
        st.session_state[key] = current_val

    # Initialize slider and num state keys if not present
    if slider_key not in st.session_state:
        st.session_state[slider_key] = current_val
    if num_key not in st.session_state:
        st.session_state[num_key] = current_val

    def on_slider_change():
        val = st.session_state[slider_key]
        st.session_state[key] = val
        st.session_state[num_key] = val

    def on_num_change():
        val = st.session_state[num_key]
        st.session_state[key] = val
        st.session_state[slider_key] = val

    c.markdown(f"**{label}**")
    col1, col2 = c.columns([3, 2])
    with col1:
        if is_int:
            st.slider(
                label,
                min_value=int(min_val),
                max_value=int(max_val),
                step=int(step),
                key=slider_key,
                on_change=on_slider_change,
                label_visibility="collapsed"
            )
        else:
            st.slider(
                label,
                min_value=float(min_val),
                max_value=float(max_val),
                step=float(step),
                key=slider_key,
                on_change=on_slider_change,
                label_visibility="collapsed"
            )
    with col2:
        if is_int:
            st.number_input(
                label,
                min_value=int(min_val),
                max_value=int(max_val),
                step=int(step),
                key=num_key,
                on_change=on_num_change,
                label_visibility="collapsed"
            )
        else:
            st.number_input(
                label,
                min_value=float(min_val),
                max_value=float(max_val),
                step=float(step),
                format=format,
                key=num_key,
                on_change=on_num_change,
                label_visibility="collapsed"
            )

    return st.session_state[key]


def render_dynamic_controller(param_specs, page_prefix="p1"):
    """
    Renders dynamic parameter sweep and animation controller controls in the sidebar.
    Does NOT block or interrupt page rendering.
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎬 動態參數演變控制器")

    running_key = f"{page_prefix}_anim_running"
    if running_key not in st.session_state:
        st.session_state[running_key] = False

    target_name = st.sidebar.selectbox(
        "🎯 選擇要變動的變數",
        list(param_specs.keys()),
        key=f"{page_prefix}_anim_target"
    )
    target_spec = param_specs[target_name]
    target_key = target_spec["key"]

    dir_choice = st.sidebar.radio(
        "🔄 變動方向",
        ["往大增加 (+)", "往小減少 (-)", "來回擺動 (Ping-Pong)"],
        horizontal=True,
        key=f"{page_prefix}_anim_dir"
    )

    col_d1, col_d2 = st.sidebar.columns([3, 2])
    with col_d1:
        step_val = st.number_input(
            "變動大小值 (Δ)",
            value=float(target_spec["step"]),
            min_value=0.0001,
            step=float(target_spec["step"]) / 2.0,
            key=f"{page_prefix}_anim_step_val"
        )
    with col_d2:
        interval_val = st.number_input(
            "間隔 (秒)",
            value=0.20,
            min_value=0.02,
            max_value=3.0,
            step=0.05,
            key=f"{page_prefix}_anim_interval"
        )

    btn_col1, btn_col2 = st.sidebar.columns(2)
    start_btn = btn_col1.button("▶️ 開始動態", use_container_width=True, type="primary")
    stop_btn = btn_col2.button("⏹️ 停止演變", use_container_width=True)

    if start_btn:
        st.session_state[running_key] = True
        st.rerun()
    if stop_btn:
        st.session_state[running_key] = False
        st.rerun()

    if st.session_state.get(running_key, False):
        curr_val = st.session_state.get(target_key, target_spec.get("default", 0.0))
        st.sidebar.info(
            f"⚡ **動態演變中**\n\n"
            f"- 變動目標：**{target_name}**\n"
            f"- 當前數值：`{curr_val:.2f}` {target_spec.get('unit', '')}\n"
            f"- 模式：{dir_choice}"
        )


def execute_dynamic_step(param_specs, page_prefix="p1"):
    """
    Executes one animation step at the VERY END of the page script.
    Guarantees that all Plotly charts, tabs, and metrics have completely rendered
    before sleeping and triggering the next frame!
    """
    import time
    running_key = f"{page_prefix}_anim_running"
    if not st.session_state.get(running_key, False):
        return

    target_name = st.session_state.get(f"{page_prefix}_anim_target")
    if not target_name or target_name not in param_specs:
        return

    target_spec = param_specs[target_name]
    target_key = target_spec["key"]
    dir_choice = st.session_state.get(f"{page_prefix}_anim_dir", "往大增加 (+)")
    step_val = float(st.session_state.get(f"{page_prefix}_anim_step_val", target_spec["step"]))
    interval_val = float(st.session_state.get(f"{page_prefix}_anim_interval", 0.20))

    curr_val = float(st.session_state.get(target_key, target_spec.get("default", 0.0)))
    min_v = float(target_spec["min"])
    max_v = float(target_spec["max"])
    pingpong_dir_key = f"{page_prefix}_{target_key}_pp_dir"

    if "Ping-Pong" in dir_choice:
        pp_dir = st.session_state.get(pingpong_dir_key, 1)
        next_val = curr_val + pp_dir * step_val
        if next_val >= max_v:
            next_val = max_v
            st.session_state[pingpong_dir_key] = -1
        elif next_val <= min_v:
            next_val = min_v
            st.session_state[pingpong_dir_key] = 1
    elif "往大" in dir_choice:
        next_val = curr_val + step_val
        if next_val >= max_v:
            next_val = max_v
            st.session_state[running_key] = False
    else:  # 往小
        next_val = curr_val - step_val
        if next_val <= min_v:
            next_val = min_v
            st.session_state[running_key] = False

    # Apply updated value to pending queue safely before next widgets instantiate
    set_param_value(target_key, next_val)

    time.sleep(interval_val)
    st.rerun()

