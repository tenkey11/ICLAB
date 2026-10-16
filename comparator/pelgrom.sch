v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -247.5 -150 -247.5 -120 {lab=d1}
N -287.5 -140 -247.5 -140 {lab=d1}
N -287.5 -140 -287.5 -90 {lab=d1}
N -80 -147.5 -80 -117.5 {lab=d2}
N -120 -137.5 -80 -137.5 {lab=d2}
N -120 -137.5 -120 -87.5 {lab=d2}
N -287.5 97.5 -287.5 142.5 {lab=dp1}
N -287.5 142.5 -247.5 142.5 {lab=dp1}
N -247.5 127.5 -247.5 142.5 {lab=dp1}
N -250 97.5 -235 97.5 {lab=VDD}
N -235 67.5 -235 97.5 {lab=VDD}
N -247.5 67.5 -235 67.5 {lab=VDD}
N -125 95 -125 140 {lab=dp2}
N -125 140 -85 140 {lab=dp2}
N -85 125 -85 140 {lab=dp2}
N -87.5 95 -72.5 95 {lab=VDD}
N -72.5 65 -72.5 95 {lab=VDD}
N -85 65 -72.5 65 {lab=VDD}
C {symbols/nfet_03v3.sym} -267.5 -90 0 0 {name=M1
L=\{lnn\}
W=\{wn\}
nf=\{nfn\}
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {isource.sym} -247.5 -180 0 0 {name=I0 value=\{irefn\}}
C {vdd.sym} -247.5 -210 0 0 {name=l1 lab=VDD}
C {gnd.sym} -247.5 -60 0 0 {name=l2 lab=0}
C {gnd.sym} -247.5 -90 3 0 {name=l3 lab=0}
C {vsource.sym} -447.5 -127.5 0 0 {name=V1 value="dc \{Vdd\}" savecurrent=false}
C {gnd.sym} -447.5 -97.5 0 0 {name=l4 lab=0}
C {vdd.sym} -447.5 -157.5 0 0 {name=l5 lab=VDD}
C {symbols/nfet_03v3.sym} -100 -87.5 0 0 {name=M2
L=\{lnn\}
W=\{wn\}
nf=\{nfn\}
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {isource.sym} -80 -177.5 0 0 {name=I1 value=\{irefn\}}
C {vdd.sym} -80 -207.5 0 0 {name=l6 lab=VDD}
C {gnd.sym} -80 -57.5 0 0 {name=l7 lab=0}
C {gnd.sym} -80 -87.5 3 0 {name=l8 lab=0}
C {symbols/pfet_03v3.sym} -267.5 97.5 0 0 {name=M3
L=\{lpp\}
W=\{wp\}
nf=\{nfp\}
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {vdd.sym} -247.5 67.5 0 0 {name=l9 lab=VDD}
C {isource.sym} -247.5 172.5 0 0 {name=I2 value=\{irefp\}}
C {gnd.sym} -247.5 202.5 0 0 {name=l10 lab=0}
C {symbols/pfet_03v3.sym} -105 95 0 0 {name=M4
L=\{lpp\}
W=\{wp\}
nf=\{nfp\}
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {vdd.sym} -85 65 0 0 {name=l11 lab=VDD}
C {isource.sym} -85 170 0 0 {name=I3 value=\{irefp\}}
C {gnd.sym} -85 200 0 0 {name=l12 lab=0}
C {code_shown.sym} 235 -142.5 0 0 {name=s1 only_toplevel=false value="
.include /home/vicente/open_pdks/gf180mcu/gf180mcuD/libs.tech/ngspice/design.ngspice
.lib /home/vicente/open_pdks/gf180mcu/gf180mcuD/libs.tech/ngspice/sm141064.ngspice typical
.include /home/vicente/iclab/comparator/mm_models.spice
"}
C {code_shown.sym} 262.5 12.5 0 0 {name=s2 only_toplevel=false value="
.param Vdd=3.3
.param wn=0.22u lnn=0.28u nfn=1 irefn=0.5u
.param wp=0.22u lpp=0.28u nfp=1 irefp=0.5u


.param sw_stat_mismatch=1
.options reltol=1e-6 abstol=1e-14 vntol=1e-9
"}
C {code_shown.sym} 262.5 230 0 0 {name=s3 only_toplevel=false value="
.control
source /home/vicente/iclab/comparator/scripts/pelgrom/pelgrom_mc.cir
.endc
"}
C {lab_pin.sym} -287.5 -90 0 0 {name=p1 sig_type=std_logic lab="d1"}
C {lab_pin.sym} -120 -87.5 0 0 {name=p2 sig_type=std_logic lab="d2"}
C {lab_pin.sym} -287.5 97.5 0 0 {name=p3 sig_type=std_logic lab="dp1"}
C {lab_pin.sym} -125 95 0 0 {name=p4 sig_type=std_logic lab="dp2"}
