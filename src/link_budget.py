from dataclasses import dataclass


@dataclass(frozen=True)
class LinkBudgetResult:
    # 用 dataclass 固定保存链路预算结果，方便后续打印、保存和画图。
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
    # 光纤损耗 = 光纤长度 * 单位长度损耗。
    fiber_loss = cfg["fiber_length_km"] * cfg["fiber_loss_dB_per_km"]
    # 连接器、熔接点损耗都按“数量 * 单个损耗”计算。
    connector_loss = cfg["num_connectors"] * cfg["connector_loss_dB"]
    splice_loss = cfg["num_splices"] * cfg["splice_loss_dB"]
    # 无源损耗包括光纤、连接器、熔接点、Mux/Demux 和其他预留损耗。
    passive_loss = (
        fiber_loss
        + connector_loss
        + splice_loss
        + cfg["mux_demux_loss_dB"]
        + cfg["other_loss_dB"]
    )
    amp_gain = cfg["amplifier_gain_dB"]
    # 放大器增益用于抵消一部分无源损耗，所以净损耗 = 无源损耗 - 放大器增益。
    total_loss_after_gain = passive_loss - amp_gain
    # 接收功率 = 发射功率 - 净损耗。
    rx_power = cfg["tx_power_dBm"] - total_loss_after_gain
    # 链路余量 = 接收功率 - 接收机灵敏度；余量为正说明功率预算满足要求。
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
