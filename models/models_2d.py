"""
Two-Dimensional Climate & Daisyworld Models Module (2D Grid: 9 Latitudes x 12 Longitudes).
Implements:
- 2D EBM with continent/ocean heat capacity and albedo contrasts, meridional and zonal diffusion
- 2D Classic Daisyworld (daisies only on land)
- 2D Grey Daisyworld (3-species competition on 2D geographic grid)
"""

import numpy as np

# 2D Grids and Land-Sea Mask
LAT_LIST_2D = np.array([85., 75., 65., 55., 45., 35., 25., 15., 6.])
LON_LIST_2D = np.arange(12) * 30.0
SUNWT_LIST_2D = np.array([0.5, 0.531, 0.624, 0.77, 0.892, 1.021, 1.12, 1.189, 1.219])
LAT_EDGES_2D = np.array([90, 80, 70, 60, 50, 40, 30, 20, 10, 1], dtype=float)
LON_EDGES_2D = np.arange(13) * 30.0 - 15

# Land-sea mask (1 = Land, 0 = Ocean)
LAND_MASK_2D = np.array([
    # 0deg 30   60   90  120  150  180  210  240  270  300  330
    [ 0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],  # 85N
    [ 0,   0,   1,   1,   0,   0,   0,   0,   0,   1,   1,   0],  # 75N
    [ 1,   0,   1,   1,   1,   0,   0,   0,   1,   1,   1,   0],  # 65N
    [ 1,   1,   1,   1,   1,   0,   0,   0,   1,   1,   1,   1],  # 55N
    [ 1,   1,   1,   1,   1,   0,   0,   0,   1,   1,   1,   0],  # 45N
    [ 0,   1,   1,   1,   1,   0,   0,   0,   1,   1,   0,   0],  # 35N
    [ 0,   1,   1,   1,   1,   0,   0,   0,   1,   1,   0,   0],  # 25N
    [ 0,   1,   1,   1,   0,   0,   0,   0,   0,   1,   0,   0],  # 15N
    [ 0,   1,   1,   0,   1,   0,   0,   0,   1,   1,   0,   0],  # 6N
], dtype=float)


