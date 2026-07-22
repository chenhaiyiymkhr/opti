from dataclasses import dataclass

from .units import db_to_linear, dBm_to_watts, linear_to_db


PLANCK = 6.62607015e-34
LIGHT_SPEED = 299792458.0


@dataclass(frozen=True)
class OsnrResult:
    signal_power_watts: float
    noise_power_watts: float
    osnr_linear: float
    osnr_dB: float
    reference_bandwidth_Hz: float
    model_note: str


def bandwidth_nm_to_hz(wavelength_nm: float, bandwidth_nm: float) -> float:
    wavelength_m = wavelength_nm * 1e-9
    bandwidth_m = bandwidth_nm * 1e-9
    return LIGHT_SPEED * bandwidth_m / (wavelength_m ** 2)


def estimate_osnr(rx_power_dBm: float, cfg: dict) -> OsnrResult:
    """Estimate OSNR in the configured optical reference bandwidth.

    This is a compact interview-level model, not a full multi-span EDFA model.
    If amplifier_gain_dB > 0, ASE is approximated by
    P_ASE ~= NF * h * nu * (G - 1) * B_ref.
    Otherwise a configured receiver-side optical noise floor is used.
    """
    signal_w = dBm_to_watts(rx_power_dBm)
    wavelength_m = cfg["wavelength_nm"] * 1e-9
    optical_freq = LIGHT_SPEED / wavelength_m
    ref_bw_hz = bandwidth_nm_to_hz(
        cfg["wavelength_nm"], cfg["reference_bandwidth_nm"]
    )

    gain_linear = db_to_linear(cfg["amplifier_gain_dB"])
    if cfg["amplifier_gain_dB"] > 0:
        nf_linear = db_to_linear(cfg["noise_figure_dB"])
        noise_w = nf_linear * PLANCK * optical_freq * (gain_linear - 1.0) * ref_bw_hz
        note = "EDFA ASE approximation"
    else:
        noise_w = dBm_to_watts(cfg["noise_floor_dBm_per_0_1nm"])
        note = "configured optical noise floor"

    osnr_linear = signal_w / noise_w if noise_w > 0 else float("inf")
    return OsnrResult(
        signal_power_watts=signal_w,
        noise_power_watts=noise_w,
        osnr_linear=osnr_linear,
        osnr_dB=linear_to_db(osnr_linear),
        reference_bandwidth_Hz=ref_bw_hz,
        model_note=note,
    )
