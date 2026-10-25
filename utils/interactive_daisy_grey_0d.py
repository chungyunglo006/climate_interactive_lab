"""
Interactive 60 FPS Client-Side Canvas Engine for 0D Grey Daisyworld (3 Species Competition).
Ensures coordinate axes, gridlines, and thresholds are rendered ONCE on a static layer,
while daisy population dynamics and temperature regulation update smoothly via requestAnimationFrame at 60 FPS.
Features:
- Wisconsin AOS Planetary Live Disk with White, Black, and Grey Daisies
- Precision Mercury Thermometer
- Real-Time Auto-Equilibrium Data Logger & CSV Exporter
- Dual-View Phase Curves (L vs Equilibrium) & Time Dynamics
- Advanced Experimental Parameters Collapsible Panel
- Full Dual-Physics Support (Lovelock 1983 Airless vs Wisconsin Stull 2000 Atmosphere)
- PNG Snapshot & Dynamic WebM Video Animation Recording
"""

def get_interactive_daisy_grey_0d_html(
    s0=917.0, l_val=1.0, alpha_w=0.75, alpha_b=0.25, alpha_g=0.50, alpha_u=0.5,
    q_val=20.0, gamma_val=0.3, aw_init=0.01, ab_init=0.01, ag_init=0.01, dt=0.1, itera=150,
    physics_mode="lovelock"
):
    """Generates self-contained 60 FPS hardware-accelerated interactive canvas HTML for 0D Grey Daisyworld."""
    opt_lovelock_sel = "selected" if physics_mode == "lovelock" else ""
    opt_stull_sel = "selected" if physics_mode == "stull" else ""
    badge_text = "🌻 Lovelock (1983)：S₀=917 W/m² (等效無大氣單一常數，光度 L=1.0 正處於三物種共存恆溫區)。" if physics_mode == "lovelock" else "🌍 Stull (2000)：S₀=1368 W/m² + 單層溫室效應 (T_s⁴ = 2T_e⁴) + 水平傳輸 Tr=0.6。在現代地球溫室下觀察灰雛菊競爭！"
    badge_border = "#00e5ff" if physics_mode == "lovelock" else "#22c55e"
    html_code = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}}

input, select, textarea {{
    user-select: text !important;
    pointer-events: auto !important;
}}

body {{
    background-color: transparent;
    color: #f8fafc;
    overflow-x: hidden;
    padding: 10px 4px 20px 4px;
}}

.control-panel {{
    background: linear-gradient(135deg, rgba(21, 28, 44, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid rgba(0, 229, 255, 0.25);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 18px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35);
}}

.panel-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}}

.panel-title {{
    font-size: 1.05rem;
    font-weight: 700;
    color: #00e5ff;
    letter-spacing: -0.3px;
}}

.ctrl-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 14px 20px;
}}

.ctrl-item {{
    display: flex;
    flex-direction: column;
    gap: 6px;
}}

.ctrl-label {{
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #94a3b8;
    font-weight: 600;
}}

.ctrl-input-row {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

input[type="range"] {{
    flex: 1;
    -webkit-appearance: none;
    height: 5px;
    background: rgba(255, 255, 255, 0.12);
    border-radius: 3px;
    outline: none;
    cursor: pointer;
}}

input[type="range"]::-webkit-slider-thumb {{
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    background: #00e5ff;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 0 10px rgba(0, 229, 255, 0.6);
    transition: transform 0.1s;
}}

input[type="range"]::-webkit-slider-thumb:hover {{
    transform: scale(1.25);
}}

.val-input {{
    width: 72px;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(0, 229, 255, 0.3);
    color: #00e5ff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 4px 6px;
    border-radius: 6px;
    text-align: right;
    outline: none;
    transition: all 0.2s;
}}

.val-input:focus {{
    border-color: #00e5ff;
    background: rgba(0, 229, 255, 0.18);
    box-shadow: 0 0 10px rgba(0, 229, 255, 0.35);
}}

.action-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    align-items: center;
}}

.btn {{
    background: linear-gradient(135deg, #00e5ff 0%, #0284c7 100%);
    color: #020617;
    border: none;
    padding: 7px 16px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}}

.btn:hover {{
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(0, 229, 255, 0.4);
}}

.btn-secondary {{
    background: rgba(255, 255, 255, 0.08);
    color: #f8fafc;
    border: 1px solid rgba(255, 255, 255, 0.15);
}}

.btn-secondary:hover {{
    background: rgba(255, 255, 255, 0.16);
    border-color: rgba(255, 255, 255, 0.3);
}}

select, input[type="number"].inline-input {{
    background: #0f172a;
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #f8fafc;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 0.82rem;
    outline: none;
}}

select:focus, input[type="number"].inline-input:focus {{
    border-color: #00e5ff;
}}

/* Wisconsin AOS Dashboard 3-Box Grid */
.planet-dashboard-grid {{
    display: grid;
    grid-template-columns: 200px 160px 1fr;
    gap: 14px;
    margin-bottom: 18px;
}}

@media (max-width: 900px) {{
    .planet-dashboard-grid {{
        grid-template-columns: 1fr;
    }}
}}

.dash-box {{
    background: linear-gradient(135deg, rgba(21, 28, 44, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}}

.dash-box-title {{
    font-size: 0.78rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
    width: 100%;
    text-align: left;
}}

.auto-table-container {{
    width: 100%;
    max-height: 145px;
    overflow-y: auto;
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(10, 15, 29, 0.6);
}}

.auto-table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
}}

.auto-table th {{
    background: rgba(15, 23, 42, 0.95);
    color: #94a3b8;
    padding: 5px 6px;
    text-align: right;
    position: sticky;
    top: 0;
    font-weight: 600;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}}

.auto-table th:first-child {{
    text-align: left;
}}

.auto-table td {{
    padding: 4px 6px;
    text-align: right;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}}

.auto-table td:first-child {{
    text-align: left;
}}

.auto-table tr:hover {{
    background: rgba(0, 229, 255, 0.08);
}}

/* Stat Cards */
.stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-bottom: 16px;
}}

.stat-card {{
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 12px 14px;
    border-left: 3px solid #00e5ff;
}}

.stat-title {{
    font-size: 0.72rem;
    color: #94a3b8;
    text-transform: uppercase;
    font-weight: 600;
}}

.stat-val {{
    font-size: 1.25rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    margin: 3px 0;
}}

.stat-sub {{
    font-size: 0.72rem;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
}}

/* Chart View Switcher */
.chart-view-switch-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 6px 14px;
    margin-bottom: 14px;
    flex-wrap: wrap;
    gap: 8px;
}}

.switch-btn-group {{
    display: flex;
    gap: 8px;
}}

.view-btn {{
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #94a3b8;
    padding: 5px 12px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.view-btn.active {{
    background: rgba(0, 229, 255, 0.2);
    border-color: #00e5ff;
    color: #00e5ff;
    box-shadow: 0 0 10px rgba(0, 229, 255, 0.25);
}}

/* Charts Grid */
.charts-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));
    gap: 16px;
}}

.chart-card {{
    background: linear-gradient(135deg, rgba(21, 28, 44, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35);
}}

.chart-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}}

.chart-title {{
    font-size: 0.92rem;
    font-weight: 700;
    color: #f8fafc;
}}

.chart-legend {{
    display: flex;
    gap: 10px;
    font-size: 0.72rem;
}}

.legend-item {{
    display: flex;
    align-items: center;
    gap: 4px;
    color: #94a3b8;
}}

.legend-color {{
    width: 10px;
    height: 10px;
    border-radius: 2px;
}}

.canvas-container {{
    position: relative;
    width: 100%;
    height: 350px;
}}

canvas {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}}

#tooltip {{
    position: absolute;
    display: none;
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid #00e5ff;
    padding: 8px 12px;
    border-radius: 8px;
    pointer-events: none;
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    color: #f8fafc;
    box-shadow: 0 4px 15px rgba(0, 229, 255, 0.25);
    z-index: 100;
}}
</style>
</head>
<body>

