import argparse, glob, os, re, csv
import numpy as np
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("base", help="folder with l*/ subfolders (e.g. pelgrom) or a single l* folder")
ap.add_argument("-o", "--out", default="pelgrom")
a = ap.parse_args()

dirs = [d for d in sorted(glob.glob(os.path.join(a.base, "l*"))) if os.path.isdir(d)] or [a.base.rstrip("/")]
csv_rows = []
for dd in dirs:
    m = re.search(r"l([\d.]+)$", os.path.basename(dd.rstrip("/")))
    if not m: continue
    L = float(m.group(1))
    groups = {}                                   # nf -> list of (W, file)
    nfd = [d for d in glob.glob(os.path.join(dd, "nf*")) if os.path.isdir(d)]
    for d in (nfd or [dd]):
        mn = re.search(r"nf(\d+)$", d); nf = int(mn.group(1)) if mn else 1
        for f in glob.glob(os.path.join(d, "w*")):
            mw = re.search(r"w([\d.]+)$", f)
            if mw: groups.setdefault(nf, []).append((float(mw.group(1)), f))
    if not groups: print("no data in", dd); continue

    res = {}                                      # nf -> arrays
    print(f"\n=== L = {L} um ===")
    print(f"{'nf':>3} {'W':>6} {'AvtN':>6} {'AvtP':>6}")
    for nf, lst in sorted(groups.items()):
        rows = []
        for w, f in sorted(lst):
            d = np.loadtxt(f); d = d[np.isfinite(d).all(axis=1)]
            n = len(d); A = w * L                  # W is the total width
            sn, sp = d[:, 0].std(ddof=1), d[:, 2].std(ddof=1)
            s1n, s1p = d[:, 1].std(ddof=1), d[:, 3].std(ddof=1)
            rows.append((w, A, n, sn, sp, 1/np.sqrt(2*(n-1))))
            print(f"{nf:3d} {w:6.2f} {sn*np.sqrt(A)*1e3:6.2f} {sp*np.sqrt(A)*1e3:6.2f}")
            csv_rows.append([L, nf, w, n, sn*1e3, sn*np.sqrt(A)*1e3, sp*1e3, sp*np.sqrt(A)*1e3, sn/s1n, sp/s1p])
        res[nf] = np.array(rows).T

    allx = np.concatenate([1/np.sqrt(r[1]) for r in res.values()])
    def fit(i):
        x = allx; s = np.concatenate([r[i] for r in res.values()])
        e = np.concatenate([r[5] for r in res.values()]); wt = 1/(s*e)**2
        return (wt*x*s).sum()/(wt*x*x).sum()
    AvN, AvP = fit(3), fit(4)
    print(f"A_VT NMOS = {AvN*1e3:.2f} mV*um   A_VT PMOS = {AvP*1e3:.2f} mV*um")

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
    mk = {1: "o", 2: "s", 4: "^", 8: "D"}
    xx = np.linspace(0, allx.max()*1.05, 50)
    for i, Av, c, lab in ((3, AvN, "tab:blue", "NMOS"), (4, AvP, "tab:red", "PMOS")):
        for nf, r in res.items():
            W, A, n, s, e = r[0], r[1], r[2], r[i], r[5]
            ax[0].errorbar(1/np.sqrt(A), s*1e3, yerr=s*e*1e3, fmt=mk.get(nf, "o"), color=c, capsize=3, label=f"{lab} nf={nf}")
            ax[1].errorbar(W, s*np.sqrt(A)*1e3, yerr=s*np.sqrt(A)*e*1e3, fmt=mk.get(nf, "o")+"-", color=c, capsize=3, label=f"{lab} nf={nf}")
        ax[0].plot(xx, Av*xx*1e3, "--", color=c, label=f"{lab} fit: {Av*1e3:.2f} mV·µm")
        ax[1].axhline(Av*1e3, color=c, ls=":", lw=1)
    ax[0].set_xlabel("1/√(W·L)  [1/µm]"); ax[0].set_ylabel("σ(ΔVth) [mV]"); ax[0].set_title(f"Pelgrom plot (L = {L} µm)")
    ax[0].set_xlim(0); ax[0].set_ylim(0)
    ax[1].set_xscale("log"); ax[1].set_xlabel("W total [µm]"); ax[1].set_ylabel("σ(ΔVth)·√(W·L) [mV·µm]")
    ax[1].set_title("A_VT per width and fingers")
    for q in ax: q.grid(alpha=0.3); q.legend(fontsize=7)
    plt.tight_layout(); png = f"{a.out}_l{L:g}.png"; plt.savefig(png, dpi=150); plt.close(fig); print("saved", png)

if csv_rows:
    with open(f"{a.out}_stats.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["L_um","nf","W_um","N","sigma_N_mV","AVT_N_mVum","sigma_P_mV","AVT_P_mVum","ratio_N","ratio_P"])
        wr.writerows(csv_rows)
    print(f"saved {a.out}_stats.csv")