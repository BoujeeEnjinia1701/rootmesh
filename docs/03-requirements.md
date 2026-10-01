---
doc_id: RMS-REQ-001
title: RootMesh requirements
project: RootMesh
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-10-01'
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
  change: First measurable requirements for TRL 2, with concept status for each
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply Amish's decisions (RMS-DDR-001); redefine R4, R5, R11, R12 and R13; status from RMS-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Figures for the constructable design (RMS-DDR-003, RMS-CAL-001 v0.3); budget treated as a value-engineering target; no status changed
---

# RootMesh requirements

These requirements reflect Amish's decisions of 2026-09-25 (RMS-DDR-001 and RMS-DDR-002) and the constructable design of RMS-DDR-003 and are checked by calculation in RMS-CAL-001. Targets are not yet validated with growers and will be revised after user input (see RMS-PRB-001; first users are still open). Nothing has been built or measured, so "met" means met on paper, by calculation or by a datasheet.

**Reference case:** one stake in a loam field, sensing at 150 and 300 mm, reporting every 20 min at SF10 to an indoor gateway about 1 km away, with the antenna at about 1 m on the marker rod, in a region with 3 peak sun hours per day in the worst month.

*Table 1. Requirements and TRL 3 status (RMS-CAL-001, Table 6).*

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | Measure volumetric water content at two root-zone depths | 150 mm and 300 mm below grade (±25 mm); 5 to 50 % VWC; ±3 % VWC after a site-specific calibration | Model geometry; later gravimetric calibration in two soils | **At risk**: depths met by the model; accuracy depends on probe contact and calibration |
| R2 | Measure root-zone soil temperature | ±0.5 °C from -10 to 60 °C at about 225 mm depth | DS18B20 datasheet; model geometry | Met (datasheet; 225 mm in the model) |
| R3 | Measure bulk soil electrical conductivity | 0 to 4 dS/m; ±10 % or ±0.1 dS/m, whichever is larger, after calibration in standard solutions; reported at 25 °C | Circuit calculation; later bench test in KCl solutions and soil | Met on paper: circuit error under 2 % (RMS-CAL-001, D) |
| R4 | Report often enough for daily irrigation decisions | Every 20 min by default (RMS-DDR-001, D9); adjustable from 10 to 60 min where the spreading factor keeps uplink airtime at 30 s or less per day; the default fits at SF10 | Airtime calculation | Met: 26.7 s per day at SF10 and 20 min; 15 min needs SF9 or faster |
| R5 | Reach the gateway | 90 % or more of uplinks received at 1 km from an indoor gateway, with the stake antenna at about 1 m on the marker rod (RMS-DDR-001, D2), open field with a mature crop | Link budget; later field range walk | **At risk**: 13.5 dB margin at 1 km, but a crop taller than the antenna can take 13 to 19 dB |
| R6 | Run on sun alone | Energy-neutral with 1 peak sun hour per day on the panel; 90 days or more of reporting with no harvest at all | Energy budget | Met: 19 times daily need at 1 sun hour; 186 days on the cell alone |
| R7 | Safe cell and charging | LiFePO4 chemistry, 2 Wh or less per stake; charging blocked below 0 °C and above 45 °C cell temperature; cell fused | Design review; charger datasheet | Met by design (1.92 Wh, NTC cut-off, PTC fuse) |
| R8 | Keep water out | Head IP67; buried section IP68 at 0.5 m for a growing season; UV-stable exposed parts | Design review; later immersion and spray test | Not verifiable at TRL 3; vent membrane added against 15 kPa daily thermal pumping |
| R9 | Operate across field temperatures | -10 to 60 °C at the head, -5 to 40 °C at the cell | Component datasheets; thermal estimate | **At risk**: head about 64 °C and cell up to about 47 °C in bare, hot soil (parts rated 85 °C); a deeper cell that fits gives 46.5 °C, so the response is proposed (RMS-DDR-002, P1) |
| R10 | Install and remove by hand | One person with a 50 mm hand auger and the slot tool (RMS-DDR-002) installs a stake in 15 min or less, with sensing depths repeatable to ±25 mm; removal by hand in 5 min or less | Push-force estimate; later timed trial | **At risk**: with the slot tool about 386 N in moist loam (within one person's 500 N), about 1.2 kN in firm dry loam (without the tool 526 N and 1.8 kN); auger hole 110 mm deep (RMS-DDR-003) |
| R11 | Survive field operations | Rigid head 300 mm or less above grade; anything higher, including the antenna (RMS-DDR-001, D2), carried on the flexible marker rod; high-visibility marker 1 m or more above grade | Model check | Met: head 171 mm; rod top 1,000 mm; antenna 914 to 1,086 mm on the rod |
| R12 | Affordable | One stake $60 or less in parts; pilot set of three stakes, one gateway and the installation slot tool $300 or less, which is how the $300 value-engineering target is read (RMS-DDR-001, D4) | Priced BOM (`bom/bom.csv`) | Met: $59.00 per stake; $281.00 per pilot set including the slot tool, USD 19 under the value-engineering target (indicative, RMS-DDR-003) |
| R13 | Grower owns the data | Data readable without a paid subscription; CSV export; open dashboard. The pilot uses The Things Network community server (RMS-DDR-001, D3) | Design review | Met by design; a fully local server with a different gateway stays a later option |
| R14 | Last in the ground | Probes and electrodes last 2 growing seasons (about 12 months buried) without replacement | Materials review; later soak test | **At risk**: hobby probes corrode quickly unless sealed |

Summary: 8 met, 5 at risk (R1, R5, R9, R10, R14), 1 not verifiable at TRL 3 (R8), none not met.

## Assumptions

- Soil water content, not soil water potential, is the quantity measured. Converting it to plant-available water needs field capacity and wilting point for the soil, set during calibration (FAO-56 method).
- EC is measured as bulk soil EC. Pore-water or saturated-paste EC, which crop salinity thresholds use, differ and need a moisture-dependent conversion.
- LoRaWAN uplink payload of 11 bytes (two moisture counts, EC, temperature, cell voltage, status), 24 bytes on air with LoRaWAN overhead.
- SF10 at 125 kHz is the design case because it is the slowest uplink data rate allowed in the US915 plan and a reasonable margin case in EU868.
- The Things Network fair use policy (30 s of uplink airtime per node per day) applies when the community network is used.
- Worst-month solar resource of 3 peak sun hours on the panel before shading and dust losses.
