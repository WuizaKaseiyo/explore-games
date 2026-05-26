# gg15 — pulse-wire-relay

Click fixed wire cells to rotate their endpoints, click source pads to inject
single coloured pulses, and press `ACTION5` to clock every live pulse one wire
cell forward. Sinks light only when the required colour reaches the receiving
side, and later levels include relays that open closed gate cells only after
the correct coloured pulse reaches the relay.

- Straight wires have two orientations.
- Bend wires have four orientations.
- Cross wires are fixed and carry vertical and horizontal currents separately.
- Diode wires rotate like arrows and conduct only in the indicated direction.
- Closed gates block pulses until their matching relay has been lit.
- The action budget is exact: every rotation, launch, and clock tick in the
  intended solution is needed.

Level 1 is a single routed pulse path with two bends that must be repaired.
Level 2 routes a red pulse first so it lights a relay and opens a blue vertical
gate through the central cross. Level 3 composes three source colours: red and
green pulses must reach separate relays before the blue pulse can pass the two
closed gates on its column.

The vertical energy bar sits on the left edge for visual variety. Win when
every sink receives its required colour; lose when the action budget reaches
zero.