<div class="control-panel">
    <div class="panel-header">
        <div class="panel-title">⚪ 0D 灰雛菊世界物理參數面板 (三物種競爭 - 滑桿 + 精確數值直接輸入)</div>
        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <span style="font-size: 0.8rem; color: #94a3b8;">🎯 預設情境:</span>
            <select id="sel_preset">
                <option value="standard" selected>標準光度 (L = 1.0 - 灰雛菊與黑白共生)</option>
                <option value="mid_opt">最適恆溫區間 (L = 1.05 - 灰雛菊大繁茂)</option>
                <option value="low_l">微弱太陽 (L = 0.75 - 黑雛菊主導保溫)</option>
                <option value="high_l">強烈太陽 (L = 1.35 - 白雛菊主導散熱)</option>
                <option value="extreme_cold">極端嚴寒 (L = 0.55 - 雛菊全數凍死)</option>
                <option value="extreme_hot">極端酷熱 (L = 1.70 - 雛菊全數熱死)</option>
            </select>
        </div>
    </div>

    <div class="ctrl-grid">
        <div class="ctrl-item">
            <span class="ctrl-label"><span>太陽光度 L</span><span>相對光度</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_l" min="0.5" max="1.8" step="0.01" value="{l_val}">
                <input type="number" class="val-input" id="num_l" min="0.5" max="1.8" step="0.01" value="{l_val}">
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label"><span>灰雛菊反照率 α_g</span><span>中性競爭者</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_ag" min="0.35" max="0.65" step="0.01" value="{alpha_g}">
                <input type="number" class="val-input" id="num_ag" min="0.35" max="0.65" step="0.01" value="{alpha_g}">
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label"><span>白雛菊反照率 α_w</span><span>反射比</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_aw" min="0.5" max="0.9" step="0.01" value="{alpha_w}">
                <input type="number" class="val-input" id="num_aw" min="0.5" max="0.9" step="0.01" value="{alpha_w}">
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label"><span>黑雛菊反照率 α_b</span><span>反射比</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_ab" min="0.1" max="0.45" step="0.01" value="{alpha_b}">
                <input type="number" class="val-input" id="num_ab" min="0.1" max="0.45" step="0.01" value="{alpha_b}">
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label"><span>死亡率 γ</span><span>率 / 時間</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_gamma" min="0.05" max="0.5" step="0.01" value="{gamma_val}">
                <input type="number" class="val-input" id="num_gamma" min="0.05" max="0.5" step="0.01" value="{gamma_val}">
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label"><span>局部溫差係數 q</span><span>℃</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_q" min="5.0" max="40.0" step="1.0" value="{q_val}">
                <input type="number" class="val-input" id="num_q" min="5.0" max="40.0" step="1.0" value="{q_val}">
            </div>
        </div>
    </div>

    <div class="action-row">
        <button class="btn" id="btn_toggle_play">▶️ 開始動態演變</button>
        <button class="btn btn-secondary" id="btn_reset">🔄 重設標準光度</button>
        <button class="btn btn-secondary" id="btn_toggle_adv">⚙️ 進階參數</button>
        <button class="btn btn-secondary" id="btn_export_png">📸 截圖 PNG</button>
        <button class="btn btn-secondary" id="btn_record_video">🎥 錄製動態</button>

        <span style="color: #64748b; margin-left: 6px;">物理體系:</span>
        <select id="sel_physics_mode">
            <option value="lovelock" {opt_lovelock_sel}>🌻 Lovelock (1983) 等效無大氣 (S₀=917)</option>
            <option value="stull" {opt_stull_sel}>🌍 Wisconsin Stull (2000) 現代地球單層溫室 (S₀=1368)</option>
        </select>

        <span style="color: #64748b; margin-left: 6px;">演變變數:</span>
        <select id="sel_anim_target">
            <option value="l_val">☀️ 太陽光度 L</option>
            <option value="alpha_g">🔘 灰雛菊反照率 α_g</option>
            <option value="alpha_w">⚪ 白雛菊反照率 α_w</option>
            <option value="alpha_b">⚫ 黑雛菊反照率 α_b</option>
            <option value="alpha_u">🟤 裸地反照率 α_u</option>
            <option value="gamma_val">🍂 死亡率 γ</option>
            <option value="q_val">🌡️ 局部溫差係數 q</option>
            <option value="ag_init">🩶 灰雛菊初始值 ag,init</option>
            <option value="aw_init">🌱 白雛菊初始值 aw,init</option>
            <option value="ab_init">🌑 黑雛菊初始值 ab,init</option>
        </select>

        <span style="color: #64748b;">方向:</span>
        <select id="sel_anim_dir">
            <option value="pingpong">來回擺動 (Ping-Pong)</option>
            <option value="inc">往大增加 (+)</option>
            <option value="dec">往小減少 (-)</option>
        </select>

        <span style="color: #64748b;">速率:</span>
        <input type="number" class="inline-input" id="num_anim_speed" value="0.003" step="0.001" min="0.0005" max="0.03" style="width: 75px;">
    </div>

    <!-- Advanced Experimental Parameters Collapsible Panel -->
    <div id="advanced_panel" style="display: none; margin-top: 14px; padding: 14px 18px; background: rgba(15, 23, 42, 0.7); border: 1px dashed rgba(0, 229, 255, 0.35); border-radius: 10px;">
        <div style="font-size: 0.82rem; font-weight: 700; color: #00e5ff; margin-bottom: 12px; display: flex; align-items: center; gap: 6px;">
            <span>⚙️ 進階實驗變數面板 (三物種初始覆蓋率與數值微調 - 支援滑桿與數字直接輸入)</span>
        </div>
        <div class="ctrl-grid" style="grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));">
            <div class="ctrl-item">
                <span class="ctrl-label"><span>灰雛菊初始覆蓋 ag,init</span><span>初始比例</span></span>
                <div class="ctrl-input-row">
                    <input type="range" id="slider_ag_init" min="0.00" max="0.50" step="0.005" value="{ag_init}">
                    <input type="number" class="val-input" id="num_ag_init" min="0.00" max="0.50" step="0.005" value="{ag_init}">
                </div>
            </div>
            <div class="ctrl-item">
                <span class="ctrl-label"><span>白雛菊初始覆蓋 aw,init</span><span>初始比例</span></span>
                <div class="ctrl-input-row">
                    <input type="range" id="slider_aw_init" min="0.00" max="0.50" step="0.005" value="{aw_init}">
                    <input type="number" class="val-input" id="num_aw_init" min="0.00" max="0.50" step="0.005" value="{aw_init}">
                </div>
            </div>
            <div class="ctrl-item">
                <span class="ctrl-label"><span>黑雛菊初始覆蓋 ab,init</span><span>初始比例</span></span>
                <div class="ctrl-input-row">
                    <input type="range" id="slider_ab_init" min="0.00" max="0.50" step="0.005" value="{ab_init}">
                    <input type="number" class="val-input" id="num_ab_init" min="0.00" max="0.50" step="0.005" value="{ab_init}">
                </div>
            </div>
            <div class="ctrl-item">
                <span class="ctrl-label"><span>裸地反照率 α_u</span><span>反射比</span></span>
                <div class="ctrl-input-row">
                    <input type="range" id="slider_au" min="0.2" max="0.8" step="0.01" value="{alpha_u}">
                    <input type="number" class="val-input" id="num_au" min="0.2" max="0.8" step="0.01" value="{alpha_u}">
                </div>
            </div>
            <div class="ctrl-item">
                <span class="ctrl-label"><span>數值步長 dt</span><span>時間微元</span></span>
                <div class="ctrl-input-row">
                    <input type="range" id="slider_dt" min="0.02" max="0.40" step="0.01" value="{dt}">
                    <input type="number" class="val-input" id="num_dt" min="0.02" max="0.40" step="0.01" value="{dt}">
                </div>
            </div>
            <div class="ctrl-item">
                <span class="ctrl-label"><span>迭代次數 N (步)</span><span>總步長</span></span>
                <div class="ctrl-input-row">
                    <input type="range" id="slider_itera" min="50" max="400" step="10" value="{itera}">
                    <input type="number" class="val-input" id="num_itera" min="50" max="400" step="10" value="{itera}">
                </div>
            </div>
        </div>
    </div>

    <div id="physics_mode_badge" style="font-size: 0.75rem; color: #64748b; background: rgba(15, 23, 42, 0.6); border-radius: 6px; padding: 6px 10px; border-left: 3px solid {badge_border}; margin-top: 12px; width: 100%;">
        {badge_text}
    </div>
</div>

<!-- Wisconsin AOS Dashboard: Planetary Live Disk + Thermometer + Experiment Logger -->
<div class="planet-dashboard-grid">
    <!-- Box 1: Planet Live Disk with 3 Daisy species -->
    <div class="dash-box">
        <div class="dash-box-title">🪐 活體行星盤面 (3物種競爭)</div>
        <div style="position: relative; width: 170px; height: 170px;">
            <canvas id="cv_planet" width="170" height="170" style="position: static;"></canvas>
        </div>
        <div id="planet_disk_caption" style="font-size: 0.70rem; color: #94a3b8; font-family: 'JetBrains Mono', monospace; margin-top: 6px; text-align: center;">
            灰: --% | 白: --% | 黑: --%
        </div>
    </div>

    <!-- Box 2: Vertical Precision Thermometer -->
    <div class="dash-box">
        <div class="dash-box-title">🌡️ 擬真水銀溫度計</div>
        <div style="position: relative; width: 140px; height: 180px;">
            <canvas id="cv_thermo" width="140" height="180" style="position: static;"></canvas>
        </div>
    </div>

    <!-- Box 3: Auto-Equilibrium Data Logger & CSV Exporter -->
    <div class="dash-box" style="align-items: stretch; padding: 0 4px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <div class="dash-box-title" style="margin-bottom: 0;">📋 平衡狀態自動紀錄表</div>
            <div style="display: flex; gap: 6px; align-items: center;">
                <span id="lbl_point_count" style="font-size: 0.72rem; color: #00e5ff; font-family: 'JetBrains Mono', monospace;">0 筆紀錄</span>
                <button class="btn btn-secondary" id="btn_clear_points" style="font-size: 0.72rem; padding: 3px 8px;">🧹 清除</button>
                <button class="btn btn-secondary" id="btn_export_csv" style="font-size: 0.72rem; padding: 3px 8px;">📥 匯出</button>
            </div>
        </div>

        <div class="auto-table-container">
            <table class="auto-table" id="table_points">
                <thead>
                    <tr>
                        <th>光度 L</th>
                        <th>灰雛菊</th>
                        <th>白雛菊</th>
                        <th>黑雛菊</th>
                        <th>裸地</th>
                        <th>調控均溫</th>
                        <th>死星基線</th>
                    </tr>
                </thead>
                <tbody id="table_points_body">
                    <tr><td colspan="7" style="text-align: center; color: #64748b; padding: 18px 6px;">動態演變時將自動即時記錄各光度平衡點...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-title">調節後行星均溫 (T_p)</div>
        <div class="stat-val" id="stat_tp" style="color: #22c55e;">-- ℃</div>
        <div class="stat-sub" id="stat_gaea_eval">三物種共存評估中...</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">灰雛菊覆蓋率 (中性競爭者)</div>
        <div class="stat-val" id="stat_ag" style="color: #94a3b8;">-- %</div>
        <div class="stat-sub" id="stat_tg">局地溫: -- ℃</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">白雛菊覆蓋率 (散熱)</div>
        <div class="stat-val" id="stat_aw" style="color: #f8fafc;">-- %</div>
        <div class="stat-sub" id="stat_tw">局地溫: -- ℃</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">黑雛菊覆蓋率 (保溫)</div>
        <div class="stat-val" id="stat_ab" style="color: #475569;">-- %</div>
        <div class="stat-sub" id="stat_tb">局地溫: -- ℃</div>
    </div>
</div>

<!-- Chart View Switch Bar -->
<div class="chart-view-switch-bar">
    <div class="switch-btn-group">
        <button class="view-btn active" id="btn_view_curves">☀️ 光度平衡曲線相圖 (L vs 平衡狀態)</button>
        <button class="view-btn" id="btn_view_timeseries">⏱️ 單次演化時間動態消長 (Time Dynamics)</button>
    </div>
    <div id="view_mode_hint" style="font-size: 0.75rem; color: #94a3b8;">
        隨著太陽光度演變，自動即時記錄三物種平衡點並直接描繪出相圖消長與恆溫倒 U 型曲線！
    </div>
</div>

<div class="charts-grid">
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title" id="title_chart1">⚪ 各光度平衡覆蓋率相圖曲線 (三物種演替消長)</div>
            <div class="chart-legend" id="legend_chart1">
                <div class="legend-item"><div class="legend-color" style="background: #94a3b8;"></div> 灰雛菊</div>
                <div class="legend-item"><div class="legend-color" style="background: #f8fafc;"></div> 白雛菊</div>
                <div class="legend-item"><div class="legend-color" style="background: #475569;"></div> 黑雛菊</div>
                <div class="legend-item"><div class="legend-color" style="background: #d97706; border-top: 1px dashed;"></div> 裸地</div>
            </div>
        </div>
        <div class="canvas-container" id="container1">
            <canvas id="bg1"></canvas>
            <canvas id="fg1"></canvas>
        </div>
    </div>

    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title" id="title_chart2">🌡️ 蓋亞恆溫調控相圖曲線 (Luminosity vs 平衡溫度)</div>
            <div class="chart-legend" id="legend_chart2">
                <div class="legend-item"><div class="legend-color" style="background: #22c55e;"></div> 調節 Tp</div>
                <div class="legend-item"><div class="legend-color" style="background: #ef4444; border-top: 1px dashed;"></div> 死星基線</div>
                <div class="legend-item"><div class="legend-color" style="background: #00e5ff; border-radius: 50%;"></div> 當前 L</div>
            </div>
        </div>
        <div class="canvas-container" id="container2">
            <canvas id="bg2"></canvas>
            <canvas id="fg2"></canvas>
        </div>
    </div>
