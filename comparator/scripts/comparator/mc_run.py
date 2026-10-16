#!/usr/bin/env python3
"""Run an xschem-generated netlist N times with ngspice and collect one printed value.
Usage: python3 mc_run.py NETLIST.spice -n 50 -s "i(vd2)"
"""
import argparse, re, subprocess, time, statistics, csv, pathlib

p = argparse.ArgumentParser()
p.add_argument("netlist")
p.add_argument("-n", type=int, default=50, help="number of runs")
p.add_argument("-s", default="i(vd2)", help="signal name as printed by ngspice")
p.add_argument("-o", default="../results/mc.csv", help="output csv")
p.add_argument("--delay", type=float, default=1.1, help="seconds between runs (reseeds RNG)")
a = p.parse_args()

pat = re.compile(re.escape(a.s) + r"\s*=\s*([-+0-9.eE]+)")
vals = []
for i in range(a.n):
    out = subprocess.run(["ngspice", "-b", a.netlist],
                         capture_output=True, text=True).stdout
    m = pat.search(out)
    if m:
        vals.append(float(m.group(1)))
        print(f"run {i+1}: {vals[-1]:.6g}")
    else:
        print(f"run {i+1}: signal not found")
    time.sleep(a.delay)

pathlib.Path(a.o).parent.mkdir(parents=True, exist_ok=True)
with open(a.o, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["run", a.s])
    for i, v in enumerate(vals, 1): w.writerow([i, v])

if len(vals) > 1:
    mu, sd = statistics.mean(vals), statistics.stdev(vals)
    print(f"\nN={len(vals)} mean={mu:.6g} sigma={sd:.6g} rel={100*sd/abs(mu):.2f}%")
