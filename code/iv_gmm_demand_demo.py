"""Synthetic Logit share inversion, price endogeneity, 2SLS, and linear GMM.

Python 3.10+, standard library only. Population shares are observed exactly.
Markets are independent; two products share a market-level quality shock.
"""

import argparse
import math
import random


PRICE_SCALE = 10.0
TRUE_ALPHA = 0.4
TRUE_THETA = (4.5, 4.0, -PRICE_SCALE * TRUE_ALPHA)


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    columns = transpose(right)
    return [[dot(row, column) for column in columns] for row in left]


def inverse(matrix):
    size = len(matrix)
    augmented = [list(row) + [float(i == j) for j in range(size)]
                 for i, row in enumerate(matrix)]
    threshold = 1e-12 * max(1.0, max(abs(v) for row in matrix for v in row))
    for col in range(size):
        pivot = max(range(col, size), key=lambda i: abs(augmented[i][col]))
        if abs(augmented[pivot][col]) <= threshold:
            raise ValueError("Singular or numerically ill-conditioned matrix; inspect identification.")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        augmented[col] = [value / scale for value in augmented[col]]
        for row in range(size):
            if row != col:
                factor = augmented[row][col]
                augmented[row] = [a - factor * b for a, b in
                                  zip(augmented[row], augmented[col])]
    return [row[size:] for row in augmented]


def cross(left, right):
    n = len(left)
    return [[value / n for value in row] for row in matmul(transpose(left), right)]


def residuals(x, y, theta):
    return [value - dot(row, theta) for row, value in zip(x, y)]


def cluster_moment_covariance(z, errors, clusters):
    """S = (1/n) sum_t h_t h_t', h_t = sum_{i in t} z_i u_i; no correction."""
    scores = {}
    for row, error, cluster in zip(z, errors, clusters):
        score = scores.setdefault(cluster, [0.0] * len(row))
        for k, value in enumerate(row):
            score[k] += value * error
    result = [[0.0] * len(z[0]) for _ in z[0]]
    for score in scores.values():
        for k in range(len(score)):
            for ell in range(len(score)):
                result[k][ell] += score[k] * score[ell] / len(z)
    return result


def fit_linear_gmm(x, y, z, clusters, weight=None):
    """Closed-form linear GMM with fixed weight and a cluster sandwich covariance."""
    n = len(x)
    if weight is None:
        weight = inverse(cross(z, z))  # This choice gives 2SLS.
    a = cross(z, x)
    b = cross(z, [[value] for value in y])
    atw = matmul(transpose(a), weight)
    bread = inverse(matmul(atw, a))
    influence = matmul(bread, atw)
    theta = [row[0] for row in matmul(influence, b)]
    errors = residuals(x, y, theta)
    s = cluster_moment_covariance(z, errors, clusters)
    covariance = [[value / n for value in row]
                  for row in matmul(matmul(influence, s), transpose(influence))]
    moments = [row[0] for row in cross(z, [[error] for error in errors])]
    criterion = dot(moments, [row[0] for row in matmul(weight, [[v] for v in moments])])
    return {'theta': theta, 'covariance': covariance, 'errors': errors, 'S': s,
            'moments': moments, 'Q': criterion, 'weight': weight}


def two_step_gmm(x, y, z, clusters):
    first = fit_linear_gmm(x, y, z, clusters)
    second = fit_linear_gmm(x, y, z, clusters, inverse(first['S']))
    return first, second


def log_shares(values):
    maximum = max(values)
    log_denom = maximum + math.log(sum(math.exp(value - maximum) for value in values))
    return [value - log_denom for value in values]


def simulate(markets=2000, seed=20261018, strength=1.0):
    rng = random.Random(seed)
    bound = math.sqrt(3.0)
    draw = lambda: rng.uniform(-bound, bound)  # mean zero and variance one
    x, y, z, bad_z, clusters = [], [], [], [], []
    maximum_inversion_error = 0.0
    for market in range(markets):
        common = draw()
        products = []
        for product, constant in enumerate((4.5, 4.0)):
            z1, z2, taste, noise = draw(), draw(), draw(), draw()
            quality = 0.4 * common + (0.5 + 0.3 * z1 * z1) * taste
            price = (10.0 + 0.7 * product + strength * (1.2 * z1 + 0.8 * z2)
                     + 0.9 * quality + 0.6 * noise)
            delta = constant - TRUE_ALPHA * price + quality
            products.append((product, price, z1, z2, quality, delta))
        logs = log_shares([0.0] + [row[-1] for row in products])
        assert math.isclose(sum(math.exp(value) for value in logs), 1.0, abs_tol=1e-12)
        for product, price, z1, z2, quality, delta in products:
            dummies = [float(product == 0), float(product == 1)]
            x.append(dummies + [price / PRICE_SCALE])
            y.append(logs[product + 1] - logs[0])
            z.append(dummies + [z1, z2])
            # An observed proxy can carry unobserved demand quality.
            bad_z.append(dummies + [z1, z2 + 0.6 * quality])
            clusters.append(market)
            maximum_inversion_error = max(maximum_inversion_error, abs(y[-1] - delta))
    return {'x': x, 'y': y, 'z': z, 'bad_z': bad_z, 'clusters': clusters,
            'inversion_error': maximum_inversion_error}


