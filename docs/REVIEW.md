# Review note: RootMesh

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch run)

### What was done

- `docs/01-problem.md` (RMS-PRB-001 v0.2): problem with sourced facts (water use, sensor adoption, sensor prices, hobby probe failure modes, calibration error), users, operating environment, constraints, out of scope, prior work with links, open questions. No co-design checklist existed, so none was kept or added.
- `docs/03-requirements.md` (RMS-REQ-001 v0.2): 14 measurable requirements (R1 to R14) with targets, verification and concept status, plus assumptions.
- `docs/02-concept.md` (RMS-PRC-001 v0.2): how it works, 14 numbered components, airtime, energy, radio link budget, measurement notes, cost, design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of one stake (panel, ASA head, controller board, antenna, LiFePO4 cell, PVC tube, sensor fin, two probes, EC electrodes, temperature probe, marker rod, seals). Hero context: soil block cut away around the stake and a 1.75 m person standing on the soil.
- `media/`: hero, blueprint sheet (PNG, PDF, SVG), cutaway, exploded view with BOM callouts 1 to 12, data flow diagram, `model.glb` and `viewer.html`.
- `bom/bom.csv`: 14 lines for a pilot set (three stakes and one gateway), rows 1 to 12 numbered to match the exploded view; `bom/bom-notes.md` rewritten.
- `README.md`: hero image and links line added; problem, concept and key components updated to match.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml` unchanged. The pitch and problem still match the numbers.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Time on air, 24 byte uplink at SF10 | about 0.37 s | |
| Airtime per day at 20 min, SF10 | about 27 s (30 s limit) | R4 met |
| Airtime per day at 15 min, SF10 | about 36 s | 15 min not possible at SF10 |
| Daily use with 30 % margin | about 2.0 mAh (6.4 mWh) | |
| Life on the 600 mAh cell alone | about 240 days | R6 met |
| Solar harvest to use ratio | about 70 times (open sky), about 7 times (dense canopy) | R6 met |
| Link margin at 1 km, indoor gateway, antenna 0.2 m | about 0 dB | **R5 not met** |
| Same with antenna at 1 m on marker rod | about 14 dB | R5 met on paper |
| Cost per stake | about $52 | R12 met |
| Pilot set (three stakes and gateway) | about $246 against $300 | R12 met |

Requirements not met or at risk:

- **R5 (range) not met** with the modeled design (whip on the head, indoor gateway): about 0 dB margin at 1 km.
- **R4 partly:** met at the 20 min default, but a 15 min interval at SF10 breaks The Things Network's 30 s per day limit.
- **R1 (moisture ±3 % VWC) at risk:** depends on soil contact and a site calibration, both unverified.
- **R14 (12 months buried) at risk:** hobby probes corrode unless sealed well.
- **R13 partly:** the TTIG-class gateway works only with The Things Stack, so fully local data needs a different gateway.
- R3, R8 and R10 are unverified.

### Proposed, awaiting Amish

1. **Power and pitch.** A: 0.5 W solar panel with a LiFePO4 cell (keeps the "solar-powered" pitch). B: primary Li-SOCl2 cell, no panel (simpler, multi-year life, changes the pitch). Recommendation: A.
2. **Range fix.** A: antenna on the marker rod at 1 m (about $4 a stake). B: outdoor gateway on a mast (about $150 to $250 more, over budget). C: accept about 500 m range. Recommendation: A. The model and BOM still show the whip on the head.
3. **Network.** The Things Network with a TTIG-class gateway for the pilot, or a Raspberry Pi gateway with local ChirpStack (about $60 to $100 more). Recommendation: TTN for the pilot.
4. **Budget reading.** The $300 taken as a pilot set of three stakes and one gateway. `budget_usd` unchanged.
5. LiFePO4 rather than Li-ion chemistry.
6. Two moisture depths (150 mm and 300 mm) rather than one.
7. Modified hobby capacitive probes rather than commercial FDR probes.
8. STM32WLE5-class module (Seeed Wio-E5) as the controller.
9. Default reporting interval of 20 min.
10. First users and region (market garden, orchard, research farm or extension program).

### Safety concerns

- LiFePO4 cell (about 1.9 Wh) in sun and frost: fused, charging blocked below 0 °C and above 45 °C, cell kept below grade.
- Machinery strikes and trip hazard: flagged marker rod; pull stakes before tillage.
- Pointed fin tip and electrodes: tip covers in storage.
- Epoxy and conformal coating: gloves and ventilation.
- Bad readings can mislead irrigation: the documents say readings inform, not replace, the grower's judgment.

### Problems and notes

- Several parts are small next to a 1.75 m person, so the hero shows a soil block cut away around the stake to make the buried sensors visible. The DS18B20 (10) and cell (5) are small in the exploded view but visible below their callouts.
- The LoRa module and carrier board are one BOM line (3) so the callout marks a visible part.
- Transmit current (about 120 mA) is an order-of-magnitude figure for an SX126x-class radio; confirm from the chosen module's datasheet at TRL 3.
- The link budget uses a simple two-ray model and typical sensitivity; range must be walked at TRL 4.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Suggestions (not done, outside this session's scope)

- A calibration note (CAL) for the two-point field calibration and EC cell constant at TRL 3.
- A simple printed tool to cut a slot for the fin in heavy soils.

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to check the energy, airtime, link and EC circuit numbers by calculation and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Amish approved all TRL 2 recommendations on 2026-09-25 ("proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them."). This session advanced RootMesh to TRL 3 and stopped there.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (RMS-DDR-001 v0.1): the nine decided items (D1 to D9) and the one open item (O1).
- `docs/04-calcs/01-sizing.md` (RMS-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: airtime, energy, radio link, EC circuit, sensing geometry, thermal and sealing, installation force and cost, with a results table for R1 to R14. The script imports the model's parameters, reads the BOM and `project.yaml`, and prints every number the note quotes.
- `cad/src/model.py`: parametric build123d model of one installed stake (head, panel, controller, tube, cell, fin, probes, EC rods, temperature probe, seals, marker rod, flag, antenna and lead). Exports `cad/step/` and `cad/stl/`: `rootmesh-stake-assembly`, `head-enclosure`, `sensor-fin`, `stake-tube`.
- `cad/src/sheets.py` and `cad/drawings/RMS-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, orthographic views at 1:5, installed elevation at 1:20, isometric, main dimensions and interfaces. The concept sheet keeps RMS-DWG-010, so RMS-DWG-001 was free. The sheet carries "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION".
- `bom/bom.csv` and `bom/bom-notes.md`: every line priced with a supplier or supplier type; antenna and feed now $7.00 (on the marker rod), seals $5.00 (vent added). Pilot set $256.50 against $300.
- `cad/src/concept_media.py` now builds the media from `model.py`; all media refreshed (hero, blueprint, cutaway, exploded, flow, `model.glb`, `viewer.html`) and checked by eye. Temporary `media/_views*` folders removed.
- RMS-PRB-001, RMS-PRC-001 and RMS-REQ-001 revised to v0.3; `README.md` and `project.yaml` (trl 3, trl_target 3, evidence list) updated. Pitch, problem and `budget_usd` unchanged.
- Model fix found on the way: the TRL 2 massing model tilted the panel away from the equator; the parametric model faces it toward +X as the precis says.

