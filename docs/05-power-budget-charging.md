# 05 · Power, current budget and charging

**Wiring HOLD.** The first concept's power system is not ready to build. The [engineering review](13-design-review.md) is the controlling status for this package.

## Rated supply problems

The original bank-to-Robo-Pico concept supplies nominal 5 V to VIN. The carrier's documented voltage drop produces roughly 4.6 V on its motor and servo rail. That is within the chosen TT motors' 3–6 V range, but below the FS90 servo listing's 4.8 V minimum. The same reduced rail must not be treated as a rated 5 V USB supply to the XIAO camera.

The proposed fix must provide each load with its specified voltage, under startup and motor load as well as at idle. Options include a servo explicitly rated for the available rail or a separate regulated servo branch, and a regulated camera branch. No regulator, splitter, switch or connector has yet been selected and priced. Do not wire the original servo/camera power paths or use the BOM as a complete electrical design.

Motor and servo currents must bypass Pico GPIO, Pico 3V3, PiicoDev cables and breadboard contacts. Use appropriately rated power connectors and wires, with a common ground. The no-soldering requirement includes every power connector.

Technical references: [Cytron Robo Pico datasheet](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6147/Robo_Pico.pdf), [FS90 listing](https://core-electronics.com.au/feetech-fs90-1-5kgcm-micro-servo-9g.html), [Seeed XIAO documentation](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/). Accessed 2026-10-19.

## Preliminary current budget

These numbers help choose a future supply. They are not measurements of a working robot. Values marked estimate need measurement.

| Load | Typical | Fault or peak estimate |
|---|---|---|
| Two TT motors | 0.5 A total, estimate | Up to about 3 A combined at stall, depending on voltage |
| FS90 servo | 0.1–0.25 A, estimate | About 0.8 A stall, listing |
| XIAO camera and mic | About 0.14 A in the cited webcam example | 0.3 A provisional allowance |
| Pico, carrier, speaker and sensor chain | About 0.2–0.4 A combined, estimate | Must be measured per rail |
| Whole robot | About 1.1–1.3 A equivalent at 5 V | About 4.2 A combined worst case, rough estimate |

The original 2.4 A bank requirement does not cover this fault estimate. Select a supply and documented hardware protection together. A higher-current bank alone does not protect a stalled motor. Account for motor winding limits, driver continuous and transient limits, connector ratings and faults in each branch.

PWM duty limits and ramps can reduce average demand but do not guarantee safe peak or stall current. The proposed accelerometer/range heuristic is not a current sensor. Do not rely on it for protection. Confirm the selected driver's actual current-limit and fault behaviour from its manufacturer documentation before bounded fault tests on a current-limited bench supply.

## Battery and charging design targets

A finished consumer power bank avoids building a lithium charger from loose parts. Its output rating, low-load shutdown, charge behaviour, physical dimensions and charge-port location still need verification. A 10,000 mAh label normally describes the internal cell capacity, not 10,000 mAh delivered at 5 V. The earlier 2–5 hour runtime estimate is unverified.

The alternative bare LiPo route is also blocked. The kit board is a charger and sensor adapter, not a motor driver. Battery polarity, protection, charger current and load sharing must match the actual battery. Do not assume two chargers can be connected to one cell.

Design the master disconnect to cut the motors, servo, camera, microphone and speaker. Software sleep is different from hard-off. A sleeping camera can remain electrically powered. Label the controls accordingly.

The power bank's charging state is not visible to the Pico in the proposed design. A door mechanically blocking the power switch was described but has not been modelled. Until a real interlock is designed and tested, no automatic prevention of driving while charging is claimed. Switch off and disconnect play power before charging. Follow the selected bank's own instructions.

## Exit criteria before electrical assembly

1. Select a complete solder-free power topology and add every part to the delivered BOM.
2. Check rated voltage and current for every branch, including startup and fault conditions.
3. Document the hardware protection and master-off wiring.
4. Design and verify charge isolation or an interlock.
5. Check polarity and continuity before first power, then measure rails with wheels guarded and a current-limited supply.
6. Test reset behaviour, network loss and audio load. Motor outputs must default off during a reset.
