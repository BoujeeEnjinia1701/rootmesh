---
doc_id: RMS-DEC-001
title: RootMesh design decisions register
project: RootMesh
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note and decision records, the design for construction (RMS-DDR-003), items to confirm when parts are bought, and the value-engineering summary
---

# RootMesh design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note (`docs/REVIEW.md`); this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction: two-part head with O-ring and screws, board guides, fin in two glued halves with collar and spigot, flush temperature probe, wedge tip and one-piece electrodes, cell holder, gland and vent moved, antenna clips, slot tool handle and stop fixings | Accept as recorded; or change any item | Accept: every change keeps the sensing depths, electrode geometry, cell depth, panel and antenna height | Every component (build plan sections 2 to 4) | RMS-DDR-003, P1 to P11 |
| 2 | Fin print size: each half is 355 mm long | (a) print on a 300 mm class printer or through a print service; (b) split each half into two lengths with a glued lap joint | (a) | Fin halves (build plan section 3.4) | RMS-DDR-003, A1 |
| 3 | Head bonded to the tube, so the stake is one piece below the cap | (a) bonded, as modelled; (b) a second O-ring and screws so the head comes off the tube | (a) for the prototype; revisit after a soak test at TRL 4 | Steps 4 and 6 | RMS-DDR-003, A2 |
| 4 | Response to the cell temperature in bare, hot soil (R9, cell up to about 47 °C) | (A) a printed shade skirt round the head; (B) restate the R9 cell limit to the chosen cell's rated discharge and storage range, with charging still blocked above 45 °C | (B), after confirming the cell's rated range from its datasheet | None in the TRL 3 build; (A) would add a part to the head | RMS-DDR-002, P1 |
| 5 | First users and region for co-design, which sets EU868 or US915 | Market garden, orchard, university research farm or extension program | None yet (co-design partners to be picked per area later) | Antenna and radio band (build plan section 3.12, safety stop S7) | RMS-DDR-001, O1 |
| 6 | Status light on the head | Keep a green LED, blinking briefly after each uplink and on a magnet or button wake only, with its charge added to the energy budget; or leave it out | Keep it, once its charge is added to RMS-CAL-001 | Not in the TRL 3 build; would add a lens hole in the body | REVIEW.md, 2026-09-26, item 2 |
| 7 | Gateway on a post in the hero render | Keep the pilot gateway indoors as decided and treat the post as a render layout only; or show it indoors | Keep it indoors; the post is a render layout | None | REVIEW.md, 2026-09-26, item 3 |

The separate solar cap proposed in the 2026-09-26 review (item 1 there) is now part of decision 1: RMS-DDR-003 adopts a separate cap, sealed by a face O-ring and two screws.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The moisture probe boards are 23 mm wide and 98 to 100 mm long, with their parts on one face within 16 x 3 mm at the top end | The fin's slots and electronics pockets are sized for them | RMS-DDR-003, P4 |
| 2 | The temperature probe's sheath is 6 mm across and about 50 mm long, and its inner wires fit a 3.5 x 5 mm channel with the jacket stripped | The fin's bore and channel are sized for it | RMS-DDR-003, P5 |
| 3 | The 14500 cell with its fuse and leads fits a 15 mm bore, 51 mm deep | The cell holder is sized for it | RMS-DDR-003, P7 |
| 4 | The PVC pipe is 42 mm outside and 36 mm inside diameter | The head socket (43 mm) and fin spigot (35.4 mm) leave glue gaps of about 0.5 and 0.3 mm | RMS-DDR-003, P3 |
| 5 | A 64 x 2 mm O-ring, an M8 gland for 2 to 4 mm cable with its locknut, and short M3 heat-set inserts for a 4.6 mm hole are available | The cap groove, gland boss and insert bosses are sized for them | RMS-DDR-003, P1 and P8 |
| 6 | The solar panel is 70 x 50 mm or smaller, with its lead near the centre of its back | The cap recess is 71 x 51 mm with a lead hole at its centre | RMS-DDR-003, P1 |
| 7 | The charger's temperature window is 0 to 45 °C | R7 and safety stops S3 to S5 depend on it | RMS-CAL-001, B6 |
| 8 | The shaft collars fit 20 mm bar | The slot tool handle depends on them | RMS-DDR-003, P11 |

## Value engineering

Value-engineering target: USD 300 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 281 for the pilot set of three stakes, one gateway and one slot tool (USD 19 under the target); USD 59 per stake against R12's USD 60. Main cost drivers and savings worth trying:

- The largest lines are the gateway (USD 90, about a third of the set), the controller board (USD 15 a stake, USD 45 for three), the antenna and feed (USD 7 a stake) and the seals (USD 5 a stake).
- Making the design constructable added USD 3.50 a stake (the two-part head, the fin halves, and the inserts, screws, epoxy and prototype board of line 16) and USD 4 on the slot tool (shaft collars and thumb screw); the set rose from USD 266.50 to USD 281.
- Savings worth trying: one gateway serves a whole farm, so the per-stake cost falls quickly in larger sets; the controller board's price should fall once the carrier board is designed at TRL 4; one slot tool serves every stake on a farm; O-rings, glands and inserts are much cheaper bought by the hundred.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D9: solar with a LiFePO4 cell, antenna at 1 m on the marker rod, The Things Network with an indoor gateway, the budget read as a pilot set, LiFePO4 chemistry, two moisture depths, modified hobby probes, Wio-E5 controller, 20 min interval | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | RMS-DDR-001 |
| 2026-09-25 | Slot tool for firm soil; deeper cell checked and kept at 62 mm; pilot set includes the slot tool; field calibration note decided but on hold | Amish: "i accept all your recommendations, go with them across all repos." | RMS-DDR-002, A1 to A4 |
| 2026-09-30 | Build plan format approved for all repos; open decisions go in this register, not in the build plan; the design is made physically buildable as the pictures are drawn | Amish: "this is the correct build plan ... this is a good quality document format. Extend this across all the other repos"; "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | RMS-BLD-001, RMS-DDR-003 |
| 2026-10-01 | The budget is a value-engineering target, not a limit; `budget_usd` stays USD 300 | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register, Value engineering |
