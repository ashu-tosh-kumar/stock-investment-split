"""
Analytical solution for optimal investment allocation.

This module provides an exact analytical solution to the investment allocation problem,
which can be used as an alternative to numerical optimization or for validation.
"""

from typing import List, Tuple

import numpy as np

from src.models.financial_instruments import FinancialInstruments


class AnalyticalSolver:
    """
    Provides analytical solution for optimal investment allocation.

    The analytical solution is derived from minimizing the MSE:
    MSE = (1/n) * Σ[(I_i + N_i)/(SI + SN) - T_i]²

    Subject to: Σ N_i = SN and N_i ≥ 0

    The unconstrained solution is: N_i = (SI + SN) * T_i - I_i
    """

    def __init__(self, financial_instruments: FinancialInstruments, new_investment: float):
        """
        Initialize the analytical solver.

        Args:
            financial_instruments: Portfolio of financial instruments
            new_investment: Total amount of new investment to allocate
        """
        self.financial_instruments = financial_instruments
        self.new_investment = new_investment
        self.num_instruments = len(financial_instruments.instruments)

        # Pre-calculate values
        self.initial_investments = np.array([inst.initial_investment for inst in financial_instruments.instruments])
        self.target_ratios = np.array([inst.target_investment_ratio for inst in financial_instruments.instruments])
        self.total_initial_investment = np.sum(self.initial_investments)
        self.total_final_investment = self.total_initial_investment + new_investment

        # Validate inputs
        self._validate_inputs()

    def _validate_inputs(self) -> None:
        """Validate input parameters for feasibility."""
        if self.new_investment <= 0:
            raise ValueError("New investment must be positive")

        if np.any(self.initial_investments < 0):
            raise ValueError("Initial investments cannot be negative")

        if np.any(self.target_ratios < 0) or np.any(self.target_ratios > 1):
            raise ValueError("Target ratios must be between 0 and 1")

        if not np.isclose(np.sum(self.target_ratios), 1.0, atol=1e-6):
            raise ValueError("Target ratios must sum to 1.0")

    def solve(self) -> Tuple[np.ndarray, dict]:
        """
        Solve for optimal allocation analytically.

        Returns:
            Tuple containing:
            - np.ndarray: Optimal allocation for each instrument
            - dict: Solution metadata including feasibility info
        """
        # Step 1: Calculate unconstrained analytical solution
        unconstrained_allocation = self._calculate_unconstrained_solution()

        # Step 2: Handle non-negativity constraints
        allocation, metadata = self._handle_constraints(unconstrained_allocation)

        # Step 3: Validate final solution
        self._validate_solution(allocation)

        return allocation, metadata

    def _calculate_unconstrained_solution(self) -> np.ndarray:
        """
        Calculate the unconstrained analytical solution.

        Formula: N_i = (SI + SN) * T_i - I_i

        Returns:
            Unconstrained allocation for each instrument
        """
        return self.total_final_investment * self.target_ratios - self.initial_investments

    def _handle_constraints(self, unconstrained_allocation: np.ndarray) -> Tuple[np.ndarray, dict]:
        """
        Handle non-negativity constraints using iterative redistribution.

        Args:
            unconstrained_allocation: Initial unconstrained solution

        Returns:
            Tuple of constrained allocation and metadata
        """
        allocation = unconstrained_allocation.copy()
        metadata = {"is_unconstrained_feasible": np.all(allocation >= 0), "iterations": 0, "constrained_instruments": [], "final_mse": 0.0}

        if metadata["is_unconstrained_feasible"]:
            metadata["final_mse"] = self._calculate_mse(allocation)
            return allocation, metadata

        # Iteratively handle constraints
        max_iterations = self.num_instruments
        for iteration in range(max_iterations):
            # Find instruments with negative allocation
            negative_mask = allocation < 0

            if not np.any(negative_mask):
                break

            # Set negative allocations to zero
            negative_amount = np.sum(allocation[negative_mask])
            constrained_instruments = np.where(negative_mask)[0]
            metadata["constrained_instruments"].extend(constrained_instruments.tolist())

            allocation[negative_mask] = 0

            # Redistribute among remaining instruments
            remaining_mask = ~negative_mask
            if not np.any(remaining_mask):
                # All instruments are constrained - infeasible target
                raise ValueError("Target allocation is infeasible with given constraints")

            # Redistribute proportionally based on remaining "capacity"
            remaining_capacity = np.zeros_like(allocation)
            for i in np.where(remaining_mask)[0]:
                target_amount = self.total_final_investment * self.target_ratios[i] - self.initial_investments[i]
                remaining_capacity[i] = max(0, target_amount - allocation[i])

            total_capacity = np.sum(remaining_capacity)
            if total_capacity > 0:
                redistribution = -negative_amount * (remaining_capacity / total_capacity)
                allocation += redistribution
            else:
                # Distribute equally among remaining instruments
                num_remaining = np.sum(remaining_mask)
                allocation[remaining_mask] += -negative_amount / num_remaining

            metadata["iterations"] = iteration + 1

        # Final validation
        if np.any(allocation < -1e-10):  # Allow for small numerical errors
            raise ValueError("Unable to find feasible solution")

        # Clean up small negative values due to numerical precision
        allocation = np.maximum(allocation, 0)

        # Ensure sum constraint is satisfied
        total_allocated = np.sum(allocation)
        if not np.isclose(total_allocated, self.new_investment, atol=1e-10):
            # Adjust proportionally
            if total_allocated > 0:
                allocation *= self.new_investment / total_allocated

        metadata["final_mse"] = self._calculate_mse(allocation)
        return allocation, metadata

    def _calculate_mse(self, allocation: np.ndarray) -> float:
        """Calculate MSE for given allocation."""
        final_investments = self.initial_investments + allocation
        final_ratios = final_investments / self.total_final_investment
        squared_errors = (final_ratios - self.target_ratios) ** 2
        return np.mean(squared_errors)

    def _validate_solution(self, allocation: np.ndarray) -> None:
        """Validate the final solution."""
        # Check non-negativity
        if np.any(allocation < -1e-10):
            raise ValueError("Solution contains negative allocations")

        # Check sum constraint
        total_allocated = np.sum(allocation)
        if not np.isclose(total_allocated, self.new_investment, atol=1e-10):
            raise ValueError(f"Allocation sum {total_allocated} != new investment {self.new_investment}")

    def compare_with_equal_split(self) -> dict:
        """
        Compare analytical solution with equal split approach.

        Returns:
            Comparison metrics
        """
        # Equal split allocation
        equal_split = np.full(self.num_instruments, self.new_investment / self.num_instruments)
        equal_split_mse = self._calculate_mse(equal_split)

        # Analytical solution
        analytical_allocation, metadata = self.solve()
        analytical_mse = metadata["final_mse"]

        return {
            "equal_split_mse": equal_split_mse,
            "analytical_mse": analytical_mse,
            "improvement_ratio": equal_split_mse / analytical_mse if analytical_mse > 0 else float("inf"),
            "mse_reduction": equal_split_mse - analytical_mse,
            "equal_split_allocation": equal_split.tolist(),
            "analytical_allocation": analytical_allocation.tolist(),
        }


def solve_analytically(financial_instruments: FinancialInstruments, new_investment: float) -> Tuple[List[float], dict]:
    """
    Convenience function to solve investment allocation analytically.

    Args:
        financial_instruments: Portfolio of financial instruments
        new_investment: Total amount of new investment to allocate

    Returns:
        Tuple containing allocation list and solution metadata
    """
    solver = AnalyticalSolver(financial_instruments, new_investment)
    allocation, metadata = solver.solve()
    return allocation.tolist(), metadata
