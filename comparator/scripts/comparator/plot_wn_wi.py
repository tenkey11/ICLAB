#!/usr/bin/env python3
"""Compare overdrives at fixed Wi and Vcm: offset, delay and trade-off vs NMOS xc width (wn).
One line per overdrive. One figure per (wi, vcm).
Layouts read:
  <base>/xcn_w<wn>/wi<wi>/ov<uV>/vos_bis_vcm_<mV>   (new, ov in uV)
  <base>/xcn_w<wn>/wi<wi>/vos_bis_vcm_<mV>          (old, taken as ov = 10000 uV)
  <base>/xcn_w<wn>/vos_bis_vcm_<mV>                 (older, wi = --legacy-wi, ov = 10000 uV)
File columns: trip[V]  oor  tdel[s]
usage: plot_wn_wi.py BASE [--wi 10] [--vcm 1650 2000] [--ov 100 1000 10000] [--out prefix]
Outputs: <out>_stats.csv, <out>_wi<Wi>_vcm<mV>.png
"""
import argparse, glob, os, re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("base")
ap.add_argument("--wi", type=float, nargs="+", default=[10.0], help="input pair widths [um], one figure each")
ap.add_argument("--vcm", type=int, nargs="+", default=[1650], help="Vcm values in mV, one figure each")
ap.add_argument("--ov", type=int, nargs="+", default=None, help="overdrives in uV to include (default: all found)")
ap.add_argument("--legacy-wi", type=float, default=5.0, help="Wi [um] of runs without a wi<..> folder")
ap.add_argument("--out", default="wn_ov")
ap.add_argument("--oor", type=float, default=0.98, help="out-of-range threshold")
args = ap.parse_args()


def num(s):
    return float(s.replace("_", ".").replace("p", "."))


def fmt_ov(uv):
    return f"{uv} uV" if uv < 1000 else f"{uv / 1000:g} mV"


files = []   # (path, wn, wi, vcm, ov_uV)
for f in glob.glob(os.path.join(args.base, "xcn_w*", "wi*", "ov*", "vos_bis_vcm_*")):
    p = f.split(os.sep)
    try:
        files.append((f, num(re.match(r"xcn_w(.+)", p[-4]).group(1)),
                      num(re.match(r"wi(.+)", p[-3]).group(1)),
                      int(p[-1].split("_")[-1]), int(p[-2][2:])))
    except (AttributeError, ValueError):
        pass
for f in glob.glob(os.path.join(args.base, "xcn_w*", "wi*", "vos_bis_vcm_*")):
    p = f.split(os.sep)
    try:
        files.append((f, num(re.match(r"xcn_w(.+)", p[-3]).group(1)),
                      num(re.match(r"wi(.+)", p[-2]).group(1)),
                      int(p[-1].split("_")[-1]), 10000))
    except (AttributeError, ValueError):
        pass
for f in glob.glob(os.path.join(args.base, "xcn_w*", "vos_bis_vcm_*")):
    p = f.split(os.sep)
    try:
        files.append((f, num(re.match(r"xcn_w(.+)", p[-2]).group(1)),
                      args.legacy_wi, int(p[-1].split("_")[-1]), 10000))
    except (AttributeError, ValueError):
        pass
if args.ov is not None:
    files = [t for t in files if t[4] in args.ov]

rows = []
for f, wn, wi, vcm, ov in files:
    d = np.loadtxt(f, ndmin=2)
    if d.shape[1] < 3:
        print("skip (need 3 columns):", f); continue
    trip, oor, tdel = d[:, 0], d[:, 1], d[:, 2]
    edge = oor >= args.oor              # offset outside the bisection range
    unres = tdel > 100e-9               # never resolved (sel = 1000 s)
    ok = ~edge & ~unres
    n = len(trip)
    if ok.sum() < 3:
        print("too few valid samples:", f); continue
    off = -trip[ok] * 1e3               # mV
    dl = tdel[ok] * 1e12                # ps
    sig = off.std(ddof=1)
    rows.append(dict(wn=wn, wi=wi, vcm=vcm, ov=ov, N=n, fail=int(unres.sum()),
                     edge=int(edge.sum()), mean=off.mean(), sig=sig,
                     err=sig / np.sqrt(2 * (ok.sum() - 1)),
                     dmean=dl.mean(), dsig=dl.std(ddof=1)))
if not rows:
    raise SystemExit("no data found under " + args.base)
rows.sort(key=lambda r: (r["wi"], r["vcm"], r["ov"], r["wn"]))

