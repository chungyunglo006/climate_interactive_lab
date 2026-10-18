"""
0D Daisyworld Model Module (Classic & Grey Daisies).
Implements:
- Watson & Lovelock (1983) Classic 2-species (Black & White) Daisyworld
- 3-species Grey Daisyworld (neutral albedo competition)
- Solar luminosity / solar constant sweep for climate regulation (homeostasis) curves
"""

import numpy as np
import pandas as pd


def beta_growth(T):
    """Parabolic temperature growth function beta(T) with optimum at 22.5 degC."""
    if isinstance(T, (np.ndarray, list)):
        return np.maximum(0.0, 1.0 - 0.003265 * ((22.5 - np.array(T)) ** 2))
    else:
        return max(0.0, 1.0 - 0.003265 * ((22.5 - float(T)) ** 2))


def run_daisyworld(S0=917.0, L=1.0, alpha_w=0.75, alpha_b=0.25, alpha_u=0.5,
                   q=20.0, gamma=0.3, aw_init=0.01, ab_init=0.01, dt=0.1, itera=150):
    """
    經典雙物種雛菊世界模擬器
    """
    sigma = 5.670374e-8
    t_list, aw_list, ab_list, au_list, Tp_list, Tw_list, Tb_list, alpha_p_list = [], [], [], [], [], [], [], []
    aw, ab = float(aw_init), float(ab_init)

    for step in range(itera + 1):
        au = max(0.0, min(1.0, 1.0 - aw - ab))
        alpha_p = aw * alpha_w + ab * alpha_b + au * alpha_u
        Tp_K = ((S0 * L * (1.0 - alpha_p)) / sigma) ** 0.25
        Tp_C = Tp_K - 273.15

        Tw = Tp_C + q * (alpha_p - alpha_w)
        Tb = Tp_C + q * (alpha_p - alpha_b)

        beta_w, beta_b = beta_growth(Tw), beta_growth(Tb)

        t_list.append(step * dt)
        aw_list.append(aw)
        ab_list.append(ab)
        au_list.append(au)
        Tp_list.append(Tp_C)
        Tw_list.append(Tw)
        Tb_list.append(Tb)
        alpha_p_list.append(alpha_p)

        daw = aw * (au * beta_w - gamma)
        dab = ab * (au * beta_b - gamma)

        aw = max(0.001, min(0.99, aw + dt * daw))
        ab = max(0.001, min(0.99, ab + dt * dab))
        if aw + ab > 0.99:
            scale = 0.99 / (aw + ab)
            aw *= scale
            ab *= scale

    # Baseline abiotic planet temperature for comparison
    T_nobio_C = (((S0 * L * (1.0 - alpha_u)) / sigma) ** 0.25) - 273.15

    df = pd.DataFrame({
        "迭代步": range(itera + 1), "時間": t_list,
        "白雛菊覆蓋率": aw_list, "黑雛菊覆蓋率": ab_list, "裸地覆蓋率": au_list,
        "行星平均溫度 (℃)": Tp_list, "白雛菊溫度 (℃)": Tw_list, "黑雛菊溫度 (℃)": Tb_list,
        "行星反照率": alpha_p_list
    })

    return df, T_nobio_C


def run_daisyworld_with_grey(S0=917.0, L=1.0, alpha_w=0.75, alpha_b=0.25, alpha_g=0.50, alpha_u=0.5,
                             q=20.0, gamma=0.3, aw_init=0.01, ab_init=0.01, ag_init=0.01, dt=0.1, itera=150):
    """
    加入灰雛菊因子的三物種雛菊世界模擬器
    """
    sigma = 5.670374e-8
    t_list, aw_list, ab_list, ag_list, au_list, Tp_list, Tw_list, Tb_list, Tg_list, alpha_p_list = [], [], [], [], [], [], [], [], [], []
    aw, ab, ag = float(aw_init), float(ab_init), float(ag_init)

    for step in range(itera + 1):
        au = max(0.0, min(1.0, 1.0 - aw - ab - ag))
        alpha_p = aw * alpha_w + ab * alpha_b + ag * alpha_g + au * alpha_u
        Tp_K = ((S0 * L * (1.0 - alpha_p)) / sigma) ** 0.25
        Tp_C = Tp_K - 273.15

        Tw = Tp_C + q * (alpha_p - alpha_w)
        Tb = Tp_C + q * (alpha_p - alpha_b)
        Tg = Tp_C + q * (alpha_p - alpha_g)

        beta_w, beta_b, beta_g = beta_growth(Tw), beta_growth(Tb), beta_growth(Tg)

        t_list.append(step * dt)
        aw_list.append(aw)
        ab_list.append(ab)
        ag_list.append(ag)
        au_list.append(au)
        Tp_list.append(Tp_C)
        Tw_list.append(Tw)
        Tb_list.append(Tb)
        Tg_list.append(Tg)
        alpha_p_list.append(alpha_p)

        daw = aw * (au * beta_w - gamma)
        dab = ab * (au * beta_b - gamma)
        dag = ag * (au * beta_g - gamma)

        aw = max(0.001, min(0.99, aw + dt * daw))
        ab = max(0.001, min(0.99, ab + dt * dab))
        ag = max(0.001, min(0.99, ag + dt * dag))

        if aw + ab + ag > 0.99:
            scale = 0.99 / (aw + ab + ag)
            aw *= scale
            ab *= scale
            ag *= scale

    T_nobio_C = (((S0 * L * (1.0 - alpha_u)) / sigma) ** 0.25) - 273.15

    df = pd.DataFrame({
        "迭代步": range(itera + 1), "時間": t_list,
        "白雛菊覆蓋率": aw_list, "黑雛菊覆蓋率": ab_list, "灰雛菊覆蓋率": ag_list, "裸地覆蓋率": au_list,
        "行星平均溫度 (℃)": Tp_list, "白雛菊溫度 (℃)": Tw_list, "黑雛菊溫度 (℃)": Tb_list, "灰雛菊溫度 (℃)": Tg_list,
        "行星反照率": alpha_p_list
    })

    return df, T_nobio_C


