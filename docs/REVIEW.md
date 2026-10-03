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

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25, in chat: "i accept all your recommendations, go with them across all repos." This session applied that instruction inside this repo only, at TRL 3, and recorded it in `docs/decisions/0002-recommendations-accepted.md` (RMS-DDR-002 v0.1).

### Decisions applied and what changed

The TRL 2 items D1 to D9 were already decided in RMS-DDR-001 and are unchanged. Newly decided (Decided by Amish, 2026-09-25: go with recommendation):

| # | Item | Change | Before | After |
| --- | --- | --- | --- | --- |
| A1 | Slot tool for firm soil (TRL 2 suggestion) | Steel slot tool, 32 x 8 mm blade pointed at 485 mm, T-handle, printed depth stop; `build_slot_tool()` in `cad/src/model.py`, `cad/step/slot-tool.step` and `cad/stl/slot-tool.stl`; BOM line 15 | Push force 517 N moist, 1,778 N firm dry | 376 N moist, 1,216 N firm dry |
| A2 | Deeper cell for R9 (TRL 3 recommended next step) | Checked by calculation (RMS-CAL-001 v0.2, [F4]); no geometry change | Cell peak 46.8 °C at 62 mm | Deepest fit about 65 mm gives 46.5 °C; 40 °C needs about 163 mm, where the upper probe sits; cell stays at 62 mm |
| A3 | Pilot set includes the slot tool | R12 restated; `budget_usd` unchanged at $300 | Pilot set $256.50, headroom $43.50 | $266.50, headroom $33.50 |
| A4 | Field calibration note (TRL 2 suggestion) | Decided but on hold: the field calibration needs gravimetric samples and KCl standards (TRL 4) | | |

Documents changed: RMS-PRC-001 v0.3 to v0.4, RMS-REQ-001 v0.3 to v0.4, RMS-CAL-001 v0.1 to v0.2 (script `docs/04-calcs/sizing.py` updated and re-run), RMS-DWG-001 Rev P1 to P2 (slot tool note), `bom/bom.csv` and `bom/bom-notes.md`, `README.md`, `project.yaml` (evidence list only). Media and all PDFs regenerated; STEP and STL re-exported. RMS-PRB-001 is unchanged (it did not attribute the idea to a brainstorm or review).

### Requirement status (RMS-CAL-001 v0.2)

Counts unchanged: 0 not met, 5 at risk, 1 not verifiable at TRL 3, 8 met.

