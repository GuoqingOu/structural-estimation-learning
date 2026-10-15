"""Two products plus an outside option: synthetic multinomial Logit demand.

Python 3.10+, standard library only. Prices are exogenous by construction.
The optimizer uses theta=(c_A, c_B, 10*alpha) for numerical conditioning.
"""

import argparse
import math
import random


PRICE_SCALE = 10.0
PRICES = ((8.0, 9.0), (10.0, 8.0), (12.0, 13.0),
          (14.0, 10.0), (9.0, 14.0), (11.0, 12.0))
TRUE_THETA = (2.0, 1.6, 1.0)  # alpha = 1 / PRICE_SCALE = 0.1


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def features(prices):
    return ((0.0, 0.0, 0.0),
            (1.0, 0.0, -prices[0] / PRICE_SCALE),
            (0.0, 1.0, -prices[1] / PRICE_SCALE))


def log_probabilities(values):
    maximum = max(values)
    shifted = [value - maximum for value in values]
    log_denom = math.log(sum(math.exp(value) for value in shifted))
    return [value - log_denom for value in shifted]


def shares(theta, prices):
    values = [dot(theta, row) for row in features(prices)]
    return [math.exp(value) for value in log_probabilities(values)]


def solve_linear(matrix, rhs):
    """Small linear solve with partial pivoting; singular designs are rejected."""
    size = len(rhs)
    augmented = [list(row) + [value] for row, value in zip(matrix, rhs)]
    for col in range(size):
        pivot = max(range(col, size), key=lambda row: abs(augmented[row][col]))
        if abs(augmented[pivot][col]) < 1e-12:
            raise ValueError("Singular information matrix: check price variation and design.")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        augmented[col] = [value / scale for value in augmented[col]]
        for row in range(size):
            if row != col:
                factor = augmented[row][col]
                augmented[row] = [a - factor * b for a, b in
                                  zip(augmented[row], augmented[col])]
    return [row[-1] for row in augmented]


def objective(theta, markets):
    """Average log likelihood, its score, and negative Hessian."""
    total = sum(sum(counts) for _, counts in markets)
    if total <= 0:
        raise ValueError("Positive counts are required.")
    likelihood = 0.0
    gradient = [0.0] * 3
    information = [[0.0] * 3 for _ in range(3)]
    for prices, counts in markets:
        x = features(prices)
        log_probs = log_probabilities([dot(theta, row) for row in x])
        probabilities = [math.exp(value) for value in log_probs]
        count = sum(counts)
        mean_x = [sum(probabilities[j] * x[j][k] for j in range(3))
                  for k in range(3)]
        likelihood += sum(counts[j] * log_probs[j] for j in range(3))
        for k in range(3):
            gradient[k] += sum(counts[j] * x[j][k] for j in range(3)) - count * mean_x[k]
            for ell in range(3):
                second = sum(probabilities[j] * x[j][k] * x[j][ell] for j in range(3))
                information[k][ell] += count * (second - mean_x[k] * mean_x[ell])
    return (likelihood / total, [value / total for value in gradient],
            [[value / total for value in row] for row in information])


def fit(markets, start=(0.0, 0.0, 0.0), tolerance=1e-10):
    # Requiring all cells positive is a conservative teaching-data safeguard.
    # A zero cell alone need not prevent finite MLE in a general Logit model.
    if not markets or any(count <= 0 for _, counts in markets for count in counts):
        raise ValueError("This demo requires positive counts for every option in each market.")
    theta = list(start)
    for iteration in range(100):
        value, gradient, information = objective(theta, markets)
        # Also check the design when a starting value happens to have zero score.
        step = solve_linear(information, gradient)
        if max(abs(item) for item in gradient) < tolerance:
            return theta, iteration, value, information
        improvement = dot(gradient, step)
        factor = 1.0
        for _ in range(40):
            candidate = [old + factor * move for old, move in zip(theta, step)]
            candidate_value = objective(candidate, markets)[0]
            if candidate_value >= value + 1e-4 * factor * improvement - 1e-14:
                theta = candidate
                break
            factor *= 0.5
        else:
            raise ValueError("Line search failed; inspect the design and sample.")
    raise ValueError("No convergence within 100 Newton iterations.")


def price_derivatives(probabilities, alpha):
    """Rows: shares of outside, A, B. Columns: prices of A, B."""
    return [[-alpha * probabilities[j] * ((1.0 if j == k else 0.0) - probabilities[k])
             for k in (1, 2)] for j in range(3)]


def simulate(seed, count):
    rng = random.Random(seed)
    markets = []
    for prices in PRICES:
        probabilities = shares(TRUE_THETA, prices)
        counts = [0, 0, 0]
        for _ in range(count):
            draw = rng.random()
            choice = (0 if draw < probabilities[0] else
                      1 if draw < probabilities[0] + probabilities[1] else 2)
            counts[choice] += 1
        markets.append((prices, counts))
    return markets


