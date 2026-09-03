import numpy as np
from motor.motor_param import MotorParam

class DCmotor:
    def __init__(self, param: MotorParam):
        self.param = param
        self._init_matrices()
    
    def _init_matrices(self):
        """
        状態方程式の係数行列を初期化
        
        状態方程式: dx = A*x + B*u + D*disturbance
        - x: [i, ω] (電流, 角速度)
        - u: [V] (電圧)
        - disturbance: [Tl] (負荷トルク)
        """
        # A行列: 状態に対する係数
        self.A = np.array([
            [-self.param.R/self.param.L, -self.param.Ke/self.param.L],
            [self.param.Kt/self.param.J, -self.param.D/self.param.J]
        ])
        # B行列: 制御入力に対する係数
        self.B = np.array([[1/self.param.L], [0]])
        # D行列: 外部入力（負荷トルク）に対する係数
        self.D = np.array([[0.0], [-1/self.param.J]])
    
    def state_eq(self, t, x, u, disturbance=None):
        """状態方程式: dx = A*x + B*u + D*disturbance
        
        Args:
            t: 時間
            x: 状態ベクトル [i, ω]
            u: 入力ベクトル [V]
            disturbance: 外部入力 [Tl] (デフォルト: None = ゼロ)
        
        Returns:
            状態の時間微分 [di/dt, dω/dt]
        """
        if disturbance is None:
            disturbance = np.zeros((1,))
        else:
            disturbance = np.atleast_1d(disturbance)
        
        dxdt = self.A @ x + self.B @ u + self.D @ disturbance
        return dxdt