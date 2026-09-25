---
doc_id: RMS-REQ-001
title: RootMesh requirements
project: RootMesh
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# RootMesh requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with growers, and will be checked by calculation at TRL 3 and revised after user input (see RMS-PRB-001). The status column gives the concept's position against each target from the first-order numbers in RMS-PRC-001. Nothing has been built or measured, so "met" means met on paper or by a datasheet.

**Reference case:** one stake in a loam field, sensing at 150 and 300 mm, reporting every 20 min to an indoor gateway about 1 km away, in a region with 3 peak sun hours per day in the worst month.

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status |
| --- | --- | --- | --- | --- |
| R1 | Measure volumetric water content at two root-zone depths | 150 mm and 300 mm below grade (±25 mm); 5 to 50 % VWC; ±3 % VWC after a site-specific calibration | Calibration method note; later gravimetric calibration in two soils | Unverified, at risk: depends on probe contact and calibration |
| R2 | Measure root-zone soil temperature | ±0.5 °C from -10 to 60 °C at about 225 mm depth | DS18B20 datasheet | Met by datasheet |
| R3 | Measure bulk soil electrical conductivity | 0 to 4 dS/m; ±10 % or ±0.1 dS/m, whichever is larger, after calibration in standard solutions; reported at 25 °C | Circuit calculation; later bench test in KCl solutions and soil | Unverified |
| R4 | Report often enough for daily irrigation decisions | Every 20 min or shorter by default, adjustable from 10 to 60 min; uplink airtime 30 s or less per day at the design spreading factor (SF10) | Airtime calculation | Met at 20 min (about 27 s per day at SF10). A 15 min interval is **not** possible at SF10 within 30 s per day |
| R5 | Reach the gateway | 90 % or more of uplinks received at 1 km from an indoor gateway, stake antenna about 0.2 m above grade, open field with a mature crop | Link budget; later field range walk | **At risk, likely not met** with an indoor gateway; see RMS-PRC-001 |
| R6 | Run on sun alone | Energy-neutral with 1 peak sun hour per day on the panel; 90 days or more of reporting with no harvest at all | Energy budget | Met on estimate: about 70 times daily use harvested at 3 sun hours; about 240 days on the cell alone |
| R7 | Safe cell and charging | LiFePO4 chemistry, 2 Wh or less per stake; charging blocked below 0 °C and above 45 °C cell temperature; cell fused | Design review; charger datasheet | Met by design (about 1.9 Wh, NTC cut-off, PTC fuse) |
| R8 | Keep water out | Head IP67; buried section IP68 at 0.5 m for a growing season; UV-stable exposed parts | Design review; later immersion and spray test | Unverified |
| R9 | Operate across field temperatures | -10 to 60 °C at the head, -5 to 40 °C at the cell | Component datasheets; thermal estimate | Met by datasheets; head temperature in full sun is an estimate |
| R10 | Install and remove by hand | One person with a 50 mm hand auger installs a stake in 15 min or less, with sensing depths repeatable to ±25 mm; removal by hand in 5 min or less | Installation sequence review; later timed trial | Unverified |
| R11 | Survive field operations | Head and antenna 300 mm or less above grade; high-visibility marker 1 m or more above grade | Model check | Met by design (antenna tip about 270 mm, flag about 1 m) |
| R12 | Affordable | One stake $60 or less in parts; pilot set of three stakes and one gateway $300 or less | Priced BOM (`bom/bom.csv`) | Met on indicative prices (about $52 per stake, about $246 per pilot set) |
| R13 | Grower owns the data | Data readable without a paid subscription; CSV export; open dashboard | Design review | Partly met: free with The Things Network; a fully local server needs a different gateway (open question) |
| R14 | Last in the ground | Probes and electrodes last 2 growing seasons (about 12 months buried) without replacement | Materials review; later soak test | **Unverified, at risk**: hobby probes corrode quickly unless sealed |

## Assumptions

- Soil water content, not soil water potential, is the quantity measured. Converting it to plant-available water needs field capacity and wilting point for the soil, set during calibration (FAO-56 method).
- EC is measured as bulk soil EC. Pore-water or saturated-paste EC, which crop salinity thresholds use, differ and need a moisture-dependent conversion.
- LoRaWAN uplink payload of about 11 bytes (two moisture counts, EC, temperature, cell voltage, status), 24 bytes on air with LoRaWAN overhead.
- SF10 at 125 kHz is the design case because it is the slowest uplink data rate allowed in the US915 plan and a reasonable margin case in EU868.
- The Things Network fair use policy (30 s of uplink airtime per node per day) applies when the community network is used.
- Worst-month solar resource of 3 peak sun hours on the panel before shading and dust losses.
