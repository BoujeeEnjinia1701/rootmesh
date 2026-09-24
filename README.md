# RootMesh

**Area:** Agriculture · **Status:** Concept · **Prototype budget:** about $300 USD · **Difficulty:** 2 of 5

Solar-powered stakes that measure soil moisture, temperature and EC and report over LoRa to a single gateway and dashboard.

## Problem

Irrigation decisions rely on guesswork without cheap, field-hardy soil sensing.

## Concept

Solar-powered stakes that measure soil moisture, temperature and EC and report over LoRa to a single gateway and dashboard.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Capacitive moisture probe
- DS18B20 temperature sensor
- EC electrodes
- LoRa module
- Printed stake housing
- Small PV panel

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