</div>

<div id="tooltip"></div>

<script>
const SIGMA = 5.670374e-8;

let state = {{
    s0: {s0},
    l_val: {l_val},
    alpha_w: {alpha_w},
    alpha_b: {alpha_b},
    alpha_g: {alpha_g},
    alpha_u: {alpha_u},
    q_val: {q_val},
    gamma_val: {gamma_val},
    aw_init: {aw_init},
    ab_init: {ab_init},
    ag_init: {ag_init},
    dt: {dt},
    itera: {itera},
    physicsMode: '{physics_mode}',
    isPlaying: false,
    pingPongDir: 1,
    simData: null,
    chartView: 'curves',
    recordedPoints: []
}};

// DOM Elements
const selPhysicsMode = document.getElementById('sel_physics_mode');
const physicsModeBadge = document.getElementById('physics_mode_badge');
const sliderL = document.getElementById('slider_l');
const numL = document.getElementById('num_l');
const sliderAg = document.getElementById('slider_ag');
const numAg = document.getElementById('num_ag');
const sliderAw = document.getElementById('slider_aw');
const numAw = document.getElementById('num_aw');
const sliderAb = document.getElementById('slider_ab');
const numAb = document.getElementById('num_ab');
const sliderGamma = document.getElementById('slider_gamma');
const numGamma = document.getElementById('num_gamma');
const sliderQ = document.getElementById('slider_q');
const numQ = document.getElementById('num_q');
const selPreset = document.getElementById('sel_preset');

const btnTogglePlay = document.getElementById('btn_toggle_play');
const btnReset = document.getElementById('btn_reset');
const selAnimTarget = document.getElementById('sel_anim_target');
const selAnimDir = document.getElementById('sel_anim_dir');
const numAnimSpeed = document.getElementById('num_anim_speed');

const sliderAgInit = document.getElementById('slider_ag_init');
const numAgInit = document.getElementById('num_ag_init');
const sliderAwInit = document.getElementById('slider_aw_init');
const numAwInit = document.getElementById('num_aw_init');
const sliderAbInit = document.getElementById('slider_ab_init');
const numAbInit = document.getElementById('num_ab_init');
const sliderAu = document.getElementById('slider_au');
const numAu = document.getElementById('num_au');
const sliderDt = document.getElementById('slider_dt');
const numDt = document.getElementById('num_dt');
const sliderItera = document.getElementById('slider_itera');
const numItera = document.getElementById('num_itera');

const btnToggleAdv = document.getElementById('btn_toggle_adv');
const advancedPanel = document.getElementById('advanced_panel');
const btnExportPng = document.getElementById('btn_export_png');
const btnRecordVideo = document.getElementById('btn_record_video');

const cvPlanet = document.getElementById('cv_planet');
const ctxPlanet = cvPlanet.getContext('2d');
const cvThermo = document.getElementById('cv_thermo');
const ctxThermo = cvThermo.getContext('2d');
const planetDiskCaption = document.getElementById('planet_disk_caption');

const btnClearPoints = document.getElementById('btn_clear_points');
const btnExportCsv = document.getElementById('btn_export_csv');
const lblPointCount = document.getElementById('lbl_point_count');
const tablePointsBody = document.getElementById('table_points_body');

const btnViewCurves = document.getElementById('btn_view_curves');
const btnViewTimeseries = document.getElementById('btn_view_timeseries');
const viewModeHint = document.getElementById('view_mode_hint');
const titleChart1 = document.getElementById('title_chart1');
const titleChart2 = document.getElementById('title_chart2');
const legendChart1 = document.getElementById('legend_chart1');
const legendChart2 = document.getElementById('legend_chart2');

const statTp = document.getElementById('stat_tp');
const statGaeaEval = document.getElementById('stat_gaea_eval');
const statAg = document.getElementById('stat_ag');
const statTg = document.getElementById('stat_tg');
const statAw = document.getElementById('stat_aw');
const statTw = document.getElementById('stat_tw');
const statAb = document.getElementById('stat_ab');
const statTb = document.getElementById('stat_tb');

const bg1 = document.getElementById('bg1');
const fg1 = document.getElementById('fg1');
const bg2 = document.getElementById('bg2');
const fg2 = document.getElementById('fg2');
const tooltip = document.getElementById('tooltip');

const ctxBg1 = bg1.getContext('2d');
const ctxFg1 = fg1.getContext('2d');
const ctxBg2 = bg2.getContext('2d');
const ctxFg2 = fg2.getContext('2d');

let width = 0, height = 0;
const margin = {{ left: 55, right: 25, top: 25, bottom: 40 }};

function resizeCanvases() {{
    const rect = document.getElementById('container1').getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    width = rect.width;
    height = rect.height;

    [bg1, fg1, bg2, fg2].forEach(c => {{
        c.width = width * dpr;
        c.height = height * dpr;
        c.style.width = width + 'px';
        c.style.height = height + 'px';
        const ctx = c.getContext('2d');
        ctx.scale(dpr, dpr);
    }});

    drawStaticBackgrounds();
    renderDynamicTraces();
}}

function betaGrowth(T) {{
    return Math.max(0.0, 1.0 - 0.003265 * Math.pow(22.5 - T, 2));
}}

function runSimulation() {{
    let t = [];
    let awList = [], abList = [], agList = [], auList = [];
    let TpList = [], TwList = [], TbList = [], TgList = [];

    let aw = state.aw_init;
    let ab = state.ab_init;
    let ag = state.ag_init;

    const isStull = state.physicsMode === 'stull';
    const numSteps = Math.round(state.itera);
    const dt = state.dt;

    for (let step = 0; step <= numSteps; step++) {{
        const au = Math.max(0.0, Math.min(1.0, 1.0 - aw - ab - ag));
        const alphaP = aw * state.alpha_w + ab * state.alpha_b + ag * state.alpha_g + au * state.alpha_u;

        let TpC, Tw, Tb, Tg;
        if (!isStull) {{
            const TpK = Math.pow((state.s0 * state.l_val * (1.0 - alphaP)) / SIGMA, 0.25);
            TpC = TpK - 273.15;
            Tw = TpC + state.q_val * (alphaP - state.alpha_w);
            Tb = TpC + state.q_val * (alphaP - state.alpha_b);
            Tg = TpC + state.q_val * (alphaP - state.alpha_g);
        }} else {{
            const q = (state.s0 * state.l_val) / (4.0 * SIGMA);
            const Te4 = q * (1.0 - alphaP);
            const Ts4 = 2.0 * Te4;
            TpC = Math.pow(Ts4, 0.25) - 273.15;
            const Tr = 0.6;
            const Tw4 = Math.max(1e5, (1.0 - Tr) * q * (alphaP - state.alpha_w) + Ts4);
            const Tb4 = Math.max(1e5, (1.0 - Tr) * q * (alphaP - state.alpha_b) + Ts4);
            const Tg4 = Math.max(1e5, (1.0 - Tr) * q * (alphaP - state.alpha_g) + Ts4);
            Tw = Math.pow(Tw4, 0.25) - 273.15;
            Tb = Math.pow(Tb4, 0.25) - 273.15;
            Tg = Math.pow(Tg4, 0.25) - 273.15;
        }}

        const betaW = betaGrowth(Tw);
        const betaB = betaGrowth(Tb);
        const betaG = betaGrowth(Tg);

        t.push(step * dt);
        awList.push(aw);
        abList.push(ab);
        agList.push(ag);
        auList.push(au);
        TpList.push(TpC);
        TwList.push(Tw);
        TbList.push(Tb);
        TgList.push(Tg);

        const daw = aw * (au * betaW - state.gamma_val);
        const dab = ab * (au * betaB - state.gamma_val);
        const dag = ag * (au * betaG - state.gamma_val);

        aw = Math.max(0.001, Math.min(0.99, aw + dt * daw));
        ab = Math.max(0.001, Math.min(0.99, ab + dt * dab));
        ag = Math.max(0.001, Math.min(0.99, ag + dt * dag));
        if (aw + ab + ag > 0.99) {{
            const sc = 0.99 / (aw + ab + ag);
            aw *= sc; ab *= sc; ag *= sc;
        }}
    }}

    let Tnobio;
    if (!isStull) {{
        Tnobio = Math.pow((state.s0 * state.l_val * (1.0 - state.alpha_u)) / SIGMA, 0.25) - 273.15;
    }} else {{
        const qDead = (state.s0 * state.l_val) / (4.0 * SIGMA);
        Tnobio = Math.pow(2.0 * qDead * (1.0 - state.alpha_u), 0.25) - 273.15;
    }}

    state.simData = {{
        t, aw: awList, ab: abList, ag: agList, au: auList,
        Tp: TpList, Tw: TwList, Tb: TbList, Tg: TgList,
        finalTp: TpList[TpList.length - 1],
        finalAw: awList[awList.length - 1],
        finalAb: abList[abList.length - 1],
        finalAg: agList[agList.length - 1],
        finalAu: auList[auList.length - 1],
        finalTw: TwList[TwList.length - 1],
        finalTb: TbList[TbList.length - 1],
        finalTg: TgList[TgList.length - 1],
        Tnobio: Tnobio
    }};

    drawPlanetDisk();
    drawThermometer();
    autoRecordEquilibrium();
}}

