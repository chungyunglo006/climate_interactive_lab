"""
Quick verification script to test all models in climate_interactive_lab.models
including the new dual physics mode features.
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
    sweep_daisyworld_grey_luminosity,
    run_daisyworld_1d,
    run_daisyworld_with_grey_1d
)

print("1. Testing 0D EBM...")
df_ebm = run_ebm(S0=1368.0, T_init=288.0)
print(f"   0D EBM final T: {df_ebm['溫度 (℃)'].iloc[-1]:.2f} °C")

states = find_three_equilibrium_states(S0=1368.0)
print(f"   Equilibrium states: State1={states['state1']['T']:.2f}K, State2={states['state2']['T']:.2f}K, State3={states['state3']['T']:.2f}K")

print("2. Testing 1D EBM...")
df_1d, mean_t = run_ebm_1d(SC=1370.0, Frac_SC=1.0)
print(f"   1D EBM mean T: {mean_t:.2f} °C, Eq={df_1d['最終溫度 (℃)'].iloc[-1]:.2f} °C, Pole={df_1d['最終溫度 (℃)'].iloc[0]:.2f} °C")

print("3. Testing 0D Classic Daisyworld (Dual Physics)...")
df_dw_love, t_nobio_love = run_daisyworld(S0=917.0, L=1.0, physics_mode="lovelock")
print(f"   [Lovelock] final Tp: {df_dw_love['行星平均溫度 (℃)'].iloc[-1]:.2f} °C (Dead: {t_nobio_love:.2f} °C)")

df_dw_stull, t_nobio_stull = run_daisyworld(S0=1368.0, L=1.0, physics_mode="stull")
print(f"   [Stull Greenhouse] final Tp: {df_dw_stull['行星平均溫度 (℃)'].iloc[-1]:.2f} °C (Dead: {t_nobio_stull:.2f} °C)")

print("4. Testing 0D Grey Daisyworld (Dual Physics)...")
df_g_love, _ = run_daisyworld_with_grey(S0=917.0, L=1.0, physics_mode="lovelock")
print(f"   [Lovelock Grey] final Tp: {df_g_love['行星平均溫度 (℃)'].iloc[-1]:.2f} °C, Grey cov: {df_g_love['灰雛菊覆蓋率'].iloc[-1]*100:.1f}%")

df_g_stull, _ = run_daisyworld_with_grey(S0=1368.0, L=1.0, physics_mode="stull")
print(f"   [Stull Grey] final Tp: {df_g_stull['行星平均溫度 (℃)'].iloc[-1]:.2f} °C, Grey cov: {df_g_stull['灰雛菊覆蓋率'].iloc[-1]*100:.1f}%")

print("5. Testing 1D Daisyworld (Dual Physics: Atmosphere vs Airless)...")
hist_1d_atmo, _, _ = run_daisyworld_1d(S0=2100.0, L=1.0, itera=25, physics_mode="atmosphere")
print(f"   [Atmosphere K=3.87] final mean T: {hist_1d_atmo[-1]['mean_t']:.2f} °C, Eq={hist_1d_atmo[-1]['temp'][-1]:.2f} °C, Pole={hist_1d_atmo[-1]['temp'][0]:.2f} °C")

hist_1d_air, _, _ = run_daisyworld_1d(S0=2100.0, L=1.0, itera=25, physics_mode="airless")
print(f"   [Airless K=0] final mean T: {hist_1d_air[-1]['mean_t']:.2f} °C, Eq={hist_1d_air[-1]['temp'][-1]:.2f} °C, Pole={hist_1d_air[-1]['temp'][0]:.2f} °C")

print("6. Testing 1D Grey Daisyworld (Dual Physics)...")
hist_g1d_atmo, _, _ = run_daisyworld_with_grey_1d(S0=2100.0, L=1.0, itera=25, physics_mode="atmosphere")
print(f"   [Atmosphere 1D Grey] final mean T: {hist_g1d_atmo[-1]['mean_t']:.2f} °C")

hist_g1d_air, _, _ = run_daisyworld_with_grey_1d(S0=2100.0, L=1.0, itera=25, physics_mode="airless")
print(f"   [Airless 1D Grey] final mean T: {hist_g1d_air[-1]['mean_t']:.2f} °C")

print("\nALL DUAL-PHYSICS TESTS PASSED SUCCESSFULLY!")
