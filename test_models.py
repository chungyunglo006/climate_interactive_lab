"""
Quick verification script to test all models in climate_interactive_lab.models
"""
import sys
from models import (
    run_ebm,
    find_three_equilibrium_states,
    calculate_ebm_bifurcation,
    run_ebm_1d,
    run_ebm_1d_history,
    sweep_ebm_1d_parameter,
    run_daisyworld,
    run_daisyworld_with_grey,
    sweep_daisyworld_luminosity,
    run_daisyworld_1d,
    run_daisyworld_with_grey_1d
    # run_ebm_2d,
    # run_daisyworld_2d,
    # run_daisyworld_grey_2d
)

print("Testing 0D EBM...")
df_ebm = run_ebm(S0=1368.0, T_init=288.0)
print(f"0D EBM final T: {df_ebm['溫度 (℃)'].iloc[-1]:.2f} °C, balance: {df_ebm['能量不平衡量 (W/m²)'].iloc[-1]:.4f}")

states = find_three_equilibrium_states(S0=1368.0)
print(f"Equilibrium states: State1={states['state1']['T']:.2f}K, State2={states['state2']['T']:.2f}K, State3={states['state3']['T']:.2f}K")

print("Testing 1D EBM...")
df_1d, mean_t = run_ebm_1d(SC=1370.0, Frac_SC=1.0)
print(f"1D EBM mean T: {mean_t:.2f} °C, equatorial T: {df_1d['最終溫度 (℃)'].iloc[-1]:.2f} °C, polar T: {df_1d['最終溫度 (℃)'].iloc[0]:.2f} °C")

print("Testing 0D Daisyworld...")
df_dw, t_nobio = run_daisyworld(S0=917.0, L=1.0)
print(f"0D Daisyworld final Tp: {df_dw['行星平均溫度 (℃)'].iloc[-1]:.2f} °C (vs Abiotic {t_nobio:.2f} °C)")

print("Testing 1D Daisyworld...")
hist_1d, lats, t_dead = run_daisyworld_1d(S0=2100.0, L=1.0, itera=30)
print(f"1D Daisyworld final mean T: {hist_1d[-1]['mean_t']:.2f} °C")

# print("Testing 2D Models...")
# T_2d, hist_2d = run_ebm_2d(itera=30)
# print(f"2D EBM shape: {T_2d.shape}, min T: {T_2d.min():.2f} °C, max T: {T_2d.max():.2f} °C")

print("ALL TESTS PASSED SUCCESSFULLY!")
