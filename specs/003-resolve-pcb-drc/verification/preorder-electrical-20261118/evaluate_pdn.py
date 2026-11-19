#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,itertools,re,csv,hashlib
out=Path(__file__).resolve().parent;work=out/'pdn';work.mkdir(exist_ok=True)
rows=[]
for rtop,rbot,tol,tcr,label in ((732e3,100e3,.01,100e-6,'baseline-1pct'),(750e3,100e3,.01,100e-6,'750k-1pct'),(75e3,10e3,.001,25e-6,'75k-precision')):
 # Independent initial tolerance and TCR signs; -40..100C gives |delta T| <=75C.
 low=(1-tol)*(1-tcr*75);high=(1+tol)*(1+tcr*75)
 vmin=.580*(1+rtop*low/(rbot*high))-20e-9*rtop*high
 vmax=.610*(1+rtop*high/(rbot*low))+20e-9*rtop*high
 for bulk,local,charge,rl,lg in itertools.product((4e-6,10e-6),(.5e-6,1e-6),('representative','budget'),(.05,.25),(10e-9,100e-9)):
  name=f'{len(rows):03d}'
  qn,qp,ipn,ipp=(80e-9,100e-9,.8,.2) if charge=='representative' else (300e-9,300e-9,1.,.25)
  wn=2*qn/ipn;wp=2*qp/ipp
  deck=f'''Gate supply passive charge-delivery envelope (not TPS61023 control model)
Vsource src 0 {vmin}
Vcut ctl 0 PWL(0 1 15u 1 15.001u 0)
Ssrc src bulk ctl 0 CUT
.model CUT SW(Ron=.001 Roff=1e12 Vt=.5 Vh=.05)
Rbulk bulk cb .01
Cbulk cb 0 {bulk}
Rtrace bulk li {rl}
Ltrace li pin {lg}
Rlocal pin cl .02
Llocal cl cc 1n
Clocal cc 0 {local}
Rfast pin cf .02
Lfast cf cff 1n
Cfast cff 0 60n
Iload pin 0 PWL(0 0 20u 0 {20e-6+wn/2} {ipn} {20e-6+wn} 0 29.314u 0 {29.314e-6+wp/2} {ipp} {29.314e-6+wp} 0)
Rdc pin 0 1G
.options method=gear reltol=.0005
.tran 1n 40u
.meas tran vmin MIN v(pin) FROM=19u TO=40u
.meas tran vmax MAX v(pin) FROM=19u TO=40u
.end
'''
  p=work/(name+'.cir');p.write_text(deck);log=work/(name+'.log')
  proc=subprocess.run(['ngspice','-n','-b','-o',str(log),str(p)],capture_output=True,text=True,timeout=20)
  text=log.read_text();meas={k:float(v) for k,v in re.findall(r'^(vmin|vmax)\s*=\s*([-+\d.eE]+)',text,re.M)}
  row={'Rtop_ohm':rtop,'Rbottom_ohm':rbot,'resistor_case':label,'initial_tolerance':tol,'TCR_per_K':tcr,'source_min_V':vmin,'static_max_including_25C_leakage_V':vmax,'Cbulk_F':bulk,'Clocal_F':local,'C104_effective_F':60e-9,'charge_case':charge,'Q1_charge_C':qn,'Q2_charge_C':qp,'Q1_pulse_peak_A':ipn,'Q2_pulse_peak_A':ipp,'supply_R_ohm':rl,'supply_L_H':lg,'case':name,'completed':proc.returncode==0 and len(meas)==2,**meas}
  if row['completed']:row['UVLO_margin_V']=meas['vmin']-4.65
  rows.append(row)
report={'status':'passive_envelope_not_full_regulator_or_guaranteed_component_corners','source_pcb_sha256':hashlib.sha256(Path('hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb').read_bytes()).hexdigest(),'cases':rows,'assumptions':['No converter response for25us after source disconnect; capacitors start charged at feedback minimum.','Two triangular gate-load pulses: representative80/100nC with0.8/0.2A peaks, budget300/300nC with1/0.25A peaks; widths derived from charge and bounded peaks. Neither charge is a guaranteed MOSFET max.','Cbulk4/10uF and Clocal0.5/1uF are explicit effective-capacitance sensitivity values, not measured nor manufacturer guaranteed minima.','60nF high-frequency bypass,1nH ESL,20mOhm local ESR,10mOhm bulk ESR and trace10/100nH,0.05/0.25ohm are assumed bounds.','Feedback580..610mV PWM from TPS61023 RevB p5; initial tolerance and independent TCR corner over -40..100C. +/-20nA FB leakage sensitivity is from25C maximum, NOT a full-temperature guarantee.','UCC27524A SOIC UVLO rising max4.65V used conservatively as run-time comparison; this is not a model of its hysteretic reset behavior.']}
(out/'pdn-results.json').write_text(json.dumps(report,indent=2)+'\n')
with (out/'pdn-results.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for label in ('baseline-1pct','750k-1pct','75k-precision'):
 for charge in ('representative','budget'):
  group=[r for r in rows if r['resistor_case']==label and r['charge_case']==charge and r['completed']]
  print(label,charge,'done',len(group),'worst',min(r['vmin'] for r in group),'below4.65',sum(r['vmin']<4.65 for r in group))
