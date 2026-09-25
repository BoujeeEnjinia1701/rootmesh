# RootMesh

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Agriculture · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $300 USD · **Difficulty:** 2 of 5

Solar-powered stakes that measure soil moisture, temperature and EC and report over LoRa to a single gateway and dashboard.

![RootMesh concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Irrigation decisions rely on guesswork without cheap, field-hardy soil sensing. Commercial wireless soil nodes cost about $150 to $600 or more per measurement point, and the cheap hobby probes corrode and drift when buried.

## Concept

Solar-powered stakes that measure soil moisture, temperature and EC and report over LoRa to a single gateway and dashboard. Each stake reads water content at 150 mm and 300 mm, bulk EC and soil temperature every 20 min, runs on a 0.5 W panel and a small LiFePO4 cell, and costs about $52 in parts. A pilot set of three stakes and an indoor gateway is about $246 (indicative).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Two capacitive moisture probes (sealed, TLC555 conversion) in a printed sensor fin
- DS18B20 temperature probe
- Stainless EC electrodes with AC excitation
- LoRaWAN module (STM32WL class) with solar charger
- 600 mAh LiFePO4 cell below grade
- 0.5 W PV panel on a printed ASA head over a PVC stake tube
- Indoor LoRaWAN gateway and open-source dashboard

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
