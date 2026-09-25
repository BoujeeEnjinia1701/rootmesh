"""RootMesh concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. One sensor stake stands at the origin with the soil surface (grade) at Z = 0,
the head above grade and the sensor fin below it. X points toward the equator (the solar panel
tilts that way), Z is up. The LoRaWAN gateway (BOM 13) sits indoors at the farmhouse and is not
modeled. Context parts (grey person, soil block cut away around the stake) appear in the hero only.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Cone, Pos, Rot
from concept import Part, render_all, human_figure

GRADE = 0.0
TUBE_OD, TUBE_ID = 42.0, 36.0         # 40 mm (1-1/4 in) PVC pressure pipe
TUBE_TOP, TUBE_BOT = 50.0, -120.0
HEAD_R, HEAD_Z0, HEAD_H = 36.0, 40.0, 110.0
TILT = 30.0                            # panel tilt, degrees
FIN_W, FIN_T = 36.0, 12.0              # sensor fin cross-section
FIN_TOP, FIN_BOT = -110.0, -420.0
SHALLOW, DEEP = -150.0, -300.0         # moisture sensing centers (150 mm and 300 mm deep)
PROBE_L = 80.0                         # exposed sensing length of each capacitive blade


def tube(r_out, r_in, z0, z1):
    h = z1 - z0
    return Pos(0, 0, z0 + h / 2) * (Cylinder(r_out, h) - Cylinder(r_in, h + 2))


# 2 Head enclosure: printed ASA cup with a sloped top that carries the panel
head_h_total = HEAD_H + 30
head = Pos(0, 0, HEAD_Z0 + head_h_total / 2) * Cylinder(HEAD_R, head_h_total)
slope_cut = Pos(0, 0, HEAD_Z0 + HEAD_H) * Rot(0, -TILT, 0) * Pos(0, 0, 60) * Box(300, 300, 120)
head = head - slope_cut
head = head - Pos(0, 0, HEAD_Z0 + 56) * Cylinder(HEAD_R - 3, 80)          # hollow for the electronics
head = head - Pos(0, 0, HEAD_Z0 + 12) * Cylinder(14, 20)                  # cable pass-through from the tube
head = head - Pos(0, 0, HEAD_Z0 + 5) * Cylinder(TUBE_OD / 2 + 0.5, 12)     # socket over the tube

# 1 Solar panel, 0.5 W, about 70 x 50 mm, lying on the slope
panel = (Pos(0, 0, HEAD_Z0 + HEAD_H) * Rot(0, -TILT, 0) * Pos(0, 0, 1.6) * Box(70, 50, 3.2))

# 3 Controller board: LoRa module (STM32WL class) on a carrier with the solar charger and sensor interface,
#   standing upright in the head
pcb_z = HEAD_Z0 + 42
controller = Pos(0, 0, pcb_z) * Box(56, 1.6, 40) + Pos(-10, -3.2, pcb_z + 4) * Box(20, 4.8, 16)

# 4 Antenna, quarter-wave whip on the high side of the head
ant_x, ant_y = -10.0, 30.0                 # beside the panel, on the sloped top
ant_base = HEAD_Z0 + HEAD_H + ant_x * 0.577 - 2   # slope surface at ant_x (30 degree tilt)
antenna = Pos(ant_x, ant_y, ant_base + 70) * Cylinder(4, 120) + Pos(ant_x, ant_y, ant_base + 5) * Cylinder(5, 10)

# 5 LiFePO4 cell (14500 size) in the tube below grade, where the soil keeps it cooler
cell = Pos(0, 0, -62) * Cylinder(7.25, 50) + Pos(0, 0, -62) * (Cylinder(11, 50) - Cylinder(7.5, 52))

# 6 Stake tube, PVC
stake_tube = tube(TUBE_OD / 2, TUBE_ID / 2, TUBE_BOT, TUBE_TOP)

# 7 Sensor fin: printed carrier with windows so each blade touches soil on both faces
fin_h = FIN_TOP - FIN_BOT
fin = Pos(0, 0, FIN_BOT + fin_h / 2) * Box(FIN_W, FIN_T, fin_h)
fin = fin + Pos(0, 0, FIN_TOP + 5) * Cylinder(TUBE_ID / 2 - 0.3, 30)      # spigot into the tube
for zc in (SHALLOW, DEEP):
    fin = fin - Pos(0, 0, zc) * Box(FIN_W - 8, FIN_T + 2, PROBE_L)
tip = Pos(0, 0, FIN_BOT - 15) * Rot(0, 0, 0) * Cone(FIN_T / 2 + 6, 3, 30)
fin = fin + tip

# 8 Capacitive moisture probes (two), edge-on in the fin windows
probes = None
for zc in (SHALLOW, DEEP):
    b = Pos(0, 0, zc) * Box(23, 1.6, PROBE_L + 10)
    probes = b if probes is None else probes + b

# 9 EC electrodes: two 316 stainless rods below the fin tip
ec = None
for dx in (-12.0, 12.0):
    r = Pos(dx, 0, FIN_BOT - 30) * Cylinder(2.0, 60) + Pos(dx, 0, FIN_BOT - 60) * Cone(2.0, 0.3, 6)
    ec = r if ec is None else ec + r

# 10 DS18B20 probe, stainless sheath on the fin edge at 200 mm depth
temp = Pos(FIN_W / 2 + 3.5, 0, -225) * Cylinder(3.5, 50)

# 11 Marker rod and flag, fiberglass, pushed in beside the stake (visibility for machinery)
rod_x = -60.0
marker = Pos(rod_x, 0, 425) * Cylinder(4, 1150) + Pos(rod_x - 76, 0, 950) * Box(140, 2, 90)

# 12 Seals: O-ring and gland at the head joint
seals = Pos(0, 0, HEAD_Z0 + 13) * (Cylinder(TUBE_OD / 2 + 2.5, 3) - Cylinder(TUBE_OD / 2 - 0.2, 4))

parts = [
    Part("Solar panel, 0.5 W", panel, "#1E3A8A", 1, (0, 0, 170)),
    Part("Head enclosure, printed ASA", head, "#E5E7EB", 2, (0, 0, 90)),
    Part("Controller board, LoRa module and charger", controller, "#16A34A", 3, (190, 0, 60)),
    Part("Antenna, quarter-wave whip", antenna, "#374151", 4, (-90, 0, 220)),
    Part("LiFePO4 cell, 600 mAh", cell, "#C2410C", 5, (190, 0, -50)),
    Part("Stake tube, 40 mm PVC", stake_tube, "#D1D5DB", 6, (0, 0, 0)),
    Part("Sensor fin, printed", fin, "#94A3B8", 7, (0, 0, -60)),
    Part("Capacitive moisture probes (2)", probes, "#7C3AED", 8, (190, 0, -70)),
    Part("EC electrodes, 316 stainless", ec, "#D4A017", 9, (0, 0, -120)),
    Part("DS18B20 temperature probe", temp, "#2563EB", 10, (-170, 0, -60)),
    Part("Marker rod and flag", marker, "#EA580C", 11, (-300, 0, -330)),
    Part("Seals and cable gland", seals, "#111827", 12, (-170, 0, 60)),
]

# Context for the hero only: a soil block cut away around the stake, and a 1.75 m person on the soil
soil = Pos(200, 150, -260) * Box(1300, 900, 520)
soil = soil - Pos(-90 + 750, 60 - 450, -250) * Box(1500, 900, 600)        # open the quadrant facing the camera
soil = soil - Pos(0, 0, -260) * Cylinder(60, 600)                           # auger hole around the stake
person = human_figure(1750.0, x=600.0, y=380.0, z=GRADE)
context = [Part("Soil block, cut away", soil, "#B7A58E"), person]

render_all(
    parts, project="RootMesh", title="Soil sensor stake concept", dwg_no="RMS-DWG-010",
    key_figures=["Moisture at 150 and 300 mm, EC and temperature",
                 "LoRaWAN uplink every 20 min at SF10 (about 0.37 s)",
                 "About 2 mAh/day; 600 mAh cell, about 240 days dark (estimate)",
                 "0.5 W panel; harvest about 70 x daily use (estimate)",
                 "Pilot set: 3 stakes and gateway about $246 (indicative)"],
    scale_figure=False, context=context, cut_exclude=("Marker rod and flag", "Antenna, quarter-wave whip"),
    flow={"title": "data flow, soil to irrigation decision (estimates)", "unit": "",
          "stages": [("Root-zone soil", "2 depths, EC, temp"), ("Stake reading", "every 20 min"),
                     ("LoRaWAN uplink", "about 24 B, SF10"), ("Gateway", "up to 1 km (to test)"),
                     ("Network server", "TTN or local"), ("Dashboard", "depletion vs threshold"),
                     ("Irrigation decision", "grower")]},
)
