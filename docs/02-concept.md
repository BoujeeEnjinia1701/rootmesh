---
doc_id: RMS-PRC-001
title: RootMesh design precis
project: RootMesh
doc_type: Design precis
version: "0.7"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, components, airtime, energy, link budget, cost, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply Amish's decisions (RMS-DDR-001); antenna on the marker rod; numbers checked against RMS-CAL-001; parametric model and drawing RMS-DWG-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Constructable design (RMS-DDR-003) and build plan RMS-BLD-001; costs and installation figures updated; budget treated as a value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Decisions of 2026-10-02 (RMS-DEC-001): first users on US915 (Texas A&M AgriLife Extension as first candidate), R9 cell limit restated on condition, status light kept'
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Follow-ups of 2026-10-02: US915 airtime and link budget, status LED, chosen cell and cost redone; open question on region closed"
---

# RootMesh design precis

RootMesh is a hand-installed soil sensor stake that measures volumetric water content at 150 mm and 300 mm, bulk EC and soil temperature, and reports every 20 min over LoRaWAN to one gateway at the farmhouse, from which an open dashboard shows root-zone depletion against a threshold the grower sets. The sizing note RMS-CAL-001 finds that a stake needs about 2.6 mAh a day including cell self-discharge, so a 0.5 W panel harvests about 58 times that need in the worst month and a 600 mAh LiFePO4 cell alone lasts about 186 days. With the antenna raised to about 1 m on the marker rod, the radio link has 13.5 dB of margin at 1 km. A stake costs $59.00 in parts, and a pilot set of three stakes, a gateway and a steel slot tool for installation costs $281.00. Value-engineering target: USD 300. Estimated cost of the constructable design: USD 281 (USD 19 under the target). Eight of fourteen requirements are met on paper; five are at risk: moisture accuracy (R1), range through tall crops (R5), head and cell temperature in bare, hot soil (R9), pushing the fin into firm dry soil (R10) and probe life (R14). The slot tool brings installation in moist soil within one person's strength (about 386 N); firm dry soil still needs about 1.2 kN. The design was made constructable on 2026-10-01 (RMS-DDR-003, open for Amish's review), and the prototype build plan [RMS-BLD-001](05-build-plan.md) shows how each part is made and fitted; decisions still open are in the design decisions register [RMS-DEC-001](06-design-decisions.md).

![Hero render](../media/hero.png)

*Figure 1. One RootMesh stake installed in soil, shown with the soil cut away, the marker rod with flag and antenna, and a 1.75 m person for scale.*

## How it works

1. **Sense.** Every 20 min the controller switches on the sensors for about 1 s. Two capacitive probes, held edge-on in windows of a printed fin, read water content at 150 mm and 300 mm. A DS18B20 on the fin edge reads soil temperature at about 225 mm. Two stainless electrodes below the fin tip read bulk EC with a short AC burst, so the electrodes do not polarize.
2. **Report.** The LoRaWAN module sends an 11 byte payload (24 bytes on air) at the slowest data rate the link needs, SF10 in the design case, through a sleeve dipole clipped to the top of the marker rod about 1 m above grade, then sleeps.
3. **Collect.** An indoor 8-channel gateway at the farmhouse forwards packets over Wi-Fi to The Things Network's free community server; a local server is a later option.
4. **Decide.** An open-source dashboard converts probe readings to water content with the site calibration, shows depletion between field capacity and the grower's refill point (the FAO-56 "management allowed depletion" idea; [Allen et al. 1998](https://www.fao.org/4/x0490e/x0490e00.htm)), and flags when the shallow or deep reading crosses it. Two depths show whether irrigation water has reached the lower root zone.
5. **Power.** A 0.5 W panel on the sloped head charges a 600 mAh LiFePO4 cell centered about 62 mm below grade, where the soil damps the daily temperature swing.

![Data flow](../media/flow.png)

