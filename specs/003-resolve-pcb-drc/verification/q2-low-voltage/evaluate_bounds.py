#!/usr/bin/env python3
"""Repeatable Q2 boundary arithmetic. Sensitivity models are not measurements."""
from pathlib import Path
import itertools,json,math
out=Path(__file__).resolve().parent
vmin=.6*.975*(1+732*.99/(100*1.01));vmax=.6*1.025*(1+732*1.01/(100*.99))
thermal=[]
for theta,factor,current in itertools.product((52,137),(1,1.5,2),(3,5,10)):
 p=current**2*.017*factor
 thermal.append({'assumed_RthetaJA_C_per_W':theta,'assumed_Rds_temperature_factor':factor,'brake_Irms_A':current,'conduction_loss_W':p,'assumed_Tambient_C':40,'steady_Tj_estimate_C':40+p*theta,'status':'fixture-dependent sensitivity, not this PCB prediction'})
limits=[{'assumed_RthetaJA_C_per_W':t,'assumed_Rds_temperature_factor':f,'illustrative_Tj_target_C':125,'assumed_Tambient_C':40,'continuous_Irms_A':math.sqrt(85/(t*.017*f))} for t,f in itertools.product((52,137),(1,1.5,2))]
corners=[{'VBAT_V':b,'OUTB_V':g,'VGS_V':g-b,'absolute_rating_8V_exceeded':abs(g-b)>8} for b,g in itertools.product((0,1.8,2.4,3.4),(0,vmin,vmax))]
result={'status':'calculated_static_bounds_and_thermal_sensitivity_only','VBAT_analysis_range_V':[1.8,3.4],'boost_static_feedback_range_V':[vmin,vmax],'UCC27524ADR_D_SOIC_UVLO_rising_max_V_at_minus40_to140C':4.65,'static_lower_boost_minus_UVLO_margin_V':vmin-4.65,'low_VGS_guarantee_magnitude_V':1.5,'maximum_OUTB_LOW_plus_reference_error_V_at_VBAT1_8':.3,'Q2_pin_mapping':{'1':'VBAT','2':'VBAT','3':'VBAT','4':'GATE_P','5':'MOTOR_MINUS','6':'MOTOR_MINUS','7':'MOTOR_MINUS','8':'MOTOR_MINUS'},'static_VGS_corners':corners,'thermal_sensitivity':thermal,'illustrative_continuous_Irms_limits':limits,'additional_source_branch_estimate':{'assumed_copper_um':35,'assumed_resistivity_ohm_m':1.724e-8,'parallel_branches':3,'each_length_mm':1.17,'each_width_mm':.42,'equivalent_R_ohm':1.724e-8*.00117/(3*.00042*35e-6),'not_included':'pad neck, original buses, contacts, vias, temperature rise'},'limitations':['No ripple/load/start-up model for the boost converter; 132mV static margin is not an enable guarantee.','RthetaJA 52/137C/W refer to datasheet test fixtures; neither is established for this PCB.','Temperature factor 1/1.5/2 is a sensitivity assumption, not a manufacturer guaranteed maximum.','125C is an illustrative engineering target, not an enforced protection threshold.','No fixed brake duration/Irms is asserted for every Mini4WD-compatible motor.','No guaranteed 5V full-temperature UCC output impedance substituted from 12V test conditions.','Reverse battery, battery regeneration, gate overshoot and logic below minimum VCC remain outside the static corners.']}
assert not any(c['absolute_rating_8V_exceeded'] for c in corners)
(out/'bounds.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'static_VGS_range_V':[min(c['VGS_V'] for c in corners),max(c['VGS_V'] for c in corners)],'UVLO_static_margin_V':vmin-4.65,'5A_40C_137CperW_Rdsx2_C':40+25*.017*2*137,'illustrative_125C_Irms_at137_Rdsx2_A':math.sqrt(85/(137*.017*2))},indent=2))
