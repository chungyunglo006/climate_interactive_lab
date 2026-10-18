"""
Page 8: Animation and Scientific Media Export Studio.
Implements the notebook's Section 7 WebP/GIF export capability with live generation and downloads.
"""

import streamlit as st
import numpy as np
import io
import matplotlib.pyplot as plt
from PIL import Image
from utils.ui import apply_custom_styles, render_hero, render_stat_card
from models.ebm_1d import run_ebm_1d_history
from models.daisy_1d import run_daisyworld_1d, run_daisyworld_with_grey_1d

st.set_page_config(
    page_title="動畫與圖表匯出工坊 | 獨立實驗網站",
    page_icon="🎬",
    layout="wide"
)

apply_custom_styles()

render_hero(
    title="動態動畫與媒體匯出工坊 (Scientific Media Studio)",
    subtitle="重現 Notebook 第 7 節功能：將一維與二維氣候演化動態，自訂參數直接渲染並匯出為輕量化動態 WebP 或 GIF 圖檔，供學術簡報、論文或網頁展示使用。",
    badges=["Pillow Engine", "WebP / GIF Export", "No FFmpeg Required", "High Performance"]
)

st.subheader("🛠️ 動畫產生器設定")

model_type = st.selectbox(
    "選擇要匯出的實驗動畫模型",
    ["一維緯度能量平衡模型 (1D EBM)", "一維緯度經典雛菊世界 (1D Daisyworld)", "一維緯度灰雛菊世界 (1D Grey Daisyworld)"]
)

col1, col2, col3 = st.columns(3)
with col1:
    out_format = st.radio("輸出動畫格式", ["WebP (推薦：體積小、色彩真)", "GIF (相容性高)"], horizontal=True)
with col2:
    frame_duration = st.slider("每幀播放時間 (毫秒 ms)", 40, 200, 80, 10)
with col3:
    max_frames = st.slider("最大抽取影格數", 10, 50, 30, 5)

st.markdown("---")

generate_btn = st.button("✨ 立即渲染並生成動態圖檔", type="primary")

