# BOM notes

`bom.csv` prices one **pilot set**: three sensor stakes and one gateway, which is how the $300 budget is read (decided by Amish, 2026-09-25; RMS-DDR-001, D4). Quantities are for the whole set; the notes column gives the count per stake. Rows 1 to 12 match the numbered callouts in `media/exploded.png`. Rows 13 and 14 (gateway and dashboard) are not in the exploded view. Every row is priced.

| Group | Indicative cost |
| --- | --- |
| One stake (rows 1 to 12) | $55.50 |
| Three stakes | $166.50 |
| Gateway (row 13) | $90.00 |
| **Pilot set total** | **$256.50** (budget $300, headroom $43.50) |

The totals are computed from `bom.csv` by `docs/04-calcs/sizing.py` (RMS-CAL-001, [H1]).

Changes at TRL 3: row 4 is now the antenna and feed on the marker rod (sleeve dipole, 1.2 m RG174 lead, gland and clip, $7.00 instead of $4.00; RMS-DDR-001, D2), and row 12 adds an ePTFE vent membrane ($5.00 instead of $4.50; RMS-CAL-001, section F).

All prices are indicative 2026 retail estimates in USD for single or small quantities, without shipping or tax. Suppliers are named where known and otherwise given as a supplier type. Printed parts are costed as material only. Tools (3D printer, soldering iron, hand auger) are not included.
