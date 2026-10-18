"""
Page 7: 2D Climate & Daisyworld Models Interactive Experiment Site (9 Latitudes x 12 Longitudes).
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.ui import apply_custom_styles, render_hero, render_stat_card, get_plotly_layout
from models.models_2d import (
    LAT_LIST_2D,
    LON_LIST_2D,
    SUNWT_LIST_2D,
    LAND_MASK_2D,
    run_ebm_2d,
    run_daisyworld_2d,
    run_daisyworld_grey_2d
)

st.set_page_config(
    page_title="2D 氣候與雛菊世界模型 | 獨立實驗網站",
    page_icon="🗺️",
    layout="wide"
)

apply_custom_styles()

render_hero(
    title="二維氣候與雛菊世界模型 (2D Climate & Daisyworld Models)",
    subtitle="9 緯度帶 × 12 經度格點（共 108 網格），結合全球海陸遮罩、陸地/海洋熱容量差異、經向/緯向二維擴散傳遞。",
    badges=["2D EBM", "2D Daisyworld", "Continent-Ocean Contrast", "Heat Transport", "Global Grid Heatmaps"]
)

# Sidebar
st.sidebar.header("⚙️ 2D 模型架構選擇")

model_choice = st.sidebar.radio(
    "選擇 2D 模型類型",
    ["2D 能量平衡模型 (2D EBM)", "2D 經典雙物種雛菊世界 (2D Classic DW)", "2D 灰雛菊世界 (2D Grey DW)"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("物理與模擬參數")

if model_choice == "2D 能量平衡模型 (2D EBM)":
    sc_2d = st.sidebar.slider("太陽常數 $SC$ (W/m²)", 1000.0, 1600.0, 1370.0, 10.0)
    frac_sc_2d = st.sidebar.slider("太陽強度因子 $Frac\\_SC$", 0.7, 1.3, 1.0, 0.05)
    k_lat_2d = st.sidebar.slider("緯向（南北）擴散 $K_{lat}$", 1.0, 6.0, 3.87, 0.1)
    k_lon_2d = st.sidebar.slider("經向（東西）擴散 $K_{lon}$", 0.5, 4.0, 1.5, 0.1)
    itera_2d = st.sidebar.slider("迭代步數", 50, 400, 200, 25)
else:
    s0_2d = st.sidebar.slider("太陽常數 $S_0$ (W/m²)", 1400.0, 2500.0, 2100.0, 50.0)
    l_2d = st.sidebar.slider("太陽光度因子 $L$", 0.7, 1.4, 1.0, 0.05)
    k_lat_2d = st.sidebar.slider("緯向（南北）擴散 $K_{lat}$", 1.0, 6.0, 3.87, 0.1)
    k_lon_2d = st.sidebar.slider("經向（東西）擴散 $K_{lon}$", 0.5, 4.0, 1.5, 0.1)
    itera_2d = st.sidebar.slider("迭代步數", 50, 300, 150, 25)

with st.expander("📐 點擊展開：2D 網格架構與海陸遮罩原理"):
    st.markdown(r"""
    ### 2D 網格物理架構
    - **空間解析度**：
      - 緯度（9 帶）：$85^\circ, 75^\circ, 65^\circ, 55^\circ, 45^\circ, 35^\circ, 25^\circ, 15^\circ, 6^\circ\text{N}$
      - 經度（12 格）：每 $30^\circ$ 一格（$0^\circ, 30^\circ, \dots, 330^\circ$）
    - **海陸對比**：
      - 陸地熱容量 $C_{\text{land}} = 5 \times 10^6 \text{ J/m}^2\text{K}$（升溫快、季節溫差劇烈）
      - 海洋熱容量 $C_{\text{ocean}} = 2.09 \times 10^8 \text{ J/m}^2\text{K}$（巨大熱緩衝，溫差穩定）
    - **熱傳導**：
      $$D_{\text{lat}} = K_{\text{lat}}(\bar{T}_{\text{global}} - T_{i,j}), \quad D_{\text{lon}} = K_{\text{lon}}(\bar{T}_{\text{zonal},i} - T_{i,j})$$
    - **雛菊規則**：雛菊只在陸地格點繁衍生長，海洋格點維持固定海洋反照率 $\alpha_{\text{ocean}} = 0.10$。
    """)

# Main Content based on model selection
if model_choice == "2D 能量平衡模型 (2D EBM)":
    st.subheader("2D 能量平衡模型 (2D EBM) 空間熱圖")

    with st.spinner("計算 2D EBM 數值場中..."):
        T_final, hist_ebm2d = run_ebm_2d(
            SC=sc_2d, Frac_SC=frac_sc_2d,
            K_lat=k_lat_2d, K_lon=k_lon_2d, itera=itera_2d
        )

    last_step = hist_ebm2d[-1]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_stat_card("全球平均溫度", f"{last_step['global_mean']:.2f} ℃")
    with col2:
        render_stat_card("地表最高溫度", f"{T_final.max():.2f} ℃")
    with col3:
        render_stat_card("地表最低溫度", f"{T_final.min():.2f} ℃")
    with col4:
        render_stat_card("陸地平均溫度", f"{T_final[LAND_MASK_2D == 1].mean():.2f} ℃", f"海洋均溫: {T_final[LAND_MASK_2D == 0].mean():.2f} ℃")

    # Time slider for animation
    sel_step = st.slider("時間演化步 (Iteration Step)", 0, len(hist_ebm2d) - 1, len(hist_ebm2d) - 1, 1)
    current_T = hist_ebm2d[sel_step]['T']
    current_alpha = hist_ebm2d[sel_step]['alpha']

    c_col1, c_col2 = st.columns(2)
    with c_col1:
        fig_t2d = go.Figure(data=go.Heatmap(
            z=current_T,
            x=[f"{int(lon)}°" for lon in LON_LIST_2D],
            y=[f"{int(lat)}°N" for lat in LAT_LIST_2D],
            colorscale="Viridis",
            zmin=-40, zmax=30,
            text=np.round(current_T, 1),
            texttemplate="%{text}",
            colorbar=dict(title="溫度 (℃)")
        ))
        fig_t2d.update_layout(get_plotly_layout(f"2D 地表溫度分佈 (步數: {hist_ebm2d[sel_step]['step']})", "經度", "緯度", height=450))
        st.plotly_chart(fig_t2d, use_container_width=True)

    with c_col2:
        fig_a2d = go.Figure(data=go.Heatmap(
            z=current_alpha,
            x=[f"{int(lon)}°" for lon in LON_LIST_2D],
            y=[f"{int(lat)}°N" for lat in LAT_LIST_2D],
            colorscale="Blues",
            zmin=0.1, zmax=0.65,
            text=np.round(current_alpha, 2),
            texttemplate="%{text}",
            colorbar=dict(title="反照率")
        ))
        fig_a2d.update_layout(get_plotly_layout(f"2D 反照率與冰雪覆蓋分佈 (步數: {hist_ebm2d[sel_step]['step']})", "經度", "緯度", height=450))
        st.plotly_chart(fig_a2d, use_container_width=True)

elif model_choice == "2D 經典雙物種雛菊世界 (2D Classic DW)":
    st.subheader("2D 經典雙物種雛菊世界 (陸地黑白雛菊空間分佈)")

    with st.spinner("計算 2D 雛菊生態動態中..."):
        aw_2d, ab_2d, T_eff_2d, hist_dw2d = run_daisyworld_2d(
            S0=s0_2d, L=l_2d, K_lat=k_lat_2d, K_lon=k_lon_2d, itera=itera_2d
        )

    last_step = hist_dw2d[-1]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_stat_card("全球平均溫度", f"{last_step['global_mean']:.2f} ℃")
    with col2:
        render_stat_card("陸地平均白雛菊覆蓋率", f"{aw_2d[LAND_MASK_2D == 1].mean()*100:.1f} %")
    with col3:
        render_stat_card("陸地平均黑雛菊覆蓋率", f"{ab_2d[LAND_MASK_2D == 1].mean()*100:.1f} %")
    with col4:
        render_stat_card("陸地平均溫度", f"{T_eff_2d[LAND_MASK_2D == 1].mean():.2f} ℃")

    sel_step = st.slider("時間演化步 (Iteration Step)", 0, len(hist_dw2d) - 1, len(hist_dw2d) - 1, 1)
    s_aw = hist_dw2d[sel_step]['aw']
    s_ab = hist_dw2d[sel_step]['ab']
    s_T = hist_dw2d[sel_step]['T']

    h_col1, h_col2, h_col3 = st.columns(3)
    with h_col1:
        fig_w = go.Figure(data=go.Heatmap(
            z=s_aw, x=[f"{int(lon)}°" for lon in LON_LIST_2D], y=[f"{int(lat)}°N" for lat in LAT_LIST_2D],
            colorscale="Purples", zmin=0, zmax=1.0,
            text=np.round(s_aw, 2), texttemplate="%{text}",
            colorbar=dict(title="覆蓋率")
        ))
        fig_w.update_layout(get_plotly_layout("白雛菊覆蓋率 (散熱降溫)", "經度", "緯度", height=380))
        st.plotly_chart(fig_w, use_container_width=True)

    with h_col2:
        fig_b = go.Figure(data=go.Heatmap(
            z=s_ab, x=[f"{int(lon)}°" for lon in LON_LIST_2D], y=[f"{int(lat)}°N" for lat in LAT_LIST_2D],
            colorscale="Greys_r", zmin=0, zmax=1.0,
            text=np.round(s_ab, 2), texttemplate="%{text}",
            colorbar=dict(title="覆蓋率")
        ))
        fig_b.update_layout(get_plotly_layout("黑雛菊覆蓋率 (吸熱保溫)", "經度", "緯度", height=380))
        st.plotly_chart(fig_b, use_container_width=True)

    with h_col3:
        fig_temp = go.Figure(data=go.Heatmap(
            z=s_T, x=[f"{int(lon)}°" for lon in LON_LIST_2D], y=[f"{int(lat)}°N" for lat in LAT_LIST_2D],
            colorscale="Thermal", zmin=-10, zmax=35,
            text=np.round(s_T, 1), texttemplate="%{text}",
            colorbar=dict(title="溫度 (℃)")
        ))
        fig_temp.update_layout(get_plotly_layout("2D 地表有效溫度分佈", "經度", "緯度", height=380))
        st.plotly_chart(fig_temp, use_container_width=True)

else:
    st.subheader("2D 灰雛菊世界 (陸地三物種空間競爭)")

    with st.spinner("計算 2D 三物種動態中..."):
        aw_2d, ab_2d, ag_2d, T_eff_2d, hist_g2d = run_daisyworld_grey_2d(
            S0=s0_2d, L=l_2d, K_lat=k_lat_2d, K_lon=k_lon_2d, itera=itera_2d
        )

    last_step = hist_g2d[-1]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_stat_card("全球平均溫度", f"{last_step['global_mean']:.2f} ℃")
    with col2:
        render_stat_card("白雛菊陸地均率", f"{aw_2d[LAND_MASK_2D == 1].mean()*100:.1f} %")
    with col3:
        render_stat_card("黑雛菊陸地均率", f"{ab_2d[LAND_MASK_2D == 1].mean()*100:.1f} %")
    with col4:
        render_stat_card("灰雛菊陸地均率", f"{ag_2d[LAND_MASK_2D == 1].mean()*100:.1f} %")

    sel_step = st.slider("時間演化步 (Iteration Step)", 0, len(hist_g2d) - 1, len(hist_g2d) - 1, 1)
    s_aw = hist_g2d[sel_step]['aw']
    s_ab = hist_g2d[sel_step]['ab']
    s_ag = hist_g2d[sel_step]['ag']
    s_T = hist_g2d[sel_step]['T']

    g_col1, g_col2 = st.columns(2)
    with g_col1:
        fig_ag = go.Figure(data=go.Heatmap(
            z=s_ag, x=[f"{int(lon)}°" for lon in LON_LIST_2D], y=[f"{int(lat)}°N" for lat in LAT_LIST_2D],
            colorscale="YlGn", zmin=0, zmax=1.0,
            text=np.round(s_ag, 2), texttemplate="%{text}",
            colorbar=dict(title="覆蓋率")
        ))
        fig_ag.update_layout(get_plotly_layout("灰雛菊陸地覆蓋率 (中性物種分佈)", "經度", "緯度", height=420))
        st.plotly_chart(fig_ag, use_container_width=True)

    with g_col2:
        fig_t_g = go.Figure(data=go.Heatmap(
            z=s_T, x=[f"{int(lon)}°" for lon in LON_LIST_2D], y=[f"{int(lat)}°N" for lat in LAT_LIST_2D],
            colorscale="Inferno", zmin=-10, zmax=35,
            text=np.round(s_T, 1), texttemplate="%{text}",
            colorbar=dict(title="溫度 (℃)")
        ))
        fig_t_g.update_layout(get_plotly_layout("三物種調控下 2D 地表有效溫度", "經度", "緯度", height=420))
        st.plotly_chart(fig_t_g, use_container_width=True)
