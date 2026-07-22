import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class QBerResult:
    mu1: float
    mu0: float
    sigma1: float
    sigma0: float
    q_factor: float
    ber_estimate: float
    decision_threshold: float
    ber_counted: float


def q_to_ber(q_factor: float) -> float:
    return 0.5 * math.erfc(q_factor / math.sqrt(2.0))


def calculate_q_ber(bits: np.ndarray, samples: np.ndarray) -> QBerResult:
    n = min(len(bits), len(samples))
    bits = bits[:n]
    samples = samples[:n]
    ones = samples[bits == 1]
    zeros = samples[bits == 0]

    mu1 = float(np.mean(ones))
    mu0 = float(np.mean(zeros))
    sigma1 = float(np.std(ones, ddof=1))
    sigma0 = float(np.std(zeros, ddof=1))
    q = (mu1 - mu0) / max(sigma1 + sigma0, 1e-12)
    ber_est = q_to_ber(q)
    threshold = 0.5 * (mu1 + mu0)
    decisions = (samples >= threshold).astype(np.int8)
    ber_counted = float(np.mean(decisions != bits))

    return QBerResult(
        mu1=mu1,
        mu0=mu0,
        sigma1=sigma1,
        sigma0=sigma0,
        q_factor=float(q),
        ber_estimate=float(ber_est),
        decision_threshold=float(threshold),
        ber_counted=ber_counted,
    )
