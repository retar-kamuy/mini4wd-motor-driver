#!/usr/bin/env python3
"""DMP2008UFG vendor-model study; assumed driver and motor are not validated ICs."""
from pathlib import Path
import hashlib,itertools,json,re,subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
MODEL=ROOT/'hardware/kicad/mini4wd-motor-driver/datasheets/DMP2008UFG.spice.txt'
raw=MODEL.read_text()
adapted='\n'.join('* ngspice compatibility: '+s if s.strip().upper()=='.SIMULATOR DEFAULT' else s for s in raw.splitlines())+'\n'
(OUT/'DMP2008UFG-ngspice.lib').write_text(adapted)

def run(name,body,measurements):
    bench=OUT/(name+'.cir');log=OUT/(name+'.log')
    text='DMP2008UFG low battery study\n.include DMP2008UFG-ngspice.lib\n'+body+'\n.end\n'
    bench.write_text(text)
    p=subprocess.run(['ngspice','-b','-o',str(log),str(bench)],cwd=OUT,capture_output=True,text=True,timeout=20)
    result={k:float(v) for k,v in re.findall(r'^([a-z_]+)\s*=\s*([-+\deE.]+)',log.read_text(),re.M) if k in measurements}
    if p.returncode or set(result)!=set(measurements):raise RuntimeError((name,p.returncode,result,str(log)))
    return result

static=[]
for i,(vb,current,temp) in enumerate(itertools.product((1.8,2.0,2.4,3.2),(1,5,10,-5),(25,85))):
    result=run('dc-%02d'%i,f'''Vbat s 0 {vb}
Vdriver g 0 0.01
Iload d 0 {current}
Xq d g s DMP2008UFG
Bds dsmon 0 V=V(d,s)
Bgs gsmon 0 V=V(g,s)
.temp {temp}
.tran 100n 1u
.measure tran vds_on FIND V(dsmon) AT=1u
.measure tran vgs_on FIND V(gsmon) AT=1u''',('vds_on','vgs_on'))
    static.append(dict(vbat_V=vb,current_A=current,temp_C=temp,r_on_model_ohm=abs(result['vds_on']/current),**result))
transient=[]
for i,(vb,lm) in enumerate(itertools.product((1.8,2.4,3.2),(10e-6,100e-6))):
    result=run('brake-%02d'%i,f'''Vbat s 0 {vb}
Vcommand cmd 0 PWL(0 5.208 1m 5.208 1.00002m 0.01 10m 0.01 10.00002m 5.208 12m 5.208)
Rdriver cmd lead 1
Ltrace lead g 20n
Xq d g s DMP2008UFG
Bds dsmon 0 V=V(d,s)
Bgs gsmon 0 V=V(g,s)
Vbemf s emf PWL(0 3 1m 3 10m 0.3 12m 0)
Rmotor emf winding 0.5
Lmotor winding d {lm}
Dfly d s freewheel
Dnbody 0 d freewheel
.model freewheel D(Is=1e-8 N=1 Rs=0.01)
Bcurrent mon 0 V=abs(i(Lmotor))
Bpower pmon 0 V=abs(v(d,s)*i(Vbat))
.tran 100n 12m 0 100n
.measure tran i_motor_peak MAX V(mon)
.measure tran vgs_max MAX V(gsmon)
.measure tran vgs_min MIN V(gsmon)
.measure tran vds_max MAX V(dsmon)
.measure tran vds_min MIN V(dsmon)''',('i_motor_peak','vgs_max','vgs_min','vds_max','vds_min'))
    transient.append(dict(vbat_V=vb,assumed_motor_inductance_H=lm,**result))
feedback_min=.6*(1-.025)*(1+732*(1-.01)/(100*(1+.01)))
feedback_max=.6*(1+.025)*(1+732*(1+.01)/(100*(1-.01)))
result={'status':'vendor_typical_model_and_explicit_assumptions_not_qualification','model_url':'https://www.diodes.com/spice/download/2274/DMP2008UFG.spice.txt','original_model_sha256':hashlib.sha256(MODEL.read_bytes()).hexdigest(),'compatibility_change':'Only .SIMULATOR DEFAULT is commented; model and vendor license retained.','static_cases':static,'transient_cases':transient,'boost_feedback_static_V':[feedback_min,feedback_max],'DC_guaranteed_25C_loss_W_at_5A':{'minus1_5V':25*.017,'minus1_8V':25*.013,'minus2_5V':25*.0098},'limitations':['Manufacturer typical MOSFET model is not a tolerance or SOA guarantee.','DC VOL=0.01V is an assumed driver level; actual UCC output and traces are not modeled.','Transient driver is a prescribed source plus 1ohm and 20nH; no UCC internal logic, UVLO or startup guarantee.','Transient motor is hypothetical 0.5ohm plus 10/100uH with a prescribed decaying 3V back EMF, not an identified motor.','Clamp diodes are generic; no measured layout parasitics, heating or real battery impedance.','Feedback output estimate includes resistor 1% and reference 2.5% only; startup/overshoot and faults are outside it.','ngspice ignores unsupported model parameter N on the LEVEL=3 MOSFET and clamps Rta=1e-20ohm to 1e-12ohm; results remain exploratory.', 'No claim of universal motor compatibility, PCBA readiness or measured temperature.']}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'static_cases':len(static),'transient_cases':len(transient),'boost_feedback_static_V':result['boost_feedback_static_V'],'static_r_model_range_ohm':[min(x['r_on_model_ohm'] for x in static),max(x['r_on_model_ohm'] for x in static)],'transient_vgs_min_V':min(x['vgs_min'] for x in transient),'transient_vgs_max_V':max(x['vgs_max'] for x in transient),'transient_motor_peak_A':max(x['i_motor_peak'] for x in transient)},indent=2))
