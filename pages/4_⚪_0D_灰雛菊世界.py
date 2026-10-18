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
    render_plotly_chart,
    render_sync_input,
    set_param_value
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
    badges=["Grey Daisy", "Neutral Albedo", "3-Species Competition", "Ecological Cheater Hypothesis", "動態演變畫布"]
)

# Unified Master Parameter Control Panel in Sidebar (Controls BOTH Plotly & Dynamic Canvas)
with st.sidebar:
    st.header("⚙️ 灰雛菊實驗參數控制面板")

    if "daisygrey0d_preset" not in st.session_state:
        st.session_state["daisygrey0d_preset"] = "標準三物種共存 (L=1.0, ag=0.01)"

    preset = st.selectbox(
        "🎯 預設情境 (Scenario Presets)",
        [
            "自訂參數 (Custom)",
            "標準三物種共存 (L=1.0, ag=0.01)",
            "灰雛菊強勢入侵 (ag_init=0.10)",
            "高光度三物種競爭 (L=1.20)",
            "低光度黑灰競爭 (L=0.80)"
        ],
        index=1
    )

    if preset != st.session_state["daisygrey0d_preset"] and preset != "自訂參數 (Custom)":
        st.session_state["daisygrey0d_preset"] = preset
        if preset == "標準三物種共存 (L=1.0, ag=0.01)":
            set_param_value("s0_dwg", 917.0)
            set_param_value("l_val_dwg", 1.0)
            set_param_value("ag_init_dwg", 0.01)
        elif preset == "灰雛菊強勢入侵 (ag_init=0.10)":
            set_param_value("s0_dwg", 917.0)
            set_param_value("l_val_dwg", 1.0)
            set_param_value("ag_init_dwg", 0.10)
        elif preset == "高光度三物種競爭 (L=1.20)":
            set_param_value("s0_dwg", 917.0)
            set_param_value("l_val_dwg", 1.20)
            set_param_value("ag_init_dwg", 0.01)
        elif preset == "低光度黑灰競爭 (L=0.80)":
            set_param_value("s0_dwg", 917.0)
            set_param_value("l_val_dwg", 0.80)
            set_param_value("ag_init_dwg", 0.01)

    s0 = render_sync_input("太陽常數 S₀ (W/m²)", "s0_dwg", 700.0, 1300.0, 917.0, 10.0, format="%.1f")
    l_val = render_sync_input("太陽光度因子 L", "l_val_dwg", 0.5, 1.8, 1.0, 0.02, format="%.2f")

    with st.expander("🔬 反照率與初始覆蓋率 (滑桿 + 精確數值)", expanded=False):
        alpha_w = render_sync_input("白雛菊反照率 α_w", "alpha_w_dwg", 0.5, 0.9, 0.75, 0.02, format="%.2f")
        alpha_b = render_sync_input("黑雛菊反照率 α_b", "alpha_b_dwg", 0.1, 0.4, 0.25, 0.02, format="%.2f")
        alpha_g = render_sync_input("灰雛菊反照率 α_g (中性物種)", "alpha_g_dwg", 0.3, 0.7, 0.50, 0.02, format="%.2f")
        alpha_u = render_sync_input("裸地反照率 α_u", "alpha_u_dwg", 0.3, 0.7, 0.50, 0.02, format="%.2f")
        q_val = render_sync_input("微氣候係數 q (℃)", "q_val_dwg", 5.0, 40.0, 20.0, 1.0, format="%.1f")
        gamma_val = render_sync_input("死亡率 γ", "gamma_val_dwg", 0.05, 0.6, 0.3, 0.02, format="%.2f")
        aw_init = render_sync_input("白雛菊初始值", "aw_init_dwg", 0.001, 0.3, 0.01, 0.005, format="%.3f")
        ab_init = render_sync_input("黑雛菊初始值", "ab_init_dwg", 0.001, 0.3, 0.01, 0.005, format="%.3f")
        ag_init = render_sync_input("灰雛菊初始值", "ag_init_dwg", 0.001, 0.3, 0.01, 0.005, format="%.3f")
        itera = render_sync_input("迭代步數", "itera_dwg", 50, 400, 150, 25, is_int=True)

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
        ["⚡ 動態演變畫布", "📊 標準 Plotly 向量圖表"],
        horizontal=True,
        key="daisygrey0d_engine_choice"
    )

    if "動態演變" in render_engine:
        components.html(
            get_interactive_daisy_grey_0d_html(
                s0=s0, l_val=l_val, alpha_w=alpha_w, alpha_b=alpha_b, alpha_g=alpha_g, alpha_u=alpha_u,
                q_val=q_val, gamma_val=gamma_val, aw_init=aw_init, ab_init=ab_init, ag_init=ag_init, itera=itera
            ),
            height=890,
            scrolling=True
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



