"""RootMesh parametric model (build123d), TRL 3, constructable design (RMS-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks only

Exports:
    rootmesh-stake-assembly.step / .stl   one installed stake with marker rod and antenna
    head-body.step / .stl                 printed ASA head body (socket, cavity, board guides, bosses)
    head-cap.step / .stl                  printed ASA cap carrying the panel, sealed by an O-ring
    sensor-fin-front.step / .stl          printed fin half with the probe pockets
    sensor-fin-back.step / .stl           printed fin half, plain
    cell-holder.step / .stl               printed cell holder with two legs
    antenna-clip.step / .stl              printed clip holding the dipole on the marker rod (make 2)
    stake-tube.step / .stl                PVC tube, 42 mm OD
    slot-tool.step / .stl                 installation slot tool (BOM 15), not part of the installed stake
    slot-tool-stop.step / .stl            printed depth stop for the slot tool

Axes: one stake at the origin, soil surface (grade) at z = 0, Z up. X points toward the
equator (the panel tilts that way), the marker rod stands on -X. The front of the stake faces -Y, and
the front fin half (the one with the electronics pockets) is on that side.

The concept model (TRL 3, RMS-DDR-001 and 002) showed what the stake does. RMS-DDR-003 made it
buildable: a head body and a removable cap with an O-ring and two screws (the board could not get
into the one-piece head), the board in printed guide slots, a fin in two glued halves with probe
slots, wire channels and pockets, a collar that the tube end sits on, a cell holder standing on the
spigot, flush temperature probe, EC rods held in the fin foot, a coax gland that clears the board,
printed antenna clips, and a slot tool whose handle passes through the blade. build_components()
gives every part; build_parts() groups them by BOM line for the concept media. Not for fabrication.
The LoRaWAN gateway (BOM 13) sits indoors at the farmhouse and is not modeled.
"""
import math
import sys
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # stake tube: 40 mm (1-1/4 in) PVC pressure pipe, 170 mm, bonded into the head socket and onto the fin
    "tube_od": 42.0, "tube_id": 36.0, "tube_top": 64.0, "tube_bot": -106.0,
    # head body and cap, printed ASA; the cap parts from the body at split_z
    "head_r": 36.0, "head_z0": 40.0, "head_h": 110.0, "wall": 5.0, "tilt": 30.0,
    "socket_depth": 26.0, "split_z": 120.0, "cap_roof": 3.0,
    "boss_y": 29.5, "boss_r": 4.0, "oring": (64.0, 2.0),          # O-ring inside diameter and section
    # solar panel, 5 V 0.5 W, bonded into a 1 mm recess in the cap
    "panel": (70.0, 50.0, 3.2),
    # controller board stand-in (Wio-E5 and charger modules on a 56 x 40 prototype board), in guide slots
    "pcb": (56.0, 1.6, 40.0), "pcb_z": 96.0,
    # coax gland and vent on the head body (azimuth from +X, degrees; height)
    "gland_az": 210.0, "coax_z": 100.0, "vent_az": 45.0, "vent_z": 82.0,
    # LiFePO4 14500 cell in a printed holder standing on the fin spigot, below grade
    "cell_d": 14.5, "cell_l": 50.0, "cell_z": -62.0,
    # sensor fin, two printed halves glued on the mid-plane; collar and spigot at the top
    "fin_w": 36.0, "fin_t": 12.0, "fin_top": -110.0, "fin_bot": -420.0, "tip_l": 30.0,
    "collar_h": 4.0, "spigot_l": 11.0, "spigot_d": 35.4,
    "win_w": 19.0, "chan": (3.5, 5.0), "chan_x": 14.75,
    # moisture sensing: window centers and length; probe boards 23 x 1.6 x 100 with electronics at the top, facing -Y
    "depths": (150.0, 300.0), "probe_l": 80.0, "probe_w": 23.0, "probe_t": 1.6, "board_l": 100.0,
    # EC electrodes: 316 stainless rods, 80 mm, held 15 mm in the fin foot, 5 mm sleeved, 60 mm bare
    "ec_d": 4.0, "ec_pitch": 24.0, "ec_exposed": 60.0, "ec_len": 80.0,
    # DS18B20 in a 6 mm sheath, flush in a bore on the +X fin edge
    "t_depth": 225.0, "t_d": 6.0, "t_l": 50.0, "t_x": 15.4,
    # marker rod, flag and antenna (Amish decision RMS-DDR-001 D2: antenna at about 1 m on the rod)
    "rod_x": -60.0, "rod_d": 8.0, "rod_len": 1200.0, "rod_bury": 200.0,
    "flag": (140.0, 2.0, 90.0), "flag_z": 840.0,
    "ant_len": 172.0, "ant_d": 10.0, "ant_center_z": 1000.0,   # half-wave sleeve dipole, 868 MHz
    "coax_d": 3.0, "clip_z": (925.0, 985.0), "tie_z": (250.0, 450.0, 650.0, 900.0),
    # slot tool (BOM 15, one per pilot set; RMS-DDR-002): steel flat bar blade driven with a mallet
    # through the auger hole to pre-cut the fin and EC rod path, then withdrawn
    "slot_w": 32.0, "slot_t": 8.0, "slot_point": 40.0, "slot_top": 165.0,
    "handle_d": 20.0, "handle_l": 250.0, "handle_z": 140.0, "stop_d": 80.0, "stop_h": 15.0,
}


