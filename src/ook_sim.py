import numpy as np


def generate_bits(num_bits: int, seed: int) -> np.ndarray:
    # 固定随机种子，保证每次运行生成相同 bit 序列，便于复现实验结果。
    rng = np.random.default_rng(seed)
    return rng.integers(0, 2, size=num_bits, dtype=np.int8)


def raised_edge_nrz(bits: np.ndarray, samples_per_bit: int, extinction_ratio_dB: float):
    """Return a simple NRZ-OOK waveform with a mild finite-bandwidth edge shape."""
    # 消光比 ER = P1/P0；dB 转线性后，用 high=1、low=1/ER 表示 OOK 高低电平。
    er_linear = 10.0 ** (extinction_ratio_dB / 10.0)
    low_level = 1.0 / er_linear
    high_level = 1.0
    # bit=1 映射为高电平，bit=0 映射为低电平。
    symbols = np.where(bits > 0, high_level, low_level)
    # 每个 bit 扩展成 samples_per_bit 个采样点，形成 NRZ 波形。
    waveform = np.repeat(symbols, samples_per_bit).astype(float)

    # Small moving-average low-pass to make the eye diagram look more realistic.
    # 用简单移动平均模拟有限带宽导致的边沿变缓。
    kernel_len = max(3, samples_per_bit // 4)
    kernel = np.ones(kernel_len) / kernel_len
    filtered = np.convolve(waveform, kernel, mode="same")
    return filtered, low_level, high_level


def add_awgn(waveform: np.ndarray, osnr_dB: float, seed: int) -> np.ndarray:
    # 加性白高斯噪声：y = x + n，其中 n ~ N(0, sigma^2)。
    rng = np.random.default_rng(seed + 1000)
    snr_linear = 10.0 ** (osnr_dB / 10.0)
    signal_span = float(np.max(waveform) - np.min(waveform))
    # 这里用 OSNR 控制噪声强度，是一个简化的幅度噪声模型。
    noise_std = signal_span / np.sqrt(max(snr_linear, 1e-12))
    return waveform + rng.normal(0.0, noise_std, size=waveform.shape)


def sample_waveform(waveform: np.ndarray, samples_per_bit: int) -> np.ndarray:
    # 在每个 bit 的中心点采样，避免在跳变边沿附近判决。
    start = samples_per_bit // 2
    return waveform[start::samples_per_bit]
