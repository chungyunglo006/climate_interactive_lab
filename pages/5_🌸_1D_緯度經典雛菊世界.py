"""
Page 5: 1D Latitudinal Classic Daisyworld Interactive Experiment Site.
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
    render_dynamic_controller
)
from models.daisy_1d import run_daisyworld_1d

st.set_page_config(
    page_title="1D 緯度經典雛菊世界 | 獨立實驗網站",
    page_icon="🌸",
    layout="wide"
)

apply_custom_styles()

render_hero(
    title="一維緯度經典雛菊世界 (1D Latitudinal Daisyworld)",
    subtitle="將雛菊世界延伸至空間維度：探索「赤道散熱白雛菊」與「極區吸熱黑雛菊」的空間生態位分化 (Niche Differentiation) 與緯度氣候調節。",
    badges=["1D Daisyworld", "Spatial Niche Differentiation", "Latitudinal Heat Transport", "Planetary Zonation"]
)

# Sidebar Parameters
st.sidebar.header("⚙️ 1D 雛菊空間參數")

if "daisy1d_preset" not in st.session_state:
with st.sidebar:
    st.header("⚙️ 1D 雛菊生態參數")

    if "daisy1d_preset" not in st.session_state:
        st.session_state["daisy1d_preset"] = "標準緯度分化 (S0=2100, L=1.0, K=3.87)"

    preset = st.selectbox(
        "🎯 預設情境 (Scenario Presets)",
        ["自訂參數 (Custom)", "標準緯度分化 (S0=2100, L=1.0, K=3.87)", "低日照極區保溫主導 (S0=1800)", "高日照赤道降溫主導 (S0=2400)", "弱大氣擴散局部孤立 (K=1.5)"],
        index=1
    )

    if preset != st.session_state["daisy1d_preset"] and preset != "自訂參數 (Custom)":
        st.session_state["daisy1d_preset"] = preset
        if preset == "標準緯度分化 (S0=2100, L=1.0, K=3.87)":
            set_param_value("s0_1dw", 2100.0)
            set_param_value("l_val_1dw", 1.0)
            set_param_value("k_diff_1dw", 3.87)
        elif preset == "低日照極區保溫主導 (S0=1800)":
            set_param_value("s0_1dw", 1800.0)
            set_param_value("l_val_1dw", 1.0)
            set_param_value("k_diff_1dw", 3.87)
        elif preset == "高日照赤道降溫主導 (S0=2400)":
            set_param_value("s0_1dw", 2400.0)
            set_param_value("l_val_1dw", 1.0)
            set_param_value("k_diff_1dw", 3.87)
        elif preset == "弱大氣擴散局部孤立 (K=1.5)":
            set_param_value("s0_1dw", 2100.0)
            set_param_value("l_val_1dw", 1.0)
            set_param_value("k_diff_1dw", 1.5)

    s0 = render_sync_input("太陽常數 S₀ (W/m²)", "s0_1dw", 1400.0, 2800.0, 2100.0, 50.0, format="%.1f")
    l_val = render_sync_input("太陽光度因子 L", "l_val_1dw", 0.6, 1.6, 1.0, 0.02, format="%.2f")
    k_diff = render_sync_input("大氣熱擴散傳遞 K (W/m²/℃)", "k_diff_1dw", 0.5, 9.0, 3.87, 0.1, format="%.2f")

    with st.expander("🔬 生態與 Budyko 參數 (滑桿 + 精確數值)", expanded=False):
        alpha_w = render_sync_input("白雛菊反照率 α_w", "alpha_w_1dw", 0.5, 0.9, 0.75, 0.02, format="%.2f")
        alpha_b = render_sync_input("黑雛菊反照率 α_b", "alpha_b_1dw", 0.1, 0.4, 0.25, 0.02, format="%.2f")
        alpha_u = render_sync_input("裸地反照率 α_u", "alpha_u_1dw", 0.3, 0.7, 0.50, 0.02, format="%.2f")
        q_val = render_sync_input("局地微氣候反饋 q (℃)", "q_val_1dw", 5.0, 40.0, 20.0, 1.0, format="%.1f")
        gamma_val = render_sync_input("死亡率 γ", "gamma_val_1dw", 0.05, 0.6, 0.3, 0.02, format="%.2f")
        a_param = render_sync_input("Budyko A", "a_param_1dw", 180.0, 260.0, 230.0, 5.0, format="%.1f")
        b_param = render_sync_input("Budyko B", "b_param_1dw", 1.5, 3.5, 2.17, 0.05, format="%.2f")
        itera = render_sync_input("總迭代步數", "itera_1dw", 30, 300, 150, 25, is_int=True)

    # Dynamic Sweeper Controller
    param_specs_1dw = {
        "太陽常數 S₀": {"key": "s0_1dw", "min": 1400.0, "max": 2800.0, "step": 50.0, "unit": "W/m²"},
        "太陽光度 L": {"key": "l_val_1dw", "min": 0.6, "max": 1.6, "step": 0.02, "unit": ""},
        "大氣擴散係數 K": {"key": "k_diff_1dw", "min": 0.5, "max": 9.0, "step": 0.2, "unit": "W/m²/℃"},
        "微氣候反饋 q": {"key": "q_val_1dw", "min": 5.0, "max": 40.0, "step": 1.0, "unit": "℃"}
    }
    render_dynamic_controller(param_specs_1dw, page_prefix="daisy1d")

with st.expander("📐 點擊展開：1D 雛菊世界生態與氣候耦合數學架構"):
    st.markdown(r"""
    ### 數學模型
    在每個緯度帶 $j \in \{85^\circ, 75^\circ, \dots, 6^\circ\}$：
    1. **局部行星反照率**：
       $$\alpha_{p,j} = a_{w,j} \alpha_w + a_{b,j} \alpha_b + (1 - a_{w,j} - a_{b,j}) \alpha_u$$
    2. **局部緯度大氣熱平衡**（包含經向熱擴散）：
       $$R_{\text{in},j}(1 - \alpha_{p,j}) + K \bar{T} - A = (B + K) T_j$$
    3. **局部物種微氣候溫度**：
       $$T_{w,j} = T_j + q(\alpha_{p,j} - \alpha_w), \quad T_{b,j} = T_j + q(\alpha_{p,j} - \alpha_b)$$
    4. **空間動態**：各緯度獨立進行生物族群消長，並透過大氣擴散項 $K(T_j - \bar{T})$ 與全體緯度產生全局熱交互作用。
    """)

tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ 1. 平衡地理覆蓋率分佈 (Niche Zonation)",
    "🌡️ 2. 緯度氣候調節 vs 無生物死星 (Temperature Regulation)",
    "🎬 3. 空間演化動態步進播放器 (Dynamic Step Playback)",
    "📋 4. 緯度詳細診斷表 (Data Matrix)"
])

# Run 1D Daisyworld Simulation
history_1d, lats_1d, temp_nobio = run_daisyworld_1d(
    S0=s0, L=l_val, alpha_w=alpha_w, alpha_b=alpha_b, alpha_u=alpha_u,
    q=q_val, gamma=gamma_val, A=a_param, B=b_param, K=k_diff, itera=itera
)

final_step = history_1d[-1]

# Tab 1: Geographic Niche Zonation
with tab1:
    st.subheader("1D 經典雛菊世界：空間生態位分化 (Niche Differentiation)")
    st.markdown("""
    - **高緯度極區（冷）**：黑雛菊覆蓋率顯著攀升，吸收更多日射防止極區冰封。
    - **低緯度赤道（熱）**：白雛菊覆蓋率大量增加，反射過強日照，防止熱帶過熱。
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_stat_card("全球加權均溫", f"{final_step['mean_t']:.2f} ℃")
    with col2:
        render_stat_card("赤道 (6°N) 白雛菊覆蓋率", f"{final_step['aw'][-1]*100:.1f} %")
    with col3:
        render_stat_card("極區 (85°N) 黑雛菊覆蓋率", f"{final_step['ab'][0]*100:.1f} %")
    with col4:
        render_stat_card("全域平均反照率", f"{np.mean(final_step['alpha_p']):.3f}")

    fig_zonation = go.Figure()
    fig_zonation.add_trace(go.Scatter(
        x=lats_1d, y=final_step["ab"],
        mode="lines+markers", marker=dict(size=8, color="#475569"),
        line=dict(color="#475569", width=3), name="黑雛菊覆蓋率 (極區優勢保溫)"
    ))
    fig_zonation.add_trace(go.Scatter(
        x=lats_1d, y=final_step["aw"],
        mode="lines+markers", marker=dict(size=8, color="#f8fafc"),
        line=dict(color="#f8fafc", width=3), name="白雛菊覆蓋率 (赤道優勢降溫)"
    ))
    fig_zonation.add_trace(go.Scatter(
        x=lats_1d, y=final_step["au"],
        mode="lines+markers", marker=dict(size=7, color="#d97706"),
        line=dict(color="#d97706", width=2, dash="dash"), name="裸地覆蓋率"
    ))
    fig_zonation.update_layout(get_plotly_layout(
        "各緯度最終平衡覆蓋率分佈 (極區黑雛菊 vs 赤道白雛菊)",
        "緯度 (度)", "覆蓋率 (0~1)", height=500
    ))
    st.plotly_chart(fig_zonation, use_container_width=True)