def derived(p=PARAMS):
    """Dimensions the calc note and drawings quote, computed from PARAMS."""
    t = math.tan(math.radians(p["tilt"]))
    slope_z = p["head_z0"] + p["head_h"]                   # slope plane height on the axis
    head_top = slope_z + p["head_r"] * t                    # highest point, on the -X side
    head_low = slope_z - p["head_r"] * t
    rod_top = p["rod_len"] - p["rod_bury"]
    fin_len = p["fin_top"] - p["fin_bot"]
    tip_z = p["fin_bot"] - p["tip_l"]
    ec_top = p["fin_bot"] - 5.0                             # bare rod starts below a 5 mm sleeve
    ec_bot = ec_top - p["ec_exposed"]
    collar_bot = p["fin_top"]
    collar_top = collar_bot + p["collar_h"]
    spigot_top = collar_top + p["spigot_l"]
    bore_r = p["head_r"] - p["wall"]
    return {
        "slope_z": slope_z, "head_top": head_top, "head_low": head_low, "rod_top": rod_top,
        "fin_len": fin_len, "tip_z": tip_z, "ec_top": ec_top, "ec_bot": ec_bot,
        "ec_rod_top": ec_bot + p["ec_len"],
        "ant_top": p["ant_center_z"] + p["ant_len"] / 2, "ant_bot": p["ant_center_z"] - p["ant_len"] / 2,
        "ec_gap": p["ec_pitch"] - p["ec_d"],
        "cell_top": p["cell_z"] + p["cell_l"] / 2,
        "bore_r": bore_r,
        "head_air_l": math.pi * bore_r ** 2 * (p["head_h"] - 20) / 1e6,  # litres
        "fin_section_mm2": p["fin_w"] * p["fin_t"],
        "fin_perimeter_mm": 2 * (p["fin_w"] + p["fin_t"]),
        "collar_bot": collar_bot, "collar_top": collar_top, "spigot_top": spigot_top,
        "cell_floor": spigot_top + 5.0 + 3.0,                # z of the holder base top: legs 5 mm, base 3 mm
        "auger_depth": -collar_bot,                          # auger hole bottom = collar bottom
        "push_depth": collar_bot - tip_z,                    # fin pushed into undisturbed soil below the auger hole
        "overall_h": rod_top - ec_bot,
        "slot_area_mm2": p["slot_w"] * p["slot_t"],
        "slot_blade_l": p["slot_top"] - ec_bot,
        "socket_bot": p["head_z0"], "socket_top": p["head_z0"] + p["socket_depth"],
        "floor_top": p["head_z0"] + p["socket_depth"] + 3.0,
    }


# ------------------------------------------------------------------------------ helpers
def _cyl(r, z0, z1, x=0.0, y=0.0):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _ring(r_in, r_out, z0, z1, x=0.0, y=0.0):
    return _cyl(r_out, z0, z1, x, y) - _cyl(r_in, z0 - 1, z1 + 1, x, y)


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _radial(r, r0, r1, az, z):
    """Cylinder of radius r along the radial line at azimuth az (deg), from radius r0 to r1, at height z."""
    from build123d import Cylinder, Pos, Rot
    return Pos(0, 0, z) * Rot(0, 0, az) * Rot(0, 90, 0) * Pos(0, 0, (r0 + r1) / 2) * Cylinder(r, r1 - r0)


def _polar(r, az):
    a = math.radians(az)
    return r * math.cos(a), r * math.sin(a)


def _slope_cut(p, drop=0.0):
    """Everything above the 30 degree slope plane (lowered by drop)."""
    from build123d import Box, Pos, Rot
    d = derived(p)
    return Pos(0, 0, d["slope_z"] - drop) * Rot(0, p["tilt"], 0) * Pos(0, 0, 80) * Box(400, 400, 160)


