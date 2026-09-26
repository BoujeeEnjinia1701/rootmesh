---
doc_id: RMS-DDR-002
title: RootMesh recommendations accepted
project: RootMesh
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of the remaining review recommendations and what changed in the repo
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for items A1 to A4; items O1 and P1 remain proposed

## Context

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." The TRL 2 review items that carried a recommendation (D1 to D9) had already been decided in RMS-DDR-001 and are unchanged. This record covers the recommendations that the review note (`docs/REVIEW.md`) and the TRL 3 documents made after that: the two suggestions in the TRL 2 review note and the recommended next step in the TRL 3 review note, which proposed design responses to the at-risk requirements R9 (cell temperature) and R10 (installation force). Items without a recommendation stay open. TRL 4 remains on hold by Amish's instruction, so any recommendation that needs building, testing or measuring is recorded as decided but on hold.

## Decision

*Table 1. Newly decided items.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| A1 | Slot tool for firm soil (TRL 2 review, suggestion; RMS-CAL-001 v0.1, section G) | Decided by Amish, 2026-09-25: go with recommendation. A tool pre-cuts the fin path. At TRL 3 it is a 32 x 8 mm mild steel flat bar, 650 mm, pointed at the EC tip depth, with a bolted T-handle and a printed depth-stop collar; steel rather than printed, because a printed blade would not survive firm soil. | `cad/src/model.py` adds `build_slot_tool()` and exports `slot-tool.step` and `.stl`; BOM line 15 ($10.00, one per set); RMS-CAL-001 v0.2 section G: push force 517 N to 376 N in moist loam and 1,778 N to 1,216 N in firm dry loam; R10 stays at risk; RMS-DWG-001 Rev P1 to P2 (slot tool note); RMS-PRC-001 v0.4 (component 15, design choice, safety). |
| A2 | Deeper cell position for R9 (TRL 3 review, recommended next step) | Decided by Amish, 2026-09-25: go with recommendation. The deeper cell was checked by calculation. | RMS-CAL-001 v0.2 [F4]: 40 °C needs the cell center about 163 mm deep, where the upper probe sits; the deepest center that fits is about 65 mm (46.5 °C against 46.8 °C). The cell stays at 62 mm; no geometry change. R9 stays at risk and the remaining choice becomes P1 below. |
| A3 | Pilot set now includes the slot tool (follows from A1) | Decided by Amish, 2026-09-25: go with recommendation. `budget_usd` stays $300. | R12 restated so that the $300 pilot set covers three stakes, one gateway and the slot tool; pilot set $256.50 to $266.50, headroom $43.50 to $33.50 (RMS-REQ-001 v0.4; `bom/bom-notes.md`; concept blueprint key figures). |
| A4 | Calibration note for the two-point field calibration (TRL 2 review, suggestion) | Decided by Amish, 2026-09-25: go with recommendation, but on hold. The EC cell constant is already calculated in RMS-CAL-001 section D; the field moisture calibration needs gravimetric samples and KCl standards, which is TRL 4 work. | None. On hold because TRL 4 is on hold by Amish's instruction. |

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First users and region for co-design (market garden, orchard, research farm or extension program), which also sets EU868 or US915. No recommendation was made. | Proposed, awaiting Amish |
| P1 | Response to the cell temperature in bare, hot soil (R9), raised by the check in A2. Option A: a printed shade skirt around the head to shade the soil over the cell (adds a part near machinery; its effect needs measuring). Option B: restate the R9 cell limit to the chosen cell's rated discharge and storage range, taken from its datasheet, while charging stays blocked above 45 °C. Recommendation: B, because the charger already blocks charging in the hot hours and B adds no part; confirm the cell's rated range before adopting it. This is a new proposal made after Amish's acceptance, so it is not decided. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: `budget_usd` stays $300; pitch and problem unchanged; `trl: 3` and `trl_target: 3`.
- RMS-PRC-001 and RMS-REQ-001 move to v0.4, RMS-CAL-001 to v0.2, and drawing RMS-DWG-001 to Rev P2. RMS-PRB-001 is unchanged by these decisions.
- Requirement status is unchanged in count: 8 met, 5 at risk (R1, R5, R9, R10, R14), 1 not verifiable at TRL 3 (R8), none not met. R10 improves in moist soil but stays at risk in firm dry soil.
- No cross-repo action follows from these items.
- Nothing here moves the design toward TRL 4. A timed installation trial, the field calibration and any build of the slot tool are TRL 4 work and on hold.
