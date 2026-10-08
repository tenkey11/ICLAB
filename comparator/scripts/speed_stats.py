import argparse, glob, os, re, csv
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("folders", nargs="+")
ap.add_argument("-o", "--out", default="speed_stats.csv")
a = ap.parse_args()

def stats(x):
    return (x.mean(), x.std(ddof=1)) if len(x) > 1 else (np.nan, np.nan)

rows = []
for folder in a.folders:
    for f in sorted(glob.glob(os.path.join(folder, "vos_bis_vcm_*"))):
        vcm = int(re.search(r"(\d+)$", f).group(1)) / 1000
        d = np.loadtxt(f, ndmin=2)
        if d.shape[1] < 3:
            continue
        n = len(d)
        ok = (d[:, 2] > 0) & (d[:, 2] < 1e-6)          # drop "no crossing"
        os_m, os_s = stats(-d[:, 0] * 1e3)             # offset, mV
        td_m, td_s = stats(d[ok, 2] * 1e12)            # delay, ps
        td_med = np.median(d[ok, 2]) * 1e12 if ok.any() else np.nan
        tau_m = tau_s = np.nan
        if d.shape[1] >= 4:
            okt = ok & (d[:, 3] > 0) & (d[:, 3] < 1e-6)
            tau_m, tau_s = stats(d[okt, 3] * 1e12)
        rows.append([os.path.basename(folder), vcm, n, n - int(ok.sum()),
                     os_m, os_s, td_m, td_s, td_med, tau_m, tau_s])

hdr = ["folder", "Vcm_V", "N", "fail", "vos_mean_mV", "vos_sigma_mV",
       "delay_mean_ps", "delay_sigma_ps"]
print(f"{'folder':<12}{'Vcm':>6}{'N':>5}{'fail':>5}{'vos_s':>8}{'td_mean':>9}{'td_sig':>8}")
for r in rows:
    print(f"{r[0]:<12}{r[1]:6.2f}{r[2]:5d}{r[3]:5d}{r[5]:8.2f}{r[6]:9.1f}{r[7]:8.1f}")
with open(a.out, "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(hdr); w.writerows(rows)
print("saved", a.out)