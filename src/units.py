import math


def db_to_linear(value_dB: float) -> float:
    # dB 是对数形式的功率比值，转回线性比例时使用 10^(dB/10)。
    return 10.0 ** (value_dB / 10.0)


def linear_to_db(value: float) -> float:
    # 线性比例必须大于 0；如果为 0 或负数，取对数没有实际物理意义。
    if value <= 0:
        return float("-inf")
    return 10.0 * math.log10(value)


def dBm_to_watts(power_dBm: float) -> float:
    # dBm 是以 1 mW 为参考的绝对功率：P(W)=1e-3*10^(dBm/10)。
    return 1e-3 * db_to_linear(power_dBm)


def watts_to_dBm(power_watts: float) -> float:
    # W 转 dBm：P(dBm)=10*log10(P(W)/1mW)。
    if power_watts <= 0:
        return float("-inf")
    return 10.0 * math.log10(power_watts / 1e-3)
