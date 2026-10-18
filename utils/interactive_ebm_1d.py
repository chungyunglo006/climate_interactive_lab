"""
Interactive 60 FPS Client-Side Canvas Engine for 1D Latitudinal Energy Balance Model (Budyko-Sellers).
Ensures coordinate axes, gridlines, and thresholds are rendered ONCE on a static layer,
while latitudinal profiles and convergence traces update smoothly via requestAnimationFrame at 60 FPS.
Includes synchronized sliders + direct numeric keyboard inputs and scenario presets.
"""

def get_interactive_ebm1d_html(
    sc=1370.0, frac_sc=1.0, a_param=230.0, b_param=2.17, k_diff=3.87,
    aice=0.6, aland=0.3, tcrit=-10.0, itera=50
):
    """Generates self-contained 60 FPS hardware-accelerated interactive canvas HTML for 1D EBM."""
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
    <div class="panel-header">
        <div class="panel-title">🌐 1D 緯度能量平衡模型參數面板 (滑桿 + 精確數值直接輸入)</div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 0.8rem; color: #94a3b8;">🎯 預設情境:</span>
            <select id="sel_preset">
                <option value="modern" selected>現今地球 (Modern Earth - 冰蓋在 72°N)</option>
                <option value="snowball">完全冰球 (Snowball Earth)</option>
                <option value="warm">無冰極暖地球 (Ice-Free Earth)</option>
                <option value="low_diff">低大氣熱擴散 (弱經向熱輸送)</option>
                <option value="high_diff">強大氣熱擴散 (均勻化全球溫度)</option>
            </select>
        </div>
    </div>

    <div class="ctrl-grid">
        <div class="ctrl-item">
            <span class="ctrl-label"><span>太陽常數因子 Frac_SC</span><span>比例</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_frac_sc" min="0.70" max="1.30" step="0.01" value="{frac_sc}">
                <input type="number" class="val-input" id="num_frac_sc" min="0.70" max="1.30" step="0.01" value="{frac_sc}">
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label"><span>熱擴散係數 K</span><span>W/m²/℃</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_k" min="0.5" max="8.0" step="0.1" value="{k_diff}">
                <input type="number" class="val-input" id="num_k" min="0.5" max="8.0" step="0.1" value="{k_diff}">
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label"><span>冰雪臨界溫 T_crit</span><span>℃</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_tcrit" min="-25.0" max="0.0" step="0.5" value="{tcrit}">
                <input type="number" class="val-input" id="num_tcrit" min="-25.0" max="0.0" step="0.5" value="{tcrit}">
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label"><span>冰雪反照率 a_ice</span><span>反射比</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_aice" min="0.4" max="0.8" step="0.01" value="{aice}">
                <input type="number" class="val-input" id="num_aice" min="0.4" max="0.8" step="0.01" value="{aice}">
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label"><span>無冰反照率 a_land</span><span>反射比</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_aland" min="0.1" max="0.5" step="0.01" value="{aland}">
                <input type="number" class="val-input" id="num_aland" min="0.1" max="0.5" step="0.01" value="{aland}">
            </div>
        </div>
        <div class="ctrl-item">
            <span class="ctrl-label"><span>長波輻射截距 A</span><span>W/m²</span></span>
            <div class="ctrl-input-row">
                <input type="range" id="slider_a" min="180.0" max="280.0" step="1.0" value="{a_param}">
                <input type="number" class="val-input" id="num_a" min="180.0" max="280.0" step="1.0" value="{a_param}">
            </div>
        </div>
    </div>

    <div class="action-row">
        <button class="btn" id="btn_toggle_play">▶️ 開始 60 FPS 絲滑動態演變</button>
        <button class="btn btn-secondary" id="btn_reset">🔄 重設現代地球</button>

        <span style="color: #64748b; margin-left: 8px;">演變變數:</span>
        <select id="sel_anim_target">
            <option value="frac_sc">太陽常數因子 Frac_SC</option>
            <option value="k">熱擴散係數 K</option>
            <option value="tcrit">冰雪臨界溫 T_crit</option>
            <option value="aice">冰雪反照率 a_ice</option>
        </select>

        <span style="color: #64748b;">方向:</span>
        <select id="sel_anim_dir">
            <option value="pingpong">來回擺動 (Ping-Pong)</option>
            <option value="inc">往大增加 (+)</option>
            <option value="dec">往小減少 (-)</option>
        </select>

        <span style="color: #64748b;">速率 (Δ/幀):</span>
        <input type="number" class="inline-input" id="num_anim_speed" value="0.002" step="0.001" min="0.0005" max="0.05" style="width: 85px;">
    </div>
