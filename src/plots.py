from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def plot_eye_diagram(waveform, samples_per_bit: int, output_path: Path, title: str):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # 眼图通常叠加 2 个 bit 周期，方便观察采样窗口和码间串扰。
    span = 2 * samples_per_bit
    usable = len(waveform) - span
    plt.figure(figsize=(8, 4.5))
    # 每隔 1 个 bit 取一段波形进行叠加，最多画 250 段，避免图像过密。
    for start in range(0, min(usable, 250 * samples_per_bit), samples_per_bit):
        segment = waveform[start : start + span]
        if len(segment) == span:
            # x 轴单位归一化为 bit period。
            x = np.arange(span) / samples_per_bit
            plt.plot(x, segment, color="#1f77b4", alpha=0.12, linewidth=0.8)
    plt.title(title)
    plt.xlabel("Time (bit periods)")
    plt.ylabel("Normalized received amplitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def plot_distance_sweep(df, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # 2x2 子图展示距离变化对链路关键指标的影响。
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))

    # 传输距离越长，接收功率通常越低。
    axes[0, 0].plot(df["distance_km"], df["rx_power_dBm"], marker="o")
    axes[0, 0].set_title("Received Power vs Distance")
    axes[0, 0].set_xlabel("Distance (km)")
    axes[0, 0].set_ylabel("Prx (dBm)")
    axes[0, 0].grid(True, alpha=0.3)

    # 链路余量为 0 是接收功率刚好等于接收机灵敏度的位置。
    axes[0, 1].plot(df["distance_km"], df["link_margin_dB"], marker="o", color="#2ca02c")
    axes[0, 1].axhline(0, color="black", linewidth=0.8, linestyle="--")
    axes[0, 1].set_title("Link Margin vs Distance")
    axes[0, 1].set_xlabel("Distance (km)")
    axes[0, 1].set_ylabel("Margin (dB)")
    axes[0, 1].grid(True, alpha=0.3)

    # OSNR 随信号功率下降而降低。
    axes[1, 0].plot(df["distance_km"], df["osnr_dB"], marker="o", color="#ff7f0e")
    axes[1, 0].set_title("OSNR Estimate vs Distance")
    axes[1, 0].set_xlabel("Distance (km)")
    axes[1, 0].set_ylabel("OSNR (dB / 0.1 nm)")
    axes[1, 0].grid(True, alpha=0.3)

    # BER 跨越多个数量级，因此使用 semilogy 对数坐标。
    axes[1, 1].semilogy(df["distance_km"], df["ber_estimate"], marker="o", color="#d62728")
    axes[1, 1].set_title("Estimated BER vs Distance")
    axes[1, 1].set_xlabel("Distance (km)")
    axes[1, 1].set_ylabel("BER")
    axes[1, 1].grid(True, which="both", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def plot_ber_q_curve(df, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7, 4.5))
    # Q 因子越大，BER 越低；同样使用对数纵轴显示 BER。
    plt.semilogy(df["q_factor"], df["ber_estimate"], marker="o")
    plt.title("BER-Q Curve")
    plt.xlabel("Q factor")
    plt.ylabel("Estimated BER")
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def show_result_images(image_paths):
    """Display generated result images in a 2x2 matplotlib window."""
    # 读取已经保存好的 4 张结果图，并在一个窗口中集中展示。
    titles = [
        "Distance Sweep",
        "Nominal Eye Diagram",
        "Low-OSNR Eye Diagram",
        "BER-Q Curve",
    ]
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    for ax, title, image_path in zip(axes.ravel(), titles, image_paths):
        img = mpimg.imread(image_path)
        ax.imshow(img)
        ax.set_title(title)
        ax.axis("off")
    plt.tight_layout()
    plt.show()
