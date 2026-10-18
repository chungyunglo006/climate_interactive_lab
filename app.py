"""
Climate & Ecological Models Interactive Laboratory
Main Entry Point and Dashboard Hub.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.ui import apply_custom_styles, render_hero, render_stat_card, get_plotly_layout

st.set_page_config(
    page_title="氣候與生態互動實驗室 | Climate Sim Lab",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()

render_hero(
    title="氣候與生態模擬互動實驗室 (Climate & Eco Sim Lab)",
    subtitle="基於能量平衡模型 (EBM) 與雛菊世界 (Daisyworld) 理論，提供多個可獨立調整參數、實時模擬與動態視覺化的科學實驗網站。",
    badges=["Python 3.11", "uv Project", "0D / 1D / 2D Models", "Interactive Web Apps", "Plotly Visuals"]
)

# Sidebar navigation & overview
st.sidebar.title("🎛️ 實驗總覽導覽")
st.sidebar.markdown("""
歡迎來到氣候與生態模擬實驗室！左側側邊欄可直接點擊進入各個**獨立互動實驗網站**：
- **1. 0D 能量平衡模型**
- **2. 1D 緯度能量平衡模型**
- **3. 0D 經典雛菊世界**
- **4. 0D 灰雛菊世界**
- **5. 1D 緯度經典雛菊世界**
- **6. 1D 緯度灰雛菊世界**
- **7. 2D 氣候與雛菊世界模型**
- **8. 動畫與圖表匯出工坊**
""")

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_stat_card("實驗模組總數", "7 大核心模型", "涵蓋 0D / 1D / 2D")
with col2:
    render_stat_card("物理機制", "冰雪反照率反饋", "S-Curve 遲滯迴線")
with col3:
    render_stat_card("生態假說", "蓋亞雛菊恆溫調節", "自然選擇 vs 氣候回饋")
with col4:
    render_stat_card("空間維度", "108 網格全球海陸", "東西與南北熱擴散傳遞")

st.markdown("---")

# Quick Navigation Grid
st.subheader("🚀 快速進入獨立實驗網站")

exp_cols = st.columns(2)

with exp_cols[0]:
    with st.container():
        st.markdown("""
        ### 🌍 [0D 能量平衡模型 (0D EBM)](1_🌍_0D_能量平衡模型)
        - **核心原理**：零維全球平均能量收支方程式 $C \\frac{dT}{dt} = \\frac{S_0}{4}(1-\\alpha(T)) - \\epsilon\\sigma T^4$。
        - **探索主題**：
          1. 溫暖起點 vs 寒冷起點的時間演化收斂。
          2. 三種全球平衡態求根（溫暖地球、不穩定過渡態、雪球地球）。
          3. 氣候分歧圖（S-curve Bifurcation）與氣候崩潰遲滯迴線（Hysteresis）。
          4. 太陽輻射遞減下的失控冰期崩潰動態模擬。
        """)

    with st.container():
        st.markdown("""
        ### 🌼 [0D 經典雙物種雛菊世界 (Daisyworld)](3_🌼_0D_經典雛菊世界)
        - **核心原理**：黑雛菊（吸熱降反照率）與白雛菊（散熱升反照率）的物種競爭。
        - **探索主題**：
          1. 蓋亞假說（Gaia Hypothesis）：無意識生命活動如何維持行星宜居性。
          2. 太陽光度 $L$ 掃描（0.6 ~ 1.6）：雛菊恆溫平台 vs 無生物死星對比。
          3. 局地微氣候溫差 $q(\\alpha_p - \\alpha_i)$ 與最適生長溫控曲線 $\\beta(T)$。
        """)

    with st.container():
        st.markdown("""
        ### 🌸 [1D 緯度經典雛菊世界 (1D Daisyworld)](5_🌸_1D_緯度經典雛菊世界)
        - **核心原理**：9 個緯度帶太陽輻射加權分佈 + 緯度間大氣熱擴散 + 局部雛菊生長。
        - **探索主題**：
          1. **生態位分化 (Niche Differentiation)**：赤道高溫區白雛菊散熱 vs 極區低溫區黑雛菊保溫。
          2. 各緯度溫度調控結果 vs 無生物基準剖面。
          3. 動態演化步驟播放器。
        """)

with exp_cols[1]:
    with st.container():
        st.markdown("""
        ### 🌐 [1D 緯度能量平衡模型 (1D Budyko-Sellers EBM)](2_🌐_1D_緯度能量平衡模型)
        - **核心原理**：引入 9 個緯度帶日射權重、Budyko 長波出射輻射 $A+BT$ 與大氣經向熱傳遞 $F_i = K(T_i - \\bar{T})$。
        - **探索主題**：
          1. 冰雪覆蓋臨界線（Ice Edge）與赤道/極區熱量輸送平衡。
          2. 動態迭代演化步歷史視覺化。
          3. 太陽強度因子 $Frac\\_SC$ 與熱擴散係數 $K$ 敏感度掃描。
        """)

    with st.container():
        st.markdown("""
        ### ⚪ [0D 灰雛菊世界 (Daisyworld with Grey Daisies)](4_⚪_0D_灰雛菊世界)
        - **核心原理**：引入反照率等於裸地的中性物種——灰雛菊（$\\alpha_g = 0.50$）。
        - **探索主題**：
          1. 檢驗中性物種在自然選擇下的演化優勢與生存空間。
          2. 灰雛菊如何與黑白雛菊競爭有限裸地，並對全球氣候調節造成何種干擾。
        """)

    with st.container():
        st.markdown("""
        ### 🌿 [1D 緯度灰雛菊世界 (1D Grey Daisyworld)](6_🌿_1D_緯度灰雛菊世界)
        - **核心原理**：將三物種競爭架構延伸至空間維度。
        - **探索主題**：
          1. 探討黑、白、灰雛菊在不同緯度的競爭排擠與共存態。
          2. 空間維度下反照率中性物種對緯度溫度梯度的影響。
        """)

st.markdown("""
### 🗺️ [2D 氣候與雛菊世界模型 (2D Models on 9x12 Grid)](7_🗺️_2D_氣候與雛菊世界模型)
- **核心原理**：9 緯度 $\\times$ 12 經度全球網格（108 格點），結合**真實大陸海陸分佈遮罩**、陸地/海洋熱容量對比、經向與緯向雙向熱擴散。
- **包含模型**：
  1. **2D EBM**：海陸比熱差異（海洋熱緩衝 vs 大陸劇烈溫差）與冰雪邊緣。
  2. **2D 經典雛菊世界**：雛菊僅在陸地生長，海洋提供恆定反照率與熱擴散。
  3. **2D 灰雛菊世界**：陸地三物種空間動態競爭與全球溫度熱圖。
