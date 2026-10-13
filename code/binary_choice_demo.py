"""Synthetic binary-choice examples; Python standard library only."""

import argparse
import math
import random


def logistic(value):
    if value >= 0:
        return 1.0 / (1.0 + math.exp(-value))
    exp_value = math.exp(value)
    return exp_value / (1.0 + exp_value)


def logit(probability):
    if not 0.0 < probability < 1.0:
        raise ValueError("Each price group must contain buyers and non-buyers.")
    return math.log(probability) - math.log1p(-probability)


def recover_parameters(price1, price2, share1, share2):
    if price1 == price2:
        raise ValueError("Two distinct prices are required to identify a and b.")
    index1, index2 = logit(share1), logit(share2)
    b = (index1 - index2) / (price2 - price1)
    return index1 + b * price1, b


def slope_se(price1, price2, share1, share2, n1, n2):
    if price1 == price2 or min(n1, n2) <= 0:
        raise ValueError("Distinct prices and positive group sizes are required.")
    logit(share1)
    logit(share2)
    variance = (1.0 / (n1 * share1 * (1.0 - share1))
                + 1.0 / (n2 * share2 * (1.0 - share2)))
    return math.sqrt(variance) / abs(price2 - price1)


def softplus(value):
    return max(value, 0.0) + math.log1p(math.exp(-abs(value)))


def log_likelihood(a, b, groups):
    # Stable Bernoulli log likelihood, without parameter-free group constants.
    return sum(-buyers * softplus(-(a - b * price))
               - (count - buyers) * softplus(a - b * price)
               for price, buyers, count in groups)


def positive_integer(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20261013)
    parser.add_argument("--n-per-price", type=positive_integer, default=4000)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    true_a, true_b = 2.0, 0.1
    price1, price2 = 10.0, 15.0
    share1 = logistic(true_a - true_b * price1)
    share2 = logistic(true_a - true_b * price2)

    print("All observations below are synthetic teaching data.")
    print("\n1. Observational equivalence at p=10")
    for a, b in ((2.0, 0.1), (3.0, 0.2)):
        print(f"a={a:.1f}, b={b:.1f}: "
              f"s(10)={logistic(a-b*10):.6f}, s(15)={logistic(a-b*15):.6f}")
    assert math.isclose(share1, logistic(3.0 - 0.2 * price1), abs_tol=1e-12)
    assert not math.isclose(share2, logistic(3.0 - 0.2 * price2), abs_tol=1e-6)

    recovered_a, recovered_b = recover_parameters(price1, price2, share1, share2)
    print("\n2. Identification using population probabilities")
    print(f"Recovered a={recovered_a:.6f}, b={recovered_b:.6f}")
    assert math.isclose(recovered_a, true_a, abs_tol=1e-12)
    assert math.isclose(recovered_b, true_b, abs_tol=1e-12)

    groups = []
    for price, probability in ((price1, share1), (price2, share2)):
        buyers = sum(rng.random() < probability for _ in range(args.n_per_price))
        groups.append((price, buyers, args.n_per_price))
    empirical1 = groups[0][1] / groups[0][2]
    empirical2 = groups[1][1] / groups[1][2]
    try:
        estimated_a, estimated_b = recover_parameters(
            price1, price2, empirical1, empirical2)
    except ValueError as error:
        parser.exit(2, f"Sample boundary: {error} Increase --n-per-price.\n")

    print("\n3. Finite-sample unconstrained MLE")
    print(f"seed={args.seed}, n per price={args.n_per_price}")
    for price, buyers, count in groups:
        fitted = logistic(estimated_a - estimated_b * price)
        print(f"p={price:.1f}: buyers={buyers}/{count}, "
              f"sample share={buyers/count:.6f}, fitted={fitted:.6f}")
        assert math.isclose(fitted, buyers / count, abs_tol=1e-12)
    estimated_se = slope_se(price1, price2, empirical1, empirical2,
                            args.n_per_price, args.n_per_price)
    print(f"a_hat={estimated_a:.6f}, b_hat={estimated_b:.6f}, "
          f"approximate SE(b_hat)={estimated_se:.6f}")
    if estimated_b <= 0:
        print("The unconstrained estimate does not satisfy the assumed b > 0.")
    fitted_ll = log_likelihood(estimated_a, estimated_b, groups)
    true_ll = log_likelihood(true_a, true_b, groups)
    print(f"log likelihood: estimated={fitted_ll:.6f}, true={true_ll:.6f}")
    assert fitted_ll >= true_ll - 1e-8

    print("\n4. Population-based asymptotic precision comparison")
    standard_errors = []
    for alternative_price in (15.0, 10.1):
        alternative_share = logistic(true_a - true_b * alternative_price)
        standard_error = slope_se(price1, alternative_price, share1,
                                 alternative_share, args.n_per_price,
                                 args.n_per_price)
        standard_errors.append(standard_error)
        print(f"prices=(10, {alternative_price:g}): "
              f"approximate SE(b_hat)={standard_error:.6f}")
    assert standard_errors[1] > standard_errors[0]
    print("\nAll mathematical checks passed.")


if __name__ == "__main__":
    main()