- At risk: R1 (moisture accuracy), R5 (range through tall crops), R9 (head about 64 °C; cell about 47 °C in bare, hot soil), R10 (now 376 N in moist loam, within one person's 500 N, but 1,216 N in firm dry loam), R14 (probe life).
- Not verifiable at TRL 3: R8 (sealing).
- Met: R2, R3, R4, R6, R7, R11, R12 ($55.50 per stake, $266.50 pilot set), R13.

### Still awaiting Amish

- O1: first users and region for co-design (sets EU868 or US915). No recommendation was made.
- P1 (new, from the A2 check): respond to the cell temperature in bare, hot soil by (A) a printed shade skirt around the head or (B) restating the R9 cell limit to the chosen cell's rated discharge and storage range, with charging still blocked above 45 °C. Recommendation: B, after confirming the cell's rated range.

### Cross-repo actions

None. No RootMesh recommendation needs another repo to change.

### Other changes

- `README.md`: added "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea" before "Problem", with cited figures (World Bank, FAO, USGS, ABS, European Parliamentary Research Service, IFPRI, Datta and Taghvaeian 2023). The inspiration point is the USDA NRCS guide *Estimating Soil Moisture by Feel and Appearance* (April 1998).
- All generated files regenerated so they carry designmolecule.com.

### Safety

The slot tool adds a pointed steel blade struck with a mallet: eye protection, gloves, feet clear of the point, collar fitted, tip cover in storage (RMS-PRC-001 v0.4, Safety). The earlier concerns (cell temperature, installation force, machinery strikes, sealed-head pressure) stand.

### TRL 4

TRL 4 remains on hold by Amish's instruction. No hardware, test, trial, PCB or firmware work was started. The field calibration (A4), a timed installation trial with the slot tool and any build of it wait for Amish to lift the cap.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose RootMesh for the first batch of product renders on 2026-09-26. This session added an appearance model for photoreal renders; the massing model, BOM, calculations and drawing are unchanged.

### What was done

- `cad/src/product_model.py` (new): `product_parts()` returns 85 parts (18 shell, 7 internal, 60 context) with colour, material class, BOM line, group and explode offset, plus `TITLE` and three `RENDER_VIEWS` (hero, exploded, detail). It imports `PARAMS` and `derived()` from `cad/src/model.py`, and every main dimension and interface (tube, socket, head radius and height, 30 degree slope, panel size, board and cell positions, fin, windows, sensing depths, EC pitch, temperature probe depth, marker rod, flag and antenna height) is taken from there. Appearance detail added:
  - head with filleted top and bottom edges, a grip-rib band, a dark nameplate with a teal line, a green status light behind a clear lens, a gland nut and dome on the coax boss and a white ePTFE vent disc;
  - a solar cap split from the head on a parting line parallel to the slope, carrying the panel (cell grid and busbars) and two cap screws;
  - controller board with the LoRaWAN module shield, charger IC and connectors; O-ring; LiFePO4 cell with terminals in its holder;
  - stake tube with eased ends; sensor fin with filleted edges, teal depth marks below each window, the capacitive probes with an epoxy edge seal, a stainless temperature sheath and stainless EC electrodes;
  - marker rod with a fabric flag, cable ties along the coax, and the sleeve dipole with its clip;
  - context: a two-layer soil block cut away on the plane through the stakes, two more stakes, and the gateway on a short timber post with bracket, status light and USB lead.
- `README.md`: the hero image is now `media/render-hero.png`, with a link to `media/render-exploded.png`. The render files are produced separately.
- Matplotlib self-check previews (not committed) were used to check that the hero, exploded and detail views read clearly.

### Where the appearance model differs from model.py

1. **Solar cap as a separate part.** `model.py` has a one-piece printed head. The appearance model splits a 10 mm cap off the top on a parting line and shows it exploded with the panel. Proposed, awaiting Amish. Options: (A) keep the one-piece head and read the line as cosmetic; (B) adopt a separate cap with the panel bonded to it, sealed to the head by a second O-ring. Recommendation: B, because the panel and board could then be serviced without pulling the stake; size the second seal in the next design step.
2. **Status light.** A green status LED behind a clear lens on the front of the head is not in the BOM or the energy budget. Proposed, awaiting Amish. Recommendation: keep it, driven as a brief blink after each uplink and on a magnet or button wake only, and add its charge to the RMS-CAL-001 energy budget before adopting it.
3. **Gateway outdoors on a post.** `model.py` and RMS-DDR-001 D3 keep the TTIG-class gateway indoors at the farmhouse; the hero shows it on a short timber post behind the stakes so one frame explains the system. Proposed, awaiting Amish. Recommendation: keep the pilot gateway indoors as decided and treat the post as a render layout only; the render note says so.
4. **Stake spacing.** The hero places three stakes 330 mm apart on one section plane. In the field they stand in different parts of a block or field. Render layout only; no change proposed.
5. **Colours.** The massing colours are replaced with product colours: white head and cap, light grey tube, mid-grey fin, black probes, stainless electrodes and temperature sheath, orange rod and flag. Appearance only; no change proposed.

### TRL

This is an appearance model only, for renders. It adds no tolerances, fabrication detail, PCB layout or test work. `trl` stays 3 and TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: kit 1.7.0, design for construction and prototype build plan

Amish approved the build plan format on 2026-09-30 and asked for it across all repos, with open decisions kept in a separate register; on 2026-10-01 he asked that budgets be treated as value-engineering targets. This session applied both to RootMesh at TRL 3. Nothing was built or tested.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` matches `.kit/CLAUDE.md`.
- `cad/src/model.py` rewritten as a constructable model: `build_components()` gives every part, `build_parts()` groups them by BOM line for the concept media, `slot_tool_components()` gives the slot tool, and `python cad/src/model.py --check` runs 331 constructability checks (no overlaps, every joint touches, board and cell holder pass their openings, cap screws clear the panel, gland nut clears the board, fin halves fit a 300 mm print bed). All pass. STEP and STL exported for the assembly and every made part (`cad/step`, `cad/stl`).
- `docs/decisions/0003-design-for-construction.md` (RMS-DDR-003 v0.1, Draft): the design changes below, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `cad/src/build_plan_media.py` (new): overview, slot tool overview, ten making sketches RMS-DWG-101 to 110, a fin inside-face layout, eleven joint close-ups, sixteen assembly step pictures and a wiring diagram, all drawn from the model.
- `docs/05-build-plan.md` (RMS-BLD-001 v0.1) and `docs/06-design-decisions.md` (RMS-DEC-001 v0.1), new.
- `bom/bom.csv` and `bom/bom-notes.md`: lines 2, 4, 5, 7, 11, 12 and 15 updated; line 16 (head fixings and bonding) added.
- `docs/04-calcs/sizing.py` and RMS-CAL-001 v0.3, RMS-REQ-001 v0.5, RMS-PRC-001 v0.5: re-run and updated for the constructable design; budget wording changed to a value-engineering target.
- RMS-DWG-001 Rev P4; concept media (`media/hero.png`, `exploded.png`, `cutaway.png`, `flow.png`, `concept-blueprint.*`, `model.glb`, `viewer.html`) regenerated.
- `project.yaml`: `design_state: constructable`; RMS-DDR-003, the build plan, the register and the media script added to `trl_evidence`; `budget_usd` unchanged at 300.
- `README.md`: value-engineering line, build plan and register links, a "Building the prototype" section with the overview picture (placed before "Repository layout", since this README has no "Safety" section), updated costs.

### Design changes made for construction (RMS-DDR-003)

1. Head split into a printed body bonded over the tube and a removable cap carrying the panel, sealed by a 64 x 2 mm face O-ring and held by two M3 screws with sealing washers into heat-set inserts; body wall 5 mm (was 3 mm); the one-piece head could not take the board and its O-ring sealed nothing.
2. Board held in two printed guide slots.
3. Fin topped by a 42 mm collar and a 35.4 mm spigot bonded in the tube; the tube moved up 14 mm (still 170 mm long) so the upper probe stays centred at 150 mm; auger hole 110 mm deep (was 120 mm).
4. Fin printed in two glued halves with probe slots, electronics pockets, wire channels, a temperature probe bore and electrode grooves; windows 19 mm wide (was 28 mm).
5. Temperature probe recessed into the fin edge (0.4 mm proud; it stood 7 mm out and would have been torn off).
6. Round tip replaced by a wedge between the electrodes; each electrode one 80 mm rod (15 mm held, 5 mm sleeved, 60 mm bare, as before).
7. Printed cell holder standing on the spigot, cell centre still 62 mm deep.
8. Coax gland moved to 100 mm above grade, turned toward the front, clear of the board.
9. Vent moved to the back right, clear of the screw bosses.
10. Two printed antenna clips and four cable ties in place of an overlapping block and a free-hanging lead.
11. Slot tool handle through a cross hole with two shaft collars; depth stop clamped by an M5 thumb screw; blade 650 mm as the BOM says.

### Key results

- Requirement status unchanged: 8 met, 5 at risk (R1, R5, R9, R10, R14), 1 not verifiable at TRL 3 (R8), none not met.
- R10: with the slot tool 386 N in moist loam (was 376 N) and 1,245 N in firm dry loam (was 1,216 N); the fin now starts 10 mm deeper.
- R9: the deepest cell centre that fits is now 62 mm (46.8 °C), where the cell already sits.
- Cost: USD 59.00 a stake (R12's USD 60 met by USD 1); pilot set USD 281.00. Value-engineering target: USD 300. Estimated cost of the constructable design: USD 281 (USD 19 under the target).

### Proposed, awaiting Amish

All open decisions are in `docs/06-design-decisions.md`: accept RMS-DDR-003; fin print size (A1); head bonded to the tube (A2); the R9 response (P1); first users and region (O1); the status light; the gateway in the hero render.

### Stale images

The design changed visibly (two-part head with a parting line and screw heads, collar on the fin, narrower windows, wedge tip, antenna clips). `media/render-hero.png`, `render-exploded.png`, `render-detail.png`, `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept and need regenerating on Amish's Mac.

### Safety

The build plan carries eight safety stops (cell, charging, slot tool, radio, field). The slot tool is a pointed steel blade struck with a mallet; grinding steel and epoxy work are added workshop hazards. The safety case is otherwise unchanged.

### Recommended next step

Review RMS-DDR-003 and the register. TRL 4 (building to this plan) stays on hold until Amish lifts the cap.

## Session 2026-10-02: open decisions decided

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This approves the recommendation written for each open decision in the design decisions register (RMS-DEC-001 v0.1). trl stays 3; no build or test work was done, and the model, BOM quantities and prices, and pictures are unchanged.

### Decisions recorded

Seven decisions, all moved to Decisions made in RMS-DEC-001, dated 2026-10-02:

1. RMS-DDR-003 accepted: design for construction P1 to P11, as recorded (including the separate solar cap).
2. Fin print size: option (a), a 300 mm class printer or a print service.
3. Head joint: option (a), bonded to the tube for the prototype; revisited after the TRL 4 soak test.
4. Cell temperature (R9): option (B), the cell limit restated to the chosen cell's rated discharge range, with charging still blocked above 45 °C, provided its datasheet rates discharge to 55 °C or more; otherwise the printed shade skirt (A) is added.
5. First users and region: a US university extension program with a research farm, on US915; Texas A&M AgriLife Extension is the first candidate to approach.
6. Status light: a green LED on the head, blinking briefly after each uplink and on a magnet or button wake only, once its charge is in the energy budget.
7. Gateway: indoors as decided; the post in the hero render is a layout only, and its caption says so.

### Documents changed

- `docs/06-design-decisions.md` (RMS-DEC-001 v0.2): open decisions moved to Decisions made; the note on the separate solar cap folded into decision 1.
- `docs/decisions/0003-design-for-construction.md` (RMS-DDR-003 v0.2, status Draft): accepted, with A1 and A2 accepted as recommended.
- `docs/decisions/0001-trl2-review-decisions.md` (RMS-DDR-001 v0.2): O1 recorded as decided.
- `docs/decisions/0002-recommendations-accepted.md` (RMS-DDR-002 v0.2): O1 and P1 recorded as decided.
- `docs/03-requirements.md` (RMS-REQ-001 v0.6): R9 cell limit restated (still at risk for the head).
- `docs/04-calcs/01-sizing.md` (RMS-CAL-001 v0.4): R9 target in the requirement table; no number re-run.
- `docs/02-concept.md` (RMS-PRC-001 v0.6): decisions on first users, US915, R9 and the status light; open questions answered.
- `docs/01-problem.md` (RMS-PRB-001 v0.4): first users and region.
- `README.md`: caption under the hero render (the post is a layout only).

### Follow-up actions to carry approved decisions into the design

1. Decision 4 (calculations and BOM): choose the cell, confirm from its datasheet that discharge is rated to 55 °C or more, and record it in the BOM notes; if it is not, add the printed shade skirt to the model, BOM, drawings and build plan pictures.
2. Decision 5 (calculations): redo the link budget, airtime and fair use figures of RMS-CAL-001 and RMS-PRC-001 for US915 (915 MHz, US power limits, 400 ms dwell time).
3. Decision 5 (model and BOM): cut the sleeve dipole for 915 MHz and specify the US915 gateway and antenna in the BOM (build plan section 3.12 and safety stop S7).
4. Decision 6 (calculations, model, BOM): add the LED's charge to the energy budget in RMS-CAL-001, then add the lens hole in the head body, the LED and its resistor to the model and BOM.
5. Decision 7 (pictures): put the "layout only" note in the hero render's own caption when the renders are next made (`.kit/photo_caption.py`).
6. Decision 1 (pictures): update `cad/src/product_model.py` to the constructable head, fin and antenna clip and re-render the photoreal renders, card and social preview on Amish's Mac.

### Points found in the review

- R9 also sets 60 °C at the head, which the head exceeds (about 64 °C at 45 °C air); neither option in decision 4 addresses it, and it was not an open item. R9 stays at risk for the head.
- Charging is blocked above 45 °C cell temperature, which in bare hot soil falls in the sunniest afternoon hours; the energy budget should show the solar charge still covers the load.

## Session 2026-10-02: approved follow-ups carried out

Amish, 2026-10-02: every follow-up action from the open-decision sign-off is approved and to be completed. trl stays 3; no build or test work was done. `budget_usd` is unchanged.

### Approved follow-ups carried out

1. Decision 4, cell: done. The cell is an IFR14500EC class LiFePO4 cell (600 mAh, 3.2 V). Its datasheet ([Simpower IFR14500EC](https://www.simpower.co.nz/wp-content/uploads/2021/11/IFR14500EC.pdf)) rates discharge from -20 to +60 °C and charge from 0 to +60 °C, so the 55 °C condition is met and the printed shade skirt is not added. BOM line 5 and the build plan record it; the charger still blocks charging above 45 °C. The datasheet is for the class, not for a purchased lot: check the supplier's own sheet before buying.
2. Decision 5, US915 calculations: done. RMS-CAL-001 v0.5 and RMS-PRC-001 v0.7 redo airtime (400 ms dwell limit, SF10 takes 371 ms), the link budget (915 MHz, 20 dBm radiated, margin at 1 km 19.5 dB) and the energy budget.
3. Decision 5, dipole and gateway: done. The model's dipole is 164 mm (was 172 mm); BOM line 4 is a 915 MHz dipole and line 13 the US915 gateway; build plan section 3.12 and stop S7 say so.
4. Decision 6, status LED: done. Charge added to the energy budget (RMS-CAL-001 [B1b]: 2.14 mA, 0.21 mAs per report, 3.2 mAs a day of wake blinks, five wakes a day assumed), then a 5.2 mm lens hole, the LED and its 560 Ω resistor added to the model (388 checks pass, 0 failures), BOM line 17 ($0.15 a stake), the build plan and the wiring picture.
5. Decision 7, hero caption: done in the render scene. The hero view's note now says the post is a layout only and the pilot gateway sits indoors; it travels in `rootmesh__jobs.json` to `.kit/photo_caption.py`.
6. Decision 1, appearance model and renders: the appearance model `cad/src/product_model.py` is updated to the constructable head (lens hole, gland and vent at the model positions), the fin collar and spigot, the cell holder, the two antenna clips, the cable tie heights and the 915 MHz dipole, with the dimensions read from `cad/src/model.py`. Render scenes exported to `/home/claude/renders/rootmesh` (hero, exploded, detail). Not done: the photoreal renders, `media/card.png` and `media/social-preview.png`, which are made on Amish's Mac next.

### Results

- Model: 388 constructability checks, 0 failures; STEP and STL regenerated.
- BOM: line 17 added; lines 3, 4, 5 and 13 reworded for US915 and the chosen cell; no other line changed. One stake $59.15, pilot set $281.45. Value-engineering target: USD 300. Estimated cost of the constructable design: USD 281.45 (USD 18.55 under the target). Mass is not tracked in the bill of materials.
- Requirement status changes: none (8 met, 5 at risk: R1, R5, R9, R10, R14; 1 not verifiable at TRL 3: R8). R5 margin rose to 19.5 dB but tall crops still take it down to 0.1 dB at 100 m of crop, so it stays at risk. R9 stays at risk because the head reaches about 64 °C against its 60 °C limit.
- Pictures regenerated: RMS-DWG-001 Rev P5, RMS-DWG-106 Rev P2 (lens hole), the other making sketches, concept media (hero, exploded, cutaway, blueprint, viewer), overview, joints 1 to 11, steps 1 to 16, wiring. `drawing.py --check-text` reports nothing.

### Documents changed

RMS-BLD-001 v0.2, RMS-CAL-001 v0.5, RMS-REQ-001 v0.7, RMS-PRC-001 v0.7, RMS-DEC-001 v0.3, with `README.md`, `bom/bom.csv`, `bom/bom-notes.md`, `cad/src/model.py`, `cad/src/product_model.py`, `cad/src/sheets.py`, `cad/src/build_plan_media.py`, `cad/src/concept_media.py` and `docs/04-calcs/sizing.py`. PDFs regenerated.

### Points found

- The 20 dBm radiated power is the module's practical limit (+22 dBm conducted less 1.6 dB of coax), not a regulatory figure; the US915 rules allow more. Proposed, awaiting Amish: none needed, but the energy budget already assumed the 22 dBm transmit current.
- The LED position (front right, 60 mm up) and the five wakes a day are my choices; both are easy to move.

### Cross-repo actions

- None for this repository's own follow-ups. Outreach to Texas A&M AgriLife Extension (decision 5) is Amish's and nothing is agreed.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
