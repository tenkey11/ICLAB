v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -495 -100 -495 -65 {lab=#net1}
N -495 -65 -390 -65 {lab=#net1}
N -390 -65 -390 -40 {lab=#net1}
N -495 -250 -495 -160 {lab=P}
N -495 -410 -495 -310 {lab=X}
N -285 -100 -285 -65 {lab=#net1}
N -390 -65 -285 -65 {lab=#net1}
N -285 -250 -285 -160 {lab=Q}
N -285 -410 -285 -310 {lab=Y}
N -455 -280 -390 -280 {lab=Y}
N -390 -280 -330 -355 {lab=Y}
N -330 -355 -285 -355 {lab=Y}
N -370 -280 -325 -280 {lab=X}
N -430 -350 -370 -280 {lab=X}
N -495 -350 -430 -350 {lab=X}
N -495 -390 -395 -390 {lab=X}
N -395 -390 -365 -435 {lab=X}
N -365 -435 -325 -435 {lab=X}
N -385 -390 -285 -390 {lab=Y}
N -415 -435 -385 -390 {lab=Y}
N -455 -435 -415 -435 {lab=Y}
N -515 -435 -490 -435 {lab=VDD}
N -515 -465 -515 -435 {lab=VDD}
N -515 -465 -495 -465 {lab=VDD}
N -290 -435 -265 -435 {lab=VDD}
N -265 -465 -265 -435 {lab=VDD}
N -285 -465 -265 -465 {lab=VDD}
N -285 -355 -255 -355 {lab=Y}
N -725 -435 -700 -435 {lab=VDD}
N -700 -465 -700 -435 {lab=VDD}
N -720 -465 -700 -465 {lab=VDD}
N -870 -435 -845 -435 {lab=VDD}
N -845 -465 -845 -435 {lab=VDD}
N -865 -465 -845 -465 {lab=VDD}
N -870 -200 -495 -200 {lab=P}
N -865 -405 -865 -200 {lab=P}
N -80 -435 -55 -435 {lab=VDD}
N -80 -465 -80 -435 {lab=VDD}
N -80 -465 -60 -465 {lab=VDD}
N 65 -435 90 -435 {lab=VDD}
N 65 -465 65 -435 {lab=VDD}
N 65 -465 85 -465 {lab=VDD}
N 85 -405 85 -200 {lab=Q}
N -255 -355 -60 -355 {lab=Y}
N -60 -405 -60 -355 {lab=Y}
N -720 -350 -495 -350 {lab=X}
N -720 -400 -720 -350 {lab=X}
N -720 -405 -720 -400 {lab=X}
N -285 -200 85 -200 {lab=Q}
N -445 -840 -445 -740 {lab=#net2}
N -450 -865 -425 -865 {lab=VDD}
N -425 -895 -425 -865 {lab=VDD}
N -445 -895 -425 -895 {lab=VDD}
N -445 -785 -415 -785 {lab=#net2}
N -520 -865 -485 -865 {lab=Y}
N -520 -865 -520 -710 {lab=Y}
N -520 -710 -480 -710 {lab=Y}
N -750 -850 -750 -750 {lab=#net3}
N -755 -875 -730 -875 {lab=VDD}
N -730 -905 -730 -875 {lab=VDD}
N -750 -905 -730 -905 {lab=VDD}
N -750 -795 -720 -795 {lab=#net3}
N -825 -875 -790 -875 {lab=X}
N -825 -875 -825 -720 {lab=X}
N -825 -720 -785 -720 {lab=X}
C {code_shown.sym} 450 -180 0 0 {name=s1 only_toplevel=false value="
.include /home/vicente/open_pdks/gf180mcu/gf180mcuD/libs.tech/ngspice/design.ngspice
.lib /home/vicente/open_pdks/gf180mcu/gf180mcuD/libs.tech/ngspice/sm141064.ngspice typical
.include /home/vicente/iclab/comparator/mm_models.spice
"}
C {vsource.sym} -1145 365 0 0 {name=VDD value="dc \{vdd\}" savecurrent=false}
C {gnd.sym} -1145 395 0 0 {name=l3 lab=0}
C {lab_pin.sym} -1145 335 0 0 {name=p3 sig_type=std_logic lab="VDD"}
C {code_shown.sym} 452.5 -25 0 0 {name=s2 only_toplevel=false value="
* transistor widths
.param w1=5u 	k1=1 		* differential pair and tail
.param w2=5u k2=2		* xc inv
.param w3=0.22u			* reset switches
.param w4=0.22u			* output inv

.param vdd=3.3
.param vcm=\{vdd/2\}
.param fclk=100e6
.param tper=\{1/fclk\}
.param tr=100p
.param tdly=\{tper/2\}
.param ncyc_ramp=150
.param vr=60m
.param tstop=\{ncyc_ramp*tper\}

.csparam tper=\{tper\}
.csparam tdly=\{tdly\}
.csparam tstop=\{tstop\}
.csparam vr=\{vr\}
.csparam vdd=\{vdd\}
.csparam ncyc_ramp=\{ncyc_ramp\}

.param sw_stat_mismatch=1
.options reltol=1e-6 abstol=1e-14 vntol=1e-9
"}
C {symbols/nfet_03v3.sym} -410 -10 0 0 {name=M1
L=0.28u
W=\{w1*k1\}
nf=1
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
C {symbols/nfet_03v3.sym} -515 -130 0 0 {name=M2
L=0.28u
W=\{w1\}
nf=1
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
C {symbols/nfet_03v3.sym} -475 -280 0 1 {name=M3
L=0.28u
W=\{w2\}
nf=1
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
C {symbols/pfet_03v3.sym} -475 -435 0 1 {name=M4
L=0.28u
W=\{w2*k2\}
nf=1
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
C {symbols/nfet_03v3.sym} -265 -130 0 1 {name=M5
L=0.28u
W=\{w1\}
nf=1
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
C {symbols/nfet_03v3.sym} -305 -280 0 0 {name=M6
L=0.28u
W=\{w2\}
nf=1
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
C {symbols/pfet_03v3.sym} -305 -435 0 0 {name=M7
L=0.28u
W=\{w2*k2\}
nf=1
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
C {vdd.sym} -495 -465 0 0 {name=l1 lab=VDD}
C {vdd.sym} -285 -465 0 0 {name=l4 lab=VDD}
C {gnd.sym} -495 -280 1 0 {name=l6 lab=0}
C {gnd.sym} -390 20 0 0 {name=l7 lab=0}
C {gnd.sym} -285 -130 1 0 {name=l8 lab=0}
C {gnd.sym} -495 -130 3 1 {name=l9 lab=0}
C {gnd.sym} -285 -280 3 1 {name=l10 lab=0}
C {gnd.sym} -390 -10 3 1 {name=l11 lab=0}
C {lab_pin.sym} -720 -350 0 0 {name=p2 sig_type=std_logic lab=X}
C {lab_pin.sym} -60 -355 0 1 {name=p4 sig_type=std_logic lab=Y}
C {lab_pin.sym} -865 -200 0 0 {name=p5 sig_type=std_logic lab=P}
C {lab_pin.sym} 85 -200 0 1 {name=p6 sig_type=std_logic lab=Q
}
C {symbols/pfet_03v3.sym} -740 -435 0 0 {name=M8
L=0.28u
W=\{w3\}
nf=1
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
C {vdd.sym} -720 -465 0 0 {name=l12 lab=VDD}
C {symbols/pfet_03v3.sym} -885 -435 0 0 {name=M9
L=0.28u
W=\{w3\}
nf=1
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
C {vdd.sym} -865 -465 0 0 {name=l13 lab=VDD}
C {symbols/pfet_03v3.sym} -40 -435 0 1 {name=M10
L=0.28u
W=\{w3\}
nf=1
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
C {vdd.sym} -60 -465 0 1 {name=l14 lab=VDD}
C {symbols/pfet_03v3.sym} 105 -435 0 1 {name=M11
L=0.28u
W=\{w3\}
nf=1
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
C {vdd.sym} 85 -465 0 1 {name=l15 lab=VDD}
C {lab_pin.sym} -535 -130 0 0 {name=p8 sig_type=std_logic lab=vip}
C {lab_pin.sym} -245 -130 0 1 {name=p9 sig_type=std_logic lab=vim
}
C {lab_pin.sym} -430 -10 0 0 {name=p10 sig_type=std_logic lab=CK}
C {lab_pin.sym} -905 -435 0 0 {name=p11 sig_type=std_logic lab=CK}
C {lab_pin.sym} -760 -435 0 0 {name=p12 sig_type=std_logic lab=CK}
C {lab_pin.sym} -20 -435 0 1 {name=p13 sig_type=std_logic lab=CK}
C {lab_pin.sym} 125 -435 0 1 {name=p14 sig_type=std_logic lab=CK}
C {vsource.sym} -975 375 0 0 {name=V1 value="PULSE(0 \{vdd\} \{tper/2\} \{tr\} \{tr\} \{tper/2-tr\} \{tper\})" savecurrent=false}
C {gnd.sym} -975 405 0 0 {name=l16 lab=0}
C {lab_pin.sym} -975 345 0 0 {name=p15 sig_type=std_logic lab="CK"}
C {vsource.sym} -1105 490 0 0 {name=Vcm value="dc \{vcm\}" savecurrent=false}
C {gnd.sym} -1105 520 0 0 {name=l2 lab=0}
C {lab_pin.sym} -1105 460 0 0 {name=p1 sig_type=std_logic lab="Vcm"}
C {vsource.sym} -975 500 0 0 {name=Vip value="dc 0" savecurrent=false}
C {lab_pin.sym} -975 470 1 0 {name=p7 sig_type=std_logic lab="vip"}
C {vsource.sym} -970 665 0 1 {name=Vim value="dc 0" savecurrent=false}
C {lab_pin.sym} -970 635 1 0 {name=p16 sig_type=std_logic lab="vim"}
C {lab_pin.sym} -975 530 3 0 {name=p17 sig_type=std_logic lab="Vcm"}
C {lab_pin.sym} -970 695 3 0 {name=p18 sig_type=std_logic lab="Vcm"}
C {symbols/nfet_03v3.sym} -465 -710 0 0 {name=M14
L=0.28u
W=\{w4\}
nf=1
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
C {symbols/pfet_03v3.sym} -465 -865 0 0 {name=M15
L=0.28u
W=\{w4*k2\}
nf=1
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
C {vdd.sym} -445 -895 0 0 {name=l19 lab=VDD}
C {gnd.sym} -445 -710 3 1 {name=l20 lab=0}
C {gnd.sym} -445 -680 0 0 {name=l21 lab=0}
C {lab_pin.sym} -520 -790 0 0 {name=p20 sig_type=std_logic lab=Y}
C {symbols/pfet_03v3.sym} -770 -875 0 0 {name=M12
L=0.28u
W=\{w4*k2\}
nf=1
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
C {vdd.sym} -750 -905 0 0 {name=l5 lab=VDD}
C {gnd.sym} -750 -720 3 1 {name=l17 lab=0}
C {gnd.sym} -750 -690 0 0 {name=l18 lab=0}
C {lab_pin.sym} -825 -800 0 0 {name=p19 sig_type=std_logic lab=X}
C {code_shown.sym} 1882.5 -40 0 0 {name=s3 only_toplevel=false value="
.control
set nruns = 200
set vrg = 0.06
set nbis = 10
set tev = 9.8e-9

foreach vc 800 900 1200 1300 1500 1650 1800
  shell rm -f vos_bis_vcm_$vc
  let vcv = $vc/1000

  repeat $nruns
    reset
    alter Vcm dc = $&vcv
    set lo = -$vrg
    set hi = $vrg

    repeat $nbis
      let midv = (($lo) + ($hi))/2
      set mid = $&midv
      let hp = ($mid)/2
      let hn = -($mid)/2
      alter Vip dc = $&hp
      alter Vim dc = $&hn

      tran 10p $tev

      let dfin = v(y)[length(v(y))-1] - v(x)[length(v(x))-1]
      if $&dfin > 0
        set hi = $mid
      else
        set lo = $mid
      end
      destroy all
    end

    let trip = (($lo) + ($hi))/2
    let oor = abs(trip)/$vrg
    echo $&trip $&oor >> vos_bis_vcm_$vc
    destroy all
  end
end
.endc
"}
C {symbols/nfet_03v3.sym} -770 -720 0 0 {name=M13
L=0.28u
W=\{w4\}
nf=1
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
