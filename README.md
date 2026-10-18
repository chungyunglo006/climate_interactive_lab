# 氣候與生態模擬互動實驗室 (Climate & Ecological Interactive Simulation Lab)

本專案將氣候科學中的**能量平衡模型 (Energy Balance Model, EBM)** 與**雛菊世界 (Daisyworld)** 演化模型，重構為現代化、模組化且具備豐富互動界面的獨立實驗網站套件。

---

## 🌟 核心特色

1. **模組化物理計算核心 (`models/`)**：
   - 完全解耦純 Python / NumPy 科學計算邏輯，忠實重現並延伸 `climate_models copy 2.ipynb` 中的所有數學公式。
   - 包含 0D、1D（Budyko-Sellers 擴散）以及 2D（9 緯度 $\times$ 12 經度海陸網格）模型。
2. **多個獨立可調整的互動實驗網站 (`pages/`)**：
   - 每個實驗均可作為**獨立網站**啟動，亦可透過統一導覽門戶 (`app.py`) 自由切換。
   - 提供實時滑桿微調、情境預設按鈕 (Presets)、時間序列動態演化、相圖/分歧圖分析、各緯度空間剖面、2D 網格熱圖與動態播放器。
3. **媒體匯出工坊 (`pages/8`)**：
   - 免安裝外部 ffmpeg，使用純 Pillow 引擎即可將各一維/二維演化動態直接在網頁端渲染匯出為輕量化動態 WebP 或 GIF 圖檔，並支援 CSV 原始數據下載。
4. **現代化工程環境**：
   - 使用高效 Python 套件管理器 **`uv`**（Python 3.11 環境）與 **Git** 版本控制。

---

## 📁 目錄結構

```text
climate_interactive_lab/
├── .python-version               # 指定 Python 3.11.15
├── pyproject.toml                # uv 專案依賴管理設定
├── app.py                        # 實驗室綜合首頁大廳 (Main Portal)
├── main.py                       # CLI 啟動中樞 (支援獨立啟動各實驗或全站)
├── test_models.py                # 物理模型單元驗證測試
├── utils/
│   └── ui.py                     # 現代化 Dark Theme、CSS 樣式與統一 Plotly 佈局
├── models/                       # 核心科學計算模組
│   ├── __init__.py
│   ├── ebm_0d.py                 # 零維 EBM、三平衡態求根、S-curve 分歧圖、崩潰模擬
│   ├── ebm_1d.py                 # 一維 Budyko-Sellers EBM、收斂步進歷史、參數敏感度掃描
│   ├── daisy_0d.py               # 零維雙物種與灰雛菊世界、光度 L 恆溫調節相圖
│   ├── daisy_1d.py               # 一維緯度雛菊世界、極區/赤道生態位分化、死星基準對比
│   └── models_2d.py              # 二維 9x12 海陸格點 EBM、二維經典雛菊世界、二維灰雛菊世界
└── pages/                        # 8 大獨立互動實驗網站
    ├── 1_🌍_0D_能量平衡模型.py
    ├── 2_🌐_1D_緯度能量平衡模型.py
    ├── 3_🌼_0D_經典雛菊世界.py
    ├── 4_⚪_0D_灰雛菊世界.py
    ├── 5_🌸_1D_緯度經典雛菊世界.py
    ├── 6_🌿_1D_緯度灰雛菊世界.py
    ├── 7_🗺️_2D_氣候與雛菊世界模型.py
    └── 8_🎬_動畫與圖表匯出工坊.py
```

---

## 🚀 快速開始

### 1. 啟動綜合實驗室大廳 (所有實驗網站自由切換)

在專案目錄下執行：

```powershell
uv run python main.py
```

或直接使用 Streamlit：

```powershell
uv run streamlit run app.py
```

預設會在瀏覽器開啟 `http://localhost:8501`。

### 2. 獨立啟動特定實驗網站

本專案每個實驗皆為獨立完整網站，您可以透過 `main.py --page <編號>` 或直接執行該頁面檔案：

| 實驗編號 | 實驗網站名稱 | CLI 啟動指令 |
| :---: | :--- | :--- |
| **1** | 0D 能量平衡模型 (EBM) | `uv run python main.py --page 1` |
| **2** | 1D 緯度能量平衡模型 (Budyko-Sellers) | `uv run python main.py --page 2` |
| **3** | 0D 經典雙物種雛菊世界 (Daisyworld) | `uv run python main.py --page 3` |
| **4** | 0D 灰雛菊世界 (Grey Daisyworld) | `uv run python main.py --page 4` |
| **5** | 1D 緯度經典雛菊世界 (1D Daisyworld) | `uv run python main.py --page 5` |
| **6** | 1D 緯度灰雛菊世界 (1D Grey Daisyworld) | `uv run python main.py --page 6` |
| **7** | 2D 氣候與雛菊世界模型 (2D Grid Models) | `uv run python main.py --page 7` |
| **8** | 動態動畫與圖表匯出工坊 (Media Studio) | `uv run python main.py --page 8` |

### 3. 執行數值物理驗證測試

```powershell
uv run python main.py --test
```

---

## 🔬 實驗物理與生態理論重點

1. **冰雪反照率回饋與臨界點 (Ice-Albedo Tipping Point)**：
   - 0D EBM 中，因溫度低於冰雪臨界點 $T_{\text{ice}}$ 反照率急升，導致吸收輻射 $R_{\text{in}}$ 呈非線性 S 型，與長波冷卻輻射 $R_{\text{out}}$ 產生 3 個交點（狀態①溫暖穩定、狀態②部分結冰不穩定、狀態③雪球地球穩定）。
   - 當太陽常數 $S_0$ 低於臨界點 $\sim 1288.6 \text{ W/m}^2$ 時，溫暖態突然崩潰墜入雪球地球。
2. **蓋亞恆溫調節 (Planetary Homeostasis)**：
   - 0D/1D 雛菊世界展示生物個體無需全球意識或預見能力，僅憑局地適應性微氣候溫差 $q(\alpha_p - \alpha_i)$ 與最適生長溫度（$22.5^\circ\text{C}$），在太陽光度變化 $L \in [0.7, 1.5]$ 廣闊區間內自發穩定全球氣候。
3. **空間生態位分化 (Spatial Niche Differentiation)**：
   - 1D 雛菊模型中，高緯度極區自發由黑雛菊主導（吸熱減緩極區降溫），低緯度赤道由白雛菊主導（散熱避免熱帶過熱）。
4. **海陸熱對比與二維擴散 (2D Climate Coupling)**：
   - 2D 模型結合真實大陸邊界遮罩，陸地熱容量小、溫差劇烈，海洋熱容量大、具顯著緩衝效應，並真實模擬南北緯向與東西經向的大氣能量輸送。
