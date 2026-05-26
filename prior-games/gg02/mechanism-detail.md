# gg02 - orc-path-tower-defense

Simplified tower defense prototype. Orcs spawn one after another at the start
of a winding, non-axis-aligned path and move one path tile toward the castle on
every action. `ACTION5` is a wait/space tick. `ACTION6` clicks either select a
tower type in the small palette or place the selected tower on any unoccupied
non-path board tile. Palette clicks and build clicks also advance the wave.

Arrow towers cost 10 coins, have range 4, and deal 1 damage to the leading orc
in range every tick. Mine towers cost 10 coins, have range 1, and deal 4 damage
to every orc in range, but only fire every second combat tick. Easy, medium,
hard, and boss orcs have 2, 4, 8, and 11 health respectively, and larger pixel
bodies communicate that health class. Boss orcs appear at the end of levels 2
and 3 with a darker red body, horns, and a wider health bar. Each killed orc
awards 1 coin.

Level 1 starts with 10 coins and only a few orcs, so one arrow tower is enough.
Level 2 gives enough starting coins for three planned towers and ends with a
boss orc. Level 3 returns to a tight 10-coin opening, then forces live building:
early kills fund a mid-wave mine and a later arrow tower before the hard cluster
and final boss reach the castle.

The board uses the full 64x64 canvas: grass texture, winding dirt path, ponds,
trees, spawn cave, bottom coin bar, build palette, and a compact castle sprite.
Tower ranges are visible in-place: arrows show dotted range rings and mines
show their tight blast cells, changing colour when on cooldown. Firing feedback
is visible as arrow beams and mine burst flashes. The implementation leaves
comments where a later visual pass can expand the forest dressing and castle
pixel art.
