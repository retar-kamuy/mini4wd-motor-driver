from pathlib import Path
import json,shutil,subprocess,re,itertools,hashlib
r=Path(__file__).resolve().parents[4];out=r/'specs/003-resolve-pcb-drc/verification/switching-validation';out.mkdir(exist_ok=True)
vendor=r/'.cache/sol-sequence/vendor'
if not (out/'UCC27524.lib').exists():
 shutil.copy2(vendor/'ucc27524/UCC27524_PSPICE_TRANS/UCC27524.LIB',out/'UCC27524.lib')
if not (out/'SiSS64DN.lib').exists():
 shutil.copy2(vendor/'siss64dn/SiSS64DN_PS_Rev_B.LIB',out/'SiSS64DN.lib')
shutil.copy2(r/'specs/003-resolve-pcb-drc/verification/q2-low-voltage/DMP2008UFG-ngspice.lib',out/'DMP2008UFG.lib')

def run(name,vb,rg,lg,scenario,temp=27,driver_lib='UCC27524.lib',rgp=None,extra_n_gate_C=0):
 name='stable-'+name
 rgp=rg if rgp is None else rgp
 if scenario=='pwm':
  rails=f'Vbat batt 0 {vb}\nVdd dd 0 5.208\nVlogic logic 0 3.3\nVena ena 0 3.3\nVa a 0 PWL(0 0 29.314u 0 29.315u 3.3 60u 3.3 60.001u 0)\nVb b 0 PWL(0 0 20u 0 20.001u 3.3 69.314u 3.3 69.315u 0)'
 elif scenario=='vdd_loss':
  rails=f'Vbat batt 0 {vb}\nVdd dd 0 PWL(0 5.208 60u 5.208 60.02u 0)\nVlogic logic 0 3.3\nVena ena 0 3.3\nVa a 0 3.3\nVb b 0 3.3'
 elif scenario=='mcu_loss':
  rails=f'Vbat batt 0 {vb}\nVdd dd 0 5.208\nVlogic logic 0 PWL(0 3.3 60u 3.3 60.02u 0)\nVena ena 0 PWL(0 3.3 59.98u 3.3 60u 0)\nVa a 0 PWL(0 3.3 60u 3.3 60.02u 0)\nVb b 0 PWL(0 3.3 60u 3.3 60.02u 0)'
 elif scenario=='startup':
  rails=f'Vbat batt 0 PWL(0 0 20n {vb})\nVdd dd 0 PWL(0 0 10u 0 30u 5.208)\nVlogic logic 0 PWL(0 0 35u 0 55u 3.3)\nVena ena 0 PWL(0 0 70u 0 70.02u 3.3)\nVa a 0 3.3\nVb b 0 3.3'
 elif scenario=='battery_open':
  rails=f'Vcell raw 0 {vb}\nRcell raw supply .1\nVdisconnect ctl 0 PWL(0 1 60u 1 60.02u 0)\nScut supply batt ctl 0 cut\n.model cut SW(Ron=.01 Roff=1e12 Vt=.5 Vh=.05)\nCinput batt 0 10u\nVdd dd 0 PWL(0 5.208 80u 5.208 100u 0)\nVlogic logic 0 PWL(0 3.3 80u 3.3 90u 0)\nVena ena 0 PWL(0 3.3 80u 3.3 80.02u 0)\nVa a 0 3.3\nVb b 0 3.3'
 elif scenario=='battery_loss':
  rails=f'Vbat batt 0 PWL(0 {vb} 60u {vb} 60.02u 0)\nVdd dd 0 PWL(0 5.208 80u 5.208 100u 0)\nVlogic logic 0 PWL(0 3.3 80u 3.3 90u 0)\nVena ena 0 PWL(0 3.3 80u 3.3 80.02u 0)\nVa a 0 3.3\nVb b 0 3.3'
 bench=f'''Q1 Q2 UCC27524 switching validation: {name}
.include {driver_lib}
.include SiSS64DN.lib
.include DMP2008UFG-stable.lib
{rails}
Xdrv a b oa ob dd ena logic 0 UCC27524
Rgn oa lgn {max(.001,rg)}
Rgp ob lgp {max(.001,rgp)}
Lgn lgn gn {lg}
Lgp lgp gp {lg}
Lsn sn snx 5n
Rsn snx 0 .001
Lsp sp spx 5n
Rsp spx batt .001
Vqn m dn 0
Vqp m dp 0
Xn dn gn sn SiSS64DN
CextraN gn sn {max(1e-18,extra_n_gate_C)}
Xp dp gp sp DMP2008UFG
Rmotor batt wind .5
Lmotor wind m 10u
Dfly m batt Dfree
.model Dfree D(Is=1e-8 N=1 Rs=.01 BV=40 Cjo=500p Tt=3n)
BvgN vgn 0 V=V(gn,sn)
BvgP vgp 0 V=V(gp,sp)
BvdN vdn 0 V=V(dn,sn)
BvdP vdp 0 V=V(dp,sp)
.temp {temp}
.options method=gear reltol=.005 abstol=1e-8 chgtol=1e-14 trtol=7
.tran 2n 110u 0 2n
.measure tran vgn_max MAX V(vgn)
.measure tran vgn_min MIN V(vgn)
.measure tran vgp_max MAX V(vgp)
.measure tran vgp_min MIN V(vgp)
.measure tran vdn_max MAX V(vdn)
.measure tran vdn_min MIN V(vdn)
.measure tran vdp_max MAX V(vdp)
.measure tran vdp_min MIN V(vdp)
.control
run
set wr_singlescale
set wr_vecnames
wrdata {name}.dat v(vgn) v(vgp) v(vdn) v(vdp) i(vqn) i(vqp)
quit
.endc
.end
'''
 p=out/(name+'.cir');p.write_text(bench);log=out/(name+'.log')
 try:
  q=subprocess.run(['ngspice','-n','-D','ngbehavior=ps','-b','-o',str(log),str(p)],cwd=out,capture_output=True,text=True,timeout=30)
  s=log.read_text();vals={k:float(v) for k,v in re.findall(r'^([a-zA-Z_]+)\s*=\s*([-+\deE.]+)',s,re.M)}
  result={'case':name,'scenario':scenario,'vbat_V':vb,'fixed_model_temperature_C':temp,'UCC_model_file':driver_lib,'external_gate_R_ohm':rg,'external_Q2_gate_R_ohm':rgp,'extra_Q1_gate_C_F':extra_n_gate_C,'assumed_gate_L_H':lg,'returncode':q.returncode,'measurements':vals,'completed':q.returncode==0 and len(vals)==8 and not any(t in s for t in ['Timestep too small','run simulation(s) aborted']),'warnings':[x.strip() for x in s.splitlines() if any(y in x.lower() for y in ['warning','unrecognized','error:','timestep too small'])]}
 except subprocess.TimeoutExpired:result={'case':name,'scenario':scenario,'completed':False,'error':'timeout30s'}
 if result['completed']:
  data=out/(name+'.dat');lines=data.read_text().splitlines();rows=[[float(x) for x in line.split()] for line in lines[1:] if line.strip()]
  overlap=0;charge=0;peak=0
  for a,b in zip(rows,rows[1:]):
   dt=b[0]-a[0]
   if b[1]>1.1 and b[2]<-.4:overlap+=dt
   cross=min(max(b[5],0),max(-b[6],0));charge+=cross*dt;peak=max(peak,cross)
  result['postprocessed']={'conservative_gate_overlap_s':overlap,'cross_current_indicator_peak_A':peak,'cross_current_indicator_charge_C':charge,'full_waveform_points':len(rows),'final_time_s':rows[-1][0]}
  indices=set(range(0,len(rows),max(1,len(rows)//1000)))
  for col in range(1,7):
   for extremum in [min,max]:
    j=extremum(range(len(rows)),key=lambda i:rows[i][col]);indices.update(range(max(0,j-5),min(len(rows),j+6)))
  (out/(name+'-sampled.csv')).write_text('time_s,vgs_Q1_V,vgs_Q2_V,vds_Q1_V,vds_Q2_V,I_Q1_A,I_Q2_A\n'+'\n'.join(','.join(map(str,rows[j])) for j in sorted(indices))+'\n')
  data.unlink()
 print(json.dumps(result),flush=True);return result
cases=[]
for vb,rg in itertools.product((1.8,2.4,3.4),(0,4.7)):
 cases.append(run(f'pwm-{vb}-{rg}',vb,rg,100e-9,'pwm'))
for scenario,rg in itertools.product(('vdd_loss','mcu_loss','startup','battery_loss'),(0,4.7)):
 cases.append(run(scenario+'-'+str(rg),3.4,rg,100e-9,scenario))
(out/'results-stable.json').write_text(json.dumps({'status':'manufacturer_typical_models_with_assumed_rails_and_parasitics_not_qualification','cases':cases,'sources':{'UCC27524':'https://www.ti.com/lit/zip/slum510','SiSS64DN':'https://www.vishay.com/docs/78813/siss64dn_ps_revb.zip','DMP2008UFG':'https://www.diodes.com/spice/download/2274/DMP2008UFG.spice.txt'},'limitations':['UCC model is original UCC27524, not guaranteed UCC27524A/SOIC corners.','MOSFET models are typical, fixed temperature, no self heating or guaranteed maximum charge. DMP Rta numerical floor changed from1e-20 to1e-6ohm; original source retained.','Rail waveforms, 0.5ohm/10uH motor and 100nH gate/5nH source L are explicit assumptions.','Generic flyback diode, ideal prescribed battery sources, no measured wiring parasitics. battery_loss is a forced battery voltage collapse, not an open-disconnect test.','Threshold overlap uses minimum data sheet thresholds at low test current, not a direct shoot-through current.','Cross-current indicator includes displacement/diode currents, not solely channel conduction.','UCC macro uses ideal internal supplies, so zero-VDD physical behavior is not proven.','4.7ohm external resistors are a circuit proposal, not present in canonical or prior candidate CAD.']},indent=2)+'\n')
