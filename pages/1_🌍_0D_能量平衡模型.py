"""
Page 1: 0D Energy Balance Model (0D EBM) Interactive Experiment Site.
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
    set_param_value,
    render_dynamic_controller,
    execute_dynamic_step
)
from models.ebm_0d import (
    run_ebm,
    find_three_equilibrium_states,
    calculate_ebm_bifurcation,
    run_ebm_transient_collapse,
    run_ebm_continuous_transient_collapse,
    run_ebm_constant
)


@st.cache_data
def get_cached_bifurcation(alpha_ice, alpha_land, t_ice, t_land, epsilon):
    """Caches bifurcation curve to ensure ultra-smooth real-time dynamic animation."""
    return calculate_ebm_bifurcation(
        alpha_ice=alpha_ice, alpha_land=alpha_land,
        T_ice=t_ice, T_land=t_land, epsilon=epsilon,
        s0_min=800.0, s0_max=2000.0, num_s0=240
    )


st.set_page_config(
    page_title="0D 能量平衡模型 (0D EBM) | 獨立實驗網站",
    page_icon="🌍",
    layout="wide"
)

apply_custom_styles()

render_hero(
    title="零維能量平衡模型 (0D Energy Balance Model)",
    subtitle="探索全球平均溫度動態演化、冰雪反照率非線性反饋、三種平衡解以及氣候突變分歧點 (Bifurcation)。",
    badges=["0D EBM", "Budyko-Sellers", "Ice-Albedo Feedback", "S-Curve", "Tipping Points", "動態演變畫布"]
)

# Unified Master Parameter Control Panel in Sidebar (Controls BOTH Plotly & Dynamic Canvas)
with st.sidebar:
    st.header("⚙️ 0D 物理參數控制面板")

    if "ebm0d_preset" not in st.session_state:
        st.session_state["ebm0d_preset"] = "標準現代地球 (S0=1368, Tinit=288K)"

    preset = st.selectbox(
        "🎯 預設情境 (Scenario Presets)",
        [
            "自訂參數 (Custom)",
            "標準現代地球 (S0=1368, Tinit=288K)",
            "完全冰球地球 (S0=1200, Tinit=230K)",
            "臨界崩潰前夕 (S0=1288.6, Tinit=280K)",
            "極端酷熱地球 (S0=1600, Tinit=295K)"
        ],
        index=1
    )

    if preset != st.session_state["ebm0d_preset"] and preset != "自訂參數 (Custom)":
        st.session_state["ebm0d_preset"] = preset
        if preset == "標準現代地球 (S0=1368, Tinit=288K)":
            set_param_value("s0", 1368.0)
            set_param_value("t_init", 288.0)
            set_param_value("epsilon", 0.62)
            set_param_value("alpha_ice", 0.60)
            set_param_value("alpha_land", 0.30)
        elif preset == "完全冰球地球 (S0=1200, Tinit=230K)":
            set_param_value("s0", 1200.0)
            set_param_value("t_init", 230.0)
            set_param_value("epsilon", 0.62)
            set_param_value("alpha_ice", 0.60)
            set_param_value("alpha_land", 0.30)
        elif preset == "臨界崩潰前夕 (S0=1288.6, Tinit=280K)":
            set_param_value("s0", 1288.6)
            set_param_value("t_init", 280.0)
            set_param_value("epsilon", 0.62)
            set_param_value("alpha_ice", 0.60)
            set_param_value("alpha_land", 0.30)
        elif preset == "極端酷熱地球 (S0=1600, Tinit=295K)":
            set_param_value("s0", 1600.0)
            set_param_value("t_init", 295.0)
            set_param_value("epsilon", 0.62)
            set_param_value("alpha_ice", 0.60)
            set_param_value("alpha_land", 0.30)

    s0 = render_sync_input("太陽常數 S₀ (W/m²)", "s0", 800.0, 2000.0, 1368.0, 10.0, format="%.1f")
    t_init = render_sync_input("初始溫度 T_init (K)", "t_init", 200.0, 320.0, 288.0, 1.0, format="%.1f")

    with st.expander("🔬 進階物性與反照率參數 (滑桿 + 精確數值)", expanded=False):
        epsilon = render_sync_input("大氣長波有效發射率 ε", "epsilon", 0.40, 0.90, 0.62, 0.01, format="%.2f")
        alpha_ice = render_sync_input("完全冰雪反照率 α_ice", "alpha_ice", 0.40, 0.85, 0.60, 0.02, format="%.2f")
        alpha_land = render_sync_input("無冰陸地反照率 α_land", "alpha_land", 0.10, 0.50, 0.30, 0.02, format="%.2f")
        t_ice = render_sync_input("結冰臨界溫度 T_ice (K)", "t_ice", 240.0, 275.0, 263.0, 1.0, format="%.1f")
        t_land = render_sync_input("無冰臨界溫度 T_land (K)", "t_land", 270.0, 300.0, 283.0, 1.0, format="%.1f")
        itera = render_sync_input("迭代步數 (Steps)", "itera_ebm0d", 50, 500, 200, 25, is_int=True)

dt = 0.1

# Mathematical Principle Expander
with st.expander("📐 點擊展開：模型數學原理與方程式"):
    st.markdown(r"""
    ### 數學公式說明
    零維能量平衡模型將地球視為單一均質系統，熱力學方程式為：
    """)
    st.latex(r"C_{\text{ocean}} \frac{dT}{dt} = R_{\text{in}} - R_{\text{out}} = \frac{S_0}{4}(1 - \alpha(T)) - \epsilon \sigma T^4")
    st.markdown(r"""
    其中：
    - $S_0$：太陽常數 (約 $1368 \text{ W/m}^2$)，因地球自轉與球體幾何面積比，地表平均入射為 $S_0 / 4$。
    - $\sigma = 5.670374 \times 10^{-8} \text{ W/m}^2\text{K}^4$ 為 Stefan-Boltzmann 常數。
    - $\epsilon$ 為大氣長波有效發射率（代表溫室氣體捕捉後穿透大氣輻射至太空之比例，典型值 $\approx 0.62$）。
    - 反照率 $\alpha(T)$ 隨溫度呈現三段式冰雪反饋：
    """)
    st.latex(r"""\alpha(T) = \begin{cases}
    \alpha_{\text{ice}}, & T \le T_{\text{ice}} \\
    \alpha_{\text{ice}} + (\alpha_{\text{land}} - \alpha_{\text{ice}}) \frac{T - T_{\text{ice}}}{T_{\text{land}} - T_{\text{ice}}}, & T_{\text{ice}} < T < T_{\text{land}} \\
    \alpha_{\text{land}}, & T \ge T_{\text{land}}
    \end{cases}""")

# Main Tabs for Experiments
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 1. 溫度與能量演化 (Time Series)",
    "⚖️ 2. 三種全球平衡態分析 (Three Equilibria)",
    "🔀 3. 氣候分歧圖與遲滯迴線 (S-Curve & Hysteresis)",
    "❄️ 4. 冰期崩潰動態模擬 (Transient Collapse)"
])

import streamlit.components.v1 as components
from utils.interactive_ebm_0d import get_interactive_ebm0d_html

# Tab 1: Time Series Evolution
with tab1:
    st.subheader("全球平均溫度與輻射通量演化")
    
    render_engine = st.radio(
        "圖表渲染模式",
        ["⚡ 動態演變畫布", "📊 標準 Plotly 向量圖表"],
        horizontal=True,
        key="ebm0d_engine_choice"
    )

    if "動態演變畫布" in render_engine:
        components.html(
            get_interactive_ebm0d_html(
                s0=s0, t_init=t_init, alpha_ice=alpha_ice, alpha_land=alpha_land,
                t_ice=t_ice, t_land=t_land, epsilon=epsilon, dt=dt, itera=itera
            ),
            height=890,
            scrolling=True
        )
    else:
        df_sim = run_ebm(
            S0=s0, alpha_ice=alpha_ice, alpha_land=alpha_land,
            T_ice=t_ice, T_land=t_land, epsilon=epsilon,
            T_init=t_init, dt=dt, itera=itera
        )

        final_row = df_sim.iloc[-1]

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            render_stat_card("最終平衡溫度", f"{final_row['溫度 (K)']:.2f} K", f"{final_row['溫度 (℃)']:.2f} ℃")
        with col_m2:
            render_stat_card("最終行星反照率", f"{final_row['反照率 (Albedo)']:.3f}")
        with col_m3:
            render_stat_card("入射 / 出射能量", f"{final_row['入射能量 (W/m²)']:.1f} W/m²", f"出射: {final_row['出射能量 (W/m²)']:.1f} W/m²")
        with col_m4:
            imbalance_val = final_row['能量不平衡量 (W/m²)']
            status = "已達完美平衡" if abs(imbalance_val) < 0.01 else "尚未完全收斂"
            render_stat_card("淨輻射不平衡量", f"{imbalance_val:.4f} W/m²", status)

        chart_c1, chart_c2 = st.columns(2)
        with chart_c1:
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(
                x=df_sim["時間 (年)"], y=df_sim["溫度 (℃)"],
                mode="lines+markers", marker=dict(size=4),
                line=dict(color="#00e5ff", width=2.5), name="地表溫度 (℃)"
            ))
            fig_temp.add_hline(y=t_ice - 273.15, line_dash="dash", line_color="#38bdf8", annotation_text=f"冰封臨界溫 {t_ice-273.15:.1f}℃")
            fig_temp.add_hline(y=t_land - 273.15, line_dash="dash", line_color="#4ade80", annotation_text=f"無冰臨界溫 {t_land-273.15:.1f}℃")
            fig_temp.update_layout(get_plotly_layout(
                "溫度隨時間演化歷程", "時間 (年)", "溫度 (℃)",
                height=480, x_range=[0, itera * dt], y_range=[-45, 35]
            ))
            render_plotly_chart(fig_temp, key="ebm0d_temp_chart")

        with chart_c2:
            fig_rad = go.Figure()
            fig_rad.add_trace(go.Scatter(
                x=df_sim["時間 (年)"], y=df_sim["入射能量 (W/m²)"],
                mode="lines", line=dict(color="#f59e0b", width=2), name="吸收入射太陽輻射 $R_{in}$"
            ))
            fig_rad.add_trace(go.Scatter(
                x=df_sim["時間 (年)"], y=df_sim["出射能量 (W/m²)"],
                mode="lines", line=dict(color="#ef4444", width=2), name="釋放長波輻射 $R_{out}$"
            ))
            fig_rad.add_trace(go.Scatter(
                x=df_sim["時間 (年)"], y=df_sim["能量不平衡量 (W/m²)"],
                mode="lines", line=dict(color="#a855f7", width=1.5, dash="dot"), name="淨不平衡通量 $R_{in}-R_{out}$"
            ))
            fig_rad.update_layout(get_plotly_layout(
                "能量平衡收支通量", "時間 (年)", "輻射通量 (W/m²)",
                height=480, x_range=[0, itera * dt], y_range=[-20, 380]
            ))
            render_plotly_chart(fig_rad, key="ebm0d_rad_chart")

    # Data download
    df_sim_export = run_ebm(
        S0=s0, alpha_ice=alpha_ice, alpha_land=alpha_land,
        T_ice=t_ice, T_land=t_land, epsilon=epsilon,
        T_init=t_init, dt=dt, itera=itera
    )
    csv = df_sim_export.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 下載本次模擬數據 (CSV)",
        data=csv,
        file_name=f"ebm0d_simulation_S0_{s0}_Tinit_{t_init}.csv",
        mime="text/csv"
    )

# Tab 2: Three Equilibrium States
with tab2:
    st.subheader("三種全球溫度平衡解 (Nonlinear Intersection Analysis)")
    st.markdown("由於冰雪反照率隨溫度增加而下降（正反饋），使得吸收太陽能曲線 $R_{in}(T)$ 呈現非線性 S 型，與長波輻射出射曲線 $R_{out}(T) = \\epsilon\\sigma T^4$ 產生**多個交點**。")

    s0_eq_col1, s0_eq_col2 = st.columns([3, 1])
    with s0_eq_col1:
        s0_tab2 = st.slider(
            "動態調整太陽常數 S₀ (W/m²) 觀察交點分歧與鞍節分岔",
            800.0, 2000.0, float(s0), 5.0, key="s0_eq_slider"
        )
    with s0_eq_col2:
        st.metric("分析太陽常數", f"{s0_tab2:.1f} W/m²")

    eq_states = find_three_equilibrium_states(
        S0=s0_tab2, alpha_ice=alpha_ice, alpha_land=alpha_land,
        T_ice=t_ice, T_land=t_land, epsilon=epsilon
    )

    t_curve = eq_states["T_curve"]
    rin_curve = eq_states["R_in"]
    rout_curve = eq_states["R_out"]

    s1 = eq_states["state1"]["T"]
    s2 = eq_states["state2"]["T"]
    s3 = eq_states["state3"]["T"]

    eq_c1, eq_c2, eq_c3 = st.columns(3)
    with eq_c1:
        if s1 is not None:
            render_stat_card("狀態 ①：無冰地球 (現代地球)", f"{s1:.2f} K ({s1-273.15:.2f} ℃)", "穩定平衡態 (Stable)")
        else:
            render_stat_card("狀態 ①：無冰地球", "不存在", "太陽輻射過低")
    with eq_c2:
        if s2 is not None:
            render_stat_card("狀態 ②：部分結冰地球", f"{s2:.2f} K ({s2-273.15:.2f} ℃)", "⚠️ 不穩定分水嶺 (Unstable)")
        else:
            render_stat_card("狀態 ②：部分結冰地球", "不存在", "單一吸引子區間")
    with eq_c3:
        if s3 is not None:
            render_stat_card("狀態 ③：完全冰封雪球地球", f"{s3:.2f} K ({s3-273.15:.2f} ℃)", "穩定平衡態 (Stable)")
        else:
            render_stat_card("狀態 ③：雪球地球", "不存在", "太陽輻射過高")

    fig_eq = go.Figure()
    fig_eq.add_trace(go.Scatter(
        x=t_curve, y=rin_curve,
        mode="lines", line=dict(color="#38bdf8", width=3),
        name=f"吸收太陽輻射 $R_{{in}}(T) = \\frac{{{s0_tab2:.0f}}}{{4}}(1-\\alpha(T))$"
    ))
    fig_eq.add_trace(go.Scatter(
        x=t_curve, y=rout_curve,
        mode="lines", line=dict(color="#f43f5e", width=3),
        name="出射長波輻射 $R_{out}(T) = \\epsilon \\sigma T^4$"
    ))

    # Add intersections
    sigma = 5.670374e-8
    if s1 is not None:
        y1 = epsilon * sigma * (s1 ** 4)
        fig_eq.add_trace(go.Scatter(
            x=[s1], y=[y1], mode="markers+text",
            marker=dict(color="#22c55e", size=14, symbol="circle"),
            text=[f"狀態① 溫暖穩定 ({s1:.1f} K)"], textposition="top left",
            name="狀態① 溫暖穩定態"
        ))
    if s2 is not None:
        y2 = epsilon * sigma * (s2 ** 4)
        fig_eq.add_trace(go.Scatter(
            x=[s2], y=[y2], mode="markers+text",
            marker=dict(color="#eab308", size=14, symbol="diamond"),
            text=[f"狀態② 不穩定分歧 ({s2:.1f} K)"], textposition="bottom center",
            name="狀態② 不穩定分水嶺"
        ))
    if s3 is not None:
        y3 = epsilon * sigma * (s3 ** 4)
        fig_eq.add_trace(go.Scatter(
            x=[s3], y=[y3], mode="markers+text",
            marker=dict(color="#06b6d4", size=14, symbol="circle"),
            text=[f"狀態③ 雪球地球穩定 ({s3:.1f} K)"], textposition="top right",
            name="狀態③ 雪球地球態"
        ))

    fig_eq.update_layout(get_plotly_layout(
        f"0D EBM 輻射收支交點分析 (目前 $S_0 = {s0:.1f}$ W/m²)",
        "全球平均溫度 $T$ (K)", "輻射通量 (W/m²)", height=520,
        x_range=[180, 320], y_range=[50, 400]
    ))
    render_plotly_chart(fig_eq, key="ebm0d_eq_chart")

# Tab 3: Bifurcation Diagram & Hysteresis
with tab3:
    st.subheader("氣候穩定度分歧圖與遲滯迴線 (Bifurcation S-Curve)")
    st.markdown("""
    當太陽常數 $S_0$ 緩慢改變時，平衡解溫度 $T^*$ 的分歧曲線呈現 **S 型遲滯迴線 (Hysteresis Loop)**。
    - **綠色分支**：穩定平衡態（微擾後可自發恢復）。
    - **紅色分支**：不穩定平衡態（微擾後將迅速失控墜入雪球或暴衝至溫室地球）。
    - **臨界點 (Tipping Points)**：當 $S_0$ 低於臨界點 $\\sim 1288.6$ W/m² 時，溫暖態突然崩潰，直接墜入雪球地球！
    """)

    with st.spinner("正在計算全域分歧分支曲線..."):
        bifur = get_cached_bifurcation(
            alpha_ice=alpha_ice, alpha_land=alpha_land,
            t_ice=t_ice, t_land=t_land, epsilon=epsilon
        )

    fig_bifur = go.Figure()
    fig_bifur.add_trace(go.Scatter(
        x=bifur["stable_s0"], y=bifur["stable_T"],
        mode="markers", marker=dict(color="#22c55e", size=3),
        name="穩定平衡分支 (Stable Branch)"
    ))
    fig_bifur.add_trace(go.Scatter(
        x=bifur["unstable_s0"], y=bifur["unstable_T"],
        mode="markers", marker=dict(color="#ef4444", size=3),
        name="不穩定平衡分支 (Unstable Branch)"
    ))

    # Mark current S0 position
    fig_bifur.add_vline(x=s0, line_dash="dash", line_color="#00e5ff", annotation_text=f"目前 S0: {s0:.0f} W/m²")
    fig_bifur.add_vline(x=1288.6, line_dash="dot", line_color="#38bdf8", annotation_text="第1臨界崩潰點 ~1288.6 W/m²")
    fig_bifur.add_vline(x=1682.5, line_dash="dot", line_color="#c084fc", annotation_text="第2解凍臨界點 ~1682.5 W/m²")

    fig_bifur.update_layout(get_plotly_layout(
        "0D EBM 氣候分歧圖 (Bifurcation Diagram / S-curve)",
        "太陽常數 $S_0$ (W/m²)", "平衡溫度 $T^*$ (K)", height=540,
        x_range=[800, 2000], y_range=[200, 320]
    ))
    render_plotly_chart(fig_bifur, key="ebm0d_bifur_chart")

# Tab 4: Transient Collapse Simulation
with tab4:
    st.subheader("太陽輻射遞減下的氣候瞬態崩潰動態模擬")
    st.markdown("模擬太陽常數衰減穿過臨界點時，系統在冰雪反照率正反饋作用下的**突變斷崖（Tipping Point Catastrophe）**。")

    sim_mode = st.radio(
        "選擇模擬演化模式",
        ["🌊 連續時間動態數值積分 (高解析度連續瞬降曲線)", "🔍 準靜態階梯分歧掃描 (可自訂細分階數)"],
        horizontal=True
    )

    if "連續時間動態" in sim_mode:
        st.markdown("基於熱容量微分方程 $C \\frac{dT}{dt} = R_{in}(S_0(t)) - R_{out}(T)$ 進行連續高密度積分 ($dt = 0.05$ 年)，呈現極度平滑真實的動態崩潰與滯後相軌跡。")
        c_p1, c_p2, c_p3 = st.columns(3)
        with c_p1:
            ramp_down_yr = st.slider("太陽常數平滑衰減年限 (年)", 20.0, 150.0, 60.0, 5.0)
        with c_p2:
            s0_min_c = st.slider("衰退終點太陽常數 S_min (W/m²)", 1050.0, 1280.0, 1160.0, 10.0)
        with c_p3:
            include_rewarming = st.checkbox("包含隨後太陽增溫解凍歷程 (遲滯迴線)", value=True)

        if st.button("🚀 執行連續瞬降動態積分", type="primary", key="btn_run_continuous_collapse"):
            with st.spinner("正在進行高精度連續微分積分 (1600+ 時間步)..."):
                stay_yr = 20.0 if include_rewarming else 0.0
                ramp_up_yr = 80.0 if include_rewarming else 0.0
                df_dyn = run_ebm_continuous_transient_collapse(
                    S0_start=s0, S0_min=s0_min_c, S0_max=1750.0,
                    ramp_down_years=ramp_down_yr, stay_cold_years=stay_yr, ramp_up_years=ramp_up_yr,
                    T_init=t_init, alpha_ice=alpha_ice, alpha_land=alpha_land,
                    T_ice=t_ice, T_land=t_land, epsilon=epsilon, dt=0.05
                )

                dcol1, dcol2 = st.columns(2)
                with dcol1:
                    fig_dyn_t = go.Figure()
                    fig_dyn_t.add_trace(go.Scatter(
                        x=df_dyn["時間 (年)"], y=df_dyn["溫度 (℃)"],
                        mode="lines", line=dict(color="#00e5ff", width=3),
                        name="地表溫度連續瞬降曲線 (℃)"
                    ))
                    fig_dyn_t.add_hline(y=t_ice - 273.15, line_dash="dash", line_color="#38bdf8", annotation_text=f"結冰臨界線 {t_ice-273.15:.1f}℃")
                    fig_dyn_t.add_hline(y=t_land - 273.15, line_dash="dash", line_color="#4ade80", annotation_text=f"無冰臨界線 {t_land-273.15:.1f}℃")
                    fig_dyn_t.update_layout(get_plotly_layout(
                        "時間 vs 地表溫度瞬降軌跡 (Continuous Transient Drop)",
                        "時間 (年)", "地表溫度 (℃)", height=480
                    ))
                    render_plotly_chart(fig_dyn_t, key="ebm0d_dyn_t_chart")

                with dcol2:
                    fig_dyn_phase = go.Figure()
                    fig_dyn_phase.add_trace(go.Scatter(
                        x=df_dyn["太陽常數 (W/m²)"], y=df_dyn["溫度 (℃)"],
                        mode="lines", line=dict(color="#f43f5e", width=3),
                        name="相空間動態軌道"
                    ))
                    fig_dyn_phase.add_vline(x=1288.6, line_dash="dot", line_color="#fbbf24", annotation_text="靜態雪球臨界點 1288.6 W/m²")
                    if include_rewarming:
                        fig_dyn_phase.add_vline(x=1682.5, line_dash="dot", line_color="#c084fc", annotation_text="靜態解凍臨界點 1682.5 W/m²")
                    fig_dyn_phase.update_layout(get_plotly_layout(
                        "相空間動態遲滯軌道 (S₀ vs 溫度)",
                        "太陽常數 S₀ (W/m²)", "地表溫度 (℃)", height=480
                    ))
                    render_plotly_chart(fig_dyn_phase, key="ebm0d_dyn_phase_chart")

                st.success("✅ 連續數值積分完成：可清晰看見溫度隨時間平滑滑降，當日照低於臨界閾值時，反照率誘發失控反饋，形成如絲般順滑的突變瞬降大瀑布！")

    else:
        st.markdown("藉由逐步調整太陽常數並於每一步計算局部微熱平衡，可觀察準靜態分歧分支。")
        s_c1, s_c2 = st.columns(2)
        with s_c1:
            s0_steps = st.slider("掃描細分步數 (Steps - 越高越絲滑)", 20, 200, 120, 10)
        with s_c2:
            s0_end_sweep = st.slider("掃描終點太陽常數 (W/m²)", 1000.0, 1280.0, 1200.0, 10.0)

        if st.button("🚀 執行準靜態分歧降溫模擬", type="primary", key="btn_run_static_collapse"):
            with st.spinner(f"正在計算 {s0_steps} 階高解析度分歧點..."):
                collapse_data = run_ebm_transient_collapse(
                    S0_start=s0, S0_end=s0_end_sweep, S0_steps=s0_steps,
                    alpha_ice=alpha_ice, alpha_land=alpha_land,
                    T_ice=t_ice, T_land=t_land, epsilon=epsilon
                )

                s0_list = [d["S0"] for d in collapse_data]
                tw_list = [d["T_warm_C"] for d in collapse_data]
                tc_list = [d["T_cold_C"] for d in collapse_data]

                fig_col = go.Figure()
                fig_col.add_trace(go.Scatter(
                    x=s0_list, y=tw_list,
                    mode="lines+markers", marker=dict(size=4),
                    line=dict(color="#ef4444", width=3),
                    name="溫暖地表起始軌跡 (Warm-Start Branch)"
                ))
                fig_col.add_trace(go.Scatter(
                    x=s0_list, y=tc_list,
                    mode="lines+markers", marker=dict(size=4),
                    line=dict(color="#38bdf8", width=3, dash="dash"),
                    name="冰封地表起始軌跡 (Cold-Start Branch)"
                ))
                fig_col.add_vline(x=1288.6, line_dash="dot", line_color="#fbbf24", annotation_text="雪球地球臨界點 (Collapse Threshold)")

                fig_col.update_layout(get_plotly_layout(
                    "高細分太陽常數遞減氣候突變斷崖",
                    "太陽常數 $S_0$ (W/m²)", "地表溫度 (℃)", height=480
                ))
                render_plotly_chart(fig_col, key="ebm0d_col_chart")
                st.success("✅ 高密度掃描完成：展示了密集細分下的臨界分岔斷崖！")


# Simulation complete

