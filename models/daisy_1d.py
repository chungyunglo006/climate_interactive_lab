"""
1D Latitudinal Daisyworld Model Module (Classic & Grey Daisies).
Implements:
- 1D Latitudinal Classic Daisyworld (9 latitude zones, latitudinal heat transport, local daisy growth)
- 1D Latitudinal Grey Daisyworld (3-species geographic niche differentiation)
- Dual physics modes:
  * "atmosphere" (with greenhouse atmosphere & meridional diffusion K)
  * "airless" (no atmosphere: K=0, pure Stefan-Boltzmann blackbody radiation balance)
- Baseline abiotic temperature profiles
"""

import math
import numpy as np
import pandas as pd

LATITUDE_LIST_1D = [85.0, 75.0, 65.0, 55.0, 45.0, 35.0, 25.0, 15.0, 6.0]
SUNWT_LIST_1D = [0.5, 0.531, 0.624, 0.77, 0.892, 1.021, 1.12, 1.189, 1.219]
SIGMA = 5.670374e-8


def run_daisyworld_1d(S0=2100.0, L=1.0, alpha_w=0.75, alpha_b=0.25, alpha_u=0.5,
                      q=20.0, gamma=0.3, aw_init=0.01, ab_init=0.01, dt=0.1, itera=150,
                      A=230.0, B=2.17, K=3.87, physics_mode="atmosphere"):
    """
    一維緯度經典雛菊世界迭代模擬器
    physics_mode: "atmosphere" (有大氣熱傳輸與溫室) 或 "airless" (無大氣純黑體輻射，K=0)
    """
    latitude_list = list(LATITUDE_LIST_1D)
    SunWt_list = list(SUNWT_LIST_1D)
    n_lat = len(latitude_list)
    is_airless = (physics_mode == "airless")

    lat_cos_list = [math.cos(math.radians(lat)) for lat in latitude_list]
    sum_cos = sum(lat_cos_list)
    R_in = np.array([(S0 / 4.0 * L * wt) for wt in SunWt_list])

    aw = np.full(n_lat, float(aw_init))
    ab = np.full(n_lat, float(ab_init))
    history = []
    temp = np.full(n_lat, 15.0)

    for step in range(itera + 1):
        au = 1.0 - aw - ab
        au = np.clip(au, 0.0, 1.0)
        alpha_p = aw * alpha_w + ab * alpha_b + au * alpha_u

        if not is_airless:
            # 有大氣：Budyko 溫室長波冷卻 + 經向熱擴散 K
            for _ in range(20):
                mean_t = np.sum(temp * lat_cos_list) / sum_cos
                temp = (R_in * (1.0 - alpha_p) + K * mean_t - A) / (B + K)
        else:
            # 無大氣：無經向輸送 (K=0) + Stefan-Boltzmann 純輻射平衡
            absorbed = np.maximum(1.0, R_in * (1.0 - alpha_p))
            temp = ((absorbed / SIGMA) ** 0.25) - 273.15

        # Local daisy temperatures
        Tw = temp + q * (alpha_p - alpha_w)
        Tb = temp + q * (alpha_p - alpha_b)

        beta_w = np.maximum(0.0, 1.0 - 0.003265 * ((22.5 - Tw) ** 2))
        beta_b = np.maximum(0.0, 1.0 - 0.003265 * ((22.5 - Tb) ** 2))

        history.append({
            "step": step,
            "time": step * dt,
            "temp": temp.copy(),
            "aw": aw.copy(),
            "ab": ab.copy(),
            "au": au.copy(),
            "alpha_p": alpha_p.copy(),
            "mean_t": float(np.sum(temp * lat_cos_list) / sum_cos)
        })

        daw = aw * (au * beta_w - gamma)
        dab = ab * (au * beta_b - gamma)

        aw = np.clip(aw + dt * daw, 0.001, 0.99)
        ab = np.clip(ab + dt * dab, 0.001, 0.99)

        over_mask = (aw + ab) > 0.99
        if np.any(over_mask):
            scale = 0.99 / (aw + ab)
            aw = np.where(over_mask, aw * scale, aw)
            ab = np.where(over_mask, ab * scale, ab)

    # Calculate abiotic baseline temperature profile
    if not is_airless:
        temp_nobio = np.full(n_lat, 15.0)
        for _ in range(30):
            mean_t_nobio = np.sum(temp_nobio * lat_cos_list) / sum_cos
            temp_nobio = (R_in * (1.0 - alpha_u) + K * mean_t_nobio - A) / (B + K)
    else:
        absorbed_dead = np.maximum(1.0, R_in * (1.0 - alpha_u))
        temp_nobio = ((absorbed_dead / SIGMA) ** 0.25) - 273.15

    return history, latitude_list, temp_nobio


