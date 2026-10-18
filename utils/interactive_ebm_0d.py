"""
Interactive 60 FPS Client-Side Canvas Engine for 0D Energy Balance Model.
Ensures coordinate axes, gridlines, and thresholds are rendered ONCE on a static layer,
while simulation traces update smoothly via requestAnimationFrame at 60 FPS without any flickering.
"""

def get_interactive_ebm0d_html(
    s0=1368.0, t_init=288.0, alpha_ice=0.6, alpha_land=0.3,
    t_ice=263.0, t_land=283.0, epsilon=0.62, dt=0.1, itera=200
):
    """Generates self-contained 60 FPS hardware-accelerated interactive canvas HTML."""
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
    user-select: none;
}}

body {{
    background-color: transparent;
    color: #f8fafc;
    overflow-x: hidden;
    padding: 10px 4px 20px 4px;
}}

.control-panel {{
    background: linear-gradient(135deg, rgba(21, 28, 44, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid rgba(0, 229, 255, 0.25);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 18px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35);
}}

.ctrl-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
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
    letter-spacing: 0.05em;
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

.val-badge {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    font-weight: 600;
    color: #00e5ff;
    min-width: 65px;
    text-align: right;
    background: rgba(0, 229, 255, 0.1);
    padding: 3px 8px;
    border-radius: 6px;
    border: 1px solid rgba(0, 229, 255, 0.25);
}}

.action-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 14px;
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

.btn-secondary:hover {{
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}}

select, input[type="number"] {{
    background: #0f172a;
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #f8fafc;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 0.85rem;
    outline: none;
}}

select:focus, input[type="number"]:focus {{
    border-color: #00e5ff;
}}

/* Stat cards */
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

/* Canvas charts grid */
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
    font-size: 1rem;
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
    height: 420px;
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
    <div class="ctrl-grid">
        <div class="ctrl-item">
            <span class="ctrl-label">太陽常數 S₀ (W/m²)</span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_s0" min="800" max="2000" step="1" value="{s0}">
                <span class="val-badge" id="badge_s0">{s0:.1f}</span>
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label">初始溫度 T_init (K)</span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_tinit" min="200" max="320" step="0.5" value="{t_init}">
                <span class="val-badge" id="badge_tinit">{t_init:.1f}</span>
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label">有效發射率 ε (溫室效應)</span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_eps" min="0.4" max="0.9" step="0.01" value="{epsilon}">
                <span class="val-badge" id="badge_eps">{epsilon:.2f}</span>
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label">冰雪反照率 α_ice</span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_aice" min="0.4" max="0.8" step="0.01" value="{alpha_ice}">
                <span class="val-badge" id="badge_aice">{alpha_ice:.2f}</span>
            </div>
        </div>
    </div>

    <div class="action-row">
        <button class="btn" id="btn_toggle_play">▶️ 開始 60 FPS 絲滑動態演變</button>
        <button class="btn btn-secondary" id="btn_reset">🔄 重設現代地球</button>

        <span style="color: #64748b; margin-left: 8px;">演變變數:</span>
        <select id="sel_anim_target">
            <option value="s0">太陽常數 S₀</option>
            <option value="t_init">初始溫度 T_init</option>
            <option value="eps">有效發射率 ε</option>
            <option value="alpha_ice">冰雪反照率 α_ice</option>
        </select>

        <span style="color: #64748b;">方向:</span>
        <select id="sel_anim_dir">
            <option value="pingpong">來回擺動 (Ping-Pong)</option>
            <option value="inc">往大增加 (+)</option>
            <option value="dec">往小減少 (-)</option>
        </select>

        <span style="color: #64748b;">速率 (Δ/幀):</span>
        <input type="number" id="num_anim_speed" value="0.8" step="0.1" min="0.05" max="5.0" style="width: 75px;">
    </div>
</div>

