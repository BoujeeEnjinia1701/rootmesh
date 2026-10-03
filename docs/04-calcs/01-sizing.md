---
doc_id: RMS-CAL-001
title: RootMesh sizing calculations
project: RootMesh
doc_type: Calculation
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (airtime, energy, radio link, EC circuit, sensing geometry, thermal and sealing, installation force, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); slot tool force case, cell depth check for R9, pilot set cost with the slot tool
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: Re-run for the constructable design (RMS-DDR-003); push depth, head air volume, cell depth check and cost updated; budget treated as a value-engineering target
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: R9 target in the requirement table restated as decided by Amish on 2026-10-02; no number re-run
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Re-run for the 2026-10-02 decisions: US915 link budget and airtime, status LED charge, cell chosen (IFR14500EC class, discharge to 60 C), BOM line 17; no requirement changed status"
---

# RootMesh sizing calculations

On paper, RootMesh meets eight of its fourteen requirements, has five at risk, and has one that cannot be verified at TRL 3. No requirement is shown to be missed outright. The five at risk are moisture accuracy (R1), which depends on soil contact and calibration; range (R5), where raising the antenna to 1 m on the marker rod gives 19.5 dB of margin at 1 km on US915, but a crop taller than the antenna can take 13 to 19 dB of it; temperature range (R9), where the head can reach about 64 °C and the cell about 47 °C in bare, hot soil; installation (R10), where pushing the fin into firm dry loam needs about 1.8 kN, more than one person can lean on it; and probe life (R14). Version 0.2 adds the two design responses Amish accepted on 2026-09-25 (RMS-DDR-002): a steel slot tool cuts the push force in moist loam from 526 N to 386 N, within one person's strength, but firm dry loam still needs about 1.2 kN; and a check of a deeper cell shows that no cell position that fits above the fin keeps the cell under 40 °C in bare, hot soil. The calculations also corrected three TRL 2 figures: days on the cell alone fall from about 240 to about 186 once LiFePO4 self-discharge is counted, the harvest ratio falls from about 70 to about 58 times daily need, and the pilot set rises from about $246 to $256.50 with the antenna feed and a vent ($266.50 with the slot tool added in v0.2, and $281.00 for the constructable design of v0.3, and $281.45 with the status LED added in v0.5, $18.55 under the $300 value-engineering target). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B4], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not replace measurement of the cell temperature in the field, a range walk, or checks of the charger's temperature cut-off. The stake holds a lithium cell; see RMS-PRC-001, Safety.

## Scope and method

Version 0.3 re-runs every figure for the constructable design of RMS-DDR-003: the fin is now pushed in from a collar 110 mm below grade, the head body has a thicker wall, the cell stands on a holder, and the BOM carries the parts added for construction. No requirement changed status.

