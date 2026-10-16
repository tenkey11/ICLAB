#!/usr/bin/env bash
NET=$HOME/iclab/comparator/netlists/comparator.spice
TPL=$HOME/iclab/comparator/scripts/controls/sweep_vcm_xcwn.cir
JOBS=$HOME/iclab/comparator/jobs
mkdir -p $JOBS && rm -f $JOBS/*

for wi in 5 10; do
  for wn in 0.5 1 2 5 10; do
    for vc in 800 1200 1650 2000 2250; do
      tag=wi${wi}_wn${wn//./p}_vc${vc}
      sed -e "s/@WI@/$wi/" -e "s/@WN@/$wn/" -e "s/@VC@/$vc/" $TPL > $JOBS/$tag.cir
      sed "s|^ *source .*|source $JOBS/$tag.cir|" $NET > $JOBS/$tag.spice
      echo $tag
    done
  done
done | xargs -P $(nproc) -I{} sh -c "ngspice -b $JOBS/{}.spice > $JOBS/{}.log 2>&1"