*Figure 2. Data flow from the root zone to the irrigation decision. Interval, payload and range values are estimates.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Solar panel | 5 V, 0.5 W, about 70 x 50 mm, on a 30 degree slope | Self-cleaning slope sheds rain and dust |
| 2 | Head enclosure | Printed ASA body, 72 mm diameter, bonded over the tube, and a removable cap carrying the panel, sealed by an O-ring and two screws (RMS-DDR-003) | ASA for UV and heat; PETG softens near 70 °C |
| 3 | Controller board | STM32WLE5-class LoRaWAN module (for example Seeed Wio-E5, about $7; [Seeed Studio](https://www.seeedstudio.com/LoRa-E5-Wireless-Module-p-4745.html)) on a carrier with a LiFePO4 solar charger with NTC cut-off, a sensor power switch and the EC drive | One chip for radio and application; decided (RMS-DDR-001, D8) |
| 4 | Antenna and feed | Half-wave sleeve dipole clipped to the top of the marker rod, centered about 1,000 mm above grade, with a 1.2 m RG174 lead through a gland on the head | Decided (RMS-DDR-001, D2); a dipole because a whip on the rod has no ground plane |
| 5 | LiFePO4 cell | 14500, 3.2 V, 600 mAh (about 1.9 Wh), PTC fuse | Inside the tube below grade, in a printed holder standing on the fin spigot |
| 6 | Stake tube | 42 mm OD PVC pressure pipe, 170 mm | Carries the cable and the cell; bonded into the head and over the fin spigot |
| 7 | Sensor fin | Printed carrier 36 x 12 mm in section, 310 mm long, in two glued halves, two windows, wedge tip, collar and spigot at the top | Pushed into undisturbed soil below the 110 mm auger hole |
| 8 | Capacitive moisture probes (2) | v1.2-class boards with the NE555 replaced by a TLC555 and the edges sealed in epoxy, read as frequency | Fixes from the [Cave Pearl Project](https://thecavepearlproject.org/2020/10/27/hacking-a-capacitive-soil-moisture-sensor-for-frequency-output/) |
| 9 | EC electrodes | Two 316 stainless rods, 4 mm diameter, 24 mm apart | Two-electrode, AC excitation; cell constant set by calibration |
| 10 | Temperature probe | DS18B20 in a 6 mm stainless sheath, ±0.5 °C from -10 to 85 °C ([SparkFun](https://www.sparkfun.com/temperature-sensor-waterproof-ds18b20.html)) | Also compensates EC and moisture readings |
| 11 | Marker rod and flag | 1.2 m fiberglass rod, 8 mm, pushed 200 mm into the soil beside the stake | Visibility for machinery and people; carries the antenna |
| 12 | Seals and consumables | O-ring, IP68 glands, ePTFE vent membrane, desiccant, potting | The vent stops daily thermal pumping of about 15 kPa (RMS-CAL-001) |
| 13 | LoRaWAN gateway | Indoor 8-channel gateway with Wi-Fi (The Things Indoor Gateway class, about $79 to $90; [Seeed Studio](https://www.seeedstudio.com/The-Things-Indoor-Gateway-EU-p-4709.html)) | Not in the exploded view; The Things Network for the pilot decided (RMS-DDR-001, D3) |
| 14 | Dashboard | Open-source (for example Node-RED or Grafana) on an existing computer | Not in the exploded view |
| 15 | Slot tool | 32 x 8 mm mild steel flat bar, 650 mm, pointed, with a 20 mm bar handle through a cross hole and a printed 80 mm depth stop; one per set | Pre-cuts the fin and EC rod path; driven with a mallet, then withdrawn (RMS-DDR-002). Not in the exploded view |
| 16 | Head fixings and bonding | Two M3 heat-set inserts, two M3 cap screws with sealing washers, structural epoxy, heat-shrink sleeves, a 56 x 40 mm prototype board for the controller modules | Added for construction (RMS-DDR-003). Not in the exploded view |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view of one stake with numbered callouts matching the BOM. The gateway and dashboard are not shown.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section through the stake: controller board in the head, cell in the tube below grade, moisture probes in the fin windows, temperature probe on the fin edge and EC electrodes below the tip. The marker rod and antenna are omitted for clarity.*

The general arrangement drawing [RMS-DWG-001](../cad/drawings/RMS-DWG-001.pdf) (Rev P2) gives the main dimensions and interfaces from the parametric model `cad/src/model.py`.

## First-order numbers

All values are estimates. They are checked in RMS-CAL-001, whose script `docs/04-calcs/sizing.py` prints every figure below.

### Airtime

Assumptions: 11 byte application payload plus 13 bytes of LoRaWAN overhead, 125 kHz bandwidth, coding rate 4/5, 8 symbol preamble, explicit header and CRC; time on air from the standard Semtech formula.

| Spreading factor | Time on air per uplink | Per day at 20 min (72 uplinks) | Per day at 15 min (96 uplinks) |
| --- | --- | --- | --- |
| SF7 | 62 ms | 4.4 s | 5.9 s |
| SF9 | 206 ms | 14.8 s | 19.8 s |
| **SF10 (design case)** | **371 ms** | **26.7 s** | **35.6 s, over the 30 s fair use limit** |
| SF12 (not allowed on US915) | 1.48 s | 106.8 s | 142.3 s |

At SF10 a 20 min interval fits The Things Network's 30 s per day fair use limit ([The Things Network](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/)); 15 min does not. With adaptive data rate, stakes close to the gateway will use SF7 to SF9 and could report every 10 to 15 min. On US915 there is no duty cycle, but each uplink may stay on a channel for at most 400 ms, so SF10 at 125 kHz (371 ms) is the slowest rate that can be used.

### Energy

Assumptions: sensors powered for 1 s at about 12 mA; microcontroller active 1.5 s at about 4 mA; transmit for the 0.371 s time on air at 120 mA (the Wio-E5 draws 111 mA at +22 dBm; [Seeed Studio](https://wiki.seeedstudio.com/LoRa-E5_STM32WLE5JC_Module/)); two receive windows 0.2 s at 6.7 mA; EC burst 20 ms at 10 mA; sleep 10 µA for the whole board including the charger; 30 % margin; cell self-discharge 3 % a month.

| Quantity | Value (RMS-CAL-001) | Basis | Requirement |
| --- | --- | --- | --- |
| Charge per report | 64.2 mAs | 12 + 6 + 44.5 + 1.3 + 0.2 + 0.2 (status LED) mAs | |
| Reports per day | 72 | Every 20 min | R4 |
| Load per day with margin | 1.98 mAh (6.3 mWh) | (1.29 active + 0.24 sleep) x 1.3 | |
| Self-discharge | 0.60 mAh per day | 3 % of 600 mAh a month | |
| **Daily need** | **2.58 mAh** | | |
| Days on the cell alone | 186 | 600 mAh x 80 % usable / 2.58 mAh | R6 (90 days) met |
| Harvest, 3 sun hours, open sky | 150 mAh per day, 58 times need | 100 mA panel current x 3 h x 50 % for tilt, dust, heat and linear charging | |
| Harvest, 1 sun hour | 50 mAh per day, 19 times need | | R6 met |
| Harvest under a canopy passing 10 % | 15 mAh per day, 5.8 times need | | |

The energy budget has large margin. That also means the panel is not strictly needed: a primary lithium cell would run a stake for years, which is how the Dragino LSE01 works ([Dragino](https://www.dragino.com/products/lora-lorawan-end-node/item/159-lse01.html)). Amish chose solar with a small rechargeable cell (RMS-DDR-001, D1) because it matches the pitch, avoids disposable cells and allows faster reporting. Charging stops below 0 °C, so in frozen ground a stake runs on its 186 days of reserve.

### Radio link

Assumptions: US915 at 915 MHz; stake radiates 20 dBm, with conducted power raised to 21.6 dBm (module maximum +22 dBm) to cover 1.6 dB of lead and connector loss; dipole taken at 0 dBi; gateway sensitivity -132 dBm at SF10 (typical SX12xx figure); 12 dB loss through the farmhouse wall and window; 10 dB allowance for crop foliage and fading; gateway at 3 m; two-ray ground reflection path loss, 40 log d - 20 log(h_t h_r), valid beyond about 115 m for these heights.

| Case | Path loss at 1 km | Loss budget available | Margin |
| --- | --- | --- | --- |
| Stake antenna 0.2 m, indoor gateway (TRL 2 layout) | 124.4 dB | 152 - 12 - 10 = 130 dB | 5.6 dB |
| **Stake antenna 1 m on the marker rod, indoor gateway (decided)** | **110.5 dB** | **130 dB** | **19.5 dB** |
| Stake antenna 0.2 m, outdoor gateway on a 6 m mast | 118.4 dB | 152 - 10 = 142 dB | 23.6 dB |

Raising the antenna to the top of the marker rod (RMS-DDR-001, D2) closes the link at 1 km on paper; at 0 dB margin it would reach about 3.1 km. The remaining risk is a crop taller than the antenna along the path: 50 m of maize or orchard can add about 13 dB and 100 m about 19 dB (Weissberger model), which leaves 0.1 dB at 100 m, so R5 stays at risk until a range walk.

### Measurement

- **Moisture.** Capacitance sensors respond to water, EC and temperature, more so at lower frequencies ([Kizito et al. 2008](https://www.sciencedirect.com/science/article/abs/pii/S0022169408000462)). Site-specific calibration cuts error to about one third of factory calibration ([Datta and Taghvaeian 2023](https://www.sciencedirect.com/science/article/pii/S0378377423000136)). The plan is a two-point field calibration (after irrigation to field capacity, and at a dry reading with a gravimetric sample) plus temperature correction from the DS18B20. Whether ±3 % VWC (R1) is reachable is unverified.
- **Air gaps.** A capacitive probe reads mostly the few millimeters of soil next to its surface, so any gap from installation reads as dry soil. The fin pushes into undisturbed soil below the auger hole to avoid this; contact quality is the largest measurement risk.
- **EC circuit.** Two 4 mm rods at 24 mm pitch with 60 mm exposed give a cell constant of about 0.13 cm⁻¹, so the electrodes read 1,315 Ω at 0.1 dS/m and 33 Ω at 4 dS/m against a 330 Ω reference. A 5 kHz square wave, sampled 10 µs after each edge, keeps polarization error under 1 %, and reading both sides of the reference resistor cancels the drive resistance (RMS-CAL-001, section D).
- **EC.** Bulk EC depends on moisture as well as salinity. Crop salinity thresholds in FAO-29 ([Ayers and Westcot 1985](https://www.fao.org/4/t0234e/t0234e00.htm)) use saturated-paste EC, so the dashboard should show EC as a trend and a pore-water estimate, not as a direct threshold. Readings are corrected to 25 °C at about 2 % per °C.

### Cost

| Group | Indicative cost | Requirement |
| --- | --- | --- |
| One stake (items 1 to 12, 16 and 17) | $59.15 | R12 ($60) met |
| Three stakes | $177.45 | |
| Gateway (item 13) | $90.00 | |
| Slot tool (item 15) | $14.00 | |
| **Pilot set** | **$281.45** | R12 ($300) met; USD 18.55 under the value-engineering target |
| Reference: Dragino SE01 node | about $151 to $170 per point ([Choovio](https://www.choovio.com/product/se01-lb-lorawan-soil-moisture-ec-sensor/)) | |

## Key design choices

Amish decided the choices below on 2026-09-25 by approving the TRL 2 recommendations (RMS-DDR-001). None is still "proposed".

- **Solar with a rechargeable LiFePO4 cell** (D1, D5): a 0.5 W panel and a 600 mAh LiFePO4 cell, rather than a primary Li-SOCl2 cell. Keeps the pitch and avoids disposable cells; adds a charger, a panel to keep clean and a cell that must not charge when frozen. LiFePO4 tolerates heat better than Li-ion and is less prone to thermal runaway.
- **Two moisture depths on one fin** (D6): 150 mm and 300 mm, to show whether water reached the lower root zone, at about $3 extra per stake.
- **Modified hobby capacitive probes** (D7): keeps the stake near $56; accuracy and life are the risks (R1, R14). A commercial reference sensor is to be borrowed for calibration later.
- **Wio-E5 (STM32WLE5) controller** (D8): one module for radio and application.
- **LoRaWAN on The Things Network for the pilot** (D3): free and simple; the fair use limit sets the 20 min interval at SF10, and a TTIG-class gateway works only with The Things Stack. A Raspberry Pi gateway with a local ChirpStack server stays a documented later option.
- **Indoor gateway, antenna on the marker rod** (D2): a sleeve dipole at about 1 m on the rod, fed by a 1.2 m lead, gives 19.5 dB margin at 1 km on US915 for $7 a stake. It adds a cable and a snag point; the rod is flexible and flagged.
- **Default interval 20 min** (D9): fits the fair use limit at SF10; faster with adaptive data rate near the gateway.
- **Budget read as a pilot set** (D4): the USD 300 value-engineering target covers three stakes and one gateway.
- **Steel slot tool for installation** (RMS-DDR-002): a pointed 32 x 8 mm steel blade, driven with a mallet down the auger hole and withdrawn, pre-cuts the fin path so the fin only widens the slot. Push force falls from 517 N to 376 N in moist loam and from 1,778 N to 1,216 N in firm dry loam (RMS-CAL-001 v0.2). Steel rather than a printed blade, because a printed blade would not survive firm soil.
- **Cell position kept at 62 mm** (RMS-DDR-002): a deeper cell was checked; in the constructable design the cell already sits as deep as fits above the fin spigot (62 mm, peak 46.8 °C in bare, hot soil), and meeting 40 °C would need about 163 mm, where the upper probe sits.

Decided by Amish on 2026-10-02 (RMS-DEC-001): the first users are a US university extension program with a research farm, on US915, with Texas A&M AgriLife Extension as the first candidate to approach; the cell limit of R9 is restated to the chosen cell's rated discharge range, provided its datasheet rates discharge to 55 °C or more, with charging still blocked above 45 °C, and otherwise a printed shade skirt is added; a green status light is kept on the head, blinking briefly after each uplink and on a magnet or button wake only, once its charge is in the energy budget. The link, airtime and power figures above are for US915 and include the status light (RMS-CAL-001 v0.5). The chosen cell is an IFR14500EC class cell, whose datasheet rates discharge from -20 to +60 °C, so no shade skirt is added.

## Safety

> **Safety:** Each stake holds a small lithium cell in a sealed enclosure buried in wet soil and exposed to sun, frost and machinery. The hazards are small but real.

- **Lithium cell.** A LiFePO4 cell of about 1.9 Wh is far less energetic than a phone battery, but a shorted or crushed cell can still overheat and vent. Fuse the cell (PTC), use a charger with an NTC input that blocks charging below 0 °C and above 45 °C, never charge a swollen or water-damaged cell, and do not leave stakes with cells in a closed hot vehicle. Plated lithium from charging below freezing can cause internal shorts later.
- **Sealed enclosure pressure.** A sealed head in sun warms from about 20 to 64 °C each day, a swing of about 15 kPa that would pump moisture past the seals. The head carries an ePTFE vent membrane and a desiccant.
- **Cell temperature.** In bare, hot soil the cell can reach about 47 °C (RMS-CAL-001). The charger's 45 °C cut-off stops charging, but check that the cell holder and fuse are rated for it, and never leave a stake in a closed vehicle.
- **Machinery and trips.** A stake struck by a tractor, mower or tiller can be thrown or can damage the implement; a low stake is a trip hazard. The flagged marker rod is part of the design, and stakes should be pulled before tillage. The antenna lead on the rod is a snag point; tape it to the rod.
- **Installation effort.** Pushing the fin into firm dry soil can take about 1.8 kN, or about 1.2 kN after the slot tool (RMS-CAL-001). Do not hammer on the head or stand on it; install after irrigation or pre-wet the hole, and cut the slot first.
- **Slot tool.** A pointed steel blade struck with a mallet: wear eye protection and gloves, keep feet clear of the point, keep the depth-stop collar fitted, and store the tool with a tip cover.
- **Sharp parts.** The fin tip and stainless electrodes are pointed; handle and store with tip covers, and keep away from children and livestock.
- **Chemicals and electrical.** Epoxy potting and conformal coating need gloves and ventilation. The stake runs at 3.2 V and carries no shock hazard; the gateway plugs into mains indoors through its own certified USB supply.
- **Data is not advice.** Readings inform a grower's decision. A failed or badly calibrated stake can read wet when the soil is dry, so growers should keep checking the crop, especially while the system is new.

## Open questions after TRL 3

- First users and region for co-design: decided on 2026-10-02, a US university extension program on US915, first candidate Texas A&M AgriLife Extension. The link budget and airtime for US915 are still to be worked.
- Can the moisture calibration reach ±3 % VWC in two soils (R1)? Needs a gravimetric calibration at TRL 4.
- Does the link hold through tall crops at 1 km (R5)? Needs a range walk at TRL 4.
- A deeper cell cannot keep the cell under 40 °C in bare, hot soil (R9). Decided on 2026-10-02: the cell limit is restated to the chosen cell's rated discharge range if its datasheet rates discharge to 55 °C or more; otherwise the soil around the head is shaded with a printed skirt.
- The slot tool brings moist soil within one person's strength on paper, but not firm dry soil (R10). A timed installation trial is TRL 4 work, on hold.
- Which edge seal lets the hobby probes last 12 months buried (R14)?

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
