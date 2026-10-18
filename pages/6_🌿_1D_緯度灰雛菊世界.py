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
    render_plotly_chart,
    render_sync_input,
    set_param_value
)
from models.daisy_1d import run_daisyworld_with_grey_1d
import streamlit.components.v1 as components
from utils.interactive_daisy_grey_1d import get_interactive_daisy_grey_1d_html

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

# Sidebar: Master Unified Control Panel
with st.sidebar:
    st.header("🎛️ 實驗參數統一控制面板")

    preset = st.selectbox(
        "📌 預設實驗場景",
        [
            "自訂參數",
            "標準三物種共存 (L=1.0)",
            "高光度白灰優勢 (L=1.20)",
            "低光度黑灰優勢 (L=0.85)",
            "強大氣經向熱輸送 (K=6.0)",
            "弱大氣經向熱輸送 (K=1.5)"
        ],
        index=0
    )

    if preset != "自訂參數":
        if preset == "標準三物種共存 (L=1.0)":
            set_param_value("s0_1dwg", 2100.0)
            set_param_value("l_val_1dwg", 1.0)
            set_param_value("k_diff_1dwg", 3.87)
        elif preset == "高光度白灰優勢 (L=1.20)":
            set_param_value("s0_1dwg", 2100.0)
            set_param_value("l_val_1dwg", 1.20)
            set_param_value("k_diff_1dwg", 3.87)
        elif preset == "低光度黑灰優勢 (L=0.85)":
            set_param_value("s0_1dwg", 2100.0)
            set_param_value("l_val_1dwg", 0.85)
            set_param_value("k_diff_1dwg", 3.87)
        elif preset == "強大氣經向熱輸送 (K=6.0)":
            set_param_value("s0_1dwg", 2100.0)
            set_param_value("l_val_1dwg", 1.0)
            set_param_value("k_diff_1dwg", 6.0)
        elif preset == "弱大氣經向熱輸送 (K=1.5)":
            set_param_value("s0_1dwg", 2100.0)
            set_param_value("l_val_1dwg", 1.0)
            set_param_value("k_diff_1dwg", 1.5)

    s0 = render_sync_input("太陽常數 S₀ (W/m²)", "s0_1dwg", 1200.0, 2800.0, 2100.0, 20.0, format="%.1f")
    l_val = render_sync_input("太陽光度因子 L", "l_val_1dwg", 0.5, 1.8, 1.0, 0.02, format="%.2f")
    k_diff = render_sync_input("大氣熱輸送係數 K (W/m²/℃)", "k_diff_1dwg", 0.5, 10.0, 3.87, 0.1, format="%.2f")

    with st.expander("🔬 反照率與物性參數 (滑桿 + 精確數值)", expanded=False):
        alpha_w = render_sync_input("白雛菊反照率 α_w", "alpha_w_1dwg", 0.5, 0.9, 0.75, 0.02, format="%.2f")
        alpha_b = render_sync_input("黑雛菊反照率 α_b", "alpha_b_1dwg", 0.1, 0.4, 0.25, 0.02, format="%.2f")
        alpha_g = render_sync_input("灰雛菊反照率 α_g (中性)", "alpha_g_1dwg", 0.3, 0.7, 0.50, 0.02, format="%.2f")
        alpha_u = render_sync_input("裸地反照率 α_u", "alpha_u_1dwg", 0.3, 0.7, 0.50, 0.02, format="%.2f")
        q_val = render_sync_input("微氣候係數 q (℃)", "q_val_1dwg", 5.0, 40.0, 20.0, 1.0, format="%.1f")
        gamma_val = render_sync_input("死亡率 γ", "gamma_val_1dwg", 0.05, 0.6, 0.30, 0.02, format="%.2f")
        ag_init = render_sync_input("灰雛菊初始覆蓋率", "ag_init_1dwg", 0.001, 0.2, 0.01, 0.005, format="%.3f")
        a_param = render_sync_input("OLR 截距 A (W/m²)", "a_param_1dwg", 150.0, 300.0, 230.0, 5.0, format="%.1f")
        b_param = render_sync_input("OLR 斜率 B (W/m²/℃)", "b_param_1dwg", 1.0, 4.0, 2.17, 0.05, format="%.2f")
        itera = render_sync_input("迭代步數", "itera_1dwg", 30, 300, 150, 10, is_int=True)

    st.markdown("""
    ---
    **三物種空間棲位機制**
    - **黑雛菊 ($a_b$)**：低反照率 (0.25)，吸收微弱太陽輻射，在寒冷的高緯極區具優勢。
    - **白雛菊 ($a_w$)**：高反照率 (0.75)，反射過剩陽光，在炎熱的低緯赤道具優勢。
    - **灰雛菊 ($a_g$)**：中性反照率 (0.50)，在溫度適中的中緯度溫帶地區具競爭力。
    """)

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

    render_engine = st.radio(
        "圖表渲染模式",
        ["⚡ 動態演變畫布", "📊 標準 Plotly 向量圖表"],
        horizontal=True,
        key="daisygrey1d_engine_choice"
    )

    if "動態演變" in render_engine:
        components.html(
            get_interactive_daisy_grey_1d_html(
                s0=s0, l_val=l_val, alpha_w=alpha_w, alpha_b=alpha_b, alpha_g=alpha_g, alpha_u=alpha_u,
                q_val=q_val, gamma_val=gamma_val, k_diff=k_diff, a_param=a_param, b_param=b_param, itera=itera
            ),
            height=890,
            scrolling=True
        )
    else:
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
            "緯度 (度)", "覆蓋率 (0~1)", height=500,
            x_range=[-90, 90], y_range=[0.0, 1.0]
        ))
        render_plotly_chart(fig_3sp, key="dw1d_grey_3sp_chart")

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
        "緯度 (度)", "溫度 (℃)", height=500,
        x_range=[-90, 90], y_range=[-40.0, 45.0]
    ))
    render_plotly_chart(fig_t_g, key="dw1d_grey_t_g_chart")

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
        f_s.update_layout(get_plotly_layout(f"步數 {selected_idx} 物種分佈", "緯度 (度)", "覆蓋率", x_range=[-90, 90], y_range=[0.0, 1.0]))
        render_plotly_chart(f_s, key="dw1d_grey_f_s_chart")

    with s_c2:
        f_t = go.Figure()
        f_t.add_trace(go.Scatter(x=lats_grey_1d, y=step_data["temp"], mode="lines+markers", name="溫度", line=dict(color="#f59e0b", width=3)))
        f_t.update_layout(get_plotly_layout(f"步數 {selected_idx} 溫度剖面 (均溫: {step_data['mean_t']:.2f}℃)", "緯度 (度)", "溫度 (℃)", x_range=[-90, 90], y_range=[-40.0, 45.0]))
        render_plotly_chart(f_t, key="dw1d_grey_f_t_chart")

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