hdr = "wi_um,Vcm_mV,ov_uV,wn_um,N,fail,edge,vos_mean_mV,vos_sigma_mV,sigma_err_mV,delay_mean_ps,delay_sigma_ps"
lines = [hdr] + [f'{r["wi"]:g},{r["vcm"]},{r["ov"]},{r["wn"]:g},{r["N"]},{r["fail"]},{r["edge"]},'
                 f'{r["mean"]:.2f},{r["sig"]:.2f},{r["err"]:.2f},{r["dmean"]:.1f},{r["dsig"]:.1f}' for r in rows]
open(args.out + "_stats.csv", "w").write("\n".join(lines) + "\n")
print(f'{"wi":>5}{"Vcm":>6}{"ov":>9}{"wn":>6}{"N":>5}{"fail":>5}{"edge":>5}{"mean":>8}{"sigma":>8}{"±":>6}{"delay":>8}{"d_sig":>7}')
for r in rows:
    print(f'{r["wi"]:5g}{r["vcm"]:6d}{fmt_ov(r["ov"]):>9}{r["wn"]:6g}{r["N"]:5d}{r["fail"]:5d}{r["edge"]:5d}'
          f'{r["mean"]:8.2f}{r["sig"]:8.2f}{r["err"]:6.2f}{r["dmean"]:8.1f}{r["dsig"]:7.1f}')


def pareto(pts):
    """indices of non-dominated points; pts = (delay, sigma), both minimized"""
    keep = []
    for i, p in enumerate(pts):
        dominated = any(q[0] <= p[0] and q[1] <= p[1] and (q[0] < p[0] or q[1] < p[1])
                        for j, q in enumerate(pts) if j != i)
        if not dominated:
            keep.append(i)
    return keep


mk = "osD^vP*X"
# ---------- one figure per (Wi, Vcm): lines = overdrive ----------
for wi in args.wi:
    for vc in args.vcm:
        rv = [r for r in rows if r["wi"] == wi and r["vcm"] == vc]
        if not rv:
            print(f"no data at Wi = {wi:g} um, Vcm = {vc} mV"); continue
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 4.8))
        for i, ov in enumerate(sorted({r["ov"] for r in rv})):
            g = sorted([r for r in rv if r["ov"] == ov], key=lambda r: r["wn"])
            lab = f"overdrive = {fmt_ov(ov)}"
            W = [r["wn"] for r in g]
            sg = [r["sig"] for r in g]; er = [r["err"] for r in g]
            dm = [r["dmean"] for r in g]; ds = [r["dsig"] for r in g]
            ax1.errorbar(W, sg, yerr=er, marker=mk[i % len(mk)], capsize=3, label=lab)
            ax2.errorbar(W, dm, yerr=ds, marker=mk[i % len(mk)], capsize=3, label=lab)
            ax3.errorbar(dm, sg, yerr=er, marker=mk[i % len(mk)], capsize=2, label=lab)
            for r in g:
                ax3.annotate(f"{r['wn']:g}", (r["dmean"], r["sig"]),
                             fontsize=7, xytext=(3, 3), textcoords="offset points")

        fr = sorted((rv[i] for i in pareto([(r["dmean"], r["sig"]) for r in rv])), key=lambda r: r["dmean"])
        ax3.step([r["dmean"] for r in fr], [r["sig"] for r in fr], where="post",
                 color="k", ls="--", lw=1.2, label="Pareto frontier")
        print(f"\nWi = {wi:g} um, Vcm = {vc / 1000:g} V, Pareto-optimal designs:")
        print(f'{"ov":>9}{"Wn":>6}{"sigma_mV":>10}{"delay_ps":>10}')
        for r in fr:
            print(f'{fmt_ov(r["ov"]):>9}{r["wn"]:6g}{r["sig"]:10.2f}{r["dmean"]:10.1f}')

        ax1.set_xlabel("NMOS xc width [um]"); ax1.set_ylabel("Offset sigma [mV]")
        ax2.set_xlabel("NMOS xc width [um]"); ax2.set_ylabel("Mean delay [ps]")
        ax3.set_xlabel("Mean delay [ps]"); ax3.set_ylabel("Offset sigma [mV]")
        ax1.set_xscale("log"); ax2.set_xscale("log"); ax2.set_yscale("log"); ax3.set_xscale("log")
        ax1.set_title(f"Offset vs width, Wi={wi:g} um, Vcm={vc / 1000:g} V (error bars = sigma uncertainty)", fontsize=9)
        ax2.set_title("Delay vs width (error bars = delay spread)", fontsize=9)
        ax3.set_title("Trade-off (labels = Wn in um)", fontsize=9)
        for ax in (ax1, ax2, ax3):
            ax.grid(alpha=0.3, which="both"); ax.legend(fontsize=8)
        fig.tight_layout()
        fn = f"{args.out}_wi{wi:g}_vcm{vc}.png"
        fig.savefig(fn, dpi=150); plt.close(fig)
        print("saved", fn)