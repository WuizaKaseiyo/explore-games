# gg16 — wavefront-ring-expand

`ACTION6` clicks an empty cell to move the emitter and start a new wave.
`ACTION5` advances all active waves by one Chebyshev radius. Switches touched
by the current ring toggle state. Later levels add echo lenses: when a wave
ring touches an unused echo lens, that lens emits its own one-step wave on the
next tick.

Level 1 teaches a single central wave. Level 2 adds walls and a short reach
limit, so echo lenses are needed to reach switches around corners. Level 3
adds one-shot switches: they toggle on their first hit and ignore later hits,
forcing careful emit positions and timing around the echo lenses.

The bottom energy bar tracks the remaining emit/tick budget. Win when every
switch matches its target state.
