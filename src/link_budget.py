from dataclasses import dataclass


@dataclass(frozen=True)
class LinkBudgetResult:
    fiber_loss_dB: float
    connector_loss_total_dB: float
    splice_loss_total_dB: float
    passive_loss_dB: float
    amplifier_gain_dB: float
    total_loss_after_gain_dB: float
    rx_power_dBm: float
    receiver_sensitivity_dBm: float
    link_margin_dB: float


def calculate_link_budget(cfg: dict) -> LinkBudgetResult:
    fiber_loss = cfg["fiber_length_km"] * cfg["fiber_loss_dB_per_km"]
    connector_loss = cfg["num_connectors"] * cfg["connector_loss_dB"]
    splice_loss = cfg["num_splices"] * cfg["splice_loss_dB"]
    passive_loss = (
        fiber_loss
        + connector_loss
        + splice_loss
        + cfg["mux_demux_loss_dB"]
        + cfg["other_loss_dB"]
    )
    amp_gain = cfg["amplifier_gain_dB"]
    total_loss_after_gain = passive_loss - amp_gain
    rx_power = cfg["tx_power_dBm"] - total_loss_after_gain
    margin = rx_power - cfg["receiver_sensitivity_dBm"]
    return LinkBudgetResult(
        fiber_loss_dB=fiber_loss,
        connector_loss_total_dB=connector_loss,
        splice_loss_total_dB=splice_loss,
        passive_loss_dB=passive_loss,
        amplifier_gain_dB=amp_gain,
        total_loss_after_gain_dB=total_loss_after_gain,
        rx_power_dBm=rx_power,
        receiver_sensitivity_dBm=cfg["receiver_sensitivity_dBm"],
        link_margin_dB=margin,
    )