<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-title">最終平衡溫度</div>
        <div class="stat-val" id="stat_t" style="color: #00e5ff;">-- K</div>
        <div class="stat-sub" id="stat_t_c">-- ℃</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">最終行星反照率</div>
        <div class="stat-val" id="stat_albedo" style="color: #38bdf8;">--</div>
        <div class="stat-sub" id="stat_state_desc">評估中...</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">入射 / 出射能量</div>
        <div class="stat-val" id="stat_rad" style="font-size: 1.15rem; color: #f59e0b;">-- W/m²</div>
        <div class="stat-sub" id="stat_rout">出射: -- W/m²</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">淨輻射不平衡量</div>
        <div class="stat-val" id="stat_imbalance" style="color: #4ade80;">-- W/m²</div>
        <div class="stat-sub" id="stat_eq_status">完美收斂</div>
    </div>
</div>

<div class="charts-grid">
    <!-- Chart 1: Temperature Evolution -->
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">📈 溫度隨時間演化歷程 (60 FPS 硬件平滑渲染)</div>
            <div class="chart-legend">
                <div class="legend-item"><div class="legend-color" style="background: #00e5ff;"></div> 地表溫度 (℃)</div>
                <div class="legend-item"><div class="legend-color" style="background: #38bdf8; border-top: 1px dashed;"></div> 冰封臨界 ({t_ice - 273.15:.1f}℃)</div>
                <div class="legend-item"><div class="legend-color" style="background: #4ade80; border-top: 1px dashed;"></div> 無冰臨界 ({t_land - 273.15:.1f}℃)</div>
            </div>
        </div>
        <div class="canvas-container" id="container1">
            <canvas id="bg1"></canvas>
            <canvas id="fg1"></canvas>
        </div>
    </div>

    <!-- Chart 2: Radiation Fluxes -->
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">⚖️ 能量平衡收支通量</div>
            <div class="chart-legend">
                <div class="legend-item"><div class="legend-color" style="background: #f59e0b;"></div> 入射 R_in</div>
                <div class="legend-item"><div class="legend-color" style="background: #ef4444;"></div> 出射 R_out</div>
                <div class="legend-item"><div class="legend-color" style="background: #a855f7;"></div> 淨通量</div>
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
// Physics constants
const SIGMA = 5.670374e-8;
const SECONDS_PER_YEAR = 3.154e7;
const C_OCEAN = 2.09e8;
const T_ICE = {t_ice};
const T_LAND = {t_land};
const DT = {dt};
const ITERA = {itera};

// State
let state = {{
    s0: {s0},
    t_init: {t_init},
    epsilon: {epsilon},
    alpha_ice: {alpha_ice},
    alpha_land: {alpha_land},
    isPlaying: false,
    pingPongDir: 1,
    simData: null
}};

// DOM Elements
const sliderS0 = document.getElementById('slider_s0');
const sliderTinit = document.getElementById('slider_tinit');
const sliderEps = document.getElementById('slider_eps');
const sliderAice = document.getElementById('slider_aice');

const badgeS0 = document.getElementById('badge_s0');
const badgeTinit = document.getElementById('badge_tinit');
const badgeEps = document.getElementById('badge_eps');
const badgeAice = document.getElementById('badge_aice');

const btnTogglePlay = document.getElementById('btn_toggle_play');
const btnReset = document.getElementById('btn_reset');
const selAnimTarget = document.getElementById('sel_anim_target');
const selAnimDir = document.getElementById('sel_anim_dir');
const numAnimSpeed = document.getElementById('num_anim_speed');

const statT = document.getElementById('stat_t');
const statTC = document.getElementById('stat_t_c');
const statAlbedo = document.getElementById('stat_albedo');
const statStateDesc = document.getElementById('stat_state_desc');
const statRad = document.getElementById('stat_rad');
const statRout = document.getElementById('stat_rout');
const statImbalance = document.getElementById('stat_imbalance');
const statEqStatus = document.getElementById('stat_eq_status');

const bg1 = document.getElementById('bg1');
const fg1 = document.getElementById('fg1');
const bg2 = document.getElementById('bg2');
const fg2 = document.getElementById('fg2');
const tooltip = document.getElementById('tooltip');

const ctxBg1 = bg1.getContext('2d');
const ctxFg1 = fg1.getContext('2d');
const ctxBg2 = bg2.getContext('2d');
const ctxFg2 = fg2.getContext('2d');

