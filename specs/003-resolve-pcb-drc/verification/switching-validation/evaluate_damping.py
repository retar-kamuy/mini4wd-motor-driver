#!/usr/bin/env python3
from pathlib import Path
import json,itertools
p=Path(__file__).with_name('evaluate_switching.py');ns={'__file__':str(p.resolve())};exec(p.read_text().split('cases=[]')[0],ns);out=ns['out'];cases=[]
for scenario,extra in itertools.product(('vdd_loss','mcu_loss','pwm'),(0,1.8e-9)):
 cases.append(ns['run']('asymmetric-'+scenario+'-'+str(extra),3.4,4.7,100e-9,scenario,rgp=22,extra_n_gate_C=extra))
(out/'results-damping.json').write_text(json.dumps({'status':'proposed_asymmetric_gate_resistor_sensitivity_only','cases':cases,'proposal':'Q1 series4.7ohm; Q2 series22ohm; not in canonical/candidate CAD','limitations':['Added1.8nF Q1 gate-source capacitor is a sensitivity knob, not a physical proposal or datasheet capacitance maximum.','MOSFET and driver remain typical models, no guaranteed Q2 minimum gate-charge or full5V PVT model.','Zero conservative threshold overlap in these scenarios does not prove all power sequences.']},indent=2)+'\n')
