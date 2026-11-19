from pathlib import Path
import json,subprocess,re,shutil,itertools
out=Path(__file__).resolve().parent/'input-retention';out.mkdir(exist_ok=True);old=out.parent.parent/'switching-validation'
for n in ('UCC27524.lib','SiSS64DN.lib','DMP2008UFG-stable.lib'):shutil.copy2(old/n,out/n)
s=(old/'evaluate_switching.py').read_text();function=s[s.index('def run('):s.index('cases=[]')].replace('.tran 2n 110u 0 2n','.tran 1n 110u 0 1n')
old_va=r'Va a 0 PWL(0 3.3 60u 3.3 60.02u 0)';old_ena=r'Vena ena 0 PWL(0 3.3 59.98u 3.3 60u 0)'
cases=[]
for cap,rpd in itertools.product((10e-12,50e-12),(1e12,2200,1000)):
 new_va=rf'Vcmd cmd 0 3.3\nVcut ctl 0 PWL(0 1 60u 1 60.001u 0)\nSret cmd a ctl 0 RET\n.model RET SW(Ron=1 Roff=1e12 Vt=.5 Vh=.05)\nCret a 0 {cap}\nRpd a 0 {rpd}'
 f=function.replace('5.208','4.903554936').replace(old_va,new_va).replace(old_ena,'Vena ena 0 3.3').replace(r'Vbat batt 0 {vb}',r'Vcell raw 0 {vb}\nRcell raw batt .1')
 ns={'out':out,'subprocess':subprocess,'re':re,'json':json};exec(f,ns)
 c=ns['run'](f'C{cap}-R{rpd}',3.4,4.7,100e-9,'mcu_loss',rgp=33,extra_n_gate_C=1.8e-9);c.update({'assumed_N_command_retained_cap_F':cap,'external_pulldown_ohm':rpd});cases.append(c)
 (out.parent/'input-retention-results.json').write_text(json.dumps({'status':'explicit_power_loss_input_retention_sensitivity_not_device_guarantee','cases':cases,'limitations':['ENA held high for entire test represents delayed reset; actual supervisor has finite response.','N_COMMAND output is assumed high-Z with10/50pF stored charge at rail loss, not a guaranteed LVC behavior.','0.1ohm battery source assumption limits otherwise ideal source shoot-through; no heating/SOA model.','UCC27524 typical macro input400k pull-down, not guaranteed UCC27524A corners.']},indent=2)+'\n')