# Tab 2: Temperature Regulation
with tab2:
    st.subheader("緯度溫度調控結果 vs 無生物死星對比")
    st.markdown("比較「有雛菊調節的地球」與「完全由裸地組成的無生命星球」在各緯度的溫度差異。")

    mean_t_bio = final_step["mean_t"]
    lat_cos_list = [np.cos(np.radians(lat)) for lat in lats_1d]
    mean_t_dead = float(np.sum(temp_nobio * lat_cos_list) / np.sum(lat_cos_list))

    m_c1, m_c2 = st.columns(2)
    with m_c1:
        render_stat_card("雛菊調節全球均溫", f"{mean_t_bio:.2f} ℃")
    with m_c2:
        render_stat_card("無生物死星全球均溫", f"{mean_t_dead:.2f} ℃", f"溫差: {mean_t_bio - mean_t_dead:+.2f} ℃")

    fig_t_comp = go.Figure()
    fig_t_comp.add_trace(go.Scatter(
        x=lats_1d, y=final_step["temp"],
        mode="lines+markers", marker=dict(size=9, color="#22c55e"),
        line=dict(color="#22c55e", width=3.5), name="雛菊調控緯度溫度剖面"
    ))
    fig_t_comp.add_trace(go.Scatter(
        x=lats_1d, y=temp_nobio,
        mode="lines+markers", marker=dict(size=8, color="#ef4444"),
        line=dict(color="#ef4444", width=2.5, dash="dash"), name="無生命行星溫度剖面 (Bare Earth)"
    ))
    fig_t_comp.add_hline(y=22.5, line_dash="dot", line_color="#00e5ff", annotation_text="最適生長溫度 (22.5℃)")
    fig_t_comp.update_layout(get_plotly_layout(
        "各緯度溫度剖面對比 (生態調控 vs 死星基線)",
        "緯度 (度)", "溫度 (℃)", height=500
    ))
    st.plotly_chart(fig_t_comp, use_container_width=True)

