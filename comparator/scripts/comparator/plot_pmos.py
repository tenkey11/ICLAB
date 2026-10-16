"""Offset sigma / delay vs PMOS xc ratio k (PMOS width = k * NMOS width), from the result folders.
Usage: python3 plot_pmos.py xcp_k11 xcp_k25 xcp_k50 xcp_k100 xcp_k150 xcp_k200 [-o out.png] [--wn 2.0]
Folder names end in k<hundredths>: xcp_k25 -> k = 0.25, xcp_k200 -> k = 2.
Each folder holds vos_bis_vcm_<mV> files with columns: trip oor tdel
--wn is the NMOS xc width in um, used only to print/label the PMOS width.
"""
import argparse, glob, os, re
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("folders", nargs="+")
ap.add_argument("-o", "--out", default="pmos_study.png")
ap.add_argument("--wn", type=float, default=2.0, help="NMOS xc width [um]")
ap.add_argument("--min-vcm", type=float, default=0.0)
a = ap.parse_args()

def kval(name):
    m = re.search(r"k(\d+)$", os.path.basename(name.rstrip("/")))
    if not m:
        raise SystemExit(f"cannot read k from folder name: {name} (expected ...k<hundredths>)")
    return int(m.group(1)) / 100

rows = []   # k, Vcm, N, fail, sigma, sig_err, mean, delay_mean, delay_sigma, n_edge
for folder in a.folders:
    k = kval(folder)
    files = glob.glob(os.path.join(folder, "vos_bis_vcm_*"))
    if not files:
        print(f"no vos_bis_vcm_* files in {folder}")
    for f in files:
        vcm = int(re.search(r"(\d+)$", f).group(1)) / 1000
        if vcm < a.min_vcm: continue
        d = np.loadtxt(f, ndmin=2)
        if d.shape[1] < 3:
            print(f"skip {f}: only {d.shape[1]} columns"); continue
        ok = (d[:, 2] > 0) & (d[:, 2] < 1e-6)
        n = len(d)
        vos = -d[:, 0] * 1e3
        sig = vos.std(ddof=1)
        rows.append((k, vcm, n, n - int(ok.sum()), sig, sig / np.sqrt(2 * (n - 1)), vos.mean(),
                     d[ok, 2].mean() * 1e12, d[ok, 2].std(ddof=1) * 1e12, int((d[:, 1] > 0.95).sum())))
if not rows: raise SystemExit("no usable data")
R = np.array(rows)

print(f"{'k':>6}{'Wp[um]':>8}{'Vcm':>6}{'N':>5}{'fail':>5}{'edge':>5}{'mean':>7}{'sigma':>8}{'+-':>6}{'delay':>9}{'d_sig':>7}")
for r in sorted(rows, key=lambda r: (r[1], r[0])):
    print(f"{r[0]:6.2f}{r[0]*a.wn:8.3f}{r[1]:6.2f}{int(r[2]):5d}{int(r[3]):5d}{int(r[9]):5d}"
          f"{r[6]:7.2f}{r[4]:8.2f}{r[5]:6.2f}{r[7]:9.1f}{r[8]:7.1f}")

def pareto(pts):
    keep = []
    for i, p in enumerate(pts):
        if not any(q[0] <= p[0] and q[1] <= p[1] and (q[0] < p[0] or q[1] < p[1])
                   for j, q in enumerate(pts) if j != i):
            keep.append(i)
    return keep

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 4.8))
for vcm in sorted(set(R[:, 1])):
    g = R[R[:, 1] == vcm]; g = g[np.argsort(g[:, 0])]
    lab = f"Vcm={vcm:g} V"
    ax1.errorbar(g[:, 0], g[:, 4], yerr=g[:, 5], marker="o", capsize=3, label=lab)
    ax2.errorbar(g[:, 0], g[:, 7], yerr=g[:, 8], marker="o", capsize=3, label=lab)
    ax3.errorbar(g[:, 7], g[:, 4], yerr=g[:, 5], marker="o", capsize=2, label=lab)
    for r in g:
        ax3.annotate(f"{r[0]:g}", (r[7], r[4]), fontsize=7, xytext=(3, 3), textcoords="offset points")
front = R[pareto(R[:, [7, 4]])]; front = front[np.argsort(front[:, 7])]
ax3.step(front[:, 7], front[:, 4], where="post", color="k", ls="--", lw=1.2, label="Pareto frontier")

for ax in (ax1, ax2):
    ax.set_xscale("log")
    sec = ax.secondary_xaxis("top", functions=(lambda x: x * a.wn, lambda x: x / a.wn))
    sec.set_xlabel(f"PMOS width [um] (NMOS = {a.wn:g} um)", fontsize=8)
ax1.set_xlabel("k = Wp / Wn"); ax1.set_ylabel("Offset sigma [mV]")
ax2.set_xlabel("k = Wp / Wn"); ax2.set_ylabel("Mean delay [ps] (+10 mV overdrive)")
ax3.set_xlabel("Mean delay [ps]"); ax3.set_ylabel("Offset sigma [mV]")
ax1.set_title("Offset vs PMOS ratio (error bars = sigma uncertainty)", fontsize=9, pad=28)
ax2.set_title("Delay vs PMOS ratio (error bars = delay spread)", fontsize=9, pad=28)
ax3.set_title("Trade-off (labels = k)", fontsize=9)
for ax in (ax1, ax2, ax3): ax.grid(alpha=0.3, which="both"); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(a.out, dpi=150); print("saved", a.out)
