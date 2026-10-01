"""RootMesh prototype build plan pictures (RMS-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components and slot_tool_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/RMS-DWG-101 to 110        making sketches for the made and cut components
    docs/05-build-plan/fin-layout.png      the inside face of a fin half, with every cut sized
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, derived, build_components, slot_tool_components, _box, _cyl  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
C = build_components(P)
T = slot_tool_components(P)

COL = {"probe": "#7C3AED", "ec": "#D4A017", "sleeve": "#111827", "temp": "#2563EB", "fin_front": "#94A3B8",
       "fin_back": "#64748B", "tube": "#D1D5DB", "holder": "#A16207", "cell": "#C2410C", "body": "#E5E7EB",
       "gland": "#374151", "ctrl": "#16A34A", "oring": "#111827", "panel": "#1E3A8A", "cap": "#F3F4F6",
       "fix": "#B45309", "rod": "#EA580C", "flag": "#F97316", "clips": "#0F766E", "antenna": "#374151",
       "coax": "#111827", "blade": "#4B5563", "handle": "#111827", "collars": "#9CA3AF", "stop": "#0F766E",
       "soil": "#B7A58E"}


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


S = lambda *ks: _fuse([C[k].shape for k in ks])  # noqa: E731


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & _box(x0, x1, y0, y1, z0, z1)


def soil(z_top=0, depth=560, r=150):
    """A block of soil around the stake for the installation steps, cut open on the -Y side."""
    blk = _box(-r, r, -r, r, -depth, z_top) - _box(-r - 1, r + 1, -r - 1, 0, -depth - 1, z_top + 1)
    blk -= _cyl(25, -D["auger_depth"], z_top + 1)                     # the 50 mm auger hole
    return part("Soil (cut open)", blk, COL["soil"])


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "probes": part("Moisture probes (2), prepared", S("probe_upper", "probe_lower"), COL["probe"]),
        "ec": part("EC electrodes (2) with sleeves", S("ec", "ec_sleeves"), COL["ec"]),
        "temp": part("Temperature probe", C["temp"].shape, COL["temp"]),
        "fin_front": part("Fin front half", C["fin_front"].shape, COL["fin_front"]),
        "fin_back": part("Fin back half", C["fin_back"].shape, COL["fin_back"]),
        "tube": part("Stake tube", C["tube"].shape, COL["tube"]),
        "holder": part("Cell holder", C["holder"].shape, COL["holder"]),
        "cell": part("LiFePO4 cell", C["cell"].shape, COL["cell"]),
        "body": part("Head body", C["body"].shape, COL["body"]),
        "gland": part("Coax gland", C["gland"].shape, COL["gland"]),
        "ctrl": part("Controller board", C["ctrl"].shape, COL["ctrl"]),
        "oring": part("O-ring", C["oring"].shape, COL["oring"]),
        "panel": part("Solar panel", C["panel"].shape, COL["panel"]),
        "cap": part("Head cap", C["cap"].shape, COL["cap"]),
        "fix": part("Inserts, cap screws and washers", S("inserts", "screws"), COL["fix"]),
        "rod": part("Marker rod and flag", S("rod", "flag"), COL["rod"]),
        "clips": part("Antenna clips (2)", C["clips"].shape, COL["clips"]),
        "antenna": part("Sleeve dipole", C["antenna"].shape, COL["antenna"]),
        "coax": part("Antenna lead and cable ties", S("coax", "ties"), COL["coax"]),
    }


ORDER = ["probes", "ec", "temp", "fin_front", "fin_back", "tube", "holder", "cell", "body", "gland", "ctrl",
         "oring", "panel", "cap", "fix", "rod", "clips", "antenna", "coax"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    cut = _box(-300, 100, -100, 100, 640, 1100)
    M["rod"] = part("Marker rod and flag (rod shown shortened)", S("rod", "flag") & cut, COL["rod"])
    M["coax"] = part("Antenna lead and cable ties (shown shortened)", S("coax", "ties") & cut, COL["coax"])
    hx, hz = 380, -380
    off = {"probes": (70, 40, 0), "ec": (70, 0, -70), "temp": (115, 0, 0), "fin_front": (0, 0, 0),
           "fin_back": (-70, -40, 0), "tube": (190, 0, -190), "holder": (270, 0, -170), "cell": (320, 0, -170),
           "body": (hx, 0, hz), "gland": (hx + 140, 30, hz + 40), "ctrl": (hx, 0, hz + 120), "oring": (hx, 0, hz + 175),
           "cap": (hx, 0, hz + 205), "fix": (hx, 0, hz + 300), "panel": (hx, 0, hz + 350),
           "rod": (-200, 0, -900), "clips": (-200, 0, -860), "antenna": (-200, 0, -820), "coax": (-120, 0, -980)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "RootMesh stake prototype: every component, pulled apart",
                       subtitle="Numbered in build order: fin parts, tube and cell, head parts, then the marker rod "
                                "parts on the left. Seen from the front right and above",
                       elev=14, azim=-62, size=(11, 8), dpi=150, key=True)


def overview_tool():
    off = {"blade": (0, 0, 0), "handle": (0, 0, 120), "collars": (0, 0, 70), "stop": (0, 0, -120),
           "thumb": (0, 0, -120)}
    parts = [Part(T[k].name, T[k].shape, COL.get(k, "#B45309"), None, off[k], 1.0)
             for k in ("blade", "handle", "collars", "stop", "thumb")]
    return bv.overview(parts, OUT / "overview-tool.png", "Slot tool: every component, pulled apart",
                       subtitle="One per pilot set. Numbered in build order. Seen from the front right and above",
                       elev=18, azim=-55, size=(9, 7), dpi=150)


# ----------------------------------------------------------------- making sketches
def sheets():
    import build123d as b
    M = made()
    base = dict(project="RootMesh", date=DATE)
    out = []
    wtop = -P["depths"][0] - P["probe_l"] / 2
    fin_nb = [M["tube"], M["probes"], M["ec"], M["temp"]]

    # 101 / 102 fin halves, laid on their outside face so the top view shows the inside face
    for key, dwg, nm, extra in (("fin_front", "RMS-DWG-101", "front", [
            "Inside face (the glue face) faces up in the top view.",
            "Electronics pockets 16 wide x 3.4 deep: above each window, for the",
            "  parts on the probe boards. The back half has no pockets."]),
            ("fin_back", "RMS-DWG-102", "back", [
            "Mirror of the front half without the electronics pockets.",
            "Its slots, channels, bore and grooves must line up with the front half:",
            "  check by laying the two halves face to face before gluing."])):
        sh = C[key].shape
        rot = b.Rot(0, 0, 90) * (b.Rot(90, 0, 0) if key == "fin_front" else b.Rot(-90, 0, 0)) * sh
        out.append(bv.component_sheet(
            Part(f"Fin {nm} half", sh, COL[key]), fin_nb + [M["fin_back" if key == "fin_front" else "fin_front"]],
            dwg_no=dwg, title=f"RootMesh sensor fin, {nm} half: making sketch",
            material="PETG or ASA, 3D printed flat on its outside face, 100 % infill",
            view_shape=rot, inset_view=(20, -60),
            notes=["Blade 36 wide, 6 thick (half of 12), 310 long below the collar,",
                   "  with a wedge tip 16 wide and 30 long between the electrode grooves.",
                   "Half collar 42 dia x 4; half spigot 35.4 dia x 11 on top of it.",
                   "Windows 19 wide x 80 long, centred 150 and 300 mm below grade",
                   "  (the upper window ends at the collar).",
                   "Board slots 23.2 wide x 0.9 deep, 100 long, for the probe edges.",
                   "Wire channels 3.5 wide x 2.5 deep, centred 14.75 each side,",
                   "  from 15 mm above the foot up through the spigot.",
                   "Temperature probe bore 6.2 dia, centred 15.4 from the centre line,",
                   "  open to the edge, 200 to 250 below grade.",
                   "Electrode grooves 4.1 dia, 24 apart, 15 deep into the foot.",
                   ] + extra + ["Check: no stringing in the channels; 4 mm rod drops into its groove."],
            **base))

    # 103 EC electrode
    rod = C["ec"].shape & _box(0, 50, -10, 10, -600, 0)
    out.append(bv.component_sheet(
        Part("EC electrode", rod, COL["ec"]), [M["fin_front"], M["fin_back"]],
        dwg_no="RMS-DWG-103", title="RootMesh EC electrode (make 2): making sketch",
        material="316 stainless steel rod, 4 mm diameter", inset_view=(10, -60),
        view_shape=b.Pos(-P["ec_pitch"] / 2, 0, -D["ec_bot"]) * rod,
        notes=["Cut two 80 mm lengths of 4 mm 316 rod; square the top ends.",
               "Grind a point on the other end: about 4 mm long, tip about 0.6 mm.",
               "Abrade the top 15 mm, tin it with stainless-steel flux and solder a",
               "  0.25 mm2 wire to it (or crimp in a 4 mm splice); wash off the flux.",
               "Slide a 5 mm length of 4 mm heat-shrink to sit just below the fin foot",
               "  (15 to 20 mm from the top end) and shrink it.",
               "Fit: top 15 mm in the foot grooves, 24 mm apart, set in epoxy when the",
               "  halves are glued; 5 mm sleeved, then 60 mm bare below the foot.",
               "Check: bare length 60 mm on each rod (it sets the EC cell constant);",
               "  no flux left on the bare length."],
        **base))

    # 104 stake tube
    out.append(bv.component_sheet(
        Part("Stake tube", C["tube"].shape, COL["tube"]), [M["fin_front"], M["fin_back"], M["body"]],
        dwg_no="RMS-DWG-104", title="RootMesh stake tube: making sketch",
        material="PVC pressure pipe, 42 mm OD (40 mm or 1-1/4 in nominal)", inset_view=(15, -60),
        view_shape=b.Pos(0, 0, -P["tube_bot"]) * C["tube"].shape,
        notes=["Cut 170 mm of 42 mm OD PVC pressure pipe with a fine-tooth saw in a",
               "  mitre box, so both ends are square to within 0.5 mm.",
               "Deburr inside and out; chamfer the outside of the bottom end 1 mm.",
               "Abrade 26 mm of the outside at the top (into the head socket) and",
               "  15 mm of the inside at the bottom (over the fin spigot) with 120 grit.",
               "Fit: the bottom end sits on the fin collar, glued over the spigot;",
               "  the top end goes 24 mm into the head socket, 2 mm short of its floor.",
               "Check: the head socket slides over the tube by hand with about",
               "  0.5 mm all round for the epoxy; the spigot slides into the tube."],
        **base))

    # 105 cell holder
    out.append(bv.component_sheet(
        Part("Cell holder", C["holder"].shape, COL["holder"]),
        [part("Stake tube, back half", C["tube"].shape & _box(-50, 50, 0, 50, -200, 100), COL["tube"]),
         part("Fin back half", C["fin_back"].shape & _box(-50, 50, -50, 50, -250, 0), COL["fin_back"])],
        dwg_no="RMS-DWG-105", title="RootMesh cell holder: making sketch",
        material="ASA, 3D printed upright", inset_view=(10, -60),
        view_shape=b.Pos(0, 0, -D["spigot_top"]) * C["holder"].shape,
        notes=["Sleeve 22 OD x 15 ID, 51 long, on a 3 mm base, on two 4 x 4 legs 5 tall",
               "  16 apart. Print upright; the legs need no support.",
               "4 mm lead hole in the base, 5 mm off centre, for the cell's lower lead.",
               "Fit: drops into the tube and stands on the top of the fin spigot,",
               "  legs either side of the probe pocket, so the cell centre is 62 mm",
               "  below grade. It lifts out through the 28 mm hole in the head floor.",
               "Tie a loop of strong cord through the top of the sleeve to lift it.",
               "Check: the 14500 cell slides in by hand; the holder drops through",
               "  a 28 mm hole and a 36 mm tube without catching."],
        **base))

    # 106 head body
    out.append(bv.component_sheet(
        Part("Head body", C["body"].shape, COL["body"]), [M["tube"], M["ctrl"], M["cap"], M["gland"]],
        dwg_no="RMS-DWG-106", title="RootMesh head body: making sketch",
        material="ASA, 3D printed upright (socket down), 5 walls, 40 % infill", inset_view=(25, -60),
        view_shape=b.Pos(0, 0, -P["head_z0"]) * C["body"].shape,
        notes=["Cup 72 dia x 80 tall. Socket at the bottom 43 dia x 26 deep for the tube;",
               "  3 mm floor with a 28 mm hole; cavity 62 dia above it, 5 mm wall.",
               "Two board guides on the side walls, slot 1.8 wide, 3 deep, 44 tall,",
               "  starting 36 above the bottom: the board stands on the slot ends.",
               "Two bosses 8 dia, 29.5 each side of centre (at right angles to the",
               "  guides), with 4.6 mm holes 6 deep for M3 heat-set inserts.",
               "Gland boss 14 dia with an 8.2 mm hole, 60 up, toward the marker rod",
               "  and 30 degrees round toward the front (away from the board).",
               "Vent boss 12 dia with a 4 mm hole, 42 up, at the back right.",
               "Press the inserts in with a soldering iron at about 220 C, flush.",
               "Check: the rim is flat (no gap under a straightedge) for the O-ring;",
               "  the board slides down both guides without force."],
        **base))

    # 107 head cap
    out.append(bv.component_sheet(
        Part("Head cap", C["cap"].shape, COL["cap"]), [M["body"], M["panel"]],
        dwg_no="RMS-DWG-107", title="RootMesh head cap: making sketch",
        material="ASA, 3D printed with the sloped top on the bed", inset_view=(25, -60),
        view_shape=b.Pos(0, 0, -P["split_z"]) * C["cap"].shape,
        notes=["Cap 72 dia; top sloped 30 degrees toward the equator; 9 mm tall at the",
               "  low edge, 51 mm at the high edge; 3 mm roof, hollow underneath.",
               "Print with the sloped top on the bed (supports under the rim only).",
               "Panel recess 71 x 51 x 1 deep in the sloped top; 5 mm lead hole",
               "  through the roof at its centre.",
               "O-ring groove in the rim face: 64.0 to 69.2 dia, 1.5 deep.",
               "Two 3.4 mm screw holes over the bosses, counterbored 6.4 dia from",
               "  the top down to 3 mm above the rim face, inside solid columns.",
               "Check: the 64 x 2 O-ring sits in the groove standing 0.5 mm proud;",
               "  the cap sits on the body with both holes over the inserts."],
        **base))

    # 108 antenna clip
    clip = C["clips"].shape & _box(-100, 0, -20, 20, 900, 950)
    out.append(bv.component_sheet(
        Part("Antenna clip", clip, COL["clips"]),
        [part("Marker rod top", C["rod"].shape & _box(-100, 0, -50, 50, 860, 1100), COL["rod"]), M["antenna"],
         part("Other clip", C["clips"].shape & _box(-100, 0, -50, 50, 960, 1100), COL["clips"])],
        dwg_no="RMS-DWG-108", title="RootMesh antenna clip (make 2): making sketch",
        material="ASA, 3D printed flat", inset_view=(15, -60),
        view_shape=b.Pos(-P["rod_x"], 0, -P["clip_z"][0]) * clip,
        notes=["Block 23 long x 12 wide x 12 tall.",
               "Rod hole 8.2 dia and dipole hole 10.2 dia, 10 mm apart centre to",
               "  centre, both straight through the 12 mm height.",
               "Print flat with the holes upright; ream with a drill if tight.",
               "Fit: both clips slide over the rod top; the dipole slides through",
               "  them so its centre is level with the rod top (1,000 mm above grade).",
               "Clip centres 925 and 985 mm above grade; a cable tie above and below",
               "  each clip stops it sliding.",
               "Check: the rod and dipole each slide through by hand, without play."],
        **base))

    # 109 slot tool blade, with the handle
    bl = T["blade"].shape
    out.append(bv.component_sheet(
        Part("Blade", bl, COL["blade"]), [Part("Handle", T["handle"].shape, "#111827"), Part("Stop", T["stop"].shape, "#111827")],
        dwg_no="RMS-DWG-109", title="RootMesh slot tool blade and handle: making sketch",
        material="Mild steel flat bar 32 x 8 mm; round bar 20 mm", inset_view=(15, -55),
        view_shape=b.Pos(0, 0, -D["ec_bot"]) * bl,
        notes=["Blade: cut 650 mm of 32 x 8 mm flat bar. Grind one end to a point",
               "  40 long (the full 32 width tapering to the centre). Chamfer the",
               "  struck top end 1 mm so it does not mushroom into sharp burrs.",
               "Drill a 20.5 mm cross hole on the centre line, 25 mm below the",
               "  top end (pilot 6 mm, then step up; clamp the bar in a vice).",
               "Handle: cut 250 mm of 20 mm round bar; chamfer both ends.",
               "Fit: handle through the hole, centred; a 20 mm shaft collar each side",
               "  against the blade, set screws tight on the bar.",
               "Mark the blade 485 mm up from the point: the stop's top face goes there",
               "  when set for the stake.",
               "Check: blade straight within 2 mm; point on the centre line."],
        **base))

    # 110 depth stop
    st = T["stop"].shape
    out.append(bv.component_sheet(
        Part("Depth stop", st, COL["stop"]), [Part("Blade", T["blade"].shape, "#111827")],
        dwg_no="RMS-DWG-110", title="RootMesh slot tool depth stop: making sketch",
        material="ASA, 3D printed flat, 100 % infill", inset_view=(25, -60),
        notes=["Disc 80 dia x 15 thick with a 32.6 x 8.6 slot through the centre.",
               "M5 thumb screw hole 5.4 dia from the edge to the slot, on the",
               "  centre line, 7.5 up; a slot for an M5 nut 20 mm from centre, open",
               "  at the top, so the nut drops in and the screw threads through it.",
               "Fit: slides on the blade; the thumb screw clamps it on the blade's",
               "  wide face, with its top face at the 485 mm mark.",
               "In use it rests on the soil beside the 50 mm auger hole and stops the",
               "  point at 485 mm below grade, the depth of the electrode tips.",
               "Check: it slides on the blade without rocking, and one finger-tight",
               "  turn of the thumb screw holds it under a firm pull."],
        **base))
    return out


# ----------------------------------------------------------------- fin layout (inside face, with sizes)
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle, Polygon as MPoly
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    fig = plt.figure(figsize=(14, 5.4), dpi=150)
    ax = fig.add_axes([0.03, 0.2, 0.94, 0.66]); ax.set_aspect("equal"); ax.set_axis_off()
    # laid flat: depth below grade runs left to right (top of the fin on the left), width vertical
    hw = P["fin_w"] / 2

    def X(z):            # z below grade (positive mm) to page x
        return z

    top, bot = -P["fin_top"], -P["fin_bot"]
    ax.add_patch(MPoly([(X(top), -hw), (X(bot - 4), -hw), (X(bot), -hw + 4), (X(bot), -8), (X(bot + 30), 0),
                        (X(bot), 8), (X(bot), hw - 4), (X(bot - 4), hw), (X(top), hw)], closed=True,
                       fc="#E5E7EB", ec=INK, lw=1.1))
    ax.add_patch(Rectangle((X(top - 4), -21), 4, 42, fc="#D1D5DB", ec=INK, lw=1))
    ax.add_patch(Rectangle((X(top - 15), -17.7), 11, 35.4, fc="#D1D5DB", ec=INK, lw=1))
    ax.text(X(top - 9.5), 0, "spigot", rotation=90, ha="center", va="center", fontsize=6.5, color=MUT)
    ax.text(X(top - 2), 24, "collar", ha="center", va="bottom", fontsize=6.5, color=MUT)
    for dz in P["depths"]:
        w0, w1 = dz - 40, dz + 40
        b0, b1 = w1 + 5 - 100, w1 + 5
        ax.add_patch(Rectangle((X(b0), -11.6), 100, 23.2, fc="#EDE9FE", ec="#7C3AED", lw=0.7, ls="--"))
        ax.add_patch(Rectangle((X(w0), -9.5), 80, 19, fc="white", ec=INK, lw=1.1))
        ax.add_patch(Rectangle((X(max(b0 - 3, top - 15)), -8), w0 - max(b0 - 3, top - 15), 16, fc="#FEF3C7", ec="#B45309", lw=0.7))
        ax.text(X(dz), 0, f"window {dz:.0f}\n(80 x 19)", ha="center", va="center", fontsize=7, color=INK)
    lw1 = P["depths"][1] - 40
    ax.add_patch(Rectangle((X(lw1 - 18), -P["chan_x"]), 3, P["chan_x"], fc="#CCFBF1", ec=AC, lw=0.7))
    ec_top = -D["ec_rod_top"]
    for sx in (-1, 1):
        y = sx * P["chan_x"]
        ax.add_patch(Rectangle((X(top - 15), y - 1.75), ec_top - (top - 15), 3.5, fc="#CCFBF1", ec=AC, lw=0.7))
        ax.add_patch(Rectangle((X(ec_top), sx * 12 - 2.05), 15, 4.1, fc="#FDE68A", ec="#B45309", lw=0.7))
    ax.add_patch(Rectangle((X(P["t_depth"] - 25), P["t_x"] - 3.1), 50, 6.2, fc="#DBEAFE", ec="#2563EB", lw=0.8))
    # dimension rows below
    ys = -34
    marks = sorted({top, 110, 190, 260, 340, 200, 250, ec_top, bot, bot + 30, 95})
    for i, m in enumerate(marks):
        ax.plot([X(m), X(m)], [-hw - 1, ys + 3 - 7 * (i % 2)], color=AC, lw=0.4, ls=":")
        ax.text(X(m), ys - 7 * (i % 2), f"{m:g}", ha="center", va="top", fontsize=7, color=AC)
    ax.text(X(270), ys - 15, "depth below grade, mm (the fin is drawn lying down, top on the left)", ha="center",
            va="top", fontsize=8, color=MUT)
    for y, ty, t in ((18, 28, "18 edge"), (P["t_x"], 22, "15.4 probe bore"), (P["chan_x"], 16, "14.75 channel"),
                     (11.6, 10, "11.6 board slot"), (9.5, 4, "9.5 window")):
        ax.plot([X(top - 16), X(top - 40), X(top - 46)], [y, y, ty], color=AC, lw=0.4, ls=":")
        ax.text(X(top - 47), ty, t, ha="right", va="center", fontsize=6.5, color=AC)
    ax.text(X(top - 70), -8, "sideways from\nthe centre line", ha="center", va="top", fontsize=7, color=MUT)
    ax.set_xlim(X(top - 100), X(bot + 40)); ax.set_ylim(-52, 34)
    # key on the right side of the figure, below the drawing
    key = [("#FFFFFF", "Window, through both halves: 19 wide, 80 long"),
           ("#EDE9FE", "Board slot (dashed): 23.2 wide, 0.9 deep each half, 100 long"),
           ("#FEF3C7", "Electronics pocket, front half only: 16 wide, 3.4 deep"),
           ("#CCFBF1", "Wire channels 3.5 wide, 2.5 deep each half, centred 14.75 each side; cross channel 3 wide"),
           ("#FDE68A", "Electrode grooves 4.1 dia, centred 12 each side, 15 long"),
           ("#DBEAFE", "Temperature probe bore 6.2 dia, centred 15.4, open to the edge")]
    for i, (c, t) in enumerate(key):
        xk = 0.04 + (i % 2) * 0.47; yk = 0.15 - (i // 2) * 0.04
        fig.patches.append(Rectangle((xk, yk - 0.008), 0.014, 0.018, transform=fig.transFigure, fc=c, ec=INK, lw=0.5))
        fig.text(xk + 0.02, yk, t, fontsize=8, color=INK, va="center")
    fig.text(0.03, 0.965, "Sensor fin half: inside face layout", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.91, "The glue face of the front half, full-size figures in mm from the model. Sideways sizes "
             "from the centre line. The back half is the same without the yellow pockets.", fontsize=8.5,
             color=MUT, va="top")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/rootmesh", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "fin-layout.png", facecolor="white"); plt.close(fig)
    return OUT / "fin-layout.png"


# ----------------------------------------------------------------- joints
def joints():
    out = []
    zs = P["split_z"]
    # 01 upper probe in the front half, at the window top (fin seen from the front, inside face up)
    bx = (-24, 24, -8, 0, -200, -88)
    out.append(bv.joint([
        part("Fin front half", win(C["fin_front"].shape, *bx), COL["fin_front"]),
        part("Upper moisture probe", win(C["probe_upper"].shape, *bx), COL["probe"])],
        OUT / "joint-01.png", "Joint 1: probe board in the front fin half (upper probe)",
        subtitle="Back half removed. Board edges sit 2 mm into the slots; its electronics end lies in the pocket above the window",
        elev=55, azim=115, size=(8, 6)))
    # 02 foot: rods, sleeves, wedge (back half removed, seen on the glue face)
    bx = (-24, 24, -8, 8, -490, -380)
    out.append(bv.joint([
        part("Fin front half (back half removed)", win(C["fin_front"].shape, *bx), COL["fin_front"]),
        part("EC electrode (2)", win(C["ec"].shape, *bx), COL["ec"]),
        part("Heat-shrink sleeve (2)", win(C["ec_sleeves"].shape, *bx), "#111827")],
        OUT / "joint-02.png", "Joint 2: EC electrodes in the fin foot",
        subtitle="Back half removed. Each rod lies 15 mm in its groove, set in epoxy; 5 mm sleeved below the foot, then 60 mm bare",
        elev=20, azim=110, size=(8, 6)))
    # 03 temperature probe in the edge bore, flush (back half removed)
    bx = (0, 24, -8, 8, -265, -185)
    out.append(bv.joint([
        part("Fin front half (back half removed)", win(C["fin_front"].shape, *bx), COL["fin_front"]),
        part("Temperature probe", win(C["temp"].shape, *bx), COL["temp"])],
        OUT / "joint-03.png", "Joint 3: temperature probe in the fin edge",
        subtitle="Back half removed. The sheath lies in its bore, 0.4 mm proud of the fin edge so soil touches it; its lead runs up the channel",
        elev=20, azim=60, size=(8, 6)))
    # 04 tube on the collar and spigot, cut open
    bx = (-30, 30, -30, 0.01, -135, -80)
    out.append(bv.joint([
        part("Stake tube", win(C["tube"].shape, *bx), COL["tube"]),
        part("Fin front half (collar and spigot)", win(C["fin_front"].shape, *bx), COL["fin_front"]),
        part("Upper probe top", win(C["probe_upper"].shape, *bx), COL["probe"]),
        part("Cell holder legs", win(C["holder"].shape, *bx), COL["holder"])],
        OUT / "joint-04.png", "Joint 4: tube on the fin collar, cut open",
        subtitle="The tube end sits on the 42 mm collar and is bonded over the spigot; the holder legs stand on the spigot top",
        elev=12, azim=80, size=(8, 6)))
    # 05 tube in the head socket, cut open
    bx = (-40, 40, -40, 0.01, 30, 90)
    out.append(bv.joint([
        part("Head body", win(C["body"].shape, *bx), "#F3F4F6"),
        part("Stake tube", win(C["tube"].shape, *bx), "#0E7490")],
        OUT / "joint-05.png", "Joint 5: tube in the head socket, cut open",
        subtitle="24 mm of tube in the 26 mm socket, 0.5 mm of epoxy all round; the floor hole above lets wires and the cell holder through",
        elev=12, azim=80, size=(8, 6)))
    # 06 board in its guides, looking down into the body
    bx = (-40, 40, -40, 40, 60, 112)
    out.append(bv.joint([
        part("Head body", win(C["body"].shape, *bx), COL["body"]),
        part("Controller board", win(C["ctrl"].shape, *bx), COL["ctrl"]),
        part("Gland locknut", win(C["gland"].shape, *bx), COL["gland"])],
        OUT / "joint-06.png", "Joint 6: controller board in the guide slots, seen from above",
        subtitle="Cap off, cut 8 mm below the rim. Board edges in the two slots; the gland nut and bosses clear it",
        elev=70, azim=-80, size=(8, 6)))
    # 07 cap on the body: O-ring, insert, screw (cut on the screw plane)
    y0 = P["boss_y"]
    bx = (-14, 0.01, 12, 40, zs - 18, zs + 34)
    out.append(bv.joint([
        part("Head body and boss", win(C["body"].shape, *bx), COL["body"]),
        part("Head cap", win(C["cap"].shape, *bx), "#CBD5E1"),
        part("O-ring in the cap groove", win(C["oring"].shape, *bx), COL["oring"]),
        part("Heat-set insert", win(C["inserts"].shape, *bx), COL["fix"]),
        part("M3 screw and sealing washer", win(C["screws"].shape, *bx), "#111827")],
        OUT / "joint-07.png", "Joint 7: cap on the body, cut through a screw",
        subtitle="The O-ring seals on the body rim; the screw passes the cap's solid column into an insert in the boss",
        elev=10, azim=12, size=(8, 6)))
    # 08 gland and antenna lead at the head
    bx = (-70, -10, -50, 20, 75, 125)
    out.append(bv.joint([
        part("Head body", win(C["body"].shape, *bx), COL["body"]),
        part("Coax gland and locknut", win(C["gland"].shape, *bx), COL["gland"]),
        part("Antenna lead", win(C["coax"].shape, *bx), "#111827"),
        part("Marker rod", win(C["rod"].shape, *bx), COL["rod"])],
        OUT / "joint-08.png", "Joint 8: antenna lead into the head through its gland",
        subtitle="Gland on a flat boss, locknut on a flat inside; the lead runs to the marker rod and up it",
        elev=20, azim=-150, size=(8, 6)))
    # 09 antenna clips on the rod
    bx = (-80, -30, -20, 20, 880, 1095)
    out.append(bv.joint([
        part("Marker rod", win(C["rod"].shape, *bx), COL["rod"]),
        part("Antenna clips (2)", win(C["clips"].shape, *bx), COL["clips"]),
        part("Sleeve dipole", win(C["antenna"].shape, *bx), COL["antenna"]),
        part("Antenna lead and cable tie", win(S("coax", "ties"), *bx), "#111827")],
        OUT / "joint-09.png", "Joint 9: dipole clipped to the top of the marker rod",
        subtitle="Two clips hold the dipole beside the rod, centred on the rod top; the lead is tied to the rod",
        elev=15, azim=-60, size=(8, 6)))
    # 10 slot tool: handle through the blade, collars
    bx = (-30, 30, -60, 60, 105, 170)
    out.append(bv.joint([
        part("Blade", win(T["blade"].shape, *bx), COL["blade"]),
        part("Handle bar", win(T["handle"].shape, *bx), "#1F2937"),
        part("Shaft collars (2)", win(T["collars"].shape, *bx), COL["collars"])],
        OUT / "joint-10.png", "Joint 10: slot tool handle through the blade",
        subtitle="The bar passes a 20.5 mm hole 25 mm below the struck end; a collar each side keeps it centred",
        elev=20, azim=-35, size=(8, 6)))
    # 11 depth stop on the blade
    bx = (-50, 50, -60, 60, -20, 35)
    out.append(bv.joint([
        part("Blade", win(T["blade"].shape, *bx), COL["blade"]),
        part("Depth stop", win(T["stop"].shape, *bx), COL["stop"]),
        part("M5 thumb screw and nut", win(T["thumb"].shape, *bx), COL["fix"])],
        OUT / "joint-11.png", "Joint 11: depth stop clamped on the blade",
        subtitle="The thumb screw passes a trapped nut and presses on the blade's wide face",
        elev=30, azim=55, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    import build123d as b
    flat = lambda p: Part(p.name, b.Pos(-280, 0, 0) * b.Rot(0, 0, 90) * b.Rot(90, 0, 0) * p.shape, p.color, None, p.explode, p.alpha)  # noqa: E731
    fin_view = dict(elev=55, azim=-95)
    ff = flat(M["fin_front"])
    st(1, [ff], [mv(flat(M["probes"]), (0, 0, 50))], "probes into the front fin half",
       "Half lying on the bench, inside face up. Lay each board in its slots, electronics up into the pocket",
       label_done=True, **fin_view)
    st(2, [ff, flat(M["probes"])], [mv(flat(M["ec"]), (0, 0, 50)), mv(flat(M["temp"]), (0, 0, 50))],
       "electrodes and temperature probe into the front half",
       "Rods into the foot grooves, sleeves at the foot; sheath into the edge bore; every lead laid in its channel",
       label_done=False, **fin_view)
    inner = [ff, flat(M["probes"]), flat(M["ec"]), flat(M["temp"])]
    st(3, inner, [mv(flat(M["fin_back"]), (0, 0, 60))], "glue on the back half",
       "Epoxy on both glue faces and round every board, rod and sheath; clamp the halves; leads out of the spigot top",
       label_done=False, **fin_view)
    inner = [M["fin_front"], M["probes"], M["ec"], M["temp"]]
    fin_all = inner + [M["fin_back"]]
    st(4, fin_all, [mv(M["tube"], (0, 0, 120))], "tube onto the fin spigot",
       "Epoxy on the spigot and inside the tube end; leads through the tube first; push down until it sits on the collar",
       elev=15, azim=-60, label_done=False)
    body = M["body"]
    st(5, [body], [mv(M["gland"], (-35, -20, 0))], "gland, inserts and vent into the head body",
       "Gland through its boss, locknut inside; vent membrane on the inside over the 4 mm hole; inserts already in",
       elev=20, azim=-95, label_done=False)
    stake = fin_all + [M["tube"]]

    def short(ps, zmin=-60):
        """Only the top of the stake, so the head fills the picture."""
        out_ = []
        for p in ps:
            sh = p.shape & _box(-200, 200, -200, 200, zmin, 400)
            if sh is not None and sh.volume > 1e-3:
                out_.append(Part(p.name, sh, p.color, None, p.explode, p.alpha))
        return out_
    st(6, short(stake), [mv(Part("Head body with gland", S("body", "gland", "inserts"), COL["body"], None, (0, 0, 0), 1.0), (0, 0, 120))],
       "head body onto the tube",
       "Top of the stake shown. Leads through the floor hole first; epoxy in the socket; gland toward the marker rod side",
       elev=15, azim=-60, label_done=False)
    hb = part("Head body with gland", S("body", "gland", "inserts"), COL["body"])
    stake_h = stake + [hb]
    st(7, short(stake_h, -110), [mv(part("Cell holder with cell", S("holder", "cell"), COL["cell"]), (0, 0, 260))],
       "cell holder and cell down into the tube",
       "Hold point: safety stops S1 and S2 first. Lower the holder on its cord through the floor hole to the spigot top",
       elev=18, azim=-60, label_done=False)
    st(8, short(stake_h), [mv(M["ctrl"], (0, 0, 110))], "controller board into the guides",
       "Top of the stake shown. Plug in the cell, probe, electrode and temperature leads; slide the board down both slots",
       elev=22, azim=-60, label_done=False)
    st(9, [M["cap"]], [mv(M["panel"], (40, 0, 60))], "panel into the cap",
       "Lead through the roof hole; a bead of outdoor sealant round the recess; press the panel in and let it cure",
       elev=30, azim=-60, label_done=False)
    st(10, short(stake_h + [M["ctrl"]]), [mv(part("Cap, O-ring in its groove, screws", S("cap", "oring", "screws"), "#94A3B8"), (0, 0, 90)),
        mv(part("Panel (bonded in step 9)", C["panel"].shape, COL["panel"]), (0, 0, 90))],
       "cap onto the body",
       "Fresh desiccant inside; plug in the panel lead; O-ring clean in its groove; two M3 screws with sealing washers, snug",
       elev=20, azim=-60, label_done=False)
    # slot tool
    st(11, [Part("Blade", T["blade"].shape, COL["blade"], None, (0, 0, 0), 1.0)],
       [Part("Handle bar and collars", T["handle"].shape + T["collars"].shape, "#1F2937", None, (0, 0, 120), 1.0),
        Part("Depth stop and thumb screw", T["stop"].shape + T["thumb"].shape, COL["stop"], None, (0, 0, -140), 1.0)],
       "assemble the slot tool",
       "Handle through the cross hole, a collar each side; stop slid up from the point to the 485 mm mark, screw tight",
       elev=18, azim=-55, label_done=True)
    tool = Part("Slot tool", _fuse([T[k].shape for k in T]), COL["blade"], None, (0, 0, 0), 1.0)
    st(12, [], [Part("Slot tool", tool.shape, COL["blade"], None, (0, 0, 300), 1.0)],
       "cut the slot (trial bed)",
       "Auger a 50 mm hole 110 mm deep; blade in the hole, broad faces as the fin will lie; drive it with a mallet to the stop; pull it out",
       context=[soil()], elev=15, azim=-60, label_done=False)
    full_stake = stake_h + [M["ctrl"], part("Cap with panel", S("cap", "panel", "oring", "screws"), COL["cap"])]
    st(13, [], [Part("Stake", _fuse([p.shape for p in full_stake]), "#94A3B8", None, (0, 0, 300), 1.0)],
       "push the stake into the slot",
       "Fin lined up with the slot, panel toward the equator. Push by hand on the head shoulders, never strike the head",
       context=[soil()], elev=15, azim=-60, label_done=False)
    st(14, full_stake, [mv(M["rod"], (0, 0, 250))], "marker rod beside the stake",
       "Push the rod 200 mm into the soil, 60 mm from the stake axis on the side away from the equator, flag at the top",
       context=[soil(r=260)], elev=12, azim=-55, label_done=False)
    top = lambda p: Part(p.name, p.shape & _box(-150, 50, -60, 60, 860, 1100), p.color, None, p.explode, p.alpha)  # noqa: E731
    st(15, [top(part("Marker rod", C["rod"].shape, COL["rod"]))],
       [mv(top(M["clips"]), (0, 0, 120)), mv(top(M["antenna"]), (0, 0, 220))],
       "dipole on the top of the rod",
       "Slide both clips over the rod top, then the dipole down through them until its centre is level with the rod top",
       elev=15, azim=-60, label_done=True)
    st(16, [part("Stake head", S("body", "cap", "panel"), COL["body"]),
            Part("Marker rod", C["rod"].shape & _box(-100, 0, -50, 50, 0, 1000), COL["rod"], None, (0, 0, 0), 1.0),
            Part("Dipole", C["antenna"].shape, COL["antenna"], None, (0, 0, 0), 1.0)],
       [part("Antenna lead and cable ties", S("coax", "ties") & _box(-100, 0, -60, 60, 50, 1000), "#111827", (-40, 0, 0))],
       "antenna lead into the gland and up the rod",
       "Lead through the gland to the board's pigtail, gland nut tight; a small drip loop; tied to the rod every 200 mm",
       elev=10, azim=-60, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "RootMesh stake prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules on a 56 x 40 mm prototype board stand in for the carrier board; no circuit board "
            "is laid out. Stranded copper; every joint soldered and sleeved.", fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/rootmesh", fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((28, 20), 61, 40, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(29.5, 59.4, "On the controller board, in the head (plug-in headers for every lead)", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8, zorder=2))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK, zorder=3)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3, zorder=3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, RF = "#B91C1C", "#1D4ED8", "#6B7280", "#374151"
    blk(3, 45, 16, 11, "Solar panel", "5 V, 0.5 W,\nin the cap", "#1E3A8A")
    blk(31, 45, 17, 11, "Charger module", "1S LiFePO4, 3.6 V,\nNTC 0 to 45 °C,\n3.3 V out", "#16A34A")
    blk(3, 24, 16, 12, "LiFePO4 cell", "14500, 600 mAh,\nPTC fuse, in the tube", "#C2410C")
    blk(52, 26, 13, 10, "Load switch", "sensor supply", "#16A34A")
    blk(72, 40, 14, 16, "Wio-E5 module", "on its breakout;\nLoRaWAN, ADC,\ntimers", "#0F766E")
    blk(72, 24, 14, 10, "EC drive", "5 kHz square wave,\n330 Ω reference", "#16A34A")
    blk(97, 45, 19, 11, "Antenna", "dipole on the rod,\nlead through the gland", RF)
    blk(97, 7, 19, 31, "", "", "#7C3AED")
    ax.text(106.5, 35.5, "In the fin", ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
    ax.text(106.5, 31.5, "Upper probe (150)\nLower probe (300)\nTemperature probe\n(DS18B20)\nEC rods (2)",
            ha="center", va="top", fontsize=7.6, color=INK, linespacing=1.5)
    wire([(19, 51), (31, 51)], RED); lab(25, 53, "0.5 mm²", RED, "center")
    wire([(19, 30), (39.5, 30), (39.5, 45)], RED); lab(40.2, 37.5, "0.5 mm²,\nPTC at the cell", RED)
    wire([(15, 36), (15, 41), (34, 41), (34, 45)], GRY, 1.2); lab(20, 42.6, "cell NTC", GRY)
    wire([(48, 51), (72, 51)], RED); lab(60, 53, "3.3 V, 0.5 mm²", RED, "center")
    wire([(58.5, 51), (58.5, 36)], RED, 1.4)
    wire([(73.5, 40), (73.5, 38.2), (67.5, 38.2), (67.5, 31), (65, 31)], GRY, 1.2); lab(68.2, 34.5, "enable", GRY)
    wire([(79, 40), (79, 34)], GRY, 1.2); lab(79.6, 37, "drive", GRY)
    wire([(86, 51), (97, 51)], RF, 1.2); lab(91.5, 53, "u.FL pigtail", RF, "center")
    wire([(86, 29), (97, 29)], BLU); lab(91.5, 31, "EC rods,\n0.25 mm²", BLU, "center")
    wire([(86, 43), (93.5, 43), (93.5, 35), (97, 35)], BLU); lab(87.3, 39.6, "probe\nsignals", BLU)
    wire([(58.5, 26), (58.5, 13), (97, 13)], GRY, 1.2); lab(70, 15, "sensor supply, 0.25 mm²", GRY)
    ax.text(3, 9.6, "Safety: cell out of its holder until stops S1 and S2 in section 6 pass. Never charge below 0 °C or above 45 °C.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(3, 6.2, "Red: power. Blue: signal. Grey: sensing and control. All circuits are extra-low voltage: 3.6 V at most "
            "from the cell, about 6 V from the panel.", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "overview_tool", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "overview_tool": overview_tool, "sheets": sheets, "layouts": layouts,
           "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
