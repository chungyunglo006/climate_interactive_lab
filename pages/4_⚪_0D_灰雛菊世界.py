"""
Page 4: 0D Daisyworld with Grey Daisies Interactive Experiment Site.
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
    run_daisyworld_with_grey,
    sweep_daisyworld_grey_luminosity,
    run_daisyworld
)
import streamlit.components.v1 as components
from utils.interactive_daisy_grey_0d import get_interactive_daisy_grey_0d_html

st.set_page_config(
    page_title="0D 灰雛菊世界 (Daisyworld with Grey Daisies) | 獨立實驗網站",
    page_icon="⚪",
    layout="wide"
)

apply_custom_styles()

render_hero(
    title="帶有灰雛菊因子的三物種雛菊世界 (Grey Daisyworld)",
    subtitle="引入反照率等於裸地的中性物種（灰雛菊），探討「無氣候調節貢獻的物種」在生態系中的競爭動態與自然選擇效應。",
    badges=["Grey Daisy", "Neutral Albedo", "3-Species Competition", "Ecological Cheater Hypothesis", "60 FPS Canvas"]
)

# Sidebar: Model Guide & Key Concepts (Unified single control panel is inside the interactive canvas)
with st.sidebar:
    st.header("⚪ 0D 灰雛菊實驗室")
    st.markdown("""
    **實驗特色**
    - ⚡ **60 FPS 前端絲滑畫布**：坐標軸固化，曲線零重劃、零閃爍。
    - 🎛️ **雙向同步面板**：滑桿平滑拖曳 + 精確數值鍵盤直接輸入。
    - 🎬 **連續動態掃描**：內建 60 FPS 硬體加速平滑推移動畫。
    
    ---
    **核心生物物理機制**
    - **灰雛菊 ($a_g$)**：反照率等於裸地 ($0.50$)，為「中性突變種/搭便車者 (Cheater)」，不對全球氣候提供主動保溫或降溫反饋。
    - **土地競爭**：灰雛菊佔據空間 ($a_u = 1 - a_w - a_b - a_g$)，限制黑白雛菊擴張。
    - **穩定性檢驗**：在適溫下灰雛菊能共存，但在偏離最適溫度的極端環境下，黑白雛菊依然憑藉微氣候優勢重新奪回主導權！
    
    ---
    **參考基準**
    - 灰雛菊反照率：$0.50$
    - 最適生長溫度：$22.5$ ℃
    - 死亡率：$0.30$
    """)

# Default parameters
s0 = 917.0
l_val = 1.0
alpha_w = 0.75
alpha_b = 0.25
alpha_g = 0.50
alpha_u = 0.50
q_val = 20.0
gamma_val = 0.30
aw_init = 0.01
ab_init = 0.01
ag_init = 0.01
itera = 150

with st.expander("📐 點擊展開：灰雛菊模型原理與演化論批判"):
    st.markdown(r"""
    ### 灰雛菊的科學意涵
    蓋亞假說常受到傳統達爾文主義演化生物學家的質疑：
    *「如果生物只為了自身繁殖優勢，那麼一個反照率等於裸地（不費力調控氣候，坐享其成的『搭便車者/中性突變種』灰雛菊）是否會淘汰黑白雛菊，導致氣候恆溫調控崩潰？」*

    在數學上：
    $$\alpha_p = a_w \alpha_w + a_b \alpha_b + a_g \alpha_g + a_u \alpha_u$$
    由於灰雛菊的反照率等於裸地（$\alpha_g = \alpha_u = 0.50$）：
    - 灰雛菊的局地溫度 $T_g = T_p + q(\alpha_p - \alpha_g)$ 完全取決於當時由黑白雛菊塑造的全球反照率 $\alpha_p$。
    - 灰雛菊佔據了生存空間 $a_u = 1 - a_w - a_b - a_g$，與黑白雛菊競爭土地。
    - 模擬證明：即使加入中性灰雛菊，在黑白雛菊建立的最適溫度環境下，灰雛菊能共存，但在偏離最適溫度的極端氣候下，具備**主動微氣候保溫/散熱優勢**的黑白雛菊依然能在局部取得更高生長率！
    """)

tab1, tab2, tab3 = st.tabs([
    "📈 1. 三物種時間動態消長 (Three-Species Dynamics)",
    "☀️ 2. 光度掃描與氣候調控比較 (Luminosity Comparison)",
    "📋 3. 診斷表格與數據導出 (Diagnostics)"
])

# Tab 1: Three-Species Dynamics
df_grey, t_nobio = run_daisyworld_with_grey(
    S0=s0, L=l_val, alpha_w=alpha_w, alpha_b=alpha_b, alpha_g=alpha_g, alpha_u=alpha_u,
    q=q_val, gamma=gamma_val, aw_init=aw_init, ab_init=ab_init, ag_init=ag_init, itera=itera
)

# Tab 1: Three-Species Dynamics
with tab1:
    st.subheader("黑、白、灰三物種共存與時間演化")

    render_engine = st.radio(
        "圖表渲染模式",
        ["⚡ 60 FPS 絲滑高幀率畫布 (坐標軸固化，曲線零重劃、零閃爍)", "📊 標準 Plotly 向量圖表模式"],
        horizontal=True,
        key="daisygrey0d_engine_choice"
    )

    if "60 FPS" in render_engine:
        components.html(
            get_interactive_daisy_grey_0d_html(
                s0=s0, l_val=l_val, alpha_w=alpha_w, alpha_b=alpha_b, alpha_g=alpha_g, alpha_u=alpha_u,
                q_val=q_val, gamma_val=gamma_val, aw_init=aw_init, ab_init=ab_init, ag_init=ag_init, itera=itera
            ),
            height=820,
            scrolling=False
        )
    else:
        last = df_grey.iloc[-1]
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            render_stat_card("調控均溫 $T_p$", f"{last['行星平均溫度 (℃)']:.2f} ℃")
        with col2:
            render_stat_card("黑雛菊覆蓋率", f"{last['黑雛菊覆蓋率']*100:.1f} %")
        with col3:
            render_stat_card("白雛菊覆蓋率", f"{last['白雛菊覆蓋率']*100:.1f} %")
        with col4:
            render_stat_card("灰雛菊覆蓋率", f"{last['灰雛菊覆蓋率']*100:.1f} %")
        with col5:
            render_stat_card("裸地覆蓋率", f"{last['裸地覆蓋率']*100:.1f} %")

        c_col1, c_col2 = st.columns(2)
        with c_col1:
            fig_cov3 = go.Figure()
            fig_cov3.add_trace(go.Scatter(
                x=df_grey["時間"], y=df_grey["黑雛菊覆蓋率"],
                mode="lines", line=dict(color="#334155", width=3), name="黑雛菊 (保溫)"
            ))
            fig_cov3.add_trace(go.Scatter(
                x=df_grey["時間"], y=df_grey["白雛菊覆蓋率"],
                mode="lines", line=dict(color="#f8fafc", width=3), name="白雛菊 (散熱)"
            ))
            fig_cov3.add_trace(go.Scatter(
                x=df_grey["時間"], y=df_grey["灰雛菊覆蓋率"],
                mode="lines", line=dict(color="#94a3b8", width=3, dash="dash"), name="灰雛菊 (中性競爭者)"
            ))
            fig_cov3.add_trace(go.Scatter(
                x=df_grey["時間"], y=df_grey["裸地覆蓋率"],
                mode="lines", line=dict(color="#d97706", width=1.5, dash="dot"), name="裸地資源"
            ))
            fig_cov3.update_layout(get_plotly_layout("三物種覆蓋率時間消長", "時間", "覆蓋率 (0~1)", y_range=[0.0, 1.0]))
            render_plotly_chart(fig_cov3, key="dw0d_grey_cov_chart")

        with c_col2:
            fig_temp3 = go.Figure()
            fig_temp3.add_trace(go.Scatter(
                x=df_grey["時間"], y=df_grey["行星平均溫度 (℃)"],
                mode="lines", line=dict(color="#22c55e", width=3), name="行星平均溫度 $T_p$"
            ))
            fig_temp3.add_trace(go.Scatter(
                x=df_grey["時間"], y=df_grey["灰雛菊溫度 (℃)"],
                mode="lines", line=dict(color="#94a3b8", width=2, dash="dash"), name="灰雛菊局地溫度 $T_g$"
            ))
            fig_temp3.add_hline(y=t_nobio, line_dash="dash", line_color="#ef4444", annotation_text=f"無生物基線 ({t_nobio:.1f}℃)")
            fig_temp3.update_layout(get_plotly_layout("行星平均溫度與物種局部溫度", "時間", "溫度 (℃)", y_range=[0.0, 50.0]))
            render_plotly_chart(fig_temp3, key="dw0d_grey_temp_chart")

# Tab 2: Luminosity Comparison
with tab2:
    st.subheader("太陽光度連續掃描：雙物種 vs 三物種恆溫平台對比")
    st.markdown("觀察加入灰雛菊後，恆溫調節平台的範圍與穩定性是否改變。")

    with st.spinner("計算三物種光度掃描中..."):
        df_l_grey = sweep_daisyworld_grey_luminosity(
            S0=s0, l_min=0.6, l_max=1.65, num_l=45,
            alpha_w=alpha_w, alpha_b=alpha_b, alpha_g=alpha_g, alpha_u=alpha_u,
            q=q_val, gamma=gamma_val
        )

    l_fig = go.Figure()
    l_fig.add_trace(go.Scatter(
        x=df_l_grey["L"], y=df_l_grey["調控溫度 (℃)"],
        mode="lines", line=dict(color="#00e5ff", width=3.5), name="三物種 (含灰雛菊) 調控溫度"
    ))
    l_fig.add_trace(go.Scatter(
        x=df_l_grey["L"], y=df_l_grey["無生物溫度 (℃)"],
        mode="lines", line=dict(color="#ef4444", width=2, dash="dash"), name="無生物死星基線"
    ))
    l_fig.update_layout(get_plotly_layout("光度 L vs 行星溫度 (含灰雛菊)", "太陽光度 L", "溫度 (℃)", x_range=[0.6, 1.65], y_range=[0.0, 60.0]))
    render_plotly_chart(l_fig, key="dw0d_grey_l_fig")

    cov_fig = go.Figure()
    cov_fig.add_trace(go.Scatter(x=df_l_grey["L"], y=df_l_grey["黑雛菊覆蓋率"], mode="lines", name="黑雛菊", line=dict(color="#475569")))
    cov_fig.add_trace(go.Scatter(x=df_l_grey["L"], y=df_l_grey["白雛菊覆蓋率"], mode="lines", name="白雛菊", line=dict(color="#f8fafc")))
    cov_fig.add_trace(go.Scatter(x=df_l_grey["L"], y=df_l_grey["灰雛菊覆蓋率"], mode="lines", name="灰雛菊", line=dict(color="#94a3b8", dash="dash")))
    cov_fig.update_layout(get_plotly_layout("三物種平衡覆蓋率隨光度之分佈", "太陽光度 L", "覆蓋率", x_range=[0.6, 1.65], y_range=[0.0, 1.0]))
    render_plotly_chart(cov_fig, key="dw0d_grey_cov_fig")

# Tab 3: Diagnostics
with tab3:
    st.subheader("模擬數據矩陣")
    st.dataframe(df_grey.style.format({
        "時間": "{:.1f}",
        "白雛菊覆蓋率": "{:.4f}",
        "黑雛菊覆蓋率": "{:.4f}",
        "灰雛菊覆蓋率": "{:.4f}",
        "裸地覆蓋率": "{:.4f}",
        "行星平均溫度 (℃)": "{:.2f}",
        "白雛菊溫度 (℃)": "{:.2f}",
        "黑雛菊溫度 (℃)": "{:.2f}",
        "灰雛菊溫度 (℃)": "{:.2f}",
        "行星反照率": "{:.4f}"
    }), use_container_width=True)

    csv_grey = df_grey.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 下載灰雛菊模擬數據 (CSV)",
        data=csv_grey,
        file_name=f"daisyworld_grey_S0_{s0}_L_{l_val}.csv",
        mime="text/csv"
    )



