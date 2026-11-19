"""Boundary-condition sensitivity for hobby prototype; not a calibrated thermal model."""
from pathlib import Path
import json,math,itertools
out=Path(__file__).parent;d=json.loads((out/'power-path-results.json').read_text());by={c['case']:c for c in d['cases']};R35=sum(by[n]['resistance_at20C_35um_ohm'] for n in ('drive_VBAT','drive_MOTOR','drive_GND'));R70=sum(by[n]['resistance_with_70um_copper_via_unchanged_ohm'] for n in ('drive_VBAT','drive_MOTOR','drive_GND'));Rbrake=sum(by[n]['resistance_at20C_35um_ohm'] for n in ('brake_VBAT','brake_MOTOR'))
A=.055*.021;alpha=.00393;ambient=40;module_analysis_ceiling=70;aux=.15;dt=11e-6
res={'pcb_sha256':d['pcb_sha256'],'status':'explicit_boundary_and_current_sensitivity_not_product_temperature_prediction','material_and_boundary_assumptions':{'board_area_m2':A,'copper_temperature_coefficient_K':alpha,'ambient_C':ambient,'module_temperature_analysis_ceiling_C':module_analysis_ceiling,'auxiliary_MCU_boost_power_W':aux,'deadtime_each_edge_budget_s':dt,'Q1_Rds_25C_max_4_5V_ohm':.00286,'Q2_Rds_25C_max_minus1_5V_ohm':.017,'MOSFET_hot_resistance_multiplier_sensitivity':2,'contact_resistance_each_initial_ohm':.010,'D1_Vf_at5A_25C_max_V':.55},'dc_copper':{'drive_35um_20C_ohm':R35,'drive_70um_20C_ohm':R70,'brake_35um_20C_ohm':Rbrake},'diode_pwm':[],'board_equilibrium_sensitivity':[],'board_current_for70C_sensitivity':[],'brake_repeated_sensitivity':[]}
for I,f,Vf,Rth in itertools.product((2,3.5,5),(1000,5000,10000,20000),(.55,.7),(60,137,250,400)):
 frac=min(1,2*f*dt);P=I*Vf*frac;res['diode_pwm'].append({'constant_current_A':I,'PWM_Hz':f,'Vf_budget_V':Vf,'diode_on_fraction_upper_sensitivity':frac,'average_loss_W':P,'assumed_Rtheta_C_W':Rth,'temperature_rise_K_sensitivity':P*Rth})
# Uniform board sensitivity includes Cu(T) feedback and explicitly selected heat exits.
for R,I,h,faces,Gwire,fcontact in itertools.product((R35,R70),(2,3.5,5),(5,10,20),(1,2),(0,.01,.025),(0,.5)):
 thick=35 if R==R35 else 70;G=h*faces*A+Gwire;Rco=R*(1+alpha*(ambient-20));Rf=.00286*2+.04*fcontact;Pfixed=aux+I*I*Rf+I*.55*min(1,2*1000*dt);den=G-I*I*R*alpha
 rise=(I*I*Rco+Pfixed)/den if den>0 else None
 res['board_equilibrium_sensitivity'].append({'assumed_copper_um':thick,'constant_current_A':I,'h_W_m2K':h,'exposed_faces':faces,'wire_heat_exit_W_K':Gwire,'fraction_contact_heat_to_board':fcontact,'temperature_C':ambient+rise if rise is not None else None,'comparison_to70C':rise is not None and ambient+rise<=70})
for R,h,faces,Gwire,fcontact in itertools.product((R35,R70),(5,10,20),(1,2),(0,.01,.025),(0,.5)):
 G=h*faces*A+Gwire;aa=R*(1+alpha*(70-20))+.00286*2+.04*fcontact;bb=.55*2*1000*dt;cc=aux-G*(70-ambient);Imax=(-bb+math.sqrt(bb*bb-4*aa*cc))/(2*aa) if cc<0 else 0
 res['board_current_for70C_sensitivity'].append({'assumed_copper_um':35 if R==R35 else 70,'h_W_m2K':h,'exposed_faces':faces,'wire_heat_exit_W_K':Gwire,'fraction_contact_heat_to_board':fcontact,'max_constant_current_A_under_assumptions':Imax})
# Exact linear one-pole repeated braking, P=I0^2*Rhot*exp(-2t/tauI).
for I0,Rth,tauh,tauI,Tb,period in itertools.product((3.5,5),(52,137,200),(1,10,100),(.1,1,5),(2,10,30),(5,15,40)):
 if Tb>=period:continue
 P=I0*I0*.017*2;a=2/tauI
 def heat(t):
  if abs(1-a*tauh)<1e-10:return Rth*P*(t/tauh)*math.exp(-t/tauh)
  return Rth*P*(math.exp(-a*t)-math.exp(-t/tauh))/(1-a*tauh)
 T0=heat(Tb)*math.exp(-(period-Tb)/tauh)/(1-math.exp(-period/tauh));peak=max(T0*math.exp(-t/tauh)+heat(t) for t in (Tb*j/1000 for j in range(1001)))
 res['brake_repeated_sensitivity'].append({'initial_current_A':I0,'assumed_Rtheta_C_W':Rth,'assumed_thermal_tau_s':tauh,'assumed_current_decay_tau_s':tauI,'brake_command_s':Tb,'repeat_period_s':period,'periodic_peak_temperature_C_at40C':40+peak})
res['steady_Q2_5A_hot_sensitivity_W']=25*.017*2
res['required_effective_Rtheta_Q2_at5A_for125C_at40C_C_W']=(125-40)/res['steady_Q2_5A_hot_sensitivity_W']
res['limitations']=['Centerline R omits pad spreading and zones; a 2D copper mesh is needed for actual via allocation.','Molex10mohm is initial low-level contact requirement, not a guaranteed hot5A value; crimp, wires, aging are separate.','Convection coefficient, exposed faces, wire heat sinking and contact heat fraction are assumed; board is not isothermal in practice.','70um copper is a sensitivity, not selected fabrication; 0.127mm routes require vendor DFM before changing copper specification.','D1 .55V is a25C5A limit; .7V and Rtheta values are sensitivities, not full-temperature guaranteed data.','D1 Rtheta60C/W uses50x50mm copper, much larger than this PCB; cannot transplant that value.','Q2 repeated thermal model assumes exponentially decaying current; a30s brake command is not30s constant5A.','No temperature feedback, calibrated thermal time constants, EMC or measured5A qualification is implied.']
(out/'thermal-budget-results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'R_drive35_mohm':1000*R35,'R_drive70_mohm':1000*R70,'R_brake35_mohm':1000*Rbrake,'copper_drive5A_W':25*R35,'D1_5A_1kHz_W':5*.55*2*1000*dt,'D1_5A_20kHz_W':5*.55*2*20000*dt,'board_cases':len(res['board_equilibrium_sensitivity']),'brake_cases':len(res['brake_repeated_sensitivity'])}))
