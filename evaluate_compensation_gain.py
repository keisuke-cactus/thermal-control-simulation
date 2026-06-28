"""
evaluate_compensation_gain.py

Purpose
-------
Evaluate the thermal interference compensation gain B.

Instead of searching for an optimum value,
this program proposes a systematic evaluation
procedure using Integral Absolute Error (IAE).

Evaluation indices
------------------
1. Zone 1 IAE
   -> Thermal interference to adjacent zone

2. Zone 2 IAE
   -> Disturbance recovery performance

Only the disturbance period
(150–160 min) is evaluated because the purpose
is to compare the transient response after
the disturbance.

The evaluation procedure can be used to
select an appropriate compensation gain
before implementation on an actual thermal
control system.
"""

import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Import simulation function
# ==========================================================
# The simulation accepts compensation gain B
# and returns:
#
# time          : simulation time [s]
# temperature   : temperature history [degC]
# heater_output : heater output history [W]
#
from pid_with_compensation_simulation import simulate_pid_control_with_gain


# ==========================================================
# IAE calculation
# ==========================================================
def calculate_iae(
    time,
    temperature,
    zone,
    target=320.0,
    start_min=150,
    end_min=160
):
    """
    Calculate Integral Absolute Error (IAE)

    Parameters
    ----------
    time : ndarray
        Simulation time [s]

    temperature : ndarray
        Temperature history

    zone : int
        Zone number
        0 : Zone1
        1 : Zone2
        2 : Zone3

    target : float
        Target temperature [degC]

    start_min : float
        Evaluation start time [min]

    end_min : float
        Evaluation end time [min]

    Returns
    -------
    iae : float
        Integral Absolute Error [degC min]
    """

    # Convert time to minutes
    time_min = time / 60

    # Extract evaluation period
    mask = (
        (time_min >= start_min) &
        (time_min <= end_min)
    )

    # Absolute temperature error
    error = np.abs(
        target - temperature[mask, zone]
    )

    # Numerical integration
    iae = np.trapz(
        error,
        time_min[mask]
    )

    return iae


# ==========================================================
# Compensation gain candidates
# ==========================================================
# Compensation gain to be evaluated
#
# Increasing B:
#   ↓ thermal interference
#   ↑ slower disturbance recovery
#
B_values = [0, 0.5, 1, 2, 4]

zone1_iae = []
zone2_iae = []

# ==========================================================
# Run simulations
# ==========================================================
for B in B_values:

    print(f"Simulating B = {B}")

    time, temperature, heater = simulate_pid_control_with_gain(B)

    # Zone1 thermal interference
    zone1_iae.append(
        calculate_iae(
            time,
            temperature,
            zone=0
        )
    )

    # Zone2 disturbance recovery
    zone2_iae.append(
        calculate_iae(
            time,
            temperature,
            zone=1
        )
    )


# ==========================================================
# Print evaluation results
# ==========================================================
print("---------------------------------------------")
print(" B      Zone1 IAE      Zone2 IAE")
print("---------------------------------------------")

for B, z1, z2 in zip(
    B_values,
    zone1_iae,
    zone2_iae
):
    print(f"{B:4.1f}   {z1:10.2f}   {z2:10.2f}")


# ==========================================================
# Plot evaluation result
# ==========================================================
plt.figure(figsize=(10,6))

plt.plot(
    B_values,
    zone1_iae,
    "o-",
    label="Zone 1 IAE"
)

plt.plot(
    B_values,
    zone2_iae,
    "s--",
    label="Zone 2 IAE"
)

plt.xlabel("Compensation gain B")
plt.ylabel("IAE [degC min]")


plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    "images/fig13_compensation_gain_evaluation.png",
    dpi=300
)

plt.show()