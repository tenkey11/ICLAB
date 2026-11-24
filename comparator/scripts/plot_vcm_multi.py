#!/usr/bin/env python3
# Offset sigma and delay vs Vcm for any number of result folders (vos_bis_vcm_<mV> files).
# usage: python3 plot_vcm_multi.py DIR [DIR ...] [--labels L ...] [-o out.png] [--vcm 1000 1650 ...] [--min-vcm 1.0]
import argparse, glob, os, re
import numpy as np
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument('folders', nargs='+')
ap.add_argument('--labels', nargs='+')
ap.add_argument('-o', '--out', default='vcm_multi.png')
ap.add_argument('--vcm', nargs='+', type=int, help='only these Vcm values [mV]')
ap.add_argument('--min-vcm', type=float, default=None, help='only Vcm >= this [V]')
ap.add_argument('--edge', type=float, default=0.98, help='oor at/above this = bisection edge (excluded)')
ap.add_argument('--maxdel', type=float, default=100e-9, help='delay above this [s] = unresolved (excluded)')
ap.add_argument('--csv', help='also write the table to this CSV file')
args = ap.parse_args()
labels = args.labels or [os.path.basename(os.path.normpath(f)) for f in args.folders]
if len(labels) != len(args.folders):
    ap.error('need one label per folder')

def load(folder):
    res = []
    for fn in glob.glob(os.path.join(folder, 'vos_bis_vcm_*')):
        m = re.search(r'vos_bis_vcm_(\d+)$', fn)
        if not m or os.path.getsize(fn) == 0:
            continue
        vmv = int(m.group(1))
        if args.vcm and vmv not in args.vcm:
            continue
        if args.min_vcm is not None and vmv / 1e3 < args.min_vcm - 1e-9:
            continue
        rows = [l.split() for l in open(fn)]
        good = [r for r in rows if len(r) == 3]
        nmal = len(rows) - len(good)
        if not good:
            continue
        d = np.array(good, dtype=float)
        trip, oor, tdel = d[:, 0], d[:, 1], d[:, 2]
        med = np.median(trip)
        rs = 1.4826 * np.median(np.abs(trip - med))
        bad = np.abs(trip - med) > 5 * rs
        if nmal or bad.any():
            print('%s: skipped %d malformed line(s), dropped %d bad run(s)'
                  % (fn, nmal, int(bad.sum())))
        edge = oor >= args.edge
        fail = tdel > args.maxdel
        ok = ~edge & ~fail & ~bad
        t = trip[ok] * 1e3
        n = len(t)
        sig = np.std(t, ddof=1) if n > 1 else np.nan
        dl_all = tdel * 1e12
        dmed = np.median(dl_all[ok])
        drs = 1.4826 * np.median(np.abs(dl_all[ok] - dmed))
        dok = ok & (np.abs(dl_all - dmed) < 10 * drs)
        if (ok & ~dok).any():
            print('%s: %d delay outlier(s) excluded from delay stats' % (fn, int((ok & ~dok).sum())))
        dl = dl_all[dok]
        res.append(dict(vcm=vmv / 1e3, N=len(trip), fail=int(fail.sum()), edge=int(edge.sum()),
                        mean=np.mean(t) if n else np.nan, sig=sig,
                        err=sig / np.sqrt(2 * (n - 1)) if n > 1 else np.nan,
                        dly=np.nanmean(dl) if n else np.nan, dsig=np.nanstd(dl, ddof=1) if n > 1 else np.nan))
    return sorted(res, key=lambda r: r['vcm'])

data = []
for f, lab in zip(args.folders, labels):
    r = load(f)
    data.append((lab, r))
    print('\n== %s ==' % lab)
    if not r:
        print('  (no vos_bis_vcm_* files found in %s)' % f)
        continue
    print('  Vcm    N fail edge  mean[mV]  sigma[mV]     +-  delay[ps]   d_sig')
    for x in r:
        print('  %.2f %4d %4d %4d  %8.2f  %9.2f  %5.2f  %9.1f  %6.1f'
              % (x['vcm'], x['N'], x['fail'], x['edge'], x['mean'], x['sig'], x['err'], x['dly'], x['dsig']))

fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))
for lab, r in data:
    if not r:
        continue
    v = np.array([x['vcm'] for x in r]); s = np.array([x['sig'] for x in r])
    e = np.array([x['err'] for x in r]); dl = np.array([x['dly'] for x in r])
    ds = np.array([x['dsig'] for x in r])
    ax[0].errorbar(v, s, yerr=e, marker='o', ms=4, capsize=3, label=lab)
    ax[1].errorbar(v, dl, yerr=ds, marker='o', ms=4, capsize=3, label=lab)
    ax[2].plot(dl, s, marker='o', ms=4, label=lab)
ax[0].set_xlabel('$V_{cm}$ [V]'); ax[0].set_ylabel('offset $\\sigma$ [mV]'); ax[0].set_ylim(bottom=0)
ax[1].set_xlabel('$V_{cm}$ [V]'); ax[1].set_ylabel('delay [ps]')
ax[2].set_xlabel('delay [ps]'); ax[2].set_ylabel('offset $\\sigma$ [mV]'); ax[2].set_ylim(bottom=0)
ax[0].set_title('Offset vs common mode'); ax[1].set_title('Delay vs common mode'); ax[2].set_title('Offset vs delay')
for a in ax:
    a.grid(True, alpha=0.4); a.legend()
fig.tight_layout()
fig.savefig(args.out, dpi=150)
print('\nsaved', args.out)
plt.show()

if args.csv:
    with open(args.csv, 'w') as f:
        f.write('label,vcm_V,sigma_mV,sigma_err_mV,delay_ps,delay_sigma_ps\n')
        for lab, r in data:
            for x in r:
                f.write('%s,%.3f,%.4f,%.4f,%.2f,%.2f\n'
                        % (lab, x['vcm'], x['sig'], x['err'], x['dly'], x['dsig']))
    print('saved', args.csv)
