#!/usr/bin/env python3
"""Offset sigma and delay vs NMOS xc width (one line per Vcm) + trade-off with Pareto frontier.
Usage: python3 plot_width.py speed_stats.csv [-o out.png] [--min-vcm 0]
Folder names like xcn_w0_5, xcn_w0p5, xcn_w5 are read as widths in um.
"""
import argparse, re
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("csv")
ap.add_argument("-o", "--out", default="width_study.png")
ap.add_argument("--min-vcm", type=float, default=0.0, help="drop Vcm below this (e.g. 1.0 to hide 0.8 V)")
a = ap.parse_args()

df = pd.read_csv(a.csv)
df = df[df["Vcm_V"] >= a.min_vcm].copy()

def width(name):
    if isinstance(name, (int, float, np.integer, np.floating)):
        return float(name)
    s = str(name)
    m = re.search(r"w(\d+(?:[_p.]\d+)?)$", s)
    if m:
        return float(m.group(1).replace("_", ".").replace("p", "."))
    m = re.search(r"(\d+(?:[_p.]\d+)?)$", s)
    if m:
        return float(m.group(1).replace("_", ".").replace("p", "."))
    raise ValueError(f"cannot read a width from folder name: {s!r}")

df["W"] = df["folder"].map(width)
df["sig_err"] = df["vos_sigma_mV"] / np.sqrt(2 * (df["N"] - 1))

def pareto(pts):
    """indices of non-dominated points; pts = (delay, sigma), both minimized"""
    keep = []
    for i, p in enumerate(pts):
        dominated = any(q[0] <= p[0] and q[1] <= p[1] and (q[0] < p[0] or q[1] < p[1])
                        for j, q in enumerate(pts) if j != i)
        if not dominated:
            keep.append(i)
    return keep

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 4.8))

for vcm, g in df.groupby("Vcm_V"):
    g = g.sort_values("W")
    lab = f"Vcm={vcm:g} V"
    ax1.errorbar(g["W"], g["vos_sigma_mV"], yerr=g["sig_err"], marker="o", capsize=3, label=lab)
    ax2.errorbar(g["W"], g["delay_mean_ps"], yerr=g["delay_sigma_ps"], marker="o", capsize=3, label=lab)
    ax3.errorbar(g["delay_mean_ps"], g["vos_sigma_mV"], yerr=g["sig_err"],
                 marker="o", capsize=2, label=lab)
    for _, r in g.iterrows():
        ax3.annotate(f"{r['W']:g}", (r["delay_mean_ps"], r["vos_sigma_mV"]),
                     fontsize=7, xytext=(3, 3), textcoords="offset points")

# Pareto frontier over all plotted designs
pts = df[["delay_mean_ps", "vos_sigma_mV"]].values
idx = pareto(pts)
front = df.iloc[idx].sort_values("delay_mean_ps")
ax3.step(front["delay_mean_ps"], front["vos_sigma_mV"], where="post",
         color="k", ls="--", lw=1.2, label="Pareto frontier")
print("Pareto-optimal designs:")
print(front[["folder", "Vcm_V", "vos_sigma_mV", "delay_mean_ps"]].to_string(index=False))

ax1.set_xlabel("NMOS xc width [um]"); ax1.set_ylabel("Offset sigma [mV]")
ax2.set_xlabel("NMOS xc width [um]"); ax2.set_ylabel("Mean delay [ps] (+10 mV overdrive)")
ax3.set_xlabel("Mean delay [ps]"); ax3.set_ylabel("Offset sigma [mV]")
ax1.set_xscale("log"); ax2.set_xscale("log"); ax2.set_yscale("log"); ax3.set_xscale("log")
ax1.set_title("Offset vs width (error bars = sigma uncertainty)", fontsize=9)
ax2.set_title("Delay vs width (error bars = delay spread)", fontsize=9)
ax3.set_title("Trade-off (labels = width in um)", fontsize=9)
for ax in (ax1, ax2, ax3):
    ax.grid(alpha=0.3, which="both"); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(a.out, dpi=150)
print("saved", a.out)
