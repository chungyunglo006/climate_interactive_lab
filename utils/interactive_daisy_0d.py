"""
Interactive 60 FPS Client-Side Canvas Engine for 0D Classic Daisyworld (Watson & Lovelock 1983).
Ensures coordinate axes, gridlines, and thresholds are rendered ONCE on a static layer,
while daisy population dynamics and temperature regulation update smoothly via requestAnimationFrame at 60 FPS.
Includes synchronized sliders + direct numeric keyboard inputs and scenario presets.
"""

def get_interactive_daisy0d_html(
    s0=917.0, l_val=1.0, alpha_w=0.75, alpha_b=0.25, alpha_u=0.5,
    q_val=20.0, gamma_val=0.3, aw_init=0.01, ab_init=0.01, dt=0.1, itera=150
):
    """Generates self-contained 60 FPS hardware-accelerated interactive canvas HTML for 0D Daisyworld."""
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
        <div class="panel-title">🌼 0D 經典雛菊世界物理參數面板 (滑桿 + 精確數值直接輸入)</div>
        <div style="display: flex; align-items: center; gap: 8px;">
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
        <button class="btn" id="btn_toggle_play">▶️ 開始 60 FPS 絲滑動態演變</button>
        <button class="btn btn-secondary" id="btn_reset">🔄 重設標準光度</button>

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

        <span style="color: #64748b;">速率 (Δ/幀):</span>
        <input type="number" class="inline-input" id="num_anim_speed" value="0.003" step="0.001" min="0.0005" max="0.03" style="width: 85px;">
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
            <div class="chart-title">🌡️ 行星溫度調控效應 vs 死星基線</div>
            <div class="chart-legend">
                <div class="legend-item"><div class="legend-color" style="background: #22c55e;"></div> 調節均溫 Tp</div>
                <div class="legend-item"><div class="legend-color" style="background: #ef4444; border-top: 1px dashed;"></div> 無生物死星</div>
                <div class="legend-item"><div class="legend-color" style="background: #00e5ff; border-top: 1px dotted;"></div> 最適點 22.5℃</div>
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
    isPlaying: false,
    pingPongDir: 1,
    simData: null
}};

// DOM Elements
const sliderL = document.getElementById('slider_l');
const numL = document.getElementById('num_l');
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

const btnTogglePlay = document.getElementById('btn_toggle_play');
const btnReset = document.getElementById('btn_reset');
const selAnimTarget = document.getElementById('sel_anim_target');
const selAnimDir = document.getElementById('sel_anim_dir');
const numAnimSpeed = document.getElementById('num_anim_speed');

const statTp = document.getElementById('stat_tp');
const statGaeaEval = document.getElementById('stat_gaea_eval');
const statTnobio = document.getElementById('stat_tnobio');
const statDeltaT = document.getElementById('stat_delta_t');
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
    let awList = [], abList = [], auList = [];
    let TpList = [], TwList = [], TbList = [];

    let aw = state.aw_init;
    let ab = state.ab_init;

    for (let step = 0; step <= ITERA; step++) {{
        const au = Math.max(0.0, Math.min(1.0, 1.0 - aw - ab));
        const alphaP = aw * state.alpha_w + ab * state.alpha_b + au * state.alpha_u;
        const TpK = Math.pow((state.s0 * state.l_val * (1.0 - alphaP)) / SIGMA, 0.25);
        const TpC = TpK - 273.15;

        const Tw = TpC + state.q_val * (alphaP - state.alpha_w);
        const Tb = TpC + state.q_val * (alphaP - state.alpha_b);

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

    const Tnobio = Math.pow((state.s0 * state.l_val * (1.0 - state.alpha_u)) / SIGMA, 0.25) - 273.15;

    state.simData = {{
        t, aw: awList, ab: abList, au: auList,
        Tp: TpList, Tw: TwList, Tb: TbList,
        finalTp: TpList[TpList.length - 1],
        finalAw: awList[awList.length - 1],
        finalAb: abList[abList.length - 1],
        finalTw: TwList[TwList.length - 1],
        finalTb: TbList[TbList.length - 1],
        Tnobio: Tnobio
    }};
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
        btnTogglePlay.innerText = '▶️ 開始 60 FPS 絲滑動態演變';
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

    numInput.addEventListener('input', e => {{
        const v = parseFloat(e.target.value);
        if (!isNaN(v)) {{
            slider.value = v;
            state[stateKey] = v;
            runSimulation();
            renderDynamicTraces();
        }}
    }});
}}

bindSync(sliderL, numL, 'l_val');
bindSync(sliderGamma, numGamma, 'gamma_val');
bindSync(sliderAw, numAw, 'alpha_w');
bindSync(sliderAb, numAb, 'alpha_b');
bindSync(sliderAu, numAu, 'alpha_u');
bindSync(sliderQ, numQ, 'q_val');

btnTogglePlay.addEventListener('click', togglePlay);

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

window.addEventListener('resize', resizeCanvases);
runSimulation();
setTimeout(resizeCanvases, 50);
</script>

</body>
</html>
"""
    return html_code
