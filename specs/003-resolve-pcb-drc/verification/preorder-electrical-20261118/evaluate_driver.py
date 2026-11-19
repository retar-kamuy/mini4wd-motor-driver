#!/usr/bin/env python3
"""Re-use the vendor-typical bench at the newly selected rail corners.
Does not model TPS61023, real motor, full power sequencing, or device PVT.
"""
from pathlib import Path
import json,subprocess,re,shutil,hashlib
base=Path(__file__).resolve().parent;out=base/'driver';out.mkdir(exist_ok=True)
old=base.parent/'switching-validation'
for name in ('UCC27524.lib','SiSS64DN.lib','DMP2008UFG-stable.lib'):shutil.copy2(old/name,out/name)
text=(old/'evaluate_switching.py').read_text();function=text[text.index('def run('):text.index('cases=[]')]
cases=[]
for rail,scenario,vbat,extra in [(5.212886364,'pwm',3.4,0),(4.903554936,'pwm',1.8,0),(5.212886364,'startup',3.4,0),(5.212886364,'battery_open',3.4,0),(5.212886364,'vdd_loss',3.4,0),(5.212886364,'mcu_loss',3.4,0),(4.903554936,'vdd_loss',3.4,1.8e-9),(4.903554936,'mcu_loss',3.4,1.8e-9)]:
 ns={'out':out,'subprocess':subprocess,'re':re,'json':json}
 exec(function.replace('5.208',str(rail)),ns)
 result=ns['run'](f'{rail}-{scenario}-{extra}',vbat,4.7,100e-9,scenario,rgp=22,extra_n_gate_C=extra)
 result['prescribed_boost_rail_V']=rail;cases.append(result)
r={'status':'vendor_typical_model_sensitivity_not_power_sequence_or_PVT_guarantee','source_pcb_sha256':hashlib.sha256(Path('hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb').read_bytes()).hexdigest(),'cases':cases,'model_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.lib')},'limitations':['UCC27524 macro is not a guaranteed UCC27524A/SOIC model; fixed internal UVLO4.25V and ideal internal supplies remain.','Prescribed rails and ENA waveforms, fixed27C, generic diode,0.5ohm/10uH motor,100nH gate/5nH source assumptions; no self-heating or full PVT.','Threshold overlap is25C minimum-threshold indicator, not separated shoot-through current.','1.8nF extra Q1 capacitance is a sensitivity knob; not an added physical component.','TPS61023 startup/control loop is NOT simulated.']}
(base/'driver-results.json').write_text(json.dumps(r,indent=2)+'\n')
print('completed',sum(c['completed'] for c in cases),'of',len(cases))
