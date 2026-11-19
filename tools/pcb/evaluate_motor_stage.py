#!/usr/bin/env python3
"""Engineering sensitivity study, not a motor or board qualification.

Run with Python 3 and ngspice. Values not derived from the canonical PCB or a
measured motor are explicitly recorded as assumptions in the output.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    simulator = shutil.which("ngspice")
    if not simulator:
        raise SystemExit("ngspice is required; no simulated result was produced")
    cases = []
    for index, (vbat, rbat, rmotor, inductance) in enumerate(itertools.product(
            [1.8, 2.4, 3.2], [0.05, 0.2], [0.05, 0.2, 0.5], [10e-6, 100e-6])):
        # Zero back EMF represents a stationary rotor. The switch and diode
        # below are simple lumped models, not the vendor MOSFET/SS54 models.
        rpath, ron = 0.01, 0.00286
        bench = f"""Hypothetical stationary RL motor - sensitivity case {index}
Vbat battery 0 {vbat}
Rbattery battery bus {rbat}
Rpath bus motor_plus {rpath}
Rmotor motor_plus winding {rmotor}
Lmotor winding motor_minus {inductance}
Sdrive motor_minus 0 gate 0 drive
Vgate gate 0 PWL(0 0 1m 0 1.001m 5 11m 5 11.001m 0 16m 0)
Dfree motor_minus motor_plus clamp
.model drive SW(Ron={ron} Roff=1e9 Vt=2.5 Vh=0.1)
.model clamp D(Is=1e-8 N=1 Rs=0.01 Cjo=0)
Bcurrent current_monitor 0 V=i(Lmotor)
.tran 2u 16m 0 2u
.measure tran i_peak MAX V(current_monitor)
.measure tran i_before_off FIND V(current_monitor) AT=10.9m
.measure tran i_after_deadtime FIND V(current_monitor) AT=11.011m
.end
"""
        bench_path = out / f"rl-stall-{index:02d}.cir"
        log_path = out / f"rl-stall-{index:02d}.log"
        bench_path.write_text(bench)
        run = subprocess.run([simulator, "-b", "-o", str(log_path), str(bench_path)],
                             capture_output=True, text=True, timeout=30)
        log = log_path.read_text() if log_path.exists() else ""
        values = {name: float(value) for name, value in re.findall(
            r"^(i_peak|i_before_off|i_after_deadtime)\s*=\s*([-+\deE.]+)", log, re.M)}
        if run.returncode or len(values) != 3:
            raise SystemExit(f"Simulation failed for case {index}; see {log_path}")
        dc = vbat / (rbat + rpath + rmotor + ron)
        cases.append({"case": index, "vbat_V": vbat, "rbat_ohm": rbat,
                      "rmotor_ohm": rmotor, "inductance_H": inductance,
                      "analytical_stationary_current_A": dc,
                      "simulated": values,
                      "relative_peak_error": abs(values["i_peak"] - dc) / dc,
                      "bench_sha256": hashlib.sha256(bench.encode()).hexdigest()})
    nominal_delay = 499000 / 50000
    # LTC6994 Rev C, NDIV=1, full-temperature accuracy +/-6.2%; RSET +/-0.5%.
    delay_min = nominal_delay * (1 - 0.062) * (1 - 0.005)
    delay_max = nominal_delay * (1 + 0.062) * (1 + 0.005)
    frequency_sensitivity = []
    for hz in (500, 1000, 2000, 10000, 20000):
        fraction = min(1.0, 2 * hz * nominal_delay * 1e-6)
        frequency_sensitivity.append({
            "pwm_Hz": hz,
            "two_deadtime_fraction_at_nominal_delay": fraction,
            "D1_deadtime_loss_W_at_assumed_constant_5A_and_0_55V": 5 * 0.55 * fraction})
    result = {
        "status": "sensitivity_only_not_qualification", "simulation_count": len(cases),
        "inputs": {"source_voltage_V": [1.8, 2.4, 3.2],
                   "assumed_battery_series_resistance_ohm": [0.05, 0.2],
                   "assumed_motor_resistance_ohm": [0.05, 0.2, 0.5],
                   "assumed_motor_inductance_H": [10e-6, 100e-6],
                   "assumed_extra_path_resistance_ohm": 0.01,
                   "assumed_driver_on_resistance_ohm": 0.00286},
        "delay_us": {"nominal": nominal_delay, "static_min": delay_min,
                     "static_max": delay_max,
                     "scope": "NDIV1 error and resistor tolerance only; not a bound on actual switch deadtime"},
        "conduction_5A_W_at_25C": {
            "Q1_Rds_2_86mohm_Vgs4_5V": 25 * .00286,
            "Q2_Si7137DP_Rds3_9mohm_Vgs_minus2_5V": 25 * .0039,
            "candidate_DMP2008_Rds13mohm_Vgs_minus1_8V": 25 * .013},
        "frequency_sensitivity": frequency_sensitivity,
        "max_peak_A": max(x["simulated"]["i_peak"] for x in cases),
        "min_peak_A": min(x["simulated"]["i_peak"] for x in cases),
        "cases_exceeding_5A": sum(x["simulated"]["i_peak"] > 5 for x in cases),
        "max_relative_peak_error": max(x["relative_peak_error"] for x in cases),
        "cases": cases,
        "limitations": [
            "Battery and motor values are hypothetical; they are not a measured load envelope.",
            "No speed, torque, brush commutation, motor back EMF, mutual inductance, or temperature model.",
            "The clamp model is not an SS54-HF model, and the switch is not a SiSS64DN gate model.",
            "No Q2 braking switch, overlapping gates, power sequencing, or hardware current limiting is simulated.",
            "D1 frequency sensitivity assumes 5 A throughout each blanking interval; it is not measured loss.",
            "Results cannot prove any peak/stall rating, thermal safety, or universal motor compatibility."
        ]}
    (out / "motor-stage-sensitivity.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "simulation_count", "min_peak_A",
                     "max_peak_A", "cases_exceeding_5A", "max_relative_peak_error", "delay_us")}, indent=2))


if __name__ == "__main__":
    main()
