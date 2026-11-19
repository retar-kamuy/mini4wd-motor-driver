#!/usr/bin/env python3
"""Conditional thermal envelope, not measured motor/PCB thermal qualification."""
from pathlib import Path
import itertools,json,math,csv
out=Path(__file__).resolve().parent
results=[]
for hold,i0,tau_i,theta,tau_th in itertools.product((3,10,30),(5,10),(0.1,1,5,None),(52,137),(1,10,100)):
 dt=.002;rise=0;peak=0;peak_t=0;e=0;integral_i2=0
 for k in range(int(hold/dt)):
  t=(k+.5)*dt;i=i0 if tau_i is None else i0*math.exp(-t/tau_i);p=i*i*.017*2
  rise=rise*math.exp(-dt/tau_th)+p*theta*(1-math.exp(-dt/tau_th))
  e+=p*dt;integral_i2+=i*i*dt
  if rise>peak:peak=rise;peak_t=t
 results.append({'hold_command_s':hold,'initial_current_A':i0,'assumed_current_decay_tau_s':tau_i,'current_profile':'sustained imposed generation' if tau_i is None else 'exponentially decaying back EMF/current','assumed_RthetaJA_C_per_W':theta,'assumed_thermal_time_constant_s':tau_th,'assumed_Rds_ohm':.034,'assumed_Tambient_C':40,'Tj_peak_sensitivity_C':40+peak,'Tj_end_sensitivity_C':40+rise,'peak_time_s':peak_t,'electrical_loss_energy_J':e,'Irms_over_hold_A':math.sqrt(integral_i2/hold)})
record={'status':'parameter_sensitivity_only_not_this_PCB_temperature','case_count':len(results),'equation':'d(Tj-Ta)/dt = (I^2*Rds*RthetaJA - (Tj-Ta))/tau_thermal; I=I0*exp(-t/tau_current), or sustained I','assumptions':['3/10/30s command hold reflects user circuit-running scenario.','40C ambient, Rds=.017ohm*2 temperature factor are engineering assumptions, not measured limits.','52/137C/W are fixture-specific data sheet numbers; neither is this PCB verified RthetaJA.','1/10/100s thermal time constants and .1/1/5s motor current decay are sensitivity inputs, not manufacturer/motor measured values.','Holding brake does not itself apply battery drive: motor back EMF drives the short-brake loop and normally decays after stopping.','Sustained current represents externally sustained rotation/generation; it is not inferred from a 30s brake command.','No coupled heating from Q1/driver/boost/battery, no airflow/enclosure measurements.','Results exceeding150C indicate a failed assumed thermal scenario, not a predicted real temperature beyond ratings.'],'cases':results}
(out/'brake-heat.json').write_text(json.dumps(record,indent=2)+'\n')
with (out/'brake-heat.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=results[0]);w.writeheader();w.writerows(results)
select=[x for x in results if x['hold_command_s']==30 and x['initial_current_A']==5 and x['assumed_RthetaJA_C_per_W']==137 and x['assumed_thermal_time_constant_s']==10]
print(json.dumps({'cases':len(results),'selected_30s_5A_137CperW_tauThermal10s':select},indent=2))
