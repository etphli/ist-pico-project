"""Probe the two straight insertion paths described in the assembly guide.

Run in the scripts/cad.sh uv environment with this file as the Python entry point.
This reports collisions, not an exhaustive search for a possible assembly path.
"""

from pip_robot import parts


def main():
    base = parts.base_plate()
    trials = {
        "Left motor lowered vertically into the cradle": [
            (offset, (base ^ parts.ref_tt_motor(1).translate((0, 0, offset))).volume())
            for offset in range(0, 81, 2)
        ],
        "Left wheel pressed laterally onto an installed motor": [
            (offset, (base ^ parts.drive_wheel(1).translate((0, offset, 0))).volume())
            for offset in range(0, 17)
        ],
        "Left wheel raised vertically from below before the motor is installed": [
            (offset, (base ^ parts.drive_wheel(1).translate((0, 0, -offset))).volume())
            for offset in range(0, 81, 2)
        ],
    }
    for name, values in trials.items():
        offset, peak = max(values, key=lambda pair: pair[1])
        blocked = peak > 0.1
        print(f"{'BLOCKED' if blocked else 'CLEAR AT SAMPLES'}: {name}")
        print(f"  Peak overlap {peak:.2f} mm^3 at displacement {offset} mm")
    print("Sampled placeholder geometry only. Oblique and combined paths are not evaluated.")
    print("Do not infer assembly readiness from a collision-free final placement.")


if __name__ == "__main__":
    main()
