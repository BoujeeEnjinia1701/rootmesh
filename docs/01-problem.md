---
doc_id: RMS-PRB-001
title: RootMesh problem statement
project: RootMesh
doc_type: Problem statement
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem, users, context, constraints, out of scope, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions (RMS-DDR-001) on the budget reading, power and network; update open questions
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: First users and region (US915; Texas A&M AgriLife Extension as first candidate), as decided by Amish on 2026-10-02
---

# RootMesh problem statement

Most small growers decide when and how much to irrigate by feel, by the look of the crop or by the calendar, because field-ready soil sensors that report wirelessly cost $150 to $600 or more per measurement point. A sensor stake that measures root-zone moisture, temperature and salinity for about $56 in parts, runs on a small solar panel and reports over LoRaWAN to one gateway at the farmhouse would put measured soil data within reach of farms that cannot justify commercial systems.

## The problem

Agriculture uses about 70 % of global freshwater withdrawals ([Our World in Data, "Water Use and Stress"](https://ourworldindata.org/water-use-stress)), so how well irrigation is scheduled matters for water, energy and yield. Scheduling with soil water sensors works: a systematic review of U.S. studies found that sensor-based scheduling used about 38 % less water than traditional scheduling and about 20 % less than evapotranspiration replacement, with similar or larger yields ([Datta and Taghvaeian 2023, *Agricultural Water Management* 278](https://www.sciencedirect.com/science/article/pii/S0378377423000136)). Yet in most U.S. states fewer than 25 % of irrigated farms report using soil moisture sensors to decide when to irrigate ([Ogallala Water CAP, citing the USDA NASS Irrigation and Water Management Survey](https://ogallalawater.org/soil-moisture-monitoring/)). Adoption is lower still on small farms and outside high-income countries.

Three gaps keep sensors out of the field:

1. **Cost per point.** A research-grade moisture, temperature and EC sensor such as the METER TEROS 12 sells for about $620 without a logger ([TEquipment listing](https://www.tequipment.net/HOBO-by-Onset/TEROS-12-US/Moisture-Meters/)). Even a low-cost commercial LoRaWAN node such as the Dragino SE01-LB or SE01-LS costs about $150 to $170 ([Choovio listing](https://www.choovio.com/product/se01-lb-lorawan-soil-moisture-ec-sensor/)). A field needs several points to capture variation in soil and slope, so the total quickly exceeds what a small grower will spend.
2. **Field hardiness of cheap parts.** The hobby capacitive moisture boards that cost a few dollars are not built for burial: the stock NE555 timer is unreliable at 3.3 V, the onboard regulator drops out below about 3.4 V, the cut board edges absorb water and corrode within weeks, and the output drifts with temperature ([Cave Pearl Project 2020](https://thecavepearlproject.org/2020/10/27/hacking-a-capacitive-soil-moisture-sensor-for-frequency-output/)). Garden-grade sensors therefore fail before a season ends.
3. **Calibration and interpretation.** Factory calibrations for capacitance sensors carry about three times the error of a site-specific calibration, and growers rarely have the means to calibrate ([Datta and Taghvaeian 2023](https://www.sciencedirect.com/science/article/pii/S0378377423000136)). Raw numbers without a threshold also do not tell a grower whether to irrigate today.

RootMesh aims to close all three: a stake built from low-cost parts but designed for burial, with a simple field calibration routine and a dashboard that shows root-zone depletion against a threshold the grower sets.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Small grower (vegetables, fruit, field crops, about 0.5 to 10 ha) | Know when the root zone is drying and how deep water has reached, without walking every bed | Drip, furrow or sprinkler irrigation; phone in hand; limited budget |
| Orchard or vineyard manager | Track deep moisture and salinity through the season in a few representative blocks | Perennial crops, stakes stay in place for months |
| Market or community garden coordinator | Share one gateway across many plots and volunteers | Mixed crops, public site, risk of tampering |
| Extension agent or researcher | Deploy many cheap points to map variation and teach irrigation scheduling | Short trials, needs raw data export |
| Farm technician | Install, calibrate, move and repair stakes with hand tools | Hand auger, multimeter, basic soldering |

### Operating environment

- **Soil:** sand to clay loam, with stones; volumetric water content from about 5 % (dry sand) to 50 % (saturated clay); bulk soil EC up to a few dS/m in saline or heavily fertigated fields.
- **Depth of interest:** the main root zone of most vegetable and field crops, about 100 to 400 mm.
- **Climate:** air from -10 to 45 °C; a dark enclosure in full sun can reach 60 to 70 °C (estimate); rain, irrigation spray, flooding of furrows; freezing topsoil in winter in temperate regions.
- **Radio path:** one gateway at the farmhouse or a shed, typically 100 m to 1 km from the stakes, with crops, trees and buildings in the path; stakes sit close to the ground.
- **Operations:** tillage, cultivation, mowing and harvest machinery pass the stakes; livestock and people may disturb them.
- **Power:** no mains in the field; sun on the stake head may be shaded by the crop canopy late in the season.

## Constraints

- Garage-buildable prototype. The project budget is $300 USD for a pilot set of three stakes and one gateway (decided by Amish, 2026-09-25; RMS-DDR-001, D4).
- Parts available from general electronics retailers; enclosure parts printable or from a hardware store.
- No mains power in the field; solar harvest with a small rechargeable LiFePO4 cell (RMS-DDR-001, D1 and D5).
- Operate within license-free radio rules for the region (for example ETSI EN 300 220 duty cycles in Europe, FCC Part 15 in the United States) and within The Things Network fair use policy if the free community network server is used ([The Things Network, "Duty Cycle"](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/)).
- The grower owns the data. The system must work without a paid cloud subscription. The pilot uses The Things Network's free community server (RMS-DDR-001, D3).
- Removable by hand before tillage or harvest, and reinstallable at the same depth.

## Out of scope

- Automatic valve or pump control. RootMesh informs the irrigation decision; it does not actuate irrigation at this stage.
- Nutrient (N, P, K) or pH sensing.
- Satellite or drone moisture products.
- Crop models or yield prediction beyond a simple root-zone depletion view.
- A new radio protocol or a new gateway design.

## Prior work

- **Commercial LoRaWAN soil nodes.** Dragino LSE01 and SE01 measure moisture, temperature and EC with an FDR probe in an IP66 enclosure, on a primary Li-SOCl2 cell or a solar panel with a Li-ion cell ([Dragino LSE01](https://www.dragino.com/products/lora-lorawan-end-node/item/159-lse01.html); [Choovio SE01 listing](https://www.choovio.com/product/se01-lb-lorawan-soil-moisture-ec-sensor/)). They prove the architecture and set the price reference, but measure at one depth and are closed designs.
- **Research-grade sensors.** METER TEROS 12 and similar sensors set the accuracy reference for moisture, EC and temperature at about $620 per sensor ([TEquipment listing](https://www.tequipment.net/HOBO-by-Onset/TEROS-12-US/Moisture-Meters/)).
- **Hacked hobby capacitive sensors.** The Cave Pearl Project documents how to make the v1.2 capacitive board usable in the field: swap the NE555 for a TLC555, bypass the regulator, read frequency and seal the edges in epoxy ([Cave Pearl Project 2020](https://thecavepearlproject.org/2020/10/27/hacking-a-capacitive-soil-moisture-sensor-for-frequency-output/)). RootMesh adopts these fixes.
- **Capacitance sensor behavior.** Low-cost capacitance sensors respond to soil EC and temperature as well as water, more strongly at low measurement frequency ([Kizito et al. 2008, *Journal of Hydrology*](https://www.sciencedirect.com/science/article/abs/pii/S0022169408000462)). This is a reason to measure EC and temperature at the same point.
- **Irrigation scheduling methods.** FAO Irrigation and Drainage Paper 56 defines root-zone depletion and management allowed depletion, the basis for a simple "irrigate now" threshold ([Allen et al. 1998, FAO-56](https://www.fao.org/4/x0490e/x0490e00.htm)). FAO Paper 29 gives crop salinity tolerance thresholds in terms of soil EC ([Ayers and Westcot 1985, FAO-29](https://www.fao.org/4/t0234e/t0234e00.htm)).
- **Community LoRaWAN.** The Things Network offers a free community network server with a fair use limit of 30 s of uplink airtime per node per day ([The Things Network, "Duty Cycle"](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/)), and low-cost indoor gateways such as The Things Indoor Gateway sell for about $79 ([Seeed Studio listing](https://www.seeedstudio.com/The-Things-Indoor-Gateway-EU-p-4709.html)).

## Open questions

- Which first users and region: a market garden, an orchard, a university research farm or an extension program? This also sets EU868 or US915. Decided by Amish on 2026-10-02: a US university extension program with a research farm, on US915, with Texas A&M AgriLife Extension as the first candidate to approach (RMS-DEC-001).
- Is one indoor gateway enough for the fields of the first users? With the antenna on the marker rod the link closes at 1 km on paper (RMS-CAL-001), but tall crops such as maize or orchard rows may need an outdoor gateway.
- Do growers want a simple "irrigate now" signal, a depletion chart, or both?
- How often must stakes come out for tillage or harvest, and how quickly must they go back in?
- Is EC (salinity) valued by the first users, or does it add cost for little use in their fields?