def run_ebm_2d(SC=1370.0, Frac_SC=1.0, A=230.0, B=2.17,
               K_lat=3.87, K_lon=1.5,
               alpha_ice=0.6, alpha_ocean=0.10, alpha_land=0.30,
               T_ice=-10.0, T_land=10.0,
               C_ocean=2.09e8, C_land=5.0e6,
               dt=0.05, itera=300):
    """
    2D Energy Balance Model (2D EBM)
    """
    n_lat, n_lon = len(LAT_LIST_2D), len(LON_LIST_2D)
    lat_cos = np.cos(np.radians(LAT_LIST_2D))
    C_grid = np.where(LAND_MASK_2D == 1, C_land, C_ocean)
    alpha_base = np.where(LAND_MASK_2D == 1, alpha_land, alpha_ocean)
    R_in = np.outer(SUNWT_LIST_2D, np.ones(n_lon)) * SC * Frac_SC / 4.0

    T = np.zeros((n_lat, n_lon))
    for i in range(n_lat):
        T[i, :] = 25.0 - 0.5 * LAT_LIST_2D[i]
    T += np.where(LAND_MASK_2D == 1, 2.0, -2.0)
    T = np.clip(T, -35.0, 35.0)

    history = []
    dt_sec = dt * 3.154e7
    record_every = max(1, itera // 30)

    for step in range(itera + 1):
        alpha = np.where(T <= T_ice, alpha_ice,
                np.where(T >= T_land, alpha_base,
                    alpha_ice + (alpha_base - alpha_ice) * (T - T_ice) / (T_land - T_ice)))
        R_out = A + B * T
        zonal_mean = np.mean(T, axis=1)
        global_mean = np.sum(zonal_mean * lat_cos) / np.sum(lat_cos)
        D_lat = K_lat * (global_mean - T)
        D_lon = K_lon * (zonal_mean[:, np.newaxis] - T)
        imbalance = R_in * (1.0 - alpha) - R_out + D_lat + D_lon

        if step % record_every == 0 or step == itera:
            history.append({
                'step': step,
                'T': T.copy(),
                'alpha': alpha.copy(),
                'global_mean': float(global_mean)
            })

        T = T + dt_sec * imbalance / C_grid

    return T, history


def run_daisyworld_2d(S0=2100.0, L=1.0,
                      alpha_w=0.75, alpha_b=0.25, alpha_u=0.5, alpha_ocean=0.10,
                      q=20.0, gamma=0.3, aw_init=0.01, ab_init=0.01,
                      K_lat=3.87, K_lon=1.5,
                      dt=0.1, itera=150):
    """
    2D Classic Daisyworld: daisies only grow on land cells
    """
    sigma = 5.670374e-8
    lat_cos = np.cos(np.radians(LAT_LIST_2D))
    n_lat, n_lon = len(LAT_LIST_2D), len(LON_LIST_2D)

    aw = np.where(LAND_MASK_2D == 1, aw_init, 0.0)
    ab = np.where(LAND_MASK_2D == 1, ab_init, 0.0)

    def beta_fn(T_arr):
        return np.maximum(0.0, 1.0 - 0.003265 * (22.5 - T_arr) ** 2)

    history = []
    record_every = max(1, itera // 30)
    T_eff = np.full((n_lat, n_lon), 15.0)

    for step in range(itera + 1):
        au = np.maximum(0.0, 1.0 - aw - ab)
        alpha_p = np.where(LAND_MASK_2D == 1,
                           aw * alpha_w + ab * alpha_b + au * alpha_u,
                           alpha_ocean)
        R_in_2d = np.outer(SUNWT_LIST_2D, np.ones(n_lon)) * S0 * L / 4.0
        Tp_K = ((R_in_2d * (1.0 - alpha_p)) / sigma) ** 0.25
        Tp_C = Tp_K - 273.15

        zonal_mean = np.mean(Tp_C, axis=1)
        global_mean = np.sum(zonal_mean * lat_cos) / np.sum(lat_cos)
        D_lat = K_lat * (global_mean - Tp_C)
        D_lon = K_lon * (zonal_mean[:, np.newaxis] - Tp_C)
        T_eff = Tp_C + D_lat + D_lon

        Tw = T_eff + q * (alpha_p - alpha_w)
        Tb = T_eff + q * (alpha_p - alpha_b)

        daw = dt * aw * (au * beta_fn(Tw) - gamma) * LAND_MASK_2D
        dab = dt * ab * (au * beta_fn(Tb) - gamma) * LAND_MASK_2D

        aw_new = np.clip(aw + daw, 0.0, 1.0)
        ab_new = np.clip(ab + dab, 0.0, 1.0)

        total = aw_new + ab_new
        overflow = np.maximum(0.0, total - 1.0)
        aw_new -= overflow * aw_new / (total + 1e-10)
        ab_new -= overflow * ab_new / (total + 1e-10)

        aw = np.maximum(0.0, aw_new)
        ab = np.maximum(0.0, ab_new)

        if step % record_every == 0 or step == itera:
            history.append({
                'step': step,
                'aw': aw.copy(),
                'ab': ab.copy(),
                'T': T_eff.copy(),
                'alpha_p': alpha_p.copy(),
                'global_mean': float(global_mean)
            })

    return aw, ab, T_eff, history


def run_daisyworld_grey_2d(S0=2100.0, L=1.0,
                           alpha_w=0.75, alpha_b=0.25, alpha_g=0.50,
                           alpha_u=0.5, alpha_ocean=0.10,
                           q=20.0, gamma=0.3,
                           aw_init=0.01, ab_init=0.01, ag_init=0.01,
                           K_lat=3.87, K_lon=1.5,
                           dt=0.1, itera=150):
    """
    2D Grey Daisyworld: adds grey daisies (alpha_g = alpha_u) to 2D framework
    """
    sigma = 5.670374e-8
    lat_cos = np.cos(np.radians(LAT_LIST_2D))
    n_lat, n_lon = len(LAT_LIST_2D), len(LON_LIST_2D)

    aw = np.where(LAND_MASK_2D == 1, aw_init, 0.0)
    ab = np.where(LAND_MASK_2D == 1, ab_init, 0.0)
    ag = np.where(LAND_MASK_2D == 1, ag_init, 0.0)

    def beta_fn(T_arr):
        return np.maximum(0.0, 1.0 - 0.003265 * (22.5 - T_arr) ** 2)

    history = []
    record_every = max(1, itera // 30)
    T_eff = np.full((n_lat, n_lon), 15.0)

    for step in range(itera + 1):
        au = np.maximum(0.0, 1.0 - aw - ab - ag)
        alpha_p = np.where(LAND_MASK_2D == 1,
                           aw * alpha_w + ab * alpha_b + ag * alpha_g + au * alpha_u,
                           alpha_ocean)
        R_in_2d = np.outer(SUNWT_LIST_2D, np.ones(n_lon)) * S0 * L / 4.0
        Tp_K = ((R_in_2d * (1.0 - alpha_p)) / sigma) ** 0.25
        Tp_C = Tp_K - 273.15

        zonal_mean = np.mean(Tp_C, axis=1)
        global_mean = np.sum(zonal_mean * lat_cos) / np.sum(lat_cos)
        D_lat = K_lat * (global_mean - Tp_C)
        D_lon = K_lon * (zonal_mean[:, np.newaxis] - Tp_C)
        T_eff = Tp_C + D_lat + D_lon

        Tw = T_eff + q * (alpha_p - alpha_w)
        Tb = T_eff + q * (alpha_p - alpha_b)
        Tg = T_eff + q * (alpha_p - alpha_g)

        daw = dt * aw * (au * beta_fn(Tw) - gamma) * LAND_MASK_2D
        dab = dt * ab * (au * beta_fn(Tb) - gamma) * LAND_MASK_2D
        dag = dt * ag * (au * beta_fn(Tg) - gamma) * LAND_MASK_2D

        aw_new = np.clip(aw + daw, 0.0, 1.0)
        ab_new = np.clip(ab + dab, 0.0, 1.0)
        ag_new = np.clip(ag + dag, 0.0, 1.0)

        total = aw_new + ab_new + ag_new
        overflow = np.maximum(0.0, total - 1.0)
        aw_new -= overflow * aw_new / (total + 1e-10)
        ab_new -= overflow * ab_new / (total + 1e-10)
        ag_new -= overflow * ag_new / (total + 1e-10)

        aw = np.maximum(0.0, aw_new)
        ab = np.maximum(0.0, ab_new)
        ag = np.maximum(0.0, ag_new)

        if step % record_every == 0 or step == itera:
            history.append({
                'step': step,
                'aw': aw.copy(),
                'ab': ab.copy(),
                'ag': ag.copy(),
                'T': T_eff.copy(),
                'alpha_p': alpha_p.copy(),
                'global_mean': float(global_mean)
            })

    return aw, ab, ag, T_eff, history