### Requirements (RMS-CAL-001, Table 6)

Counts: 0 not met, 5 at risk, 1 not verifiable at TRL 3, 8 met.

| ID | Status | Key number |
| --- | --- | --- |
| R1 moisture | At risk | Depths 150 and 300 mm met by the model; ±3 % VWC unverifiable on paper |
| R5 range | At risk | 13.5 dB margin at 1 km with the antenna at 1 m; 50 to 100 m of tall crop takes 13 to 19 dB |
| R9 temperature | At risk | Head about 64 °C at 45 °C air (limit 60 °C; parts rated 85 °C); cell up to about 47 °C in bare hot soil (limit 40 °C) |
| R10 installation | At risk | Push force about 520 N in moist loam, about 1.8 kN in firm dry loam; one person gives about 500 N |
| R14 probe life | At risk | 12 months buried depends on the epoxy edge seal |
| R8 sealing | Not verifiable at TRL 3 | Sealed head would see about 15 kPa daily thermal pumping; ePTFE vent added |
| R2, R3, R4, R6, R7, R11, R12, R13 | Met | 26.7 s/day airtime at SF10; 2.58 mAh/day need, 186 days dark, 19 times need at 1 sun hour; 1.92 Wh cell; EC circuit error under 2 %; head 171 mm; $55.50 per stake |

Corrections to TRL 2 figures: days on the cell fell from about 240 to 186 (self-discharge), the harvest ratio from about 70 to 58 times, and the pilot set rose from about $246 to $256.50.

### Decisions recorded (RMS-DDR-001)

Decided by Amish, 2026-09-25: go with recommendation.

- D1 solar panel with rechargeable cell (pitch kept); D2 antenna on the marker rod at about 1 m; D3 The Things Network with a TTIG-class gateway for the pilot; D4 $300 read as a pilot set of three stakes and a gateway (`budget_usd` unchanged, written into R12); D5 LiFePO4; D6 two moisture depths; D7 modified hobby capacitive probes; D8 Wio-E5 (STM32WLE5); D9 20 min default interval.
- Requirement changes that follow: R4 redefined around the 20 min default, R5 for the antenna on the rod, R11 so that only the rigid head is held to 300 mm, R12 and R13 name the decisions. No target was relaxed.
- The portfolio SwapCell decisions do not apply; RootMesh uses no SwapCell pack.

### Still awaiting Amish

- O1: first users and region for co-design (market garden, orchard, research farm or extension program), which also sets EU868 or US915. No recommendation was made; co-design partners are to be picked per area later.

### Safety concerns

- LiFePO4 cell (1.92 Wh): may reach about 47 °C in bare, hot soil; the charger's 45 °C cut-off only stops charging. Fused (PTC), charging blocked below 0 °C.
- Sealed head: about 15 kPa daily pressure swing without a vent; ePTFE vent added.
- Machinery strikes and trips: flagged marker rod; the antenna lead on the rod is a snag point; pull stakes before tillage.
- Installation: up to about 1.8 kN in firm soil; do not hammer on or stand on the head.
- Pointed fin tip and electrodes; epoxy and coating fumes; readings inform, not replace, the grower's judgment.

### Citations and other notes

- The TRL 2 note listed no unchecked citations. The module currents that note flagged were checked against the Seeed Studio Wio-E5 module page (111 mA at +22 dBm, 6.7 mA receive, 2.1 µA sleep) and cited in RMS-CAL-001.
- No TRL 4 material exists in the repo (`electronics/` and `firmware/` are empty; `build-log/` holds only its README). None was created.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Useful paper work that stays within TRL 3: decide O1 (first users and region), then consider design responses to the at-risk items, such as a deeper cell position or soil shade for R9 and a thin slot tool for R10, as a TRL 3 revision.

For the record only, TRL 4 would need: a lab test report (TST, `environment: lab`) covering the EC circuit in KCl standards, gravimetric moisture calibration in two soils, a soak and immersion test of the sealed head and probes, and a measured energy budget on a built stake; build log entries; and later a field range walk through tall crops. None of this is to start until Amish lifts the TRL cap.
