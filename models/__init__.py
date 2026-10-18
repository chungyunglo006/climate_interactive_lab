"""
Models package for Climate and Ecological Models.
Contains 0D/1D/2D Energy Balance Models (EBM) and Daisyworld simulations.
"""

from .ebm_0d import (
    run_ebm,
    calculate_ebm_bifurcation,
    find_three_equilibrium_states,
    run_ebm_transient_collapse,
    run_ebm_constant
)
from .ebm_1d import (
    run_ebm_1d,
    run_ebm_1d_history,
    sweep_ebm_1d_parameter
)
from .daisy_0d import (
    run_daisyworld,
    run_daisyworld_with_grey,
    sweep_daisyworld_luminosity,
    sweep_daisyworld_grey_luminosity
)
from .daisy_1d import (
    run_daisyworld_1d,
    run_daisyworld_with_grey_1d
)
# from .models_2d.py import (
#     LAT_LIST_2D,
#     LON_LIST_2D,
#     SUNWT_LIST_2D,
#     LAT_EDGES_2D,
#     LON_EDGES_2D,
#     LAND_MASK_2D,
#     run_ebm_2d,
#     run_daisyworld_2d,
#     run_daisyworld_grey_2d
# )

__all__ = [
    "run_ebm",
    "calculate_ebm_bifurcation",
    "find_three_equilibrium_states",
    "run_ebm_transient_collapse",
    "run_ebm_constant",
    "run_ebm_1d",
    "run_ebm_1d_history",
    "sweep_ebm_1d_parameter",
    "run_daisyworld",
    "run_daisyworld_with_grey",
    "sweep_daisyworld_luminosity",
    "sweep_daisyworld_grey_luminosity",
    "run_daisyworld_1d",
    "run_daisyworld_with_grey_1d"
    # 2D models temporarily commented out
]