def on_slope(p, x, y, n):
    """Location helper: a point (x, y) on the slope plane, raised n along its normal."""
    from build123d import Pos, Rot
    d = derived(p)
    return Pos(0, 0, d["slope_z"]) * Rot(0, p["tilt"], 0) * Pos(x, y, n)


class Comp:
    def __init__(self, shape, color, bom, group, name):
        self.shape, self.color, self.bom, self.group, self.name = shape, color, bom, group, name


# ------------------------------------------------------------------------------ the components
def fin_whole(p=PARAMS):
    """The fin before it is split: blade, collar, spigot and every internal cut."""
    from build123d import Plane, Polygon, extrude
    d = derived(p)
    hw, ht = p["fin_w"] / 2, p["fin_t"] / 2
    top, bot = p["fin_top"], p["fin_bot"]
    pts = [(-hw, top), (hw, top), (hw, bot + 4), (hw - 4, bot), (8, bot), (0, bot - p["tip_l"]),
           (-8, bot), (-hw + 4, bot), (-hw, bot + 4)]
    blade = extrude(Plane.XZ * Polygon(*pts, align=None), amount=ht, both=True)
    fin = blade + _cyl(p["tube_od"] / 2, d["collar_bot"], d["collar_top"]) \
        + _cyl(p["spigot_d"] / 2, d["collar_top"], d["spigot_top"])
    ww = p["win_w"] / 2
    sw = p["probe_w"] / 2 + 0.1
    for dz in p["depths"]:
        w0, w1 = -dz - p["probe_l"] / 2, -dz + p["probe_l"] / 2
        fin -= _box(-ww, ww, -ht - 1, ht + 1, w0, w1)                               # window, both faces
        b0, b1 = w0 - 5, w0 - 5 + p["board_l"]
        fin -= _box(-sw, sw, -0.9, 0.9, b0, b1)                                    # board slot
        fin -= _box(-8, 8, -3.4, 0, w1, min(b1 + 3, d["spigot_top"] + 1))          # electronics pocket (front half, -Y)
    # cross channel from the lower probe's connector to the -X wire channel
    lw1 = -p["depths"][1] + p["probe_l"] / 2
    lb1 = lw1 - 5 - p["probe_l"] - 5 + p["board_l"]
    fin -= _box(-p["chan_x"] - p["chan"][0] / 2, 0, -1.5, 1.5, lb1, lb1 + 3)
    # wire channels in both rails, from the EC rod tops up through the spigot
    cw, cd = p["chan"]
    for sx in (-1, 1):
        fin -= _box(sx * p["chan_x"] - cw / 2, sx * p["chan_x"] + cw / 2, -cd / 2, cd / 2,
                    d["ec_rod_top"], d["spigot_top"] + 1)
    # DS18B20 bore, open to the +X edge
    fin -= _cyl(p["t_d"] / 2 + 0.1, -p["t_depth"] - p["t_l"] / 2, -p["t_depth"] + p["t_l"] / 2, x=p["t_x"])
    # EC rod grooves in the foot
    for sx in (-1, 1):
        fin -= _cyl(p["ec_d"] / 2 + 0.05, bot - 1, d["ec_rod_top"], x=sx * p["ec_pitch"] / 2)
    return fin


