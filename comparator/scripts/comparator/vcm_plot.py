"""Mean and sigma of the StrongARM offset versus Vcm.

Usage: python3 vcm_plot.py vos_bis_vcm_* [-o out.png]
File names must end in the Vcm in millivolts (e.g. vos_bis_vcm_1650).
Column 1 = trip (V), column 2 = oor. Offset = -trip, as in hist.py.
"""
import argparse, re, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("files", nargs="+")
ap.add_argument("-o", "--out", default="vos_vs_vcm.png")
ap.add_argument("--oor", type=float, default=0.95,
                help="flag samples with oor above this (hit the search range edge)")
a = ap.parse_args()

rows = []
for f in a.files:
    m = re.search(r"(\d+)$", os.path.basename(f))
    if not m:
        print(f"skip {f}: name must end in Vcm in mV"); continue
    d = np.loadtxt(f, ndmin=2)
    vos = -d[:, 0] * 1e3                 # mV
    n = len(vos)
    mu = vos.mean()
    sd = vos.std(ddof=1) if n > 1 else 0.0
    nedge = int((d[:, 1] > a.oor).sum())
    rows.append((int(m.group(1)) / 1000, mu, sd, n, nedge))

rows.sort()
vcm, mu, sd, n, nedge = map(np.array, zip(*rows))
sd_err = sd / np.sqrt(2 * np.maximum(n - 1, 1))
mu_err = sd / np.sqrt(n)

print(f"{'Vcm[V]':>7} {'N':>5} {'mean[mV]':>9} {'sigma[mV]':>10} {'at edge':>8}")
for r in rows:
    print(f"{r[0]:7.3f} {r[3]:5d} {r[1]:9.2f} {r[2]:10.2f} {r[4]:8d}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
ax1.errorbar(vcm, mu, yerr=mu_err, marker="o", capsize=3)
ax1.set_ylabel("Mean offset [mV]")
ax1.axhline(0, color="gray", lw=0.8)
ax1.grid(alpha=0.3)
ax2.errorbar(vcm, sd, yerr=sd_err, marker="o", capsize=3, color="C1")
ax2.set_ylabel("Sigma of offset [mV]")
ax2.set_xlabel("Common-mode voltage Vcm [V]")
ax2.grid(alpha=0.3)

bad = nedge > 0
if bad.any():
    ax2.plot(vcm[bad], sd[bad], "rx", ms=10, label="samples at search-range edge")
    ax2.legend(fontsize=8)

fig.suptitle("StrongARM offset vs Vcm (Monte Carlo)")
fig.tight_layout()
fig.savefig(a.out, dpi=150)
print("saved", a.out)