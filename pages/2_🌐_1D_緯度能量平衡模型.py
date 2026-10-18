"""
Page 2: 1D Latitudinal Energy Balance Model (1D EBM - Budyko-Sellers) Interactive Experiment Site.
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
from models.ebm_1d import (
    run_ebm_1d,
    run_ebm_1d_history,
    sweep_ebm_1d_parameter
)

import streamlit.components.v1 as components
from utils.interactive_ebm_1d import get_interactive_ebm1d_html

st.set_page_config(
    page_title="1D 緯度能量平衡模型 (1D EBM) | 獨立實驗網站",
    page_icon="🌐",
    layout="wide"
)

apply_custom_styles()

render_hero(
    title="一維緯度能量平衡模型 (1D Latitudinal EBM)",
    subtitle="基於 Budyko-Sellers 擴散架構，研究太陽輻射緯度分佈、大氣經向熱傳遞、各緯度反照率階梯與冰雪邊界線 (Ice Edge)。",
    badges=["1D EBM", "Budyko-Sellers", "Heat Diffusion K", "Ice Edge Dynamics", "60 FPS Canvas"]
)

# Sidebar: Model Guide & Key Concepts (Unified single control panel is inside the interactive canvas)
with st.sidebar:
    st.header("🌐 1D 緯度能量平衡實驗室")
    st.markdown("""
    **實驗特色**
    - ⚡ **60 FPS 前端絲滑畫布**：坐標軸固化，曲線零重劃、零閃爍。
    - 🎛️ **雙向同步面板**：滑桿平滑拖曳 + 精確數值鍵盤直接輸入。
    - 🎬 **連續動態掃描**：內建 60 FPS 硬體加速平滑推移動畫。
    
    ---
    **核心物理機制**
    - **太陽常數因子 ($Frac\_SC$)**：整體縮放太陽常數，驅動地球暖化或寒冷化。
    - **大氣熱擴散係數 ($K$)**：決定赤道熱量向極區傳輸的效率。$K$ 越大，赤道與極區溫差越小。
    - **冰雪臨界溫 ($T_{crit}$)**：低於此溫度地表轉為高反照率冰雪 ($a_{ice}$)。
    - **出射公式**：Budyko 線性出射 $R_{out} = A + B \\cdot T$。
    
    ---
    **參考基準**
    - 現代地球赤道溫：約 $25 \\sim 28$ ℃
    - 現代地球極區溫：約 $-20 \\sim -30$ ℃
    - 現代冰雪邊界線：約 $72^\\circ\\text{N}$
    """)

# Default parameters
sc = 1370.0
frac_sc = 1.0
k_diff = 3.87
a_param = 230.0
b_param = 2.17
tcrit = -10.0
aice = 0.60
aland = 0.30
itera = 50

with st.expander("📐 點擊展開：1D EBM 數學原理與各緯度熱傳導公式"):
    st.markdown(r"""
    ### 數學公式說明
    在 1D 緯度能量平衡模型中，將北半球離散為 9 個緯度帶（$85^\circ, 75^\circ, \dots, 6^\circ$）。
    在緯度帶 $i$ 上的局地能量收支為：
    $$R_{\text{in},i}(1 - \alpha_i) = R_{\text{out},i} + F_i$$
    其中：
    - 入射輻射：$R_{\text{in},i} = \frac{SC \times \text{Frac\_SC}}{4} \times \text{SunWt}_i$
    - 出射長波輻射（Budyko 線性化公式）：$R_{\text{out},i} = A + B \cdot T_i$
    - 經向大氣熱輸送通量（將熱量由高溫帶輸送至低溫帶）：
      $$F_i = K (T_i - \bar{T})$$
      其中 $\bar{T} = \frac{\sum T_i \cos\phi_i}{\sum \cos\phi_i}$ 為全球面積加權平均溫度。
    - 迭代格式：
      $$T_i^{(n+1)} = \frac{R_{\text{in},i}(1 - \alpha_i^{(n)}) + K \bar{T}^{(n)} - A}{B + K}$$
    - 反照率開關：若 $T_i < T_{\text{crit}}$ 則 $\alpha_i = a_{\text{ice}}$，否則 $\alpha_i = a$。
    """)

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 1. 平衡緯度剖面 (Equilibrium Profile)",
    "🎬 2. 動態收斂迭代動畫 (Convergence Animation)",
    "🔍 3. 太陽強度與擴散敏感度掃描 (Parameter Sweep)",
    "📋 4. 各緯度能量通量守恆診斷表 (Diagnostics Table)"
])

df_1d, mean_t = run_ebm_1d(
    SC=sc, Frac_SC=frac_sc, A=a_param, B=b_param, K=k_diff,
    aice=aice, a=aland, Tcrit=tcrit, itera=itera
)

# Tab 1: Equilibrium Profile
with tab1:
    st.subheader("1D EBM 各緯度最終平衡分佈")

    render_engine = st.radio(
        "圖表渲染模式",
        ["⚡ 60 FPS 絲滑高幀率畫布 (坐標軸固化，曲線零重劃、零閃爍)", "📊 標準 Plotly 向量圖表模式"],
        horizontal=True,
        key="ebm1d_engine_choice"
    )

    if "60 FPS" in render_engine:
        components.html(
            get_interactive_ebm1d_html(
                sc=sc, frac_sc=frac_sc, a_param=a_param, b_param=b_param,
                k_diff=k_diff, aice=aice, aland=aland, tcrit=tcrit, itera=itera
            ),
            height=820,
            scrolling=False
        )
    else:
        ice_lats = [lat for lat, t in zip(df_1d["緯度 (度)"], df_1d["最終溫度 (℃)"]) if t < tcrit]
        ice_edge = min(ice_lats) if ice_lats else 90.0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_stat_card("全球加權均溫", f"{mean_t:.2f} ℃")
        with col2:
            render_stat_card("赤道 (6°N) 溫度", f"{df_1d['最終溫度 (℃)'].iloc[-1]:.2f} ℃")
        with col3:
            render_stat_card("極區 (85°N) 溫度", f"{df_1d['最終溫度 (℃)'].iloc[0]:.2f} ℃")
        with col4:
            edge_text = f"{ice_edge:.0f}°N 以北" if ice_edge < 90 else "無冰覆蓋"
            render_stat_card("冰雪邊界線 (Ice Edge)", edge_text, f"臨界值: {tcrit}℃")

        pcol1, pcol2 = st.columns(2)
        with pcol1:
            fig_t = go.Figure()
            fig_t.add_trace(go.Scatter(
                x=df_1d["緯度 (度)"], y=df_1d["最終溫度 (℃)"],
                mode="lines+markers", marker=dict(size=8, color="#ef4444"),
                line=dict(color="#ef4444", width=3), name="平衡溫度 (℃)"
            ))
            fig_t.add_hline(y=tcrit, line_dash="dash", line_color="#38bdf8", annotation_text=f"結冰臨界線 {tcrit}℃")
            fig_t.update_layout(get_plotly_layout("緯度 vs 平衡溫度", "緯度 (度)", "溫度 (℃)", x_range=[-90, 90], y_range=[-60, 45]))
            render_plotly_chart(fig_t, key="ebm1d_t_chart")

        with pcol2:
            fig_a = go.Figure()
            fig_a.add_trace(go.Scatter(
                x=df_1d["緯度 (度)"], y=df_1d["最終反照率 (Albedo)"],
                mode="lines+markers", marker=dict(size=8, color="#00e5ff", symbol="square"),
                line=dict(color="#00e5ff", width=2.5), name="反照率 (Albedo)"
            ))
            fig_a.update_layout(get_plotly_layout("緯度 vs 階梯反照率", "緯度 (度)", "反照率 (Albedo)", x_range=[-90, 90], y_range=[0.0, 1.0]))
            render_plotly_chart(fig_a, key="ebm1d_a_chart")

# Tab 2: Dynamic Convergence Animation
with tab2:
    st.subheader("動態收斂過程步進播放器")
    st.markdown("拖動下方滑桿或點擊播放，觀察各緯度溫度與反照率如何由初始猜測值擴散收斂至穩定態。")

    hist_1d, lats_1d = run_ebm_1d_history(
        SC=sc, Frac_SC=frac_sc, A=a_param, B=b_param, K=k_diff,
        aice=aice, a=aland, Tcrit=tcrit, itera=itera
    )

    selected_step = st.slider("選擇迭代步 (Step)", 0, len(hist_1d) - 1, 0, 1)
    step_data = hist_1d[selected_step]

    anim_col1, anim_col2 = st.columns(2)
    with anim_col1:
        fig_step_t = go.Figure()
        fig_step_t.add_trace(go.Scatter(
            x=lats_1d, y=step_data["temp"],
            mode="lines+markers", marker=dict(size=9, color="#f97316"),
            line=dict(color="#f97316", width=3), name=f"步數 {selected_step} 溫度"
        ))
        fig_step_t.add_hline(y=tcrit, line_dash="dash", line_color="#00e5ff", annotation_text=f"Tcrit = {tcrit}℃")
        fig_step_t.update_layout(get_plotly_layout(
            f"迭代步 {selected_step} 溫度分佈 (均溫: {step_data['mean_t']:.2f} ℃)",
            "緯度 (度)", "溫度 (℃)", x_range=[-90, 90], y_range=[-60, 45]
        ))
        render_plotly_chart(fig_step_t, key="ebm1d_step_t_chart")

    with anim_col2:
        fig_step_a = go.Figure()
        fig_step_a.add_trace(go.Scatter(
            x=lats_1d, y=step_data["albedo"],
            mode="lines+markers", marker=dict(size=9, color="#a855f7", symbol="square"),
            line=dict(color="#a855f7", width=3), name=f"步數 {selected_step} 反照率"
        ))
        fig_step_a.update_layout(get_plotly_layout(
            f"迭代步 {selected_step} 反照率階梯 (冰緣: {step_data['ice_edge']:.0f}°N)",
            "緯度 (度)", "反照率", x_range=[-90, 90], y_range=[0.0, 1.0]
        ))
        render_plotly_chart(fig_step_a, key="ebm1d_step_a_chart")

# Tab 3: Parameter Sweep
with tab3:
    st.subheader("參數敏感度連續掃描 (Parameter Sweep)")
    sweep_param = st.radio("選擇掃描參數", ["太陽強度因子 Frac_SC", "熱擴散係數 K"], horizontal=True)

    base_cfg = {
        "SC": sc, "Frac_SC": frac_sc, "A": a_param, "B": b_param, "K": k_diff,
        "aice": aice, "a": aland, "Tcrit": tcrit, "itera": itera
    }

    if sweep_param == "太陽強度因子 Frac_SC":
        sweep_data = sweep_ebm_1d_parameter("Frac_SC", 0.75, 1.25, 25, base_cfg)
        param_keys = [d["Frac_SC"] for d in sweep_data]
        x_label = "太陽強度因子 Frac_SC"
    else:
        sweep_data = sweep_ebm_1d_parameter("K", 0.5, 8.0, 25, base_cfg)
        param_keys = [d["K"] for d in sweep_data]
        x_label = "大氣熱擴散係數 K (W/m²/℃)"

    mean_temps = [d["mean_t"] for d in sweep_data]
    ice_edges = [d["ice_edge"] for d in sweep_data]

    sw_col1, sw_col2 = st.columns(2)
    with sw_col1:
        fig_sw_t = go.Figure()
        fig_sw_t.add_trace(go.Scatter(
            x=param_keys, y=mean_temps,
            mode="lines+markers", marker=dict(size=6, color="#22c55e"),
            line=dict(color="#22c55e", width=2.5), name="全球平均溫度 (℃)"
        ))
        fig_sw_t.update_layout(get_plotly_layout(f"{x_label} vs 全球均溫", x_label, "全球均溫 (℃)"))
        render_plotly_chart(fig_sw_t, key="ebm1d_sw_t_chart")

    with sw_col2:
        fig_sw_ice = go.Figure()
        fig_sw_ice.add_trace(go.Scatter(
            x=param_keys, y=ice_edges,
            mode="lines+markers", marker=dict(size=6, color="#38bdf8"),
            line=dict(color="#38bdf8", width=2.5), name="冰緣最低緯度 (°N)"
        ))
        fig_sw_ice.update_layout(get_plotly_layout(f"{x_label} vs 冰雪前緣位置", x_label, "冰緣緯度 (°N)", y_range=[0, 90]))
        render_plotly_chart(fig_sw_ice, key="ebm1d_sw_ice_chart")

# Tab 4: Diagnostics Table
with tab4:
    st.subheader("各緯度能量通量守恆診斷數據表")
    st.dataframe(df_1d.style.format({
        "太陽權重 (SunWt)": "{:.3f}",
        "面積權重 (cos)": "{:.3f}",
        "入射能量 (R_in)": "{:.2f}",
        "最終溫度 (℃)": "{:.2f}",
        "最終反照率 (Albedo)": "{:.2f}",
        "出射輻射 (R_out)": "{:.2f}",
        "傳導通量 (F)": "{:.2f}",
        "吸收能量": "{:.2f}",
        "守恆差值 (Balance)": "{:.5f}"
    }), use_container_width=True)

    csv_1d = df_1d.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 下載 1D EBM 平衡數據 (CSV)",
        data=csv_1d,
        file_name=f"ebm1d_SC_{sc}_FracSC_{frac_sc}_K_{k_diff}.csv",
        mime="text/csv"
    )