def build_components(p=PARAMS):
    """Every part of one installed stake, as {key: Comp}. BOM numbers follow bom/bom.csv."""
    from build123d import Box, Cone, Cylinder, Pos, Rot, Sphere
    d = derived(p)
    R, z0, zs = p["head_r"], p["head_z0"], p["split_z"]
    br = d["bore_r"]
    C = {}

    def add(key, shape, color, bom, group, name):
        C[key] = Comp(shape, color, bom, group, name)

    # ---- 6 stake tube
    add("tube", _ring(p["tube_id"] / 2, p["tube_od"] / 2, p["tube_bot"], p["tube_top"]), "#D1D5DB", 6, "stake",
        "Stake tube")

    # ---- 7 sensor fin, two halves
    fin = fin_whole(p)
    big = 200
    add("fin_front", fin & _box(-big, big, -big, 0, -600, 0), "#94A3B8", 7, "fin", "Fin front half")
    add("fin_back", fin & _box(-big, big, 0, big, -600, 0), "#64748B", 7, "fin", "Fin back half")

    # ---- 8 capacitive probes: board 23 x 1.6 x 100, electronics on the +Y face at the top
    for i, dz in enumerate(p["depths"]):
        w0 = -dz - p["probe_l"] / 2
        b0 = w0 - 5
        brd = _box(-p["probe_w"] / 2, p["probe_w"] / 2, -p["probe_t"] / 2, p["probe_t"] / 2, b0, b0 + p["board_l"])
        brd += _box(-7, 7, -p["probe_t"] / 2 - 2.2, -p["probe_t"] / 2, b0 + p["board_l"] - 13, b0 + p["board_l"] - 1)
        add(f"probe_{'upper' if i == 0 else 'lower'}", brd, "#1F2937", 8, "fin",
            f"Moisture probe, {'upper' if i == 0 else 'lower'}")

    # ---- 9 EC rods with insulating sleeves
    rods = None
    for sx in (-1, 1):
        x = sx * p["ec_pitch"] / 2
        r = _cyl(p["ec_d"] / 2, d["ec_bot"] + 4, d["ec_rod_top"], x=x) + Pos(x, 0, d["ec_bot"] + 2) * Cone(0.3, p["ec_d"] / 2, 4)
        rods = r if rods is None else rods + r
    add("ec", rods, "#D4A017", 9, "fin", "EC electrodes (2)")
    sl = _ring(p["ec_d"] / 2, p["ec_d"] / 2 + 0.4, d["ec_top"], p["fin_bot"], x=-p["ec_pitch"] / 2) \
        + _ring(p["ec_d"] / 2, p["ec_d"] / 2 + 0.4, d["ec_top"], p["fin_bot"], x=p["ec_pitch"] / 2)
    add("ec_sleeves", sl, "#111827", 9, "fin", "Insulating sleeves")

    # ---- 10 DS18B20
    add("temp", _cyl(p["t_d"] / 2, -p["t_depth"] - p["t_l"] / 2, -p["t_depth"] + p["t_l"] / 2, x=p["t_x"]),
        "#2563EB", 10, "fin", "Temperature probe")

    # ---- 5 cell holder (printed) and cell
    st = d["spigot_top"]
    holder = _cyl(11, st + 5, st + 8) + _ring(p["cell_d"] / 2 + 0.25, 11, st + 8, d["cell_top"] + 1)
    holder -= _cyl(2.0, st + 4, st + 9, x=0, y=5)                                  # lead hole in the base
    for sy in (-1, 1):
        holder += _box(-2, 2, sy * 8 - 2, sy * 8 + 2, st, st + 5)                 # legs onto the spigot top
    add("holder", holder, "#A16207", 5, "stake", "Cell holder")
    add("cell", _cyl(p["cell_d"] / 2, p["cell_z"] - p["cell_l"] / 2, p["cell_z"] + p["cell_l"] / 2), "#C2410C", 5,
        "stake", "LiFePO4 cell")

    # ---- 2 head body
    sock_r = p["tube_od"] / 2 + 0.5
    body = _cyl(R, z0, zs)
    body -= _cyl(sock_r, z0 - 1, d["socket_top"])
    body -= _cyl(14, d["socket_top"] - 1, d["floor_top"] + 1)
    body -= _cyl(br, d["floor_top"], zs + 1)
    for sy in (-1, 1):
        body += _cyl(p["boss_r"], d["floor_top"], zs, y=sy * p["boss_y"]) & _cyl(R - 0.5, d["floor_top"], zs)
        body -= _cyl(2.3, zs - 6, zs + 1, y=sy * p["boss_y"])                     # heat-set insert hole
        body -= _cyl(1.6, zs - 12, zs - 5, y=sy * p["boss_y"])                    # screw tip clearance
    bx = p["pcb"][0] / 2
    for sx in (-1, 1):
        rib = _box(min(sx * (bx - 2), sx * (br + 1)), max(sx * (bx - 2), sx * (br + 1)), -3.5, 3.5,
                   d["floor_top"], zs - 2)
        rib -= _box(min(sx * (bx - 2.1), sx * (bx + 1)), max(sx * (bx - 2.1), sx * (bx + 1)), -0.9, 0.9,
                    p["pcb_z"] - p["pcb"][2] / 2, zs)
        body += rib & _cyl(R - 0.5, d["floor_top"], zs)
    body += _radial(7, br - 2, R + 4, p["gland_az"], p["coax_z"])                 # gland boss, flat inside and out
    body -= _radial(4.1, br - 4, R + 6, p["gland_az"], p["coax_z"])
    body += _radial(6, R - 3, R + 3, p["vent_az"], p["vent_z"])                    # vent boss
    body -= _radial(2.0, br - 3, R + 5, p["vent_az"], p["vent_z"])
    add("body", body, "#E5E7EB", 2, "head", "Head body")

    # ---- 2 head cap
    cap = _cyl(R, zs, zs + 80)
    pocket = _cyl(br, zs - 1, zs + 80) - _slope_cut(p, p["cap_roof"] / math.cos(math.radians(p["tilt"])))
    for sy in (-1, 1):
        pocket -= _cyl(4.5, zs - 2, zs + 80, y=sy * p["boss_y"])                  # solid columns round the screws
    cap -= pocket
    cap -= _slope_cut(p)
    cap -= _ring(32.0, 34.6, zs - 1, zs + 1.5)                                     # O-ring groove
    for sy in (-1, 1):
        cap -= _cyl(3.2, zs + 3, zs + 90, y=sy * p["boss_y"])                     # counterbore
        cap -= _cyl(1.7, zs - 1, zs + 4, y=sy * p["boss_y"])                      # screw hole
    pw, pl, pt = p["panel"]
    cap -= on_slope(p, 0, 0, -0.5) * Box(pw + 1, pl + 1, 1.0)                     # panel recess
    cap -= on_slope(p, 0, 0, -5) * Cylinder(2.5, 12)                              # panel lead hole
    add("cap", cap, "#F3F4F6", 2, "head", "Head cap")

    # ---- 12 seals and fixings on the head
    ocs = p["oring"][1]
    add("oring", _ring(32.3, 32.3 + ocs, zs, zs + 1.5), "#111827", 12, "head", "O-ring")
    ins = None
    scr = None
    for sy in (-1, 1):
        y = sy * p["boss_y"]
        i_ = _ring(1.5, 2.3, zs - 6, zs, y=y)
        s_ = _cyl(1.5, zs - 8, zs + 4, y=y) + _ring(1.6, 3.0, zs + 3, zs + 4, y=y) + _cyl(2.85, zs + 4, zs + 5.7, y=y)
        ins = i_ if ins is None else ins + i_
        scr = s_ if scr is None else scr + s_
    add("inserts", ins, "#B45309", 16, "head", "Heat-set inserts (2)")
    add("screws", scr, "#111827", 16, "head", "Cap screws and sealing washers (2)")
    gland = _radial(6.5, R + 4, R + 16, p["gland_az"], p["coax_z"]) \
        + _radial(6.2, br - 6, br - 2, p["gland_az"], p["coax_z"])
    add("gland", gland, "#374151", 12, "head", "Coax gland")

    # ---- 1 panel, 3 controller
    add("panel", on_slope(p, 0, 0, pt / 2 - 1.0) * Box(pw, pl, pt), "#1E3A8A", 1, "head", "Solar panel")
    bxx, byy, bzz = p["pcb"]
    ctrl = _box(-bxx / 2, bxx / 2, -byy / 2, byy / 2, p["pcb_z"] - bzz / 2, p["pcb_z"] + bzz / 2)
    ctrl += _box(-20, 0, -byy / 2 - 4.8, -byy / 2, p["pcb_z"] - 4, p["pcb_z"] + 12)
    add("ctrl", ctrl, "#16A34A", 3, "head", "Controller board")

    # ---- 4 antenna, clips and coax; 11 marker rod, flag and ties
    rx, rc = p["rod_x"], p["rod_d"] / 2
    ax = rx + rc + p["ant_d"] / 2 + 1
    add("antenna", _cyl(p["ant_d"] / 2, d["ant_bot"], d["ant_top"], x=ax), "#374151", 4, "rod", "Sleeve dipole")
    clips = None
    for zc in p["clip_z"]:
        c = _box(rx - 6, ax + p["ant_d"] / 2 + 2, -6, 6, zc - 6, zc + 6)
        c -= _cyl(rc + 0.1, zc - 7, zc + 7, x=rx) + _cyl(p["ant_d"] / 2 + 0.1, zc - 7, zc + 7, x=ax)
        clips = c if clips is None else clips + c
    add("clips", clips, "#0F766E", 4, "rod", "Antenna clips (2)")
    cx_ = rx + rc + p["coax_d"] / 2
    gx, gy = _polar(R + 22, p["gland_az"])
    run = math.hypot(cx_ - gx, -gy)
    az = math.degrees(math.atan2(-gy, cx_ - gx))
    coax = _radial(p["coax_d"] / 2, R + 16, R + 22, p["gland_az"], p["coax_z"]) + Pos(gx, gy, p["coax_z"]) * Sphere(p["coax_d"] / 2)
    coax += Pos(gx, gy, p["coax_z"]) * Rot(0, 0, az) * Rot(0, 90, 0) * Pos(0, 0, run / 2) * Cylinder(p["coax_d"] / 2, run)
    coax += Pos(cx_, 0, p["coax_z"]) * Sphere(p["coax_d"] / 2)
    coax += _cyl(p["coax_d"] / 2, p["coax_z"], d["ant_bot"], x=cx_)
    add("coax", coax, "#111827", 4, "rod", "Antenna lead (RG174)")
    add("rod", _cyl(rc, d["rod_top"] - p["rod_len"], d["rod_top"], x=rx), "#EA580C", 11, "rod", "Marker rod")
    fw, ft, fh = p["flag"]
    add("flag", _box(rx - rc - fw, rx - rc, -ft / 2, ft / 2, p["flag_z"] - fh / 2, p["flag_z"] + fh / 2), "#F97316", 11,
        "rod", "Flag")
    tc = (rx - rc + cx_ + p["coax_d"] / 2) / 2
    ties = None
    for zt in p["tie_z"]:
        t_ = _ring(5.6, 6.4, zt - 1.25, zt + 1.25, x=tc)
        ties = t_ if ties is None else ties + t_
    add("ties", ties, "#111827", 11, "rod", "Cable ties")
    return C


