from pathlib import Path
import json,subprocess,re,shutil,hashlib
out=Path(__file__).resolve().parent/'gate33';out.mkdir(exist_ok=True);old=out.parent.parent/'switching-validation'
for n in ('UCC27524.lib','SiSS64DN.lib','DMP2008UFG-stable.lib'):shutil.copy2(old/n,out/n)
s=(old/'evaluate_switching.py').read_text();function=s[s.index('def run('):s.index('cases=[]')].replace('.tran 2n 110u 0 2n','.tran 1n 110u 0 1n')
function=function.replace("data.unlink()", "result['positive_terminal_energy_J']={label:sum(max(bb[v]*bb[i],0)*(bb[0]-aa[0]) for aa,bb in zip(rows,rows[1:])) for label,v,i in [('Q1',3,5),('Q2',4,6)]};data.unlink()")
cases=[]
for rgp,rail,scenario,vb,extra in [(22,4.903554936,'vdd_loss',3.4,1.8e-9),(33,4.903554936,'vdd_loss',3.4,1.8e-9),(33,4.903554936,'mcu_loss',3.4,1.8e-9),(33,5.212886364,'pwm',3.4,0),(33,4.903554936,'pwm',1.8,0),(33,5.212886364,'startup',3.4,0),(33,5.212886364,'battery_open',3.4,0),(33,5.212886364,'vdd_loss',3.4,0),(33,5.212886364,'mcu_loss',3.4,0)]:
 ns={'out':out,'subprocess':subprocess,'re':re,'json':json};exec(function.replace('5.208',str(rail)),ns)
 r=ns['run'](f'Rgp{rgp}-{rail}-{scenario}-{extra}',vb,4.7,100e-9,scenario,rgp=rgp,extra_n_gate_C=extra);r['prescribed_boost_V']=rail;cases.append(r)
 (out.parent/'gate33-results.json').write_text(json.dumps({'status':'vendor_typical_model_sensitivity_not_PVT_or_SOA_guarantee','timestep_s':1e-9,'cases':cases,'limitations':['UCC27524 macro not guaranteed UCC27524A/SOIC corners; fixed27C and assumed EN/rails.','0.5ohm/10uH motor,100nH gate/5nH source, generic diode.','Extra1.8nF Q1 capacitor is sensitivity only, not physical addition.','Positive terminal energy includes displacement/storage, not isolated channel thermal dissipation.']},indent=2)+'\n')
