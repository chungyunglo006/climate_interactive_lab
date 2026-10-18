"""
Page 3: 0D Classic Daisyworld Interactive Experiment Site.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.ui import (
    apply_custom_styles,
    render_hero,
    render_stat_card,
    get_plotly_layout,
    render_plotly_chart
)
from models.daisy_0d import (
    run_daisyworld,
    sweep_daisyworld_luminosity,
    beta_growth
)
import streamlit.components.v1 as components
from utils.interactive_daisy_0d import get_interactive_daisy0d_html

st.set_page_config(
    page_title="0D 經典雛菊世界 (Classic Daisyworld) | 獨立實驗網站",
    page_icon="🌼",
    layout="wide"
)

apply_custom_styles()

render_hero(
    title="經典雙物種雛菊世界 (Classic Daisyworld)",
    subtitle="基於 Watson & Lovelock (1983) 蓋亞模型：黑雛菊吸熱升溫 vs 白雛菊散熱降溫的自發恆溫調節 (Homeostasis)。",
    badges=["Daisyworld", "Gaia Hypothesis", "Temperature Regulation", "Biotic Feedback", "60 FPS Canvas"]
)

# Sidebar: Model Guide & Key Concepts (Unified single control panel is inside the interactive canvas)
with st.sidebar:
    st.header("🌼 0D 經典雛菊世界實驗室")
    st.markdown("""
    **實驗特色**
    - ⚡ **60 FPS 前端絲滑畫布**：坐標軸固化，曲線零重劃、零閃爍。
    - 🎛️ **雙向同步面板**：滑桿平滑拖曳 + 精確數值鍵盤直接輸入。
    - 🎬 **連續動態掃描**：內建 60 FPS 硬體加速平滑推移動畫。
    
    ---
    **核心生物物理機制**
    - **黑雛菊 ($a_b$)**：低反照率 (0.25)，吸收更多陽光使周圍升溫，在寒冷環境下具競爭優勢。
    - **白雛菊 ($a_w$)**：高反照率 (0.75)，反射陽光使周圍降溫，在炎熱環境下具競爭優勢。
    - **恆溫機制 (Homeostasis)**：兩種雛菊自發消長，將行星整體均溫調節在最適生長點 ($22.5^\\circ\\text{C}$) 附近。
    
    ---
    **參考基準**
    - 最適生長溫度：$22.5$ ℃
    - 生存極限範圍：$5.0 \\sim 40.0$ ℃
    - 裸地反照率：$0.50$
    """)

# Default parameters
s0 = 917.0
l_val = 1.0
alpha_w = 0.75
alpha_b = 0.25
alpha_u = 0.50
q_val = 20.0
gamma_val = 0.30
aw_init = 0.01
ab_init = 0.01
itera = 150

with st.expander("📐 點擊展開：經典雛菊世界數學原理與生物物理聯立方程"):
    st.markdown(r"""
    ### 數學公式說明
    - **行星反照率**：由白雛菊覆蓋率 $a_w$、黑雛菊覆蓋率 $a_b$ 與裸地 $a_u = 1 - a_w - a_b$ 線性疊加：
      $$\alpha_p = a_w \alpha_w + a_b \alpha_b + a_u \alpha_u$$
    - **行星有效溫度**：
      $$T_p = \left( \frac{S_0 L (1 - \alpha_p)}{\sigma} \right)^{1/4} - 273.15$$
    - **局地微氣候溫度**（局地反照率差異吸收能量，使黑雛菊周邊更熱、白雛菊周邊更冷）：
      $$T_w = T_p + q(\alpha_p - \alpha_w), \quad T_b = T_p + q(\alpha_p - \alpha_b)$$
    - **溫度生長函數**（最適溫度為 $22.5^\circ\text{C}$）：
      $$\beta(T) = \max\left(0, 1 - 0.003265(22.5 - T)^2\right)$$
    - **族群消長方程式**：
      $$\frac{da_w}{dt} = a_w(a_u \beta(T_w) - \gamma), \quad \frac{da_b}{dt} = a_b(a_u \beta(T_b) - \gamma)$$
    """)

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 1. 時間動態演化 (Time Dynamics)",
    "☀️ 2. 太陽光度掃描與恆溫相圖 (Luminosity Homeostasis)",
    "🧪 3. 溫度響應生長函數 $\\beta(T)$ (Growth Curve)",
    "📋 4. 數值診斷與數據下載 (Diagnostics)"
])

# Tab 1: Time Dynamics
df_dw, t_nobio = run_daisyworld(
    S0=s0, L=l_val, alpha_w=alpha_w, alpha_b=alpha_b, alpha_u=alpha_u,
    q=q_val, gamma=gamma_val, aw_init=aw_init, ab_init=ab_init, itera=itera
)

# Tab 1: Time Dynamics
with tab1:
    st.subheader("經典雛菊世界時間演化軌跡")

    render_engine = st.radio(
        "圖表渲染模式",
        ["⚡ 60 FPS 絲滑高幀率畫布 (坐標軸固化，曲線零重劃、零閃爍)", "📊 標準 Plotly 向量圖表模式"],
        horizontal=True,
        key="daisy0d_engine_choice"
    )

    if "60 FPS" in render_engine:
        components.html(
            get_interactive_daisy0d_html(
                s0=s0, l_val=l_val, alpha_w=alpha_w, alpha_b=alpha_b, alpha_u=alpha_u,
                q_val=q_val, gamma_val=gamma_val, aw_init=aw_init, ab_init=ab_init, itera=itera
            ),
            height=820,
            scrolling=False
        )
    else:
        last = df_dw.iloc[-1]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_stat_card("行星調控溫度 $T_p$", f"{last['行星平均溫度 (℃)']:.2f} ℃", f"死星無生物溫: {t_nobio:.2f} ℃")
        with col2:
            render_stat_card("黑雛菊覆蓋率 $a_b$", f"{last['黑雛菊覆蓋率']*100:.1f} %", f"黑雛菊溫: {last['黑雛菊溫度 (℃)']:.1f} ℃")
        with col3:
            render_stat_card("白雛菊覆蓋率 $a_w$", f"{last['白雛菊覆蓋率']*100:.1f} %", f"白雛菊溫: {last['白雛菊溫度 (℃)']:.1f} ℃")
        with col4:
            render_stat_card("裸地覆蓋率 $a_u$", f"{last['裸地覆蓋率']*100:.1f} %", f"行星反照率: {last['行星反照率']:.3f}")

        d_col1, d_col2 = st.columns(2)
        with d_col1:
            fig_cov = go.Figure()
            fig_cov.add_trace(go.Scatter(
                x=df_dw["時間"], y=df_dw["黑雛菊覆蓋率"],
                mode="lines", line=dict(color="#334155", width=3), name="黑雛菊 (Black Daisy)"
            ))
            fig_cov.add_trace(go.Scatter(
                x=df_dw["時間"], y=df_dw["白雛菊覆蓋率"],
                mode="lines", line=dict(color="#f8fafc", width=3), name="白雛菊 (White Daisy)"
            ))
            fig_cov.add_trace(go.Scatter(
                x=df_dw["時間"], y=df_dw["裸地覆蓋率"],
                mode="lines", line=dict(color="#d97706", width=2, dash="dash"), name="裸地 (Bare Ground)"
            ))
            fig_cov.update_layout(get_plotly_layout("雛菊物種覆蓋率時間消長", "時間", "覆蓋率 (0~1)", y_range=[0.0, 1.0]))
            render_plotly_chart(fig_cov, key="dw0d_cov_chart")

        with d_col2:
            fig_tp = go.Figure()
            fig_tp.add_trace(go.Scatter(
                x=df_dw["時間"], y=df_dw["行星平均溫度 (℃)"],
                mode="lines", line=dict(color="#22c55e", width=3), name="雛菊調節後行星均溫 $T_p$"
            ))
            fig_tp.add_hline(y=t_nobio, line_dash="dash", line_color="#ef4444", annotation_text=f"無生物死星基線 ({t_nobio:.1f}℃)")
            fig_tp.add_hline(y=22.5, line_dash="dot", line_color="#00e5ff", annotation_text="最適生長溫度 (22.5℃)")
            fig_tp.update_layout(get_plotly_layout("行星溫度調控效應 vs 死星基線", "時間", "溫度 (℃)", y_range=[0.0, 50.0]))
            render_plotly_chart(fig_tp, key="dw0d_tp_chart")

# Tab 2: Luminosity Sweep
with tab2:
    st.subheader("太陽光度連續掃描：恆溫調節相圖 (Homeostasis Curve)")
    st.markdown("觀察隨恆星演化光度 $L$ 逐漸增強（0.6 至 1.6 倍）時，生命如何自動切換主導物種（冷時黑雛菊繁茂吸熱、熱時白雛菊繁茂散熱），維持幾乎恆定的宜居溫度！")

    with st.spinner("正在計算太陽光度連續平衡態..."):
        df_l = sweep_daisyworld_luminosity(
            S0=s0, l_min=0.6, l_max=1.65, num_l=50,
            alpha_w=alpha_w, alpha_b=alpha_b, alpha_u=alpha_u,
            q=q_val, gamma=gamma_val
        )

    l_col1, l_col2 = st.columns(2)
    with l_col1:
        fig_l_temp = go.Figure()
        fig_l_temp.add_trace(go.Scatter(
            x=df_l["L"], y=df_l["調控溫度 (℃)"],
            mode="lines", line=dict(color="#22c55e", width=3.5), name="雛菊調控行星溫度 $T_p$"
        ))
        fig_l_temp.add_trace(go.Scatter(
            x=df_l["L"], y=df_l["無生物溫度 (℃)"],
            mode="lines", line=dict(color="#ef4444", width=2.5, dash="dash"), name="無生物死星對照線"
        ))
        fig_l_temp.add_vline(x=l_val, line_dash="dash", line_color="#00e5ff", annotation_text=f"目前 L: {l_val:.2f}")
        fig_l_temp.update_layout(get_plotly_layout("光度 L vs 行星平衡溫度 (蓋亞恆溫平台)", "太陽光度 L", "平衡溫度 (℃)", x_range=[0.6, 1.65], y_range=[0.0, 60.0]))
        render_plotly_chart(fig_l_temp, key="dw0d_l_temp_chart")

    with l_col2:
        fig_l_cov = go.Figure()
        fig_l_cov.add_trace(go.Scatter(
            x=df_l["L"], y=df_l["黑雛菊覆蓋率"],
            mode="lines", line=dict(color="#475569", width=2.5), name="黑雛菊 (低光度保溫)"
        ))
        fig_l_cov.add_trace(go.Scatter(
            x=df_l["L"], y=df_l["白雛菊覆蓋率"],
            mode="lines", line=dict(color="#f8fafc", width=2.5), name="白雛菊 (高光度散熱)"
        ))
        fig_l_cov.add_vline(x=l_val, line_dash="dash", line_color="#00e5ff")
        fig_l_cov.update_layout(get_plotly_layout("物種隨光度演化的接替消長", "太陽光度 L", "平衡覆蓋率", x_range=[0.6, 1.65], y_range=[0.0, 1.0]))
        render_plotly_chart(fig_l_cov, key="dw0d_l_cov_chart")

# Tab 3: Growth Function
with tab3:
    st.subheader("雛菊溫度生長率函數 $\\beta(T)$")
    t_range = np.linspace(0.0, 45.0, 200)
    beta_vals = beta_growth(t_range)

    fig_beta = go.Figure()
    fig_beta.add_trace(go.Scatter(
        x=t_range, y=beta_vals,
        mode="lines", line=dict(color="#00e5ff", width=3), name="生長係數 $\\beta(T)$"
    ))
    fig_beta.add_vline(x=22.5, line_dash="dash", line_color="#22c55e", annotation_text="最適生長點 22.5℃")
    fig_beta.add_hline(y=gamma_val, line_dash="dot", line_color="#ef4444", annotation_text=f"死亡率臨界 \\gamma = {gamma_val}")
    fig_beta.update_layout(get_plotly_layout("拋物線生長函數 (最適溫度 22.5℃，可生存區間 5℃ ~ 40℃)", "溫度 (℃)", "生長率 $\\beta$", x_range=[0.0, 45.0], y_range=[0.0, 1.05]))
    render_plotly_chart(fig_beta, key="dw0d_beta_chart")

# Tab 4: Diagnostics
with tab4:
    st.subheader("模擬數值表格")
    st.dataframe(df_dw.style.format({
        "時間": "{:.1f}",
        "白雛菊覆蓋率": "{:.4f}",
        "黑雛菊覆蓋率": "{:.4f}",
        "裸地覆蓋率": "{:.4f}",
        "行星平均溫度 (℃)": "{:.2f}",
        "白雛菊溫度 (℃)": "{:.2f}",
        "黑雛菊溫度 (℃)": "{:.2f}",
        "行星反照率": "{:.4f}"
    }), use_container_width=True)

    csv_dw = df_dw.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 下載經典雛菊世界模擬數據 (CSV)",
        data=csv_dw,
        file_name=f"daisyworld0d_S0_{s0}_L_{l_val}.csv",
        mime="text/csv"
    )



