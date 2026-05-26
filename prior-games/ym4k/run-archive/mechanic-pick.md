# Mechanic Pick

- `game_id`: `ym4k`
- `mechanic_family`: `counterweight-latch-bridge`
- `seed`: `(autonomous)`

Chosen rule: the avatar walks a scaffold, climbs ladders, and rides a coupled pair of platforms with `ACTION5`; early levels teach the counterweight swap, then a latch freezes the left platform high so the right platform can be reused independently, and the final level turns the restored right platform into a bridge-deployment trigger.

Closest prior comparisons:
- `kx14` also uses vertical state changes, but that game is about water level and buoyancy rather than riding a coupled elevator pair.
- `wt39` is path-planning over motion constraints, but motion there is forced sliding, not local lift actuation from under the avatar.
- `rk7x` sequences a route by toggling infrastructure, but the moving object there is an autonomous courier, not a player-ridden transport surface.

