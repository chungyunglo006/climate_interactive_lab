"""
1D Latitudinal Energy Balance Model (1D EBM - Budyko-Sellers Type) Module.
Implements:
- 1D latitudinal temperature diffusion and energy balance
- Step-by-step convergence history
- Parameter sensitivity sweep across solar fraction or diffusion coefficient
"""

import math
import numpy as np
import pandas as pd

LATITUDE_LIST_DEFAULT = [85.0, 75.0, 65.0, 55.0, 45.0, 35.0, 25.0, 15.0, 6.0]
SUNWT_LIST_DEFAULT = [0.5, 0.531, 0.624, 0.77, 0.892, 1.021, 1.12, 1.189, 1.219]
INIT_T_LIST_DEFAULT = [-15.0, -15.0, -5.0, 5.0, 10.0, 15.0, 18.0, 22.0, 24.0]


def run_ebm_1d(SC=1370.0, Frac_SC=1.0, A=230.0, B=2.17, K=3.87, aice=0.6, a=0.3,
               Tcrit=-10.0, itera=50, init_T=None):
    """
    一維緯度能量平衡模型 (1D EBM) 迭代模擬器
    """
    latitude_list = list(LATITUDE_LIST_DEFAULT)
    SunWt_list = list(SUNWT_LIST_DEFAULT)
    Init_T_list = list(init_T) if init_T is not None else list(INIT_T_LIST_DEFAULT)

    lat_cos_list = [math.cos(math.radians(lat)) for lat in latitude_list]
    sum_cos = sum(lat_cos_list)
    R_in = [(SC / 4.0 * Frac_SC * wt) for wt in SunWt_list]

    albedo = [aice if t < Tcrit else a for t in Init_T_list]
    temp = list(Init_T_list)

    def step(t_current, alb_current):
        t_cos = [t * cos for t, cos in zip(t_current, lat_cos_list)]
        mean_t = sum(t_cos) / sum_cos

        t_next = [((rin * (1.0 - alb) + K * mean_t - A) / (B + K))
                  for rin, alb in zip(R_in, alb_current)]

        alb_next = [aice if t < Tcrit else a for t in t_next]
        return t_next, alb_next

    for _ in range(itera):
        temp, albedo = step(temp, albedo)

    t_cos = [t * cos for t, cos in zip(temp, lat_cos_list)]
    final_mean_t = sum(t_cos) / sum_cos

    R_out = [(t * B + A) for t in temp]
    F_i = [(K * (t - final_mean_t)) for t in temp]
    R_absorbed = [rin * (1.0 - alb) for rin, alb in zip(R_in, albedo)]
    balance = [round(out + f - absb, 5) for absb, out, f in zip(R_absorbed, R_out, F_i)]

    df = pd.DataFrame({
        "緯度 (度)": latitude_list,
        "太陽權重 (SunWt)": SunWt_list,
        "面積權重 (cos)": lat_cos_list,
        "入射能量 (R_in)": R_in,
        "最終溫度 (℃)": temp,
        "最終反照率 (Albedo)": albedo,
        "出射輻射 (R_out)": R_out,
        "傳導通量 (F)": F_i,
        "吸收能量": R_absorbed,
        "守恆差值 (Balance)": balance
    })

    return df, final_mean_t


def run_ebm_1d_history(SC=1370.0, Frac_SC=1.0, A=230.0, B=2.17, K=3.87, aice=0.6, a=0.3,
                       Tcrit=-10.0, itera=50, init_T=None):
    """
    動態迭代演變記錄器，記錄每一步各緯度溫度、反照率與全球均溫。
    """
    latitude_list = list(LATITUDE_LIST_DEFAULT)
    SunWt_list = list(SUNWT_LIST_DEFAULT)
    Init_T_list = list(init_T) if init_T is not None else list(INIT_T_LIST_DEFAULT)

    lat_cos_list = [math.cos(math.radians(lat)) for lat in latitude_list]
    sum_cos = sum(lat_cos_list)
    R_in = [(SC / 4.0 * Frac_SC * wt) for wt in SunWt_list]
    albedo = [aice if t < Tcrit else a for t in Init_T_list]
    temp = list(Init_T_list)

    history = []

    for step in range(itera + 1):
        t_cos = [t * cos for t, cos in zip(temp, lat_cos_list)]
        mean_t = sum(t_cos) / sum_cos

        # Identify ice-edge latitude (lowest latitude with T < Tcrit)
        ice_lats = [lat for lat, t in zip(latitude_list, temp) if t < Tcrit]
        ice_edge = min(ice_lats) if ice_lats else 90.0

        history.append({
            "step": step,
            "temp": list(temp),
            "albedo": list(albedo),
            "mean_t": mean_t,
            "ice_edge": ice_edge
        })

        if step < itera:
            temp = [((rin * (1.0 - alb) + K * mean_t - A) / (B + K)) for rin, alb in zip(R_in, albedo)]
            albedo = [aice if t < Tcrit else a for t in temp]

    return history, latitude_list


def sweep_ebm_1d_parameter(param_name="Frac_SC", start_val=0.75, end_val=1.2, num_steps=25,
                           base_config=None):
    """
    Performs parameter sweep on 1D EBM, e.g. varying solar fraction Frac_SC or diffusion K.
    Returns: list of results containing parameter value, final temperatures, mean temp, ice edge.
    """
    if base_config is None:
        base_config = {
            "SC": 1370.0, "Frac_SC": 1.0, "A": 230.0, "B": 2.17, "K": 3.87,
            "aice": 0.6, "a": 0.3, "Tcrit": -10.0, "itera": 50
        }

    val_range = np.linspace(start_val, end_val, num_steps)
    sweep_results = []

    for val in val_range:
        cfg = dict(base_config)
        cfg[param_name] = float(val)
        df, mean_t = run_ebm_1d(**cfg)

        temp_list = df["最終溫度 (℃)"].tolist()
        ice_lats = [lat for lat, t in zip(df["緯度 (度)"], temp_list) if t < cfg.get("Tcrit", -10.0)]
        ice_edge = min(ice_lats) if ice_lats else 90.0

        sweep_results.append({
            param_name: float(val),
            "mean_t": mean_t,
            "ice_edge": ice_edge,
            "temp_profile": temp_list,
            "latitude_list": df["緯度 (度)"].tolist(),
            "albedo_profile": df["最終反照率 (Albedo)"].tolist()
        })

    return sweep_results
