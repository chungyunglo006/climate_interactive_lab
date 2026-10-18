"""
Interactive Client-Side Canvas Engine for 0D Classic Daisyworld.
Enhanced with Wisconsin AOS (UW-Madison / Roland Stull 2000) features:
1. Circular Planetary Live Disk (Pie & Organic Disk with Atmospheric Glow)
2. Precision Vertical Mercury Thermometer (Comparing Tp vs T_dead across habitability zones)
3. Multi-Run Empirical Phase Accumulator (Log experiment scatter points)
4. Dual Physics Framework Selector (Lovelock 1983 equivalent model vs Stull 2000 modern Earth + single-layer greenhouse)
"""

def get_interactive_daisy0d_html(
    s0=917.0, l_val=1.0, alpha_w=0.75, alpha_b=0.25, alpha_u=0.5,
    q_val=20.0, gamma_val=0.3, aw_init=0.01, ab_init=0.01, dt=0.1, itera=150
):
    """Generates self-contained hardware-accelerated interactive canvas HTML for 0D Daisyworld."""
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
    flex-wrap: wrap;
    gap: 10px;
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

input[type="number"].val-input {{
    width: 78px;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 6px;
    color: #00e5ff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    font-weight: 600;
    padding: 4px 6px;
    text-align: right;
}}

input[type="number"].val-input:focus {{
    outline: none;
    border-color: #00e5ff;
    box-shadow: 0 0 8px rgba(0, 229, 255, 0.4);
}}

.action-row {{
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 0.85rem;
}}