// DPR Canvas resizing
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

// Albedo function
function getAlbedo(T, aIce, aLand) {{
    if (T <= T_ICE) return aIce;
    if (T >= T_LAND) return aLand;
    return aIce + (aLand - aIce) * (T - T_ICE) / (T_LAND - T_ICE);
}}

// 0D EBM ODE Integration
function runSimulation() {{
    let t = [];
    let TC = [];
    let Rin = [];
    let Rout = [];
    let imbalance = [];
    let albedo = [];

    let T = state.t_init;
    const aIce = state.alpha_ice;
    const aLand = state.alpha_land;
    const s0 = state.s0;
    const eps = state.epsilon;

    for (let step = 0; step <= ITERA; step++) {{
        const a = getAlbedo(T, aIce, aLand);
        const r_in = (s0 / 4.0) * (1.0 - a);
        const r_out = eps * SIGMA * Math.pow(T, 4);
        const imb = r_in - r_out;

        t.push(step * DT);
        TC.push(T - 273.15);
        Rin.push(r_in);
        Rout.push(r_out);
        imbalance.push(imb);
        albedo.push(a);

        T += (DT * SECONDS_PER_YEAR) * imb / C_OCEAN;
    }}

    state.simData = {{
        t, TC, Rin, Rout, imbalance, albedo,
        finalT: T,
        finalTC: T - 273.15,
        finalAlbedo: albedo[albedo.length - 1],
        finalRin: Rin[Rin.length - 1],
        finalRout: Rout[Rout.length - 1],
        finalImbalance: imbalance[imbalance.length - 1]
    }};
}}

// Draw Static Axes and Grids ONCE (never redrawn on data update!)
function drawStaticBackgrounds() {{
    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;

    // --- Chart 1 Static BG ---
    ctxBg1.clearRect(0, 0, width, height);
    ctxBg1.fillStyle = 'rgba(15, 23, 42, 0.45)';
    ctxBg1.fillRect(margin.left, margin.top, plotW, plotH);

    // Ticks & Grid Y: -40 to 30 degC
    const yMin1 = -45, yMax1 = 35;
    const yTicks1 = [-40, -30, -20, -10, 0, 10, 20, 30];

    ctxBg1.font = '11px "JetBrains Mono", monospace';
    ctxBg1.fillStyle = '#64748b';
    ctxBg1.textAlign = 'right';
    ctxBg1.textBaseline = 'middle';
    ctxBg1.strokeStyle = 'rgba(255, 255, 255, 0.07)';
    ctxBg1.lineWidth = 1;

    yTicks1.forEach(val => {{
        const y = margin.top + plotH * (1.0 - (val - yMin1) / (yMax1 - yMin1));
        ctxBg1.beginPath();
        ctxBg1.moveTo(margin.left, y);
        ctxBg1.lineTo(margin.left + plotW, y);
        ctxBg1.stroke();
        ctxBg1.fillText(val + '℃', margin.left - 8, y);
    }});

    // Critical threshold dashed lines
    const yTice = margin.top + plotH * (1.0 - ((T_ICE - 273.15) - yMin1) / (yMax1 - yMin1));
    ctxBg1.save();
    ctxBg1.setLineDash([5, 4]);
    ctxBg1.strokeStyle = '#38bdf8';
    ctxBg1.beginPath();
    ctxBg1.moveTo(margin.left, yTice);
    ctxBg1.lineTo(margin.left + plotW, yTice);
    ctxBg1.stroke();
    ctxBg1.fillStyle = '#38bdf8';
    ctxBg1.textAlign = 'left';
    ctxBg1.fillText('冰封臨界線 -10.1℃', margin.left + 8, yTice - 7);

    const yTland = margin.top + plotH * (1.0 - ((T_LAND - 273.15) - yMin1) / (yMax1 - yMin1));
    ctxBg1.strokeStyle = '#4ade80';
    ctxBg1.beginPath();
    ctxBg1.moveTo(margin.left, yTland);
    ctxBg1.lineTo(margin.left + plotW, yTland);
    ctxBg1.stroke();
    ctxBg1.fillStyle = '#4ade80';
    ctxBg1.fillText('無冰臨界線 9.9℃', margin.left + 8, yTland - 7);
    ctxBg1.restore();

    // X Ticks: 0 to itera*dt (e.g. 0 to 20 yrs)
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
        ctxBg1.fillText(xVal + '年', x, margin.top + plotH + 8);
    }}

    // Axis Border lines
    ctxBg1.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctxBg1.strokeRect(margin.left, margin.top, plotW, plotH);


    // --- Chart 2 Static BG (Radiation) ---
    ctxBg2.clearRect(0, 0, width, height);
    ctxBg2.fillStyle = 'rgba(15, 23, 42, 0.45)';
    ctxBg2.fillRect(margin.left, margin.top, plotW, plotH);

    const yMin2 = -20, yMax2 = 380;
    const yTicks2 = [0, 50, 100, 150, 200, 250, 300, 350];

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
        ctxBg2.fillText(val, margin.left - 8, y);
    }});

    for (let xVal = 0; xVal <= xMax; xVal += xStep) {{
        const x = margin.left + plotW * (xVal / xMax);
        ctxBg2.beginPath();
        ctxBg2.moveTo(x, margin.top);
        ctxBg2.lineTo(x, margin.top + plotH);
        ctxBg2.stroke();
        ctxBg2.fillText(xVal + '年', x, margin.top + plotH + 8);
    }}

    ctxBg2.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctxBg2.strokeRect(margin.left, margin.top, plotW, plotH);
}}

