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
