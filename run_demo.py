import argparse
import json
from dataclasses import asdict
from pathlib import Path

import pandas as pd

from src.link_budget import calculate_link_budget
from src.metrics import calculate_q_ber
from src.ook_sim import add_awgn, generate_bits, raised_edge_nrz, sample_waveform
from src.osnr import estimate_osnr
from src.plots import plot_ber_q_curve, plot_distance_sweep, plot_eye_diagram


ROOT = Path(__file__).resolve().parent


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def run_single_case(cfg: dict, results_dir: Path):
    link = calculate_link_budget(cfg)
    osnr = estimate_osnr(link.rx_power_dBm, cfg)
    bits = generate_bits(cfg["num_bits"], cfg["seed"])
    clean_wave, _, _ = raised_edge_nrz(
        bits, cfg["samples_per_bit"], cfg["extinction_ratio_dB"]
    )
    noisy_wave = add_awgn(clean_wave, osnr.osnr_dB, cfg["seed"])
    samples = sample_waveform(noisy_wave, cfg["samples_per_bit"])
    metrics = calculate_q_ber(bits, samples)

    # Also generate an intentionally noisy eye diagram for visual comparison.
    low_osnr_wave = add_awgn(clean_wave, max(osnr.osnr_dB - 12.0, 1.0), cfg["seed"] + 1)

    plot_eye_diagram(
        noisy_wave,
        cfg["samples_per_bit"],
        results_dir / "eye_diagram_nominal.png",
        f"Nominal Eye Diagram, OSNR={osnr.osnr_dB:.1f} dB",
    )
    plot_eye_diagram(
        low_osnr_wave,
        cfg["samples_per_bit"],
        results_dir / "eye_diagram_low_osnr.png",
        f"Low-OSNR Eye Diagram, OSNR={max(osnr.osnr_dB - 12.0, 1.0):.1f} dB",
    )

    summary = {
        "link_budget": asdict(link),
        "osnr": asdict(osnr),
        "q_ber": asdict(metrics),
    }
    with (results_dir / "single_case_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return link, osnr, metrics


def run_distance_sweep(cfg: dict, results_dir: Path):
    sweep = cfg["distance_sweep_km"]
    distances = list(range(int(sweep["start"]), int(sweep["stop"]) + 1, int(sweep["step"])))
    rows = []
    for i, distance in enumerate(distances):
        case = dict(cfg)
        case["fiber_length_km"] = float(distance)
        case["seed"] = int(cfg["seed"]) + i
        link = calculate_link_budget(case)
        osnr = estimate_osnr(link.rx_power_dBm, case)
        bits = generate_bits(case["num_bits"], case["seed"])
        clean_wave, _, _ = raised_edge_nrz(
            bits, case["samples_per_bit"], case["extinction_ratio_dB"]
        )
        noisy_wave = add_awgn(clean_wave, osnr.osnr_dB, case["seed"])
        samples = sample_waveform(noisy_wave, case["samples_per_bit"])
        metrics = calculate_q_ber(bits, samples)
        rows.append(
            {
                "distance_km": distance,
                "rx_power_dBm": link.rx_power_dBm,
                "link_margin_dB": link.link_margin_dB,
                "osnr_dB": osnr.osnr_dB,
                "q_factor": metrics.q_factor,
                "ber_estimate": metrics.ber_estimate,
                "ber_counted": metrics.ber_counted,
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv(results_dir / "distance_sweep.csv", index=False)
    plot_distance_sweep(df, results_dir / "distance_sweep.png")
    plot_ber_q_curve(df, results_dir / "ber_q_curve.png")
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default=str(ROOT / "configs" / "default.json"),
        help="Path to JSON config.",
    )
    parser.add_argument(
        "--results-dir",
        default=str(ROOT / "results"),
        help="Directory for generated tables and figures.",
    )
    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    link, osnr, metrics = run_single_case(cfg, results_dir)
    df = run_distance_sweep(cfg, results_dir)

    print("Single-case result")
    print(f"  Rx power: {link.rx_power_dBm:.2f} dBm")
    print(f"  Link margin: {link.link_margin_dB:.2f} dB")
    print(f"  OSNR: {osnr.osnr_dB:.2f} dB / 0.1 nm ({osnr.model_note})")
    print(f"  Q factor: {metrics.q_factor:.2f}")
    print(f"  BER estimate: {metrics.ber_estimate:.3e}")
    print()
    print(f"Generated {len(df)} sweep points in {results_dir}")


if __name__ == "__main__":
    main()
