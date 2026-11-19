# Design Data Model

This model defines the records and acceptance checks needed to move from candidate research to a fabrication package. Values remain open until supported by a manufacturer document, measurement, or approved test.

## Entities

### Motor Candidate

Fields: manufacturer, model/MPN, availability evidence, motor topology, can dimensions, mount geometry, shaft diameter/length/projection/sides, connector and lead exit, sensor type and pinout, rated voltage, KV or back-EMF constant, pole pairs, maximum mechanical/electrical speed, phase resistance, phase inductance, continuous/peak phase current, mass, source documents, revision/date, confidence.

Validation: drawing or measured dimensions must match the selected chassis/mount, pinion and gear. Controller limits must cover operating voltage, electrical speed, phase current, and winding parameters. Unknown critical fields block design freeze.

### Chassis and Gear Set

Fields: manufacturer/model, chassis revision, stock motor mount dimensions, battery bay dimensions, gear/pinion identifiers and ratio, motor shaft/pinion interface, cover and body clearances, ground clearance, available PCB envelope, allowed modification locations, modification method/reason, source or measurement record.

Validation: demonstrate installation on a commercially sold chassis. Prefer stock features. Record each cutting/drilling operation and show why component choice or layout cannot avoid it. Fully custom chassis requires user approval.

### Battery Pack

Fields: chemistry, cell count and arrangement, dimensions, nominal/full/cutoff voltage, continuous/transient current, connector/polarity, protection circuitry, protection trip/recovery, charging method, source/manufacturer, mass.

Validation: full voltage stays within controller and component operating ratings; low voltage allows intended operation or triggers safe stop; current capability covers measured/tested load with margin; battery protection and braking energy paths are understood. Charging stays external unless separately specified.

### Commutation Controller

Fields: architecture (integrated IC, separate ESC, or XIAO plus gate driver), device/MPN, commutation type, sensor support, operating voltage, recommended electrical-speed range, motor R/L range, peak and continuous current evidence, startup method, low-speed behavior, speed-command protocol, stop/coast/brake options, enable/fault signals, protections, thermal implementation, firmware/configuration revision.

Validation: demonstrate compatibility with the selected motor and battery, loaded startup, safe outputs through reset/command loss, fault shutdown, and requested stop semantics. Peak ratings are not treated as continuous ratings.

### XIAO Command Interface

Fields: signal names, electrical levels, protocol, PWM rate/range or serial baud/format, speed mapping, enable polarity/default, timeout, stop/coast/brake semantics, fault input, optional telemetry, boot/reset behavior, test result under concurrent BLE/IMU operation.

Validation: match the interface contract; default remains disabled until a valid command is accepted; stale/invalid command and fault cause the documented safe state without automatic restart.

### Controller PCB and Power Budget

Fields: revision, board outline and thickness, stackup/copper, input and logic rails, switching devices, current sense/protection, thermal path, DC-link capacitance/overvoltage strategy, connector ratings, antenna/USB separation, measured/tested current and temperature envelopes.

Validation: electrical rules, pinout, component derating, fault response, thermal/current estimates, and mechanical envelope are reviewed against the selected motor/chassis/battery. Do not inherit the 003 board’s outline, current targets, connector, or power assumptions without new evidence.

### Manufacturing Package and Test Evidence

Fields: source revision/commit, schematic/PCB files, Gerber, drill, BOM with approved MPNs and sourcing status, CPL, assembly notes, panelization, fabrication stackup, inspection criteria, test limits, file hashes, manufacturer DFM/quote, known exceptions, approval record.

Validation: all files refer to one revision; BOM and CPL references/rotation/side/pin-1 agree with PCB; no unapproved substitute; DRC/ERC and applicable design reviews are recorded; manufacturer answers outstanding DFM questions before order release.

## Relationships

- One project target contains one selected chassis/gear set and one selected motor for the first prototype.
- The selected motor, battery, and commutation controller form one jointly validated operating envelope.
- The XIAO interface commands the commutation controller and receives fault/status indications where supported.
- The controller PCB implements the power and signal connection between the battery, motor, controller, and XIAO.
- A manufacturing package is generated from one immutable design revision and links its validation/test evidence.
