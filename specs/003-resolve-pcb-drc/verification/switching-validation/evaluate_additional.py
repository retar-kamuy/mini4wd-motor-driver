#!/usr/bin/env python3
from pathlib import Path
import json
p=Path(__file__).with_name('evaluate_switching.py');ns={'__file__':str(p.resolve())};exec(p.read_text().split('cases=[]')[0],ns)
out=ns['out'];u=(out/'UCC27524.lib').read_text(errors='replace')
(out/'UCC27524-UVLO-high.lib').write_text(u.replace('4.25','4.65').replace('0.35*','0.25*'))
(out/'UCC27524-UVLO-low.lib').write_text(u.replace('4.25','3.70').replace('0.35*','0.30*'))
cases=[]
for rg in (0,4.7):cases.append(ns['run']('open-'+str(rg),3.4,rg,100e-9,'battery_open'))
for variant in ['high','low']:
 cases.append(ns['run']('vdd-UVLO-'+variant,3.4,4.7,100e-9,'vdd_loss',driver_lib='UCC27524-UVLO-'+variant+'.lib'))
for mode in ['pwm','vdd_loss']:cases.append(ns['run']('hot85-'+mode,3.4,4.7,100e-9,mode,temp=85))
(out/'results-additional.json').write_text(json.dumps({'status':'additional_assumed_corner_models_not_guaranteed_corners','cases':cases,'limitations':['Open-switch test has10uF battery-side input capacitor,0.11ohm source impedance, prescribed retained5V/3.3V rails.','UVLO high4.65V falling4.40V and low3.70V falling3.40V are model variants based on SOIC table endpoints; other model parameters remain typical.','27/85C model temperatures do not include self heating.','Minimum25C gate thresholds used for the overlap indicator are not full-temperature minimum thresholds.']},indent=2)+'\n')
