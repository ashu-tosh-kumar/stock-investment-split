
# stock-investment-split

- [stock-investment-split](#stock-investment-split)
  - [Introduction](#introduction)
  - [Example](#example)
  - [Solution Methods](#solution-methods)
    - [Numerical Optimization](#numerical-optimization)
    - [Analytical Solution](#analytical-solution)
  - [Mathematics](#mathematics)
    - [Numerical Approach](#numerical-approach)
    - [Analytical Approach](#analytical-approach)
  - [Assumptions](#assumptions)
  - [How to use?](#how-to-use)
    - [Using file](#using-file)
    - [Using Terminal](#using-terminal)
    - [Method Selection](#method-selection)
  - [Implementation Details](#implementation-details)
  - [Changelog](#changelog)

## Introduction

This project solves the problem of optimal investment allocation: how much to invest in
each financial instrument from a portfolio to achieve target percentage allocations.

The system provides two complementary approaches:
- **Numerical optimization** using scipy's constrained minimization
- **Analytical solution** using mathematical derivation with Lagrange multipliers

Both methods minimize the Mean Squared Error (MSE) between actual and target allocations,
with the analytical solution providing exact optimal results and the numerical method
offering enhanced robustness through smart initial guessing and fallback strategies.

## Example

Let's say you have invested in 3 stocks (or any other instruments for that matter) viz.
INFOSYS, TCS and WIPRO. Your initial investment in as follows:

| Instrument | Initial Investment | Initial Investment % | Target Investment % |
|------------|--------------------|--------------------------|-------------------------|
| INFOSYS    | ₹30                 | 30%                      | 33%                     |
| TCS        | ₹50                 | 50%                      | 33%                     |
| WIPRO      | ₹20                 | 20%                      | 34%                     |

Now, you want to invest an additional sum of $₹30$ in such a way that your investment in
each of these stocks reach closer to their respective target investment %. So, how
much should you invest in each of these three stocks?

If we assume that we invest $₹10$ in INFOSYS, $₹5$ in TCS and $₹15$ in WIPRO, then the
allocation % would become:

| Instrument | Allocation % |
|------------|------------------|
| INFOSYS    | 30.7%            |
| TCS        | 42.3%            |
| WIPRO      | 26.9%            |

However, these might not be the most optimal allocation. Our objective here is to find
the most optimal allocation.

Running the enhanced code now provides optimal allocation using both analytical and 
numerical methods:

```bash
>> python -m src.views.file
Computing optimal allocation using both analytical and numerical methods for comparison...
Analytical solution is optimal
Final allocation of investment of unit 30 is as follows:
```

| Instrument | Initial Investment % | Target Investment % | Suggested Investment | Final % |
|------------|---------------------|---------------------|---------------------|---------|
| INFOSYS    | 30                  | 33                  | 11                  | 31.54   |
| TCS        | 50                  | 33                  | 0                   | 38.46   |
| WIPRO      | 20                  | 34                  | 19                  | 30.00   |

```
============================================================
SOLUTION ANALYSIS
============================================================
Analytical MSE: 0.001824
Numerical MSE:  0.001824
Analytical solution is better by 0.00%
Both solutions are very similar (difference < 0.01)

ANALYTICAL SOLUTION DETAILS:
   • Unconstrained feasible: No
   • Constraint iterations: 1
   • Constrained instruments: [1]
   • Final MSE: 0.001621
============================================================
```

Notice how the enhanced system correctly identifies that TCS (which is over-allocated 
at 50% vs target 33%) should receive no new investment, while INFOSYS and WIPRO 
(both under-allocated) receive the optimal amounts to minimize allocation error.

## Solution Methods

The system provides two complementary approaches to solve the investment allocation problem:

### Numerical Optimization

The original approach uses scipy's constrained optimization to minimize the MSE function.
This method has been enhanced with:

- **Smart initial guessing** using analytical solution as starting point
- **Multiple fallback strategies** for optimization failures
- **Comprehensive edge case handling** for zero investments and infeasible targets
- **Enhanced convergence validation** and result sanitization

### Analytical Solution

**Note**: The analytical solution was developed using WindSurf's agentic mode to address
edge cases and the equal-splitting bias observed in the original numerical approach.

The analytical method derives the exact mathematical solution using Lagrange multipliers,
providing:

- **Exact optimal allocation** without numerical approximation errors
- **Instant computation** with no iterative convergence required
- **Mathematical insight** into why certain allocations are optimal
- **Constraint handling** through iterative redistribution for non-negativity requirements

The analytical approach often reveals that optimal allocation involves putting all new
investment into under-allocated instruments rather than splitting equally across all
instruments.

## Mathematics

### Problem Formulation

You have a portfolio of $n$ financial instruments: $[F_1, F_2, ..., F_i, ..., F_n]$ 
and your current investments in each financial instrument is: $[I_1, I_2,..., I_i, ..., I_n]$.

This means that your current investment allocation ratio (between $0$ and $1$) is 
$[{I_1 \over SI}, {I_2 \over SI}, ..., {I_i \over SI}, ..., {I_n \over SI}]$ where $SI = \sum_{i=1}^nI_i$.

Now, suppose you want to invest an additional amount of $SN$ split between these $n$
financial instruments. You want to achieve a target allocation ratio of $[T_1, T_2, ..., T_i, ..., T_n]$ 
for each of these instruments.

The objective is to find the optimal allocation $[N_1, N_2, ..., N_i, ..., N_n]$ where 
$N_i$ is the new investment allocated to instrument $F_i$, subject to:

- **Sum constraint**: $\sum_{i=1}^nN_i = SN$ (must invest the full amount)
- **Non-negativity constraint**: $N_i \geq 0$ (no selling of existing investments)
- **Optimality**: Minimize deviation from target allocations

### Numerical Approach

The original approach converts this into an optimization problem by minimizing the 
Mean Squared Error (MSE) between actual and target allocation ratios:

$MSE = {1 \over n} \sum_{i=1}^n \left({(I_i + N_i) \over (SI + SN)} - T_i\right)^2$

This is solved using scipy's constrained optimization with:
- **Objective function**: Minimize MSE
- **Equality constraint**: $\sum_{i=1}^nN_i = SN$
- **Bound constraints**: $0 \leq N_i \leq SN$ for all $i$
- **Method**: SLSQP (Sequential Least Squares Programming)

### Analytical Approach

The analytical solution derives the exact mathematical optimum using Lagrange multipliers.

**Step 1: Lagrangian Formulation**

$L = {1 \over n} \sum_{i=1}^n \left({(I_i + N_i) \over (SI + SN)} - T_i\right)^2 + \lambda\left(\sum_{i=1}^nN_i - SN\right)$

**Step 2: First-Order Conditions**

Taking partial derivatives and setting them to zero:

${\partial L \over \partial N_i} = {2 \over n} \cdot {1 \over (SI + SN)} \left({(I_i + N_i) \over (SI + SN)} - T_i\right) + \lambda = 0$

**Step 3: Unconstrained Solution**

Solving the system of equations yields:

$N_i = (SI + SN) \cdot T_i - I_i$

This elegant formula directly calculates how much each instrument "needs" to reach its target allocation.

**Step 4: Constraint Handling**

When $N_i < 0$ (instrument is over-allocated), the solution uses iterative redistribution:
1. Set negative $N_i$ values to zero
2. Redistribute the remaining investment among instruments that can accept it
3. Repeat until all constraints are satisfied

The analytical solution often reveals that optimal allocation involves concentrating 
new investment in under-allocated instruments rather than splitting equally across all instruments.

## Assumptions

- **No selling**: The system does not sell existing instruments to adjust allocations.
  All optimization is achieved through new investment allocation only.
- **Full investment**: The entire `new_investment` amount must be allocated across
  the instruments. Partial investment is not supported.
- **Target ratios sum to 1**: The target allocation ratios must sum to 1.0 (100%).
- **Non-negative investments**: All initial investments and target ratios must be
  non-negative values.
- **Currency consistency**: All investment amounts should be in the same currency unit.

## How to use?

Setup a virtual environment and install the requirements using `pip install poetry` 
and then `poetry install` command.

### Using file

Modify the file `src/views/file.py` with your investment data. It contains example 
values from this README. Run with:

```bash
python -m src.views.file
```

### Using Terminal

For interactive input without modifying files:

```bash
python -m src.views.terminal
```

Example terminal session:
```bash
Please add identifier/names of financial instruments separated by comma(,)
INFOSYS,TCS,WIPRO
Please add initial investment (all in same currency) of financial instruments separated by comma(,)
30,50,20
How much money do you want to invest?
30
Please add target investment ratio (between 0 and 1) of financial instruments separated by comma(,)
.33,.33,.34
```

### Method Selection

The system supports three solution methods:

**1. Analytical Solution (Recommended)**
```python
from src.controller.run import run

results, metadata = run(financial_instruments, new_investment, method="analytical")
```

**2. Enhanced Numerical Optimization**
```python
results, metadata = run(financial_instruments, new_investment, method="numerical")
```

**3. Both Methods with Comparison (Default)**
```python
results, metadata = run(financial_instruments, new_investment, method="both")
```

The `metadata` dictionary contains detailed information about the solution process,
including MSE values, constraint handling details, and method comparison results.

## Implementation Details

The system implements both numerical and analytical approaches to solve the investment
allocation optimization problem.

### Architecture

The repository follows a clean architecture pattern with three main components:

- **`controller`**: Contains the core optimization logic
  - `run.py`: Main orchestration with dual method support
  - `analytical_solver.py`: Exact mathematical solution using Lagrange multipliers
  - `scipy_optimizer.py`: Enhanced numerical optimization with smart initial guessing
  - `error.py`: MSE calculation functions
  - `utils/`: Result processing and validation utilities

- **`models`**: Pydantic models and enums for type safety
  - `financial_instruments.py`: Portfolio and instrument data models
  - `optimizers.py`: Optimization method enumerations

- **`views`**: User interfaces
  - `file.py`: File-based interface with predefined examples
  - `terminal.py`: Interactive command-line interface

### Key Enhancements

**Analytical Solution**: Developed using WindSurf's agentic mode to address edge cases
and equal-splitting bias. Provides exact optimal allocation using mathematical derivation.

**Enhanced Numerical Optimizer**: 
- Smart initial guessing using analytical solution
- Multiple fallback strategies for convergence failures
- Comprehensive input validation and edge case handling
- Enhanced result sanitization and validation

**Dual Method Architecture**: 
- Compare analytical vs numerical solutions
- Automatic selection of optimal result
- Detailed metadata and performance analysis
- Backward compatibility support

### Supported Optimization Methods

- **SLSQP**: Sequential Least Squares Programming (primary method)
- **TRUST_CONSTR**: Trust region constrained optimization (fallback)
- **L_BFGS_B**: Limited-memory BFGS with bounds (fallback)

## Changelog

### v0.2.0 (Enhanced with WindSurf Agentic Mode)

**Major Enhancements:**
- **Analytical Solution**: Added exact mathematical solution using Lagrange multipliers
- **Equal Splitting Fix**: Resolved bias where optimizer would split investment equally even when optimal solution required concentrated allocation
- **Enhanced Numerical Optimizer**: Smart initial guessing, multiple fallback strategies, comprehensive edge case handling
- **Dual Method Architecture**: Compare analytical vs numerical solutions with automatic optimal selection
- **Edge Case Handling**: Robust handling of zero investments, infeasible targets, and constraint violations
- **Solution Analysis**: Detailed metadata including MSE comparison, constraint handling details, and convergence information

**Technical Improvements:**
- Smart initial guess using analytical solution for numerical optimizer
- Iterative redistribution algorithm for constraint handling
- Enhanced input validation and error handling
- Comprehensive test suite demonstrating all improvements
- Backward compatibility support with `run_simple()` function

**Files Added/Modified:**
- `src/controller/analytical_solver.py` (new)
- `src/controller/scipy_optimizer.py` (enhanced)
- `src/controller/run.py` (dual method support)
- `src/controller/utils/results.py` (metadata display)
- `test_edge_cases.py` (comprehensive tests)

### v0.1.1

- Package and security upgrades
- Fix code smell per Sonarlint and Snyk

### v0.1.0

- First working release with numerical optimization
