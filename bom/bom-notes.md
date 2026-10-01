# BOM notes

`bom.csv` prices one **pilot set**: three sensor stakes and one gateway, which is how the USD 300 value-engineering target (`budget_usd`, a hypothetical control target, not a limit) is read (decided by Amish, 2026-09-25; RMS-DDR-001, D4). Quantities are for the whole set; the notes column gives the count per stake. Rows 1 to 12 match the numbered callouts in `media/exploded.png`. Rows 13 to 16 (gateway, dashboard, slot tool, and head fixings and bonding) are not in the exploded view. Every row is priced.

| Group | Indicative cost |
| --- | --- |
| One stake (rows 1 to 12 and 16) | $59.00 |
| Three stakes | $177.00 |
| Gateway (row 13) | $90.00 |
| Slot tool (row 15), one per set | $14.00 |
| **Pilot set total** | **$281.00** (value-engineering target USD 300; USD 19 under the target) |

The totals are computed from `bom.csv` by `docs/04-calcs/sizing.py` (RMS-CAL-001, [H1]).

Changes at TRL 3: row 4 is now the antenna and feed on the marker rod (sleeve dipole, 1.2 m RG174 lead, gland and clip, $7.00 instead of $4.00; RMS-DDR-001, D2), and row 12 adds an ePTFE vent membrane ($5.00 instead of $4.50; RMS-CAL-001, section F).

Change on 2026-09-25 after Amish accepted the recommendations (RMS-DDR-002): row 15 adds a steel slot tool ($10.00, one per pilot set) that pre-cuts the fin path so the fin needs less push force (RMS-CAL-001 v0.2, section G). The pilot set rises from $256.50 to $266.50.

Change on 2026-10-01 for the constructable design (RMS-DDR-003): row 2 is now a printed head body and cap ($3.50, was $3.00); row 7 is a fin printed in two halves ($3.00, was $2.50); rows 4, 5, 11 and 12 re-described (antenna clips, cell holder, cable ties, 64 x 2 mm O-ring and M8 gland); row 15 adds a cross-hole handle with two shaft collars and a thumb-screw depth stop ($14.00, was $10.00); new row 16 carries the heat-set inserts, cap screws, sealing washers, epoxy, heat-shrink and prototype board ($2.50 per stake). One stake rises from $55.50 to $59.00 and the pilot set from $266.50 to $281.00.

All prices are indicative 2026 retail estimates in USD for single or small quantities, without shipping or tax. Suppliers are named where known and otherwise given as a supplier type. Printed parts are costed as material only. Tools (3D printer, soldering iron, hand auger) are not included.