# Tab 3: Dynamic Step Playback
with tab3:
    st.subheader("空間動態演化時間步步進播放器")
    selected_idx = st.slider("時間步 (Step)", 0, len(history_1d) - 1, 0, 1)
    step_data = history_1d[selected_idx]

    step_c1, step_c2 = st.columns(2)
    with step_c1:
        fig_s_cov = go.Figure()
        fig_s_cov.add_trace(go.Scatter(x=lats_1d, y=step_data["ab"], mode="lines+markers", name="黑雛菊", line=dict(color="#475569", width=2.5)))
        fig_s_cov.add_trace(go.Scatter(x=lats_1d, y=step_data["aw"], mode="lines+markers", name="白雛菊", line=dict(color="#f8fafc", width=2.5)))
        fig_s_cov.add_trace(go.Scatter(x=lats_1d, y=step_data["au"], mode="lines+markers", name="裸地", line=dict(color="#d97706", width=2, dash="dash")))
        fig_s_cov.update_layout(get_plotly_layout(f"步數 {selected_idx} 各緯度覆蓋率", "緯度 (度)", "覆蓋率"))
        st.plotly_chart(fig_s_cov, use_container_width=True)

    with step_c2:
        fig_s_t = go.Figure()
        fig_s_t.add_trace(go.Scatter(x=lats_1d, y=step_data["temp"], mode="lines+markers", name="地表溫度", line=dict(color="#f59e0b", width=3)))
        fig_s_t.update_layout(get_plotly_layout(f"步數 {selected_idx} 溫度剖面 (均溫: {step_data['mean_t']:.2f}℃)", "緯度 (度)", "溫度 (℃)"))
        st.plotly_chart(fig_s_t, use_container_width=True)

# Tab 4: Data Matrix
with tab4:
    st.subheader("平衡狀態各緯度數據診斷矩陣")
    df_matrix = pd.DataFrame({
        "緯度 (度)": lats_1d,
        "最終溫度 (℃)": final_step["temp"],
        "無生物溫度 (℃)": temp_nobio,
        "調控溫差 (℃)": final_step["temp"] - temp_nobio,
        "白雛菊覆蓋率": final_step["aw"],
        "黑雛菊覆蓋率": final_step["ab"],
        "裸地覆蓋率": final_step["au"],
        "行星反照率": final_step["alpha_p"]
    })

    st.dataframe(df_matrix.style.format({
        "最終溫度 (℃)": "{:.2f}",
        "無生物溫度 (℃)": "{:.2f}",
        "調控溫差 (℃)": "{:+.2f}",
        "白雛菊覆蓋率": "{:.4f}",
        "黑雛菊覆蓋率": "{:.4f}",
        "裸地覆蓋率": "{:.4f}",
        "行星反照率": "{:.4f}"
    }), use_container_width=True)

    csv_1d_dw = df_matrix.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 下載 1D 雛菊世界數據 (CSV)",
        data=csv_1d_dw,
        file_name=f"daisyworld1d_S0_{s0}_L_{l_val}_K_{k_diff}.csv",
        mime="text/csv"
    )
