# RootMesh

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Agriculture · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $300 USD · **Difficulty:** 2 of 5

Solar-powered stakes that measure soil moisture, temperature and EC and report over LoRa to a single gateway and dashboard.

![RootMesh concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement RMS-DWG-001 (PDF)](cad/drawings/RMS-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Irrigation decisions rely on guesswork without cheap, field-hardy soil sensing. Commercial wireless soil nodes cost about $150 to $600 or more per measurement point, and the cheap hobby probes corrode and drift when buried.

## Concept

Solar-powered stakes that measure soil moisture, temperature and EC and report over LoRa to a single gateway and dashboard. Each stake reads water content at 150 mm and 300 mm, bulk EC and soil temperature every 20 min, runs on a 0.5 W panel and a small LiFePO4 cell, carries its antenna at about 1 m on the flagged marker rod, and costs about $55.50 in parts. A pilot set of three stakes and an indoor gateway is $256.50 (indicative), within the $300 budget.

The sizing note [RMS-CAL-001](docs/04-calcs/01-sizing.md) finds 8 of 14 requirements met on paper and 5 at risk: moisture accuracy, range through tall crops, head and cell temperature in bare hot soil, installation in firm dry soil and probe life. The parametric model is `cad/src/model.py` (STEP and STL in `cad/step` and `cad/stl`).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Two capacitive moisture probes (sealed, TLC555 conversion) in a printed sensor fin
- DS18B20 temperature probe
- Stainless EC electrodes with AC excitation
- LoRaWAN module (Seeed Wio-E5, STM32WLE5) with solar charger
- Sleeve dipole antenna at about 1 m on the marker rod
- 600 mAh LiFePO4 cell below grade
- 0.5 W PV panel on a printed ASA head over a PVC stake tube
- Indoor LoRaWAN gateway on The Things Network and an open-source dashboard

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (RMS-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `RMS-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
