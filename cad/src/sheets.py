"""RootMesh general arrangement sheet RMS-DWG-001, Rev P2 (TRL 3).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/RMS-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(),
so they follow any parameter change. The concept sheet in media/ is RMS-DWG-010.
Orthographic views show the stake (head, tube, fin and sensors) at 1:5; an installed
elevation at 1:20 adds the marker rod, flag and antenna.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, build_parts, derived  # noqa: E402

DATE = "2026-09-25"
ACC = "#0F766E"


def safe_project_views(part, workdir, line_weight=0.35, names=("front", "top", "right", "iso")):
    """drawing.project_views, edge by edge, so a degenerate projected edge is skipped, not fatal."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out = {}
    for name in names:
        origin, up = setups[name]
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    pass
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    return out


def ortho_cells(k, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, k * max(fh, rh)),
            "right": (ax + colw + gap, front_y, k * rw, k * max(fh, rh))}


def dim_h(x1, x2, y, text, below=False):
    a = 1.2
    ty = y + 3.0 if below else y - 1.0
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.45 l0 0.9 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.45 l0 0.9 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, ty, text, 2.2, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.2
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.45 {a} l0.9 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.45 {-a} l0.9 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.2, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2, color=MUTED, w=0.13, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{w}"{da}/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [ext(x1, y1, x2, y2, INK, 0.15), f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    from build123d import Compound
    D = derived(P)
    parts = build_parts()
    stake_keys = [k for k in parts if k not in ("marker", "antenna")]
    stake = Compound(children=[parts[k][0] for k in stake_keys])
    full = Compound(children=[s for s, _, _ in build_parts().values()])   # fresh shapes: children are re-parented
    work = ROOT / "cad" / "drawings" / "_views"
    views = safe_project_views(stake, work / "stake")
    elev = safe_project_views(full, work / "full", names=("front", "iso"))
    bb = stake.bounding_box()

    s = Sheet(project="RootMesh", title="General arrangement, sensor stake", dwg_no="RMS-DWG-001", rev="P2",
              author="Amish Chadha", date=DATE, scale=0.2, theme="technical",
              material="ASA head, PVC tube, PETG or ASA fin, 316 stainless electrodes; bought-in parts per bom/bom.csv. "
                       "PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Slot tool note added (RMS-DDR-002)", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(k, views)
    L = []

    # ---- front view (from -Y): X right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    xl, xr = X(bb.min.X), X(bb.max.X)
    L.append(ext(xl - 22, Z(0), xr + 24, Z(0), ACC, 0.3, "2 1"))
    L.append(_t(xr + 24, Z(0) - 1, "GRADE", 2.0, 600, ACC, "end"))
    # vertical dimensions on the left, from grade
    for i, (zz, txt) in enumerate([(D["head_top"], f"{D['head_top']:.0f} head top"),
                                   (-P["depths"][0], f"{P['depths'][0]:.0f} probe 1"),
                                   (-P["depths"][1], f"{P['depths'][1]:.0f} probe 2"),
                                   (D["ec_bot"], f"{-D['ec_bot']:.0f} EC tips")]):
        xd = xl - 6 - 5 * i
        L.append(ext(X(0) - 2, Z(zz), xd - 1, Z(zz)))
        L += dim_v(xd, Z(zz), Z(0), txt)
    # right side: temperature probe depth and fin bottom
    L.append(ext(X(P["fin_w"] / 2 + P["t_d"]), Z(-P["t_depth"]), xr + 8, Z(-P["t_depth"])))
    L += dim_v(xr + 7, Z(0), Z(-P["t_depth"]), f"{P['t_depth']:.0f} temp", side=1)
    L.append(ext(X(P["fin_w"] / 2), Z(P["fin_bot"]), xr + 14, Z(P["fin_bot"])))
    L += dim_v(xr + 13, Z(0), Z(P["fin_bot"]), f"{-P['fin_bot']:.0f} fin foot", side=1)
    # horizontal: EC pitch and fin width
    # leaders on the right view (from +X: Y to the right, Z up)
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    xo = x + w + 4
    L += leader(Yr(P["tube_od"] / 2), Zr(-60), xo, Zr(-60), f"tube {P['tube_od']:.0f} OD, cell inside")
    L += leader(Yr(P["fin_t"] / 2), Zr(-380), xo, Zr(-380), f"fin {P['fin_w']:.0f} x {P['fin_t']:.0f}")
    L += leader(Yr(0), Zr(D["ec_bot"] + 20), xo, Zr(D["ec_bot"] + 20), f"EC rods {P['ec_d']:.0f} dia, {P['ec_pitch']:.0f} pitch")
    L += leader(Yr(0), Zr(P["pcb_z"]), xo, Zr(P["pcb_z"]), "controller board")

    # ---- top view: slope direction and panel
    x, y, w, h = c["top"]
    L.append(_t(x + w / 2, y - 2, f"panel {P['panel'][0]:.0f} x {P['panel'][1]:.0f} at {P['tilt']:.0f} deg, faces +X (equator)",
                2.0, 400, MUTED, "middle"))

    # ---- installed elevation at 1:20 on the left of the sheet
    ke = 0.05
    fb = full.bounding_box()
    vx, vy, vw, vh = _viewbox(Path(elev["front"]).read_text())
    ex0, ey0 = M + 26, M + 44
    s.add_svg(elev["front"], ex0, ey0, vw * ke, vh * ke, scale=ke, label="Installed elevation",
              sublabel="Scale 1:20; front, with marker rod and antenna")
    Xe = lambda mx: ex0 + (mx - fb.min.X) * ke
    Ze = lambda mz: ey0 + vh * ke - (mz - fb.min.Z) * ke
    L.append(ext(Xe(fb.min.X) - 8, Ze(0), Xe(fb.max.X) + 8, Ze(0), ACC, 0.3, "2 1"))
    L += dim_v(Xe(fb.min.X) - 4, Ze(P["ant_center_z"]), Ze(0), f"{P['ant_center_z']:.0f} antenna")
    L.append(ext(Xe(P["rod_x"]), Ze(P["ant_center_z"]), Xe(fb.min.X) - 5, Ze(P["ant_center_z"])))
    L += dim_v(Xe(fb.max.X) + 5, Ze(D["head_top"]), Ze(0), "", side=1)
    L.append(_t(Xe(fb.max.X) + 7, Ze(D["head_top"]) + 1, f"{D['head_top']:.0f}", 2.0, 400, INK, "start", mono=True))
    L += leader(Xe(P["rod_x"]), Ze(500), Xe(fb.max.X) + 3, Ze(500), "marker rod 8, 1.2 m")
    L += leader(Xe(P["rod_x"] - 60), Ze(P["flag_z"]), Xe(fb.max.X) + 3, Ze(P["flag_z"]), "flag")
    L += leader(Xe(P["rod_x"]), Ze(-150), Xe(fb.max.X) + 3, Ze(-200), f"rod {P['rod_bury']:.0f} in soil")

    s._layers += L
    s.add_svg(elev["iso"], 276, 32, 140, 100, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Tube {P['tube_od']:.0f} OD x {P['tube_id']:.0f} ID PVC, Z {P['tube_bot']:.0f} to {P['tube_top']:.0f}; head socket {P['socket_depth']:.0f} deep",
        f"Head {2 * P['head_r']:.0f} dia ASA, top {D['head_top']:.0f} above grade; panel {P['panel'][0]:.0f} x {P['panel'][1]:.0f} at {P['tilt']:.0f} deg",
        f"Fin {P['fin_w']:.0f} x {P['fin_t']:.0f} x {D['fin_len']:.0f}, spigot {P['tube_id'] - 0.6:.1f} dia into the tube",
        f"Probe windows centered {P['depths'][0]:.0f} and {P['depths'][1]:.0f} deep, {P['probe_l']:.0f} long",
        f"DS18B20 at {P['t_depth']:.0f}; EC rods {P['ec_d']:.0f} dia at {P['ec_pitch']:.0f} pitch, {P['ec_exposed']:.0f} exposed",
        f"Cell 14500 LiFePO4 centered {-P['cell_z']:.0f} below grade",
        f"Antenna sleeve dipole centered {P['ant_center_z']:.0f} on the marker rod (RMS-DDR-001 D2)",
        f"Fin pushed {D['push_depth']:.0f} into undisturbed soil below a 50 dia auger hole",
        f"Slot tool (BOM 15, separate): {P['slot_w']:.0f} x {P['slot_t']:.0f} steel blade, point {-D['ec_bot']:.0f} deep, {P['stop_d']:.0f} dia stop collar",
        "Third-angle; front view from -Y; X toward the equator",
    ], x=276, y=153, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "RMS-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png; orthographic scale 1:{1 / k:g}, elevation 1:20")


if __name__ == "__main__":
    main()