.btn {{
    background: linear-gradient(135deg, #00e5ff 0%, #0284c7 100%);
    color: #04101e;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 7px 14px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}}

.btn:hover {{
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(0, 229, 255, 0.35);
}}

.btn-secondary {{
    background: rgba(255, 255, 255, 0.08);
    color: #e2e8f0;
    border: 1px solid rgba(255, 255, 255, 0.15);
}}

.btn-secondary:hover {{
    background: rgba(255, 255, 255, 0.15);
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
}}

select, input[type="number"].inline-input {{
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 6px;
    color: #f8fafc;
    padding: 5px 8px;
    font-size: 0.82rem;
    font-family: inherit;
}}

/* Wisconsin AOS Dashboard Section */
.planet-dashboard-grid {{
    display: grid;
    grid-template-columns: 220px 170px 1fr;
    gap: 16px;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.75) 0%, rgba(30, 41, 59, 0.7) 100%);
    border: 1px solid rgba(0, 229, 255, 0.2);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 18px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    align-items: center;
}}

@media (max-width: 950px) {{
    .planet-dashboard-grid {{
        grid-template-columns: 1fr;
        justify-items: center;
        text-align: center;
    }}
}}

.dash-box {{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}}

.dash-box-title {{
    font-size: 0.8rem;
    color: #94a3b8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
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
        <div class="panel-title">🌼 0D 經典雛菊世界物理參數面板 (滑桿 + 精確數值直接輸入)</div>
        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <span style="font-size: 0.8rem; color: #94a3b8;">🎯 預設情境:</span>
            <select id="sel_preset">
                <option value="standard" selected>標準光度 (L = 1.0 - 黑白共生)</option>
                <option value="low_l">微弱太陽 (L = 0.72 - 黑雛菊主導保溫)</option>
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
            <span class="ctrl-label"><span>太陽常數 S₀ (W/m²)</span><span>基礎日射</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_s0" min="700" max="1600" step="1" value="{s0}">
                <input type="number" class="val-input" id="num_s0" min="700" max="1600" step="1" value="{s0}">
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
            <span class="ctrl-label"><span>裸地反照率 α_u</span><span>反射比</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_au" min="0.3" max="0.7" step="0.01" value="{alpha_u}">
                <input type="number" class="val-input" id="num_au" min="0.3" max="0.7" step="0.01" value="{alpha_u}">
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

        <span style="color: #64748b; margin-left: 8px;">物理體系:</span>
        <select id="sel_physics_mode">
            <option value="lovelock" selected>🌻 Lovelock (1983) 等效無大氣 (S₀=917)</option>
            <option value="stull">🌍 Wisconsin Stull (2000) 現代地球單層溫室 (S₀=1368)</option>
        </select>

        <span style="color: #64748b; margin-left: 8px;">演變變數:</span>
        <select id="sel_anim_target">
            <option value="l_val">太陽光度 L</option>
            <option value="gamma_val">死亡率 γ</option>
            <option value="alpha_w">白雛菊反照率 α_w</option>
            <option value="alpha_b">黑雛菊反照率 α_b</option>
        </select>

        <span style="color: #64748b;">方向:</span>
        <select id="sel_anim_dir">
            <option value="pingpong">來回擺動 (Ping-Pong)</option>
            <option value="inc">往大增加 (+)</option>
            <option value="dec">往小減少 (-)</option>
        </select>

        <span style="color: #64748b;">速率:</span>
        <input type="number" class="inline-input" id="num_anim_speed" value="0.003" step="0.001" min="0.0005" max="0.03" style="width: 80px;">
    </div>
</div>

<!-- Wisconsin AOS Dashboard: Planetary Live Disk + Thermometer + Experiment Logger -->
<div class="planet-dashboard-grid">
    <!-- Box 1: Planet Live Disk -->
    <div class="dash-box">
        <div class="dash-box-title">🪐 活體行星盤面 (Planet Disk)</div>
        <div style="position: relative; width: 170px; height: 170px;">
            <canvas id="cv_planet" width="170" height="170" style="position: static;"></canvas>
        </div>
        <div id="planet_disk_caption" style="font-size: 0.72rem; color: #94a3b8; font-family: 'JetBrains Mono', monospace; margin-top: 6px; text-align: center;">
            白: --% | 黑: --% | 裸: --%
        </div>
    </div>

    <!-- Box 2: Vertical Precision Thermometer -->
    <div class="dash-box">
        <div class="dash-box-title">🌡️ 擬真水銀溫度計</div>
        <div style="position: relative; width: 140px; height: 180px;">
            <canvas id="cv_thermo" width="140" height="180" style="position: static;"></canvas>
        </div>
    </div>

    <!-- Box 3: Empirical Lab Accumulator & Physics Insights -->
    <div class="dash-box" style="align-items: flex-start; padding: 0 10px;">
        <div class="dash-box-title">🧪 實測點記錄工坊 (Wisconsin AOS 實驗法)</div>
        <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.5; margin-bottom: 10px;">
            如同威斯康辛大學互動實驗，每次改變光度 $L$ 或微氣候參數後，按下「記錄平衡點」，畫布將在溫度圖表留下實測散佈點。累積多點即可由實測數據親手拼出蓋婭恆溫倒 U 型曲線！
        </p>
        <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 8px;">
            <button class="btn btn-secondary" id="btn_record_point" style="font-size: 0.8rem; padding: 5px 12px;">📍 記錄當前平衡點</button>
            <button class="btn btn-secondary" id="btn_clear_points" style="font-size: 0.8rem; padding: 5px 12px;">🧹 清除實驗紀錄</button>
            <span id="lbl_point_count" style="font-size: 0.78rem; color: #00e5ff; font-family: 'JetBrains Mono', monospace;">已記錄 0 個實測點</span>
        </div>
        <div id="physics_mode_badge" style="font-size: 0.75rem; color: #64748b; background: rgba(15, 23, 42, 0.6); border-radius: 6px; padding: 5px 8px; border-left: 3px solid #00e5ff; width: 100%;">
            🌻 Lovelock (1983)：S₀=917 W/m² (等效無大氣單一常數，光度 L=1.0 正處於黑白雛菊共生的恆溫平台)。
        </div>
    </div>
</div>

<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-title">調節後行星均溫 (T_p)</div>
        <div class="stat-val" id="stat_tp" style="color: #22c55e;">-- ℃</div>
        <div class="stat-sub" id="stat_gaea_eval">蓋亞恆溫評估中...</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">無生物死星基線</div>
        <div class="stat-val" id="stat_tnobio" style="color: #ef4444;">-- ℃</div>
        <div class="stat-sub" id="stat_delta_t">溫差: -- ℃</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">白雛菊覆蓋率 (散熱)</div>
        <div class="stat-val" id="stat_aw" style="color: #f8fafc;">-- %</div>
        <div class="stat-sub" id="stat_tw">局地溫: -- ℃</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">黑雛菊覆蓋率 (保溫)</div>
        <div class="stat-val" id="stat_ab" style="color: #94a3b8;">-- %</div>
        <div class="stat-sub" id="stat_tb">局地溫: -- ℃</div>
    </div>
</div>

<div class="charts-grid">
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">🌼 物種覆蓋率時間消長 (60 FPS 族群動態)</div>
            <div class="chart-legend">
                <div class="legend-item"><div class="legend-color" style="background: #f8fafc;"></div> 白雛菊</div>
                <div class="legend-item"><div class="legend-color" style="background: #475569;"></div> 黑雛菊</div>
                <div class="legend-item"><div class="legend-color" style="background: #d97706; border-top: 1px dashed;"></div> 裸地資源</div>
            </div>
        </div>
        <div class="canvas-container" id="container1">
            <canvas id="bg1"></canvas>
            <canvas id="fg1"></canvas>
        </div>
    </div>

    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">🌡️ 行星溫度調控效應 vs 死星基線 (含實驗散佈點)</div>
            <div class="chart-legend">
                <div class="legend-item"><div class="legend-color" style="background: #22c55e;"></div> 調節 Tp</div>
                <div class="legend-item"><div class="legend-color" style="background: #ef4444; border-top: 1px dashed;"></div> 死星基線</div>
                <div class="legend-item"><div class="legend-color" style="background: #00e5ff; border-radius: 50%;"></div> 實測點</div>
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
const DT = {dt};
const ITERA = {itera};

let state = {{
    s0: {s0},
    l_val: {l_val},
    alpha_w: {alpha_w},
    alpha_b: {alpha_b},
    alpha_u: {alpha_u},
    q_val: {q_val},
    gamma_val: {gamma_val},
    aw_init: {aw_init},
    ab_init: {ab_init},
    physicsMode: 'lovelock', // 'lovelock' or 'stull'
    isPlaying: false,
    pingPongDir: 1,
    simData: null,
    recordedPoints: [] // {{ l, Tp, Tnobio, aw, ab, au, mode }}
}};

// DOM Elements
const sliderL = document.getElementById('slider_l');
const numL = document.getElementById('num_l');
const sliderS0 = document.getElementById('slider_s0');
const numS0 = document.getElementById('num_s0');
const sliderGamma = document.getElementById('slider_gamma');
const numGamma = document.getElementById('num_gamma');
const sliderAw = document.getElementById('slider_aw');
const numAw = document.getElementById('num_aw');
const sliderAb = document.getElementById('slider_ab');
const numAb = document.getElementById('num_ab');
const sliderAu = document.getElementById('slider_au');
const numAu = document.getElementById('num_au');
const sliderQ = document.getElementById('slider_q');
const numQ = document.getElementById('num_q');
const selPreset = document.getElementById('sel_preset');
const selPhysicsMode = document.getElementById('sel_physics_mode');
const physicsModeBadge = document.getElementById('physics_mode_badge');

const btnTogglePlay = document.getElementById('btn_toggle_play');
const btnReset = document.getElementById('btn_reset');
const selAnimTarget = document.getElementById('sel_anim_target');
const selAnimDir = document.getElementById('sel_anim_dir');
const numAnimSpeed = document.getElementById('num_anim_speed');

const btnRecordPoint = document.getElementById('btn_record_point');
const btnClearPoints = document.getElementById('btn_clear_points');
const lblPointCount = document.getElementById('lbl_point_count');

const statTp = document.getElementById('stat_tp');
const statGaeaEval = document.getElementById('stat_gaea_eval');
const statTnobio = document.getElementById('stat_tnobio');
const statDeltaT = document.getElementById('stat_delta_t');
const statAw = document.getElementById('stat_aw');
const statTw = document.getElementById('stat_tw');
const statAb = document.getElementById('stat_ab');
const statTb = document.getElementById('stat_tb');
const planetDiskCaption = document.getElementById('planet_disk_caption');

const cvPlanet = document.getElementById('cv_planet');
const ctxPlanet = cvPlanet.getContext('2d');
const cvThermo = document.getElementById('cv_thermo');
const ctxThermo = cvThermo.getContext('2d');

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
    let awList = [], abList = [], auList = [];
    let TpList = [], TwList = [], TbList = [];

    let aw = state.aw_init;
    let ab = state.ab_init;

    const isStull = state.physicsMode === 'stull';

    for (let step = 0; step <= ITERA; step++) {{
        const au = Math.max(0.0, Math.min(1.0, 1.0 - aw - ab));
        const alphaP = aw * state.alpha_w + ab * state.alpha_b + au * state.alpha_u;

        let TpC, Tw, Tb;

        if (!isStull) {{
            // --- 🌻 Lovelock 1983 (Equivalent solar constant, no atmosphere) ---
            const TpK = Math.pow((state.s0 * state.l_val * (1.0 - alphaP)) / SIGMA, 0.25);
            TpC = TpK - 273.15;
            Tw = TpC + state.q_val * (alphaP - state.alpha_w);
            Tb = TpC + state.q_val * (alphaP - state.alpha_b);
        }} else {{
            // --- 🌍 Wisconsin Stull 2000 (S0 = 1368, single-layer greenhouse + Tr = 0.6) ---
            const q = (state.s0 * state.l_val) / (4.0 * SIGMA);
            const Te4 = q * (1.0 - alphaP);
            const Ts4 = 2.0 * Te4; // 1-layer greenhouse effect
            TpC = Math.pow(Ts4, 0.25) - 273.15;
            const Tr = 0.6; // horizontal heat transport parameter
            const Tw4 = Math.max(1e5, (1.0 - Tr) * q * (alphaP - state.alpha_w) + Ts4);
            const Tb4 = Math.max(1e5, (1.0 - Tr) * q * (alphaP - state.alpha_b) + Ts4);
            Tw = Math.pow(Tw4, 0.25) - 273.15;
            Tb = Math.pow(Tb4, 0.25) - 273.15;
        }}

        const betaW = betaGrowth(Tw);
        const betaB = betaGrowth(Tb);

        t.push(step * DT);
        awList.push(aw);
        abList.push(ab);
        auList.push(au);
        TpList.push(TpC);
        TwList.push(Tw);
        TbList.push(Tb);

        const daw = aw * (au * betaW - state.gamma_val);
        const dab = ab * (au * betaB - state.gamma_val);

        aw = Math.max(0.001, Math.min(0.99, aw + DT * daw));
        ab = Math.max(0.001, Math.min(0.99, ab + DT * dab));
        if (aw + ab > 0.99) {{
            const sc = 0.99 / (aw + ab);
            aw *= sc; ab *= sc;
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
        t, aw: awList, ab: abList, au: auList,
        Tp: TpList, Tw: TwList, Tb: TbList,
        finalTp: TpList[TpList.length - 1],
        finalAw: awList[awList.length - 1],
        finalAb: abList[abList.length - 1],
        finalAu: auList[auList.length - 1],
        finalTw: TwList[TwList.length - 1],
        finalTb: TbList[TbList.length - 1],
        Tnobio: Tnobio
    }};

    drawPlanetDisk();
    drawThermometer();
}}

// Draw Wisconsin AOS Feature 1: Planetary Live Disk
function drawPlanetDisk() {{
    if (!state.simData) return;
    const d = state.simData;
    const w = cvPlanet.width;
    const h = cvPlanet.height;
    ctxPlanet.clearRect(0, 0, w, h);

    const cx = w / 2;
    const cy = h / 2;
    const r = 58;

    // Atmospheric Glow Color (Temperature-sensitive)
    const Tp = d.finalTp;
    let haloColor = 'rgba(34, 197, 94, 0.35)'; // Emerald green (optimal)
    if (Tp < 5.0) haloColor = 'rgba(56, 189, 248, 0.45)'; // Freezing blue
    else if (Tp > 35.0) haloColor = 'rgba(239, 68, 68, 0.45)'; // Overheating red

    // 1. Atmosphere Halo
    const gradHalo = ctxPlanet.createRadialGradient(cx, cy, r * 0.85, cx, cy, r * 1.35);
    gradHalo.addColorStop(0, haloColor);
    gradHalo.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctxPlanet.fillStyle = gradHalo;
    ctxPlanet.beginPath();
    ctxPlanet.arc(cx, cy, r * 1.35, 0, Math.PI * 2);
    ctxPlanet.fill();

    // 2. Planet Sphere with 3D Sphere shading
    ctxPlanet.save();
    ctxPlanet.beginPath();
    ctxPlanet.arc(cx, cy, r, 0, Math.PI * 2);
    ctxPlanet.clip();

    // Base Soil (Bare Ground: Golden Brown)
    ctxPlanet.fillStyle = '#92400e';
    ctxPlanet.fillRect(cx - r, cy - r, r * 2, r * 2);

    // Dynamic Slices for White & Black Daisies
    const aw = d.finalAw;
    const ab = d.finalAb;
    const au = d.finalAu;

    // White Daisy patch (Top & Equatorial crescent)
    const angleW = aw * Math.PI * 2;
    ctxPlanet.fillStyle = '#f8fafc';
    ctxPlanet.beginPath();
    ctxPlanet.moveTo(cx, cy);
    ctxPlanet.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + angleW);
    ctxPlanet.closePath();
    ctxPlanet.fill();

    // Black Daisy patch
    const angleB = ab * Math.PI * 2;
    ctxPlanet.fillStyle = '#334155';
    ctxPlanet.beginPath();
    ctxPlanet.moveTo(cx, cy);
    ctxPlanet.arc(cx, cy, r, -Math.PI / 2 + angleW, -Math.PI / 2 + angleW + angleB);
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

    // Outer Rim Glow
    ctxPlanet.strokeStyle = 'rgba(255, 255, 255, 0.25)';
    ctxPlanet.lineWidth = 1.5;
    ctxPlanet.beginPath();
    ctxPlanet.arc(cx, cy, r, 0, Math.PI * 2);
    ctxPlanet.stroke();

    // Update Caption
    planetDiskCaption.innerHTML = `白雛菊: <b style="color:#f8fafc;">${{(aw*100).toFixed(1)}}%</b> | 黑雛菊: <b style="color:#94a3b8;">${{(ab*100).toFixed(1)}}%</b> | 裸地: <b style="color:#d97706;">${{(au*100).toFixed(1)}}%</b>`;
}}

// Draw Wisconsin AOS Feature 2: Precision Mercury Thermometer
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

    // 1. Habitable Daisy Range Green Shading (5°C to 40°C)
    const y5 = getY(5.0);
    const y40 = getY(40.0);
    ctxThermo.fillStyle = 'rgba(34, 197, 94, 0.12)';
    ctxThermo.fillRect(tubeX - 2, y40, tubeW + 4, y5 - y40);

    // 2. Ticks & Labels
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

    // 22.5°C Optimal Line
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

    // 3. Glass Tube Outline
    ctxThermo.fillStyle = 'rgba(15, 23, 42, 0.7)';
    ctxThermo.fillRect(tubeX, tubeY, tubeW, tubeH);

    // 4. Dead Planet Red Marker (Right half-line)
    const yDead = Math.max(tubeY, Math.min(tubeY + tubeH, getY(d.Tnobio)));
    ctxThermo.fillStyle = '#ef4444';
    ctxThermo.fillRect(tubeX + tubeW / 2, yDead, tubeW / 2, (tubeY + tubeH) - yDead);

    // 5. Regulated Planet Temperature Mercury Fill (Left / Full glowing column)
    const yBio = Math.max(tubeY, Math.min(tubeY + tubeH, getY(d.finalTp)));
    const gradMerc = ctxThermo.createLinearGradient(tubeX, 0, tubeX + tubeW / 2, 0);
    gradMerc.addColorStop(0, '#4ade80');
    gradMerc.addColorStop(1, '#22c55e');
    ctxThermo.fillStyle = gradMerc;
    ctxThermo.fillRect(tubeX, yBio, tubeW / 2, (tubeY + tubeH) - yBio);

    // 6. Glass Tube Border
    ctxThermo.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctxThermo.lineWidth = 1.5;
    ctxThermo.strokeRect(tubeX, tubeY, tubeW, tubeH);

    // 7. Bulb at base
    ctxThermo.beginPath();
    ctxThermo.arc(tubeX + tubeW / 2, bulbY, bulbR, 0, Math.PI * 2);
    ctxThermo.fillStyle = '#22c55e';
    ctxThermo.fill();
    ctxThermo.strokeStyle = 'rgba(255, 255, 255, 0.4)';
    ctxThermo.lineWidth = 1.5;
    ctxThermo.stroke();

    // Dual Column Legends on Right
    ctxThermo.textAlign = 'left';
    ctxThermo.font = '10px "Plus Jakarta Sans", sans-serif';
    ctxThermo.fillStyle = '#22c55e';
    ctxThermo.fillText(`Tp: ${{d.finalTp.toFixed(1)}}℃`, tubeX + tubeW + 12, tubeY + 20);
    ctxThermo.fillStyle = '#ef4444';
    ctxThermo.fillText(`死星: ${{d.Tnobio.toFixed(1)}}℃`, tubeX + tubeW + 12, tubeY + 36);
}}

