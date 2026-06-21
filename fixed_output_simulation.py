import numpy as np
import matplotlib.pyplot as plt


def simulate_fixed_output():
    # =====================================
    # Simulation Settings
    # =====================================
    dt = 1.0                 # Time step [s]
    t_end = 10000            # Simulation time [s]
    time = np.arange(0, t_end + dt, dt)

    # =====================================
    # Physical Parameters
    # =====================================

    # Solder properties
    rho = 9000.0             # Density [kg/m3]
    cp = 176.0               # Specific heat [J/(kg*K)]

    # Geometry of each thermal zone
    volume = 1.0e-3          # Volume [m3]
    surface_area_edge = 5.0e-2      # Effective surface area of edge zones [m2]
    surface_area_center = 4.0e-2    # Effective surface area of center zone [m2]
    conduction_area = 1.0e-2        # Contact area between adjacent zones [m2]
    block_length = 0.1              # Distance between adjacent zones [m]

    # Environment
    ambient = 25.0           # Ambient temperature [degC]

    # Heater input
    heater_output = np.array([500.0, 500.0, 500.0])  # Heater output [W]

    # Heat transfer to ambient air
    h = 14.5                 # Heat transfer coefficient [W/(m2*K)]

    # Thermal conductivity
    thermal_conductivity = 49.0  # Thermal conductivity [W/(m*K)]

    # =====================================
    # Derived Parameters
    # =====================================
    mass = rho * volume      # Mass [kg]
    heat_capacity = mass * cp  # Heat capacity [J/K]

    k_loss_edge = h * surface_area_edge          # [W/K]
    k_loss_center = h * surface_area_center      # [W/K]
    k_loss = np.array([k_loss_edge, k_loss_center, k_loss_edge])

    k_cond = thermal_conductivity * conduction_area / block_length  # [W/K]

    # =====================================
    # Simulation
    # =====================================
    temperature = np.zeros((len(time), 3))
    temperature[0, :] = ambient

    for i in range(len(time) - 1):
        T1, T2, T3 = temperature[i, :]

        # Zone 1: heater input - heat loss + heat conduction from Zone 2
        dT1 = (
            heater_output[0]
            - k_loss[0] * (T1 - ambient)
            + k_cond * (T2 - T1)
        ) / heat_capacity

        # Zone 2: heater input - heat loss + heat conduction from Zone 1 and Zone 3
        dT2 = (
            heater_output[1]
            - k_loss[1] * (T2 - ambient)
            + k_cond * (T1 - T2)
            + k_cond * (T3 - T2)
        ) / heat_capacity

        # Zone 3: heater input - heat loss + heat conduction from Zone 2
        dT3 = (
            heater_output[2]
            - k_loss[2] * (T3 - ambient)
            + k_cond * (T2 - T3)
        ) / heat_capacity

        temperature[i + 1, 0] = T1 + dT1 * dt
        temperature[i + 1, 1] = T2 + dT2 * dt
        temperature[i + 1, 2] = T3 + dT3 * dt

    return time, temperature


def plot_fixed_output_result():
    time, temperature = simulate_fixed_output()
    time_min = time / 60

    plt.figure(figsize=(10, 6))
    plt.plot(time_min, temperature[:, 0], label="Zone 1")
    plt.plot(time_min, temperature[:, 1], label="Zone 2")
    plt.plot(time_min, temperature[:, 2], label="Zone 3")

    plt.xlabel("Time [min]")
    plt.ylabel("Temperature [degC]")
    plt.title("Fig.1 Temperature Response with Fixed Heater Output")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("fixed_output_temperature_response.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    plot_fixed_output_result()