from dataclasses import dataclass

@dataclass(frozen=True)
class MotorParam:
    R: float
    L: float
    Ke: float
    J: float
    D: float
    p: int
    Kt: float