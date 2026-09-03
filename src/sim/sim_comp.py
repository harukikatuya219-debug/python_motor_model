import numpy as np
from types import SimpleNamespace

def euler(xn, motor, u, dt, disturbance=None):
    """オイラー法による数値積分
    
    Args:
        xn: 現在の状態ベクトル [i, ω]
        motor: DCmotorクラスのインスタンス
        u: 入力ベクトル [V]
        dt: 時間ステップ
        disturbance: 外部入力 [Tl] (デフォルト: None = ゼロ)
    
    Returns:
        次の状態ベクトル [i_next, ω_next]
    """
    dxdt = motor.state_eq(0, xn, u, disturbance)
    xn_next = xn + dxdt * dt
    return xn_next

def Runge_Kutta(xn, motor, u, dt, disturbance=None):
    """4次のルンゲ・クッタ法による数値積分
    
    Args:
        xn: 現在の状態ベクトル [i, ω]
        motor: DCmotorクラスのインスタンス
        u: 入力ベクトル [V]
        dt: 時間ステップ
        disturbance: 外部入力 [Tl] (デフォルト: None = ゼロ)
    
    Returns:
        次の状態ベクトル [i_next, ω_next]
    """
    k1 = motor.state_eq(0, xn, u, disturbance)
    k2 = motor.state_eq(0, xn + 0.5 * dt * k1, u, disturbance)
    k3 = motor.state_eq(0, xn + 0.5 * dt * k2, u, disturbance)
    k4 = motor.state_eq(0, xn + dt * k3, u, disturbance)
    
    xn_next = xn + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)
    return xn_next

def run_simulation(motor, x0, u, sim_time, dt, disturbance=None):
    """
    シミュレーションを実行する関数
    
    Args:
        motor: DCmotorクラスのインスタンス
        x0: 初期状態ベクトル [i, ω]
        u: 入力ベクトル [V]
        sim_time: シミュレーション時間のタプル (start, end)
        dt: 時間ステップ
        disturbance: 外部入力 [Tl] (デフォルト: None = ゼロ)
    
    Returns:
        t: 時間配列
        x_Euler: オイラー法による状態配列
        x_RK4: ルンゲ・クッタ法による状態配列
    """
    t = np.arange(sim_time[0], sim_time[1], dt)
    x_Euler = np.zeros((len(t), len(x0)))
    x_RK4 = np.zeros((len(t), len(x0)))
    x_Euler[0] = x0
    x_RK4[0] = x0

    
    for i in range(1, len(t)):
        x_Euler[i] = euler(x_Euler[i-1], motor, u, dt, disturbance)
        x_RK4[i] = Runge_Kutta(x_RK4[i-1], motor, u, dt, disturbance)
    
    sol_Euler = SimpleNamespace(
        t=t,
        y=x_Euler.T
    )

    sol_RK4 = SimpleNamespace(
        t=t,
        y=x_RK4.T
    )

    return sol_Euler, sol_RK4