from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_eye_diagram(waveform, samples_per_bit: int, output_path: Path, title: str):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    span = 2 * samples_per_bit
    usable = len(waveform) - span
    plt.figure(figsize=(8, 4.5))
    for start in range(0, min(usable, 250 * samples_per_bit), samples_per_bit):
        segment = waveform[start : start + span]
        if len(segment) == span:
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
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))

    axes[0, 0].plot(df["distance_km"], df["rx_power_dBm"], marker="o")
    axes[0, 0].set_title("Received Power vs Distance")
    axes[0, 0].set_xlabel("Distance (km)")
    axes[0, 0].set_ylabel("Prx (dBm)")
    axes[0, 0].grid(True, alpha=0.3)

    axes[0, 1].plot(df["distance_km"], df["link_margin_dB"], marker="o", color="#2ca02c")
    axes[0, 1].axhline(0, color="black", linewidth=0.8, linestyle="--")
    axes[0, 1].set_title("Link Margin vs Distance")
    axes[0, 1].set_xlabel("Distance (km)")
    axes[0, 1].set_ylabel("Margin (dB)")
    axes[0, 1].grid(True, alpha=0.3)

    axes[1, 0].plot(df["distance_km"], df["osnr_dB"], marker="o", color="#ff7f0e")
    axes[1, 0].set_title("OSNR Estimate vs Distance")
    axes[1, 0].set_xlabel("Distance (km)")
    axes[1, 0].set_ylabel("OSNR (dB / 0.1 nm)")
    axes[1, 0].grid(True, alpha=0.3)

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
    plt.semilogy(df["q_factor"], df["ber_estimate"], marker="o")
    plt.title("BER-Q Curve")
    plt.xlabel("Q factor")
    plt.ylabel("Estimated BER")
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()
