import numpy as np


def generate_bits(num_bits: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.integers(0, 2, size=num_bits, dtype=np.int8)


def raised_edge_nrz(bits: np.ndarray, samples_per_bit: int, extinction_ratio_dB: float):
    """Return a simple NRZ-OOK waveform with a mild finite-bandwidth edge shape."""
    er_linear = 10.0 ** (extinction_ratio_dB / 10.0)
    low_level = 1.0 / er_linear
    high_level = 1.0
    symbols = np.where(bits > 0, high_level, low_level)
    waveform = np.repeat(symbols, samples_per_bit).astype(float)

    # Small moving-average low-pass to make the eye diagram look more realistic.
    kernel_len = max(3, samples_per_bit // 4)
    kernel = np.ones(kernel_len) / kernel_len
    filtered = np.convolve(waveform, kernel, mode="same")
    return filtered, low_level, high_level


def add_awgn(waveform: np.ndarray, osnr_dB: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed + 1000)
    snr_linear = 10.0 ** (osnr_dB / 10.0)
    signal_span = float(np.max(waveform) - np.min(waveform))
    noise_std = signal_span / np.sqrt(max(snr_linear, 1e-12))
    return waveform + rng.normal(0.0, noise_std, size=waveform.shape)


def sample_waveform(waveform: np.ndarray, samples_per_bit: int) -> np.ndarray:
    start = samples_per_bit // 2
    return waveform[start::samples_per_bit]
