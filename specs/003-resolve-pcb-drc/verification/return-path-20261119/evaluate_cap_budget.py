from pathlib import Path
import json,csv,itertools,subprocess,re
out=Path(__file__).resolve().parent;work=out/'pdn-cap';work.mkdir(exist_ok=True)
rail=.580*(1+75e3*.999*(1-.000025*75)/(10e3*1.001*(1+.000025*75)))-20e-9*75e3*1.001*(1+.000025*75)
rows=[]
for bulk,local,dc,hold,rl,lg in itertools.product((4e-6,10e-6),(1e-6,2e-6,4e-6),(.02,.05),(5e-6,25e-6),(.05,.25),(10e-9,100e-9)):
 name=str(len(rows));restore=15e-6+hold;deck=f'''Passive PDN sensitivity with selected22uF local candidate; not TPS61023 loop
Vsrc src 0 {rail}
Vctl ctl 0 PWL(0 1 15u 1 15.001u 0 {restore} 0 {restore+1e-9} 1)
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
Idc pin 0 {dc}
Igate pin 0 PWL(0 0 20u 0 20.3u 1 20.6u 0 29.314u 0 30.514u .25 31.714u 0)
.options method=gear reltol=.0005
.tran 2n 45u
.meas tran vmin MIN v(pin) FROM=15u TO=45u
.meas tran vmax MAX v(pin) FROM=15u TO=45u
.end
'''
 p=work/(name+'.cir');p.write_text(deck);log=work/(name+'.log');r=subprocess.run(['ngspice','-n','-b','-o',str(log),str(p)],capture_output=True,text=True,timeout=15)
 meas={k:float(v) for k,v in re.findall(r'^(vmin|vmax)\s*=\s*([-+\d.eE]+)',log.read_text(),re.M)}
 row={'bulk_effective_F':bulk,'C105_effective_F':local,'constant_load_A':dc,'no_converter_response_s':hold,'Rtrace_ohm':rl,'Ltrace_H':lg,'completed':r.returncode==0 and len(meas)==2,**meas};rows.append(row)
(out/'cap-pdn-results.json').write_text(json.dumps({'status':'explicit_effective_cap_and_response_sensitivity_not_component_minimum_or_converter_model','source_min_V':rail,'gate_charge_each_C':300e-9,'cases':rows},indent=2)+'\n')
with (out/'cap-pdn-results.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Bounded startup charge/energy estimates, not real TPS61023 time guarantees.
startup=[]
for cap,drive,load in itertools.product((50e-6,110e-6),(.05,.1,.2),(0,.02,.05)):
 startup.append({'C_load_upper_F':cap,'assumed_boost_output_available_A':drive,'assumed_startup_load_A':load,'time_to5_213V_s':None if drive<=load else cap*5.213/(drive-load),'energy_at5_213V_J':.5*cap*5.213**2})
(out/'startup-cap-budget.json').write_text(json.dumps({'status':'constant_cap_constant_current_budget_not_regulator_startup_simulation','cases':startup,'note':'50/110uF cover external capacitor nominal/tolerance/temperature and approximate module loading as sensitivity bounds. Available output currents and loads are assumptions, not TPS61023 guaranteed startup currents.'},indent=2)+'\n')
for local in (1e-6,2e-6,4e-6):
 for dc in (.02,.05):
  for hold in (5e-6,25e-6):
   x=[r for r in rows if r['C105_effective_F']==local and r['constant_load_A']==dc and r['no_converter_response_s']==hold and r['completed']];print(local,dc,hold,'min',min(r['vmin'] for r in x),'below4.65',sum(r['vmin']<4.65 for r in x),flush=True)
