---
doc_id: RMS-BLD-001
title: RootMesh prototype build plan
project: RootMesh
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (RMS-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Decisions of 2026-10-02 carried into the plan and pictures: 915 MHz dipole and US915 gateway, cell chosen, status LED and its resistor"
---

# RootMesh prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every stake component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. The 20 stake components, pulled apart and numbered in build order. The marker rod and antenna lead are drawn shortened.*

![Figure 2. The slot tool, pulled apart](05-build-plan/overview-tool.png)

*Figure 2. The slot tool, one per pilot set, used to cut the path for the fin before each stake goes in.*

The prototype is one RootMesh sensor stake, installed in a trial bed of soil, and the steel slot tool that prepares the ground for it. The stake is a flat sensor fin pushed into the soil, carrying two moisture probes, a temperature probe and two steel electrodes; a short plastic pipe above it holds a small lithium iron phosphate cell; and a printed head just above the ground holds the controller board under a cap that carries the solar panel. The antenna stands on a flagged fibreglass marker rod beside the stake. Figure 1 shows the 20 stake components in the order you make or fit them. Eight are made in a small workshop: the two halves of the fin, the head body and cap, the cell holder and the two antenna clips are 3D printed, the pipe is cut to length, and the two electrodes are cut and pointed from stainless rod. The slot tool (Figure 2) is a steel blade, a round bar handle, two shaft collars and a printed depth stop. Everything else is bought: the probes, temperature probe, cell, panel, electronic modules, antenna, status LED, O-ring, gland, inserts, screws, rod and flag. The work is 3D printing, sawing, drilling and grinding steel bar, gluing with epoxy, and soldering bought modules together. The parts cost about $59.15 a stake and $281.45 for a pilot set of three stakes, a gateway and a slot tool, from the bill of materials.

> **Safety:** The stake holds a lithium iron phosphate cell of about 1.9 Wh and its charger. Keep the cell out of its holder until section 6 says otherwise, never charge it below 0 °C or above 45 °C, and never leave a first build charging unattended. The slot tool is a pointed steel blade struck with a mallet: wear eye protection and gloves and keep feet clear of the point. Grinding steel throws sparks; grind away from anything that burns. Epoxy and printing ASA give off fumes; work in a ventilated space and wear nitrile gloves with epoxy. The fin tip and electrodes are sharp: cover them when the stake is not in the ground.

## 2. What changed to make it buildable

The concept showed what the stake does; some of its parts could not be made, fitted or fixed as drawn. Each change below keeps what the stake does (the same sensing depths, electrode spacing, cell depth, panel and antenna height), and all of them are recorded in decision record RMS-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Head | One printed cup with only a 28 mm hole into it; an O-ring that sealed nothing; no fixing to the tube | A body bonded over the tube and a removable cap carrying the panel, sealed by an O-ring on the body rim and held by two screws (Figure 19) | The 56 mm board can now go in from the top, and the head is sealed and fixed |
| Controller board | Loose in the head | Stands in two guide slots printed in the body (Figure 15) | A fixing that needs no extra part |
| Top of the fin | Ran 10 mm inside the tube, cutting into its wall; the upper probe window reached inside the tube | A 42 mm collar the tube end sits on, and a spigot glued inside the tube; the tube moved up 14 mm (Figure 11) | Keeps the probe at 150 mm and gives the tube a stop and a sealed joint |
| Fin | Solid, with nowhere to hold the sensors or run their wires | Two printed halves glued together, with slots, pockets, wire channels, a bore and grooves inside (Figures 8 and 9) | Traps and pots every sensor and carries its wires to the tube |
| Temperature probe | Stood 7 mm proud of the fin edge, where installation would tear it off | Lies in a bore in the fin edge, 0.4 mm proud (Figure 6) | Survives installation and still touches the soil |
| Fin tip and electrodes | A round cone wider than the fin; each electrode in three loose pieces | A wedge tip between the electrodes; each electrode one 80 mm rod held in the foot (Figure 5) | The bare length and spacing that set the reading are unchanged |
| Cell | Loose in the tube | A printed holder standing on the spigot top (Figure 11) | Holds the cell at 62 mm and lifts out for a change |
| Gland and vent | The gland at the cap's parting line, in line with the board; the vent where a screw boss now is | Gland 100 mm above grade, turned toward the front; vent at the back right (Figure 16) | Both clear the board and the bosses |
| Antenna clip | A block that overlapped the rod; the lead hung in the air | Two printed clips and four cable ties (Figure 21) | A fixing that slides on by hand |
| Slot tool | A handle that passed through the blade's own plane; a loose depth stop | A bar through a cross hole with two shaft collars; a stop clamped by a thumb screw (Figures 24 and 25) | No welding; the stop can be set |
| Installation | Auger hole 120 mm deep | Auger hole 110 mm deep, to the bottom of the collar | Follows the collar; the fin is pushed 10 mm further into firm soil |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. Directions are as seen standing at the front of the stake: the panel slopes down to your right, toward the equator, and the marker rod stands on your left. The front half of the fin (the one with the electronics pockets) faces you. Depths are measured down from the soil surface, heights up from it. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Moisture probes (prepare 2)

![Figure 3. A probe board in the front fin half](05-build-plan/joint-01.png)

*Figure 3. A probe board in its slots in the front half of the fin, with its electronics end in the pocket above the window (shown for the upper probe).*

**What it is and what it is made from.** A bought capacitive soil moisture board, version 1.2 class, about 23 mm wide and 98 to 100 mm long, with its parts on one face at the top end. It is changed so that it gives a frequency, not a voltage, and so that it survives in wet soil.

**How to prepare it.**

1. Remove the NE555 timer and fit a TLC555 in its place (the low-voltage CMOS version, which runs at 3.3 V and draws less current).
2. Solder a three-core lead of 0.25 mm² (24 AWG) wire, about 600 mm long, to the board's power, ground and output pads in place of its plug.
3. Paint every cut edge of the board with a thin coat of epoxy, so water cannot creep into the board's layers. Let it cure.
4. Label each lead: "upper" and "lower".

**How it fits the parts next to it.** Each board lies in the middle of the fin, its two long edges held 2 mm deep in slots in each fin half, its sensing area behind a 19 mm window open on both faces, and its electronics end in a pocket above the window (Figure 3). Its lead runs from the top of the board up to the spigot: straight up for the upper probe, and along a cross channel and the left wire channel for the lower probe (Figure 9).

**Check before moving on.** Each board lies flat in its slots in the front fin half with its parts inside the pocket; at 3.3 V the output gives a steady square wave whose frequency falls when you hold the sensing area in your hand.

### 3.2 EC electrodes (make 2)

![Figure 4. Making sketch of the EC electrode](../cad/drawings/RMS-DWG-103.png)

*Figure 4. EC electrode making sketch (RMS-DWG-103).*

![Figure 5. The electrodes in the fin foot](05-build-plan/joint-02.png)

*Figure 5. Each electrode lies 15 mm in its groove in the fin foot; 5 mm is sleeved below the foot, then 60 mm is bare.*

**What it is and what it is made from.** One of the two steel rods below the fin that measure the soil's electrical conductivity. Type 316 stainless steel rod, 4 mm diameter.

**How to make it.**

1. Cut two 80 mm lengths of rod. Square the top ends with a file.
2. Grind the other end to a point about 4 mm long, keeping the tip on the rod's centre line.
3. Clean the top 15 mm with abrasive paper. Tin it using flux made for stainless steel and solder on a 0.25 mm² lead about 600 mm long (or crimp the lead in a 4 mm splice). Wash off all the flux.
4. Slide a 5 mm length of 4 mm heat-shrink sleeve onto the rod so it sits 15 to 20 mm from the top end, and shrink it.

**How it fits the parts next to it.** The top 15 mm of each rod lies in a 4.1 mm groove between the two fin halves, 12 mm either side of the centre line (24 mm apart), set in the epoxy that glues the halves. The sleeve sits just below the fin foot, and the 60 mm below it is bare. The fin's wedge tip sits between the two rods (Figure 5).

**Check before moving on.** The bare length is 60 mm on both rods (it sets the reading); no flux is left on the bare steel; the soldered lead holds a firm pull.

### 3.3 Temperature probe

![Figure 6. The temperature probe in the fin edge](05-build-plan/joint-03.png)

*Figure 6. The probe's steel sheath lies in a bore in the right edge of the fin, 0.4 mm proud of the edge, between the two windows.*

**What it is and what it is made from.** A bought DS18B20 digital temperature sensor in a 6 mm stainless steel sheath, about 50 mm long, with a 1 m three-core lead.

**How to prepare it.** Cut the lead to about 600 mm. Strip the outer jacket from the first 300 mm next to the sheath, so the three inner wires lie flat in the wire channel; keep the inner insulation whole.

**How it fits the parts next to it.** The sheath lies in a 6.2 mm bore in the right edge of the fin, 15.4 mm from the centre line, from 200 to 250 mm deep, so its outer face stands 0.4 mm out from the fin edge and touches the soil. Its wires run up the right wire channel to the spigot. The epoxy that glues the halves fills round it.

**Check before moving on.** The sheath drops into the bore in the front half and stands just proud of the edge; it reads room temperature to within 0.5 °C of a reference thermometer.

### 3.4 Sensor fin halves (print 2: a front and a back)

![Figure 7. Making sketch of the front fin half](../cad/drawings/RMS-DWG-101.png)

*Figure 7. Front half making sketch (RMS-DWG-101).*

![Figure 8. Making sketch of the back fin half](../cad/drawings/RMS-DWG-102.png)

*Figure 8. Back half making sketch (RMS-DWG-102).*

![Figure 9. The inside face of a fin half, with every cut sized](05-build-plan/fin-layout.png)

*Figure 9. The inside (glue) face of the front half, drawn lying down with the top on the left, with every cut sized from the model.*

**What it is and what it is made from.** The flat blade that is pushed into the soil and carries all the sensors. It is printed in two halves, 6 mm thick each, that are glued face to face into a blade 36 mm wide, 12 mm thick and 310 mm long, with a half collar (42 mm across, 4 mm thick) and a half spigot (35.4 mm across, 11 mm long) at the top and a wedge tip at the bottom. PETG or ASA, printed flat on its outside face at 100 % infill.

**How to make it.**

1. Print each half lying on its outside face, so the inside face with all its cuts faces up. A half is 355 mm long overall: print it on a 300 x 300 mm bed laid diagonally.
2. Clean out every slot, channel, pocket, bore and groove with a hobby knife; there must be no strings of plastic in the wire channels.
3. Check the cuts against Figure 9: two windows 19 wide and 80 long through the half, centred 150 and 300 mm deep; board slots 23.2 wide and 0.9 deep each half, 100 long; two wire channels 3.5 wide and 2.5 deep each half, centred 14.75 mm each side, from 405 mm deep up through the spigot; a cross channel from the top of the lower probe to the left channel; a 6.2 mm bore on the right edge from 200 to 250 mm deep; two 4.1 mm grooves for the electrodes, 15 mm long, in the foot. The front half also has two electronics pockets, 16 wide and 3.4 deep, above each window.
4. Lightly sand both glue faces flat on abrasive paper laid on a flat board, and wipe them with isopropyl alcohol.

**How it fits the parts next to it.** The two halves meet on their inside faces and are glued with epoxy, which also fills round the probes, electrodes and temperature probe and their wires (Figures 3, 5 and 6). The tube's bottom end sits on the collar and is glued over the spigot (Figure 11). The cell holder's legs stand on the spigot top. The channels and the upper probe's pocket open at the spigot top, where the wires leave the fin.

**Check before moving on.** Lay the two halves face to face with nothing between them: the windows, slots, channels, bore and grooves line up, and no light shows along the joint. A 4 mm rod drops into each electrode groove, and each probe board lies flat in its slots.

### 3.5 Stake tube

![Figure 10. Making sketch of the stake tube](../cad/drawings/RMS-DWG-104.png)

*Figure 10. Stake tube making sketch (RMS-DWG-104).*

**What it is and what it is made from.** The pipe between the fin and the head that carries the cell and the wires. PVC pressure pipe, 42 mm outside and 36 mm inside diameter (40 mm or 1-1/4 in nominal).

**How to make it.**

1. Cut 170 mm of pipe with a fine-tooth saw in a mitre box, so both ends are square to within 0.5 mm.
2. Deburr inside and out, and chamfer the outside of the bottom end 1 mm.
3. Roughen the outside of the top 26 mm and the inside of the bottom 15 mm with 120 grit paper, for the epoxy.

**How it fits the parts next to it.**

![Figure 11. The tube on the fin collar, cut open](05-build-plan/joint-04.png)

*Figure 11. The tube's bottom end sits on the 42 mm collar and is glued over the spigot; the cell holder's legs stand on the spigot top.*

The bottom end sits on the fin collar, 106 mm below the soil surface, glued over the spigot with about 0.3 mm of epoxy all round (Figure 11). The top end goes 24 mm into the head socket, 2 mm short of its floor, with about 0.5 mm of epoxy all round (Figure 14).

**Check before moving on.** The spigot slides into the tube, and the head socket slides over it, by hand, with an even gap.

### 3.6 Cell holder

![Figure 12. Making sketch of the cell holder](../cad/drawings/RMS-DWG-105.png)

*Figure 12. Cell holder making sketch (RMS-DWG-105).*

**What it is and what it is made from.** A printed sleeve that holds the cell at the right depth inside the tube. ASA, printed upright.

**How to make it.**

1. Print the holder: a sleeve 22 mm outside and 15 mm inside diameter, 51 mm long, on a 3 mm base, standing on two legs 4 x 4 mm and 5 mm tall, 16 mm apart. The base has a 4 mm hole 5 mm off centre for the cell's lower lead.
2. Tie a loop of strong nylon cord through the top of the sleeve, long enough to reach out of the head.

**How it fits the parts next to it.** It drops down the tube and stands on the spigot top, its legs either side of the upper probe's pocket, so the cell's centre is 62 mm below the soil surface (Figure 11). The cell slides into the sleeve. The holder is 22 mm across, so it passes the 28 mm hole in the head floor and lifts out on its cord once the cap and board are out.

**Check before moving on.** The cell slides in by hand; the holder drops through a 28 mm hole and down the tube without catching.

### 3.7 Head body, with its gland, vent, status LED and inserts

![Figure 13. Making sketch of the head body](../cad/drawings/RMS-DWG-106.png)

*Figure 13. Head body making sketch (RMS-DWG-106).*

**What it is and what it is made from.** The lower part of the head, just above the ground: a printed cup that is glued over the tube and holds the controller board. ASA, printed upright with the socket down, five walls, 40 % infill.

**How to make it.**

1. Print the body: a cup 72 mm across and 80 mm tall. At the bottom, a socket 43 mm across and 26 mm deep for the tube; above it a 3 mm floor with a 28 mm hole; above that, a cavity 62 mm across with a 5 mm wall.
2. Check the two board guides on the left and right walls: slots 1.8 mm wide and 3 mm deep, 44 mm tall, starting 36 mm above the body's bottom.
3. Check the two bosses on the front and back walls, 29.5 mm from the centre, each with a 4.6 mm hole 6 mm deep.
4. Press an M3 brass heat-set insert into each boss hole with a soldering iron at about 220 °C, until it sits flush with the rim.
5. Fit the antenna gland through the 8.2 mm hole in the gland boss, 60 mm up the body, on the left, turned 30 degrees toward the front, with its seal outside and its locknut inside; tighten the locknut by hand and a quarter turn.
6. Stick the ePTFE vent membrane on the inside of the body over the 4 mm vent hole at the back right, 42 mm up, pressing it flat round its edge.
7. Check the 5.2 mm lens hole through the wall at the front right, 60 mm up and at least 45 degrees round from the gland and the vent. Press the 5 mm green LED into it from inside until its 5.8 mm flange sits against the inside wall; the flange is larger than the hole, so the LED cannot fall out. Run a thin bead of epoxy round the flange on the inside and leave its two leads long.

**How it fits the parts next to it.**

![Figure 14. The tube in the head socket, cut open](05-build-plan/joint-05.png)

*Figure 14. 24 mm of tube in the 26 mm socket, with about 0.5 mm of epoxy all round; the floor hole above lets the wires and the cell holder through.*

![Figure 15. The board in its guide slots](05-build-plan/joint-06.png)

*Figure 15. Seen from above with the cap off: the board's edges in the two guide slots, clear of the gland locknut and the screw bosses.*

![Figure 16. The antenna lead through its gland](05-build-plan/joint-08.png)

*Figure 16. The gland on its flat boss, with its locknut on a flat inside; the lead runs to the marker rod.*

The socket is glued over the top of the tube (Figure 14). The board stands in the guides (Figure 15). The cap sits on the rim, its O-ring sealing on the rim face, held by two screws into the inserts (Figure 19). The gland faces the marker rod (Figure 16).

**Check before moving on.** The rim is flat (no gap under a straightedge); the board slides down both guides without force; the inserts are square and flush.

### 3.8 Controller board (bought modules)

![Figure 17. Block-level wiring](05-build-plan/wiring.png)

*Figure 17. Block-level wiring with wire sizes. No circuit board is laid out at this stage; bought modules on a prototype board stand in for the carrier board.*

The carrier board in the bill of materials is a custom board, which is TRL 4 work. For this prototype, lay out bought modules on a 56 x 40 mm prototype board (perforated board, 1.6 mm thick) to this specification:

*Table 2. Modules that stand in for the carrier board.*

| Module | What to buy |
| --- | --- |
| Radio and controller | STM32WLE5-class LoRaWAN module (Seeed Wio-E5 or similar) on its maker's small breakout, set to the US915 band plan (902 to 928 MHz) |
| Charger | Single-cell lithium iron phosphate solar charger (CN3058E class), charge voltage 3.6 V, with a temperature input that stops charging below 0 °C and above 45 °C, and a 3.3 V output or a 3.3 V regulator after it |
| Load switch | A small high-side switch that the controller turns on to power the sensors for about 1 s per reading |
| EC drive | Two controller pins driving the electrodes through a 330 Ω reference resistor, with both sides of the resistor wired to analog inputs |
| Status light | One 560 Ω, 0.25 W axial resistor in series with the green LED, on one controller pin: about 2 mA when lit. The controller blinks it once for 0.1 s after each uplink and three times when a magnet or button wakes it, and at no other time |

Wire it like this, with stranded copper, every joint soldered and sleeved, and a plug-in header for each lead that leaves the board:

1. Panel lead (from the cap) to the charger input: 0.5 mm².
2. Cell holder leads, through the cell's fuse, to the charger battery terminals: 0.5 mm².
3. The cell's temperature sensor to the charger's temperature input: 0.25 mm², twisted.
4. Charger 3.3 V output to the controller and to the load switch: 0.5 mm².
5. Load switch output to the supply wire of each probe and of the temperature probe: 0.25 mm².
6. Probe outputs and the temperature probe's data wire to controller pins: 0.25 mm².
7. Electrode leads to the EC drive: 0.25 mm².
8. Controller to the antenna: the u.FL pigtail to the gland, then the lead through the gland.
9. Controller pin to the 560 Ω resistor on the board, then a pair of 0.25 mm² leads from the resistor and the 3.3 V rail to the LED in the head wall, through a plug-in header.

Check that the charger's temperature window really is 0 to 45 °C in its datasheet before buying: some chargers of this class fix a different window.

**Check before moving on.** Every wire continues end to end; with no cell fitted, the battery terminals and the 3.3 V rail read open to ground; every lead and header is labelled.

### 3.9 Head cap, with its panel and O-ring

![Figure 18. Making sketch of the head cap](../cad/drawings/RMS-DWG-107.png)

*Figure 18. Head cap making sketch (RMS-DWG-107).*

**What it is and what it is made from.** The top of the head: a printed cap sloped 30 degrees toward the equator, carrying the solar panel and sealing the head. ASA, printed with the sloped top on the bed and supports under the rim only.

**How to make it.**

1. Print the cap: 72 mm across, 9 mm tall at its low edge and 51 mm at its high edge, with a 3 mm roof and hollow underneath.
2. Check the panel recess, 71 x 51 mm and 1 mm deep, the 5 mm lead hole at its centre, the O-ring groove in the rim face (64.0 to 69.2 mm across, 1.5 mm deep), and the two 3.4 mm screw holes over the bosses, counterbored 6.4 mm from the top down to 3 mm above the rim face.
3. Pass the panel's lead through the hole. Run a bead of clear outdoor sealant round the recess and over the hole, press the panel in, wipe off the excess and let it cure for a day.
4. Lay the 64 x 2 mm O-ring in its groove.

**How it fits the parts next to it.**

![Figure 19. The cap on the body, cut through a screw](05-build-plan/joint-07.png)

*Figure 19. The O-ring seals on the body rim; each screw passes through a solid column in the cap into an insert in a body boss.*

The cap sits on the body rim with the O-ring between them. Two M3 x 12 stainless button-head screws, each with an EPDM sealing washer under its head, pass through the cap into the inserts and are tightened snug, enough to close the gap evenly but not to crush the O-ring flat (Figure 19). The panel faces the equator.

**Check before moving on.** The O-ring stands about 0.5 mm out of its groove; the panel is bonded all round with no gap at its edge.

### 3.10 Antenna clips (print 2)

![Figure 20. Making sketch of the antenna clip](../cad/drawings/RMS-DWG-108.png)

*Figure 20. Antenna clip making sketch (RMS-DWG-108).*

**What it is and what it is made from.** A small printed block that holds the dipole beside the marker rod. ASA, printed flat.

**How to make it.** Print two blocks 23 x 12 x 12 mm, each with an 8.2 mm hole for the rod and a 10.2 mm hole for the dipole, 10 mm apart centre to centre, straight through the 12 mm height. Ream the holes with a drill if tight.

**How it fits the parts next to it.**

![Figure 21. The dipole clipped to the rod](05-build-plan/joint-09.png)

*Figure 21. Two clips hold the dipole beside the top of the rod; the lead is tied to the rod below them.*

Both clips slide over the rod top, centred 925 and 985 mm above the soil surface; the dipole slides down through them until its centre is level with the rod top, 1,000 mm above the soil. A cable tie above and below each clip stops it sliding.

**Check before moving on.** The rod and the dipole each slide through by hand without play.

### 3.11 Slot tool

![Figure 22. Making sketch of the slot tool blade and handle](../cad/drawings/RMS-DWG-109.png)

*Figure 22. Blade and handle making sketch (RMS-DWG-109).*

![Figure 23. Making sketch of the depth stop](../cad/drawings/RMS-DWG-110.png)

*Figure 23. Depth stop making sketch (RMS-DWG-110).*

**What it is and what it is made from.** A steel blade, the same shape as the fin but slightly thinner, that is driven down the auger hole with a mallet and pulled out, so the fin only has to widen a slot. Mild steel flat bar 32 x 8 mm for the blade; 20 mm round bar for the handle; two 20 mm bore shaft collars; a printed ASA depth stop with an M5 thumb screw and nut.

**How to make it.**

1. Blade: cut 650 mm of flat bar. Grind one end to a point 40 mm long, the full 32 mm width tapering to the centre. Chamfer the other end (the struck end) 1 mm.
2. Clamp the blade in a vice and drill a 20.5 mm cross hole on its centre line, 25 mm below the struck end: pilot 6 mm, then step up.
3. Handle: cut 250 mm of 20 mm round bar and chamfer both ends.
4. Depth stop: print a disc 80 mm across and 15 mm thick with a 32.6 x 8.6 mm slot through its centre, a 5.4 mm hole from its edge to the slot, and a slot for an M5 nut 20 mm from the centre, open at the top.
5. Mark the blade 485 mm up from the point with a paint pen.

**How it fits the parts next to it.**

![Figure 24. The handle through the blade](05-build-plan/joint-10.png)

*Figure 24. The bar passes the cross hole; a collar each side keeps it centred.*

![Figure 25. The depth stop on the blade](05-build-plan/joint-11.png)

*Figure 25. The thumb screw passes the trapped nut and presses on the blade's wide face.*

The handle passes through the cross hole, centred, with a shaft collar against each face of the blade, set screws tight on the bar (Figure 24). The depth stop slides up the blade from the point until its top face is at the 485 mm mark; the M5 nut drops into its slot and the thumb screw, through the nut, clamps the stop on the blade's wide face (Figure 25). In use the stop rests on the soil beside the auger hole and stops the point 485 mm deep, level with the electrode tips.

**Check before moving on.** The blade is straight within 2 mm and the point is on its centre line; the handle does not slide in the collars; one finger-tight turn of the thumb screw holds the stop under a firm pull.

### 3.12 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Solar panel (line 1).** 5 V, 0.5 W monocrystalline, about 70 x 50 mm, epoxy or PET laminate, with its lead on the back near the centre.
- **Controller (line 3).** The modules of Table 2 and a 56 x 40 mm prototype board (line 16).
- **Antenna (line 4).** Half-wave sleeve dipole for 915 MHz, about 164 mm long and 10 mm across, with 1.2 m of RG174 lead and a u.FL to SMA pigtail.
- **Cell (line 5).** 14500 size lithium iron phosphate cell, 3.2 V, 600 mAh, of the IFR14500EC class, whose datasheet rates discharge from -20 to +60 °C and charge from 0 to +60 °C (the charger still stops charging above 45 °C), with a resettable (PTC) fuse and leads fitted.
- **Gateway (line 13).** Indoor eight-channel LoRaWAN gateway, US915 version, with its own antenna, Wi-Fi link and USB supply, joined to The Things Network. It is not part of the stake and stays indoors.
- **Pipe (line 6).** 42 mm outside diameter PVC pressure pipe, 170 mm.
- **Moisture probes (line 8).** Two capacitive soil moisture boards, version 1.2 class, and two TLC555 timers.
- **Electrode rod (line 9).** 4 mm 316 stainless steel rod, 160 mm.
- **Temperature probe (line 10).** DS18B20 in a 6 mm stainless sheath with a 1 m lead.
- **Marker rod and flag (line 11).** 8 mm fibreglass rod, 1.2 m, with a high-visibility flag; four cable ties.
- **Seals (line 12).** One 64 x 2 mm nitrile or EPDM O-ring; one M8 IP68 cable gland for 2 to 4 mm cable; an adhesive ePTFE vent membrane about 10 mm across; a desiccant sachet; two-part epoxy for potting.
- **Fixings and bonding (line 16).** Two M3 brass heat-set inserts (short, for a 4.6 mm hole); two M3 x 12 stainless button-head screws and two EPDM sealing washers; structural two-part epoxy; 4 mm heat-shrink sleeve.
- **Status LED and resistor (line 17).** One 5 mm green diffused LED with a 5.8 mm flange, and one 560 Ω, 0.25 W axial resistor.
- **Slot tool (line 15).** 650 mm of 32 x 8 mm mild steel flat bar; 250 mm of 20 mm mild steel round bar; two 20 mm bore shaft collars with set screws; an M5 thumb screw about 40 mm long and an M5 nut.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in. Steps 1 to 11 are done on the bench; steps 12 to 16 install the stake in a trial bed of soil, at least 600 mm deep.

### Step 1: probes into the front fin half

![Step 1](05-build-plan/step-01.png)

Lay the front half on the bench, inside face up. Lay each probe board in its slots with its parts up in the pocket and its lead in its channel: the upper probe's lead straight out of the spigot top, the lower probe's lead along the cross channel and up the left channel.

### Step 2: electrodes and temperature probe into the front half

![Step 2](05-build-plan/step-02.png)

Lay each electrode in its groove with its sleeve against the foot and its lead in the channel on its side. Lay the temperature probe's sheath in its bore and its wires in the right channel. Tape the leads together where they leave the spigot.

### Step 3: glue on the back half

![Step 3](05-build-plan/step-03.png)

Mix enough slow-setting epoxy for the whole fin. Fill every channel and pocket round the wires, coat both glue faces, press the back half on, and clamp the halves every 50 mm between two straight battens. Wipe the excess from the windows, the edges and the bare electrodes. Let it cure fully. **Hold point:** each lead still continues end to end and none is shorted to another.

### Step 4: tube onto the fin spigot

![Step 4](05-build-plan/step-04.png)

Thread all the fin leads up through the tube. Coat the spigot and the inside of the tube's bottom end with structural epoxy and push the tube down until it sits on the collar all round. Wipe the joint and stand the fin upright until the epoxy cures.

### Step 5: gland, vent and status LED into the head body

![Step 5](05-build-plan/step-05.png)

If not done in section 3.7: inserts flush in the bosses, gland through its boss with the locknut inside, vent membrane on the inside over its hole, and the LED pressed into its lens hole with its flange against the inside wall.

### Step 6: head body onto the tube

![Step 6](05-build-plan/step-06.png)

Thread all the leads up through the floor hole. Coat the inside of the socket and the top of the tube with structural epoxy, and push the body down until 24 mm of tube is inside it, with the gland on the left and turned toward the front (the side the fin's front half faces). Check from above that the fin is square to the board guides. Let it cure.

### Step 7: cell holder and cell down into the tube

![Step 7](05-build-plan/step-07.png)

**Hold point:** safety stops S1 and S2 first. Slide the cell into its holder, pass its leads up, and lower the holder on its cord through the floor hole until its legs stand on the spigot top. Leave the cord's loop and the cell's plug at the top, not yet connected.

### Step 8: controller board into the guides

![Step 8](05-build-plan/step-08.png)

Plug in the probe, temperature, electrode and LED leads and the antenna pigtail, then slide the board down both guide slots until it stands on their ends. **Hold point:** safety stops S3 and S4 before the cell's plug goes in.

### Step 9: panel into the cap

![Step 9](05-build-plan/step-09.png)

If not done in section 3.9: lead through the roof hole, sealant round the recess, panel pressed in and cured, O-ring in its groove.

### Step 10: cap onto the body

![Step 10](05-build-plan/step-10.png)

Put a fresh desiccant sachet in the cavity. Plug in the panel lead. Check the O-ring is clean and seated with no wire across the rim, set the cap on with the panel facing the equator, and fit the two M3 screws with their sealing washers, tightened evenly until snug.

### Step 11: assemble the slot tool

![Step 11](05-build-plan/step-11.png)

Handle through the cross hole with a collar each side, set screws tight. Slide the depth stop up from the point to the 485 mm mark, drop in the nut, and tighten the thumb screw.

### Step 12: cut the slot

![Step 12](05-build-plan/step-12.png)

In the trial bed, auger a 50 mm hole 110 mm deep. Stand the blade in the hole with its broad faces to the front and back, as the fin will lie. Drive it with a mallet on the struck end until the stop sits on the soil, then pull it straight out by the handle. **Hold point:** safety stop S6.

### Step 13: push the stake into the slot

![Step 13](05-build-plan/step-13.png)

Line the fin up with the slot, panel toward the equator, and push the stake down by hand on the shoulders of the head until the collar reaches the bottom of the auger hole. Never strike the head. In dry soil, pour a litre of water into the slot first. Firm the soil round the tube.

### Step 14: marker rod beside the stake

![Step 14](05-build-plan/step-14.png)

Push the rod 200 mm into the soil, 60 mm to the left of the stake's centre (on the gland side, away from the equator), flag at the top.

### Step 15: dipole on the top of the rod

![Step 15](05-build-plan/step-15.png)

Slide both clips over the rod top, then the dipole down through them until its centre is level with the rod top; fit a cable tie above and below each clip.

### Step 16: antenna lead into the gland and up the rod

![Step 16](05-build-plan/step-16.png)

The lead already runs from the board through the gland: tighten the gland's cap nut on it, leave a small drip loop below the gland, run the lead up the rod to the dipole's connector, and tie it to the rod every 200 mm with cable ties. **Hold point:** safety stop S7 before the radio transmits.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of RMS-REQ-001.

*Table 3. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Sensing depths | R1, R2, R10 | After step 13, measure from the soil surface to the head's bottom edge; the model puts it 40 mm above the soil | 40 mm, give or take 25 mm, so the windows sit at 150 and 300 mm and the temperature probe at 225 mm |
| Probe outputs | R1 | With the stake out of the ground, read each probe's frequency in air, then with the window wrapped in a wet cloth | Each frequency falls clearly when wet; the two probes read within 10 % of each other in air |
| Temperature | R2 | Stake and a reference thermometer in a bucket of water | Within 0.5 °C |
| Electrode circuit | R3 | Immerse the electrodes in a 1.41 dS/m potassium chloride standard | A steady reading that the calibration can scale; repeat readings within 2 % |
| Charge voltage | R7 | Bench supply at 5 V with a 200 mA limit in place of the panel, cell not plugged in; measure the charger output | 3.60 V, give or take 0.05 V |
| Cold and hot charge stop | R7 | Cell plugged in; replace the cell temperature sensor with a resistor equal to its value at -1 °C, then at 46 °C | No charge current in either case (under 5 mA) |
| Reports | R4, R13 | Join The Things Network and watch the gateway's console for an hour | Three uplinks an hour, decoded on the dashboard |
| Status light | | Watch the head through one uplink, then wake the stake with a magnet | One blink of about 0.1 s after the uplink, three blinks on the wake, dark otherwise |
| Head seal assembled | R8 | Look at the O-ring through the joint and at the panel bead | O-ring evenly squeezed all round; bead unbroken (the spray and immersion tests come later) |
| Push force | R10 | Bathroom scale under the trial bed, or a hand force gauge on the head | Recorded; about 390 N expected in moist loam |
| Installation time | R10 | Time steps 12 to 16 for one stake | 15 minutes or less |
| Heights | R11 | Measure the head top and the dipole centre above the soil | About 171 mm and 1,000 mm |
| Cell change | | Time removing the cap, board and cell holder and putting them back | Recorded for the TRL 4 report |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the cell comes into the workshop.** Cell voltage about 2.8 to 3.4 V; no swelling, dents or leaks; a datasheet from its maker; its fuse fitted. A charging spot ready on a non-combustible surface (ceramic tile or steel tray) with a fire extinguisher for electrical fires within reach.
- **S2. Before the cell goes into its holder.** The holder leads' polarity matches the charger's battery terminals, checked with a meter, not by wire colour; the fuse is in the lead.
- **S3. Before any charging source is connected.** The charge voltage is set and measured at 3.6 V with no cell plugged in; the panel lead's polarity is checked at the charger.
- **S4. Before the cell is allowed to charge.** Both charge-stop checks of section 5 pass with the substitute resistors; then the cell's temperature sensor is reconnected.
- **S5. First charge.** Attended the whole time, cap off, stake on the charging spot; cell temperature checked every 15 minutes. Stop if the cell passes 45 °C or 3.65 V. Never bypass the charge stop to gain energy.
- **S6. Before the slot tool is struck.** Eye protection and gloves on; the depth stop tight; feet and hands clear of the blade; nobody else within 2 m. Store the tool with a cover over its point.
- **S7. Before the radio transmits.** The 915 MHz dipole is connected, the radio is set to the US915 band plan and the gateway is the US915 version. Transmitting without an antenna can damage the radio.
- **S8. Before any field installation (outside this plan).** Check with the grower where machinery will pass; keep the flag on the rod; pull stakes before tillage; never install where buried services may run without checking first.

## 7. Tools, skills and workspace

**Tools.** 3D printer with an enclosure, a bed of at least 300 x 300 mm and settings for ASA and PETG; hacksaw with a 24 teeth per inch blade and a mitre box; bench vice; bench drill or a drill in a stand; drills 2 to 10 mm and a step drill or drills up to 20.5 mm; bench grinder or angle grinder with a flap disc; files and a deburring tool; hobby knife; abrasive paper 120 to 400 grit; soldering iron with a heat-set insert tip; flux for stainless steel; heat gun; wire strippers and crimper; multimeter; bench power supply with an adjustable current limit (0 to 15 V, 0 to 2 A); M3 hex key; spanners for the gland; a 50 mm hand auger; a 1 kg rubber or dead-blow mallet; clamps and two straight battens about 400 mm long; tape measure, steel rule and calipers; stopwatch.

**Skills.** No certified trade is needed. 3D printing with engineering plastics, two-part epoxy work, basic metalwork (sawing, drilling, grinding), through-hole soldering, and care with lithium cells and a bench power supply. All circuits are extra-low voltage: 3.6 V at most from the cell and about 6 V from the panel. The bench supply must be a certified, undamaged unit; no mains wiring is part of this build (the gateway uses its own certified USB supply).

**Workspace.** A bench about 1.2 x 0.6 m; a metalwork corner apart from the electronics so steel dust stays off the modules; a ventilated place for printing and epoxy; the charging spot of S1; a trial bed of loam at least 600 mm deep and 300 mm across, outdoors or in a large tub.

**Personal protective equipment.** Safety glasses for cutting, drilling, grinding, soldering and striking; nitrile gloves for epoxy; work gloves for bar stock and the slot tool; hearing protection when grinding; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/RMS-DWG-101` to `RMS-DWG-110`.
- General arrangement: `cad/drawings/RMS-DWG-001.pdf`, Rev P5.
- Calculations: `docs/04-calcs/01-sizing.md` (RMS-CAL-001 v0.5) and `docs/04-calcs/sizing.py`; push force [G1], [G4]; cell depth [F2], [F4]; head air [F3]; cost [H1].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (RMS-DDR-003), with RMS-DDR-001 and RMS-DDR-002.
- Requirements: `docs/03-requirements.md` (RMS-REQ-001 v0.7).