def first_stage(x, z, clusters):
    price = [row[2] for row in x]
    unrestricted = fit_linear_gmm(z, price, z, clusters)
    controls = [row[:2] for row in z]
    restricted = fit_linear_gmm(controls, price, controls, clusters)
    ssr_u = sum(value * value for value in unrestricted['errors'])
    ssr_r = sum(value * value for value in restricted['errors'])
    partial_r2 = 1.0 - ssr_u / ssr_r
    coefficients = unrestricted['theta'][2:]
    covariance = [row[2:] for row in unrestricted['covariance'][2:]]
    quadratic = dot(coefficients, [row[0] for row in
                    matmul(inverse(covariance), [[v] for v in coefficients])])
    return partial_r2, quadratic / len(coefficients)


def report_estimate(name, result):
    alpha = -result['theta'][2] / PRICE_SCALE
    se = math.sqrt(result['covariance'][2][2]) / PRICE_SCALE
    print(f"{name:12s} c_A={result['theta'][0]:.6f} c_B={result['theta'][1]:.6f} "
          f"alpha={alpha:.6f} cluster-SE(alpha)={se:.6f}")


def report_j(result, n, label):
    # Both IV specifications have four instruments and three regressors: df=1.
    statistic = max(0.0, n * result['Q'])
    p_value = math.erfc(math.sqrt(statistic / 2.0))
    print(f"{label}: J={statistic:.6f}, df=1, chi-square reference p={p_value:.6g}")
    return statistic, p_value


def mathematical_checks(data, first, second):
    assert data['inversion_error'] < 1e-12
    x, z = data['x'], data['z']
    # The computed two-step solution must minimize the fixed second-step criterion.
    errors_first = residuals(x, data['y'], first['theta'])
    g_first = [row[0] for row in cross(z, [[value] for value in errors_first])]
    q_first = dot(g_first, [row[0] for row in
                  matmul(second['weight'], [[v] for v in g_first])])
    assert second['Q'] <= q_first + 1e-12
    normal = matmul(matmul(transpose(cross(z, x)), second['weight']),
                    [[value] for value in second['moments']])
    assert max(abs(row[0]) for row in normal) < 1e-9


def positive_markets(value):
    count = int(value)
    if count < 20:
        raise argparse.ArgumentTypeError("use at least 20 markets for this numerical demo")
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--markets', type=positive_markets, default=2000)
    parser.add_argument('--seed', type=int, default=20261018)
    args = parser.parse_args()
    data = simulate(args.markets, args.seed)
    x, y, z, clusters = (data[key] for key in ('x', 'y', 'z', 'clusters'))
    try:
        ols = fit_linear_gmm(x, y, x, clusters)
        iv, gmm = two_step_gmm(x, y, z, clusters)
        mathematical_checks(data, iv, gmm)
        print('All data are synthetic; shares are population probabilities, without consumer sampling.')
        print(f'markets={args.markets}, product-market rows={len(x)}, seed={args.seed}')
        print('True c_A=4.5, c_B=4.0, alpha=0.4. Prices depend on unobserved quality.')
        print('\n1. Strong, valid instruments')
        report_estimate('OLS', ols)
        report_estimate('2SLS', iv)
        report_estimate('Two-step GMM', gmm)
        r2, wald = first_stage(x, z, clusters)
        print(f'First-stage partial R2={r2:.6f}; cluster-robust Wald/2={wald:.6f}')
        print('Wald/2 is descriptive here; it is not a universal weak-IV cutoff test.')
        report_j(gmm, len(x), 'Valid-instrument specification')

        print('\n2. Invalid proxy instrument z2 + 0.6*quality')
        _, invalid = two_step_gmm(x, y, data['bad_z'], clusters)
        report_estimate('Invalid GMM', invalid)
        report_j(invalid, len(x), 'Joint moment-specification test')
        print('Reported SE cannot correct the invalid moment conditions.')

        print('\n3. Weak valid instruments: price loading multiplied by 0.02')
        weak = simulate(args.markets, args.seed, strength=0.02)
        weak_iv = fit_linear_gmm(weak['x'], weak['y'], weak['z'], weak['clusters'])
        r2, wald = first_stage(weak['x'], weak['z'], weak['clusters'])
        print(f'2SLS alpha={-weak_iv["theta"][2]/PRICE_SCALE:.6f}; '
              f'partial R2={r2:.6f}; cluster-robust Wald/2={wald:.6f}')
        print('Ordinary Wald intervals and chi-square J inference can be unreliable under weak identification.')
        print('A non-rejection of J never proves instrument validity; finite-sample results depend on the seed.')
        print('\nShare inversion, GMM first-order conditions, and fixed-weight minimization checks passed.')
    except ValueError as error:
        parser.exit(2, f'Estimation stopped: {error}\n')


if __name__ == '__main__':
    main()
