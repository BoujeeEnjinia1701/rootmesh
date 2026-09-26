# BOM notes

`bom.csv` prices one **pilot set**: three sensor stakes and one gateway, which is how the $300 budget is read (decided by Amish, 2026-09-25; RMS-DDR-001, D4). Quantities are for the whole set; the notes column gives the count per stake. Rows 1 to 12 match the numbered callouts in `media/exploded.png`. Rows 13 to 15 (gateway, dashboard and slot tool) are not in the exploded view. Every row is priced.

| Group | Indicative cost |
| --- | --- |
| One stake (rows 1 to 12) | $55.50 |
| Three stakes | $166.50 |
| Gateway (row 13) | $90.00 |
| Slot tool (row 15), one per set | $10.00 |
| **Pilot set total** | **$266.50** (budget $300, headroom $33.50) |

The totals are computed from `bom.csv` by `docs/04-calcs/sizing.py` (RMS-CAL-001, [H1]).

Changes at TRL 3: row 4 is now the antenna and feed on the marker rod (sleeve dipole, 1.2 m RG174 lead, gland and clip, $7.00 instead of $4.00; RMS-DDR-001, D2), and row 12 adds an ePTFE vent membrane ($5.00 instead of $4.50; RMS-CAL-001, section F).

Change on 2026-09-25 after Amish accepted the recommendations (RMS-DDR-002): row 15 adds a steel slot tool ($10.00, one per pilot set) that pre-cuts the fin path so the fin needs less push force (RMS-CAL-001 v0.2, section G). The pilot set rises from $256.50 to $266.50.

All prices are indicative 2026 retail estimates in USD for single or small quantities, without shipping or tax. Suppliers are named where known and otherwise given as a supplier type. Printed parts are costed as material only. Tools (3D printer, soldering iron, hand auger) are not included.