// Draw Planet Live Disk (3 Species)
function drawPlanetDisk() {{
    if (!state.simData) return;
    const d = state.simData;
    const w = cvPlanet.width;
    const h = cvPlanet.height;
    ctxPlanet.clearRect(0, 0, w, h);

    const cx = w / 2;
    const cy = h / 2;
    const r = 58;

    const Tp = d.finalTp;
    let haloColor = 'rgba(34, 197, 94, 0.35)';
    if (Tp < 5.0) haloColor = 'rgba(56, 189, 248, 0.45)';
    else if (Tp > 35.0) haloColor = 'rgba(239, 68, 68, 0.45)';

    // Halo
    const gradHalo = ctxPlanet.createRadialGradient(cx, cy, r * 0.85, cx, cy, r * 1.35);
    gradHalo.addColorStop(0, haloColor);
    gradHalo.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctxPlanet.fillStyle = gradHalo;
    ctxPlanet.beginPath();
    ctxPlanet.arc(cx, cy, r * 1.35, 0, Math.PI * 2);
    ctxPlanet.fill();

    // Planet Sphere
    ctxPlanet.save();
    ctxPlanet.beginPath();
    ctxPlanet.arc(cx, cy, r, 0, Math.PI * 2);
    ctxPlanet.clip();

    // Soil background
    ctxPlanet.fillStyle = '#92400e';
    ctxPlanet.fillRect(cx - r, cy - r, r * 2, r * 2);

    const aw = d.finalAw;
    const ab = d.finalAb;
    const ag = d.finalAg;

    // Grey Daisy slice
    const angleG = ag * Math.PI * 2;
    ctxPlanet.fillStyle = '#94a3b8';
    ctxPlanet.beginPath();
    ctxPlanet.moveTo(cx, cy);
    ctxPlanet.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + angleG);
    ctxPlanet.closePath();
    ctxPlanet.fill();

    // White Daisy slice
    const angleW = aw * Math.PI * 2;
    ctxPlanet.fillStyle = '#f8fafc';
    ctxPlanet.beginPath();
    ctxPlanet.moveTo(cx, cy);
    ctxPlanet.arc(cx, cy, r, -Math.PI / 2 + angleG, -Math.PI / 2 + angleG + angleW);
    ctxPlanet.closePath();
    ctxPlanet.fill();

    // Black Daisy slice
    const angleB = ab * Math.PI * 2;
    ctxPlanet.fillStyle = '#334155';
    ctxPlanet.beginPath();
    ctxPlanet.moveTo(cx, cy);
    ctxPlanet.arc(cx, cy, r, -Math.PI / 2 + angleG + angleW, -Math.PI / 2 + angleG + angleW + angleB);
    ctxPlanet.closePath();
    ctxPlanet.fill();

    // 3D Sphere Spherical Shadow Gradient
    const sphereGrad = ctxPlanet.createRadialGradient(cx - r * 0.35, cy - r * 0.35, r * 0.1, cx, cy, r);
    sphereGrad.addColorStop(0, 'rgba(255, 255, 255, 0.35)');
    sphereGrad.addColorStop(0.6, 'rgba(0, 0, 0, 0)');
    sphereGrad.addColorStop(1, 'rgba(0, 0, 0, 0.7)');
    ctxPlanet.fillStyle = sphereGrad;
    ctxPlanet.beginPath();
    ctxPlanet.arc(cx, cy, r, 0, Math.PI * 2);
    ctxPlanet.fill();
    ctxPlanet.restore();

    ctxPlanet.strokeStyle = 'rgba(255, 255, 255, 0.25)';
    ctxPlanet.lineWidth = 1.5;
    ctxPlanet.beginPath();
    ctxPlanet.arc(cx, cy, r, 0, Math.PI * 2);
    ctxPlanet.stroke();

    planetDiskCaption.innerHTML = `灰: <b style="color:#94a3b8;">${{(ag*100).toFixed(1)}}%</b> | 白: <b style="color:#f8fafc;">${{(aw*100).toFixed(1)}}%</b> | 黑: <b style="color:#475569;">${{(ab*100).toFixed(1)}}%</b>`;
}}

// Draw Precision Mercury Thermometer
function drawThermometer() {{
    if (!state.simData) return;
    const d = state.simData;
    const w = cvThermo.width;
    const h = cvThermo.height;
    ctxThermo.clearRect(0, 0, w, h);

    const tubeX = 48;
    const tubeY = 22;
    const tubeW = 20;
    const tubeH = 130;
    const bulbR = 17;
    const bulbY = tubeY + tubeH + 8;

    const tMin = -15.0;
    const tMax = 55.0;
    const getY = temp => tubeY + tubeH * (1.0 - (temp - tMin) / (tMax - tMin));

    // Green zone 5 to 40 degC
    const y5 = getY(5.0);
    const y40 = getY(40.0);
    ctxThermo.fillStyle = 'rgba(34, 197, 94, 0.12)';
    ctxThermo.fillRect(tubeX - 2, y40, tubeW + 4, y5 - y40);

    // Ticks
    const ticks = [-10, 0, 10, 20, 30, 40, 50];
    ctxThermo.font = '9px "JetBrains Mono", monospace';
    ctxThermo.textAlign = 'right';
    ctxThermo.textBaseline = 'middle';

    ticks.forEach(tv => {{
        const y = getY(tv);
        ctxThermo.strokeStyle = tv === 0 ? '#38bdf8' : (tv === 20 ? '#22c55e' : 'rgba(255, 255, 255, 0.15)');
        ctxThermo.lineWidth = tv === 0 ? 1.5 : 1;
        ctxThermo.beginPath();
        ctxThermo.moveTo(tubeX - 8, y);
        ctxThermo.lineTo(tubeX - 2, y);
        ctxThermo.stroke();

        ctxThermo.fillStyle = tv === 0 ? '#38bdf8' : '#64748b';
        ctxThermo.fillText(tv + '°', tubeX - 10, y);
    }});

    // Optimal 22.5 degC line
    const yOpt = getY(22.5);
    ctxThermo.setLineDash([2, 2]);
    ctxThermo.strokeStyle = '#00e5ff';
    ctxThermo.beginPath();
    ctxThermo.moveTo(tubeX + tubeW + 2, yOpt);
    ctxThermo.lineTo(tubeX + tubeW + 14, yOpt);
    ctxThermo.stroke();
    ctxThermo.setLineDash([]);
    ctxThermo.fillStyle = '#00e5ff';
    ctxThermo.textAlign = 'left';
    ctxThermo.fillText('22.5°', tubeX + tubeW + 16, yOpt);

    // Glass Tube
    ctxThermo.fillStyle = 'rgba(15, 23, 42, 0.7)';
    ctxThermo.fillRect(tubeX, tubeY, tubeW, tubeH);

    // Dead planet marker
    const yDead = Math.max(tubeY, Math.min(tubeY + tubeH, getY(d.Tnobio)));
    ctxThermo.fillStyle = '#ef4444';
    ctxThermo.fillRect(tubeX + tubeW / 2, yDead, tubeW / 2, (tubeY + tubeH) - yDead);

    // Mercury column
    const yBio = Math.max(tubeY, Math.min(tubeY + tubeH, getY(d.finalTp)));
    const gradMerc = ctxThermo.createLinearGradient(tubeX, 0, tubeX + tubeW / 2, 0);
    gradMerc.addColorStop(0, '#4ade80');
    gradMerc.addColorStop(1, '#22c55e');
    ctxThermo.fillStyle = gradMerc;
    ctxThermo.fillRect(tubeX, yBio, tubeW / 2, (tubeY + tubeH) - yBio);

    // Border
    ctxThermo.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctxThermo.lineWidth = 1.5;
    ctxThermo.strokeRect(tubeX, tubeY, tubeW, tubeH);

    // Bulb
    ctxThermo.beginPath();
    ctxThermo.arc(tubeX + tubeW / 2, bulbY, bulbR, 0, Math.PI * 2);
    ctxThermo.fillStyle = '#22c55e';
    ctxThermo.fill();
    ctxThermo.strokeStyle = 'rgba(255, 255, 255, 0.4)';
    ctxThermo.lineWidth = 1.5;
    ctxThermo.stroke();

    ctxThermo.textAlign = 'left';
    ctxThermo.font = '10px "Plus Jakarta Sans", sans-serif';
    ctxThermo.fillStyle = '#22c55e';
    ctxThermo.fillText(`Tp: ${{d.finalTp.toFixed(1)}}℃`, tubeX + tubeW + 12, tubeY + 20);
    ctxThermo.fillStyle = '#ef4444';
    ctxThermo.fillText(`死星: ${{d.Tnobio.toFixed(1)}}℃`, tubeX + tubeW + 12, tubeY + 36);
}}

function autoRecordEquilibrium() {{
    if (!state.simData) return;
    const d = state.simData;
    const l = parseFloat(state.l_val.toFixed(2));
    const pt = {{
        l: l,
        Tp: d.finalTp,
        Tnobio: d.Tnobio,
        ag: d.finalAg,
        aw: d.finalAw,
        ab: d.finalAb,
        au: d.finalAu,
        mode: state.physicsMode
    }};
    const idx = state.recordedPoints.findIndex(p => Math.abs(p.l - l) < 0.005);
    if (idx >= 0) {{
        state.recordedPoints[idx] = pt;
    }} else {{
        state.recordedPoints.push(pt);
        state.recordedPoints.sort((a, b) => a.l - b.l);
    }}
    updateTablePoints();
}}

function updateTablePoints() {{
    lblPointCount.innerText = `${{state.recordedPoints.length}} 筆紀錄`;
    if (state.recordedPoints.length === 0) {{
        tablePointsBody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: #64748b; padding: 18px 6px;">動態演變時將自動即時記錄各光度平衡點...</td></tr>';
        return;
    }}
    let html = '';
    const curL = parseFloat(state.l_val.toFixed(2));
    state.recordedPoints.forEach(p => {{
        const isCur = Math.abs(p.l - curL) < 0.005;
        const rowStyle = isCur ? 'style="background: rgba(0, 229, 255, 0.16); font-weight: bold;"' : '';
        html += `<tr ${{rowStyle}}>
            <td style="color: #00e5ff; font-weight: 600;">${{p.l.toFixed(2)}}</td>
            <td style="color: #94a3b8;">${{(p.ag * 100).toFixed(1)}}%</td>
            <td style="color: #f8fafc;">${{(p.aw * 100).toFixed(1)}}%</td>
            <td style="color: #475569;">${{(p.ab * 100).toFixed(1)}}%</td>
            <td style="color: #d97706;">${{(p.au * 100).toFixed(1)}}%</td>
            <td style="color: #22c55e;">${{p.Tp.toFixed(2)}}℃</td>
            <td style="color: #ef4444;">${{p.Tnobio.toFixed(1)}}℃</td>
        </tr>`;
    }});
    tablePointsBody.innerHTML = html;
}}