""")

st.markdown("---")

# Quick Interactive Sandbox Preview: Comparing 0D Models
st.subheader("🧪 快速互動預覽：零維模型對照沙盒 (Live Sandbox)")

preview_col1, preview_col2 = st.columns([1, 2])

with preview_col1:
    st.markdown("**參數微調**")
    p_s0 = st.slider("太陽常數 $S_0$ (W/m²)", min_value=800.0, max_value=1600.0, value=1368.0, step=10.0)
    p_ice_albedo = st.slider("冰雪反照率 $\\alpha_{ice}$", min_value=0.4, max_value=0.8, value=0.6, step=0.05)
    p_land_albedo = st.slider("陸地反照率 $\\alpha_{land}$", min_value=0.1, max_value=0.5, value=0.3, step=0.05)

    from models.ebm_0d import run_ebm
    df_w = run_ebm(S0=p_s0, alpha_ice=p_ice_albedo, alpha_land=p_land_albedo, T_init=290.0)
    df_c = run_ebm(S0=p_s0, alpha_ice=p_ice_albedo, alpha_land=p_land_albedo, T_init=230.0)

    final_tw = df_w["溫度 (℃)"].iloc[-1]
    final_tc = df_c["溫度 (℃)"].iloc[-1]

    st.metric("暖起點 (290K) 平衡溫度", f"{final_tw:.2f} ℃")
    st.metric("冷起點 (230K) 平衡溫度", f"{final_tc:.2f} ℃")

with preview_col2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_w["時間 (年)"], y=df_w["溫度 (℃)"],
        mode="lines", name="暖起點 (290 K) 演化軌跡",
        line=dict(color="#ef4444", width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=df_c["時間 (年)"], y=df_c["溫度 (℃)"],
        mode="lines", name="冷起點 (230 K) 演化軌跡",
        line=dict(color="#38bdf8", width=2.5)
    ))
    fig.update_layout(get_plotly_layout(
        title=f"0D EBM 溫度收斂對照 ($S_0 = {p_s0}$ W/m²)",
        xaxis_title="時間 (年)",
        yaxis_title="全球平均溫度 (℃)",
        height=380
    ))
    st.plotly_chart(fig, use_container_width=True)

st.info("💡 提示：點擊左側側邊欄的選單，進入各個具備完整進階分析功能的獨立實驗網站！")