def slot_tool_components(p=PARAMS):
    """Slot tool (BOM 15): blade, handle through a hole in the blade, two shaft collars, printed depth
    stop clamped to the blade by a thumb screw. Shown in its driven position (stop on grade)."""
    from build123d import Box, Cylinder, Plane, Polygon, Pos, Rot, extrude
    d = derived(p)
    w, t, pt = p["slot_w"], p["slot_t"], p["slot_point"]
    z_tip = d["ec_bot"]
    blade = _box(-w / 2, w / 2, -t / 2, t / 2, z_tip + pt, p["slot_top"])
    tri = Plane.XZ * Polygon((-w / 2, z_tip + pt), (w / 2, z_tip + pt), (0, z_tip), align=None)
    blade += extrude(tri, amount=t / 2, both=True)
    hz = p["handle_z"]
    yax = lambda r, y0, y1: Pos(0, (y0 + y1) / 2, hz) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)  # noqa: E731
    blade -= yax(p["handle_d"] / 2 + 0.25, -10, 10)
    handle = yax(p["handle_d"] / 2, -p["handle_l"] / 2, p["handle_l"] / 2)
    collars = (yax(18, t / 2, t / 2 + 12) - yax(p["handle_d"] / 2, 0, 30)) + (yax(18, -t / 2 - 12, -t / 2) - yax(p["handle_d"] / 2, -30, 0))
    sz = p["stop_h"] / 2
    stop = _cyl(p["stop_d"] / 2, 0, p["stop_h"]) - _box(-w / 2 - 0.3, w / 2 + 0.3, -t / 2 - 0.3, t / 2 + 0.3, -1, p["stop_h"] + 1)
    ys = lambda r, y0, y1: Pos(0, (y0 + y1) / 2, sz) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)  # noqa: E731
    stop -= ys(2.7, t / 2, p["stop_d"] / 2 + 1)
    stop -= Pos(0, 20, sz) * Box(9, 4.5, p["stop_h"] + 2)                          # M5 nut slot, open at the top
    thumb = ys(2.5, t / 2 + 0.3, p["stop_d"] / 2 + 6) + ys(7, p["stop_d"] / 2 + 6, p["stop_d"] / 2 + 12)
    nut = Pos(0, 20, sz) * Box(8, 4, 8) - ys(2.5, 17, 23)
    return {"blade": Comp(blade, "#4B5563", 15, "tool", "Blade"),
            "handle": Comp(handle, "#111827", 15, "tool", "Handle bar"),
            "collars": Comp(collars, "#9CA3AF", 15, "tool", "Shaft collars (2)"),
            "stop": Comp(stop, "#0F766E", 15, "tool", "Depth stop"),
            "thumb": Comp(thumb + nut, "#B45309", 15, "tool", "Thumb screw and nut")}