// Render ONLY dynamic line traces at 60 FPS (zero axis redraw!)
function renderDynamicTraces() {{
    if (!state.simData) return;

    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;
    const d = state.simData;
    const xMax = ITERA * DT;

    // --- Chart 1: Temperature Trace ---
    ctxFg1.clearRect(0, 0, width, height);
    const yMin1 = -45, yMax1 = 35;

    ctxFg1.save();
    ctxFg1.beginPath();
    ctxFg1.rect(margin.left, margin.top, plotW, plotH);
    ctxFg1.clip();

    // Glowing Neon Stroke
    ctxFg1.shadowBlur = 8;
    ctxFg1.shadowColor = '#00e5ff';
    ctxFg1.strokeStyle = '#00e5ff';
    ctxFg1.lineWidth = 2.8;
    ctxFg1.beginPath();

    for (let i = 0; i < d.t.length; i++) {{
        const x = margin.left + plotW * (d.t[i] / xMax);
        const y = margin.top + plotH * (1.0 - (d.TC[i] - yMin1) / (yMax1 - yMin1));
        if (i === 0) ctxFg1.moveTo(x, y);
        else ctxFg1.lineTo(x, y);
    }}
    ctxFg1.stroke();

    // Draw endpoint pulse marker
    const endX = margin.left + plotW;
    const endY = margin.top + plotH * (1.0 - (d.finalTC - yMin1) / (yMax1 - yMin1));
    ctxFg1.fillStyle = '#00e5ff';
    ctxFg1.beginPath();
    ctxFg1.arc(endX, endY, 5, 0, Math.PI * 2);
    ctxFg1.fill();
    ctxFg1.restore();

    // --- Chart 2: Radiation Traces ---
    ctxFg2.clearRect(0, 0, width, height);
    const yMin2 = -20, yMax2 = 380;

    ctxFg2.save();
    ctxFg2.beginPath();
    ctxFg2.rect(margin.left, margin.top, plotW, plotH);
    ctxFg2.clip();

    // 1. Rin (Amber)
    ctxFg2.shadowBlur = 6;
    ctxFg2.shadowColor = '#f59e0b';
    ctxFg2.strokeStyle = '#f59e0b';
    ctxFg2.lineWidth = 2.2;
    ctxFg2.beginPath();
    for (let i = 0; i < d.t.length; i++) {{
        const x = margin.left + plotW * (d.t[i] / xMax);
        const y = margin.top + plotH * (1.0 - (d.Rin[i] - yMin2) / (yMax2 - yMin2));
        if (i === 0) ctxFg2.moveTo(x, y);
        else ctxFg2.lineTo(x, y);
    }}
    ctxFg2.stroke();

    // 2. Rout (Red)
    ctxFg2.shadowColor = '#ef4444';
    ctxFg2.strokeStyle = '#ef4444';
    ctxFg2.lineWidth = 2.2;
    ctxFg2.beginPath();
    for (let i = 0; i < d.t.length; i++) {{
        const x = margin.left + plotW * (d.t[i] / xMax);
        const y = margin.top + plotH * (1.0 - (d.Rout[i] - yMin2) / (yMax2 - yMin2));
        if (i === 0) ctxFg2.moveTo(x, y);
        else ctxFg2.lineTo(x, y);
    }}
    ctxFg2.stroke();

    // 3. Imbalance (Purple dot)
    ctxFg2.shadowColor = '#a855f7';
    ctxFg2.strokeStyle = '#a855f7';
    ctxFg2.lineWidth = 1.6;
    ctxFg2.setLineDash([4, 3]);
    ctxFg2.beginPath();
    for (let i = 0; i < d.t.length; i++) {{
        const x = margin.left + plotW * (d.t[i] / xMax);
        const y = margin.top + plotH * (1.0 - (d.imbalance[i] - yMin2) / (yMax2 - yMin2));
        if (i === 0) ctxFg2.moveTo(x, y);
        else ctxFg2.lineTo(x, y);
    }}
    ctxFg2.stroke();
    ctxFg2.restore();

    // Update Live Stat Cards
    statT.innerText = d.finalT.toFixed(2) + ' K';
    statTC.innerText = d.finalTC.toFixed(2) + ' ℃';
    statAlbedo.innerText = d.finalAlbedo.toFixed(3);
    statRad.innerText = d.finalRin.toFixed(1) + ' W/m²';
    statRout.innerText = '出射: ' + d.finalRout.toFixed(1) + ' W/m²';
    statImbalance.innerText = d.finalImbalance.toFixed(4) + ' W/m²';

    if (d.finalTC < -20) {{
        statStateDesc.innerText = '❄️ 冰球雪球地球態 (Snowball)';
        statT.style.color = '#38bdf8';
    }} else if (d.finalTC < 5) {{
        statStateDesc.innerText = '⚠️ 臨界轉折過渡態';
        statT.style.color = '#fbbf24';
    }} else {{
        statStateDesc.innerText = '🌿 溫暖繁茂態 (Modern Warm)';
        statT.style.color = '#00e5ff';
    }}

    statEqStatus.innerText = Math.abs(d.finalImbalance) < 0.01 ? '已達完美熱力平衡' : '淨能量微幅傳遞中';
}}