function drawStaticBackgrounds() {{
    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;

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

    const xMax = ITERA * DT;
    const xStep = Math.max(2, Math.round(xMax / 6));
    ctxBg1.textAlign = 'center';
    ctxBg1.textBaseline = 'top';

    for (let xVal = 0; xVal <= xMax; xVal += xStep) {{
        const x = margin.left + plotW * (xVal / xMax);
        ctxBg1.beginPath();
        ctxBg1.moveTo(x, margin.top);
        ctxBg1.lineTo(x, margin.top + plotH);
        ctxBg1.stroke();
        ctxBg1.fillText(xVal, x, margin.top + plotH + 8);
    }}

    ctxBg1.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctxBg1.strokeRect(margin.left, margin.top, plotW, plotH);


    // --- Chart 2 Static BG (Temperature) ---
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

    // Optimum growth temperature 22.5 degC line
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

    for (let xVal = 0; xVal <= xMax; xVal += xStep) {{
        const x = margin.left + plotW * (xVal / xMax);
        ctxBg2.beginPath();
        ctxBg2.moveTo(x, margin.top);
        ctxBg2.lineTo(x, margin.top + plotH);
        ctxBg2.stroke();
        ctxBg2.fillText(xVal, x, margin.top + plotH + 8);
    }}

    ctxBg2.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctxBg2.strokeRect(margin.left, margin.top, plotW, plotH);
}}