The note checks every requirement in RMS-REQ-001 v0.5 against the design in RMS-PRC-001 v0.5 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and `derived()`, so depths, heights, fin section and electrode geometry are the ones in the STEP files and in drawing RMS-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The reference case is one stake in loam, sensing at 150 mm and 300 mm, reporting every 20 min at SF10 to an indoor gateway 1 km away, with 3 peak sun hours on the panel in the worst month.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Payload | 11 application bytes plus 13 bytes of LoRaWAN overhead, 24 bytes on air | Two moisture counts, EC, temperature, cell voltage, status |
| Radio settings | 125 kHz, coding rate 4/5, 8 symbol preamble, explicit header, CRC; low data rate optimization at SF11 and SF12 | Semtech time-on-air formula |
| Fair use | 30 s of uplink airtime per node per day | [The Things Network, "Duty Cycle"](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/) |
| Module currents | Transmit 111 mA at +22 dBm, receive 6.7 mA, sleep 2.1 µA, -40 to 85 °C | [Seeed Studio, Wio-E5 module wiki](https://wiki.seeedstudio.com/LoRa-E5_STM32WLE5JC_Module/) |
| Energy per report | Transmit 120 mA for the time on air (datasheet rounded up for the carrier); receive 6.7 mA for 0.2 s; sensors 12 mA for 1 s; core 4 mA for 1.5 s; EC burst 10 mA for 20 ms; board sleep 10 µA; 30 % margin | Order-of-magnitude figures to confirm on hardware |
| Cell | 600 mAh LiFePO4, 3.2 V, 80 % usable, self-discharge 3 % per month | Typical 14500 LiFePO4 cells |
| Harvest | 0.5 W, 5 V panel gives 100 mA at 1,000 W/m²; 50 % derate for tilt, dust, heat and linear charger headroom | Linear charger passes panel current, not power |
| Link | 915 MHz (US915); 20 dBm radiated (module maximum +22 dBm conducted, less 1.6 dB of coax; the US915 limit is far higher), coax loss made up by conducted power; gateway sensitivity -132 dBm at SF10; 12 dB wall loss; 10 dB foliage and fading allowance; gateway antenna 3 m; two-ray path loss 40 log d - 20 log(h_t h_r) | Typical SX12xx figures; a range walk would replace this at TRL 4 |
| Foliage | Weissberger model for a crop taller than the antenna along the path | Standard empirical vegetation model |
| EC | Two parallel 4 mm rods, 24 mm pitch, 60 mm exposed; 330 Ω reference; 12-bit ADC; double layer 10 µF/cm² | Parallel-cylinder cell constant; low-end double-layer value is the conservative case |
| Thermal | Panel NOCT 45 °C; head interior at air temperature plus 0.6 of the panel rise; soil diffusivity 0.5 × 10⁻⁶ m²/s with a daily sine at the surface | Engineering estimates |
| Installation | Cone resistance 0.5 MPa and shaft friction 10 kPa in moist loam; 2.0 MPa and 30 kPa in firm dry loam; one person leaning gives about 500 N | Typical penetrometer ranges for loam |

## A. Airtime (R4)

A 24 byte uplink at SF10 takes 371 ms on air [A2-SF10]. At the 20 min default, 72 uplinks use 26.7 s a day, inside the 30 s limit. A 15 min interval at SF10 would use 35.6 s and is not allowed. The 11 byte application payload is also the most US915 allows at SF10 (DR0), so the payload fits both regional plans [A1].

*Table 2. Time on air and the shortest interval inside 30 s per day [A2].*

| Spreading factor | Time on air | Per day at 20 min | Per day at 15 min | Shortest interval |
| --- | --- | --- | --- | --- |
| SF7 | 62 ms | 4.4 s | 5.9 s | 3.0 min |
| SF8 | 113 ms | 8.1 s | 10.9 s | 5.4 min |
| SF9 | 206 ms | 14.8 s | 19.8 s | 9.9 min |
| **SF10** | **371 ms** | **26.7 s** | **35.6 s** | **17.8 min** |
| SF11 (not allowed on US915) | 823 ms | 59.3 s | 79.0 s | 39.5 min |
| SF12 (not allowed on US915) | 1,483 ms | 106.8 s | 142.3 s | 71.2 min |

US915 has no duty-cycle limit, but each uplink may stay on a channel for at most 400 ms; SF10 at 125 kHz takes 371 ms, so DR0 is the slowest rate that can be used and SF11 and SF12 at 125 kHz are not allowed [A3]. Fair use, not the radio rules, then sets the airtime. With adaptive data rate, stakes that reach the gateway at SF9 or faster can report every 10 to 15 min. At SF11 and SF12 the 20 min default breaks the fair use limit, so a stake that needs those rates must report every 40 to 72 min; this is why the design case keeps the link at SF10 or faster (section C).

## B. Energy (R6, R7)

One report costs 64.2 mAs, most of it the transmission (44.5 mAs) [B1]. The status LED (decision 6 of 2026-10-02) is a green 5 mm LED behind a 560 ohm resistor on 3.3 V, which draws 2.14 mA; one 100 ms blink after each uplink adds 0.21 mAs to the report, and three blinks on each of an assumed five magnet or button wakes a day add 3.2 mAs a day [B1b]. With 72 reports, the wake blinks, sleep and a 30 % margin the load is still 1.98 mAh (6.3 mWh) a day [B2]; adding 0.60 mAh a day of self-discharge gives a daily need of 2.58 mAh [B3]. The 600 mAh cell alone then lasts 186 days (242 days if self-discharge were ignored, which is the TRL 2 figure of about 240) [B4].

*Table 3. Harvest against daily need of 2.58 mAh [B5].*

| Case | Harvest | Ratio to need |
| --- | --- | --- |
| 3 sun hours, open sky | 150 mAh/day | 58.1 |
| 1 sun hour, open sky (R6 case) | 50 mAh/day | 19.4 |
| 3 sun hours, canopy passing 10 % | 15 mAh/day | 5.8 |

The cell stores 1.92 Wh, inside the 2 Wh limit, with an NTC window of 0 to 45 °C and a PTC fuse [B6]. Because charging stops below 0 °C, a stake in frozen ground runs on the cell alone; 186 days covers a temperate winter.

## C. Radio link (R5)

With the antenna at 1 m on the marker rod (RMS-DDR-001, D2), path loss at 1 km is 110.5 dB against an available 130 dB on US915, a margin of 19.5 dB after the 10 dB foliage and fading allowance [C2-2]. The TRL 2 case with the antenna 0.2 m above grade has 5.6 dB [C2-1], and an outdoor gateway on a 6 m mast would have 23.6 dB [C2-3]. At 0 dB margin the decided layout reaches about 3.1 km [C3]. The two-ray model holds beyond about 115 m for these heights. The margins are 6 dB higher than the 868 MHz figures of version 0.4 (13.5, -0.4 and 17.6 dB) because the stake now radiates 20 dBm instead of 14 dBm; the loss at 1 km is unchanged because the model has no frequency term.

To keep 20 dBm radiated through 1.6 dB of lead and connectors, the module transmits at 21.6 dBm, just inside its +22 dBm [C1]. The half-wave sleeve dipole is cut to 164 mm for 915 MHz (a half wave is 163.9 mm in free space [C0]; it was 172 mm at 868 MHz). A half-wave sleeve dipole replaces the TRL 2 quarter-wave whip, because a whip on a rod has no ground plane; the budget takes it at 0 dBi although a dipole gives about 2 dBi.

The risk is tall crops. If the path runs through a crop taller than 1 m, such as maize or orchard rows, Weissberger's model gives 7.5 dB for 20 m of foliage, 12.9 dB for 50 m and 19.4 dB for 100 m [C4]. Beyond about 33 m of tall crop the 10 dB allowance is used up and the 19.5 dB margin starts to go [C5]; at 100 m of tall crop it is down to 0.1 dB. Short vegetable crops leave the antenna clear. R5 is therefore **at risk** in tall crops until a range walk (TRL 4) measures it.

## D. EC circuit (R3)

The two rods form a cell with a constant of about 13.1 m⁻¹ (0.131 cm⁻¹) from the parallel-cylinder formula; end effects will lower it, and calibration in KCl standards sets the real value [D1]. With a 330 Ω reference resistor the electrode resistance runs from 1,315 Ω at 0.1 dS/m to 33 Ω at 4 dS/m.

*Table 4. EC divider resolution with a 12-bit ADC [D2].*

| Bulk EC | Electrode resistance | Divider ratio | 1 LSB as share of reading |
| --- | --- | --- | --- |
| 0.1 dS/m | 1,315 Ω | 0.799 | 0.15 % |
| 1 dS/m | 131 Ω | 0.285 | 0.12 % |
| 4 dS/m | 33 Ω | 0.091 | 0.30 % |

Electrode polarization is the main circuit error. Each electrode has about 75 µF of double-layer capacitance; driven with a 5 kHz square wave and sampled 10 µs after each edge, polarization adds 2.4 mV to a 299 mV reading at 4 dS/m, or 0.8 % [D3]. The design samples late in a half period at its peril: at the end of a 1 kHz half period the same error would be about 40 % [D3b]. The GPIO drive resistance (tens of ohms) is comparable to the electrode at high EC, so the ADC reads both sides of the reference resistor to cancel it. Temperature correction at 2 % per °C with a ±0.5 °C sensor adds ±1.0 % [D4]. The circuit error stays under 2 % across the range, well inside ±10 %, so R3 is met on paper. The soil reading itself, which depends on moisture and contact, is a TRL 4 question.

## E. Moisture and temperature sensing (R1, R2)

The probe windows are centered 150 mm and 300 mm below grade and the blades are 80 mm long, so the probes read 110 to 190 mm and 260 to 340 mm [E1]. The depth part of R1 is met by geometry, and the repeatability of ±25 mm depends on the installer seating the head at grade. The ±3 % VWC accuracy depends on soil contact and on the two-point site calibration and cannot be shown by calculation [E2], so R1 stays **at risk**. The DS18B20 sits at 225 mm and is specified ±0.5 °C from -10 to 85 °C, which covers R2 [E3].

## F. Thermal and sealing (R8, R9)

In full sun at 45 °C air the panel reaches about 76 °C and the head interior about 64 °C [F1], above the 60 °C in R9. The Wio-E5 is rated to 85 °C and ASA softens near 100 °C, so the parts survive, but the requirement's range is exceeded. The cell sits 62 mm below grade, where the daily swing is damped with a depth scale of 117 mm.

*Table 5. Cell temperature at 62 mm depth [F2].*

| Case | Surface range | Cell range |
| --- | --- | --- |
| Bare soil, hot summer | 15 to 55 °C | 23.2 to 46.8 °C |
| Under a crop canopy, summer | 20 to 36 °C | 23.3 to 32.7 °C |
| Bare soil, cold winter | -7 to 3 °C | -4.9 to 0.9 °C |

In bare, hot soil the cell exceeds the 40 °C limit of R9 by about 7 °C. The charger's 45 °C cut-off stops charging for part of the afternoon but does not stop the cell from warming. R9 is **at risk**. Decided on 2026-10-02: the limit at the cell is restated to the chosen cell's rated discharge range. The cell is an IFR14500EC class LiFePO4 cell, whose datasheet rates discharge from -20 to +60 °C and charge from 0 to +60 °C [F5]. That is above the 55 °C the decision asks for and 13 °C above the hottest cell estimate of 47 °C, so the printed shade skirt is not added. Charging stays blocked above 45 °C by the charger. The head still reaches about 64 °C against its 60 °C limit, so R9 stays **at risk** for the head.

Amish accepted the recommendation to check a deeper cell (RMS-DDR-002). To stay at or below 40 °C in bare, hot soil the cell center would have to sit about 163 mm deep [F4]. In the constructable design (RMS-DDR-003) the cell stands in a holder on the fin spigot, with the holder base 87 mm below grade, and the upper probe window starts at 110 mm, so the deepest cell center that fits is 62 mm, where the cell already sits (46.8 °C). Version 0.2 found about 65 mm (46.5 °C) before the holder was added. A deeper cell alone therefore cannot meet R9 without moving the 150 mm probe that R1 fixes, and the cell stays at 62 mm. The remaining responses, shading the soil around the head or restating the cell limit to the chosen cell's rated discharge range while charging stays blocked above 45 °C, are decided on 2026-10-02 (RMS-DDR-002, P1; see above).

A sealed head holds about 272 cm³ of air (308 cm³ before the body wall was thickened to 5 mm in v0.3). Heating from 20 to 64 °C raises its pressure by 15.1 kPa, three times the 4.9 kPa of 0.5 m immersion [F3]. Daily pumping of that size would work water past the seals, so an adhesive ePTFE vent membrane is added to the head (BOM line 12). Whether the head reaches IP67 and the buried part IP68 needs an immersion test, so R8 is **not verifiable at TRL 3**.

## G. Installation and geometry (R10, R11)

The installer augers a 50 mm hole 110 mm deep, to the bottom of the fin collar that the tube sits on (RMS-DDR-003), then pushes the fin 310 mm into undisturbed soil (340 mm with the tip). In moist loam after irrigation this takes about 526 N (54 kgf), about what one person can lean on the head (about 500 N) [G1, G2]. In firm dry loam it takes about 1,807 N (184 kgf), which one person cannot do [G1]. Without help, R10 is at risk.

Amish accepted the slot tool suggestion (RMS-DDR-002). A printed blade would not survive firm soil, so the tool is a 32 x 8 mm mild steel flat bar ground to a point at the EC tip depth (485 mm), with a 20 mm round bar handle through a cross hole, held by two shaft collars, and a printed depth stop clamped by a thumb screw that rests on grade (BOM line 15, model `slot-tool.step`; fixings from RMS-DDR-003). The installer augers the 50 mm hole, drives the blade down the hole with a mallet, so the blows go into the tool rather than the stake head, withdraws it and then pushes the fin in. The EC rods (4 mm) pass inside the 8 mm slot, and the fin only widens the slot, displacing 2 mm of soil on each face, which keeps the probes in contact with undisturbed soil. Taking the tip resistance on the residual 176 mm² and keeping shaft friction unchanged (conservative), the fin needs about 386 N in moist loam and about 1,245 N in firm dry loam [G4, G5]. Moist soil is now within one person's 500 N with 23 % margin; firm dry loam is not. R10 stays **at risk**, and the installation guidance is to pre-wet the hole in dry soil.

The head top is 171 mm above grade, the antenna spans 914 to 1,086 mm on the flexible rod, and the rod top is 1,000 mm with the flag centered at 840 mm [G3]. R11, as redefined for the antenna on the rod, is met.

## H. Cost (R12, R13, R14)

From `bom/bom.csv`, one stake costs $59.15, three cost $177.45, and with the $90 gateway and the $14 slot tool the pilot set is $281.45. Value-engineering target: USD 300. Estimated cost of the constructable design: USD 281.45 (USD 18.55 under the target) [H1]. The $3.50 added per stake since v0.2 is the parts that make the design buildable (RMS-DDR-003): the two-part head, the fin halves, and BOM line 16 (inserts, cap screws, sealing washers, epoxy, sleeves and the prototype board); BOM line 17 (status LED and resistor, $0.15 per stake) was added on 2026-10-02. The per-stake figure in R12 ($60) is met by $0.85. All prices are indicative. R13 is met by design with The Things Network community server and a local open dashboard with CSV export. R14 (12 months buried) depends on the epoxy seal of the probe edges and on the stainless electrodes and cannot be shown by calculation; it stays **at risk**.

## Results

*Table 6. Requirement status against RMS-REQ-001 v0.5 (from the script's results table).*

| ID | Value | Target | Status |
| --- | --- | --- | --- |
| R1 | Depths 150 and 300 mm by model; accuracy unverified | 150 and 300 mm (±25 mm); ±3 % VWC after site calibration | At risk |
| R5 | 19.5 dB margin at 1 km on US915; tall crops take 13 to 19 dB, leaving 0.1 dB at 100 m of crop | 90 % of uplinks at 1 km, indoor gateway, antenna on the marker rod | At risk |
| R9 | Head about 64 °C at 45 °C air; cell up to 47 °C in bare hot soil, inside the chosen cell's -20 to +60 °C discharge rating [F5] | -10 to 60 °C at the head; the cell's rated discharge range, 55 °C or more, charging blocked above 45 °C (restated 2026-10-02) | At risk (head) |
| R10 | With the slot tool 386 N in moist loam, 1,245 N in firm dry loam (without: 526 N, 1,807 N) | One person, 50 mm auger, 15 min; depths ±25 mm | At risk |
| R14 | Sealed probes, 316 stainless electrodes; life unverified | 12 months buried | At risk |
| R8 | 15 kPa daily thermal pumping without a vent; vent added | Head IP67; buried IP68 at 0.5 m; UV-stable | Not verifiable at TRL 3 |
| R2 | ±0.5 °C, -10 to 85 °C, at 225 mm | ±0.5 °C from -10 to 60 °C at about 225 mm | Met |
| R3 | Circuit error under 2 % from 0.1 to 4 dS/m | 0 to 4 dS/m, ±10 % or ±0.1 dS/m | Met |
| R4 | 26.7 s/day at SF10 and 20 min | 20 min default; 30 s/day or less | Met |
| R6 | 19 times need at 1 sun hour; 186 days dark | Energy-neutral at 1 sun hour; 90 days dark | Met |
| R7 | LiFePO4, 1.92 Wh, NTC 0 to 45 °C, PTC fuse | LiFePO4, 2 Wh or less, fused, charge 0 to 45 °C | Met |
| R11 | Head 171 mm; flag 840 mm, rod 1,000 mm | Rigid head 300 mm or less; marker 1 m or more | Met |
| R12 | $59.15 per stake; $281.45 pilot set (USD 18.55 under the value-engineering target) | $60 per stake; $300 pilot set | Met |
| R13 | TTN community server, local dashboard, CSV | No paid subscription; CSV export; open dashboard | Met |

Counts: met 8, at risk 5, not verifiable at TRL 3 1, not met 0.

## Corrections to the TRL 2 documents

- Days on the cell alone: about 240 at TRL 2, now 186 with self-discharge.
- Harvest to use ratio: about 70 times at TRL 2, now 58 times the daily need (including self-discharge) at 3 sun hours, 19 times at 1 sun hour and 5.8 times under a canopy.
- Link margin with the antenna on the marker rod: about 14 dB at TRL 2, 13.5 dB at 868 MHz in version 0.4, now 19.5 dB on US915 at 20 dBm radiated with 1.6 dB of lead loss made up by conducted power.
- Pilot set cost: about $246 at TRL 2, now $256.50 ($266.50 with the slot tool from v0.2); one stake about $52, now $55.50.
- The whip antenna becomes a half-wave sleeve dipole, because a whip on the rod has no ground plane.

## Changes in version 0.2

- R10: slot tool (BOM 15) added; push force in moist loam 517 N to 376 N, in firm dry loam 1,778 N to 1,216 N. Status unchanged (at risk).
- R9: deeper cell checked; the deepest position that fits gives 46.5 °C against 46.8 °C, so the cell stays at 62 mm. Status unchanged (at risk).
- R12: pilot set $256.50 to $266.50 with the slot tool; headroom $43.50 to $33.50. Status unchanged (met).

## Changes in version 0.3

Re-run on 2026-10-01 for the constructable design (RMS-DDR-003). No requirement changed status.

- R10: the auger hole is now 110 mm deep (to the fin collar) and the fin is pushed 310 mm into undisturbed soil instead of 300 mm. Push force with the slot tool 376 N to 386 N in moist loam, 1,216 N to 1,245 N in firm dry loam; without it 517 N to 526 N and 1,778 N to 1,807 N. Still at risk.
- R9: the cell now stands in a holder on the fin spigot; the deepest center that fits is 62 mm (46.8 °C), where it already sits. Still at risk.
- R8: head air 308 cm³ to 272 cm³ with the 5 mm body wall; the pressure rise is unchanged at 15.1 kPa. Still not verifiable at TRL 3.
- R12: one stake $55.50 to $59.00, pilot set $266.50 to $281.00, USD 19 under the USD 300 value-engineering target. Still met.

## Changes in version 0.5

Re-run on 2026-10-02 for the decisions of that day (RMS-DEC-001). No requirement changed status.

- R5: US915 at 915 MHz, 20 dBm radiated. Margin at 1 km 13.5 dB to 19.5 dB; tall crops take 13 to 19 dB, leaving 0.1 dB at 100 m. Still at risk. Dipole cut from 172 to 164 mm [C0].
- R4: the 868 MHz duty-cycle line is replaced by the 400 ms dwell limit; SF10 takes 371 ms and stays the slowest rate. Still met.
- R6: the status LED adds 0.21 mAs per report and 3.2 mAs a day for wakes [B1b]; the daily need is unchanged to the digit shown (2.58 mAh) and the cell lasts 186 days. Still met.
- R9: the cell is chosen, IFR14500EC class, discharge -20 to +60 °C [F5]; no shade skirt. The head stays over 60 °C, so still at risk.
- R12: one stake $59.00 to $59.15, pilot set $281.00 to $281.45, USD 18.55 under the USD 300 value-engineering target. Still met.