def mathematical_checks():
    baseline_prices = (10.0, 12.0)
    baseline = shares(TRUE_THETA, baseline_prices)
    assert math.isclose(sum(baseline), 1.0, abs_tol=1e-12)
    for j in (1, 2):
        expected = dot(TRUE_THETA, features(baseline_prices)[j])
        assert math.isclose(math.log(baseline[j] / baseline[0]), expected, abs_tol=1e-12)
    # Expected counts represent a population objective, not a random sample.
    population = [(prices, shares(TRUE_THETA, prices)) for prices in PRICES]
    recovered = fit(population)[0]
    assert all(math.isclose(a, b, abs_tol=1e-7) for a, b in zip(recovered, TRUE_THETA))
    # Analytic share derivatives must agree with numerical perturbations.
    analytic = price_derivatives(baseline, TRUE_THETA[2] / PRICE_SCALE)
    epsilon = 1e-4
    for column in range(2):
        plus, minus = list(baseline_prices), list(baseline_prices)
        plus[column] += epsilon
        minus[column] -= epsilon
        upper, lower = shares(TRUE_THETA, plus), shares(TRUE_THETA, minus)
        assert math.isclose(sum(row[column] for row in analytic), 0.0, abs_tol=1e-12)
        for row in range(3):
            difference = (upper[row] - lower[row]) / (2.0 * epsilon)
            assert math.isclose(difference, analytic[row][column], abs_tol=1e-9)
    # Changing only B's price leaves the A/outside odds unchanged under IIA.
    changed = shares(TRUE_THETA, (10.0, 20.0))
    assert math.isclose(baseline[1] / baseline[0], changed[1] / changed[0], rel_tol=1e-12)
    return recovered


def positive_integer(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20261015)
    parser.add_argument("--n-per-market", type=positive_integer, default=4000)
    args = parser.parse_args()
    recovered = mathematical_checks()
    print("All data are synthetic. Outside option is included in every market.")
    print("\n1. Population recovery")
    print(f"c_A={recovered[0]:.6f}, c_B={recovered[1]:.6f}, "
          f"alpha={recovered[2]/PRICE_SCALE:.6f}")
    markets = simulate(args.seed, args.n_per_market)
    try:
        estimate, iterations, value, information = fit(markets)
    except ValueError as error:
        parser.exit(2, f"Estimation stopped: {error}\n")
    alpha = estimate[2] / PRICE_SCALE
    total_count = len(markets) * args.n_per_market
    variance_scaled = solve_linear(information, (0.0, 0.0, 1.0))[2] / total_count
    se_alpha = math.sqrt(variance_scaled) / PRICE_SCALE
    print("\n2. Grouped multinomial maximum likelihood")
    print(f"seed={args.seed}, markets={len(markets)}, n per market={args.n_per_market}")
    print("prices          counts [outside,A,B]     fitted shares [outside,A,B]")
    for prices, counts in markets:
        predicted = ", ".join(f"{item:.4f}" for item in shares(estimate, prices))
        print(f"{str(prices):15} {str(counts):25} [{predicted}]")
    print(f"c_A_hat={estimate[0]:.6f}, c_B_hat={estimate[1]:.6f}, "
          f"alpha_hat={alpha:.6f}, approximate SE(alpha_hat)={se_alpha:.6f}")
    print(f"Newton iterations={iterations}, average log likelihood={value:.8f}")
    if alpha <= 0:
        print("The unconstrained estimate does not satisfy the teaching assumption alpha > 0.")
    assert value >= objective(TRUE_THETA, markets)[0] - 1e-10

    baseline_prices, new_prices = (10.0, 12.0), (12.0, 12.0)
    before, after = shares(estimate, baseline_prices), shares(estimate, new_prices)
    derivatives = price_derivatives(before, alpha)
    print("\n3. Demand-only price change using estimated parameters")
    for j, name in enumerate(("outside", "A", "B")):
        print(f"{name}: before={before[j]:.6f}, after={after[j]:.6f}, "
              f"change={after[j]-before[j]:+.6f}")
    print("Elasticity rows [A,B], price columns [A,B]:")
    for j in (1, 2):
        print([round(derivatives[j][k] * baseline_prices[k] / before[j], 6)
               for k in range(2)])
    print("No firm pricing or equilibrium response is modeled here.")

    print("\n4. IIA and duplicate-label illustration")
    print("Equal systematic utilities: [outside,A,B] -> shares [1/3,1/3,1/3]")
    duplicate = [math.exp(item) for item in log_probabilities((0.0, 0.0, 0.0, 0.0))]
    print(f"Treat A2 as an independent option: [outside,A,A2,B] -> {duplicate}")
    print("A and A2 together receive 1/2. A mere duplicate label is not a new independent option.")
    print("\nProbability, population recovery, derivative, IIA, and likelihood checks passed.")


if __name__ == "__main__":
    main()
