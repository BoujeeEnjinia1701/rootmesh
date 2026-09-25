"""RootMesh parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    rootmesh-stake-assembly.step / .stl   one installed stake with marker rod and antenna
    head-enclosure.step / .stl            printed ASA head (panel seat, socket, gland and vent bosses)
    sensor-fin.step / .stl                printed fin with spigot, probe windows and tip
    stake-tube.step / .stl                PVC tube, 42 mm OD

Axes: one stake at the origin, soil surface (grade) at z = 0, Z up. X points toward the
equator (the panel tilts that way), the marker rod stands on -X. Main dimensions and
interfaces only: tube and socket diameters, spigot, sensing depths, electrode spacing,
panel tilt, head height, cell position, antenna height on the marker rod. Not fabrication
detail; not for fabrication. The same PARAMS feed docs/04-calcs/sizing.py (RMS-CAL-001),
the drawing RMS-DWG-001 (cad/src/sheets.py) and the concept media (cad/src/concept_media.py).
The LoRaWAN gateway (BOM 13) sits indoors at the farmhouse and is not modeled.
"""
import math
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # stake tube: 40 mm (1-1/4 in) PVC pressure pipe
    "tube_od": 42.0, "tube_id": 36.0, "tube_top": 50.0, "tube_bot": -120.0,
    # head enclosure, printed ASA
    "head_r": 36.0, "head_z0": 40.0, "head_h": 110.0, "wall": 3.0, "tilt": 30.0,
    "socket_depth": 12.0,
    # solar panel, 5 V 0.5 W
    "panel": (70.0, 50.0, 3.2),
    # controller carrier board (Wio-E5 module on a carrier)
    "pcb": (56.0, 1.6, 40.0), "pcb_z": 82.0,
    # LiFePO4 14500 cell in the tube, below grade
    "cell_d": 14.5, "cell_l": 50.0, "cell_z": -62.0,
    # sensor fin
    "fin_w": 36.0, "fin_t": 12.0, "fin_top": -110.0, "fin_bot": -420.0, "tip_l": 30.0,
    "spigot_l": 30.0,
    # moisture sensing: window centers and blade length
    "depths": (150.0, 300.0), "probe_l": 80.0, "probe_w": 23.0, "probe_t": 1.6,
    # EC electrodes: 316 stainless rods below the fin tip
    "ec_d": 4.0, "ec_pitch": 24.0, "ec_exposed": 60.0,
    # DS18B20 in a 6 mm sheath on the fin edge
    "t_depth": 225.0, "t_d": 7.0, "t_l": 50.0,
    # marker rod, flag and antenna (Amish decision RMS-DDR-001 D2: antenna at about 1 m on the rod)
    "rod_x": -60.0, "rod_d": 8.0, "rod_len": 1200.0, "rod_bury": 200.0,
    "flag": (140.0, 2.0, 90.0), "flag_z": 840.0,
    "ant_len": 172.0, "ant_d": 10.0, "ant_center_z": 1000.0,   # half-wave sleeve dipole, 868 MHz
    "coax_d": 3.0, "coax_z": 120.0,
}


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    t = math.tan(math.radians(p["tilt"]))
    slope_z = p["head_z0"] + p["head_h"]                   # slope plane height on the axis
    head_top = slope_z + p["head_r"] * t                    # highest point, on the -X side
    head_low = slope_z - p["head_r"] * t
    rod_top = p["rod_len"] - p["rod_bury"]
    fin_len = p["fin_top"] - p["fin_bot"]
    tip_z = p["fin_bot"] - p["tip_l"]
    ec_top = p["fin_bot"] - 5.0
    ec_bot = ec_top - p["ec_exposed"]
    return {
        "slope_z": slope_z, "head_top": head_top, "head_low": head_low, "rod_top": rod_top,
        "fin_len": fin_len, "tip_z": tip_z, "ec_top": ec_top, "ec_bot": ec_bot,
        "ant_top": p["ant_center_z"] + p["ant_len"] / 2, "ant_bot": p["ant_center_z"] - p["ant_len"] / 2,
        "ec_gap": p["ec_pitch"] - p["ec_d"],
        "cell_top": p["cell_z"] + p["cell_l"] / 2,
        "head_air_l": math.pi * (p["head_r"] - p["wall"]) ** 2 * (p["head_h"] - 20) / 1e6,  # litres
        "fin_section_mm2": p["fin_w"] * p["fin_t"],
        "fin_perimeter_mm": 2 * (p["fin_w"] + p["fin_t"]),
        "push_depth": p["tube_bot"] - tip_z,                # depth pushed into undisturbed soil below the auger hole
        "overall_h": rod_top - ec_bot,
    }


