"""
0D Energy Balance Model (0D EBM) Module.
Implements:
- Time-stepping temperature evolution
- Three equilibrium state solver via bisection
- Bifurcation & stability S-curve calculation
- Constant S0 evolution
- Transient collapse simulation under declining solar radiation
"""

import numpy as np
import pandas as pd


def get_albedo(T, alpha_ice=0.6, alpha_land=0.3, T_ice=263.0, T_land=283.0):
    """Calculate temperature-dependent planetary albedo."""
    if isinstance(T, np.ndarray):
        alpha = np.zeros_like(T, dtype=float)
        alpha[T <= T_ice] = alpha_ice
        alpha[T >= T_land] = alpha_land
        mask = (T > T_ice) & (T < T_land)
        alpha[mask] = alpha_ice + (alpha_land - alpha_ice) * (T[mask] - T_ice) / (T_land - T_ice)
        return alpha
    else:
        if T <= T_ice:
            return float(alpha_ice)
        elif T >= T_land:
            return float(alpha_land)
        else:
            return float(alpha_ice + (alpha_land - alpha_ice) * (T - T_ice) / (T_land - T_ice))


def run_ebm(S0=1368.0, alpha_ice=0.6, alpha_land=0.3, T_ice=263.0, T_land=283.0,
            epsilon=0.62, C_ocean=2.09e8, T_init=288.0, dt=0.1, itera=200):
    """
    零維能量平衡模型 (0D EBM) 迭代模擬器
    """
    sigma = 5.670374e-8  # Stefan-Boltzmann Constant (W/m²/K⁴)
    seconds_per_year = 3.154e7

    t_list = []
    T_list = []
    alpha_list = []
    R_in_list = []
    R_out_list = []
    Imbalance_list = []

    T = float(T_init)

    for step in range(itera + 1):
        alpha = get_albedo(T, alpha_ice, alpha_land, T_ice, T_land)
        R_in = (S0 / 4.0) * (1.0 - alpha)
        R_out = epsilon * sigma * (T ** 4)
        imbalance = R_in - R_out

        t_list.append(step * dt)
        T_list.append(T)
        alpha_list.append(alpha)
        R_in_list.append(R_in)
        R_out_list.append(R_out)
        Imbalance_list.append(imbalance)

        T = T + (dt * seconds_per_year) * imbalance / C_ocean

    df = pd.DataFrame({
        "迭代步": range(itera + 1),
        "時間 (年)": t_list,
        "溫度 (K)": T_list,
        "溫度 (℃)": np.array(T_list) - 273.15,
        "反照率 (Albedo)": alpha_list,
        "入射能量 (W/m²)": R_in_list,
        "出射能量 (W/m²)": R_out_list,
        "能量不平衡量 (W/m²)": Imbalance_list
    })

    return df


def bisection_root(func, x1, x2, max_iter=35, tol=1e-5):
    """Bisection root finder."""
    f1 = func(x1)
    f2 = func(x2)
    if f1 * f2 > 0:
        return None
    for _ in range(max_iter):
        xm = (x1 + x2) / 2.0
        fm = func(xm)
        if abs(fm) < tol:
            return xm
        if fm * f1 <= 0:
            x2 = xm
            f2 = fm
        else:
            x1 = xm
            f1 = fm
    return (x1 + x2) / 2.0


def find_three_equilibrium_states(S0=1368.0, alpha_ice=0.6, alpha_land=0.3,
                                  T_ice=263.0, T_land=283.0, epsilon=0.62):
    """
    Finds the 3 equilibrium temperatures for given parameters.
    Returns: dict with state1 (warm/stable), state2 (partial/unstable), state3 (ice/stable)
    and radiation curves for plotting.
    """
    sigma = 5.670374e-8

    def f_eq(T_val):
        al = get_albedo(T_val, alpha_ice, alpha_land, T_ice, T_land)
        return (S0 / 4.0) * (1.0 - al) - epsilon * sigma * (T_val ** 4)

    T_curve = np.linspace(200.0, 320.0, 600)
    alpha_curve = get_albedo(T_curve, alpha_ice, alpha_land, T_ice, T_land)
    R_in_curve = (S0 / 4.0) * (1.0 - alpha_curve)
    R_out_curve = epsilon * sigma * (T_curve ** 4)

    t_eq3 = bisection_root(f_eq, 200.0, T_ice)
    t_eq2 = bisection_root(f_eq, T_ice, T_land)
    t_eq1 = bisection_root(f_eq, T_land, 320.0)

    states = {
        "state1": {"T": t_eq1, "name": "狀態 ① (無冰溫暖地球)", "stable": True},
        "state2": {"T": t_eq2, "name": "狀態 ② (部分結冰地球)", "stable": False},
        "state3": {"T": t_eq3, "name": "狀態 ③ (完全冰封雪球地球)", "stable": True},
        "T_curve": T_curve,
        "R_in": R_in_curve,
        "R_out": R_out_curve
    }
    return states


