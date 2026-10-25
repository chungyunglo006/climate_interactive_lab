"""
Interactive 60 FPS Client-Side Canvas Engine for 1D Latitudinal Grey Daisyworld (3 Species Spatial Competition).
Ensures coordinate axes, gridlines, and thresholds are rendered ONCE on a static layer,
while latitudinal daisy coverage and temperature profiles update smoothly via requestAnimationFrame at 60 FPS.
Includes synchronized sliders + direct numeric keyboard inputs and scenario presets.
"""

def get_interactive_daisy_grey_1d_html(
    s0=2100.0, l_val=1.0, alpha_w=0.75, alpha_b=0.25, alpha_g=0.50, alpha_u=0.5,
    q_val=20.0, gamma_val=0.3, k_diff=3.87, a_param=230.0, b_param=2.17, itera=150,
    ag_init=0.01, aw_init=0.01, ab_init=0.01, dt=0.10,
    physics_mode="atmosphere"
):
    """Generates self-contained 60 FPS hardware-accelerated interactive canvas HTML for 1D Grey Daisyworld."""
    opt_atmo_sel = "selected" if physics_mode == "atmosphere" else ""
    opt_airless_sel = "selected" if physics_mode == "airless" else ""
    badge_text = "🌍 地球溫室大氣模式：包含長波溫室效應與經向大氣熱輸送 (K)，三物種在全球與緯度生態位競爭。" if physics_mode == "atmosphere" else "🌻 無大氣模式 (如月球)：無大氣熱輸送 (K=0) 且無溫室效應，各緯度獨立進行純黑體輻射平衡，赤道酷熱、兩極極寒！"
    badge_border = "#22c55e" if physics_mode == "atmosphere" else "#00e5ff"
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
    color: #f8fafc;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.ctrl-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 14px 20px;
    align-items: center;
}}

.ctrl-item {{
    display: flex;
    flex-direction: column;
    gap: 6px;
}}

.ctrl-label {{
    font-size: 0.8rem;
    color: #94a3b8;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    display: flex;
    justify-content: space-between;
}}

.ctrl-input-row {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

input[type="range"] {{
    flex: 1;
    accent-color: #00e5ff;
    cursor: pointer;
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
}}

.val-input {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    font-weight: 600;
    color: #00e5ff;
    width: 85px;
    text-align: right;
    background: rgba(0, 229, 255, 0.08);
    padding: 4px 8px;
    border-radius: 6px;
    border: 1px solid rgba(0, 229, 255, 0.3);
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
    gap: 12px;
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    align-items: center;
}}