def _tube(r_out, r_in, z0, z1):
    from build123d import Cylinder, Pos
    h = z1 - z0
    return Pos(0, 0, z0 + h / 2) * (Cylinder(r_out, h) - Cylinder(r_in, h + 2))


def build_parts(p=PARAMS):
    """Return {name: (shape, color, bom)} for every modeled part."""
    from build123d import Box, Cylinder, Cone, Pos, Rot
    d = derived(p)
    z0, R, tilt = p["head_z0"], p["head_r"], p["tilt"]
    parts = {}

    # 2 Head enclosure: printed ASA cup, sloped top, socket over the tube, gland and vent bosses
    hh = p["head_h"] + 40
    head = Pos(0, 0, z0 + hh / 2) * Cylinder(R, hh)
    head -= Pos(0, 0, d["slope_z"]) * Rot(0, tilt, 0) * Pos(0, 0, 80) * Box(400, 400, 160)
    head -= Pos(0, 0, z0 + 56) * Cylinder(R - p["wall"], 80)               # electronics cavity
    head -= Pos(0, 0, z0 + p["socket_depth"] + 4) * Cylinder(14, 20)        # cable pass-through
    head -= Pos(0, 0, z0 + p["socket_depth"] / 2) * Cylinder(p["tube_od"] / 2 + 0.5, p["socket_depth"] + 0.01)
    gland = Pos(-R - 4, 0, p["coax_z"]) * Rot(0, 90, 0) * Cylinder(6, 10)    # coax gland boss, -X side
    vent = Pos(0, R + 3, z0 + 30) * Rot(90, 0, 0) * Cylinder(5, 7)           # ePTFE vent boss, +Y side
    parts["head"] = (head + gland + vent, "#E5E7EB", 2)

    # 1 Solar panel on the slope
    pw, pl, pt = p["panel"]
    parts["panel"] = (Pos(0, 0, d["slope_z"]) * Rot(0, tilt, 0) * Pos(0, 0, pt / 2) * Box(pw, pl, pt), "#1E3A8A", 1)

    # 3 Controller board, upright in the head
    bx, by, bz = p["pcb"]
    parts["controller"] = (Pos(0, 0, p["pcb_z"]) * Box(bx, by, bz)
                           + Pos(-10, -3.2, p["pcb_z"] + 4) * Box(20, 4.8, 16), "#16A34A", 3)

    # 4 Antenna: half-wave sleeve dipole clipped to the top of the marker rod, coax to the head
    rx, rc = p["rod_x"], p["rod_d"] / 2
    ax = rx + rc + p["ant_d"] / 2 + 1
    ant = Pos(ax, 0, p["ant_center_z"]) * Cylinder(p["ant_d"] / 2, p["ant_len"])
    ant += Pos(ax - 3, 0, d["rod_top"] - 30) * Box(12, 12, 16)              # rod clip
    run_up = d["ant_bot"] - p["coax_z"]
    coax = Pos(ax, 0, p["coax_z"] + run_up / 2) * Cylinder(p["coax_d"] / 2, run_up)
    span = (-R - 9) - ax
    coax += Pos(ax + span / 2, 0, p["coax_z"]) * Rot(0, 90, 0) * Cylinder(p["coax_d"] / 2, abs(span))
    parts["antenna"] = (ant + coax, "#374151", 4)

    # 5 LiFePO4 cell with holder, in the tube below grade
    parts["cell"] = (Pos(0, 0, p["cell_z"]) * Cylinder(p["cell_d"] / 2, p["cell_l"])
                     + Pos(0, 0, p["cell_z"]) * (Cylinder(11, p["cell_l"]) - Cylinder(p["cell_d"] / 2 + 0.25, p["cell_l"] + 2)),
                     "#C2410C", 5)

    # 6 Stake tube
    parts["tube"] = (_tube(p["tube_od"] / 2, p["tube_id"] / 2, p["tube_bot"], p["tube_top"]), "#D1D5DB", 6)

    # 7 Sensor fin with spigot into the tube, two windows and a pointed tip
    fl = d["fin_len"]
    fin = Pos(0, 0, p["fin_bot"] + fl / 2) * Box(p["fin_w"], p["fin_t"], fl)
    fin += Pos(0, 0, p["fin_top"] + p["spigot_l"] / 2 - 10) * Cylinder(p["tube_id"] / 2 - 0.3, p["spigot_l"])
    for dz in p["depths"]:
        fin -= Pos(0, 0, -dz) * Box(p["fin_w"] - 8, p["fin_t"] + 2, p["probe_l"])
    fin += Pos(0, 0, p["fin_bot"] - p["tip_l"] / 2) * Cone(p["fin_t"] / 2 + 6, 3, p["tip_l"])
    parts["fin"] = (fin, "#94A3B8", 7)

    # 8 Two capacitive probes, edge-on in the windows
    probes = None
    for dz in p["depths"]:
        b = Pos(0, 0, -dz) * Box(p["probe_w"], p["probe_t"], p["probe_l"] + 10)
        probes = b if probes is None else probes + b
    parts["probes"] = (probes, "#7C3AED", 8)

    # 9 EC electrodes, held in the fin foot either side of the tip
    ec = None
    L = p["ec_exposed"]
    for dx in (-p["ec_pitch"] / 2, p["ec_pitch"] / 2):
        r = Pos(dx, 0, d["ec_top"] - L / 2 + 2) * Cylinder(p["ec_d"] / 2, L - 4) \
            + Pos(dx, 0, d["ec_bot"] + 2) * Cone(p["ec_d"] / 2, 0.3, 4)
        r += Pos(dx, 0, p["fin_bot"] + 10) * Cylinder(p["ec_d"] / 2, 20)     # embedded length in the fin foot
        ec = r if ec is None else ec + r
    parts["ec"] = (ec, "#D4A017", 9)

    # 10 DS18B20 probe on the fin edge
    parts["temp"] = (Pos(p["fin_w"] / 2 + p["t_d"] / 2, 0, -p["t_depth"]) * Cylinder(p["t_d"] / 2, p["t_l"]), "#2563EB", 10)

    # 11 Marker rod and flag
    rod = Pos(rx, 0, d["rod_top"] - p["rod_len"] / 2) * Cylinder(rc, p["rod_len"])
    fw, ft, fh = p["flag"]
    rod += Pos(rx - rc - fw / 2, 0, p["flag_z"]) * Box(fw, ft, fh)
    parts["marker"] = (rod, "#EA580C", 11)

    # 12 Seals: O-ring at the head joint (gland and vent are bosses on the head)
    od = p["tube_od"]
    parts["seals"] = (Pos(0, 0, z0 + p["socket_depth"] + 1) * (Cylinder(od / 2 + 2.5, 3) - Cylinder(od / 2 - 0.2, 4)),
                      "#111827", 12)
    return parts