// 60 FPS Animation Loop
let animFrameId = null;

function animationStep() {{
    if (!state.isPlaying) return;

    const speed = parseFloat(numAnimSpeed.value) || 0.8;
    const target = selAnimTarget.value;
    const dirMode = selAnimDir.value;

    let minV = 800, maxV = 2000;
    if (target === 's0') {{ minV = 800; maxV = 2000; }}
    else if (target === 't_init') {{ minV = 200; maxV = 320; }}
    else if (target === 'eps') {{ minV = 0.4; maxV = 0.9; }}
    else if (target === 'alpha_ice') {{ minV = 0.4; maxV = 0.8; }}

    let curVal = state[target];

    if (dirMode === 'pingpong') {{
        curVal += state.pingPongDir * speed;
        if (curVal >= maxV) {{
            curVal = maxV;
            state.pingPongDir = -1;
        }} else if (curVal <= minV) {{
            curVal = minV;
            state.pingPongDir = 1;
        }}
    }} else if (dirMode === 'inc') {{
        curVal += speed;
        if (curVal >= maxV) {{
            curVal = maxV;
            togglePlay();
        }}
    }} else if (dirMode === 'dec') {{
        curVal -= speed;
        if (curVal <= minV) {{
            curVal = minV;
            togglePlay();
        }}
    }}

    state[target] = curVal;

    // Sync input sliders & badges
    if (target === 's0') {{
        sliderS0.value = curVal;
        badgeS0.innerText = curVal.toFixed(1);
    }} else if (target === 't_init') {{
        sliderTinit.value = curVal;
        badgeTinit.innerText = curVal.toFixed(1);
    }} else if (target === 'eps') {{
        sliderEps.value = curVal;
        badgeEps.innerText = curVal.toFixed(2);
    }} else if (target === 'alpha_ice') {{
        sliderAice.value = curVal;
        badgeAice.innerText = curVal.toFixed(2);
    }}

    // Integrate & render smoothly
    runSimulation();
    renderDynamicTraces();

    animFrameId = requestAnimationFrame(animationStep);
}}