def sweep_daisyworld_luminosity(S0=917.0, l_min=0.6, l_max=1.6, num_l=60,
                                alpha_w=0.75, alpha_b=0.25, alpha_u=0.5,
                                q=20.0, gamma=0.3, dt=0.1, itera_per_l=150):
    """
    Sweeps luminosity L to generate classic Daisyworld temperature regulation curve.
    Uses sequential continuation (each step initializes with previous equilibrium).
    """
    sigma = 5.670374e-8
    l_vals = np.linspace(l_min, l_max, num_l)

    aw_eq, ab_eq, au_eq, tp_eq, t_nobio_eq = [], [], [], [], []

    curr_aw = 0.01
    curr_ab = 0.01

    for l_val in l_vals:
        df, _ = run_daisyworld(S0=S0, L=l_val, alpha_w=alpha_w, alpha_b=alpha_b, alpha_u=alpha_u,
                               q=q, gamma=gamma, aw_init=curr_aw, ab_init=curr_ab,
                               dt=dt, itera=itera_per_l)
        last_aw = df["白雛菊覆蓋率"].iloc[-1]
        last_ab = df["黑雛菊覆蓋率"].iloc[-1]
        last_au = df["裸地覆蓋率"].iloc[-1]
        last_tp = df["行星平均溫度 (℃)"].iloc[-1]

        aw_eq.append(last_aw)
        ab_eq.append(last_ab)
        au_eq.append(last_au)
        tp_eq.append(last_tp)

        t_dead = (((S0 * l_val * (1.0 - alpha_u)) / sigma) ** 0.25) - 273.15
        t_nobio_eq.append(t_dead)

        curr_aw = max(0.01, last_aw)
        curr_ab = max(0.01, last_ab)

    return pd.DataFrame({
        "L": l_vals,
        "白雛菊覆蓋率": aw_eq,
        "黑雛菊覆蓋率": ab_eq,
        "裸地覆蓋率": au_eq,
        "調控溫度 (℃)": tp_eq,
        "無生物溫度 (℃)": t_nobio_eq
    })


def sweep_daisyworld_grey_luminosity(S0=917.0, l_min=0.6, l_max=1.6, num_l=60,
                                     alpha_w=0.75, alpha_b=0.25, alpha_g=0.50, alpha_u=0.5,
                                     q=20.0, gamma=0.3, dt=0.1, itera_per_l=150):
    """
    Sweeps luminosity L for 3-species Grey Daisyworld.
    """
    sigma = 5.670374e-8
    l_vals = np.linspace(l_min, l_max, num_l)

    aw_eq, ab_eq, ag_eq, au_eq, tp_eq, t_nobio_eq = [], [], [], [], [], []

    curr_aw, curr_ab, curr_ag = 0.01, 0.01, 0.01

    for l_val in l_vals:
        df, _ = run_daisyworld_with_grey(S0=S0, L=l_val, alpha_w=alpha_w, alpha_b=alpha_b,
                                         alpha_g=alpha_g, alpha_u=alpha_u, q=q, gamma=gamma,
                                         aw_init=curr_aw, ab_init=curr_ab, ag_init=curr_ag,
                                         dt=dt, itera=itera_per_l)
        last_aw = df["白雛菊覆蓋率"].iloc[-1]
        last_ab = df["黑雛菊覆蓋率"].iloc[-1]
        last_ag = df["灰雛菊覆蓋率"].iloc[-1]
        last_au = df["裸地覆蓋率"].iloc[-1]
        last_tp = df["行星平均溫度 (℃)"].iloc[-1]

        aw_eq.append(last_aw)
        ab_eq.append(last_ab)
        ag_eq.append(last_ag)
        au_eq.append(last_au)
        tp_eq.append(last_tp)

        t_dead = (((S0 * l_val * (1.0 - alpha_u)) / sigma) ** 0.25) - 273.15
        t_nobio_eq.append(t_dead)

        curr_aw = max(0.01, last_aw)
        curr_ab = max(0.01, last_ab)
        curr_ag = max(0.01, last_ag)

    return pd.DataFrame({
        "L": l_vals,
        "白雛菊覆蓋率": aw_eq,
        "黑雛菊覆蓋率": ab_eq,
        "灰雛菊覆蓋率": ag_eq,
        "裸地覆蓋率": au_eq,
        "調控溫度 (℃)": tp_eq,
        "無生物溫度 (℃)": t_nobio_eq
    })