.btn {{
    background: linear-gradient(135deg, #00e5ff 0%, #0284c7 100%);
    color: #020617;
    border: none;
    padding: 8px 18px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.88rem;
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

select, input[type="number"].inline-input {{
    background: #0f172a;
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #f8fafc;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 0.85rem;
    outline: none;
}}

select:focus, input[type="number"].inline-input:focus {{
    border-color: #00e5ff;
}}

.stats-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 18px;
}}

@media (max-width: 800px) {{
    .stats-grid {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

.stat-card {{
    background: rgba(21, 28, 44, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 14px 16px;
    backdrop-filter: blur(8px);
}}

.stat-title {{
    font-size: 0.75rem;
    color: #94a3b8;
    font-weight: 600;
    text-transform: uppercase;
}}

.stat-val {{
    font-size: 1.45rem;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 4px;
    font-family: 'JetBrains Mono', monospace;
}}

.stat-sub {{
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 2px;
}}

.charts-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
}}

@media (max-width: 900px) {{
    .charts-grid {{
        grid-template-columns: 1fr;
    }}
}}

.chart-card {{
    background: rgba(15, 23, 42, 0.55);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 16px;
    position: relative;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}}

.chart-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}}

.chart-title {{
    font-size: 0.95rem;
    font-weight: 700;
    color: #f8fafc;
}}

.chart-legend {{
    display: flex;
    gap: 12px;
    font-size: 0.75rem;
}}

.legend-item {{
    display: flex;
    align-items: center;
    gap: 5px;
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
        <div class="panel-title">🌿 1D 緯度灰雛菊世界物理參數面板 (三物種空間競爭 - 滑桿 + 精確數值直接輸入)</div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 0.8rem; color: #94a3b8;">🎯 預設情境:</span>
            <select id="sel_preset">
                <option value="standard" selected>標準光度 (L = 1.0 - 灰雛菊在中緯度繁盛)</option>
                <option value="mid_opt">最適溫和太陽 (L = 1.05 - 灰雛菊大繁茂)</option>
                <option value="low_l">微弱太陽 (L = 0.75 - 黑雛菊主導保溫)</option>
                <option value="high_l">強烈太陽 (L = 1.30 - 白雛菊主導散熱)</option>
            </select>
        </div>
    </div>

    <div class="ctrl-grid">
        <div class="ctrl-item">
            <span class="ctrl-label"><span>太陽光度 L</span><span>相對光度</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_l" min="0.6" max="1.6" step="0.01" value="{l_val}">
                <input type="number" class="val-input" id="num_l" min="0.6" max="1.6" step="0.01" value="{l_val}">
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
            <span class="ctrl-label"><span>大氣熱擴散 K</span><span>W/m²/℃</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_k" min="0.5" max="8.0" step="0.1" value="{k_diff}">
                <input type="number" class="val-input" id="num_k" min="0.5" max="8.0" step="0.1" value="{k_diff}">
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
    </div>

    <div class="action-row">
        <button class="btn" id="btn_toggle_play">▶️ 開始動態演變</button>
        <button class="btn btn-secondary" id="btn_reset">🔄 重設標準光度</button>
        <button class="btn btn-secondary" id="btn_toggle_adv">⚙️ 進階參數</button>
        <button class="btn btn-secondary" id="btn_export_png">📸 截圖 PNG</button>
        <button class="btn btn-secondary" id="btn_record_video">🎥 錄製動態</button>

        <span style="color: #64748b; margin-left: 8px;">物理狀態:</span>
        <select id="sel_physics_mode">
            <option value="atmosphere" {opt_atmo_sel}>🌍 溫室大氣 + 經向熱擴散 (K=3.87)</option>
            <option value="airless" {opt_airless_sel}>🌻 無大氣純黑體輻射 (K=0 孤立緯度)</option>
        </select>

        <span style="color: #64748b; margin-left: 8px;">視角範圍:</span>
        <select id="sel_view_domain">
            <option value="global" selected>🌐 全球對稱 (85°S ~ 85°N)</option>
            <option value="north">🧭 北半球視角 (0° ~ 85°N)</option>
        </select>

        <span style="color: #64748b; margin-left: 8px;">演變變數:</span>
        <select id="sel_anim_target">
            <option value="l_val">太陽光度 L</option>
            <option value="alpha_g">灰雛菊反照率 α_g</option>
            <option value="k_diff">熱擴散係數 K</option>
            <option value="gamma_val">死亡率 γ</option>
        </select>

        <span style="color: #64748b;">方向:</span>
        <select id="sel_anim_dir">
            <option value="pingpong">來回擺動 (Ping-Pong)</option>
            <option value="inc">往大增加 (+)</option>
            <option value="dec">往小減少 (-)</option>
        </select>

        <span style="color: #64748b;">速率 (Δ/幀):</span>
        <input type="number" class="inline-input" id="num_anim_speed" value="0.002" step="0.001" min="0.0005" max="0.03" style="width: 85px;">
    </div>

    
    <!-- Advanced Experimental Parameters Collapsible Panel -->
    <div id="advanced_panel" style="display: none; margin-top: 14px; padding: 14px 18px; background: rgba(15, 23, 42, 0.7); border: 1px dashed rgba(0, 229, 255, 0.35); border-radius: 10px;">
        <div style="font-size: 0.82rem; font-weight: 700; color: #00e5ff; margin-bottom: 12px;">⚙️ 進階實驗變數面板 (三物種初始覆蓋率、裸地反照率與步長參數微調)</div>
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

<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-title">雛菊調節全球均溫</div>
        <div class="stat-val" id="stat_mean_t" style="color: #22c55e;">-- ℃</div>
        <div class="stat-sub" id="stat_gaea_eval">三物種生態評估中...</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">死星對照全球均溫</div>
        <div class="stat-val" id="stat_dead_t" style="color: #ef4444;">-- ℃</div>
        <div class="stat-sub" id="stat_diff_t">溫差: -- ℃</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">灰雛菊中緯度覆蓋率</div>
        <div class="stat-val" id="stat_ag_mid" style="color: #94a3b8;">-- %</div>
        <div class="stat-sub">中緯度生態席位</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">赤道白 / 極區黑覆蓋率</div>
        <div class="stat-val" id="stat_wb_ratio" style="font-size: 1.15rem; color: #f8fafc;">--</div>
        <div class="stat-sub">白(6°N) / 黑(85°N)</div>
    </div>
</div>

<div class="charts-grid">
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">🌿 各緯度三物種空間平衡分佈</div>
            <div class="chart-legend">
                <div class="legend-item"><div class="legend-color" style="background: #f8fafc;"></div> 白雛菊</div>
                <div class="legend-item"><div class="legend-color" style="background: #475569;"></div> 黑雛菊</div>
                <div class="legend-item"><div class="legend-color" style="background: #94a3b8; border-top: 1px dashed;"></div> 灰雛菊</div>
                <div class="legend-item"><div class="legend-color" style="background: #d97706; border-top: 1px dotted;"></div> 裸地</div>
            </div>
        </div>
        <div class="canvas-container" id="container1">
            <canvas id="bg1"></canvas>
            <canvas id="fg1"></canvas>
        </div>
    </div>

    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">🌡️ 各緯度溫度剖面對比 (含灰生態系 vs 死星基線)</div>
            <div class="chart-legend">
                <div class="legend-item"><div class="legend-color" style="background: #22c55e;"></div> 三物種剖面</div>
                <div class="legend-item"><div class="legend-color" style="background: #ef4444; border-top: 1px dashed;"></div> 死星對照剖面</div>
                <div class="legend-item"><div class="legend-color" style="background: #00e5ff; border-top: 1px dotted;"></div> 最適 22.5℃</div>
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
const LATS_1D = [85.0, 75.0, 65.0, 55.0, 45.0, 35.0, 25.0, 15.0, 6.0];
const SUNWT_1D = [0.5, 0.531, 0.624, 0.77, 0.892, 1.021, 1.12, 1.189, 1.219];
const latCos = LATS_1D.map(l => Math.cos(l * Math.PI / 180.0));
const sumCos = latCos.reduce((a, b) => a + b, 0);

// Monotonic global coordinates [-85 to +85]
const fullLats = [];
for (let i = 0; i < LATS_1D.length; i++) fullLats.push(-LATS_1D[i]);
for (let i = LATS_1D.length - 1; i >= 0; i--) fullLats.push(LATS_1D[i]);

// Northern hemisphere only [6 to 85]
const northLats = [];
for (let i = LATS_1D.length - 1; i >= 0; i--) northLats.push(LATS_1D[i]);

let state = {{
    s0: {s0},
    l_val: {l_val},
    alpha_w: {alpha_w},
    alpha_b: {alpha_b},
    alpha_g: {alpha_g},
    alpha_u: {alpha_u},
    q_val: {q_val},
    gamma_val: {gamma_val},
    k_diff: {k_diff},
    a_param: {a_param},
    b_param: {b_param},
    itera: {itera},
    physicsMode: '{physics_mode}',
    viewDomain: 'global',
    isPlaying: false,
    pingPongDir: 1,
    simData: null
}};

// DOM Elements
const selPhysicsMode = document.getElementById('sel_physics_mode');
const physicsModeBadge = document.getElementById('physics_mode_badge');
const selViewDomain = document.getElementById('sel_view_domain');
const sliderL = document.getElementById('slider_l');
const numL = document.getElementById('num_l');
const sliderAg = document.getElementById('slider_ag');
const numAg = document.getElementById('num_ag');
const sliderK = document.getElementById('slider_k');
const numK = document.getElementById('num_k');
const sliderAw = document.getElementById('slider_aw');
const numAw = document.getElementById('num_aw');
const sliderAb = document.getElementById('slider_ab');
const numAb = document.getElementById('num_ab');
const sliderGamma = document.getElementById('slider_gamma');
const numGamma = document.getElementById('num_gamma');
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

const statMeanT = document.getElementById('stat_mean_t');
const statGaeaEval = document.getElementById('stat_gaea_eval');
const statDeadT = document.getElementById('stat_dead_t');
const statDiffT = document.getElementById('stat_diff_t');
const statAgMid = document.getElementById('stat_ag_mid');
const statWbRatio = document.getElementById('stat_wb_ratio');

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

function runSimulation() {{
    const nLat = LATS_1D.length;
    const Rin = SUNWT_1D.map(wt => (state.s0 / 4.0) * state.l_val * wt);

    let aw = new Array(nLat).fill(0.01);
    let ab = new Array(nLat).fill(0.01);
    let ag = new Array(nLat).fill(0.01);
    let temp = new Array(nLat).fill(15.0);
    const dt = 0.1;

    for (let step = 0; step < state.itera; step++) {{
        let au = [];
        let alphaP = [];
        for (let i = 0; i < nLat; i++) {{
            const u = Math.max(0.0, Math.min(1.0, 1.0 - aw[i] - ab[i] - ag[i]));
            au.push(u);
            alphaP.push(aw[i] * state.alpha_w + ab[i] * state.alpha_b + ag[i] * state.alpha_g + u * state.alpha_u);
        }}

        // Temperature Calculation: Atmosphere vs Airless
        const isAirless = state.physicsMode === 'airless';
        if (!isAirless) {{
            for (let iter = 0; iter < 15; iter++) {{
                const meanT = temp.reduce((acc, t, i) => acc + t * latCos[i], 0) / sumCos;
                for (let i = 0; i < nLat; i++) {{
                    temp[i] = (Rin[i] * (1.0 - alphaP[i]) + state.k_diff * meanT - state.a_param) / (state.b_param + state.k_diff);
                }}
            }}
        }} else {{
            for (let i = 0; i < nLat; i++) {{
                const absorbed = Math.max(1.0, Rin[i] * (1.0 - alphaP[i]));
                temp[i] = Math.pow(absorbed / 5.670374e-8, 0.25) - 273.15;
            }}
        }}

        for (let i = 0; i < nLat; i++) {{
            const Tw = temp[i] + state.q_val * (alphaP[i] - state.alpha_w);
            const Tb = temp[i] + state.q_val * (alphaP[i] - state.alpha_b);
            const Tg = temp[i] + state.q_val * (alphaP[i] - state.alpha_g);

            const betaW = Math.max(0.0, 1.0 - 0.003265 * Math.pow(22.5 - Tw, 2));
            const betaB = Math.max(0.0, 1.0 - 0.003265 * Math.pow(22.5 - Tb, 2));
            const betaG = Math.max(0.0, 1.0 - 0.003265 * Math.pow(22.5 - Tg, 2));

            const daw = aw[i] * (au[i] * betaW - state.gamma_val);
            const dab = ab[i] * (au[i] * betaB - state.gamma_val);
            const dag = ag[i] * (au[i] * betaG - state.gamma_val);

            aw[i] = Math.max(0.001, Math.min(0.99, aw[i] + dt * daw));
            ab[i] = Math.max(0.001, Math.min(0.99, ab[i] + dt * dab));
            ag[i] = Math.max(0.001, Math.min(0.99, ag[i] + dt * dag));

            if (aw[i] + ab[i] + ag[i] > 0.99) {{
                const sc = 0.99 / (aw[i] + ab[i] + ag[i]);
                aw[i] *= sc; ab[i] *= sc; ag[i] *= sc;
            }}
        }}
    }}

    let tempNobio = new Array(nLat).fill(15.0);
    const isAirlessDead = state.physicsMode === 'airless';
    if (!isAirlessDead) {{
        for (let iter = 0; iter < 20; iter++) {{
            const meanDead = tempNobio.reduce((acc, t, i) => acc + t * latCos[i], 0) / sumCos;
            for (let i = 0; i < nLat; i++) {{
                tempNobio[i] = (Rin[i] * (1.0 - state.alpha_u) + state.k_diff * meanDead - state.a_param) / (state.b_param + state.k_diff);
            }}
        }}
    }} else {{
        for (let i = 0; i < nLat; i++) {{
            const absorbedDead = Math.max(1.0, Rin[i] * (1.0 - state.alpha_u));
            tempNobio[i] = Math.pow(absorbedDead / 5.670374e-8, 0.25) - 273.15;
        }}
    }}

    // Full symmetric arrays (Monotonic from South Pole -85 to North Pole +85)
    const fullTemp = [], fullDead = [], fullAw = [], fullAb = [], fullAg = [], fullAu = [];
    for (let i = 0; i < nLat; i++) {{
        fullTemp.push(temp[i]); fullDead.push(tempNobio[i]);
        fullAw.push(aw[i]); fullAb.push(ab[i]); fullAg.push(ag[i]); fullAu.push(1.0 - aw[i] - ab[i] - ag[i]);
    }}
    for (let i = nLat - 1; i >= 0; i--) {{
        fullTemp.push(temp[i]); fullDead.push(tempNobio[i]);
        fullAw.push(aw[i]); fullAb.push(ab[i]); fullAg.push(ag[i]); fullAu.push(1.0 - aw[i] - ab[i] - ag[i]);
    }}

    // Northern hemisphere only [6 to 85] (Equator to North Pole)
    const northTemp = [], northDead = [], northAw = [], northAb = [], northAg = [], northAu = [];
    for (let i = nLat - 1; i >= 0; i--) {{
        northTemp.push(temp[i]); northDead.push(tempNobio[i]);
        northAw.push(aw[i]); northAb.push(ab[i]); northAg.push(ag[i]); northAu.push(1.0 - aw[i] - ab[i] - ag[i]);
    }}

    const meanT = temp.reduce((acc, t, i) => acc + t * latCos[i], 0) / sumCos;
    const meanDead = tempNobio.reduce((acc, t, i) => acc + t * latCos[i], 0) / sumCos;

    state.simData = {{
        fullLats, fullTemp, fullDead, fullAw, fullAb, fullAg, fullAu,
        northLats, northTemp, northDead, northAw, northAb, northAg, northAu,
        meanT: meanT, meanDead: meanDead,
        agMid: ag[4], eqW: aw[nLat - 1], poleB: ab[0]
    }};
}}

function drawStaticBackgrounds() {{
    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;
    const isNorth = state.viewDomain === 'north';

    // --- Chart 1 Static BG (Coverage) ---
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

    const xTicks = isNorth ? [0, 15, 30, 45, 60, 75, 90] : [-90, -60, -30, 0, 30, 60, 90];
    ctxBg1.textAlign = 'center';
    ctxBg1.textBaseline = 'top';

    xTicks.forEach(lat => {{
        const x = isNorth ? (margin.left + plotW * (lat / 90.0)) : (margin.left + plotW * ((lat + 90.0) / 180.0));
        ctxBg1.beginPath();
        ctxBg1.moveTo(x, margin.top);
        ctxBg1.lineTo(x, margin.top + plotH);
        ctxBg1.stroke();
        const lbl = lat === 0 ? '赤道' : (lat > 0 ? lat + '°N' : Math.abs(lat) + '°S');
        ctxBg1.fillText(lbl, x, margin.top + plotH + 8);
    }});

    ctxBg1.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctxBg1.strokeRect(margin.left, margin.top, plotW, plotH);


    // --- Chart 2 Static BG (Temperature) ---
    ctxBg2.clearRect(0, 0, width, height);
    ctxBg2.fillStyle = 'rgba(15, 23, 42, 0.45)';
    ctxBg2.fillRect(margin.left, margin.top, plotW, plotH);

    const yMin2 = -40.0, yMax2 = 45.0;
    const yTicks2 = [-30, -15, 0, 15, 30, 45];

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
    ctxBg2.fillText('最適點 22.5℃', margin.left + 8, yOpt - 7);
    ctxBg2.restore();

    xTicks.forEach(lat => {{
        const x = isNorth ? (margin.left + plotW * (lat / 90.0)) : (margin.left + plotW * ((lat + 90.0) / 180.0));
        ctxBg2.beginPath();
        ctxBg2.moveTo(x, margin.top);
        ctxBg2.lineTo(x, margin.top + plotH);
        ctxBg2.stroke();
        const lbl = lat === 0 ? '赤道' : (lat > 0 ? lat + '°N' : Math.abs(lat) + '°S');
        ctxBg2.fillText(lbl, x, margin.top + plotH + 8);
    }});

    ctxBg2.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctxBg2.strokeRect(margin.left, margin.top, plotW, plotH);
}}

function renderDynamicTraces() {{
    if (!state.simData) return;

    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;
    const d = state.simData;
    const isNorth = state.viewDomain === 'north';
    const lats = isNorth ? d.northLats : d.fullLats;
    const awVals = isNorth ? d.northAw : d.fullAw;
    const abVals = isNorth ? d.northAb : d.fullAb;
    const agVals = isNorth ? d.northAg : d.fullAg;
    const auVals = isNorth ? d.northAu : d.fullAu;
    const tempVals = isNorth ? d.northTemp : d.fullTemp;
    const deadVals = isNorth ? d.northDead : d.fullDead;

    const getX = lat => isNorth ? (margin.left + plotW * (lat / 90.0)) : (margin.left + plotW * ((lat + 90.0) / 180.0));

    // --- Chart 1: Coverage Lines ---
    ctxFg1.clearRect(0, 0, width, height);
    ctxFg1.save();
    ctxFg1.beginPath();
    ctxFg1.rect(margin.left, margin.top, plotW, plotH);
    ctxFg1.clip();

    // 1. Bare Ground (Orange dash)
    ctxFg1.strokeStyle = '#d97706';
    ctxFg1.lineWidth = 1.6;
    ctxFg1.setLineDash([3, 3]);
    ctxFg1.beginPath();
    for (let i = 0; i < lats.length; i++) {{
        const x = getX(lats[i]);
        const y = margin.top + plotH * (1.0 - auVals[i]);
        if (i === 0) ctxFg1.moveTo(x, y);
        else ctxFg1.lineTo(x, y);
    }}
    ctxFg1.stroke();
    ctxFg1.setLineDash([]);

    // 2. Grey Daisy (Neutral Slate dash)
    ctxFg1.shadowBlur = 6;
    ctxFg1.shadowColor = '#94a3b8';
    ctxFg1.strokeStyle = '#94a3b8';
    ctxFg1.lineWidth = 2.5;
    ctxFg1.setLineDash([5, 4]);
    ctxFg1.beginPath();
    for (let i = 0; i < lats.length; i++) {{
        const x = getX(lats[i]);
        const y = margin.top + plotH * (1.0 - agVals[i]);
        if (i === 0) ctxFg1.moveTo(x, y);
        else ctxFg1.lineTo(x, y);
    }}
    ctxFg1.stroke();
    ctxFg1.setLineDash([]);

    // 3. Black Daisy (Polar species)
    ctxFg1.shadowBlur = 6;
    ctxFg1.shadowColor = '#475569';
    ctxFg1.strokeStyle = '#64748b';
    ctxFg1.lineWidth = 2.8;
    ctxFg1.beginPath();
    for (let i = 0; i < lats.length; i++) {{
        const x = getX(lats[i]);
        const y = margin.top + plotH * (1.0 - abVals[i]);
        if (i === 0) ctxFg1.moveTo(x, y);
        else ctxFg1.lineTo(x, y);
    }}
    ctxFg1.stroke();

    // 4. White Daisy (Equatorial species)
    ctxFg1.shadowBlur = 8;
    ctxFg1.shadowColor = '#ffffff';
    ctxFg1.strokeStyle = '#f8fafc';
    ctxFg1.lineWidth = 3.0;
    ctxFg1.beginPath();
    for (let i = 0; i < lats.length; i++) {{
        const x = getX(lats[i]);
        const y = margin.top + plotH * (1.0 - awVals[i]);
        if (i === 0) ctxFg1.moveTo(x, y);
        else ctxFg1.lineTo(x, y);
    }}
    ctxFg1.stroke();
    ctxFg1.restore();


    // --- Chart 2: Temperature Profile ---
    ctxFg2.clearRect(0, 0, width, height);
    const yMin2 = -40.0, yMax2 = 45.0;
    ctxFg2.save();
    ctxFg2.beginPath();
    ctxFg2.rect(margin.left, margin.top, plotW, plotH);
    ctxFg2.clip();

    // Abiotic Baseline (Red dash)
    ctxFg2.strokeStyle = '#ef4444';
    ctxFg2.lineWidth = 2.2;
    ctxFg2.setLineDash([5, 4]);
    ctxFg2.beginPath();
    for (let i = 0; i < lats.length; i++) {{
        const x = getX(lats[i]);
        const y = margin.top + plotH * (1.0 - (deadVals[i] - yMin2) / (yMax2 - yMin2));
        if (i === 0) ctxFg2.moveTo(x, y);
        else ctxFg2.lineTo(x, y);
    }}
    ctxFg2.stroke();
    ctxFg2.setLineDash([]);

    // Regulated Planet Temperature (Green)
    ctxFg2.shadowBlur = 8;
    ctxFg2.shadowColor = '#22c55e';
    ctxFg2.strokeStyle = '#22c55e';
    ctxFg2.lineWidth = 3.2;
    ctxFg2.beginPath();
    for (let i = 0; i < lats.length; i++) {{
        const x = getX(lats[i]);
        const y = margin.top + plotH * (1.0 - (tempVals[i] - yMin2) / (yMax2 - yMin2));
        if (i === 0) ctxFg2.moveTo(x, y);
        else ctxFg2.lineTo(x, y);
    }}
    ctxFg2.stroke();
    ctxFg2.restore();

    // Update Stats
    statMeanT.innerText = d.meanT.toFixed(2) + ' ℃';
    statDeadT.innerText = d.meanDead.toFixed(2) + ' ℃';
    const diff = d.meanT - d.meanDead;
    statDiffT.innerText = '調節淨溫差: ' + (diff >= 0 ? '+' : '') + diff.toFixed(2) + ' ℃';
    statAgMid.innerText = (d.agMid * 100).toFixed(1) + ' %';
    statWbRatio.innerText = (d.eqW * 100).toFixed(0) + '% / ' + (d.poleB * 100).toFixed(0) + '%';

    if (d.agMid > 0.15) {{
        statGaeaEval.innerText = '🩶 灰雛菊成功佔據中緯度溫和席位';
        statMeanT.style.color = '#38bdf8';
    }} else if (d.eqW > 0.20) {{
        statGaeaEval.innerText = '☀️ 高溫驅動全球白雛菊優勢';
        statMeanT.style.color = '#00e5ff';
    }} else if (d.poleB > 0.20) {{
        statGaeaEval.innerText = '❄️ 寒冷驅動全球黑雛菊優勢';
        statMeanT.style.color = '#f59e0b';
    }} else {{
        statGaeaEval.innerText = '💀 空間生態枯萎滅絕';
        statMeanT.style.color = '#ef4444';
    }}
}}

// 60 FPS Animation Loop
let animFrameId = null;

function animationStep() {{
    if (!state.isPlaying) return;

    const speed = parseFloat(numAnimSpeed.value) || 0.002;
    const target = selAnimTarget.value;
    const dirMode = selAnimDir.value;

    let minV = 0.6, maxV = 1.6;
    if (target === 'l_val') {{ minV = 0.6; maxV = 1.6; }}
    else if (target === 'alpha_g') {{ minV = 0.35; maxV = 0.65; }}
    else if (target === 'k_diff') {{ minV = 0.5; maxV = 8.0; }}
    else if (target === 'gamma_val') {{ minV = 0.05; maxV = 0.5; }}

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
    }} else if (target === 'k_diff') {{
        sliderK.value = val; numK.value = val.toFixed(1);
    }} else if (target === 'gamma_val') {{
        sliderGamma.value = val; numGamma.value = val.toFixed(2);
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
bindSync(sliderK, numK, 'k_diff');
bindSync(sliderAw, numAw, 'alpha_w');
bindSync(sliderAb, numAb, 'alpha_b');
bindSync(sliderGamma, numGamma, 'gamma_val');

btnTogglePlay.addEventListener('click', togglePlay);

selViewDomain.addEventListener('change', e => {{
    state.viewDomain = e.target.value;
    drawStaticBackgrounds();
    renderDynamicTraces();
}});

// Physics Mode Switch
if (selPhysicsMode) {{
    selPhysicsMode.addEventListener('change', e => {{
        state.physicsMode = e.target.value;
        if (state.physicsMode === 'atmosphere') {{
            if (physicsModeBadge) {{
                physicsModeBadge.innerHTML = '🌍 地球溫室大氣模式：包含長波溫室效應與經向大氣熱輸送 (K)，三物種在全球與緯度生態位競爭。';
                physicsModeBadge.style.borderLeftColor = '#22c55e';
            }}
        }} else {{
            if (physicsModeBadge) {{
                physicsModeBadge.innerHTML = '🌻 無大氣模式 (如月球)：無大氣熱輸送 (K=0) 且無溫室效應，各緯度獨立進行純黑體輻射平衡，赤道酷熱、兩極極寒！';
                physicsModeBadge.style.borderLeftColor = '#00e5ff';
            }}
        }}
        runSimulation();
        renderDynamicTraces();
    }});
}}

// Scenario Presets
selPreset.addEventListener('change', e => {{
    const p = e.target.value;
    if (p === 'standard') {{
        setParams({{ l: 1.0, ag: 0.50, k: 3.87, aw: 0.75, ab: 0.25, gamma: 0.3 }});
    }} else if (p === 'mid_opt') {{
        setParams({{ l: 1.05, ag: 0.50, k: 3.87, aw: 0.75, ab: 0.25, gamma: 0.3 }});
    }} else if (p === 'low_l') {{
        setParams({{ l: 0.75, ag: 0.50, k: 3.87, aw: 0.75, ab: 0.25, gamma: 0.3 }});
    }} else if (p === 'high_l') {{
        setParams({{ l: 1.30, ag: 0.50, k: 3.87, aw: 0.75, ab: 0.25, gamma: 0.3 }});
    }}
}});

function setParams(cfg) {{
    if (cfg.l !== undefined) {{ state.l_val = cfg.l; sliderL.value = cfg.l; numL.value = cfg.l; }}
    if (cfg.ag !== undefined) {{ state.alpha_g = cfg.ag; sliderAg.value = cfg.ag; numAg.value = cfg.ag; }}
    if (cfg.k !== undefined) {{ state.k_diff = cfg.k; sliderK.value = cfg.k; numK.value = cfg.k; }}
    if (cfg.aw !== undefined) {{ state.alpha_w = cfg.aw; sliderAw.value = cfg.aw; numAw.value = cfg.aw; }}
    if (cfg.ab !== undefined) {{ state.alpha_b = cfg.ab; sliderAb.value = cfg.ab; numAb.value = cfg.ab; }}
    if (cfg.gamma !== undefined) {{ state.gamma_val = cfg.gamma; sliderGamma.value = cfg.gamma; numGamma.value = cfg.gamma; }}
    runSimulation();
    renderDynamicTraces();
}}


// Export High-Res PNG Snapshot
function exportSnapshotPng() {{
    if (!state.simData) runSimulation();

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
    const modeName = state.physicsMode === 'atmosphere' ? '大氣溫室+經向熱擴散模式' : '無大氣純黑體輻射模式';
    ctx.fillText(`1D 緯度灰雛菊三物種世界空間模擬實測 - [${{modeName}}]`, pad, pad + 18);

    ctx.font = '12px "JetBrains Mono", monospace';
    ctx.fillStyle = '#94a3b8';
    ctx.fillText(`光度 L: ${{state.l_val.toFixed(2)}} | 調控全球均溫: ${{state.simData.meanTp.toFixed(2)}}℃ | 死星均溫: ${{state.simData.meanTdead.toFixed(2)}}℃ | K: ${{state.k_diff.toFixed(1)}}`, pad, pad + 40);

    ctx.drawImage(bg1, pad, pad + headerH, width, height);
    ctx.drawImage(fg1, pad, pad + headerH, width, height);

    ctx.drawImage(bg2, pad * 2 + width, pad + headerH, width, height);
    ctx.drawImage(fg2, pad * 2 + width, pad + headerH, width, height);

    const link = document.createElement('a');
    link.download = `daisyworld_grey_1d_L${{state.l_val.toFixed(2)}}_${{state.physicsMode}}.png`;
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
    if (!isRecording || !recordCtx || !state.simData) return;
    recordCtx.fillStyle = '#0b1120';
    recordCtx.fillRect(0, 0, 1200, 680);

    recordCtx.fillStyle = '#00e5ff';
    recordCtx.font = 'bold 20px "Plus Jakarta Sans", sans-serif';
    recordCtx.fillText('1D Latitude Grey Daisyworld Simulation Lab (3 Species)', 25, 35);
    recordCtx.fillStyle = '#94a3b8';
    recordCtx.font = '13px "JetBrains Mono", monospace';
    recordCtx.fillText(`L=${{state.l_val.toFixed(2)}} | MeanTp=${{state.simData.meanTp.toFixed(2)}}℃ | DeadTp=${{state.simData.meanTdead.toFixed(2)}}℃ | K=${{state.k_diff.toFixed(1)}}`, 25, 60);

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
        link.download = `daisyworld_grey_1d_dynamic_${{Date.now()}}.webm`;
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

btnToggleAdv.addEventListener('click', () => {{
    const isHidden = advancedPanel.style.display === 'none';
    advancedPanel.style.display = isHidden ? 'block' : 'none';
    btnToggleAdv.style.background = isHidden ? 'rgba(0, 229, 255, 0.25)' : '';
    btnToggleAdv.innerText = isHidden ? '🔼 收合進階參數' : '⚙️ 進階參數';
}});

btnExportPng.addEventListener('click', exportSnapshotPng);
btnRecordVideo.addEventListener('click', toggleRecordVideo);

btnReset.addEventListener('click', () => {{
    selPreset.value = 'standard';
    setParams({{ l: 1.0, ag: 0.50, k: 3.87, aw: 0.75, ab: 0.25, gamma: 0.3 }});
}});

// Tooltip on Chart 1
fg1.addEventListener('mousemove', e => {{
    const rect = fg1.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const plotW = width - margin.left - margin.right;
    if (mouseX >= margin.left && mouseX <= margin.left + plotW) {{
        const normX = (mouseX - margin.left) / plotW;
        const isNorth = state.viewDomain === 'north';
        const lat = isNorth ? (normX * 90.0) : (-90.0 + normX * 180.0);
        const d = state.simData;
        if (d) {{
            const lats = isNorth ? d.northLats : d.fullLats;
            const awVals = isNorth ? d.northAw : d.fullAw;
            const abVals = isNorth ? d.northAb : d.fullAb;
            const agVals = isNorth ? d.northAg : d.fullAg;
            const auVals = isNorth ? d.northAu : d.fullAu;
            const tempVals = isNorth ? d.northTemp : d.fullTemp;
            let closestIdx = 0, minDiff = 999;
            lats.forEach((l, idx) => {{
                const diff = Math.abs(l - lat);
                if (diff < minDiff) {{ minDiff = diff; closestIdx = idx; }}
            }});

            tooltip.style.display = 'block';
            tooltip.style.left = (e.clientX + 14) + 'px';
            tooltip.style.top = (e.clientY - 25) + 'px';
            const latStr = lats[closestIdx] === 0 ? '赤道' : (lats[closestIdx] > 0 ? lats[closestIdx] + '°N' : Math.abs(lats[closestIdx]) + '°S');
            tooltip.innerHTML = `緯度: ${{latStr}}<br>白雛菊: ${{(awVals[closestIdx]*100).toFixed(1)}}%<br>黑雛菊: ${{(abVals[closestIdx]*100).toFixed(1)}}%<br>灰雛菊: ${{(agVals[closestIdx]*100).toFixed(1)}}%<br>裸地: ${{(auVals[closestIdx]*100).toFixed(1)}}%<br>均溫: ${{tempVals[closestIdx].toFixed(2)}}℃`;
            return;
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
        const normX = (mouseX - margin.left) / plotW;
        const isNorth = state.viewDomain === 'north';
        const lat = isNorth ? (normX * 90.0) : (-90.0 + normX * 180.0);
        const d = state.simData;
        if (d) {{
            const lats = isNorth ? d.northLats : d.fullLats;
            const tempVals = isNorth ? d.northTemp : d.fullTemp;
            const deadVals = isNorth ? d.northDead : d.fullDead;
            let closestIdx = 0, minDiff = 999;
            lats.forEach((l, idx) => {{
                const diff = Math.abs(l - lat);
                if (diff < minDiff) {{ minDiff = diff; closestIdx = idx; }}
            }});

            tooltip.style.display = 'block';
            tooltip.style.left = (e.clientX + 14) + 'px';
            tooltip.style.top = (e.clientY - 25) + 'px';
            const latStr = lats[closestIdx] === 0 ? '赤道' : (lats[closestIdx] > 0 ? lats[closestIdx] + '°N' : Math.abs(lats[closestIdx]) + '°S');
            const diffDead = tempVals[closestIdx] - deadVals[closestIdx];
            tooltip.innerHTML = `緯度: ${{latStr}}<br>三物種調控溫: ${{tempVals[closestIdx].toFixed(2)}}℃<br>死星基線: ${{deadVals[closestIdx].toFixed(2)}}℃<br>調節溫差: ${{diffDead >= 0 ? '+' : ''}}${{diffDead.toFixed(2)}}℃`;
            return;
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