function togglePlay() {{
    state.isPlaying = !state.isPlaying;
    if (state.isPlaying) {{
        btnTogglePlay.innerText = '⏸️ 暫停動態演變';
        btnTogglePlay.style.background = 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)';
        animFrameId = requestAnimationFrame(animationStep);
    }} else {{
        btnTogglePlay.innerText = '▶️ 開始 60 FPS 絲滑動態演變';
        btnTogglePlay.style.background = 'linear-gradient(135deg, #00e5ff 0%, #0284c7 100%)';
        if (animFrameId) cancelAnimationFrame(animFrameId);
    }}
}}

// User Input Listeners
sliderS0.addEventListener('input', e => {{
    state.s0 = parseFloat(e.target.value);
    badgeS0.innerText = state.s0.toFixed(1);
    runSimulation();
    renderDynamicTraces();
}});

sliderTinit.addEventListener('input', e => {{
    state.t_init = parseFloat(e.target.value);
    badgeTinit.innerText = state.t_init.toFixed(1);
    runSimulation();
    renderDynamicTraces();
}});

sliderEps.addEventListener('input', e => {{
    state.epsilon = parseFloat(e.target.value);
    badgeEps.innerText = state.epsilon.toFixed(2);
    runSimulation();
    renderDynamicTraces();
}});

sliderAice.addEventListener('input', e => {{
    state.alpha_ice = parseFloat(e.target.value);
    badgeAice.innerText = state.alpha_ice.toFixed(2);
    runSimulation();
    renderDynamicTraces();
}});

btnTogglePlay.addEventListener('click', togglePlay);

btnReset.addEventListener('click', () => {{
    state.s0 = 1368.0;
    state.t_init = 288.0;
    state.epsilon = 0.62;
    state.alpha_ice = 0.60;
    sliderS0.value = 1368.0; badgeS0.innerText = '1368.0';
    sliderTinit.value = 288.0; badgeTinit.innerText = '288.0';
    sliderEps.value = 0.62; badgeEps.innerText = '0.62';
    sliderAice.value = 0.60; badgeAice.innerText = '0.60';
    runSimulation();
    renderDynamicTraces();
}});

// Interactive Tooltip Hover on Chart 1
fg1.addEventListener('mousemove', e => {{
    const rect = fg1.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const plotW = width - margin.left - margin.right;
    if (mouseX >= margin.left && mouseX <= margin.left + plotW) {{
        const normX = (mouseX - margin.left) / plotW;
        const idx = Math.min(ITERA, Math.max(0, Math.round(normX * ITERA)));
        const d = state.simData;
        if (d) {{
            tooltip.style.display = 'block';
            tooltip.style.left = (e.clientX + 14) + 'px';
            tooltip.style.top = (e.clientY - 25) + 'px';
            tooltip.innerHTML = `時間: ${{d.t[idx].toFixed(1)}} 年<br>溫度: ${{d.TC[idx].toFixed(2)}} ℃<br>反照率: ${{d.albedo[idx].toFixed(3)}}`;
            return;
        }}
    }}
    tooltip.style.display = 'none';
}});

fg1.addEventListener('mouseleave', () => {{
    tooltip.style.display = 'none';
}});

// Initialize
window.addEventListener('resize', resizeCanvases);
runSimulation();
setTimeout(resizeCanvases, 50);
</script>

</body>
</html>
"""
    return html_code
