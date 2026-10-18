"""
Page 6: 1D Latitudinal Grey Daisyworld Interactive Experiment Site.
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
    render_sync_input,
    set_param_value,
    render_dynamic_controller,
    execute_dynamic_step
)
from models.daisy_1d import run_daisyworld_with_grey_1d

st.set_page_config(
    page_title="1D 緯度灰雛菊世界 | 獨立實驗網站",
    page_icon="🌿",
    layout="wide"
)

apply_custom_styles()

render_hero(
    title="一維緯度灰雛菊世界 (1D Latitudinal Grey Daisyworld)",
    subtitle="在空間維度上引入中性反照率的第三物種（灰雛菊），探討三物種在不同緯度的空間競爭、棲位劃分與對氣候調節的影響。",
    badges=["1D Grey Daisyworld", "3-Species Spatial Competition", "Niche Differentiation", "Neutral Feedbacks"]
)

# Sidebar Parameters
st.sidebar.header("⚙️ 1D 灰雛菊空間參數")

if "daisygrey1d_preset" not in st.session_state:
with st.sidebar:
    st.header("⚙️ 1D 灰雛菊空間參數")

    if "daisygrey1d_preset" not in st.session_state:
        st.session_state["daisygrey1d_preset"] = "標準三物種空間平衡 (S0=2100, L=1.0)"

    preset = st.selectbox(
        "🎯 預設情境 (Scenario Presets)",
        ["自訂參數 (Custom)", "標準三物種空間平衡 (S0=2100, L=1.0)", "灰雛菊高初始佔據 (ag_init=0.08)", "極區黑灰競爭 (S0=1850)", "赤道白灰競爭 (S0=2350)"],
        index=1
    )

    if preset != st.session_state["daisygrey1d_preset"] and preset != "自訂參數 (Custom)":
        st.session_state["daisygrey1d_preset"] = preset
        if preset == "標準三物種空間平衡 (S0=2100, L=1.0)":
            set_param_value("s0_1dwg", 2100.0)
            set_param_value("l_val_1dwg", 1.0)
            set_param_value("ag_init_1dwg", 0.01)
        elif preset == "灰雛菊高初始佔據 (ag_init=0.08)":
            set_param_value("s0_1dwg", 2100.0)
            set_param_value("l_val_1dwg", 1.0)
            set_param_value("ag_init_1dwg", 0.08)
        elif preset == "極區黑灰競爭 (S0=1850)":
            set_param_value("s0_1dwg", 1850.0)
            set_param_value("l_val_1dwg", 1.0)
            set_param_value("ag_init_1dwg", 0.01)
        elif preset == "赤道白灰競爭 (S0=2350)":
            set_param_value("s0_1dwg", 2350.0)
            set_param_value("l_val_1dwg", 1.0)
            set_param_value("ag_init_1dwg", 0.01)

    s0 = render_sync_input("太陽常數 S₀ (W/m²)", "s0_1dwg", 1400.0, 2800.0, 2100.0, 50.0, format="%.1f")
    l_val = render_sync_input("太陽光度因子 L", "l_val_1dwg", 0.6, 1.6, 1.0, 0.02, format="%.2f")
    k_diff = render_sync_input("大氣熱擴散傳遞 K (W/m²/℃)", "k_diff_1dwg", 0.5, 9.0, 3.87, 0.1, format="%.2f")

    with st.expander("🔬 反照率與初始分佈 (滑桿 + 精確數值)", expanded=False):
        alpha_w = render_sync_input("白雛菊反照率 α_w", "alpha_w_1dwg", 0.5, 0.9, 0.75, 0.02, format="%.2f")
        alpha_b = render_sync_input("黑雛菊反照率 α_b", "alpha_b_1dwg", 0.1, 0.4, 0.25, 0.02, format="%.2f")
        alpha_g = render_sync_input("灰雛菊反照率 α_g", "alpha_g_1dwg", 0.3, 0.7, 0.50, 0.02, format="%.2f")
        alpha_u = render_sync_input("裸地反照率 α_u", "alpha_u_1dwg", 0.3, 0.7, 0.50, 0.02, format="%.2f")
        q_val = render_sync_input("微氣候係數 q (℃)", "q_val_1dwg", 5.0, 40.0, 20.0, 1.0, format="%.1f")
        gamma_val = render_sync_input("死亡率 γ", "gamma_val_1dwg", 0.05, 0.6, 0.3, 0.02, format="%.2f")
        ag_init = render_sync_input("灰雛菊初始覆蓋率", "ag_init_1dwg", 0.001, 0.2, 0.01, 0.005, format="%.3f")
        itera = render_sync_input("迭代步數", "itera_1dwg", 30, 300, 150, 25, is_int=True)

    # Dynamic Sweeper Controller
    param_specs_1dwg = {
        "太陽常數 S₀": {"key": "s0_1dwg", "min": 1400.0, "max": 2800.0, "step": 50.0, "unit": "W/m²"},
        "太陽光度 L": {"key": "l_val_1dwg", "min": 0.6, "max": 1.6, "step": 0.02, "unit": ""},
        "大氣擴散係數 K": {"key": "k_diff_1dwg", "min": 0.5, "max": 9.0, "step": 0.2, "unit": "W/m²/℃"},
        "灰雛菊初始覆蓋率": {"key": "ag_init_1dwg", "min": 0.001, "max": 0.2, "step": 0.01, "unit": ""}
    }
    render_dynamic_controller(param_specs_1dwg, page_prefix="daisygrey1d")

# Run Simulation
history_grey_1d, lats_grey_1d, temp_nobio_g = run_daisyworld_with_grey_1d(
    S0=s0, L=l_val, alpha_w=alpha_w, alpha_b=alpha_b, alpha_g=alpha_g, alpha_u=alpha_u,
    q=q_val, gamma=gamma_val, ag_init=ag_init, K=k_diff, itera=itera
)

final_g = history_grey_1d[-1]

tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ 1. 三物種空間棲位分佈 (3-Species Spatial Profile)",
    "🌡️ 2. 溫度調控 vs 無生物死星 (Temperature Comparison)",
    "🎬 3. 動態演化播放器 (Dynamic Step Playback)",
    "📋 4. 診斷矩陣表 (Diagnostics Table)"
])

# Tab 1: 3-Species Profile
with tab1:
    st.subheader("1D 灰雛菊世界：三物種緯度平衡分佈")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_stat_card("全球加權均溫", f"{final_g['mean_t']:.2f} ℃")
    with col2:
        render_stat_card("赤道白雛菊", f"{final_g['aw'][-1]*100:.1f} %")
    with col3:
        render_stat_card("極區黑雛菊", f"{final_g['ab'][0]*100:.1f} %")
    with col4:
        render_stat_card("中緯度灰雛菊", f"{final_g['ag'][4]*100:.1f} %")
    with col5:
        render_stat_card("全域裸地率", f"{np.mean(final_g['au'])*100:.1f} %")

    fig_3sp = go.Figure()
    fig_3sp.add_trace(go.Scatter(
        x=lats_grey_1d, y=final_g["ab"],
        mode="lines+markers", marker=dict(size=8, color="#475569"),
        line=dict(color="#475569", width=3), name="黑雛菊 (極區優勢保溫)"
    ))
    fig_3sp.add_trace(go.Scatter(
        x=lats_grey_1d, y=final_g["aw"],
        mode="lines+markers", marker=dict(size=8, color="#f8fafc"),
        line=dict(color="#f8fafc", width=3), name="白雛菊 (赤道優勢降溫)"
    ))
    fig_3sp.add_trace(go.Scatter(
        x=lats_grey_1d, y=final_g["ag"],
        mode="lines+markers", marker=dict(size=8, color="#94a3b8"),
        line=dict(color="#94a3b8", width=3, dash="dash"), name="灰雛菊 (中性物種)"
    ))
    fig_3sp.add_trace(go.Scatter(
        x=lats_grey_1d, y=final_g["au"],
        mode="lines+markers", marker=dict(size=6, color="#d97706"),
        line=dict(color="#d97706", width=2, dash="dot"), name="裸地資源"
    ))
    fig_3sp.update_layout(get_plotly_layout(
        "各緯度最終平衡覆蓋率分佈 (黑 / 白 / 灰 / 裸地)",
        "緯度 (度)", "覆蓋率 (0~1)", height=500
    ))
    st.plotly_chart(fig_3sp, use_container_width=True)

# Tab 2: Temperature
with tab2:
    st.subheader("三物種調控後的緯度溫度剖面 vs 無生物死星")
    fig_t_g = go.Figure()
    fig_t_g.add_trace(go.Scatter(
        x=lats_grey_1d, y=final_g["temp"],
        mode="lines+markers", marker=dict(size=9, color="#22c55e"),
        line=dict(color="#22c55e", width=3.5), name="三物種雛菊調控溫度"
    ))
    fig_t_g.add_trace(go.Scatter(
        x=lats_grey_1d, y=temp_nobio_g,
        mode="lines+markers", marker=dict(size=8, color="#ef4444"),
        line=dict(color="#ef4444", width=2.5, dash="dash"), name="無生命行星溫度剖面"
    ))
    fig_t_g.add_hline(y=22.5, line_dash="dot", line_color="#00e5ff", annotation_text="最適生長溫度 (22.5℃)")
    fig_t_g.update_layout(get_plotly_layout(
        "各緯度溫度剖面對比 (含灰雛菊生態系 vs 死星基線)",
        "緯度 (度)", "溫度 (℃)", height=500
    ))
    st.plotly_chart(fig_t_g, use_container_width=True)

# Tab 3: Step Playback
with tab3:
    st.subheader("三物種空間動態演化時間步步進播放器")
    selected_idx = st.slider("時間步 (Step)", 0, len(history_grey_1d) - 1, 0, 1)
    step_data = history_grey_1d[selected_idx]

    s_c1, s_c2 = st.columns(2)
    with s_c1:
        f_s = go.Figure()
        f_s.add_trace(go.Scatter(x=lats_grey_1d, y=step_data["ab"], mode="lines+markers", name="黑雛菊", line=dict(color="#475569")))
        f_s.add_trace(go.Scatter(x=lats_grey_1d, y=step_data["aw"], mode="lines+markers", name="白雛菊", line=dict(color="#f8fafc")))
        f_s.add_trace(go.Scatter(x=lats_grey_1d, y=step_data["ag"], mode="lines+markers", name="灰雛菊", line=dict(color="#94a3b8", dash="dash")))
        f_s.update_layout(get_plotly_layout(f"步數 {selected_idx} 物種分佈", "緯度 (度)", "覆蓋率"))
        st.plotly_chart(f_s, use_container_width=True)

    with s_c2:
        f_t = go.Figure()
        f_t.add_trace(go.Scatter(x=lats_grey_1d, y=step_data["temp"], mode="lines+markers", name="溫度", line=dict(color="#f59e0b", width=3)))
        f_t.update_layout(get_plotly_layout(f"步數 {selected_idx} 溫度剖面 (均溫: {step_data['mean_t']:.2f}℃)", "緯度 (度)", "溫度 (℃)"))
        st.plotly_chart(f_t, use_container_width=True)

# Tab 4: Diagnostics Table
with tab4:
    st.subheader("平衡狀態各緯度數據診斷矩陣")
    df_matrix_g = pd.DataFrame({
        "緯度 (度)": lats_grey_1d,
        "最終溫度 (℃)": final_g["temp"],
        "無生物溫度 (℃)": temp_nobio_g,
        "白雛菊覆蓋率": final_g["aw"],
        "黑雛菊覆蓋率": final_g["ab"],
        "灰雛菊覆蓋率": final_g["ag"],
        "裸地覆蓋率": final_g["au"],
        "行星反照率": final_g["alpha_p"]
    })

    st.dataframe(df_matrix_g.style.format({
        "最終溫度 (℃)": "{:.2f}",
        "無生物溫度 (℃)": "{:.2f}",
        "白雛菊覆蓋率": "{:.4f}",
        "黑雛菊覆蓋率": "{:.4f}",
        "灰雛菊覆蓋率": "{:.4f}",
        "裸地覆蓋率": "{:.4f}",
        "行星反照率": "{:.4f}"
    }), use_container_width=True)

    csv_1d_grey = df_matrix_g.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 下載 1D 灰雛菊世界數據 (CSV)",
        data=csv_1d_grey,
        file_name=f"daisyworld1d_grey_S0_{s0}_L_{l_val}.csv",
        mime="text/csv"
    )

# Execute dynamic animation step at end of page
execute_dynamic_step(param_specs_1dwg, page_prefix="daisygrey1d")

