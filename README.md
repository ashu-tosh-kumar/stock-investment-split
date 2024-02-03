
# stock-investment-split

- [stock-investment-split](#stock-investment-split)
  - [Introduction](#introduction)
  - [Example](#example)
  - [Mathematics](#mathematics)
  - [How to use?](#how-to-use)
  - [Implementation Details](#implementation-details)

## Introduction

Creating this project to solve personally encountered problem of how much to invest in
each stock out of a basket to achieve a target % allocation for each stock.

## Example

Let's say you have invested in 3 stocks viz. INFOSYS, TCS and WIPRO. Your initial
investment in as follows:

| Instrument | Initial Investment | Initial Investment Ratio | Target Investment Ratio |
|------------|--------------------|--------------------------|-------------------------|
| INFOSYS    | ₹30                 | 30%                      | 33%                     |
| TCS        | ₹50                 | 50%                      | 33%                     |
| WIPRO      | ₹20                 | 20%                      | 34%                     |

Now, you want to invest an additional sum of $₹30$ in such a way that your investment in
each of these stocks reach closer to their respective target investment ratio. So, how
much should you invest in each of these three stocks?

If we assume that we invest $₹10$ in INFOSYS, $₹5$ in TCS and $₹15$ in WIPRO, then the
allocation ratio would become:
| Instrument | Allocation ratio |
|------------|------------------|
| INFOSYS    | 30.7%            |
| TCS        | 42.3%            |
| WIPRO      | 26.9%            |

However, these might not be the most optimal allocation. Our objective here is to find
the most optimal allocation.

## Mathematics

You have a portfolio of $n$ financial instruments: $[F_1, F_2,
..., F_i, ..., F_n]$ and your current investments in each
financial instrument is: $[I_1, I_2,..., I_i, ..., I_n]$.

This means that your current investment allocation ratio is $[{I_1 \over SI},
{I_2 \over SI}, ..., {I_i \over SI}, ..., {I_n \over SI}]$ where
$SI = \sum_{i=1}^nI_i$.

Now, suppose you want to invest an additional amount of $SN$ split between these $n$
financial instruments. You want to achieve a target allocation ratio of $[T_1, T_2,
..., T_i, ..., T_n]$ for each of
these instruments.

This implies that:

$$
{(I_1 + N_1) \over (SI + SN)} = T_1\\

{(I_2 + N_2) \over (SI + SN)} = T_2\\

...\\

{(I_i + N_i) \over (SI + SN)} = T_i\\

...\\

{(I_n + N_n) \over (SI + SN)} = T_n
$$

where, $N_i$ is the new investment allocated to instrument
$F_i$ and our objective is to find out these
$N_i$. And, $SN = \sum_{i=1}^nN_i$ i.e. new
investment that you want to make.

To solve this problem, I have converted it into an optimizing problem. If we assume some
initial allocation for each instrument and calculate the Mean Squared Error ($MSE$)
between the objective allocation ratio and actual allocation ratio. Then, we can simply
use any (bounded and constrained, explained later) optimizing tool to solve the problem.

So,
$$
MSE = {1 \over n} \sum_{i=1}^n ({(I_i + N_i) \over (SI + SN)} - T_i)^2
$$

And, we can minimize this function to find all $N_i$s.

## How to use?

## Implementation Details