def run_daisyworld_with_grey_1d(S0=2100.0, L=1.0, alpha_w=0.75, alpha_b=0.25, alpha_g=0.50, alpha_u=0.5,
                                 q=20.0, gamma=0.3, aw_init=0.01, ab_init=0.01, ag_init=0.01, dt=0.1, itera=150,
                                 A=230.0, B=2.17, K=3.87, physics_mode="atmosphere"):
    """
    一維緯度灰雛菊世界迭代模擬器
    physics_mode: "atmosphere" (有大氣熱傳輸與溫室) 或 "airless" (無大氣純黑體輻射，K=0)
    """
    latitude_list = list(LATITUDE_LIST_1D)
    SunWt_list = list(SUNWT_LIST_1D)
    n_lat = len(latitude_list)
    is_airless = (physics_mode == "airless")

    lat_cos_list = [math.cos(math.radians(lat)) for lat in latitude_list]
    sum_cos = sum(lat_cos_list)
    R_in = np.array([(S0 / 4.0 * L * wt) for wt in SunWt_list])

    aw = np.full(n_lat, float(aw_init))
    ab = np.full(n_lat, float(ab_init))
    ag = np.full(n_lat, float(ag_init))
    history = []
    temp = np.full(n_lat, 15.0)

    for step in range(itera + 1):
        au = 1.0 - aw - ab - ag
        au = np.clip(au, 0.0, 1.0)
        alpha_p = aw * alpha_w + ab * alpha_b + ag * alpha_g + au * alpha_u

        if not is_airless:
            for _ in range(20):
                mean_t = np.sum(temp * lat_cos_list) / sum_cos
                temp = (R_in * (1.0 - alpha_p) + K * mean_t - A) / (B + K)
        else:
            absorbed = np.maximum(1.0, R_in * (1.0 - alpha_p))
            temp = ((absorbed / SIGMA) ** 0.25) - 273.15

        Tw = temp + q * (alpha_p - alpha_w)
        Tb = temp + q * (alpha_p - alpha_b)
        Tg = temp + q * (alpha_p - alpha_g)

        beta_w = np.maximum(0.0, 1.0 - 0.003265 * ((22.5 - Tw) ** 2))
        beta_b = np.maximum(0.0, 1.0 - 0.003265 * ((22.5 - Tb) ** 2))
        beta_g = np.maximum(0.0, 1.0 - 0.003265 * ((22.5 - Tg) ** 2))

        history.append({
            "step": step,
            "time": step * dt,
            "temp": temp.copy(),
            "aw": aw.copy(),
            "ab": ab.copy(),
            "ag": ag.copy(),
            "au": au.copy(),
            "alpha_p": alpha_p.copy(),
            "mean_t": float(np.sum(temp * lat_cos_list) / sum_cos)
        })

        daw = aw * (au * beta_w - gamma)
        dab = ab * (au * beta_b - gamma)
        dag = ag * (au * beta_g - gamma)

        aw = np.clip(aw + dt * daw, 0.001, 0.99)
        ab = np.clip(ab + dt * dab, 0.001, 0.99)
        ag = np.clip(ag + dt * dag, 0.001, 0.99)

        over_mask = (aw + ab + ag) > 0.99
        if np.any(over_mask):
            scale = 0.99 / (aw + ab + ag)
            aw = np.where(over_mask, aw * scale, aw)
            ab = np.where(over_mask, ab * scale, ab)
            ag = np.where(over_mask, ag * scale, ag)

    if not is_airless:
        temp_nobio = np.full(n_lat, 15.0)
        for _ in range(30):
            mean_t_nobio = np.sum(temp_nobio * lat_cos_list) / sum_cos
            temp_nobio = (R_in * (1.0 - alpha_u) + K * mean_t_nobio - A) / (B + K)
    else:
        absorbed_dead = np.maximum(1.0, R_in * (1.0 - alpha_u))
        temp_nobio = ((absorbed_dead / SIGMA) ** 0.25) - 273.15

    return history, latitude_list, temp_nobio
