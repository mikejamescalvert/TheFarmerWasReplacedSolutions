import f1

"""
f2 - routines and experiments for TFWR save.

Provides a deterministic grid sweep routine that mixes in companion planting
when available. Defaults to running forever (the game script loop will also
control execution). Prints only when `debug=True`.

Public API:
- grid_sweep_with_companion_mix(companion_interval=5, debug=False, passes=None)
    companion_interval: every N tiles (based on x+y) attempt companion planting
    debug: if True, prints minimal runtime info
    passes: if None, runs forever; if an int, does that many full grid passes

Example usage:
    grid_sweep_with_companion_mix(companion_interval=4, debug=False, passes=None)

This routine uses helpers from `f1.py`: `resetPosition`, `moveToPosition`,
`handleSpotHarvestingProcess`, `getEntityForSpot`, and `plantCompanionAndReturn`.
"""


def grid_sweep_with_companion_mix(companion_interval=5, debug=False, passes=None):
    """Deterministic serpentine grid sweep with occasional companion planting.

    - companion_interval: integer; attempt companion planting when (x+y) % companion_interval == 0
    - debug: print minimal actions when True
    - passes: None (run forever) or integer number of full grid passes
    """

    # Start from the canonical origin
    f1.resetPosition()

    size = get_world_size()
    if size is None or size <= 0:
        if debug:
            print("grid_sweep: invalid world size", size)
        return

    pass_count = 0

    while True:
        if passes is not None and pass_count >= passes:
            if debug:
                print("grid_sweep: completed passes", passes)
            return

        # Sweep rows 0..size-1
        for row in range(size):
            # Serpentine order: left->right on even rows, right->left on odd rows
            if (row % 2) == 0:
                x_iter = range(0, size)
            else:
                x_iter = range(size - 1, -1, -1)

            for col in x_iter:
                # Move deterministically to the tile
                f1.moveToPosition(col, row)

                # Harvest / water / till as required by existing helper
                f1.handleSpotHarvestingProcess()

                # Decide whether to attempt companion planting here
                try:
                    companion = get_companion()
                except:
                    # If the builtin is not available for some reason, treat as no companion
                    companion = None

                if companion is not None and ((col + row) % companion_interval) == 0:
                    # Use the helper that travels to companion, plants it, and returns
                    # If the helper is not present or fails, fall back to planting the
                    # default entity for this spot.
                    try:
                        f1.plantCompanionAndReturn()
                    except:
                        plant(f1.getEntityForSpot(col, row))
                else:
                    # Default planting choice based on f1 rule
                    plant(f1.getEntityForSpot(col, row))

                # Minimal debug output only when requested
                if debug:
                    print("visited", col, row)

        pass_count += 1


def self_test():
    """Run a single-pass test with debug output to validate behavior."""
    grid_sweep_with_companion_mix(companion_interval=4, debug=True, passes=1)
    print("self_test: position", get_pos_x(), get_pos_y())


if __name__ == "__main__":
    # Running directly should execute a single test pass (safe for maintainers)
    self_test()
