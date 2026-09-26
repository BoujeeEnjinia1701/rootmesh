"""RootMesh sizing calculations (RMS-CAL-001 v0.2), TRL 3.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number that RMS-CAL-001 (docs/04-calcs/01-sizing.md) quotes, tagged [A1], [B3] and
so on, and the results table against RMS-REQ-001 v0.4. Geometry comes from cad/src/model.py
(PARAMS and derived), cost from bom/bom.csv and the budget from project.yaml.
All values are first-principles estimates for a paper proof of concept.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived  # noqa: E402

D = derived(P)
RESULTS = []


def out(tag, text):
    print(f"[{tag}] {text}")


def req(rid, value, target, status):
    RESULTS.append((rid, value, target, status))


# ---------------------------------------------------------------- A. Airtime (R4)
PAYLOAD_APP = 11          # bytes: 2 moisture counts, EC, temperature, cell voltage, status
OVERHEAD = 13             # MHDR 1 + FHDR 7 + FPort 1 + MIC 4
PHY = PAYLOAD_APP + OVERHEAD
BW, CR, NPRE = 125e3, 1, 8
FUP = 30.0                # s per node per day, The Things Network fair use
INTERVAL = 20.0           # min, default (RMS-DDR-001 D9)


def toa(sf, n=PHY, bw=BW):
    """Semtech SX127x/SX126x time on air, explicit header, CRC on."""
    ts = 2 ** sf / bw
    de = 1 if (sf >= 11 and bw == 125e3) else 0
    npay = 8 + max(math.ceil((8 * n - 4 * sf + 28 + 16) / (4 * (sf - 2 * de))) * (CR + 4), 0)
    return (NPRE + 4.25) * ts + npay * ts


print("A. Airtime")
out("A1", f"PHY payload {PHY} bytes ({PAYLOAD_APP} application + {OVERHEAD} LoRaWAN overhead); "
          f"US915 DR0 (SF10) allows 11 application bytes, so the payload fits at SF10 in both plans")
per_day = 24 * 60 / INTERVAL
for sf in (7, 8, 9, 10, 11, 12):
    t = toa(sf)
    min_int = t * 24 * 60 / FUP
    out(f"A2-SF{sf}", f"SF{sf}: time on air {t * 1000:.0f} ms; {per_day:.0f} uplinks at {INTERVAL:.0f} min = {t * per_day:.1f} s/day; "
                      f"at 15 min {t * 96:.1f} s/day; shortest interval within {FUP:.0f} s/day = {min_int:.1f} min")
t10 = toa(10)
out("A3", f"EU868 1 % duty cycle: after a {t10:.3f} s SF10 uplink the sub-band is closed for {t10 * 99:.0f} s, "
          f"far below the {INTERVAL * 60:.0f} s interval")
air10 = t10 * per_day
req("R4", f"{air10:.1f} s/day at SF10, 20 min; 15 min needs SF9 or faster ({toa(9) * 96:.1f} s/day)",
    "20 min default; 30 s/day or less at SF10; 10 to 60 min where the SF allows", "Met")

# ---------------------------------------------------------------- B. Energy (R6, R7)
print("\nB. Energy")
# Currents from the Wio-E5 module page (Seeed Studio wiki): TX 111 mA at +22 dBm, RX 6.7 mA, sleep 2.1 uA.
I_TX, T_TX = 120.0, t10          # mA, s: 111 mA datasheet at +22 dBm, plus carrier board, rounded up
I_RX, T_RX = 6.7, 0.2            # two receive windows, about 0.1 s each at SF10 preamble detection
I_SENS, T_SENS = 12.0, 1.0       # two TLC555 probes, DS18B20, dividers
I_MCU, T_MCU = 4.0, 1.5          # STM32WL core active
I_EC, T_EC = 10.0, 0.02          # EC burst, 5 kHz square wave through about 330 ohm
I_SLEEP = 10e-3                  # mA, whole board incl. charger and dividers (module 2.1 uA)
MARGIN = 1.30
CELL_MAH, CELL_V, DOD = 600.0, 3.2, 0.80
SELF_DIS = 0.03                  # per month, LiFePO4 with protection
charge = {"sensors": I_SENS * T_SENS, "mcu": I_MCU * T_MCU, "tx": I_TX * T_TX, "rx": I_RX * T_RX, "ec": I_EC * T_EC}
q_rep = sum(charge.values())
out("B1", "charge per report " + " + ".join(f"{k} {v:.1f}" for k, v in charge.items()) + f" = {q_rep:.1f} mAs")
active = q_rep * per_day / 3600
sleep = I_SLEEP * 24
use = (active + sleep) * MARGIN
selfd = CELL_MAH * SELF_DIS / 30
need = use + selfd
out("B2", f"active {active:.2f} mAh/day + sleep {sleep:.2f} mAh/day = {active + sleep:.2f}; x {MARGIN} margin = {use:.2f} mAh/day "
          f"({use * CELL_V:.1f} mWh/day)")
out("B3", f"self-discharge {selfd:.2f} mAh/day; total daily need {need:.2f} mAh/day")
dark_days = CELL_MAH * DOD / need
out("B4", f"days on the cell alone ({CELL_MAH:.0f} mAh x {DOD:.0%} usable): {dark_days:.0f} days "
          f"({CELL_MAH * DOD / use:.0f} days ignoring self-discharge)")
I_PANEL = 0.5 / 5.0 * 1000       # mA at maximum power point, 1000 W/m2
DERATE = 0.5                     # tilt, dust, heat, linear charger headroom
for psh, shade, label in ((3, 1.0, "3 sun hours, open sky"), (1, 1.0, "1 sun hour, open sky"),
                          (3, 0.1, "3 sun hours, canopy passing 10 %")):
    h = I_PANEL * psh * DERATE * shade
    out(f"B5-{psh}-{int(shade * 100)}", f"harvest {label}: {h:.0f} mAh/day = {h / need:.1f} x daily need")
h1 = I_PANEL * 1 * DERATE
req("R6", f"{h1 / need:.0f} x need at 1 sun hour; {dark_days:.0f} days dark",
    "Energy-neutral at 1 sun hour; 90 days or more dark", "Met")
wh = CELL_MAH * CELL_V / 1000
out("B6", f"cell energy {wh:.2f} Wh (limit 2 Wh); charger NTC window 0 to 45 C; PTC fuse")
req("R7", f"LiFePO4, {wh:.2f} Wh, NTC 0 to 45 C, PTC fuse", "LiFePO4, 2 Wh or less, charge 0 to 45 C, fused", "Met")

# ---------------------------------------------------------------- C. Radio link (R5)
print("\nC. Radio link")
F = 868e6
LAM = 3e8 / F
P_RAD = 14.0         # dBm radiated (EU868 limit 14 dBm ERP); conducted power raised to cover the coax
COAX = 1.2 * 1.0 + 0.3   # dB: 1.2 m RG174 at about 1.0 dB/m, plus connectors
G_ANT = 0.0          # dBi, sleeve dipole taken at 0 dBi (a half-wave dipole is about 2 dBi)
SENS = -132.0        # dBm, gateway at SF10, 125 kHz
WALL = 12.0          # dB, farmhouse wall and window
FADE = 10.0          # dB, allowance for crop foliage and fading
H_GW = 3.0
out("C1", f"conducted power {P_RAD + COAX - G_ANT:.1f} dBm to radiate {P_RAD:.0f} dBm through {COAX:.1f} dB of coax "
          f"(module maximum +22 dBm)")


def two_ray(d, ht, hr):
    return 40 * math.log10(d) - 20 * math.log10(ht * hr)


def breakpoint(ht, hr):
    return 4 * math.pi * ht * hr / LAM


budget = P_RAD - SENS - WALL - FADE
h_ant = P["ant_center_z"] / 1000
cases = [("antenna 0.2 m on the head (TRL 2)", 0.2, H_GW, WALL),
         (f"antenna {h_ant:.1f} m on the marker rod (decided)", h_ant, H_GW, WALL),
         ("antenna 0.2 m, outdoor gateway on a 6 m mast", 0.2, 6.0, 0.0)]
margins = {}
for i, (name, ht, hr, wall) in enumerate(cases, 1):
    pl = two_ray(1000, ht, hr)
    b = P_RAD - SENS - wall - FADE
    margins[i] = b - pl
    out(f"C2-{i}", f"{name}: two-ray path loss at 1 km {pl:.1f} dB (valid beyond {breakpoint(ht, hr):.0f} m); "
                   f"budget {b:.0f} dB; margin {b - pl:.1f} dB")
m_dec = margins[2]
d_max = 10 ** ((budget + 20 * math.log10(h_ant * H_GW)) / 40)
out("C3", f"range at 0 dB margin with the decided antenna: {d_max:.0f} m")


def weissberger(depth_m, f_ghz=F / 1e9):
    return 1.33 * f_ghz ** 0.284 * depth_m ** 0.588 if depth_m > 14 else 0.45 * f_ghz ** 0.284 * depth_m


for dep in (20, 50, 100):
    out(f"C4-{dep}", f"Weissberger foliage loss through {dep} m of crop taller than the antenna: {weissberger(dep):.1f} dB")
d10 = next(dd for dd in range(15, 200) if weissberger(dd) >= FADE)
out("C5", f"tall crop depth that uses up the {FADE:.0f} dB allowance: about {d10} m")
req("R5", f"{m_dec:.1f} dB margin at 1 km (after 10 dB fade allowance); tall crops add {weissberger(50):.0f} to "
          f"{weissberger(100):.0f} dB", "90 % of uplinks at 1 km, indoor gateway, antenna on marker rod", "At risk")

# ---------------------------------------------------------------- D. EC circuit (R3)
print("\nD. EC circuit")
a = P["ec_d"] / 2 / 1000
s = P["ec_pitch"] / 1000
L = P["ec_exposed"] / 1000
K = math.acosh(s / (2 * a)) / (math.pi * L)     # 1/m, two parallel cylinders
out("D1", f"cell constant, two {P['ec_d']:.0f} mm rods at {P['ec_pitch']:.0f} mm, {P['ec_exposed']:.0f} mm exposed: "
          f"K = {K:.1f} 1/m ({K / 100:.3f} 1/cm); end effects lower it, calibration sets it")
R_REF = 330.0
V = 3.3
for ec in (0.1, 1.0, 4.0):
    sig = ec / 10     # dS/m to S/m
    rx = K / sig
    ratio = rx / (rx + R_REF)
    dr = (1 / 4096) / (R_REF / (rx + R_REF) ** 2)
    out(f"D2-{ec:g}", f"EC {ec:g} dS/m: electrode resistance {rx:.0f} ohm; divider ratio {ratio:.3f}; "
                      f"1 LSB (12 bit) = {dr / rx * 100:.2f} % of reading")
area = math.pi * P["ec_d"] * P["ec_exposed"] / 100     # cm2 per electrode
c_dl = 10e-6 * area                                     # F, 10 uF/cm2 double-layer (conservative low)
c_ser = c_dl / 2
rx4 = K / 0.4
i4 = V / (rx4 + R_REF)
t_s = 10e-6
drift = i4 * t_s / c_ser
out("D3", f"double layer {c_dl * 1e6:.0f} uF per electrode ({area:.1f} cm2 at 10 uF/cm2); at 4 dS/m, sampling {t_s * 1e6:.0f} us "
          f"after each edge of a 5 kHz square wave, polarization adds {drift * 1000:.1f} mV on {i4 * rx4 * 1000:.0f} mV "
          f"({drift / (i4 * rx4) * 100:.1f} %)")
drift_1k = i4 * 0.5e-3 / c_ser
out("D3b", f"same at the end of a 1 kHz half period (500 us): {drift_1k * 1000:.0f} mV ({drift_1k / (i4 * rx4) * 100:.0f} %)")
out("D4", "temperature correction 2 %/C with DS18B20 at +/-0.5 C: +/-1.0 % of reading; "
          "ADC nodes on both sides of the reference resistor cancel the GPIO drive resistance")
req("R3", f"circuit error under 2 % from 0.1 to 4 dS/m (K = {K / 100:.3f} 1/cm, 330 ohm reference)",
    "0 to 4 dS/m, +/-10 % or +/-0.1 dS/m after calibration", "Met")

# ---------------------------------------------------------------- E. Moisture and temperature sensing (R1, R2)
print("\nE. Moisture and temperature")
out("E1", f"sensing centers {P['depths'][0]:.0f} and {P['depths'][1]:.0f} mm below grade, blades {P['probe_l']:.0f} mm "
          f"long, so each reads {P['depths'][0] - P['probe_l'] / 2:.0f} to {P['depths'][0] + P['probe_l'] / 2:.0f} mm and "
          f"{P['depths'][1] - P['probe_l'] / 2:.0f} to {P['depths'][1] + P['probe_l'] / 2:.0f} mm")
out("E2", "accuracy depends on soil contact and the two-point site calibration; not verifiable by calculation")
req("R1", f"depths {P['depths'][0]:.0f} and {P['depths'][1]:.0f} mm by model; accuracy unverified",
    "150 and 300 mm (+/-25 mm); +/-3 % VWC after site calibration", "At risk")
out("E3", f"DS18B20 at {P['t_depth']:.0f} mm; datasheet +/-0.5 C from -10 to 85 C")
req("R2", f"+/-0.5 C, -10 to 85 C, at {P['t_depth']:.0f} mm", "+/-0.5 C from -10 to 60 C at about 225 mm", "Met")

# ---------------------------------------------------------------- F. Thermal (R8, R9)
print("\nF. Thermal and sealing")
NOCT, G = 45.0, 1000.0
dT_panel = (NOCT - 20) / 800 * G
T_AIR = 45.0
T_head = T_AIR + 0.6 * dT_panel
out("F1", f"panel {T_AIR + dT_panel:.0f} C at {T_AIR:.0f} C air and {G:.0f} W/m2 (NOCT {NOCT:.0f} C); "
          f"head interior about {T_head:.0f} C (air plus 0.6 of the panel rise)")
ALPHA = 0.5e-6    # m2/s, moist loam
omega = 2 * math.pi / 86400
Dd = math.sqrt(2 * ALPHA / omega)
zc = -P["cell_z"] / 1000
for label, mean, amp in (("bare soil, hot summer", 35.0, 20.0), ("under a crop canopy, summer", 28.0, 8.0),
                         ("bare soil, cold winter", -2.0, 5.0)):
    A = amp * math.exp(-zc / Dd)
    out(f"F2-{label.split(',')[0][:4]}-{label.split()[-1][:4]}",
        f"cell at {zc * 1000:.0f} mm, {label}: surface {mean - amp:.0f} to {mean + amp:.0f} C, damping depth {Dd * 1000:.0f} mm, "
        f"cell {mean - A:.1f} to {mean + A:.1f} C")
A_hot = 20.0 * math.exp(-zc / Dd)
# F4 (RMS-DDR-002): how deep would the cell have to sit to stay at or below 40 C in bare hot soil?
z_need = Dd * math.log(20.0 / (40.0 - 35.0))
spigot_top = -(P["fin_top"] + P["spigot_l"] - 10)       # depth of the fin spigot top inside the tube
win_top = P["depths"][0] - P["probe_l"] / 2
z_max = spigot_top - P["cell_l"] / 2                      # deepest cell center above the spigot
A_max = 20.0 * math.exp(-z_max / 1000 / Dd)
out("F4", f"cell center for 40 C or less in bare hot soil: {z_need * 1000:.0f} mm deep; the fin spigot reaches up to "
          f"{spigot_top:.0f} mm and the upper probe window starts at {win_top:.0f} mm, so the deepest cell center that fits "
          f"is about {z_max:.0f} mm ({35 + A_max:.1f} C); a deeper cell alone cannot meet R9 without moving the "
          f"150 mm probe that R1 fixes")
req("R9", f"head about {T_head:.0f} C at 45 C air (parts rated 85 C); cell up to {35 + A_hot:.0f} C in bare hot soil",
    "-10 to 60 C at the head; -5 to 40 C at the cell", "At risk")
v_l = D["head_air_l"]
T1, T2 = 293.15, 273.15 + T_head
dp = 101.325 * (T2 / T1 - 1)
p_imm = 1000 * 9.81 * 0.5 / 1000
out("F3", f"sealed head air about {v_l * 1000:.0f} cm3; heating 20 to {T_head:.0f} C raises it {dp:.1f} kPa, "
          f"against {p_imm:.1f} kPa for 0.5 m immersion; an ePTFE vent removes the daily pumping")
req("R8", f"thermal pumping {dp:.0f} kPa daily without a vent; vent added", "Head IP67; buried IP68 at 0.5 m; UV-stable",
    "Not verifiable at TRL 3")

# ---------------------------------------------------------------- G. Installation (R10, R11)
print("\nG. Installation and geometry")
A_sec = (D["fin_section_mm2"] + 2 * math.pi * (P["ec_d"] / 2) ** 2) / 1e6
# with the slot tool (RMS-DDR-002) the fin only widens a 32 x 8 mm pre-cut slot; the EC rods (4 mm) pass
# inside it. Shaft friction is kept unchanged (conservative: the fin faces still displace 2 mm of soil each side)
A_slot = (D["fin_section_mm2"] - D["slot_area_mm2"]) / 1e6
per = D["fin_perimeter_mm"] / 1000
fin_in = (P["tube_bot"] - P["fin_bot"]) / 1000
forces, forces_slot = {}, {}
for label, qc, fs in (("moist loam (after irrigation)", 0.5e6, 10e3), ("firm dry loam", 2.0e6, 30e3)):
    f = qc * A_sec + fs * per * fin_in
    fsl = qc * A_slot + fs * per * fin_in
    forces[label], forces_slot[label] = f, fsl
    out(f"G1-{label.split()[0]}", f"push force, {label}: tip {qc * A_sec:.0f} N + shaft {fs * per * fin_in:.0f} N "
                                  f"= {f:.0f} N ({f / 9.81:.0f} kgf); fin {fin_in * 1000:.0f} mm into undisturbed soil")
    out(f"G4-{label.split()[0]}", f"with the slot tool, {label}: tip {qc * A_slot:.0f} N on the residual "
                                  f"{A_slot * 1e6:.0f} mm2 + shaft {fs * per * fin_in:.0f} N = {fsl:.0f} N ({fsl / 9.81:.0f} kgf)")
out("G2", "one person leaning on the head gives about 500 N (51 kgf)")
out("G5", f"slot tool: {P['slot_w']:.0f} x {P['slot_t']:.0f} mm steel blade, point at {-D['ec_bot']:.0f} mm, driven with a "
          f"mallet ({D['slot_blade_l']:.0f} mm from point to handle), so hammer blows go into the tool, not the stake head")
req("R10", f"with slot tool {forces_slot['moist loam (after irrigation)']:.0f} N moist, "
           f"{forces_slot['firm dry loam']:.0f} N firm dry (without: {forces['moist loam (after irrigation)']:.0f} N, "
           f"{forces['firm dry loam']:.0f} N)",
    "One person, 50 mm auger, 15 min; depths +/-25 mm", "At risk")
out("G3", f"head top {D['head_top']:.0f} mm above grade; antenna {D['ant_bot']:.0f} to {D['ant_top']:.0f} mm on the "
          f"flexible rod; rod top {D['rod_top']:.0f} mm; flag center {P['flag_z']:.0f} mm")
req("R11", f"head {D['head_top']:.0f} mm; flag {P['flag_z']:.0f} mm, rod {D['rod_top']:.0f} mm",
    "Rigid head 300 mm or less; marker 1 m or more; antenna only on the flexible rod", "Met")

# ---------------------------------------------------------------- H. Cost (R12) and data (R13, R14)
print("\nH. Cost")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
stake = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows if int(r["item"].split()[0]) <= 12) / 3
total = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows)
budget_usd = None
for line in (ROOT / "project.yaml").read_text().splitlines():
    if line.startswith("budget_usd:"):
        budget_usd = float(line.split(":")[1].split("#")[0])
tool = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows if int(r["item"].split()[0]) == 15)
out("H1", f"one stake ${stake:.2f}; three stakes ${3 * stake:.2f}; gateway $90.00; slot tool ${tool:.2f}; pilot set ${total:.2f} "
          f"against budget ${budget_usd:.0f} (headroom ${budget_usd - total:.2f})")
req("R12", f"${stake:.2f} per stake; ${total:.2f} pilot set", "$60 per stake; $300 pilot set", "Met")
req("R13", "TTN community server (free), webhook to a local Node-RED or Grafana with CSV export",
    "No paid subscription; CSV export; open dashboard", "Met")
req("R14", "316 stainless electrodes; epoxy-sealed probes; life unverified", "12 months buried", "At risk")

# ---------------------------------------------------------------- Results
print("\nResults against RMS-REQ-001 v0.4")
order = {"Not met": 0, "At risk": 1, "Not verifiable at TRL 3": 2, "Met on paper": 3, "Met": 4}
RESULTS.sort(key=lambda r: (order[r[3]], int(r[0][1:])))
for rid, v, t, st in RESULTS:
    print(f"{rid:<4} {st:<24} {v}  |  target: {t}")
counts = {}
for r in RESULTS:
    counts[r[3]] = counts.get(r[3], 0) + 1
print("counts: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items(), key=lambda kv: order[kv[0]])) +
      f"; total {len(RESULTS)}")
