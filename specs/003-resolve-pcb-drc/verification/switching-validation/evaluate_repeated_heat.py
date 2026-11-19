#!/usr/bin/env python3
"""Periodic thermal sensitivity using a sourced lap time and assumed brake events."""
from pathlib import Path
import json,math,itertools,csv
out=Path(__file__).resolve().parent
lap=75.476/10

def response(initial,t,tau,theta,p0,a):
 decay=math.exp(-t/tau)
 if abs(1-a*tau)<1e-9:return initial*decay+p0*theta*(t/tau)*decay
 return initial*decay+p0*theta*(math.exp(-a*t)-decay)/(1-a*tau)

cases=[]
for brakes_per_lap,i0,taui,theta,tauth in itertools.product((1,2,3),(5,10),(.1,1,5,None),(52,137),(1,10,100)):
 period=lap/brakes_per_lap;hold=2;rd=.034;p0=i0*i0*rd;a=0 if taui is None else 2/taui
 after=response(0,hold,tauth,theta,p0,a)*math.exp(-(period-hold)/tauth)
 initial=after/(1-math.exp(-period/tauth))
 samples=[response(initial,hold*k/2000,tauth,theta,p0,a) for k in range(2001)]
 energy=p0*hold if a==0 else p0/a*(1-math.exp(-a*hold))
 cases.append({'assumed_brake_events_per_lap':brakes_per_lap,'assumed_start_interval_s':period,'assumed_hold_command_s':hold,'initial_current_A':i0,'assumed_current_decay_tau_s':taui,'assumed_Rds_ohm':rd,'assumed_RthetaJA_C_per_W':theta,'assumed_thermal_tau_s':tauth,'assumed_ambient_C':40,'steady_period_start_Tj_sensitivity_C':40+initial,'steady_period_peak_Tj_sensitivity_C':40+max(samples),'steady_mean_Tj_sensitivity_C':40+energy/period*theta,'loss_energy_per_event_J':energy,'average_loss_W':energy/period,'Irms_over_period_A':math.sqrt(energy/rd/period)})
r={'status':'sourced_lap_time_but_assumed_electrical_braking_period_thermal_sensitivity','source_lap_time':{'url':'https://www.jstage.jst.go.jp/article/jsoft/36/3/36_655/_pdf','pages':'660-662','ten_lap_time_s':75.476,'mean_lap_time_s':lap,'fastest_lap_s':6.947,'not_electrical_brake_timing_measurement':True},'track_context_source':'https://www.tamiya.com/japan/mini4wd/feature/2019/1206.html','assumptions':['1/2/3 brake events per lap are deliberately assumed; no measured electrical braking interval is published here.','2s brake command hold is a sensitivity assumption, not extracted from the paper.','0.1s sponge-contact time in the paper is not used as electrical brake duration or interval.','Each event resets the current to5/10A, assuming drive/re-acceleration between events; not a measured vehicle history.','ThetaJA52/137C/W and thermal time constants1/10/100s are unverified for this PCB.','Rds=.017*2ohm and40C ambient are assumptions, not full-temperature guaranteed loss.','Free decay and externally sustained generation are distinct conditions.','Steady periodic temperature is calculated analytically from the first-order thermal map; actual multicell thermal path is not modeled.','Standalone30s free/forced brake cases are in brake-heat.json; long overlapping commands are not reset into artificial new motor-current pulses.'],'cases':cases}
(out/'repeated-heat.json').write_text(json.dumps(r,indent=2)+'\n')
with (out/'repeated-heat.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=cases[0]);w.writeheader();w.writerows(cases)
print(json.dumps({'cases':len(cases),'mean_lap_s':lap,'representative':[x for x in cases if x['assumed_brake_events_per_lap'] in (1,3) and x['initial_current_A']==5 and x['assumed_RthetaJA_C_per_W']==137 and x['assumed_thermal_tau_s']==10 and x['assumed_current_decay_tau_s'] in (1,None)]},indent=2))