</div>

<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-title">全球面積加權均溫</div>
        <div class="stat-val" id="stat_mean_t" style="color: #00e5ff;">-- ℃</div>
        <div class="stat-sub" id="stat_climate_state">狀態評估中...</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">冰雪前緣最低緯度</div>
        <div class="stat-val" id="stat_ice_edge" style="color: #38bdf8;">-- °N</div>
        <div class="stat-sub" id="stat_ice_desc">臨界結冰邊界</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">赤道 - 極區溫差</div>
        <div class="stat-val" id="stat_dt_pole" style="color: #f59e0b;">-- ℃</div>
        <div class="stat-sub">赤道 (6°N) vs 極區 (85°N)</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">極區平衡溫度</div>
        <div class="stat-val" id="stat_pole_t" style="color: #4ade80;">-- ℃</div>
        <div class="stat-sub" id="stat_pole_sub">緯度 85°N</div>
    </div>
</div>

<div class="charts-grid">
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">🌐 緯度 vs 平衡溫度剖面 (60 FPS 絲滑形變)</div>
            <div class="chart-legend">
                <div class="legend-item"><div class="legend-color" style="background: #ef4444;"></div> 平衡溫度 (℃)</div>
                <div class="legend-item"><div class="legend-color" style="background: #38bdf8; border-top: 1px dashed;"></div> 結冰臨界 (T_crit)</div>
            </div>
        </div>
        <div class="canvas-container" id="container1">
            <canvas id="bg1"></canvas>
            <canvas id="fg1"></canvas>
        </div>
    </div>

    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">🧊 緯度 vs 階梯反照率分佈 (Albedo Step)</div>
            <div class="chart-legend">
                <div class="legend-item"><div class="legend-color" style="background: #00e5ff;"></div> 階梯反照率 (Albedo)</div>
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
const LATS_DEFAULT = [85.0, 75.0, 65.0, 55.0, 45.0, 35.0, 25.0, 15.0, 6.0];
const SUNWT_DEFAULT = [0.5, 0.531, 0.624, 0.77, 0.892, 1.021, 1.12, 1.189, 1.219];
const INIT_T_DEFAULT = [-15.0, -15.0, -5.0, 5.0, 10.0, 15.0, 18.0, 22.0, 24.0];

const latCos = LATS_DEFAULT.map(lat => Math.cos(lat * Math.PI / 180.0));
const sumCos = latCos.reduce((a, b) => a + b, 0);

// Mirror coordinates for symmetric global display [-85 to +85]
const fullLats = [];
for (let i = LATS_DEFAULT.length - 1; i >= 0; i--) fullLats.push(-LATS_DEFAULT[i]);
for (let i = 0; i < LATS_DEFAULT.length; i++) fullLats.push(LATS_DEFAULT[i]);

let state = {{
    sc: {sc},
    frac_sc: {frac_sc},
    a: {a_param},
    b: {b_param},
    k: {k_diff},
    aice: {aice},
    aland: {aland},
    tcrit: {tcrit},
    itera: {itera},
    isPlaying: false,
    pingPongDir: 1,
    simData: null
}};