def build_slot_tool(p=PARAMS):
    out = None
    for c in slot_tool_components(p).values():
        out = c.shape if out is None else out + c.shape
    return out


# ------------------------------------------------------------------------------ grouped by BOM line
NAMES = {"panel": "Solar panel, 0.5 W", "head": "Head body and cap, printed ASA",
         "controller": "Controller board, Wio-E5 and charger", "antenna": "Antenna on marker rod, with coax",
         "cell": "LiFePO4 cell in its holder", "tube": "Stake tube, 40 mm PVC", "fin": "Sensor fin, two printed halves",
         "probes": "Capacitive moisture probes (2)", "ec": "EC electrodes, 316 stainless",
         "temp": "DS18B20 temperature probe", "marker": "Marker rod and flag", "seals": "Seals, gland and cap screws"}
GROUPS = {"panel": ["panel"], "head": ["body", "cap"], "controller": ["ctrl"], "antenna": ["antenna", "clips", "coax"],
          "cell": ["holder", "cell"], "tube": ["tube"], "fin": ["fin_front", "fin_back"],
          "probes": ["probe_upper", "probe_lower"], "ec": ["ec", "ec_sleeves"], "temp": ["temp"],
          "marker": ["rod", "flag", "ties"], "seals": ["oring", "gland", "inserts", "screws"]}
