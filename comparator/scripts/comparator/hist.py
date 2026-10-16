#!/usr/bin/env python3
"""Histogram of StrongARM offset from the bisection/ramp results file.

Usage: python3 hist.py results.txt [more_files.txt ...] [-o out.png] [-b BINS]
Column 1 of each file is 'trip' (Vin1-Vin2 at the flip); offset = -trip.
"""
import argparse
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")           # no display needed
import matplotlib.pyplot as plt


def load_offset_mv(path):
    data = np.loadtxt(path, ndmin=2)
    return -data[:, 0] * 1e3     # offset in mV


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("-b", "--bins", type=int, default=15)
    args = ap.parse_args()

    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    # common bin edges so overlaid histograms are comparable
    all_vos = [load_offset_mv(f) for f in args.files]
    lo = min(v.min() for v in all_vos)
    hi = max(v.max() for v in all_vos)
    pad = 0.05 * (hi - lo if hi > lo else 1.0)
    edges = np.linspace(lo - pad, hi + pad, args.bins + 1)
    x = np.linspace(edges[0], edges[-1], 400)

    for i, (f, vos) in enumerate(zip(args.files, all_vos)):
        n = len(vos)
        m = vos.mean()
        s = vos.std(ddof=1) if n > 1 else 0.0
        name = os.path.splitext(os.path.basename(f))[0]
        print(f"{name}: n={n}  mean={m:.3f} mV  sigma={s:.3f} mV  "
              f"(sigma err ~ {s / np.sqrt(2 * max(n - 1, 1)):.3f} mV)  "
              f"min={vos.min():.2f}  max={vos.max():.2f}")
        c = colors[i % len(colors)]
        ax.hist(vos, bins=edges, density=True, alpha=0.45 if len(args.files) > 1 else 0.8,
                color=c, edgecolor="white")
        if s > 0:
            pdf = np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))
            ax.plot(x, pdf, color=c, lw=2,
                    label=f"{name}: mean={m:.2f} mV, $\\sigma$={s:.2f} mV (N={n})")

    ax.set_xlabel("Input-referred offset [mV]")
    ax.set_ylabel("Probability density")
    ax.set_title("StrongARM offset, Monte Carlo")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()

    out = args.out or os.path.splitext(args.files[0])[0] + "_hist.png"
    fig.savefig(out, dpi=150)
    print("saved", out)


if __name__ == "__main__":
    sys.exit(main())