// sch_path: /home/vicente/iclab/comparator/comparator.sch
module comparator
(

);
wire VDD ;
wire CK ;
wire Vim ;
wire Vip ;
wire vg ;
wire vd1 ;
wire vd2 ;
wire 0 ;
wire P ;
wire Q ;
wire X ;
wire Y ;
wire net1 ;
wire net2 ;

vsource
#(
.value ( 1.5 ) ,
.savecurrent ( false )
)
vd1 ( 
 .p( vd1 ),
 .m( 0 )
);


vsource
#(
.value ( 1 ) ,
.savecurrent ( false )
)
V2 ( 
 .p( vg ),
 .m( 0 )
);


vsource
#(
.value ( 1.5 ) ,
.savecurrent ( false )
)
vd2 ( 
 .p( vd2 ),
 .m( 0 )
);


nfet_03v3
#(
.L ( 2.8e-07 ) ,
.W ( 2.2e-07 ) ,
.nf ( 1 ) ,
.m ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.18u ) ,
.nrs ( "'0.18u ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( nfet_03v3 ) ,
.spiceprefix ( X )
)
M1 ( 
 .D( net1 ),
 .G( CK ),
 .S( 0 ),
 .B( 0 )
);


nfet_03v3
#(
.L ( 2.8e-07 ) ,
.W ( 2.2e-07 ) ,
.nf ( 1 ) ,
.m ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.18u ) ,
.nrs ( "'0.18u ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( nfet_03v3 ) ,
.spiceprefix ( X )
)
M2 ( 
 .D( P ),
 .G( Vip ),
 .S( net1 ),
 .B( 0 )
);


nfet_03v3
#(
.L ( 2.8e-07 ) ,
.W ( 2.2e-07 ) ,
.nf ( 1 ) ,
.m ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.18u ) ,
.nrs ( "'0.18u ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( nfet_03v3 ) ,
.spiceprefix ( X )
)
M3 ( 
 .D( X ),
 .G( Y ),
 .S( P ),
 .B( 0 )
);


pfet_03v3
#(
.L ( 2.8e-07 ) ,
.W ( 2.2e-07 ) ,
.nf ( 1 ) ,
.m ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.18u ) ,
.nrs ( "'0.18u ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( pfet_03v3 ) ,
.spiceprefix ( X )
)
M4 ( 
 .D( X ),
 .G( Y ),
 .S( VDD ),
 .B( VDD )
);


nfet_03v3
#(
.L ( 2.8e-07 ) ,
.W ( 2.2e-07 ) ,
.nf ( 1 ) ,
.m ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.18u ) ,
.nrs ( "'0.18u ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( nfet_03v3 ) ,
.spiceprefix ( X )
)
M5 ( 
 .D( Q ),
 .G( Vim ),
 .S( net1 ),
 .B( 0 )
);


nfet_03v3
#(
.L ( 2.8e-07 ) ,
.W ( 2.2e-07 ) ,
.nf ( 1 ) ,
.m ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.18u ) ,
.nrs ( "'0.18u ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( nfet_03v3 ) ,
.spiceprefix ( X )
)
M6 ( 
 .D( Y ),
 .G( X ),
 .S( Q ),
 .B( 0 )
);


pfet_03v3
#(
.L ( 2.8e-07 ) ,
.W ( 2.2e-07 ) ,
.nf ( 1 ) ,
.m ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.18u ) ,
.nrs ( "'0.18u ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( pfet_03v3 ) ,
.spiceprefix ( X )
)
M7 ( 
 .D( Y ),
 .G( X ),
 .S( VDD ),
 .B( VDD )
);


pfet_03v3
#(
.L ( {l_sw} ) ,
.W ( {w_sw} ) ,
.nf ( 1 ) ,
.m ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.18u ) ,
.nrs ( "'0.18u ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( pfet_03v3 ) ,
.spiceprefix ( X )
)
M9 ( 
 .D( P ),
 .G( CK ),
 .S( VDD ),
 .B( VDD )
);


vsource
#(
.value ( "PULSE(0 ) ,
.savecurrent ( false )
)
V1 ( 
 .p( CK ),
 .m( 0 )
);


pfet_03v3
#(
.L ( {l_sw} ) ,
.W ( {w_sw} ) ,
.nf ( 1 ) ,
.m ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.18u ) ,
.nrs ( "'0.18u ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( pfet_03v3 ) ,
.spiceprefix ( X )
)
M8 ( 
 .D( X ),
 .G( CK ),
 .S( VDD ),
 .B( VDD )
);


pfet_03v3
#(
.L ( {l_sw} ) ,
.W ( {w_sw} ) ,
.nf ( 1 ) ,
.m ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.18u ) ,
.nrs ( "'0.18u ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( pfet_03v3 ) ,
.spiceprefix ( X )
)
M11 ( 
 .D( Q ),
 .G( CK ),
 .S( VDD ),
 .B( VDD )
);


pfet_03v3
#(
.L ( {l_sw} ) ,
.W ( {w_sw} ) ,
.nf ( 1 ) ,
.m ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.18u ) ,
.nrs ( "'0.18u ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( pfet_03v3 ) ,
.spiceprefix ( X )
)
M10 ( 
 .D( Y ),
 .G( CK ),
 .S( VDD ),
 .B( VDD )
);


vsource
#(
.value ( 1 ) ,
.savecurrent ( false )
)
V3 ( 
 .p( net2 ),
 .m( 0 )
);


vsource
#(
.value ( 1 ) ,
.savecurrent ( false )
)
V4 ( 
 .p( Vip ),
 .m( net2 )
);


vsource
#(
.value ( 1 ) ,
.savecurrent ( false )
)
V5 ( 
 .p( net2 ),
 .m( Vim )
);


.include /home/vicente/open_pdks/gf180mcu/gf180mcuD/libs.tech/ngspice/design.ngspice
.lib /home/vicente/open_pdks/gf180mcu/gf180mcuD/libs.tech/ngspice/sm141064.ngspice typical
.include /home/vicente/iclab/comparator/mm_models.spice


.control
.param vdd=3.3
.param fclk=100e6
.param tper={1/fclk}
.param tr=100p
.param w_pair=0.22u l_pair=0.28u
set rndseed=12345
set nruns=100

shell rm -f ~/iclab/comparator/results/mc_results.txt

repeat $nruns
  reset
  op
  print i(vd1) i(vd2) >> ~/iclab/comparator/results/mc_results.txt
end
.endc

endmodule
