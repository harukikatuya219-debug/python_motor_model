import pytest

from gui import ParameterGUI


def test_default_motor_values_are_realistic():
    expected = {
        "R": pytest.approx(0.5),
        "L": pytest.approx(0.003),
        "Ke": pytest.approx(0.08),
        "J": pytest.approx(0.01),
        "D": pytest.approx(0.005),
        "p": 4,
        "Kt": pytest.approx(0.08),
    }

    for key, value in expected.items():
        assert ParameterGUI.DEFAULT_MOTOR_VALUES[key] == value


def test_default_simulation_values_are_available():
    assert ParameterGUI.DEFAULT_SIMULATION_VALUES["sim_time"] == pytest.approx(2.0)
    assert ParameterGUI.DEFAULT_SIMULATION_VALUES["dt"] == pytest.approx(0.001)
