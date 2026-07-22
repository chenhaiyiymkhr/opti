import math


def db_to_linear(value_dB: float) -> float:
    return 10.0 ** (value_dB / 10.0)


def linear_to_db(value: float) -> float:
    if value <= 0:
        return float("-inf")
    return 10.0 * math.log10(value)


def dBm_to_watts(power_dBm: float) -> float:
    return 1e-3 * db_to_linear(power_dBm)


def watts_to_dBm(power_watts: float) -> float:
    if power_watts <= 0:
        return float("-inf")
    return 10.0 * math.log10(power_watts / 1e-3)
