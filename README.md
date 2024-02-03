
# stock-investment-split

- [stock-investment-split](#stock-investment-split)
  - [Introduction](#introduction)
  - [Example](#example)
  - [Mathematics](#mathematics)
  - [How to use?](#how-to-use)
    - [Using file](#using-file)
    - [Using Terminal](#using-terminal)
  - [Implementation Details](#implementation-details)

## Introduction

Creating this project to solve personally encountered problem of how much to invest in
each stock out of a basket to achieve a target % allocation for each stock.

## Example

Let's say you have invested in 3 stocks viz. INFOSYS, TCS and WIPRO. Your initial
investment in as follows:

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

Running the code gives that we should split the amount of $₹30$ equally across all
instruments:

```bash
>> python -m src.views.file
Optimizing the MSE to compute optimal allocation. Sit tight!
Final allocation of investment of unit 30 is as follows:
```

| Instrument | Initial<br> <br>Investment<br> <br>% | Target<br> <br>Investment<br> <br>% | Suggested<br> <br>Investment | Final<br> <br>% |
|------------|--------------------------------------|-------------------------------------|------------------------------|-----------------|
| INFOSYS    | 30                                   | 33                                  | 10                           | 30.7692         |
| TCS        | 50                                   | 33                                  | 10                           | 46.1538         |
| WIPRO      | 20                                   | 34                                  | 10                           | 23.0769         |

## Mathematics

You have a portfolio of $n$ financial instruments: $[F_1, F_2,
..., F_i, ..., F_n]$ and your current investments in each
financial instrument is: $[I_1, I_2,..., I_i, ..., I_n]$.

This means that your current investment allocation ratio (between $0$ and $1$) is $[{I_1
\over SI}, {I_2 \over SI}, ..., {I_i \over SI}, ..., {I_n \over SI}]$ where $SI =
\sum_{i=1}^nI_i$.

Now, suppose you want to invest an additional amount of $SN$ split between these $n$
financial instruments. You want to achieve a target allocation ratio of $[T_1, T_2,
..., T_i, ..., T_n]$ for each of
these instruments.

This implies that:

${(I_1 + N_1) \over (SI + SN)} = T_1,\\ {(I_2 + N_2) \over (SI + SN)} = T_2,\\ ...\\
{(I_i + N_i) \over (SI + SN)} = T_i,\\ ...\\ {(I_n + N_n) \over (SI + SN)} = T_n$

where, $N_i$ is the new investment allocated to instrument $F_i$ and our objective is to
find out these $N_i$. And, $SN = \sum_{i=1}^nN_i$ i.e. new investment that you want to
make.

To solve this problem, we have converted it into an optimizing problem. If we assume
some initial allocation for each instrument and calculate the Mean Squared Error ($MSE$)
between the objective allocation ratio and actual allocation ratio. Then, we can simply
use any (bounded and constrained, explained later) optimizing tool to solve the problem.

So,
$MSE = {1 \over n} \sum_{i=1}^n ({(I_i + N_i) \over (SI + SN)} - T_i)^2$

And, we can minimize this function to find all $N_i$s.

## How to use?

Right now there are two ways of using the code. But first setup a virtual environment
and install the requirements using `pip install -r requirements.txt` command. If there's
an interest and people find it useful, I can build a simple UI for usage.

### Using file

If you wish to easily change values to play around, you can directly modify the file
`src/views/file.py`. It already contains example values from the `README` file. To run
the code, run command `python -m src.views.file` from project directory.

### Using Terminal

If you do not wish to temper with any file, simply run code `python -m
src.views.terminal` and follow the terminal instructions. Example usage given below:

```bash
>> python -m src.views.terminal
Please add identifier/names of financial instruments separated by comma(,)
INFOSYS,TCS,WIPRO
Please add initial investment (all in same currency) of financial instruments separated by comma(,)
30,50,20
How much money do you want to invest?
30
Please add target investment ratio (between 0 and 1) of financial instruments separated by comma(,)
.33,.33,.34
```

## Implementation Details

It's a simple program with scary looking but simplistic mathematics behind it as
explained above. We have used `scipy.optimizers.minimize` function (with `SLSQP` method)
to minimize the Mean Squared Error function. There are two more methods defined in the
models viz. `TRUST_CONSTR` and `COBYLA` but they are not supported atm to keep things
simple and avoid over engineering for a plain use case.

The repository contains three parts:

- `controller`: It contains the core logic of the application.
- `models`: It contains standard pydantic/enum models used across the code.
- `views`: It provides interface to end users to interact with the code. Currently there
  are two interfaces viz. a terminal based `src/views/terminal.py` and a file based
  `src/views/file.py`.
