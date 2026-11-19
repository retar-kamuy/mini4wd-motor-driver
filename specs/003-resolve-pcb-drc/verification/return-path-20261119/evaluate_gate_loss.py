from pathlib import Path
import json,subprocess,re,shutil,hashlib
out=Path(__file__).resolve().parent/'gate33';out.mkdir(exist_ok=True);old=out.parent.parent/'switching-validation'
for n in ('UCC27524.lib','SiSS64DN.lib','DMP2008UFG-stable.lib'):shutil.copy2(old/n,out/n)
s=(old/'evaluate_switching.py').read_text();function=s[s.index('def run('):s.index('cases=[]')].replace('.tran 2n 110u 0 2n','.tran 1n 110u 0 1n')
function=function.replace("data.unlink()", "result['positive_terminal_energy_J']={label:sum(max(bb[v]*bb[i],0)*(bb[0]-aa[0]) for aa,bb in zip(rows,rows[1:])) for label,v,i in [('Q1',3,5),('Q2',4,6)]};data.unlink()")
cases=[]
for rgp,rail,vb in [(22,5.212886364,3.4),(33,5.212886364,3.4),(22,4.903554936,1.8),(33,4.903554936,1.8)]:
 ns={'out':out,'subprocess':subprocess,'re':re,'json':json};exec(function.replace('5.208',str(rail)).replace('3.3','3.267'),ns)
 r=ns['run'](f'losscompare-{rgp}-{vb}',vb,4.7,100e-9,'pwm',rgp=rgp);r['logic_nominal_V']=3.267;cases.append(r)
 (out.parent/'gate-loss-compare.json').write_text(json.dumps({'status':'typical_27C_model_energy_comparison_not_heat_or_PVT_guarantee','cases':cases},indent=2)+'\n')
