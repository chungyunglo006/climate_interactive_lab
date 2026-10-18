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
    render_plotly_chart
)
from models.daisy_1d import run_daisyworld_1d
import streamlit.components.v1 as components
from utils.interactive_daisy_1d import get_interactive_daisy1d_html

st.set_page_config(
    page_title="1D 緯度經典雛菊世界 | 獨立實驗網站",
    page_icon="🌸",
    layout="wide"
)

apply_custom_styles()

render_hero(
    title="一維緯度經典雛菊世界 (1D Latitudinal Daisyworld)",
    subtitle="將雛菊世界延伸至空間維度：探索「赤道散熱白雛菊」與「極區吸熱黑雛菊」的空間生態位分化 (Niche Differentiation) 與緯度氣候調節。",
    badges=["1D Daisyworld", "Spatial Niche Differentiation", "Latitudinal Heat Transport", "Planetary Zonation", "60 FPS Canvas"]
)

# Sidebar: Model Guide & Key Concepts (Unified single control panel is inside the interactive canvas)
with st.sidebar:
    st.header("🌸 1D 緯度雛菊實驗室")
    st.markdown("""
    **實驗特色**
    - ⚡ **60 FPS 前端絲滑畫布**：坐標軸固化，曲線零重劃、零閃爍。
    - 🎛️ **雙向同步面板**：滑桿平滑拖曳 + 精確數值鍵盤直接輸入。
    - 🎬 **連續動態掃描**：內建 60 FPS 硬體加速平滑推移動畫。
    
    ---
    **空間生態位分化機制**
    - **赤道低緯區**：接受強烈日射，白雛菊大面積繁茂，藉由高反照率反射陽光，防止熱帶過熱。
    - **極地高緯區**：接受傾斜微弱日射，黑雛菊繁茂生長，藉由低反照率吸收稀少熱量，減輕極區嚴寒。
    - **大氣擴散傳輸 ($K$)**：透過經向熱輸送將赤道多餘熱量平流輸送至兩極，與生物反饋共同均溫全球。
    
    ---
    **參考基準**
    - 太陽常數 $S_0$：$2100$ W/m²
    - 大氣擴散係數 $K$：$3.87$ W/m²/℃
    - 最適生長溫度：$22.5$ ℃
    """)

# Default parameters
s0 = 2100.0
l_val = 1.0
k_diff = 3.87
alpha_w = 0.75
alpha_b = 0.25
alpha_u = 0.50
q_val = 20.0
gamma_val = 0.30
a_param = 230.0
b_param = 2.17
itera = 150

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

    render_engine = st.radio(
        "圖表渲染模式",
        ["⚡ 60 FPS 絲滑高幀率畫布 (坐標軸固化，曲線零重劃、零閃爍)", "📊 標準 Plotly 向量圖表模式"],
        horizontal=True,
        key="daisy1d_engine_choice"
    )

    if "60 FPS" in render_engine:
        components.html(
            get_interactive_daisy1d_html(
                s0=s0, l_val=l_val, alpha_w=alpha_w, alpha_b=alpha_b, alpha_u=alpha_u,
                q_val=q_val, gamma_val=gamma_val, k_diff=k_diff, a_param=a_param, b_param=b_param, itera=itera
            ),
            height=820,
            scrolling=False
        )
    else:
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
            "緯度 (度)", "覆蓋率 (0~1)", height=500,
            x_range=[-90, 90], y_range=[0.0, 1.0]
        ))
        render_plotly_chart(fig_zonation, key="dw1d_zonation_chart")

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
        "緯度 (度)", "溫度 (℃)", height=500,
        x_range=[-90, 90], y_range=[-40.0, 45.0]
    ))
    render_plotly_chart(fig_t_comp, key="dw1d_t_comp_chart")

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
        fig_s_cov.update_layout(get_plotly_layout(f"步數 {selected_idx} 各緯度覆蓋率", "緯度 (度)", "覆蓋率", x_range=[-90, 90], y_range=[0.0, 1.0]))
        render_plotly_chart(fig_s_cov, key="dw1d_s_cov_chart")

    with step_c2:
        fig_s_t = go.Figure()
        fig_s_t.add_trace(go.Scatter(x=lats_1d, y=step_data["temp"], mode="lines+markers", name="地表溫度", line=dict(color="#f59e0b", width=3)))
        fig_s_t.update_layout(get_plotly_layout(f"步數 {selected_idx} 溫度剖面 (均溫: {step_data['mean_t']:.2f}℃)", "緯度 (度)", "溫度 (℃)", x_range=[-90, 90], y_range=[-40.0, 45.0]))
        render_plotly_chart(fig_s_t, key="dw1d_s_t_chart")

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