function renderDynamicTraces() {{
    if (!state.simData) return;

    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;
    const d = state.simData;
    const xMax = ITERA * DT;

    // --- Chart 1: Coverages ---
    ctxFg1.clearRect(0, 0, width, height);
    ctxFg1.save();
    ctxFg1.beginPath();
    ctxFg1.rect(margin.left, margin.top, plotW, plotH);
    ctxFg1.clip();

    // 1. Bare Ground (Orange dash)
    ctxFg1.strokeStyle = '#d97706';
    ctxFg1.lineWidth = 1.8;
    ctxFg1.setLineDash([4, 3]);
    ctxFg1.beginPath();
    for (let i = 0; i < d.t.length; i++) {{
        const x = margin.left + plotW * (d.t[i] / xMax);
        const y = margin.top + plotH * (1.0 - d.au[i]);
        if (i === 0) ctxFg1.moveTo(x, y);
        else ctxFg1.lineTo(x, y);
    }}
    ctxFg1.stroke();
    ctxFg1.setLineDash([]);

    // 2. Black Daisy (Dark Slate Blue)
    ctxFg1.shadowBlur = 6;
    ctxFg1.shadowColor = '#475569';
    ctxFg1.strokeStyle = '#64748b';
    ctxFg1.lineWidth = 2.8;
    ctxFg1.beginPath();
    for (let i = 0; i < d.t.length; i++) {{
        const x = margin.left + plotW * (d.t[i] / xMax);
        const y = margin.top + plotH * (1.0 - d.ab[i]);
        if (i === 0) ctxFg1.moveTo(x, y);
        else ctxFg1.lineTo(x, y);
    }}
    ctxFg1.stroke();

    // 3. White Daisy (Pure White)
    ctxFg1.shadowBlur = 8;
    ctxFg1.shadowColor = '#ffffff';
    ctxFg1.strokeStyle = '#f8fafc';
    ctxFg1.lineWidth = 3.0;
    ctxFg1.beginPath();
    for (let i = 0; i < d.t.length; i++) {{
        const x = margin.left + plotW * (d.t[i] / xMax);
        const y = margin.top + plotH * (1.0 - d.aw[i]);
        if (i === 0) ctxFg1.moveTo(x, y);
        else ctxFg1.lineTo(x, y);
    }}
    ctxFg1.stroke();
    ctxFg1.restore();


    // --- Chart 2: Temperature ---
    ctxFg2.clearRect(0, 0, width, height);
    const yMin2 = 0.0, yMax2 = 50.0;
    ctxFg2.save();
    ctxFg2.beginPath();
    ctxFg2.rect(margin.left, margin.top, plotW, plotH);
    ctxFg2.clip();

    // Abiotic baseline horizontal line (Red dash)
    const yDead = margin.top + plotH * (1.0 - (d.Tnobio - yMin2) / (yMax2 - yMin2));
    ctxFg2.setLineDash([5, 4]);
    ctxFg2.strokeStyle = '#ef4444';
    ctxFg2.lineWidth = 2.0;
    ctxFg2.beginPath();
    ctxFg2.moveTo(margin.left, yDead);
    ctxFg2.lineTo(margin.left + plotW, yDead);
    ctxFg2.stroke();
    ctxFg2.setLineDash([]);

    // Regulated Planet Temperature (Green)
    ctxFg2.shadowBlur = 8;
    ctxFg2.shadowColor = '#22c55e';
    ctxFg2.strokeStyle = '#22c55e';
    ctxFg2.lineWidth = 3.2;
    ctxFg2.beginPath();
    for (let i = 0; i < d.t.length; i++) {{
        const x = margin.left + plotW * (d.t[i] / xMax);
        const y = margin.top + plotH * (1.0 - (d.Tp[i] - yMin2) / (yMax2 - yMin2));
        if (i === 0) ctxFg2.moveTo(x, y);
        else ctxFg2.lineTo(x, y);
    }}
    ctxFg2.stroke();

    // Wisconsin AOS Feature 3: Overlay Multi-Run Empirical Experiment Scatter Points
    state.recordedPoints.forEach(pt => {{
        const x = margin.left + plotW * 0.92; // Displayed on equilibrium side
        const yPt = margin.top + plotH * (1.0 - (pt.Tp - yMin2) / (yMax2 - yMin2));
        ctxFg2.fillStyle = '#00e5ff';
        ctxFg2.shadowBlur = 6;
        ctxFg2.shadowColor = '#00e5ff';
        ctxFg2.beginPath();
        ctxFg2.arc(x, yPt, 5, 0, Math.PI * 2);
        ctxFg2.fill();
    }});

    ctxFg2.restore();

    // Update Stats
    statTp.innerText = d.finalTp.toFixed(2) + ' ℃';
    statTnobio.innerText = d.Tnobio.toFixed(1) + ' ℃';
    const dtDiff = d.finalTp - d.Tnobio;
    statDeltaT.innerText = '調節溫差: ' + (dtDiff >= 0 ? '+' : '') + dtDiff.toFixed(2) + ' ℃';
    statAw.innerText = (d.finalAw * 100).toFixed(1) + ' %';
    statTw.innerText = '局地溫: ' + d.finalTw.toFixed(1) + ' ℃';
    statAb.innerText = (d.finalAb * 100).toFixed(1) + ' %';
    statTb.innerText = '局地溫: ' + d.finalTb.toFixed(1) + ' ℃';

    if (Math.abs(d.finalTp - 22.5) < 3.0 && (d.finalAw > 0.05 || d.finalAb > 0.05)) {{
        statGaeaEval.innerText = '🌿 蓋亞強效恆溫中 (接近最適 22.5℃)';
        statTp.style.color = '#22c55e';
    }} else if (d.finalAw <= 0.015 && d.finalAb <= 0.015) {{
        statGaeaEval.innerText = '💀 生態崩潰：雛菊全數滅絕 (死星態)';
        statTp.style.color = '#ef4444';
    }} else {{
        statGaeaEval.innerText = '⚡ 邊緣調節過渡態';
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

    let minV = 0.6, maxV = 1.6;
    if (target === 'l_val') {{ minV = 0.6; maxV = 1.6; }}
    else if (target === 'gamma_val') {{ minV = 0.05; maxV = 0.5; }}
    else if (target === 'alpha_w') {{ minV = 0.5; maxV = 0.9; }}
    else if (target === 'alpha_b') {{ minV = 0.1; maxV = 0.45; }}

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

    animFrameId = requestAnimationFrame(animationStep);
}}

function syncControls(target, val) {{
    if (target === 'l_val') {{
        sliderL.value = val; numL.value = val.toFixed(2);
    }} else if (target === 'gamma_val') {{
        sliderGamma.value = val; numGamma.value = val.toFixed(2);
    }} else if (target === 'alpha_w') {{
        sliderAw.value = val; numAw.value = val.toFixed(2);
    }} else if (target === 'alpha_b') {{
        sliderAb.value = val; numAb.value = val.toFixed(2);
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
bindSync(sliderS0, numS0, 's0');
bindSync(sliderGamma, numGamma, 'gamma_val');
bindSync(sliderAw, numAw, 'alpha_w');
bindSync(sliderAb, numAb, 'alpha_b');
bindSync(sliderAu, numAu, 'alpha_u');
bindSync(sliderQ, numQ, 'q_val');

btnTogglePlay.addEventListener('click', togglePlay);

// Physics Framework Switch
selPhysicsMode.addEventListener('change', e => {{
    state.physicsMode = e.target.value;
    if (state.physicsMode === 'stull') {{
        state.s0 = 1368.0;
        sliderS0.value = 1368;
        numS0.value = 1368;
        physicsModeBadge.innerHTML = '🌍 Stull (2000)：S₀=1368 W/m² + 單層溫室效應 (T_s⁴ = 2T_e⁴) + 水平傳輸 Tr=0.6。在 L=1.0 下溫室增溫使黑白雛菊穩定共存繁盛！';
        physicsModeBadge.style.borderLeftColor = '#22c55e';
    }} else {{
        state.s0 = 917.0;
        sliderS0.value = 917;
        numS0.value = 917;
        physicsModeBadge.innerHTML = '🌻 Lovelock (1983)：S₀=917 W/m² (等效無大氣單一常數，光度 L=1.0 正處於黑白雛菊共生的恆溫平台)。';
        physicsModeBadge.style.borderLeftColor = '#00e5ff';
    }}
    runSimulation();
    renderDynamicTraces();
}});

// Wisconsin AOS Feature 3: Record Experiment Points
btnRecordPoint.addEventListener('click', () => {{
    if (!state.simData) return;
    const d = state.simData;
    state.recordedPoints.push({{
        l: state.l_val,
        Tp: d.finalTp,
        Tnobio: d.Tnobio,
        aw: d.finalAw,
        ab: d.finalAb,
        au: d.finalAu,
        mode: state.physicsMode
    }});
    lblPointCount.innerText = `已記錄 ${{state.recordedPoints.length}} 個實測點`;
    renderDynamicTraces();
}});

btnClearPoints.addEventListener('click', () => {{
    state.recordedPoints = [];
    lblPointCount.innerText = '已記錄 0 個實測點';
    renderDynamicTraces();
}});

// Scenario Presets
selPreset.addEventListener('change', e => {{
    const p = e.target.value;
    if (p === 'standard') {{
        setParams({{ l: 1.0, gamma: 0.3, aw: 0.75, ab: 0.25, au: 0.50 }});
    }} else if (p === 'low_l') {{
        setParams({{ l: 0.72, gamma: 0.3, aw: 0.75, ab: 0.25, au: 0.50 }});
    }} else if (p === 'high_l') {{
        setParams({{ l: 1.35, gamma: 0.3, aw: 0.75, ab: 0.25, au: 0.50 }});
    }} else if (p === 'extreme_cold') {{
        setParams({{ l: 0.55, gamma: 0.3, aw: 0.75, ab: 0.25, au: 0.50 }});
    }} else if (p === 'extreme_hot') {{
        setParams({{ l: 1.70, gamma: 0.3, aw: 0.75, ab: 0.25, au: 0.50 }});
    }}
}});

function setParams(cfg) {{
    if (cfg.l !== undefined) {{ state.l_val = cfg.l; sliderL.value = cfg.l; numL.value = cfg.l; }}
    if (cfg.gamma !== undefined) {{ state.gamma_val = cfg.gamma; sliderGamma.value = cfg.gamma; numGamma.value = cfg.gamma; }}
    if (cfg.aw !== undefined) {{ state.alpha_w = cfg.aw; sliderAw.value = cfg.aw; numAw.value = cfg.aw; }}
    if (cfg.ab !== undefined) {{ state.alpha_b = cfg.ab; sliderAb.value = cfg.ab; numAb.value = cfg.ab; }}
    if (cfg.au !== undefined) {{ state.alpha_u = cfg.au; sliderAu.value = cfg.au; numAu.value = cfg.au; }}
    runSimulation();
    renderDynamicTraces();
}}

btnReset.addEventListener('click', () => {{
    selPreset.value = 'standard';
    setParams({{ l: 1.0, gamma: 0.3, aw: 0.75, ab: 0.25, au: 0.50 }});
}});

// Tooltip on Chart 1
fg1.addEventListener('mousemove', e => {{
    const rect = fg1.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const plotW = width - margin.left - margin.right;
    if (mouseX >= margin.left && mouseX <= margin.left + plotW) {{
        const normX = (mouseX - margin.left) / plotW;
        const idx = Math.min(ITERA, Math.max(0, Math.round(normX * ITERA)));
        const d = state.simData;
        if (d) {{
            tooltip.style.display = 'block';
            tooltip.style.left = (e.clientX + 14) + 'px';
            tooltip.style.top = (e.clientY - 25) + 'px';
            tooltip.innerHTML = `時間: ${{d.t[idx].toFixed(1)}}<br>白雛菊: ${{(d.aw[idx]*100).toFixed(1)}}%<br>黑雛菊: ${{(d.ab[idx]*100).toFixed(1)}}%<br>裸地: ${{(d.au[idx]*100).toFixed(1)}}%<br>均溫: ${{d.Tp[idx].toFixed(2)}}℃`;
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
        const idx = Math.min(ITERA, Math.max(0, Math.round(normX * ITERA)));
        const d = state.simData;
        if (d) {{
            tooltip.style.display = 'block';
            tooltip.style.left = (e.clientX + 14) + 'px';
            tooltip.style.top = (e.clientY - 25) + 'px';
            tooltip.innerHTML = `時間: ${{d.t[idx].toFixed(1)}}<br>行星均溫: ${{d.Tp[idx].toFixed(2)}}℃<br>白雛菊局地: ${{d.Tw[idx].toFixed(2)}}℃<br>黑雛菊局地: ${{d.Tb[idx].toFixed(2)}}℃<br>死星基線: ${{d.Tnobio.toFixed(1)}}℃`;
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