def check_stability(T_val, S0_val, alpha_ice=0.6, alpha_land=0.3,
                    T_ice=263.0, T_land=283.0, epsilon=0.62, delta=1e-4):
    """Checks stability via numerical derivative of f(T). df/dT < 0 -> Stable."""
    sigma = 5.670374e-8

    def f(t):
        al = get_albedo(t, alpha_ice, alpha_land, T_ice, T_land)
        return (S0_val / 4.0) * (1.0 - al) - epsilon * sigma * (t ** 4)

    df_dT = (f(T_val + delta) - f(T_val - delta)) / (2.0 * delta)
    return df_dT < 0.0


def calculate_ebm_bifurcation(alpha_ice=0.6, alpha_land=0.3, T_ice=263.0, T_land=283.0,
                              epsilon=0.62, s0_min=800.0, s0_max=2000.0, num_s0=300):
    """
    Calculates bifurcation diagram (S-curve) of equilibrium temperatures across S0 range.
    """
    sigma = 5.670374e-8
    s0_array = np.linspace(s0_min, s0_max, num_s0)

    stable_x = []
    stable_y = []
    unstable_x = []
    unstable_y = []

    t_grid = np.linspace(200.0, 320.0, 300)

    for s0 in s0_array:
        def f(t):
            al = get_albedo(t, alpha_ice, alpha_land, T_ice, T_land)
            return (s0 / 4.0) * (1.0 - al) - epsilon * sigma * (t ** 4)

        y_vals = [f(t) for t in t_grid]
        for i in range(len(t_grid) - 1):
            if y_vals[i] * y_vals[i + 1] <= 0:
                t_root = bisection_root(f, t_grid[i], t_grid[i + 1])
                if t_root is not None:
                    stable = check_stability(t_root, s0, alpha_ice, alpha_land, T_ice, T_land, epsilon)
                    if stable:
                        stable_x.append(s0)
                        stable_y.append(t_root)
                    else:
                        unstable_x.append(s0)
                        unstable_y.append(t_root)

    return {
        "stable_s0": np.array(stable_x),
        "stable_T": np.array(stable_y),
        "unstable_s0": np.array(unstable_x),
        "unstable_T": np.array(unstable_y),
    }


def run_ebm_constant(S0=1368.0, T_init=288.26, alpha_ice=0.6, alpha_land=0.3,
                     T_ice=263.0, T_land=283.0, epsilon=0.62, C_ocean=2.09e8,
                     dt=0.1, itera=200):
    """Wrapper for constant S0 equilibrium evolution."""
    return run_ebm(S0=S0, alpha_ice=alpha_ice, alpha_land=alpha_land,
                   T_ice=T_ice, T_land=T_land, epsilon=epsilon,
                   C_ocean=C_ocean, T_init=T_init, dt=dt, itera=itera)