GCOL = {"panel": "#1E3A8A", "head": "#E5E7EB", "controller": "#16A34A", "antenna": "#374151", "cell": "#C2410C",
        "tube": "#D1D5DB", "fin": "#94A3B8", "probes": "#7C3AED", "ec": "#D4A017", "temp": "#2563EB",
        "marker": "#EA580C", "seals": "#111827"}
GBOM = {"panel": 1, "head": 2, "controller": 3, "antenna": 4, "cell": 5, "tube": 6, "fin": 7, "probes": 8, "ec": 9,
        "temp": 10, "marker": 11, "seals": 12}


def build_parts(p=PARAMS):
    """Return {name: (shape, color, bom)} grouped by BOM line, for the concept media and the GA sheet."""
    C = build_components(p)
    out = {}
    for g, keys in GROUPS.items():
        s = None
        for k in keys:
            s = C[k].shape if s is None else s + C[k].shape
        out[g] = (s, GCOL[g], GBOM[g])
    return out


def assembly(p=PARAMS):
    from build123d import Compound
    kids = []
    for k, c in build_components(p).items():
        s = c.shape
        s.label = c.name
        kids.append(s)
    return Compound(children=kids)


# ------------------------------------------------------------------------------ constructability checks
# Pairs that must touch or sit in a fit (glued joints and slip fits up to 0.6 mm), with what holds them.
CONTACTS = [
    ("fin_front", "fin_back", "glued on the mid-plane with epoxy"),
    ("probe_upper", "fin_front", "board edges in the slots, potted"), ("probe_upper", "fin_back", "board edges in the slots"),
    ("probe_lower", "fin_front", "board edges in the slots, potted"), ("probe_lower", "fin_back", "board edges in the slots"),
    ("ec", "fin_front", "rods in the foot grooves, epoxy"), ("ec", "fin_back", "rods in the foot grooves, epoxy"),
    ("ec_sleeves", "ec", "heat-shrink on the rods"), ("ec_sleeves", "fin_front", "sleeve against the foot"),
    ("temp", "fin_front", "sheath in its bore, epoxy"), ("temp", "fin_back", "sheath in its bore, epoxy"),
    ("tube", "fin_front", "tube end on the collar, spigot bonded in the tube"),
    ("tube", "fin_back", "tube end on the collar, spigot bonded in the tube"),
    ("holder", "fin_front", "legs stand on the spigot top"), ("holder", "fin_back", "legs stand on the spigot top"),
    ("cell", "holder", "cell in the holder"),
    ("tube", "body", "tube bonded in the socket, epoxy"),
    ("ctrl", "body", "board edges in the guide slots"),
    ("oring", "body", "O-ring on the body rim"), ("oring", "cap", "O-ring in the cap groove"),
    ("cap", "body", "cap seated on the rim"),
    ("inserts", "body", "inserts pressed into the bosses"), ("screws", "inserts", "screws in the inserts"),
    ("screws", "cap", "screw heads on the counterbore floors"),
    ("gland", "body", "gland through the boss, locknut inside"),
    ("panel", "cap", "panel bonded in the recess"),
    ("coax", "gland", "lead through the gland"), ("coax", "rod", "lead along the rod"),
    ("coax", "antenna", "lead to the dipole feed"),
    ("clips", "rod", "clip on the rod"), ("clips", "antenna", "dipole in the clip"),
    ("flag", "rod", "flag sleeve on the rod"),
]
TOOL_CONTACTS = [("handle", "blade", "bar through the 20.5 mm hole"), ("collars", "handle", "collars on the bar"),
                 ("collars", "blade", "collars against the blade faces"), ("stop", "blade", "blade through the stop slot"),
                 ("thumb", "stop", "thumb screw in the stop")]