function exportPointsToCsv() {{
    if (state.recordedPoints.length === 0) {{
        alert('尚無紀錄可供匯出！請先進行動態演變或調整光度。');
        return;
    }}
    let csv = 'Luminosity,GreyDaisy_Percent,WhiteDaisy_Percent,BlackDaisy_Percent,BareGround_Percent,RegulatedTemp_C,DeadPlanetTemp_C,PhysicsMode\n';
    state.recordedPoints.forEach(p => {{
        csv += `${{p.l.toFixed(2)}},${{(p.ag * 100).toFixed(2)}},${{(p.aw * 100).toFixed(2)}},${{(p.ab * 100).toFixed(2)}},${{(p.au * 100).toFixed(2)}},${{p.Tp.toFixed(2)}},${{p.Tnobio.toFixed(2)}},${{p.mode}}\n`;
    }});
    const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `daisyworld_0d_grey_equilibrium_${{state.physicsMode}}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}}

function setChartView(view) {{
    state.chartView = view;
    if (view === 'curves') {{
        btnViewCurves.classList.add('active');
        btnViewTimeseries.classList.remove('active');
        titleChart1.innerText = '⚪ 各光度平衡覆蓋率相圖曲線 (三物種演替消長)';
        titleChart2.innerText = '🌡️ 蓋亞恆溫調控相圖曲線 (Luminosity vs 平衡溫度)';
        legendChart2.innerHTML = `
            <div class="legend-item"><div class="legend-color" style="background: #22c55e;"></div> 調節 Tp</div>
            <div class="legend-item"><div class="legend-color" style="background: #ef4444; border-top: 1px dashed;"></div> 死星基線</div>
            <div class="legend-item"><div class="legend-color" style="background: #00e5ff; border-radius: 50%;"></div> 當前 L</div>
        `;
        viewModeHint.innerText = '隨著太陽光度演變，自動即時記錄三物種平衡點並直接描繪出相圖消長與恆溫倒 U 型曲線！';
    }} else {{
        btnViewTimeseries.classList.add('active');
        btnViewCurves.classList.remove('active');
        titleChart1.innerText = '⚪ 三物種覆蓋率時間消長 (Time Dynamics)';
        titleChart2.innerText = '🌡️ 行星與物種溫度時間動態 (Time Dynamics)';
        legendChart2.innerHTML = `
            <div class="legend-item"><div class="legend-color" style="background: #22c55e;"></div> 行星均溫 Tp</div>
            <div class="legend-item"><div class="legend-color" style="background: #94a3b8; border-top: 1px dashed;"></div> 灰雛菊 Tg</div>
            <div class="legend-item"><div class="legend-color" style="background: #ef4444; border-top: 1px dashed;"></div> 死星基線</div>
        `;
        viewModeHint.innerText = '展示當前光度下 150 步時間動態數值演變歷程。';
    }}
    drawStaticBackgrounds();
    renderDynamicTraces();
}}

function drawStaticBackgrounds() {{
    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;
    const isCurves = state.chartView === 'curves';

    // Chart 1 BG
    ctxBg1.clearRect(0, 0, width, height);
    ctxBg1.fillStyle = 'rgba(15, 23, 42, 0.45)';
    ctxBg1.fillRect(margin.left, margin.top, plotW, plotH);

    const yTicks1 = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0];
    ctxBg1.font = '11px "JetBrains Mono", monospace';
    ctxBg1.fillStyle = '#64748b';
    ctxBg1.textAlign = 'right';
    ctxBg1.textBaseline = 'middle';
    ctxBg1.strokeStyle = 'rgba(255, 255, 255, 0.07)';
    ctxBg1.lineWidth = 1;

    yTicks1.forEach(val => {{
        const y = margin.top + plotH * (1.0 - val);
        ctxBg1.beginPath();
        ctxBg1.moveTo(margin.left, y);
        ctxBg1.lineTo(margin.left + plotW, y);
        ctxBg1.stroke();
        ctxBg1.fillText((val * 100).toFixed(0) + '%', margin.left - 8, y);
    }});

    ctxBg1.textAlign = 'center';
    ctxBg1.textBaseline = 'top';

    if (isCurves) {{
        const lMin = 0.6, lMax = 1.6;
        const lTicks = [0.6, 0.8, 1.0, 1.2, 1.4, 1.6];
        lTicks.forEach(lv => {{
            const x = margin.left + plotW * ((lv - lMin) / (lMax - lMin));
            ctxBg1.beginPath();
            ctxBg1.moveTo(x, margin.top);
            ctxBg1.lineTo(x, margin.top + plotH);
            ctxBg1.stroke();
            ctxBg1.fillText(lv.toFixed(1), x, margin.top + plotH + 8);
        }});
        const x1 = margin.left + plotW * ((1.0 - lMin) / (lMax - lMin));
        ctxBg1.save();
        ctxBg1.setLineDash([2, 4]);
        ctxBg1.strokeStyle = 'rgba(0, 229, 255, 0.25)';
        ctxBg1.beginPath();
        ctxBg1.moveTo(x1, margin.top);
        ctxBg1.lineTo(x1, margin.top + plotH);
        ctxBg1.stroke();
        ctxBg1.restore();

        ctxBg1.fillStyle = '#00e5ff';
        ctxBg1.font = '11px "Plus Jakarta Sans", sans-serif';
        ctxBg1.fillText('太陽光度 L (Luminosity)', margin.left + plotW / 2, margin.top + plotH + 24);
    }} else {{
        const xMax = state.itera * state.dt;
        const xStep = Math.max(2, Math.round(xMax / 6));
        for (let xVal = 0; xVal <= xMax; xVal += xStep) {{
            const x = margin.left + plotW * (xVal / xMax);
            ctxBg1.beginPath();
            ctxBg1.moveTo(x, margin.top);
            ctxBg1.lineTo(x, margin.top + plotH);
            ctxBg1.stroke();
            ctxBg1.fillText(xVal, x, margin.top + plotH + 8);
        }}
        ctxBg1.fillStyle = '#64748b';
        ctxBg1.fillText('演化時間 (Time Steps)', margin.left + plotW / 2, margin.top + plotH + 24);
    }}

    ctxBg1.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctxBg1.strokeRect(margin.left, margin.top, plotW, plotH);

    // Chart 2 BG
    ctxBg2.clearRect(0, 0, width, height);
    ctxBg2.fillStyle = 'rgba(15, 23, 42, 0.45)';
    ctxBg2.fillRect(margin.left, margin.top, plotW, plotH);

    const yMin2 = 0.0, yMax2 = 50.0;
    const yTicks2 = [0, 10, 20, 30, 40, 50];

    ctxBg2.font = '11px "JetBrains Mono", monospace';
    ctxBg2.fillStyle = '#64748b';
    ctxBg2.textAlign = 'right';
    ctxBg2.textBaseline = 'middle';
    ctxBg2.strokeStyle = 'rgba(255, 255, 255, 0.07)';
    ctxBg2.lineWidth = 1;

    yTicks2.forEach(val => {{
        const y = margin.top + plotH * (1.0 - (val - yMin2) / (yMax2 - yMin2));
        ctxBg2.beginPath();
        ctxBg2.moveTo(margin.left, y);
        ctxBg2.lineTo(margin.left + plotW, y);
        ctxBg2.stroke();
        ctxBg2.fillText(val + '℃', margin.left - 8, y);
    }});

    const yOpt = margin.top + plotH * (1.0 - (22.5 - yMin2) / (yMax2 - yMin2));
    ctxBg2.save();
    ctxBg2.setLineDash([3, 3]);
    ctxBg2.strokeStyle = '#00e5ff';
    ctxBg2.beginPath();
    ctxBg2.moveTo(margin.left, yOpt);
    ctxBg2.lineTo(margin.left + plotW, yOpt);
    ctxBg2.stroke();
    ctxBg2.fillStyle = '#00e5ff';
    ctxBg2.textAlign = 'left';
    ctxBg2.fillText('最適生長點 22.5℃', margin.left + 8, yOpt - 7);
    ctxBg2.restore();

    ctxBg2.textAlign = 'center';
    ctxBg2.textBaseline = 'top';

    if (isCurves) {{
        const lMin = 0.6, lMax = 1.6;
        const lTicks = [0.6, 0.8, 1.0, 1.2, 1.4, 1.6];
        lTicks.forEach(lv => {{
            const x = margin.left + plotW * ((lv - lMin) / (lMax - lMin));
            ctxBg2.beginPath();
            ctxBg2.moveTo(x, margin.top);
            ctxBg2.lineTo(x, margin.top + plotH);
            ctxBg2.stroke();
            ctxBg2.fillText(lv.toFixed(1), x, margin.top + plotH + 8);
        }});
        const x1 = margin.left + plotW * ((1.0 - lMin) / (lMax - lMin));
        ctxBg2.save();
        ctxBg2.setLineDash([2, 4]);
        ctxBg2.strokeStyle = 'rgba(0, 229, 255, 0.25)';
        ctxBg2.beginPath();
        ctxBg2.moveTo(x1, margin.top);
        ctxBg2.lineTo(x1, margin.top + plotH);
        ctxBg2.stroke();
        ctxBg2.restore();

        ctxBg2.fillStyle = '#00e5ff';
        ctxBg2.font = '11px "Plus Jakarta Sans", sans-serif';
        ctxBg2.fillText('太陽光度 L (Luminosity)', margin.left + plotW / 2, margin.top + plotH + 24);
    }} else {{
        const xMax = state.itera * state.dt;
        const xStep = Math.max(2, Math.round(xMax / 6));
        for (let xVal = 0; xVal <= xMax; xVal += xStep) {{
            const x = margin.left + plotW * (xVal / xMax);
            ctxBg2.beginPath();
            ctxBg2.moveTo(x, margin.top);
            ctxBg2.lineTo(x, margin.top + plotH);
            ctxBg2.stroke();
            ctxBg2.fillText(xVal, x, margin.top + plotH + 8);
        }}
        ctxBg2.fillStyle = '#64748b';
        ctxBg2.fillText('演化時間 (Time Steps)', margin.left + plotW / 2, margin.top + plotH + 24);
    }}

    ctxBg2.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctxBg2.strokeRect(margin.left, margin.top, plotW, plotH);
}}

function renderDynamicTraces() {{
    if (!state.simData) return;

    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;
    const d = state.simData;
    const isCurves = state.chartView === 'curves';

    if (isCurves) {{
        const lMin = 0.6, lMax = 1.6;
        const pts = state.recordedPoints;

        // Chart 1: Coverages vs L
        ctxFg1.clearRect(0, 0, width, height);
        ctxFg1.save();
        ctxFg1.beginPath();
        ctxFg1.rect(margin.left, margin.top, plotW, plotH);
        ctxFg1.clip();

        if (pts.length > 0) {{
            // Bare ground
            ctxFg1.strokeStyle = '#d97706';
            ctxFg1.lineWidth = 1.8;
            ctxFg1.setLineDash([4, 3]);
            ctxFg1.beginPath();
            pts.forEach((p, i) => {{
                const x = margin.left + plotW * ((p.l - lMin) / (lMax - lMin));
                const y = margin.top + plotH * (1.0 - p.au);
                if (i === 0) ctxFg1.moveTo(x, y); else ctxFg1.lineTo(x, y);
            }});
            ctxFg1.stroke();
            ctxFg1.setLineDash([]);

            // Grey Daisy
            ctxFg1.shadowBlur = 6;
            ctxFg1.shadowColor = '#94a3b8';
            ctxFg1.strokeStyle = '#94a3b8';
            ctxFg1.lineWidth = 2.8;
            ctxFg1.beginPath();
            pts.forEach((p, i) => {{
                const x = margin.left + plotW * ((p.l - lMin) / (lMax - lMin));
                const y = margin.top + plotH * (1.0 - p.ag);
                if (i === 0) ctxFg1.moveTo(x, y); else ctxFg1.lineTo(x, y);
            }});
            ctxFg1.stroke();

            // Black Daisy
            ctxFg1.shadowBlur = 6;
            ctxFg1.shadowColor = '#475569';
            ctxFg1.strokeStyle = '#475569';
            ctxFg1.lineWidth = 2.6;
            ctxFg1.beginPath();
            pts.forEach((p, i) => {{
                const x = margin.left + plotW * ((p.l - lMin) / (lMax - lMin));
                const y = margin.top + plotH * (1.0 - p.ab);
                if (i === 0) ctxFg1.moveTo(x, y); else ctxFg1.lineTo(x, y);
            }});
            ctxFg1.stroke();

            // White Daisy
            ctxFg1.shadowBlur = 8;
            ctxFg1.shadowColor = '#ffffff';
            ctxFg1.strokeStyle = '#f8fafc';
            ctxFg1.lineWidth = 3.0;
            ctxFg1.beginPath();
            pts.forEach((p, i) => {{
                const x = margin.left + plotW * ((p.l - lMin) / (lMax - lMin));
                const y = margin.top + plotH * (1.0 - p.aw);
                if (i === 0) ctxFg1.moveTo(x, y); else ctxFg1.lineTo(x, y);
            }});
            ctxFg1.stroke();
            ctxFg1.shadowBlur = 0;

            // Dots
            pts.forEach(p => {{
                const x = margin.left + plotW * ((p.l - lMin) / (lMax - lMin));
                ctxFg1.fillStyle = '#94a3b8';
                ctxFg1.beginPath();
                ctxFg1.arc(x, margin.top + plotH * (1.0 - p.ag), 2.5, 0, Math.PI * 2);
                ctxFg1.fill();

                ctxFg1.fillStyle = '#f8fafc';
                ctxFg1.beginPath();
                ctxFg1.arc(x, margin.top + plotH * (1.0 - p.aw), 2.5, 0, Math.PI * 2);
                ctxFg1.fill();

                ctxFg1.fillStyle = '#475569';
                ctxFg1.beginPath();
                ctxFg1.arc(x, margin.top + plotH * (1.0 - p.ab), 2.5, 0, Math.PI * 2);
                ctxFg1.fill();

                ctxFg1.fillStyle = '#d97706';
                ctxFg1.beginPath();
                ctxFg1.arc(x, margin.top + plotH * (1.0 - p.au), 2.0, 0, Math.PI * 2);
                ctxFg1.fill();
            }});
        }}

        // Cursor line
        const xCur1 = margin.left + plotW * ((state.l_val - lMin) / (lMax - lMin));
        if (xCur1 >= margin.left && xCur1 <= margin.left + plotW) {{
            ctxFg1.save();
            ctxFg1.setLineDash([3, 3]);
            ctxFg1.strokeStyle = '#00e5ff';
            ctxFg1.lineWidth = 1.5;
            ctxFg1.beginPath();
            ctxFg1.moveTo(xCur1, margin.top);
            ctxFg1.lineTo(xCur1, margin.top + plotH);
            ctxFg1.stroke();
            ctxFg1.restore();

            const yCurG = margin.top + plotH * (1.0 - d.finalAg);
            const yCurW = margin.top + plotH * (1.0 - d.finalAw);
            const yCurB = margin.top + plotH * (1.0 - d.finalAb);
            const yCurU = margin.top + plotH * (1.0 - d.finalAu);
            ctxFg1.fillStyle = '#00e5ff';
            [yCurG, yCurW, yCurB, yCurU].forEach(yPos => {{
                ctxFg1.beginPath();
                ctxFg1.arc(xCur1, yPos, 4.0, 0, Math.PI * 2);
                ctxFg1.fill();
            }});
        }}
        ctxFg1.restore();

        // Chart 2: Temperature vs L
        ctxFg2.clearRect(0, 0, width, height);
        const yMin2 = 0.0, yMax2 = 50.0;
        ctxFg2.save();
        ctxFg2.beginPath();
        ctxFg2.rect(margin.left, margin.top, plotW, plotH);
        ctxFg2.clip();

        if (pts.length > 0) {{
            // Abiotic Baseline
            ctxFg2.strokeStyle = '#ef4444';
            ctxFg2.lineWidth = 2.0;
            ctxFg2.setLineDash([5, 4]);
            ctxFg2.beginPath();
            pts.forEach((p, i) => {{
                const x = margin.left + plotW * ((p.l - lMin) / (lMax - lMin));
                const y = margin.top + plotH * (1.0 - (p.Tnobio - yMin2) / (yMax2 - yMin2));
                if (i === 0) ctxFg2.moveTo(x, y); else ctxFg2.lineTo(x, y);
            }});
            ctxFg2.stroke();
            ctxFg2.setLineDash([]);

            // Regulated Temperature
            ctxFg2.shadowBlur = 10;
            ctxFg2.shadowColor = '#22c55e';
            ctxFg2.strokeStyle = '#22c55e';
            ctxFg2.lineWidth = 3.2;
            ctxFg2.beginPath();
            pts.forEach((p, i) => {{
                const x = margin.left + plotW * ((p.l - lMin) / (lMax - lMin));
                const y = margin.top + plotH * (1.0 - (p.Tp - yMin2) / (yMax2 - yMin2));
                if (i === 0) ctxFg2.moveTo(x, y); else ctxFg2.lineTo(x, y);
            }});
            ctxFg2.stroke();
            ctxFg2.shadowBlur = 0;

            // Dots
            pts.forEach(p => {{
                const x = margin.left + plotW * ((p.l - lMin) / (lMax - lMin));
                ctxFg2.fillStyle = '#ef4444';
                ctxFg2.beginPath();
                ctxFg2.arc(x, margin.top + plotH * (1.0 - (p.Tnobio - yMin2) / (yMax2 - yMin2)), 2.5, 0, Math.PI * 2);
                ctxFg2.fill();

                ctxFg2.fillStyle = '#22c55e';
                ctxFg2.beginPath();
                ctxFg2.arc(x, margin.top + plotH * (1.0 - (p.Tp - yMin2) / (yMax2 - yMin2)), 3.5, 0, Math.PI * 2);
                ctxFg2.fill();
            }});
        }}

        const xCur2 = margin.left + plotW * ((state.l_val - lMin) / (lMax - lMin));
        if (xCur2 >= margin.left && xCur2 <= margin.left + plotW) {{
            ctxFg2.save();
            ctxFg2.setLineDash([3, 3]);
            ctxFg2.strokeStyle = '#00e5ff';
            ctxFg2.lineWidth = 1.5;
            ctxFg2.beginPath();
            ctxFg2.moveTo(xCur2, margin.top);
            ctxFg2.lineTo(xCur2, margin.top + plotH);
            ctxFg2.stroke();
            ctxFg2.restore();

            const yCurTp = margin.top + plotH * (1.0 - (d.finalTp - yMin2) / (yMax2 - yMin2));
            const yCurDead = margin.top + plotH * (1.0 - (d.Tnobio - yMin2) / (yMax2 - yMin2));
            ctxFg2.fillStyle = '#00e5ff';
            ctxFg2.shadowBlur = 8;
            ctxFg2.shadowColor = '#00e5ff';
            ctxFg2.beginPath();
            ctxFg2.arc(xCur2, yCurTp, 5.5, 0, Math.PI * 2);
            ctxFg2.fill();
            ctxFg2.beginPath();
            ctxFg2.arc(xCur2, yCurDead, 4.0, 0, Math.PI * 2);
            ctxFg2.fill();
            ctxFg2.shadowBlur = 0;
        }}
        ctxFg2.restore();

    }} else {{
        // Timeseries mode
        const xMax = state.itera * state.dt;

        // Chart 1
        ctxFg1.clearRect(0, 0, width, height);
        ctxFg1.save();
        ctxFg1.beginPath();
        ctxFg1.rect(margin.left, margin.top, plotW, plotH);
        ctxFg1.clip();

        // Bare ground
        ctxFg1.strokeStyle = '#d97706';
        ctxFg1.lineWidth = 1.8;
        ctxFg1.setLineDash([4, 3]);
        ctxFg1.beginPath();
        for (let i = 0; i < d.t.length; i++) {{
            const x = margin.left + plotW * (d.t[i] / xMax);
            const y = margin.top + plotH * (1.0 - d.au[i]);
            if (i === 0) ctxFg1.moveTo(x, y); else ctxFg1.lineTo(x, y);
        }}
        ctxFg1.stroke();
        ctxFg1.setLineDash([]);

        // Grey Daisy
        ctxFg1.shadowBlur = 6;
        ctxFg1.shadowColor = '#94a3b8';
        ctxFg1.strokeStyle = '#94a3b8';
        ctxFg1.lineWidth = 2.8;
        ctxFg1.beginPath();
        for (let i = 0; i < d.t.length; i++) {{
            const x = margin.left + plotW * (d.t[i] / xMax);
            const y = margin.top + plotH * (1.0 - d.ag[i]);
            if (i === 0) ctxFg1.moveTo(x, y); else ctxFg1.lineTo(x, y);
        }}
        ctxFg1.stroke();

        // Black Daisy
        ctxFg1.shadowBlur = 6;
        ctxFg1.shadowColor = '#475569';
        ctxFg1.strokeStyle = '#475569';
        ctxFg1.lineWidth = 2.6;
        ctxFg1.beginPath();
        for (let i = 0; i < d.t.length; i++) {{
            const x = margin.left + plotW * (d.t[i] / xMax);
            const y = margin.top + plotH * (1.0 - d.ab[i]);
            if (i === 0) ctxFg1.moveTo(x, y); else ctxFg1.lineTo(x, y);
        }}
        ctxFg1.stroke();

        // White Daisy
        ctxFg1.shadowBlur = 8;
        ctxFg1.shadowColor = '#ffffff';
        ctxFg1.strokeStyle = '#f8fafc';
        ctxFg1.lineWidth = 3.0;
        ctxFg1.beginPath();
        for (let i = 0; i < d.t.length; i++) {{
            const x = margin.left + plotW * (d.t[i] / xMax);
            const y = margin.top + plotH * (1.0 - d.aw[i]);
            if (i === 0) ctxFg1.moveTo(x, y); else ctxFg1.lineTo(x, y);
        }}
        ctxFg1.stroke();
        ctxFg1.restore();

        // Chart 2
        ctxFg2.clearRect(0, 0, width, height);
        const yMin2 = 0.0, yMax2 = 50.0;
        ctxFg2.save();
        ctxFg2.beginPath();
        ctxFg2.rect(margin.left, margin.top, plotW, plotH);
        ctxFg2.clip();

        const yDead = margin.top + plotH * (1.0 - (d.Tnobio - yMin2) / (yMax2 - yMin2));
        ctxFg2.setLineDash([5, 4]);
        ctxFg2.strokeStyle = '#ef4444';
        ctxFg2.lineWidth = 2.0;
        ctxFg2.beginPath();
        ctxFg2.moveTo(margin.left, yDead);
        ctxFg2.lineTo(margin.left + plotW, yDead);
        ctxFg2.stroke();
        ctxFg2.setLineDash([]);

        // Grey daisy local temp
        ctxFg2.setLineDash([3, 3]);
        ctxFg2.strokeStyle = '#94a3b8';
        ctxFg2.lineWidth = 1.8;
        ctxFg2.beginPath();
        for (let i = 0; i < d.t.length; i++) {{
            const x = margin.left + plotW * (d.t[i] / xMax);
            const y = margin.top + plotH * (1.0 - (d.Tg[i] - yMin2) / (yMax2 - yMin2));
            if (i === 0) ctxFg2.moveTo(x, y); else ctxFg2.lineTo(x, y);
        }}
        ctxFg2.stroke();
        ctxFg2.setLineDash([]);

        // Planet temp
        ctxFg2.shadowBlur = 8;
        ctxFg2.shadowColor = '#22c55e';
        ctxFg2.strokeStyle = '#22c55e';
        ctxFg2.lineWidth = 3.2;
        ctxFg2.beginPath();
        for (let i = 0; i < d.t.length; i++) {{
            const x = margin.left + plotW * (d.t[i] / xMax);
            const y = margin.top + plotH * (1.0 - (d.Tp[i] - yMin2) / (yMax2 - yMin2));
            if (i === 0) ctxFg2.moveTo(x, y); else ctxFg2.lineTo(x, y);
        }}
        ctxFg2.stroke();
        ctxFg2.restore();
    }}

    // Update Stats
    statTp.innerText = d.finalTp.toFixed(2) + ' ℃';
    statAg.innerText = (d.finalAg * 100).toFixed(1) + ' %';
    statTg.innerText = '局地溫: ' + d.finalTg.toFixed(1) + ' ℃';
    statAw.innerText = (d.finalAw * 100).toFixed(1) + ' %';
    statTw.innerText = '局地溫: ' + d.finalTw.toFixed(1) + ' ℃';
    statAb.innerText = (d.finalAb * 100).toFixed(1) + ' %';
    statTb.innerText = '局地溫: ' + d.finalTb.toFixed(1) + ' ℃';

    if (d.finalAg > 0.05 && (d.finalAw > 0.02 || d.finalAb > 0.02)) {{
        statGaeaEval.innerText = '🌿 灰雛菊大繁盛 (三物種穩定競爭)';
        statTp.style.color = '#22c55e';
    }} else if (d.finalAw <= 0.015 && d.finalAb <= 0.015 && d.finalAg <= 0.015) {{
        statGaeaEval.innerText = '💀 生態崩潰：雛菊全數滅絕 (死星態)';
        statTp.style.color = '#ef4444';
    }} else {{
        statGaeaEval.innerText = '⚡ 邊緣調節或兩物種偏勝';
        statTp.style.color = '#f59e0b';
    }}
}}

// 60 FPS Animation Loop
let animFrameId = null;

function animationStep() {{
    if (!state.isPlaying) return;

    const speed = parseFloat(numAnimSpeed.value) || 0.003;
    const target = selAnimTarget.value;
    const dirMode = selAnimDir.value;

    let minV = 0.5, maxV = 1.8;
    if (target === 'l_val') {{ minV = 0.5; maxV = 1.8; }}
    else if (target === 'alpha_g') {{ minV = 0.35; maxV = 0.65; }}
    else if (target === 'gamma_val') {{ minV = 0.05; maxV = 0.5; }}
    else if (target === 'alpha_w') {{ minV = 0.5; maxV = 0.9; }}
    else if (target === 'alpha_b') {{ minV = 0.1; maxV = 0.45; }}
    else if (target === 'alpha_u') {{ minV = 0.2; maxV = 0.8; }}
    else if (target === 'q_val') {{ minV = 5.0; maxV = 40.0; }}
    else if (target === 'ag_init') {{ minV = 0.001; maxV = 0.45; }}
    else if (target === 'aw_init') {{ minV = 0.001; maxV = 0.45; }}
    else if (target === 'ab_init') {{ minV = 0.001; maxV = 0.45; }}

    let curVal = state[target];

    if (dirMode === 'pingpong') {{
        curVal += state.pingPongDir * speed;
        if (curVal >= maxV) {{ curVal = maxV; state.pingPongDir = -1; }}
        else if (curVal <= minV) {{ curVal = minV; state.pingPongDir = 1; }}
    }} else if (dirMode === 'inc') {{
        curVal += speed;
        if (curVal >= maxV) {{ curVal = maxV; togglePlay(); }}
    }} else if (dirMode === 'dec') {{
        curVal -= speed;
        if (curVal <= minV) {{ curVal = minV; togglePlay(); }}
    }}

    state[target] = curVal;
    syncControls(target, curVal);

    runSimulation();
    renderDynamicTraces();
    if (isRecording) updateRecordFrame();

    animFrameId = requestAnimationFrame(animationStep);
}}

function syncControls(target, val) {{
    if (target === 'l_val') {{
        sliderL.value = val; numL.value = val.toFixed(2);
    }} else if (target === 'alpha_g') {{
        sliderAg.value = val; numAg.value = val.toFixed(2);
    }} else if (target === 'gamma_val') {{
        sliderGamma.value = val; numGamma.value = val.toFixed(2);
    }} else if (target === 'alpha_w') {{
        sliderAw.value = val; numAw.value = val.toFixed(2);
    }} else if (target === 'alpha_b') {{
        sliderAb.value = val; numAb.value = val.toFixed(2);
    }} else if (target === 'alpha_u') {{
        sliderAu.value = val; numAu.value = val.toFixed(2);
    }} else if (target === 'q_val') {{
        sliderQ.value = val; numQ.value = val.toFixed(1);
    }} else if (target === 'ag_init') {{
        sliderAgInit.value = val; numAgInit.value = val.toFixed(3);
    }} else if (target === 'aw_init') {{
        sliderAwInit.value = val; numAwInit.value = val.toFixed(3);
    }} else if (target === 'ab_init') {{
        sliderAbInit.value = val; numAbInit.value = val.toFixed(3);
    }}
}}

function togglePlay() {{
    state.isPlaying = !state.isPlaying;
    if (state.isPlaying) {{
        btnTogglePlay.innerText = '⏸️ 暫停動態演變';
        btnTogglePlay.style.background = 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)';
        animFrameId = requestAnimationFrame(animationStep);
    }} else {{
        btnTogglePlay.innerText = '▶️ 開始動態演變';
        btnTogglePlay.style.background = 'linear-gradient(135deg, #00e5ff 0%, #0284c7 100%)';
        if (animFrameId) cancelAnimationFrame(animFrameId);
    }}
}}

function bindSync(slider, numInput, stateKey) {{
    slider.addEventListener('input', e => {{
        const v = parseFloat(e.target.value);
        numInput.value = v;
        state[stateKey] = v;
        runSimulation();
        renderDynamicTraces();
    }});

    const updateFromNum = e => {{
        const v = parseFloat(e.target.value);
        if (!isNaN(v)) {{
            slider.value = v;
            state[stateKey] = v;
            runSimulation();
            renderDynamicTraces();
        }}
    }};
    numInput.addEventListener('input', updateFromNum);
    numInput.addEventListener('change', updateFromNum);
}}

bindSync(sliderL, numL, 'l_val');
bindSync(sliderAg, numAg, 'alpha_g');
bindSync(sliderAw, numAw, 'alpha_w');
bindSync(sliderAb, numAb, 'alpha_b');
bindSync(sliderGamma, numGamma, 'gamma_val');
bindSync(sliderQ, numQ, 'q_val');

bindSync(sliderAgInit, numAgInit, 'ag_init');
bindSync(sliderAwInit, numAwInit, 'aw_init');
bindSync(sliderAbInit, numAbInit, 'ab_init');
bindSync(sliderAu, numAu, 'alpha_u');
bindSync(sliderDt, numDt, 'dt');
bindSync(sliderItera, numItera, 'itera');

btnTogglePlay.addEventListener('click', togglePlay);

// Physics switch
selPhysicsMode.addEventListener('change', e => {{
    state.physicsMode = e.target.value;
    if (state.physicsMode === 'stull') {{
        state.s0 = 1368.0;
        physicsModeBadge.innerHTML = '🌍 Stull (2000)：S₀=1368 W/m² + 單層溫室效應 (T_s⁴ = 2T_e⁴) + 水平傳輸 Tr=0.6。在現代地球溫室下觀察灰雛菊競爭！';
        physicsModeBadge.style.borderLeftColor = '#22c55e';
    }} else {{
        state.s0 = 917.0;
        physicsModeBadge.innerHTML = '🌻 Lovelock (1983)：S₀=917 W/m² (等效無大氣單一常數，光度 L=1.0 正處於三物種共存恆溫區)。';
        physicsModeBadge.style.borderLeftColor = '#00e5ff';
    }}
    runSimulation();
    renderDynamicTraces();
}});

// Export High-Res PNG Snapshot
function exportSnapshotPng() {{
    const dpr = window.devicePixelRatio || 1;
    const pad = 24;
    const headerH = 65;
    const totalW = width * 2 + pad * 3;
    const totalH = height + headerH + pad * 2;

    const outCv = document.createElement('canvas');
    outCv.width = totalW * dpr;
    outCv.height = totalH * dpr;
    outCv.style.width = totalW + 'px';
    outCv.style.height = totalH + 'px';
    const ctx = outCv.getContext('2d');
    ctx.scale(dpr, dpr);

    ctx.fillStyle = '#0b1120';
    ctx.fillRect(0, 0, totalW, totalH);

    ctx.font = 'bold 18px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = '#00e5ff';
    const modeName = state.physicsMode === 'stull' ? 'Wisconsin Stull (2000) 溫室大氣模式' : 'Lovelock (1983) 等效無大氣模式';
    ctx.fillText(`Daisyworld 0D 灰雛菊三物種世界實測 - [${{modeName}}]`, pad, pad + 18);

    ctx.font = '12px "JetBrains Mono", monospace';
    ctx.fillStyle = '#94a3b8';
    ctx.fillText(`光度 L: ${{state.l_val.toFixed(2)}} | Tp: ${{state.simData.finalTp.toFixed(2)}}℃ | 死星基線: ${{state.simData.Tnobio.toFixed(1)}}℃ | 灰: ${{(state.simData.finalAg*100).toFixed(1)}}% | 白: ${{(state.simData.finalAw*100).toFixed(1)}}% | 黑: ${{(state.simData.finalAb*100).toFixed(1)}}%`, pad, pad + 40);

    ctx.drawImage(bg1, pad, pad + headerH, width, height);
    ctx.drawImage(fg1, pad, pad + headerH, width, height);

    ctx.drawImage(bg2, pad * 2 + width, pad + headerH, width, height);
    ctx.drawImage(fg2, pad * 2 + width, pad + headerH, width, height);

    const link = document.createElement('a');
    link.download = `daisyworld_0d_grey_L${{state.l_val.toFixed(2)}}_${{state.physicsMode}}.png`;
    link.href = outCv.toDataURL('image/png');
    link.click();
}}

// Dynamic WebM Video Recording
let mediaRecorder = null;
let recordedChunks = [];
let isRecording = false;
let recordCanvas = null;
let recordCtx = null;

function initRecordCanvas() {{
    if (!recordCanvas) {{
        recordCanvas = document.createElement('canvas');
        recordCanvas.width = 1200;
        recordCanvas.height = 680;
        recordCtx = recordCanvas.getContext('2d');
    }}
}}

function updateRecordFrame() {{
    if (!isRecording || !recordCtx) return;
    recordCtx.fillStyle = '#0b1120';
    recordCtx.fillRect(0, 0, 1200, 680);

    recordCtx.fillStyle = '#00e5ff';
    recordCtx.font = 'bold 20px "Plus Jakarta Sans", sans-serif';
    recordCtx.fillText('Daisyworld Dynamic Evolution Lab (0D Grey - 3 Species)', 25, 35);
    recordCtx.fillStyle = '#94a3b8';
    recordCtx.font = '13px "JetBrains Mono", monospace';
    recordCtx.fillText(`L=${{state.l_val.toFixed(2)}} | Tp=${{state.simData.finalTp.toFixed(2)}}℃ | Ag=${{(state.simData.finalAg*100).toFixed(1)}}% | Aw=${{(state.simData.finalAw*100).toFixed(1)}}% | Ab=${{(state.simData.finalAb*100).toFixed(1)}}%`, 25, 60);

    if (cvPlanet) recordCtx.drawImage(cvPlanet, 1020, 10, 150, 150);

    recordCtx.drawImage(bg1, 20, 80, 560, 560);
    recordCtx.drawImage(fg1, 20, 80, 560, 560);

    recordCtx.drawImage(bg2, 600, 80, 560, 560);
    recordCtx.drawImage(fg2, 600, 80, 560, 560);
}}

function toggleRecordVideo() {{
    if (!isRecording) {{
        startRecording();
    }} else {{
        stopRecording();
    }}
}}

function startRecording() {{
    initRecordCanvas();
    updateRecordFrame();
    recordedChunks = [];

    let stream = null;
    try {{
        stream = recordCanvas.captureStream(30);
    }} catch(e) {{
        alert('當前瀏覽器環境不支援 captureStream 錄製。');
        return;
    }}

    let mimeType = 'video/webm;codecs=vp9';
    if (!MediaRecorder.isTypeSupported(mimeType)) {{
        mimeType = 'video/webm';
    }}

    try {{
        mediaRecorder = new MediaRecorder(stream, {{ mimeType }});
    }} catch(e) {{
        mediaRecorder = new MediaRecorder(stream);
    }}

    mediaRecorder.ondataavailable = e => {{
        if (e.data && e.data.size > 0) recordedChunks.push(e.data);
    }};

    mediaRecorder.onstop = () => {{
        const blob = new Blob(recordedChunks, {{ type: 'video/webm' }});
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.download = `daisyworld_0d_grey_dynamic_${{Date.now()}}.webm`;
        link.href = url;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }};

    mediaRecorder.start(100);
    isRecording = true;
    btnRecordVideo.innerText = '⏹️ 停止並下載動畫';
    btnRecordVideo.style.background = 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)';

    if (!state.isPlaying) togglePlay();
}}

function stopRecording() {{
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {{
        mediaRecorder.stop();
    }}
    isRecording = false;
    btnRecordVideo.innerText = '🎥 錄製動態';
    btnRecordVideo.style.background = '';
}}

// Clear & Export CSV
btnClearPoints.addEventListener('click', () => {{
    state.recordedPoints = [];
    updateTablePoints();
    renderDynamicTraces();
}});

btnExportCsv.addEventListener('click', exportPointsToCsv);
btnViewCurves.addEventListener('click', () => setChartView('curves'));
btnViewTimeseries.addEventListener('click', () => setChartView('timeseries'));

btnToggleAdv.addEventListener('click', () => {{
    const isHidden = advancedPanel.style.display === 'none';
    advancedPanel.style.display = isHidden ? 'block' : 'none';
    btnToggleAdv.style.background = isHidden ? 'rgba(0, 229, 255, 0.25)' : '';
    btnToggleAdv.innerText = isHidden ? '🔼 收合進階參數' : '⚙️ 進階參數';
}});

btnExportPng.addEventListener('click', exportSnapshotPng);
btnRecordVideo.addEventListener('click', toggleRecordVideo);

// Scenario Presets
selPreset.addEventListener('change', e => {{
    const p = e.target.value;
    if (p === 'standard') {{
        setParams({{ l: 1.0, gamma: 0.3, ag: 0.50, aw: 0.75, ab: 0.25 }});
    }} else if (p === 'mid_opt') {{
        setParams({{ l: 1.05, gamma: 0.3, ag: 0.50, aw: 0.75, ab: 0.25 }});
    }} else if (p === 'low_l') {{
        setParams({{ l: 0.75, gamma: 0.3, ag: 0.50, aw: 0.75, ab: 0.25 }});
    }} else if (p === 'high_l') {{
        setParams({{ l: 1.35, gamma: 0.3, ag: 0.50, aw: 0.75, ab: 0.25 }});
    }} else if (p === 'extreme_cold') {{
        setParams({{ l: 0.55, gamma: 0.3, ag: 0.50, aw: 0.75, ab: 0.25 }});
    }} else if (p === 'extreme_hot') {{
        setParams({{ l: 1.70, gamma: 0.3, ag: 0.50, aw: 0.75, ab: 0.25 }});
    }}
}});

function setParams(cfg) {{
    if (cfg.l !== undefined) {{ state.l_val = cfg.l; sliderL.value = cfg.l; numL.value = cfg.l; }}
    if (cfg.gamma !== undefined) {{ state.gamma_val = cfg.gamma; sliderGamma.value = cfg.gamma; numGamma.value = cfg.gamma; }}
    if (cfg.ag !== undefined) {{ state.alpha_g = cfg.ag; sliderAg.value = cfg.ag; numAg.value = cfg.ag; }}
    if (cfg.aw !== undefined) {{ state.alpha_w = cfg.aw; sliderAw.value = cfg.aw; numAw.value = cfg.aw; }}
    if (cfg.ab !== undefined) {{ state.alpha_b = cfg.ab; sliderAb.value = cfg.ab; numAb.value = cfg.ab; }}
    runSimulation();
    renderDynamicTraces();
}}

btnReset.addEventListener('click', () => {{
    selPreset.value = 'standard';
    setParams({{ l: 1.0, gamma: 0.3, ag: 0.50, aw: 0.75, ab: 0.25 }});
}});

// Tooltip on Chart 1
fg1.addEventListener('mousemove', e => {{
    const rect = fg1.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const plotW = width - margin.left - margin.right;
    if (mouseX >= margin.left && mouseX <= margin.left + plotW) {{
        if (state.chartView === 'curves') {{
            const lMin = 0.6, lMax = 1.6;
            const targetL = lMin + ((mouseX - margin.left) / plotW) * (lMax - lMin);
            let closest = null, minDist = 0.08;
            state.recordedPoints.forEach(p => {{
                const dist = Math.abs(p.l - targetL);
                if (dist < minDist) {{ minDist = dist; closest = p; }}
            }});
            if (closest) {{
                tooltip.style.display = 'block';
                tooltip.style.left = (e.clientX + 14) + 'px';
                tooltip.style.top = (e.clientY - 25) + 'px';
                tooltip.innerHTML = `<b style="color: #00e5ff;">平衡光度 L: ${{closest.l.toFixed(2)}}</b><br>灰雛菊: ${{(closest.ag * 100).toFixed(1)}}%<br>白雛菊: ${{(closest.aw * 100).toFixed(1)}}%<br>黑雛菊: ${{(closest.ab * 100).toFixed(1)}}%<br>裸地: ${{(closest.au * 100).toFixed(1)}}%`;
                return;
            }}
        }} else {{
            const normX = (mouseX - margin.left) / plotW;
            const idx = Math.min(state.itera, Math.max(0, Math.round(normX * state.itera)));
            const d = state.simData;
            if (d && d.t && d.t[idx] !== undefined) {{
                tooltip.style.display = 'block';
                tooltip.style.left = (e.clientX + 14) + 'px';
                tooltip.style.top = (e.clientY - 25) + 'px';
                tooltip.innerHTML = `時間: ${{d.t[idx].toFixed(1)}}<br>灰雛菊: ${{(d.ag[idx] * 100).toFixed(1)}}%<br>白雛菊: ${{(d.aw[idx] * 100).toFixed(1)}}%<br>黑雛菊: ${{(d.ab[idx] * 100).toFixed(1)}}%<br>裸地: ${{(d.au[idx] * 100).toFixed(1)}}%<br>均溫: ${{d.Tp[idx].toFixed(2)}}℃`;
                return;
            }}
        }}
    }}
    tooltip.style.display = 'none';
}});

fg1.addEventListener('mouseleave', () => {{
    tooltip.style.display = 'none';
}});

// Tooltip on Chart 2
fg2.addEventListener('mousemove', e => {{
    const rect = fg2.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const plotW = width - margin.left - margin.right;
    if (mouseX >= margin.left && mouseX <= margin.left + plotW) {{
        if (state.chartView === 'curves') {{
            const lMin = 0.6, lMax = 1.6;
            const targetL = lMin + ((mouseX - margin.left) / plotW) * (lMax - lMin);
            let closest = null, minDist = 0.08;
            state.recordedPoints.forEach(p => {{
                const dist = Math.abs(p.l - targetL);
                if (dist < minDist) {{ minDist = dist; closest = p; }}
            }});
            if (closest) {{
                tooltip.style.display = 'block';
                tooltip.style.left = (e.clientX + 14) + 'px';
                tooltip.style.top = (e.clientY - 25) + 'px';
                const diff = closest.Tp - closest.Tnobio;
                tooltip.innerHTML = `<b style="color: #00e5ff;">平衡光度 L: ${{closest.l.toFixed(2)}}</b><br>調控均溫: <span style="color:#22c55e;">${{closest.Tp.toFixed(2)}}℃</span><br>死星基線: <span style="color:#ef4444;">${{closest.Tnobio.toFixed(1)}}℃</span><br>調節溫差: ${{(diff >= 0 ? '+' : '')}}${{diff.toFixed(2)}}℃`;
                return;
            }}
        }} else {{
            const normX = (mouseX - margin.left) / plotW;
            const idx = Math.min(state.itera, Math.max(0, Math.round(normX * state.itera)));
            const d = state.simData;
            if (d && d.t && d.t[idx] !== undefined) {{
                tooltip.style.display = 'block';
                tooltip.style.left = (e.clientX + 14) + 'px';
                tooltip.style.top = (e.clientY - 25) + 'px';
                tooltip.innerHTML = `時間: ${{d.t[idx].toFixed(1)}}<br>行星均溫: ${{d.Tp[idx].toFixed(2)}}℃<br>灰雛菊局地: ${{d.Tg[idx].toFixed(2)}}℃<br>白雛菊局地: ${{d.Tw[idx].toFixed(2)}}℃<br>黑雛菊局地: ${{d.Tb[idx].toFixed(2)}}℃<br>死星基線: ${{d.Tnobio.toFixed(1)}}℃`;
                return;
            }}
        }}
    }}
    tooltip.style.display = 'none';
}});

fg2.addEventListener('mouseleave', () => {{
    tooltip.style.display = 'none';
}});

window.addEventListener('resize', resizeCanvases);
runSimulation();
setTimeout(resizeCanvases, 50);
</script>

</body>
</html>
"""
    return html_code