def run_ebm_transient_collapse(S0_start=1368.0, S0_end=1200.0, S0_steps=20,
                               T_warm_init=290.0, T_cold_init=230.0,
                               alpha_ice=0.6, alpha_land=0.3, T_ice=263.0, T_land=283.0,
                               epsilon=0.62, C_ocean=2.09e8, dt=0.1, itera_per_step=150):
    """
    Simulates transient climate collapse as solar constant ramps down across critical bifurcation point.
    Tracks warm-start and cold-start branches.
    """
    s0_values = np.linspace(S0_start, S0_end, S0_steps)
    results = []

    t_w = T_warm_init
    t_c = T_cold_init

    for s0 in s0_values:
        df_w = run_ebm(S0=s0, alpha_ice=alpha_ice, alpha_land=alpha_land,
                       T_ice=T_ice, T_land=T_land, epsilon=epsilon,
                       C_ocean=C_ocean, T_init=t_w, dt=dt, itera=itera_per_step)
        df_c = run_ebm(S0=s0, alpha_ice=alpha_ice, alpha_land=alpha_land,
                       T_ice=T_ice, T_land=T_land, epsilon=epsilon,
                       C_ocean=C_ocean, T_init=t_c, dt=dt, itera=itera_per_step)

        final_tw = df_w["溫度 (K)"].iloc[-1]
        final_tc = df_c["溫度 (K)"].iloc[-1]

        # Use final state as next initial state to demonstrate hysteresis
        t_w = final_tw
        t_c = final_tc

        results.append({
            "S0": s0,
            "T_warm_K": final_tw,
            "T_warm_C": final_tw - 273.15,
            "T_cold_K": final_tc,
            "T_cold_C": final_tc - 273.15,
            "albedo_warm": df_w["反照率 (Albedo)"].iloc[-1],
            "albedo_cold": df_c["反照率 (Albedo)"].iloc[-1],
            "warm_time_series": df_w,
            "cold_time_series": df_c
        })

    return results


def run_ebm_continuous_transient_collapse(
    S0_start=1368.0, S0_min=1180.0, S0_max=1750.0,
    ramp_down_years=80.0, stay_cold_years=20.0, ramp_up_years=80.0,
    T_init=288.15, alpha_ice=0.6, alpha_land=0.3,
    T_ice=263.0, T_land=283.0, epsilon=0.62, C_ocean=2.09e8, dt=0.05
):
    """
    連續時間動態數值積分 (Continuous ODE Integration) 模擬瞬態氣候崩潰與解凍遲滯。
    太陽輻射 S(t) 平滑演化：
    1. 溫暖期平滑衰退至冰期 (S0_start -> S0_min)
    2. 深度冰球期 (維持 S0_min)
    3. 增溫解凍期 (S0_min -> S0_max)
    回傳高解析度時間序列 DataFrame。
    """
    sigma = 5.670374e-8
    seconds_per_year = 3.154e7
    dt_sec = dt * seconds_per_year

    total_years = ramp_down_years + stay_cold_years + ramp_up_years
    total_steps = int(np.ceil(total_years / dt))

    t_list = []
    s0_list = []
    T_list = []
    alpha_list = []
    R_in_list = []
    R_out_list = []
    dTdt_list = []

    T = float(T_init)

    for step in range(total_steps + 1):
        t = step * dt

        # Determine solar constant S0(t)
        if t <= ramp_down_years:
            frac = t / ramp_down_years
            s0_t = S0_start + (S0_min - S0_start) * frac
        elif t <= ramp_down_years + stay_cold_years:
            s0_t = S0_min
        else:
            frac = (t - ramp_down_years - stay_cold_years) / ramp_up_years
            s0_t = S0_min + (S0_max - S0_min) * min(1.0, frac)

        alpha = get_albedo(T, alpha_ice, alpha_land, T_ice, T_land)
        R_in = (s0_t / 4.0) * (1.0 - alpha)
        R_out = epsilon * sigma * (T ** 4)
        net_flux = R_in - R_out

        dTdt = (net_flux / C_ocean) * seconds_per_year  # K / year

        t_list.append(t)
        s0_list.append(s0_t)
        T_list.append(T)
        alpha_list.append(alpha)
        R_in_list.append(R_in)
        R_out_list.append(R_out)
        dTdt_list.append(dTdt)

        # RK4 or Euler integration
        T = T + (net_flux / C_ocean) * dt_sec

    return pd.DataFrame({
        "時間 (年)": t_list,
        "太陽常數 (W/m²)": s0_list,
        "溫度 (K)": T_list,
        "溫度 (℃)": np.array(T_list) - 273.15,
        "反照率 (Albedo)": alpha_list,
        "入射能量 (W/m²)": R_in_list,
        "出射能量 (W/m²)": R_out_list,
        "淨不平衡通量 (W/m²)": np.array(R_in_list) - np.array(R_out_list),
        "升降溫速率 (℃/年)": dTdt_list
    })