def _vol(a, b):
    try:
        bb1, bb2 = a.bounding_box(), b.bounding_box()
        if (bb1.max.X < bb2.min.X or bb2.max.X < bb1.min.X or bb1.max.Y < bb2.min.Y or bb2.max.Y < bb1.min.Y
                or bb1.max.Z < bb2.min.Z or bb2.max.Z < bb1.min.Z):
            return 0.0
        i = a & b
        return i.volume if i is not None else 0.0
    except Exception:
        return float("nan")


def check(p=PARAMS, verbose=True):
    """Constructability checks: no two parts overlap; every joint touches; assembly order and
    process checks. Returns (passed, failed) lists of strings."""
    d = derived(p)
    passed, failed = [], []

    def ok(cond, text):
        (passed if cond else failed).append(text)

    for label, comps, contacts in (("stake", build_components(p), CONTACTS), ("slot tool", slot_tool_components(p), TOOL_CONTACTS)):
        keys = list(comps)
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                v = _vol(comps[a].shape, comps[b].shape)
                ok(v < 0.05, f"{label}: {a} and {b} do not overlap (common volume {v:.3f} mm3)")
        for a, b, why in contacts:
            dist = comps[a].shape.distance_to(comps[b].shape)
            ok(dist <= 0.6, f"{label}: {a} touches {b} ({why}); gap {dist:.2f} mm")
    # assembly order and fit
    ok(22.0 < 28.0, "cell holder (22 mm) lifts out through the 28 mm hole in the head floor")
    chord = 2 * math.sqrt(d["bore_r"] ** 2 - (p["pcb"][1] / 2 + 4.8) ** 2)
    ok(chord > p["pcb"][0] + 1, f"board {p['pcb'][0]:.0f} mm wide drops into the {2 * d['bore_r']:.0f} mm bore "
                                 f"(chord {chord:.1f} mm at the module face)")
    ok(p["boss_y"] - 3.2 > p["panel"][1] / 2 + 0.5, "cap screw counterbores clear the panel recess")
    gx, gy = _polar(d["bore_r"] - 4, p["gland_az"])
    ok(abs(gy) - 6.2 > p["pcb"][1] / 2 + 4.8, "gland locknut clears the board and module")
    ok(d["collar_bot"] < -p["depths"][0] + p["probe_l"] / 2 + 0.01, "upper window ends at the collar, below the tube")
    ok(abs((p["cell_z"] - p["cell_l"] / 2) - d["cell_floor"]) < 0.01, "cell sits on the holder base at the modelled depth")
    # process: print bed for the fin halves
    fb = build_components(p)["fin_front"].shape.bounding_box()
    L, W = fb.size.Z, max(fb.size.X, fb.size.Y)
    ok(L + W <= 300 * math.sqrt(2) - 10, f"fin half {L:.0f} x {W:.0f} mm fits diagonally on a 300 x 300 mm print bed")
    ok(p["fin_t"] / 2 - p["chan"][1] / 2 >= 3.0, "channel walls at least 3 mm to the fin faces")
    if verbose:
        for f in failed:
            print("FAIL", f)
        print(f"constructability checks: {len(passed)} passed, {len(failed)} failed")
    return passed, failed


if __name__ == "__main__":
    if "--check" in sys.argv:
        _, f = check()
        sys.exit(1 if f else 0)
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    C = build_components()
    asm = assembly()
    T = slot_tool_components()
    exports = {"rootmesh-stake-assembly": asm, "head-body": C["body"].shape, "head-cap": C["cap"].shape,
               "sensor-fin-front": C["fin_front"].shape, "sensor-fin-back": C["fin_back"].shape,
               "cell-holder": C["holder"].shape, "antenna-clip": C["clips"].shape, "stake-tube": C["tube"].shape,
               "slot-tool": build_slot_tool(), "slot-tool-stop": T["stop"].shape}
    for name, shape in exports.items():
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
    d = derived()
    bb = asm.bounding_box()
    print(f"assembly bounding box {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print(f"head top {d['head_top']:.1f} mm above grade; antenna {d['ant_bot']:.0f} to {d['ant_top']:.0f} mm; "
          f"rod top {d['rod_top']:.0f} mm; EC tips {d['ec_bot']:.0f} mm; auger {d['auger_depth']:.0f} mm; "
          f"push {d['push_depth']:.0f} mm")
    for k, c in C.items():
        print(f"  {k:<12} volume {c.shape.volume / 1000:8.2f} cm3")
    print("exported:", ", ".join(exports))
    check()
