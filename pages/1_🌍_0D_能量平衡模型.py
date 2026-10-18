"""
Page 1: 0D Energy Balance Model (0D EBM) Interactive Experiment Site.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.ui import apply_custom_styles, render_hero, render_stat_card, get_plotly_layout
from models.ebm_0d import (
    run_ebm,
    find_three_equilibrium_states,
    calculate_ebm_bifurcation,
    run_ebm_transient_collapse,
    run_ebm_constant
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
    badges=["0D EBM", "Budyko-Sellers", "Ice-Albedo Feedback", "S-Curve", "Tipping Points"]
)

# Sidebar: Presets and Parameters
st.sidebar.header("⚙️ 實驗控制面板")

preset = st.sidebar.selectbox(
    "🎯 預設情境 (Scenario Presets)",
    ["自訂參數 (Custom)", "現今溫暖地球 (Modern Earth)", "冰球地球 (Snowball Earth)", "第一臨界點失控崩潰 (Tipping Collapse ~1288 W/m²)", "高太陽輻射超溫暖態"]
)

if preset == "現今溫暖地球 (Modern Earth)":
    default_s0 = 1368.0
    default_t_init = 288.0
elif preset == "冰球地球 (Snowball Earth)":
    default_s0 = 1200.0
    default_t_init = 230.0
elif preset == "第一臨界點失控崩潰 (Tipping Collapse ~1288 W/m²)":
    default_s0 = 1288.6
    default_t_init = 280.0
elif preset == "高太陽輻射超溫暖態":
    default_s0 = 1600.0
    default_t_init = 295.0
else:
    default_s0 = 1368.0
    default_t_init = 288.0

s0 = st.sidebar.slider("太陽常數 $S_0$ (W/m²)", min_value=800.0, max_value=2000.0, value=default_s0, step=5.0)
t_init = st.sidebar.slider("初始溫度 $T_{init}$ (K)", min_value=200.0, max_value=320.0, value=default_t_init, step=1.0)

with st.sidebar.expander("🔬 進階物性參數 (Physical Parameters)"):
    alpha_ice = st.slider("冰雪反照率 $\\alpha_{ice}$", 0.4, 0.8, 0.6, 0.05)
    alpha_land = st.slider("陸地反照率 $\\alpha_{land}$", 0.1, 0.5, 0.3, 0.05)
    t_ice = st.slider("冰雪臨界溫度 $T_{ice}$ (K)", 240.0, 275.0, 263.0, 1.0)
    t_land = st.slider("暖地臨界溫度 $T_{land}$ (K)", 270.0, 300.0, 283.0, 1.0)
    epsilon = st.slider("有效發射率 $\\epsilon$ (溫室效應)", 0.4, 0.9, 0.62, 0.02)
    dt = st.slider("時間步長 $\\Delta t$ (年)", 0.01, 0.5, 0.1, 0.01)
    itera = st.slider("總迭代步數", 50, 500, 200, 25)

# Mathematical Principle Expander
with st.expander("📐 點擊展開：模型數學原理與方程式"):
    st.markdown(r"""
    ### 數學公式說明
    零維能量平衡模型將地球視為單一均質系統，熱力學方程式為：
    $$C_{\text{ocean}} \frac{dT}{dt} = R_{\text{in}} - R_{\text{out}} = \frac{S_0}{4}(1 - \alpha(T)) - \epsilon \sigma T^4$$
    其中：
    - $S_0$：太陽常數 (約 $1368 \text{ W/m}^2$)，因地球自轉與球體幾何面積比，地表平均入射為 $S_0 / 4$。
    - $\sigma = 5.670374 \times 10^{-8} \text{ W/m}^2\text{K}^4$ 為 Stefan-Boltzmann 常數。
    - $\epsilon$ 為大氣長波有效發射率（代表溫室氣體捕捉後穿透大氣輻射至太空之比例，典型值 $\approx 0.62$）。
    - 反照率 $\alpha(T)$ 隨溫度呈現三段式冰雪反饋：
    $$\alpha(T) = \begin{cases}
    \alpha_{\text{ice}}, & T \le T_{\text{ice}} \\
    \alpha_{\text{ice}} + (\alpha_{\text{land}} - \alpha_{\text{ice}}) \frac{T - T_{\text{ice}}}{T_{\text{land}} - T_{\text{ice}}}, & T_{\text{ice}} < T < T_{\text{land}} \\
    \alpha_{\text{land}}, & T \ge T_{\text{land}}
    \end{cases}$$
    """)

# Main Tabs for Experiments
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 1. 溫度與能量演化 (Time Series)",
    "⚖️ 2. 三種全球平衡態分析 (Three Equilibria)",
    "🔀 3. 氣候分歧圖與遲滯迴線 (S-Curve & Hysteresis)",
    "❄️ 4. 冰期崩潰動態模擬 (Transient Collapse)"
])

# Tab 1: Time Series Evolution
with tab1:
    st.subheader("全球平均溫度與輻射通量演化")
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
        fig_temp.update_layout(get_plotly_layout("溫度隨時間演化歷程", "時間 (年)", "溫度 (℃)"))
        st.plotly_chart(fig_temp, use_container_width=True)

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
        fig_rad.update_layout(get_plotly_layout("能量平衡收支通量", "時間 (年)", "輻射通量 (W/m²)"))
        st.plotly_chart(fig_rad, use_container_width=True)

    # Data download
    csv = df_sim.to_csv(index=False).encode('utf-8')
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

    eq_states = find_three_equilibrium_states(
        S0=s0, alpha_ice=alpha_ice, alpha_land=alpha_land,
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
        name="吸收太陽輻射 $R_{in}(T) = \\frac{S_0}{4}(1-\\alpha(T))$"
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
        "全球平均溫度 $T$ (K)", "輻射通量 (W/m²)", height=520
    ))
    st.plotly_chart(fig_eq, use_container_width=True)

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
        bifur = calculate_ebm_bifurcation(
            alpha_ice=alpha_ice, alpha_land=alpha_land,
            T_ice=t_ice, T_land=t_land, epsilon=epsilon,
            s0_min=800.0, s0_max=2000.0, num_s0=240
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
        "太陽常數 $S_0$ (W/m²)", "平衡溫度 $T^*$ (K)", height=540
    ))
    st.plotly_chart(fig_bifur, use_container_width=True)

# Tab 4: Transient Collapse Simulation
with tab4:
    st.subheader("太陽輻射遞減下的氣候瞬態崩潰動態模擬")
    st.markdown("模擬太陽常數自 $1368$ W/m² 逐步衰減至 $1200$ W/m²。觀察溫暖起點與寒冷起點的氣候軌跡在穿過臨界點時的**突變斷崖**。")

    col_sim_btn, col_sim_info = st.columns([1, 3])
    with col_sim_btn:
        run_collapse = st.button("🚀 執行崩潰降溫模擬", type="primary")

    if run_collapse:
        with st.spinner("模擬計算中..."):
            collapse_data = run_ebm_transient_collapse(
                S0_start=1368.0, S0_end=1200.0, S0_steps=20,
                alpha_ice=alpha_ice, alpha_land=alpha_land,
                T_ice=t_ice, T_land=t_land, epsilon=epsilon
            )

            s0_list = [d["S0"] for d in collapse_data]
            tw_list = [d["T_warm_C"] for d in collapse_data]
            tc_list = [d["T_cold_C"] for d in collapse_data]

            fig_col = go.Figure()
            fig_col.add_trace(go.Scatter(
                x=s0_list, y=tw_list,
                mode="lines+markers", marker=dict(size=7),
                line=dict(color="#ef4444", width=3),
                name="溫暖地表起始軌跡 (Warm-Start Branch)"
            ))
            fig_col.add_trace(go.Scatter(
                x=s0_list, y=tc_list,
                mode="lines+markers", marker=dict(size=7),
                line=dict(color="#38bdf8", width=3, dash="dash"),
                name="冰封地表起始軌跡 (Cold-Start Branch)"
            ))
            fig_col.add_vline(x=1288.6, line_dash="dot", line_color="#fbbf24", annotation_text="雪球地球臨界點 (Collapse Threshold)")

            fig_col.update_layout(get_plotly_layout(
                "太陽常數遞減時的氣候突變斷崖 (Transient Bifurcation Collapse)",
                "太陽常數 $S_0$ (W/m²)", "地表溫度 (℃)", height=480
            ))
            st.plotly_chart(fig_col, use_container_width=True)

            st.success("✅ 觀察結果：當太陽常數降至約 1288 W/m² 以下時，溫暖起始軌跡無法再維持液態水，反照率劇增造成溫度斷崖式墜落至 -40℃ 以下，全球徹底冰封！")
