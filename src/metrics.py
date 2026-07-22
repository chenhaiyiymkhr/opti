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
    # 高斯噪声近似下，BER 与 Q 因子的关系：BER≈0.5*erfc(Q/sqrt(2))。
    return 0.5 * math.erfc(q_factor / math.sqrt(2.0))


def calculate_q_ber(bits: np.ndarray, samples: np.ndarray) -> QBerResult:
    # 防止 bit 数和采样点数因边界处理略有差异，先截取共同长度。
    n = min(len(bits), len(samples))
    bits = bits[:n]
    samples = samples[:n]
    # 按原始 bit 标签把采样点分成 1 电平和 0 电平两组。
    ones = samples[bits == 1]
    zeros = samples[bits == 0]

    # 分别统计两个电平的均值和标准差。
    mu1 = float(np.mean(ones))
    mu0 = float(np.mean(zeros))
    sigma1 = float(np.std(ones, ddof=1))
    sigma0 = float(np.std(zeros, ddof=1))
    # Q 因子衡量 1/0 电平分布的分离程度，分母加极小值避免除零。
    q = (mu1 - mu0) / max(sigma1 + sigma0, 1e-12)
    ber_est = q_to_ber(q)
    # 简化判决门限取两个均值的中点。
    threshold = 0.5 * (mu1 + mu0)
    decisions = (samples >= threshold).astype(np.int8)
    # ber_counted 是有限 bit 仿真中的实际错误比例。
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
