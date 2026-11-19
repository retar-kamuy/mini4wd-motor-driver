from pathlib import Path
import json,subprocess,re,shutil,hashlib,itertools
out=Path(__file__).resolve().parent/'gate-sweep';out.mkdir(exist_ok=True)
old=out.parent.parent/'switching-validation'
for n in ('UCC27524.lib','SiSS64DN.lib','DMP2008UFG-stable.lib'):shutil.copy2(old/n,out/n)
s=(old/'evaluate_switching.py').read_text();function=s[s.index('def run('):s.index('cases=[]')]
cases=[]
for rgp,(rail,scenario,vb,extra) in itertools.product((22,27,33),((4.903554936,'vdd_loss',3.4,1.8e-9),(4.903554936,'mcu_loss',3.4,1.8e-9),(5.212886364,'pwm',3.4,1.8e-9),(4.903554936,'pwm',1.8,1.8e-9))):
 ns={'out':out,'subprocess':subprocess,'re':re,'json':json};exec(function.replace('5.208',str(rail)).replace('.tran 2n 110u 0 2n','.tran .2n 110u 0 .2n'),ns)
 r=ns['run'](f'Rgp{rgp}-{rail}-{scenario}',vb,4.7,100e-9,scenario,rgp=rgp,extra_n_gate_C=extra)
 r['prescribed_boost_V']=rail;cases.append(r)
p=out.parent/'gate-sweep-results.json';p.write_text(json.dumps({'status':'vendor_typical_model_and_assumed_parasitics_not_PVT_guarantee','timestep_s':.2e-9,'cases':cases,'limitations':['Same vendor-typical models and prescribed EN/rails as prior switching bench.','Extra1.8nF Q1 capacitor is sensitivity only, not physically added.','Threshold overlap is not directly channel shoot-through current; fixed27C.']},indent=2)+'\n')
