---
doc_id: RMS-DDR-001
title: RootMesh TRL 2 review decisions
project: RootMesh
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the item that remains open
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: O1 decided by Amish on 2026-10-02 as recommended (Texas A&M AgriLife Extension on US915 as first candidate)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D9; item O1 decided on 2026-10-02 as recommended (Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions.")

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed ten items as "Proposed, awaiting Amish", and the design precis RMS-PRC-001 v0.2 listed the same key design choices with options. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided in favor of that recommendation. The item without a recommendation stays open. The same instruction approved portfolio-wide decisions on the SwapCell interface and shared SwapCell pricing; RootMesh does not use SwapCell, so they do not apply here. It also approved that community designs pick co-design partners per area later.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in RMS-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Power and pitch | Option A: a 0.5 W solar panel with a rechargeable cell, keeping the "solar-powered" pitch, rather than a primary Li-SOCl2 cell. Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | Range fix | Option A: move the stake antenna to the top of the marker rod, about 1 m above grade, with a short coax lead (about $4 a stake at TRL 2; $7 with the dipole, lead and clip in the TRL 3 BOM). Not an outdoor gateway on a mast, and not a shorter range. Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Network | The Things Network community server with a TTIG-class indoor gateway for the pilot. A Raspberry Pi gateway with a local ChirpStack server stays a documented later option. Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | Budget reading | Keep `budget_usd` at $300 and read it as a pilot set of three stakes and one gateway. The redefinition is written into R12. Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | Cell chemistry | LiFePO4 rather than Li-ion. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | Sensing depths | Two moisture depths, 150 mm and 300 mm, on one fin. Decided by Amish, 2026-09-25: go with recommendation. |
| D7 | Moisture probes | Modified hobby capacitive probes (TLC555, sealed edges, frequency output) at TRL 2 and 3, with a commercial reference sensor borrowed for calibration later, rather than commercial FDR or TDR probes. Decided by Amish, 2026-09-25: go with recommendation. |
| D8 | Controller | STM32WLE5-class LoRaWAN module (Seeed Wio-E5) on a carrier board. Decided by Amish, 2026-09-25: go with recommendation. |
| D9 | Reporting interval | 20 min by default. Faster intervals only where the spreading factor keeps the uplink within 30 s per day. Decided by Amish, 2026-09-25: go with recommendation. |

*Table 2. Item that remains open (no recommendation was made).*

| # | Item | Status |
| --- | --- | --- |
| O1 | First users and region for co-design: a market garden, an orchard, a university research farm or an extension program. This also settles EU868 or US915. | Decided by Amish on 2026-10-02 as recommended in RMS-DEC-001: a US university extension program with a research farm, on US915, with Texas A&M AgriLife Extension as the first candidate to approach |

## Consequences

- `project.yaml`: `budget_usd` stays $300. The pitch and problem lines are unchanged, because no reworded pitch or problem was recommended and D1 keeps "solar-powered".
- RMS-PRB-001, RMS-PRC-001 and RMS-REQ-001 are revised to v0.3. R5 is redefined for the antenna on the marker rod (D2), R11 is redefined so that only the rigid head is held to 300 mm and the antenna may sit on the flexible marker rod (D2), R4 is redefined around the 20 min default (D9), R12 carries the pilot-set reading of the budget (D4) and R13 names The Things Network for the pilot (D3). The key design choices in the precis are no longer "proposed".
- The model, drawing RMS-DWG-001 and BOM carry the antenna on the marker rod: a half-wave sleeve dipole centered 1,000 mm above grade, fed by a 1.2 m RG174 lead through a gland on the head. RMS-CAL-001 gives the link margin as 13.5 dB at 1 km.
- Items D1 to D9 do not move the design toward TRL 4. No hardware, test or build work follows from them in this session.
