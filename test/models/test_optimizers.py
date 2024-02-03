from src.models.optimizers import ScipyOptimizeMinimizeMethods


class TestScipyOptimizeMinimizeMethods:
    def test_scipy_optimize_minimize_methods(self):
        expected_value = set(["SLSQP", "trust-constr", "COBYLA"])

        actual_value = set([enum.value for enum in ScipyOptimizeMinimizeMethods])

        assert expected_value == actual_value
