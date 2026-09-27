"""RootMesh product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the solar soil stake: a filleted ASA head with a
grip-rib band, a separate solar cap on a parting line carrying the 0.5 W panel (cell grid and
busbars) and two cap screws, a dark nameplate with a teal line, a status light behind a clear
lens, the coax gland and ePTFE vent; the controller board with its LoRaWAN module inside the
head; the PVC tube with its O-ring; the charcoal sensor fin with depth marks, capacitive probes
in their windows, the stainless DS18B20 sheath and EC electrodes; the marker rod with a fabric
flag, cable ties and the sleeve dipole. Context is a compact soil block cut away on the plane
through the stakes so the sensing depths show, two more stakes and the LoRaWAN gateway on a
short timber post.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS and derived() in model.py. Axes as
model.py: stake 1 at the origin, grade at Z = 0, Z up, X toward the equator (the panel faces +X),
marker rod on -X. The front of the render is -Y. Render layout (not a field layout): stakes 2
and 3 stand 330 mm either side of stake 1 on the same section plane, and the gateway, which the
pilot keeps indoors at the farmhouse (RMS-DDR-001 D3), is shown on a short post behind them so
one frame explains the system. See docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cone, Cylinder, Pos, RectangleRounded, RegularPolygon, Rot,
                       Sphere, extrude, fillet)
from model import PARAMS, derived

TITLE = "RootMesh: solar soil-sensor stakes with a LoRaWAN gateway"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); three stakes in a soil "
             "block cut away through the stakes to show the fins at sensing depth, marker rods with flags and "
             "antennas, and the gateway on a short post behind (render layout; the pilot gateway sits indoors)"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): solar cap and panel, head "
             "enclosure, controller board, O-ring, LiFePO4 cell, stake tube, sensor fin, moisture probes, "
             "temperature probe and EC electrodes"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 16, "az": -35,
     "note": "Detail from the front right, slightly above (about 16 deg elevation): one stake out of the soil, "
             "solar cap and head above the tube, sensor fin with both probe windows, temperature probe and "
             "EC electrodes below"},
]

# Render layout (not a field layout)
STAKE_X = (-330.0, 330.0)          # stakes 2 and 3, on the section plane Y = 0
GATEWAY_AT = (470.0, 230.0)        # post centre X, Y
POST = (60.0, 620.0, 300.0)        # post section, top above grade, depth below grade
SOIL_X = (-600.0, 620.0)
SOIL_Y = (0.0, 340.0)
SOIL_Z0 = -540.0
TOPSOIL = 70.0

# Colours (restrained product palette; kit accent)
C_HEAD = "#ECEDEF"
C_TUBE = "#C9CDD2"
C_FIN = "#8E98A3"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_PV = "#1B2A44"
C_BUS = "#B8BEC6"
C_METAL = "#B8BEC6"
C_STEEL = "#C4C9CF"
C_PCB = "#166534"
C_CHIP = "#111827"
C_CELL = "#1E40AF"
C_LENS = "#DCEBF5"
C_LED = "#22C55E"
C_PTFE = "#F7F7F5"
C_ROD = "#D9531E"
C_FLAG = "#F26B1D"
C_TOPSOIL = "#5E4636"
C_SUBSOIL = "#8A6E55"
C_POST = "#A58B6F"
C_GW = "#F2F2F0"

# Appearance-only detail sizes (mm)
FIL_TOP = 3.0          # top edge of the head
FIL_BOT = 1.5          # bottom edge of the head
CAP_T = 10.0           # solar cap thickness, normal to the slope
GROOVE = 0.6           # parting line gap between cap and head
RIB_Z = (44.0, 64.0)   # grip-rib band on the head
RIB_N = 40


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _curved_patch(r_in, r_out, a_mid, a_span, z0, z1):
    """Thin curved patch on a cylinder about Z: radii r_in..r_out, angles a_mid +/- a_span/2 (deg)."""
    h = z1 - z0
    ring = Pos(0, 0, z0 + h / 2) * (Cylinder(r_out, h) - Cylinder(r_in, h + 2))
    L = r_out * 2 + 10
    chord = 2 * r_out * math.sin(math.radians(a_span / 2))
    keep = Rot(0, 0, a_mid) * Pos(L / 2, 0, z0 + h / 2) * Box(L, chord, h + 2)
    return ring & keep


def _slope(P, D):
    """Location of the slope plane: origin on the axis at slope_z, +Z along the slope normal."""
    return Pos(0, 0, D["slope_z"]) * Rot(0, P["tilt"], 0)


def _head(P, D):
    """Head body and solar cap, split on a parting line parallel to the slope."""
    z0, R, w = P["head_z0"], P["head_r"], P["wall"]
    SL = _slope(P, D)
    hh = P["head_h"] + 40
    head = Pos(0, 0, z0 + hh / 2) * Cylinder(R, hh)
    head -= SL * Pos(0, 0, 80) * Box(400, 400, 160)
    top_face = head.faces().sort_by(Axis.Z)[-1]
    head = _fillet_try(head, [e for e in head.edges() if e in top_face.edges()], [FIL_TOP, 2.0, 1.2])
    head = _fillet_try(head, _bottom(head), [FIL_BOT, 1.0, 0.6])
    # interior exactly as model.py: cavity, cable pass-through, socket over the tube
    head -= Pos(0, 0, z0 + 56) * Cylinder(R - w, 80)
    head -= Pos(0, 0, z0 + P["socket_depth"] + 4) * Cylinder(14, 20)
    head -= Pos(0, 0, z0 + P["socket_depth"] / 2) * Cylinder(P["tube_od"] / 2 + 0.5, P["socket_depth"] + 0.01)
    # status light opening on the front (-Y)
    head -= Pos(0, -R + 1.0, 112.0) * Rot(90, 0, 0) * Cylinder(2.3, 6.0)
    # split: body below, solar cap above, with a parting-line gap
    below = SL * Pos(0, 0, -CAP_T - GROOVE / 2 - 150) * Box(400, 400, 300)
    above = SL * Pos(0, 0, -CAP_T + GROOVE / 2 + 150) * Box(400, 400, 300)
    body = head & below
    cap = head & above
    # grip ribs around the lower head, clear of the vent boss on +Y
    rh = RIB_Z[1] - RIB_Z[0]
    ribs = []
    for k in range(RIB_N):
        a = 360.0 * k / RIB_N
        if abs(((a - 90.0) + 180) % 360 - 180) < 12:
            continue
        rib = Rot(0, 0, a) * Pos(R + 0.35, 0, RIB_Z[0] + rh / 2) * Box(1.6, 1.5, rh)
        ribs.append(rib)
    body += _union(ribs)
    # coax gland boss (-X) and ePTFE vent boss (+Y), as model.py
    gland = Pos(-R - 4, 0, P["coax_z"]) * Rot(0, 90, 0) * Cylinder(6, 10)
    vent = Pos(0, R + 3, z0 + 30) * Rot(90, 0, 0) * Cylinder(5, 7)
    body += gland + vent
    return body, cap


def _panel(P, D):
    SL = _slope(P, D)
    pw, pl, pt = P["panel"]
    lam = extrude(RectangleRounded(pw, pl, 2.0), amount=pt)
    lam = _fillet_try(lam, _top(lam), [0.6, 0.3])
    lines = [Pos(x, 0, pt + 0.06) * Box(0.9, pl - 5, 0.12) for x in (-pw / 4, 0.0, pw / 4)]
    lines += [Pos(0, y, pt + 0.06) * Box(pw - 5, 0.5, 0.12) for y in (-pl / 6, pl / 6)]
    bus = _union(lines)
    screws = None
    for x in (-(pw / 2 + 3.3), pw / 2 + 3.3):
        s = Pos(x, 0, 0.5) * Cylinder(1.8, 1.0)
        s = _fillet_try(s, _top(s), [0.5, 0.3])
        s -= Pos(x, 0, 0.9) * Box(2.2, 0.5, 0.6)
        screws = s if screws is None else screws + s
    return SL * lam, SL * bus, SL * screws


def _board(P):
    bx, by, bz = P["pcb"]
    z = P["pcb_z"]
    pcb = Pos(0, 0, z) * Box(bx, by, bz)
    pcb = _fillet_try(pcb, pcb.edges().filter_by(Axis.Y), [1.5, 0.8])
    y = -by / 2
    module = Pos(-10, y - 1.2, z + 6) * Box(12.0, 2.4, 12.0)                 # Wio-E5 module, shielded
    comps = Pos(10, y - 0.6, z + 8) * Box(6.0, 1.2, 6.0)                     # charger IC
    comps += Pos(14, y - 0.5, z - 6) * Box(4.0, 1.0, 3.0)
    comps += Pos(-6, y - 0.7, z - 12) * Box(10.0, 1.4, 4.0)                  # sensor connector
    comps += Pos(22, y - 2.0, z - 14) * Box(6.0, 4.0, 5.0)                   # terminal block
    ufl = Pos(-20, y - 0.6, z + 14) * Cylinder(1.3, 1.2)
    return pcb, module, comps, ufl


def _fin(P, D):
    fl = D["fin_len"]
    fin = Pos(0, 0, P["fin_bot"] + fl / 2) * Box(P["fin_w"], P["fin_t"], fl)
    fin = _fillet_try(fin, fin.edges().filter_by(Axis.Z), [3.0, 2.0, 1.0])
    fin = _fillet_try(fin, _bottom(fin), [1.5, 0.8])
    for dz in P["depths"]:
        win = Pos(0, 0, -dz) * Box(P["fin_w"] - 8, P["fin_t"] + 2, P["probe_l"])
        fin -= win
    spig = Pos(0, 0, P["fin_top"] + P["spigot_l"] / 2 - 10) * Cylinder(P["tube_id"] / 2 - 0.3, P["spigot_l"])
    spig = _fillet_try(spig, _top(spig), [1.0, 0.5])
    fin += spig
    fin += Pos(0, 0, P["fin_bot"] - P["tip_l"] / 2) * Cone(P["fin_t"] / 2 + 6, 3, P["tip_l"])
    marks = None
    for dz in P["depths"]:
        m = Pos(0, -P["fin_t"] / 2 - 0.2, -dz - P["probe_l"] / 2 - 9) * Box(22.0, 0.4, 5.0)
        marks = m if marks is None else marks + m
    return fin, marks


def _stake(P, D):
    """One stake as a list of (key, name, shape, colour, material, bom, kind, explode)."""
    R = P["head_r"]
    out = []

    def a(key, name, shape, color, material, bom, kind, ex):
        out.append((key, name, shape, color, material, bom, kind, ex))

    E_CAP, E_HEAD = (0, 0, 240), (0, 0, 125)
    body, cap = _head(P, D)
    a("head", "Head enclosure, printed ASA", body, C_HEAD, "plastic", 2, "shell", E_HEAD)
    a("cap", "Solar cap, printed ASA", cap, C_HEAD, "plastic", 2, "shell", E_CAP)
    lam, bus, screws = _panel(P, D)
    a("panel", "Solar panel, 0.5 W", lam, C_PV, "screen", 1, "shell", E_CAP)
    a("bus", "Solar panel busbars", bus, C_BUS, "metal", 1, "shell", E_CAP)
    a("capscrews", "Cap screws", screws, C_METAL, "metal", 12, "shell", E_CAP)

    # nameplate with a teal line, on the front of the head
    plate = _curved_patch(R - 0.2, R + 0.35, -90.0, 56.0, 80.0, 98.0)
    a("label", "Nameplate", plate, C_DARK, "plastic", 2, "shell", E_HEAD)
    stripe = _curved_patch(R + 0.2, R + 0.55, -90.0, 44.0, 85.0, 87.0)
    a("stripe", "Nameplate accent line", stripe, C_ACCENT, "plastic", 2, "shell", E_HEAD)
    # status light: clear lens in the front opening, lit green LED behind it
    lens = Pos(0, -R + 1.2, 112.0) * Rot(90, 0, 0) * Cylinder(2.3, 3.6)
    lens += Pos(0, -R - 0.6, 112.0) * Sphere(2.3)
    lens &= Pos(0, -R + 1.0, 112.0) * Box(8, 7.4, 8)
    a("lens", "Status light lens, clear", lens, C_LENS, "clear", 3, "shell", E_HEAD)
    led = Pos(0, -R + 3.4, 112.0) * Rot(90, 0, 0) * Cylinder(1.8, 0.8)
    a("led", "Status light (lit)", led, C_LED, "emissive", 3, "shell", E_HEAD)
    # coax gland nut and dome on the -X boss; ePTFE vent membrane on the +Y boss
    gx = -R - 9.0
    nut = Pos(gx - 2.0, 0, P["coax_z"]) * Rot(0, 90, 0) * extrude(RegularPolygon(7.5, 6), amount=4.0, both=True)
    nut = _fillet_try(nut, nut.edges().filter_by(Axis.X), [0.6, 0.3])
    dome = Pos(gx - 6.5, 0, P["coax_z"]) * Rot(0, 90, 0) * Cylinder(5.5, 5.0)
    dome = _fillet_try(dome, dome.faces().sort_by(Axis.X)[0].edges(), [2.0, 1.2])
    a("gland", "Coax gland, IP68", nut + dome, C_BLACK, "plastic", 12, "shell", E_HEAD)
    vent = Pos(0, R + 6.8, P["head_z0"] + 30) * Rot(90, 0, 0) * Cylinder(3.8, 0.4)
    a("vent", "Vent membrane, ePTFE", vent, C_PTFE, "fabric", 12, "shell", E_HEAD)

    # controller board inside the head
    pcb, module, comps, ufl = _board(P)
    E_BRD = (0, -150, 60)
    a("pcb", "Controller board", pcb, C_PCB, "plastic", 3, "internal", E_BRD)
    a("module", "LoRaWAN module (Wio-E5)", module, C_STEEL, "metal", 3, "internal", E_BRD)
    a("comps", "Controller components", comps + ufl, C_CHIP, "plastic", 3, "internal", E_BRD)

    # O-ring at the head joint, as model.py
    od = P["tube_od"]
    oring = Pos(0, 0, P["head_z0"] + P["socket_depth"] + 1) * (Cylinder(od / 2 + 2.5, 3) - Cylinder(od / 2 - 0.2, 4))
    a("oring", "O-ring, head joint", oring, C_BLACK, "rubber", 12, "internal", (0, 0, 70))

    # LiFePO4 cell with holder, in the tube below grade
    cl, cr, cz = P["cell_l"], P["cell_d"] / 2, P["cell_z"]
    E_CELL = (0, -150, 20)
    wrap = Pos(0, 0, cz) * Cylinder(cr, cl - 1.6)
    wrap = _fillet_try(wrap, wrap.edges(), [0.5, 0.3])
    a("cell", "LiFePO4 cell, 600 mAh", wrap, C_CELL, "painted", 5, "internal", E_CELL)
    ends = Pos(0, 0, cz + cl / 2 - 0.4) * Cylinder(cr - 0.8, 0.8) + Pos(0, 0, cz - cl / 2 + 0.4) * Cylinder(cr - 0.8, 0.8)
    ends += Pos(0, 0, cz + cl / 2 + 0.6) * Cylinder(2.2, 1.2)
    a("cellends", "LiFePO4 cell terminals", ends, C_METAL, "metal", 5, "internal", E_CELL)
    holder = Pos(0, 0, cz) * (Cylinder(11, cl) - Cylinder(cr + 0.25, cl + 2))
    holder -= Pos(0, -11, cz) * Box(9.0, 8.0, cl - 12)
    a("holder", "Cell holder", holder, C_DARK, "plastic", 5, "internal", E_CELL)

    # stake tube, PVC, eased ends
    tube = Pos(0, 0, (P["tube_bot"] + P["tube_top"]) / 2) * (
        Cylinder(P["tube_od"] / 2, P["tube_top"] - P["tube_bot"]) - Cylinder(P["tube_id"] / 2, P["tube_top"] - P["tube_bot"] + 2))
    tube = _fillet_try(tube, tube.edges(), [0.8, 0.4])
    a("tube", "Stake tube, 40 mm PVC", tube, C_TUBE, "plastic", 6, "shell", (0, 0, 0))

    # sensor fin, depth marks, probes, temperature probe, EC electrodes
    fin, marks = _fin(P, D)
    E_FIN = (0, 0, -110)
    a("fin", "Sensor fin, printed", fin, C_FIN, "plastic", 7, "shell", E_FIN)
    a("marks", "Fin depth marks", marks, C_ACCENT, "plastic", 7, "shell", E_FIN)
    probes, coats = [], []
    for dz in P["depths"]:
        b = Pos(0, 0, -dz) * Box(P["probe_w"], P["probe_t"], P["probe_l"] + 10)
        probes.append(_fillet_try(b, b.edges().filter_by(Axis.Y), [0.8, 0.4]))
        coats.append(Pos(0, 0, -dz + (P["probe_l"] + 10) / 2 - 6) * Box(P["probe_w"] + 0.4, P["probe_t"] + 0.6, 8.0))
    E_PRB = (0, -130, -110)
    a("probes", "Capacitive moisture probes (2)", _union(probes), C_BLACK, "plastic", 8, "shell", E_PRB)
    a("probecoat", "Probe epoxy edge seal", _union(coats), "#8B6A2B", "painted", 8, "shell", E_PRB)
    tx = P["fin_w"] / 2 + P["t_d"] / 2
    sheath = Pos(tx, 0, -P["t_depth"]) * Cylinder(P["t_d"] / 2, P["t_l"])
    sheath = _fillet_try(sheath, _bottom(sheath), [2.0, 1.2])
    a("temp", "DS18B20 temperature probe, stainless", sheath, C_STEEL, "metal", 10, "shell", (110, 0, -110))
    L = P["ec_exposed"]
    rods = []
    for dx in (-P["ec_pitch"] / 2, P["ec_pitch"] / 2):
        r = Pos(dx, 0, D["ec_top"] - L / 2 + 2) * Cylinder(P["ec_d"] / 2, L - 4) \
            + Pos(dx, 0, D["ec_bot"] + 2) * Cone(P["ec_d"] / 2, 0.3, 4)
        r += Pos(dx, 0, P["fin_bot"] + 10) * Cylinder(P["ec_d"] / 2, 20)
        rods.append(r)
    a("ec", "EC electrodes, 316 stainless", _union(rods), C_STEEL, "metal", 9, "shell", (0, 0, -200))

    # marker rod, fabric flag, cable ties, sleeve dipole and coax (context: they frame the stake)
    rx, rc = P["rod_x"], P["rod_d"] / 2
    rod = Pos(rx, 0, D["rod_top"] - P["rod_len"] / 2) * Cylinder(rc, P["rod_len"])
    rod = _fillet_try(rod, _top(rod), [2.0, 1.0])
    a("rod", "Marker rod, fibreglass", rod, C_ROD, "painted", 11, "rod", (0, 0, 0))
    fw, ft, fh = P["flag"]
    flag = Pos(rx - rc - fw / 2, 0, P["flag_z"]) * Box(fw, ft, fh)
    flag = _fillet_try(flag, flag.edges().filter_by(Axis.Y), [3.0, 1.5])
    a("flag", "Marker flag, high-visibility fabric", flag, C_FLAG, "fabric", 11, "rod", (0, 0, 0))
    ax = rx + rc + P["ant_d"] / 2 + 1
    ant = Pos(ax, 0, P["ant_center_z"]) * Cylinder(P["ant_d"] / 2, P["ant_len"])
    ant = _fillet_try(ant, ant.edges(), [3.0, 2.0, 1.0])
    clip = Pos(ax - 3, 0, D["rod_top"] - 30) * Box(12, 12, 16)
    clip = _fillet_try(clip, clip.edges(), [1.5, 0.8])
    a("antenna", "Sleeve dipole antenna and rod clip", ant + clip, C_DARK, "plastic", 4, "rod", (0, 0, 0))
    run_up = D["ant_bot"] - P["coax_z"]
    coax = Pos(ax, 0, P["coax_z"] + run_up / 2) * Cylinder(P["coax_d"] / 2, run_up)
    span = (gx - 9.0) - ax
    coax += Pos(ax + span / 2, 0, P["coax_z"]) * Rot(0, 90, 0) * Cylinder(P["coax_d"] / 2, abs(span))
    coax += Pos(ax, 0, P["coax_z"]) * Sphere(P["coax_d"] / 2)
    ties = [Pos((rx + ax) / 2, 0, z) * Box(ax - rx + 6, 10.5, 3.0) for z in (250.0, 450.0, 650.0, 850.0)]
    ties = [t - Pos(rx, 0, t.center().Z) * Cylinder(rc, 5) - Pos(ax, 0, t.center().Z) * Cylinder(P["coax_d"] / 2, 5)
            for t in ties]
    a("coax", "Coax lead, RG174", coax, C_BLACK, "rubber", 4, "rod", (0, 0, 0))
    a("ties", "Cable ties", _union(ties), C_BLACK, "plastic", 12, "rod", (0, 0, 0))
    return out


def _soil(P, D, stake_xs):
    x0, x1 = SOIL_X
    y0, y1 = SOIL_Y
    blk = Pos((x0 + x1) / 2, (y0 + y1) / 2, SOIL_Z0 / 2) * Box(x1 - x0, y1 - y0, -SOIL_Z0)
    holes = []
    for x in stake_xs:
        hb = D["ec_bot"] - 12.0
        holes.append(Pos(x, 0, hb / 2 + 1) * Cylinder(26.0, -hb + 4))
        holes.append(Pos(x + P["rod_x"], 0, -P["rod_bury"] / 2 + 1) * Cylinder(P["rod_d"] / 2 + 1.0, P["rod_bury"] + 4))
    gx, gy = GATEWAY_AT
    s = POST[0] + 2
    holes.append(Pos(gx, gy, -POST[2] / 2 + 1) * Box(s, s, POST[2] + 4))
    blk -= _union(holes)
    top = blk & Pos(0, 0, -TOPSOIL / 2) * Box(5000, 5000, TOPSOIL)
    sub = blk & Pos(0, 0, SOIL_Z0 / 2 - TOPSOIL / 2 - 1) * Box(5000, 5000, -SOIL_Z0 - TOPSOIL + 2 - 0.02)
    top = _fillet_try(top, [e for e in top.edges().filter_by(Axis.Z) if abs(e.center().Y - y1) < 1
                            or abs(e.center().Y - y0) < 1], [3.0, 1.5])
    return top, sub


def _gateway():
    gx, gy = GATEWAY_AT
    s, h, dep = POST
    post = Pos(gx, gy, (h - dep) / 2) * Box(s, s, h + dep)
    post = _fillet_try(post, post.edges().filter_by(Axis.Z), [3.0, 1.5])
    post = _fillet_try(post, _top(post), [4.0, 2.0])
    fy = gy - s / 2                      # front face of the post
    zc = h - 110.0
    bracket = Pos(gx, fy - 1.5, zc) * Box(50.0, 3.0, 110.0)
    bracket = _fillet_try(bracket, bracket.edges().filter_by(Axis.Y), [4.0, 2.0])
    bolts = None
    for z in (zc - 44, zc + 44):
        b = Pos(gx, fy - 3.0 - 1.2, z) * Rot(90, 0, 0) * extrude(RegularPolygon(4.0, 6), amount=1.2, both=True)
        bolts = b if bolts is None else bolts + b
    uy = fy - 3.0 - 17.0
    unit = Pos(gx, uy, zc) * Rot(90, 0, 0) * extrude(RectangleRounded(92.0, 92.0, 14.0), amount=17.0, both=True)
    unit = _fillet_try(unit, unit.faces().sort_by(Axis.Y)[0].edges(), [5.0, 3.0, 1.5])
    unit = _fillet_try(unit, unit.faces().sort_by(Axis.Y)[-1].edges(), [1.5, 0.8])
    band = Pos(gx, uy, zc) * Rot(90, 0, 0) * (extrude(RectangleRounded(93.2, 93.2, 14.6), amount=2.0, both=True)
                                              - extrude(RectangleRounded(90.0, 90.0, 13.0), amount=3.0, both=True))
    band = Pos(0, 4.0, 0) * band
    led = Pos(gx, uy - 17.0 - 0.1, zc + 26.0) * Rot(90, 0, 0) * Cylinder(2.2, 0.8)
    cz0 = zc - 46.0
    cable = Pos(gx + 30.0, uy + 6.0, cz0 - 12.0) * Cylinder(2.0, 24.0)
    cable += Pos(gx + 30.0, uy + 6.0, cz0 - 24.0) * Sphere(2.0)
    run = Pos((gx + 30.0 + gx + 20.0) / 2, uy + 6.0, cz0 - 24.0) * Rot(0, 90, 0) * Cylinder(2.0, 10.0)
    dn = Pos(gx + 20.0, fy - 2.0, (cz0 - 24.0) / 2) * Cylinder(2.0, cz0 - 24.0)
    jog = Pos(gx + 20.0, (uy + 6.0 + fy - 2.0) / 2, cz0 - 24.0) * Rot(90, 0, 0) * Cylinder(2.0, abs(uy + 6.0 - fy + 2.0))
    cable += run + dn + jog + Pos(gx + 20.0, uy + 6.0, cz0 - 24.0) * Sphere(2.0) + Pos(gx + 20.0, fy - 2.0, cz0 - 24.0) * Sphere(2.0)
    boot = Pos(gx + 30.0, uy + 6.0, cz0 - 2.0) * Cylinder(3.2, 6.0)
    return post, bracket, bolts, unit, band, led, cable + boot


def product_parts(P=PARAMS):
    D = derived(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    stake = _stake(P, D)
    # stake 1: the product (shell and internal); its rod, antenna and coax frame the scene
    for key, name, shape, color, mat, bom, kind, ex in stake:
        group = "context" if kind == "rod" else kind
        add(name, shape, color, mat, bom, group, ex)
    # stakes 2 and 3: outside parts only, same geometry, moved along the section plane
    for i, x in enumerate(STAKE_X):
        for key, name, shape, color, mat, bom, kind, ex in stake:
            if kind == "internal":
                continue
            add(f"Stake {i + 2}: {name}", Pos(x, 0, 0) * shape, color, mat, bom, "context", (0, 0, 0))

    # soil block cut away on the plane through the stakes (Y = 0)
    top, sub = _soil(P, D, (0.0,) + STAKE_X)
    add("Topsoil, cut away", top, C_TOPSOIL, "rubber", None, "context", (0, 0, 0))
    add("Subsoil, cut away", sub, C_SUBSOIL, "rubber", None, "context", (0, 0, 0))

    # LoRaWAN gateway (BOM 13) on a short timber post (render layout; the pilot keeps it indoors)
    post, bracket, bolts, unit, band, led, cable = _gateway()
    add("Gateway post, timber", post, C_POST, "wood", None, "context", (0, 0, 0))
    add("Gateway bracket", bracket, C_METAL, "metal", 13, "context", (0, 0, 0))
    add("Gateway bracket bolts", bolts, C_METAL, "metal", 13, "context", (0, 0, 0))
    add("LoRaWAN gateway", unit, C_GW, "plastic", 13, "context", (0, 0, 0))
    add("LoRaWAN gateway accent band", band, C_ACCENT, "plastic", 13, "context", (0, 0, 0))
    add("LoRaWAN gateway status light (lit)", led, C_LED, "emissive", 13, "context", (0, 0, 0))
    add("LoRaWAN gateway USB lead", cable, C_BLACK, "rubber", 13, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:52s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:8.2f} cm3")