// DOM Elements
const sliderFracSc = document.getElementById('slider_frac_sc');
const numFracSc = document.getElementById('num_frac_sc');
const sliderK = document.getElementById('slider_k');
const numK = document.getElementById('num_k');
const sliderTcrit = document.getElementById('slider_tcrit');
const numTcrit = document.getElementById('num_tcrit');
const sliderAice = document.getElementById('slider_aice');
const numAice = document.getElementById('num_aice');
const sliderAland = document.getElementById('slider_aland');
const numAland = document.getElementById('num_aland');
const sliderA = document.getElementById('slider_a');
const numA = document.getElementById('num_a');
const selPreset = document.getElementById('sel_preset');

const btnTogglePlay = document.getElementById('btn_toggle_play');
const btnReset = document.getElementById('btn_reset');
const selAnimTarget = document.getElementById('sel_anim_target');
const selAnimDir = document.getElementById('sel_anim_dir');
const numAnimSpeed = document.getElementById('num_anim_speed');

const statMeanT = document.getElementById('stat_mean_t');
const statClimateState = document.getElementById('stat_climate_state');
const statIceEdge = document.getElementById('stat_ice_edge');
const statDtPole = document.getElementById('stat_dt_pole');
const statPoleT = document.getElementById('stat_pole_t');

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

// 1D EBM Solver
function runSimulation() {{
    const Rin = SUNWT_DEFAULT.map(wt => (state.sc / 4.0) * state.frac_sc * wt);
    let temp = [...INIT_T_DEFAULT];
    let albedo = temp.map(t => t < state.tcrit ? state.aice : state.aland);

    for (let step = 0; step < state.itera; step++) {{
        const meanT = temp.reduce((acc, t, i) => acc + t * latCos[i], 0) / sumCos;
        temp = Rin.map((rin, i) => {{
            const alb = albedo[i];
            return (rin * (1.0 - alb) + state.k * meanT - state.a) / (state.b + state.k);
        }});
        albedo = temp.map(t => t < state.tcrit ? state.aice : state.aland);
    }}

    const meanT = temp.reduce((acc, t, i) => acc + t * latCos[i], 0) / sumCos;
    const iceLats = LATS_DEFAULT.filter((lat, i) => temp[i] < state.tcrit);
    const iceEdge = iceLats.length > 0 ? Math.min(...iceLats) : 90.0;

    // Full symmetric arrays for global lat display
    const fullTemp = [];
    const fullAlbedo = [];
    for (let i = temp.length - 1; i >= 0; i--) {{ fullTemp.push(temp[i]); fullAlbedo.push(albedo[i]); }}
    for (let i = 0; i < temp.length; i++) {{ fullTemp.push(temp[i]); fullAlbedo.push(albedo[i]); }}

    state.simData = {{
        lats: fullLats,
        temp: fullTemp,
        albedo: fullAlbedo,
        meanT: meanT,
        iceEdge: iceEdge,
        equatorT: temp[temp.length - 1],
        poleT: temp[0]
    }};
}}

