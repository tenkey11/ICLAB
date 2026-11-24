import argparse, glob, os, re
import numpy as np
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("folders", nargs=2, help="two result folders, e.g. sweep_vcm sweep_vcm_tail")
ap.add_argument("--labels", nargs=2, default=None)
ap.add_argument("-o", "--out", default="vcm_tail_compare.png")
ap.add_argument("--vcm", type=float, nargs="+", default=None, help="only these Vcm [V]")
ap.add_argument("--min-vcm", type=float, default=0.0)
ap.add_argument("--maxdel", type=float, default=100e-9, help="delays above this count as failures [s]")
ap.add_argument("--ov", default="+10 mV overdrive", help="text for the delay axis label")
a = ap.parse_args()

labels = a.labels or [os.path.basename(os.path.normpath(f)) for f in a.folders]
cols, marks = ["tab:blue", "tab:orange"], ["o", "s"]

def load(folder):
    out = []
    for f in glob.glob(os.path.join(folder, "vos_bis_vcm_*")):
        m = re.search(r"(\d+)$", f)
        if not m: continue
        vcm = int(m.group(1)) / 1000
        if vcm < a.min_vcm: continue
        if a.vcm is not None and not any(abs(vcm - v) < 1e-6 for v in a.vcm): continue
        d = np.loadtxt(f, ndmin=2)
        if d.size == 0: continue
        trip, oor = d[:, 0], d[:, 1]
        edge = oor >= 0.98
        ok = ~edge
        t = trip[ok]
        if len(t) < 3: continue
        sig = t.std(ddof=1)
        row = dict(vcm=vcm, n=len(d), edge=int(edge.sum()), mean=-t.mean(), sig=sig,
                   err=sig / np.sqrt(2 * (len(t) - 1)), fail=0, dmean=np.nan, dsig=np.nan, dsem=np.nan)
        if d.shape[1] >= 3:
            td = d[:, 2]
            good = ok & (td > 0) & (td < a.maxdel)
            row["fail"] = int((ok & ~good).sum())
            if good.sum() > 1:
                x = td[good] * 1e12
                row.update(dmean=x.mean(), dsig=x.std(ddof=1), dsem=x.std(ddof=1) / np.sqrt(len(x)))
        out.append(row)
    return sorted(out, key=lambda r: r["vcm"])

data = [load(f) for f in a.folders]
for lab, rows in zip(labels, data):
    print(f"\n== {lab} ==")
    print(f"{'Vcm':>5} {'N':>4} {'fail':>4} {'edge':>4} {'mean[mV]':>9} {'sigma[mV]':>10} {'+-':>6} {'delay[ps]':>10} {'d_sig':>7}")
    for r in rows:
        print(f"{r['vcm']:5.2f} {r['n']:4d} {r['fail']:4d} {r['edge']:4d} {r['mean']*1e3:9.2f} "
              f"{r['sig']*1e3:10.2f} {r['err']*1e3:6.2f} {r['dmean']:10.1f} {r['dsig']:7.1f}")
    if all(np.isnan(r["dmean"]) for r in rows):
        print("  (no delay column in this folder: delay panels will be empty for it)")

A = {r["vcm"]: r for r in data[0]}
B = {r["vcm"]: r for r in data[1]}
print(f"\n== {labels[1]} relative to {labels[0]} ==")
print(f"{'Vcm':>5} {'sigma ratio':>12} {'delay diff [ps]':>16}")
for v in sorted(set(A) & set(B)):
    print(f"{v:5.2f} {B[v]['sig']/A[v]['sig']:12.2f} {B[v]['dmean']-A[v]['dmean']:16.1f}")

def pareto(pts):                          # minimise both (sigma, delay)
    keep = []
    for i, (s, d) in enumerate(pts):
        dom = any((s2 <= s and d2 <= d) and (s2 < s or d2 < d) for j, (s2, d2) in enumerate(pts) if j != i)
        if not dom: keep.append(i)
    return keep

fig, ax = plt.subplots(1, 3, figsize=(17, 4.8))
allpts = []
for k, (lab, rows) in enumerate(zip(labels, data)):
    v = np.array([r["vcm"] for r in rows])
    s = np.array([r["sig"] for r in rows]) * 1e3
    e = np.array([r["err"] for r in rows]) * 1e3
    dm = np.array([r["dmean"] for r in rows])
    ds = np.array([r["dsem"] for r in rows])
    ax[0].errorbar(v, s, yerr=e, fmt=marks[k] + "-", color=cols[k], capsize=3, label=lab)
    ax[1].errorbar(v, dm, yerr=ds, fmt=marks[k] + "-", color=cols[k], capsize=3, label=lab)
    good = ~np.isnan(dm)
    ax[2].scatter(s[good], dm[good], marker=marks[k], color=cols[k], label=lab, zorder=3)
    for x, y, vv in zip(s[good], dm[good], v[good]):
        ax[2].annotate(f"{vv:g}", (x, y), textcoords="offset points", xytext=(4, 4), fontsize=7, color=cols[k])
    pts = list(zip(s[good], dm[good]))
    fr = sorted(pareto(pts), key=lambda i: pts[i][0])
    if fr:
        ax[2].step([pts[i][0] for i in fr], [pts[i][1] for i in fr], where="post", color=cols[k], alpha=0.5)
    allpts += [(x, y, lab, vv) for (x, y), vv in zip(pts, v[good])]

if allpts:
    fr = pareto([(p[0], p[1]) for p in allpts])
    print("\nCombined Pareto points (sigma [mV], delay [ps]):")
    for i in sorted(fr, key=lambda i: allpts[i][0]):
        print(f"  {allpts[i][2]:>20}  Vcm={allpts[i][3]:.2f}  sigma={allpts[i][0]:.2f}  delay={allpts[i][1]:.1f}")

ax[0].set_xlabel("Vcm [V]"); ax[0].set_ylabel("σ offset [mV]"); ax[0].set_title("Offset")
ax[1].set_xlabel("Vcm [V]"); ax[1].set_ylabel(f"Mean delay [ps] ({a.ov})"); ax[1].set_title("Delay")
ax[2].set_xlabel("σ offset [mV]"); ax[2].set_ylabel("Mean delay [ps]"); ax[2].set_title("Trade-off (lower left is better)")
for q in ax:
    q.grid(alpha=0.3); q.legend()
plt.tight_layout(); plt.savefig(a.out, dpi=150)
print("saved", a.out)