NAMES = {"panel": "Solar panel, 0.5 W", "head": "Head enclosure, printed ASA",
         "controller": "Controller board, Wio-E5 and charger", "antenna": "Antenna on marker rod, with coax",
         "cell": "LiFePO4 cell, 600 mAh", "tube": "Stake tube, 40 mm PVC", "fin": "Sensor fin, printed",
         "probes": "Capacitive moisture probes (2)", "ec": "EC electrodes, 316 stainless",
         "temp": "DS18B20 temperature probe", "marker": "Marker rod and flag", "seals": "Seals, gland and vent"}


def assembly(p=PARAMS):
    from build123d import Compound
    parts = build_parts(p)
    kids = []
    for k, (s, _, _) in parts.items():
        s.label = NAMES[k]
        kids.append(s)
    return Compound(children=kids)


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    asm = assembly()
    exports = {"rootmesh-stake-assembly": asm, "head-enclosure": parts["head"][0],
               "sensor-fin": parts["fin"][0], "stake-tube": parts["tube"][0]}
    for name, shape in exports.items():
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"))
    d = derived()
    bb = asm.bounding_box()
    print(f"assembly bounding box {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print(f"head top {d['head_top']:.1f} mm above grade; antenna {d['ant_bot']:.0f} to {d['ant_top']:.0f} mm; "
          f"rod top {d['rod_top']:.0f} mm; EC tips {d['ec_bot']:.0f} mm")
    for k, (s, _, _) in parts.items():
        print(f"  {k:<11} volume {s.volume / 1000:8.1f} cm3")
    print("exported:", ", ".join(exports))
