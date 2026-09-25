"""RootMesh concept media (TRL 3), generated from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Parts, colors and BOM numbers come from model.build_parts(); figures on the sheet and in the
flow diagram come from docs/04-calcs/sizing.py (RMS-CAL-001). Not for fabrication.

Coordinates in mm. One sensor stake stands at the origin with the soil surface (grade) at Z = 0,
the head above grade and the sensor fin below it. X points toward the equator (the solar panel
faces that way), Z is up; the marker rod, with the antenna at about 1 m, stands on -X. The
LoRaWAN gateway (BOM 13) sits indoors at the farmhouse and is not modeled. Context parts (grey person, soil block cut away around the stake) appear in the hero only.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Cylinder, Pos  # noqa: E402
from concept import Part, render_all, human_figure  # noqa: E402
from model import NAMES, build_parts  # noqa: E402

GRADE = 0.0
m = build_parts()
EXPLODE = {"panel": (0, 0, 170), "head": (0, 0, 90), "controller": (190, 0, 60), "antenna": (-120, 0, 120),
           "cell": (190, 0, -50), "tube": (0, 0, 0), "fin": (0, 0, -60), "probes": (190, 0, -70),
           "ec": (0, 0, -120), "temp": (-170, 0, -60), "marker": (-300, 0, -330), "seals": (-170, 0, 60)}
parts = [Part(NAMES[k], shape, color, bom, EXPLODE[k]) for k, (shape, color, bom) in m.items()]
parts.sort(key=lambda p: p.bom)

# Context for the hero only: a soil block cut away around the stake, and a 1.75 m person on the soil
soil = Pos(200, 150, -260) * Box(1300, 900, 520)
soil = soil - Pos(-90 + 750, 60 - 450, -250) * Box(1500, 900, 600)        # open the quadrant facing the camera
soil = soil - Pos(0, 0, -260) * Cylinder(60, 600)                           # auger hole around the stake
person = human_figure(1750.0, x=600.0, y=380.0, z=GRADE)
context = [Part("Soil block, cut away", soil, "#B7A58E"), person]

render_all(
    parts, project="RootMesh", title="Soil sensor stake concept", dwg_no="RMS-DWG-010", date="2026-09-25",
    key_figures=["Moisture at 150 and 300 mm, EC and temperature",
                 "LoRaWAN every 20 min at SF10: 0.37 s, 26.7 s/day",
                 "About 2.6 mAh/day; about 186 days dark (RMS-CAL-001)",
                 "Antenna at 1 m: 13.5 dB margin at 1 km (estimate)",
                 "Pilot set: 3 stakes and gateway $256.50 (indicative)"],
    scale_figure=False, context=context, cut_exclude=(NAMES["marker"], NAMES["antenna"]),
    flow={"title": "data flow, soil to irrigation decision (estimates)", "unit": "",
          "stages": [("Root-zone soil", "2 depths, EC, temp"), ("Stake reading", "every 20 min"),
                     ("LoRaWAN uplink", "about 24 B, SF10"), ("Gateway", "1 km, 13.5 dB (est.)"),
                     ("Network server", "TTN (pilot)"), ("Dashboard", "depletion vs threshold"),
                     ("Irrigation decision", "grower")]},
)