if generate_btn:
    frames = []
    status_bar = st.progress(0, text="正在進行數值運算與影格渲染...")

    if model_type == "一維緯度能量平衡模型 (1D EBM)":
        history, lats = run_ebm_1d_history(SC=1370.0, Frac_SC=1.0, itera=40)
        step_stride = max(1, len(history) // max_frames)
        sampled_history = history[::step_stride]

        for idx, h in enumerate(sampled_history):
            fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
            fig.patch.set_facecolor('#0f172a')
            ax.set_facecolor('#1e293b')

            ax.plot(lats, h["temp"], marker='o', color="#ef4444", linewidth=2.5, label="地表溫度")
            ax.axhline(y=-10.0, color="#38bdf8", linestyle="--", alpha=0.7, label="結冰臨界溫 (-10℃)")
            ax.set_title(f"1D EBM 溫度演變 - 迭代步 {h['step']} (均溫: {h['mean_t']:.2f} ℃)", color="white", fontsize=12, fontweight="bold")
            ax.set_xlabel("緯度 (度)", color="#cbd5e1")
            ax.set_ylabel("溫度 (℃)", color="#cbd5e1")
            ax.set_ylim(-35, 30)
            ax.tick_params(colors="#cbd5e1")
            ax.grid(True, linestyle="--", alpha=0.3, color="#64748b")
            ax.legend(facecolor="#1e293b", edgecolor="#475569", labelcolor="white")
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
            plt.close(fig)
            buf.seek(0)
            img = Image.open(buf)
            frames.append(img.copy())

            status_bar.progress((idx + 1) / len(sampled_history), text=f"渲染影格 {idx+1}/{len(sampled_history)}...")

    elif model_type == "一維緯度經典雛菊世界 (1D Daisyworld)":
        history, lats, _ = run_daisyworld_1d(S0=2100.0, L=1.0, itera=40)
        step_stride = max(1, len(history) // max_frames)
        sampled_history = history[::step_stride]

        for idx, h in enumerate(sampled_history):
            fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
            fig.patch.set_facecolor('#0f172a')
            ax.set_facecolor('#1e293b')

            ax.plot(lats, h["ab"], marker='o', color="#94a3b8", linewidth=2.5, label="黑雛菊 (保溫)")
            ax.plot(lats, h["aw"], marker='s', color="#ffffff", linewidth=2.5, label="白雛菊 (散熱)")
            ax.set_title(f"1D 雛菊覆蓋率演化 - 步數 {h['step']}", color="white", fontsize=12, fontweight="bold")
            ax.set_xlabel("緯度 (度)", color="#cbd5e1")
            ax.set_ylabel("覆蓋率 (0~1)", color="#cbd5e1")
            ax.set_ylim(0, 1.0)
            ax.tick_params(colors="#cbd5e1")
            ax.grid(True, linestyle="--", alpha=0.3, color="#64748b")
            ax.legend(facecolor="#1e293b", edgecolor="#475569", labelcolor="white")
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
            plt.close(fig)
            buf.seek(0)
            img = Image.open(buf)
            frames.append(img.copy())

            status_bar.progress((idx + 1) / len(sampled_history), text=f"渲染影格 {idx+1}/{len(sampled_history)}...")

    else:
        history, lats, _ = run_daisyworld_with_grey_1d(S0=2100.0, L=1.0, itera=40)
        step_stride = max(1, len(history) // max_frames)
        sampled_history = history[::step_stride]

        for idx, h in enumerate(sampled_history):
            fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
            fig.patch.set_facecolor('#0f172a')
            ax.set_facecolor('#1e293b')

            ax.plot(lats, h["ab"], marker='o', color="#64748b", linewidth=2.5, label="黑雛菊")
            ax.plot(lats, h["aw"], marker='s', color="#ffffff", linewidth=2.5, label="白雛菊")
            ax.plot(lats, h["ag"], marker='^', color="#38bdf8", linewidth=2.5, label="灰雛菊")
            ax.set_title(f"1D 灰雛菊世界演化 - 步數 {h['step']}", color="white", fontsize=12, fontweight="bold")
            ax.set_xlabel("緯度 (度)", color="#cbd5e1")
            ax.set_ylabel("覆蓋率 (0~1)", color="#cbd5e1")
            ax.set_ylim(0, 1.0)
            ax.tick_params(colors="#cbd5e1")
            ax.grid(True, linestyle="--", alpha=0.3, color="#64748b")
            ax.legend(facecolor="#1e293b", edgecolor="#475569", labelcolor="white")
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
            plt.close(fig)
            buf.seek(0)
            img = Image.open(buf)
            frames.append(img.copy())

            status_bar.progress((idx + 1) / len(sampled_history), text=f"渲染影格 {idx+1}/{len(sampled_history)}...")

    # Save animation buffer
    out_buf = io.BytesIO()
    if "WebP" in out_format:
        frames[0].save(
            out_buf, format="WEBP", save_all=True,
            append_images=frames[1:], duration=frame_duration, loop=0, quality=90
        )
        file_ext = "webp"
        mime_type = "image/webp"
    else:
        frames[0].save(
            out_buf, format="GIF", save_all=True,
            append_images=frames[1:], duration=frame_duration, loop=0
        )
        file_ext = "gif"
        mime_type = "image/gif"

    out_bytes = out_buf.getvalue()
    status_bar.empty()

    st.success(f"🎉 動畫渲染完成！共 {len(frames)} 幀，大小: {len(out_bytes)/1024:.1f} KB")

    preview_c1, preview_c2 = st.columns([2, 1])
    with preview_c1:
        st.image(out_bytes, caption=f"動態動畫即時預覽 ({file_ext.upper()})", use_container_width=True)

    with preview_c2:
        render_stat_card("檔案格式", file_ext.upper())
        render_stat_card("影格數量", f"{len(frames)} Frames")
        render_stat_card("檔案大小", f"{len(out_bytes)/1024:.1f} KB")

        st.download_button(
            f"📥 下載動態 {file_ext.upper()} 圖檔",
            data=out_bytes,
            file_name=f"simulation_animation_{model_type.split()[0]}.{file_ext}",
            mime=mime_type,
            type="primary"
        )