// Static Axes (Drawn ONCE, 0 redraws)
function drawStaticBackgrounds() {{
    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;

    // --- Chart 1 Static BG (Temperature) ---
    ctxBg1.clearRect(0, 0, width, height);
    ctxBg1.fillStyle = 'rgba(15, 23, 42, 0.45)';
    ctxBg1.fillRect(margin.left, margin.top, plotW, plotH);

    const yMin1 = -60, yMax1 = 45;
    const yTicks1 = [-50, -30, -10, 0, 15, 30, 45];

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

    // Critical threshold dashed line
    const yTcrit = margin.top + plotH * (1.0 - (state.tcrit - yMin1) / (yMax1 - yMin1));
    ctxBg1.save();
    ctxBg1.setLineDash([5, 4]);
    ctxBg1.strokeStyle = '#38bdf8';
    ctxBg1.beginPath();
    ctxBg1.moveTo(margin.left, yTcrit);
    ctxBg1.lineTo(margin.left + plotW, yTcrit);
    ctxBg1.stroke();
    ctxBg1.fillStyle = '#38bdf8';
    ctxBg1.textAlign = 'left';
    ctxBg1.fillText('結冰臨界 T_crit ' + state.tcrit.toFixed(1) + '℃', margin.left + 8, yTcrit - 7);
    ctxBg1.restore();

    // X Ticks: -90 to +90 deg
    const xTicks = [-90, -60, -30, 0, 30, 60, 90];
    ctxBg1.textAlign = 'center';
    ctxBg1.textBaseline = 'top';

    xTicks.forEach(lat => {{
        const x = margin.left + plotW * ((lat + 90.0) / 180.0);
        ctxBg1.beginPath();
        ctxBg1.moveTo(x, margin.top);
        ctxBg1.lineTo(x, margin.top + plotH);
        ctxBg1.stroke();
        const lbl = lat === 0 ? '赤道' : (lat > 0 ? lat + '°N' : Math.abs(lat) + '°S');
        ctxBg1.fillText(lbl, x, margin.top + plotH + 8);
    }});

    ctxBg1.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctxBg1.strokeRect(margin.left, margin.top, plotW, plotH);


    // --- Chart 2 Static BG (Albedo) ---
    ctxBg2.clearRect(0, 0, width, height);
    ctxBg2.fillStyle = 'rgba(15, 23, 42, 0.45)';
    ctxBg2.fillRect(margin.left, margin.top, plotW, plotH);

    const yMin2 = 0.0, yMax2 = 1.0;
    const yTicks2 = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0];

    ctxBg2.font = '11px "JetBrains Mono", monospace';
    ctxBg2.fillStyle = '#64748b';
    ctxBg2.textAlign = 'right';
    ctxBg2.textBaseline = 'middle';
    ctxBg2.strokeStyle = 'rgba(255, 255, 255, 0.07)';
    ctxBg2.lineWidth = 1;

    yTicks2.forEach(val => {{
        const y = margin.top + plotH * (1.0 - val);
        ctxBg2.beginPath();
        ctxBg2.moveTo(margin.left, y);
        ctxBg2.lineTo(margin.left + plotW, y);
        ctxBg2.stroke();
        ctxBg2.fillText(val.toFixed(1), margin.left - 8, y);
    }});

    xTicks.forEach(lat => {{
        const x = margin.left + plotW * ((lat + 90.0) / 180.0);
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

// Dynamic Traces (60 FPS)
function renderDynamicTraces() {{
    if (!state.simData) return;

    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;
    const d = state.simData;

    // --- Chart 1: Temperature Profile ---
    ctxFg1.clearRect(0, 0, width, height);
    const yMin1 = -60, yMax1 = 45;

    ctxFg1.save();
    ctxFg1.beginPath();
    ctxFg1.rect(margin.left, margin.top, plotW, plotH);
    ctxFg1.clip();

    ctxFg1.shadowBlur = 8;
    ctxFg1.shadowColor = '#ef4444';
    ctxFg1.strokeStyle = '#ef4444';
    ctxFg1.lineWidth = 3.0;
    ctxFg1.beginPath();

    for (let i = 0; i < d.lats.length; i++) {{
        const x = margin.left + plotW * ((d.lats[i] + 90.0) / 180.0);
        const y = margin.top + plotH * (1.0 - (d.temp[i] - yMin1) / (yMax1 - yMin1));
        if (i === 0) ctxFg1.moveTo(x, y);
        else ctxFg1.lineTo(x, y);
    }}
    ctxFg1.stroke();

    // Data points markers
    d.lats.forEach((lat, i) => {{
        const x = margin.left + plotW * ((lat + 90.0) / 180.0);
        const y = margin.top + plotH * (1.0 - (d.temp[i] - yMin1) / (yMax1 - yMin1));
        ctxFg1.fillStyle = '#ef4444';
        ctxFg1.beginPath();
        ctxFg1.arc(x, y, 4, 0, Math.PI * 2);
        ctxFg1.fill();
    }});
    ctxFg1.restore();


    // --- Chart 2: Albedo Profile ---
    ctxFg2.clearRect(0, 0, width, height);

    ctxFg2.save();
    ctxFg2.beginPath();
    ctxFg2.rect(margin.left, margin.top, plotW, plotH);
    ctxFg2.clip();

    ctxFg2.shadowBlur = 8;
    ctxFg2.shadowColor = '#00e5ff';
    ctxFg2.strokeStyle = '#00e5ff';
    ctxFg2.lineWidth = 2.8;
    ctxFg2.beginPath();

    for (let i = 0; i < d.lats.length; i++) {{
        const x = margin.left + plotW * ((d.lats[i] + 90.0) / 180.0);
        const y = margin.top + plotH * (1.0 - d.albedo[i]);
        if (i === 0) ctxFg2.moveTo(x, y);
        else ctxFg2.lineTo(x, y);
    }}
    ctxFg2.stroke();

    d.lats.forEach((lat, i) => {{
        const x = margin.left + plotW * ((lat + 90.0) / 180.0);
        const y = margin.top + plotH * (1.0 - d.albedo[i]);
        ctxFg2.fillStyle = '#00e5ff';
        ctxFg2.fillRect(x - 3.5, y - 3.5, 7, 7);
    }});
    ctxFg2.restore();

    // Update Stats
    statMeanT.innerText = d.meanT.toFixed(2) + ' ℃';
    statIceEdge.innerText = d.iceEdge >= 90 ? '無冰蓋 (Ice-Free)' : d.iceEdge.toFixed(0) + ' °N';
    statDtPole.innerText = (d.equatorT - d.poleT).toFixed(1) + ' ℃';
    statPoleT.innerText = d.poleT.toFixed(1) + ' ℃';

    if (d.meanT < -15) {{
        statClimateState.innerText = '❄️ 冰球雪球地球態 (Snowball Earth)';
        statMeanT.style.color = '#38bdf8';
    }} else if (d.iceEdge < 90) {{
        statClimateState.innerText = '🌿 現代極區冰蓋態 (Seasonal Polar Cap)';
        statMeanT.style.color = '#00e5ff';
    }} else {{
        statClimateState.innerText = '☀️ 無冰超溫暖水世界 (Ice-Free Waterworld)';
        statMeanT.style.color = '#fbbf24';
    }}
}}

// 60 FPS Animation Loop
let animFrameId = null;

function animationStep() {{
    if (!state.isPlaying) return;

    const speed = parseFloat(numAnimSpeed.value) || 0.002;
    const target = selAnimTarget.value;
    const dirMode = selAnimDir.value;

    let minV = 0.70, maxV = 1.30;
    if (target === 'frac_sc') {{ minV = 0.70; maxV = 1.30; }}
    else if (target === 'k') {{ minV = 0.5; maxV = 8.0; }}
    else if (target === 'tcrit') {{ minV = -25.0; maxV = 0.0; }}
    else if (target === 'aice') {{ minV = 0.4; maxV = 0.8; }}

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
    if (target === 'frac_sc') {{
        sliderFracSc.value = val; numFracSc.value = val.toFixed(2);
    }} else if (target === 'k') {{
        sliderK.value = val; numK.value = val.toFixed(1);
    }} else if (target === 'tcrit') {{
        sliderTcrit.value = val; numTcrit.value = val.toFixed(1);
    }} else if (target === 'aice') {{
        sliderAice.value = val; numAice.value = val.toFixed(2);
    }}
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

function bindSync(slider, numInput, stateKey, isInt=false) {{
    slider.addEventListener('input', e => {{
        const v = isInt ? parseInt(e.target.value) : parseFloat(e.target.value);
        numInput.value = v;
        state[stateKey] = v;
        runSimulation();
        renderDynamicTraces();
    }});

    numInput.addEventListener('input', e => {{
        const v = isInt ? parseInt(e.target.value) : parseFloat(e.target.value);
        if (!isNaN(v)) {{
            slider.value = v;
            state[stateKey] = v;
            runSimulation();
            renderDynamicTraces();
        }}
    }});
}}

bindSync(sliderFracSc, numFracSc, 'frac_sc');
bindSync(sliderK, numK, 'k');
bindSync(sliderTcrit, numTcrit, 'tcrit');
bindSync(sliderAice, numAice, 'aice');
bindSync(sliderAland, numAland, 'aland');
bindSync(sliderA, numA, 'a');

btnTogglePlay.addEventListener('click', togglePlay);

// Scenario Presets
selPreset.addEventListener('change', e => {{
    const p = e.target.value;
    if (p === 'modern') {{
        setParams({{ frac_sc: 1.0, k: 3.87, tcrit: -10.0, aice: 0.60, aland: 0.30, a: 230.0 }});
    }} else if (p === 'snowball') {{
        setParams({{ frac_sc: 0.85, k: 3.87, tcrit: -10.0, aice: 0.60, aland: 0.30, a: 230.0 }});
    }} else if (p === 'warm') {{
        setParams({{ frac_sc: 1.15, k: 3.87, tcrit: -10.0, aice: 0.60, aland: 0.30, a: 230.0 }});
    }} else if (p === 'low_diff') {{
        setParams({{ frac_sc: 1.0, k: 1.0, tcrit: -10.0, aice: 0.60, aland: 0.30, a: 230.0 }});
    }} else if (p === 'high_diff') {{
        setParams({{ frac_sc: 1.0, k: 7.0, tcrit: -10.0, aice: 0.60, aland: 0.30, a: 230.0 }});
    }}
}});

function setParams(cfg) {{
    if (cfg.frac_sc !== undefined) {{ state.frac_sc = cfg.frac_sc; sliderFracSc.value = cfg.frac_sc; numFracSc.value = cfg.frac_sc; }}
    if (cfg.k !== undefined) {{ state.k = cfg.k; sliderK.value = cfg.k; numK.value = cfg.k; }}
    if (cfg.tcrit !== undefined) {{ state.tcrit = cfg.tcrit; sliderTcrit.value = cfg.tcrit; numTcrit.value = cfg.tcrit; }}
    if (cfg.aice !== undefined) {{ state.aice = cfg.aice; sliderAice.value = cfg.aice; numAice.value = cfg.aice; }}
    if (cfg.aland !== undefined) {{ state.aland = cfg.aland; sliderAland.value = cfg.aland; numAland.value = cfg.aland; }}
    if (cfg.a !== undefined) {{ state.a = cfg.a; sliderA.value = cfg.a; numA.value = cfg.a; }}
    drawStaticBackgrounds();
    runSimulation();
    renderDynamicTraces();
}}

btnReset.addEventListener('click', () => {{
    selPreset.value = 'modern';
    setParams({{ frac_sc: 1.0, k: 3.87, tcrit: -10.0, aice: 0.60, aland: 0.30, a: 230.0 }});
}});

// Tooltip on Chart 1
fg1.addEventListener('mousemove', e => {{
    const rect = fg1.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const plotW = width - margin.left - margin.right;
    if (mouseX >= margin.left && mouseX <= margin.left + plotW) {{
        const normX = (mouseX - margin.left) / plotW;
        const lat = -90.0 + normX * 180.0;
        const d = state.simData;
        if (d) {{
            // Find closest lat
            let closestIdx = 0;
            let minDiff = 999;
            d.lats.forEach((l, idx) => {{
                const diff = Math.abs(l - lat);
                if (diff < minDiff) {{ minDiff = diff; closestIdx = idx; }}
            }});

            tooltip.style.display = 'block';
            tooltip.style.left = (e.clientX + 14) + 'px';
            tooltip.style.top = (e.clientY - 25) + 'px';
            const latStr = d.lats[closestIdx] === 0 ? '赤道' : (d.lats[closestIdx] > 0 ? d.lats[closestIdx] + '°N' : Math.abs(d.lats[closestIdx]) + '°S');
            tooltip.innerHTML = `緯度: ${{latStr}}<br>平衡溫度: ${{d.temp[closestIdx].toFixed(2)}} ℃<br>反照率: ${{d.albedo[closestIdx].toFixed(2)}}`;
            return;
        }}
    }}
    tooltip.style.display = 'none';
}});

fg1.addEventListener('mouseleave', () => {{
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
