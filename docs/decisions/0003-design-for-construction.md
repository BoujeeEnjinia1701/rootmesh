---
doc_id: RMS-DDR-003
title: RootMesh design for construction
project: RootMesh
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish on 2026-10-02, including the recommendations for A1 and A2
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations in Table 3 (A1 and A2), which are now decided as recommended and recorded in the design decisions register (RMS-DEC-001).

## Context

On 2026-09-30 Amish approved the build plan format and asked for it across all repos, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of RootMesh (RMS-DDR-001 and RMS-DDR-002) showed what the stake does, but it was a massing model: several of its parts could not be made, fitted or fixed as drawn. Checking it with build123d (overlaps, contacts, assembly order and the process for each part) found the eleven problems in Table 1.

The changes keep what the stake does: the same sensing depths (150 mm and 300 mm), electrode spacing and bare length, temperature probe depth, cell depth, panel size and tilt, head height above grade, antenna height on the marker rod, reporting, radio and power design. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 331 constructability checks (`python cad/src/model.py --check`): no two parts overlap, every joint touches (glued joints and slip fits within 0.6 mm), the board and cell holder pass the openings they must pass, the cap screws clear the panel, the gland nut clears the board, and each fin half fits a 300 x 300 mm print bed laid diagonally. All 331 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The head was one printed piece whose only opening was a 28 mm hole above the socket, so the 56 mm controller board could not be put in. The O-ring sat inside solid head material above the tube end and sealed nothing, nothing held the head on the tube, and the cavity broke through the sloped top beside the panel. | The head is a printed body and a removable cap parted 120 mm above grade. The body (5 mm wall, was 3 mm) has a 26 mm socket bonded over the tube, a 3 mm floor with a 28 mm hole, and two bosses with M3 heat-set inserts. The cap has a 3 mm roof under the panel, a 1 mm panel recess, a lead hole, a 64 x 2 mm O-ring in a groove in its rim face (a face seal on the body rim), and two M3 screws with sealing washers in counterbores clear of the panel. | The board must go in from the top, so the head must open there. A face seal on the rim keeps the inside of the body clear for the board; the 5 mm wall gives the O-ring a land. This follows option B of the 2026-09-26 appearance review (a separate cap carrying the panel), with a face seal instead of a second radial O-ring. |
| P2 | The controller board floated in the cavity with no fixing. | Two printed guide ribs on the body walls with 1.8 mm slots; the board slides down them and stands on the slot ends, 76 to 116 mm above grade. | Printed with the body, no extra part; the board lifts out after the cap. |
| P3 | The fin's top ran 10 mm inside the tube and its corners cut into the tube wall (a 36 mm wide fin in a 36 mm bore). The upper probe window reached 110 mm deep, 10 mm above the tube's bottom end, so it was inside the tube. The tube end had nothing to sit on and no seal. | A 42 mm collar, 4 mm thick, tops the fin at 110 mm below grade, with a 35.4 mm spigot, 11 mm long, bonded inside the tube. The tube (still 170 mm) moves up 14 mm to run from 106 mm below grade to 64 mm above it; the head socket is deepened so the head stays at the same height. The upper window keeps its centre at 150 mm and ends at the collar. | Keeps both sensing depths exactly (RMS-DDR-001, D6) and gives the tube a positive stop and a glued, sealed joint. The auger hole becomes 110 mm deep (was 120 mm). |
| P4 | The fin was a solid print: the probes floated in through-windows with nothing to hold them and no route for their wires, and nothing held the temperature probe or the electrodes. | The fin is printed in two halves split on its mid-plane and glued with epoxy. Inside: 0.9 mm slots for the probe board edges, 3.4 mm pockets for the probe electronics (front half), two 3.5 x 5 mm wire channels in the side rails from the foot to the spigot top, a cross channel for the lower probe, a 6.2 mm bore for the temperature probe and 4.1 mm grooves for the electrodes. The windows narrow from 28 to 19 mm so each board edge is held 2 mm on each side and the rails have room for the channels. | A two-part print is the simplest way to make closed internal channels and to trap the sensors, and the epoxy glue line also pots them. |
| P5 | The temperature probe stood 7 mm proud of the fin edge, outside the 32 mm slot that the slot tool cuts, so it would be torn off when the fin is pushed in. | The sheath lies in the bore in the fin edge, 0.4 mm proud. | It still touches undisturbed soil at 225 mm and survives installation. |
| P6 | The fin tip was a round cone 24 mm across, twice the fin thickness, overlapping the electrodes; each electrode was modelled as three separate pieces with a gap. | A wedge tip 16 mm wide and 30 mm long between the electrodes, with flat shoulders where the electrodes leave the foot. Each electrode is one 80 mm rod: 15 mm held in the foot grooves, 5 mm in a heat-shrink sleeve, 60 mm bare. | The bare length and spacing set the EC cell constant and are unchanged, so section D of RMS-CAL-001 stands. |
| P7 | The cell floated in the tube. | A printed holder, 22 mm across, stands on two legs on the spigot top, with the cell centre still 62 mm below grade. It lifts out on a cord through the 28 mm floor hole once the cap and board are out. | Holds the cell at the depth the thermal calculation uses and gives a way to change it without cutting the stake. |
| P8 | The coax gland boss sat 120 mm above grade, now the cap's parting line, and in line with the board. | The gland moves to 100 mm above grade, turned 30 degrees toward the front, on a boss with flat faces outside and inside for the gland and its locknut. | The locknut clears the board and module by about 2 mm (checked). |
| P9 | The vent boss at the back would cut into a cap screw boss. | The vent moves to the back right, 82 mm above grade. | Same vent, clear of the bosses and guides. |
| P10 | The antenna clip was a block overlapping the rod; the dipole was held at one point; the lead ran 1.5 mm off the rod in the air. | Two printed clips, each with an 8.2 mm rod hole and a 10.2 mm dipole hole, centred 925 and 985 mm above grade; the lead runs along the rod held by four cable ties. | A real fixing that slides on by hand; the dipole stays centred 1,000 mm above grade (RMS-DDR-001, D2). |
| P11 | The slot tool's 20 mm handle lay in the plane of the 32 mm blade, passing through it, and the depth stop was loose. | The handle passes through a 20.5 mm cross hole 25 mm below the struck end, held centred by two 20 mm shaft collars. The printed stop is clamped to the blade by an M5 thumb screw in a trapped nut. The blade is 650 mm long overall, as the BOM says (the model had 635 mm). | No welding; the stop can be set to the electrode tip depth (485 mm) and moved for other stakes. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| BOM | Line 2 head body and cap ($3.50, was $3.00); line 7 fin in two halves ($3.00, was $2.50); lines 4, 5, 11 and 12 re-described; line 15 slot tool fixings ($14.00, was $10.00); new line 16, head fixings and bonding ($2.50 per stake). One stake $55.50 to $59.00; pilot set $266.50 to $281.00. | Parts added for construction. |
| Cost | Value-engineering target: USD 300 (`budget_usd`, unchanged). Estimated cost of the constructable design: USD 281 (USD 19 under the target). R12's $60 per stake is met by $1.00 [H1]. | |
| Installation (R10) | Auger hole 110 mm deep; fin pushed 310 mm into undisturbed soil instead of 300 mm. With the slot tool 386 N in moist loam (was 376 N) and 1,245 N in firm dry loam (was 1,216 N) [G4]. Status unchanged: at risk. | P3 lowered the start of undisturbed soil by 10 mm. |
| Cell temperature (R9) | Deepest cell centre that fits is now 62 mm (46.8 °C), where the cell already sits; v0.2 found 65 mm (46.5 °C) [F4]. Status unchanged: at risk. | The holder base takes the 3 mm the cell could have dropped. |
| Sealing (R8) | Head air 272 cm³ (was 308 cm³); pressure rise unchanged at 15.1 kPa [F3]. A second seal (the cap's O-ring) is added. Status unchanged: not verifiable at TRL 3. | Thicker body wall. |
| Documents | RMS-CAL-001 v0.3, RMS-REQ-001 v0.5, RMS-PRC-001 v0.5; RMS-DWG-001 Rev P4; making sketches RMS-DWG-101 to 110; build plan RMS-BLD-001 and register RMS-DEC-001 added. No requirement changed status. | Follows the model. |

*Table 3. Proposed, then accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Each fin half is 355 mm long with its collar and spigot. It fits a 300 x 300 mm print bed laid diagonally, but not the common 220 or 256 mm beds. | (a) print on a 300 mm class printer or through a print service; (b) split each half into two lengths with a glued lap joint between the windows. | (a): a joint between the windows would add a seam across the wire channels and the temperature probe. Accepted 2026-10-02. |
| A2 | The tube is now bonded into the head body and onto the fin, so the stake is one permanent piece below the cap. The cell and board are reached through the cap; the fin cannot be separated from the head for repair. | (a) bonded, as modelled; (b) a second O-ring and two screws at the head socket, so the head comes off the tube. | (a) for the prototype: fewer seals in the ground, and the cell is still reachable. Revisit after a soak test at TRL 4. Accepted 2026-10-02. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan RMS-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status is unchanged: 8 met, 5 at risk (R1, R5, R9, R10, R14), 1 not verifiable at TRL 3 (R8), none not met (RMS-CAL-001 v0.3).
- The open item from the 2026-09-26 appearance review on a separate solar cap is answered by P1 in this record, accepted with the rest of it by Amish on 2026-10-02.
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept head, fin and antenna clip; they need updating on Amish's Mac, where Blender is.
- The probe boards, temperature probe, cell, O-ring, gland, inserts and PVC pipe are chosen at TRL 4; the sizes in the register's "to confirm" list must be checked against the parts bought, and the slots, pockets, bores and holes moved to suit.
