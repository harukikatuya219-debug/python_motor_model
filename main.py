import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gui import ParameterGUI
from motor.DCmotor import DCmotor
import numpy as np
from scipy.integrate import solve_ivp
from plot import plot_result
from sim.sim_comp import run_simulation

def init():
    gui = ParameterGUI()
    parameter, sim_time, dt = gui.run()
    return parameter, sim_time, dt

def main():
    parameter, sim_time, dt = init()
    motor = DCmotor(parameter)
    x = np.array([0.0, 0.0])  # 初期状態
    u = np.array([24.0])  # 入力（スカラー）
    func = lambda t, x: motor.state_eq(t, x, u)
    sol_Euler, sol_RK4 = run_simulation(motor, x, u, sim_time, dt)

    plot_result(sol_Euler, sol_RK4)

if __name__ == "__main__":
    main()
