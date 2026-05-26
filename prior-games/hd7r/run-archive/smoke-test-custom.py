"""Custom smoke checks for hd7r. Each: <=5 setup actions, 1 action under
test, 1 boolean. Run from repo root via the smoke runner."""

from novaengine import ActionInput, GameAction


def _act(g, n):
    g.perform_action(ActionInput(id=GameAction.from_id(n), data={}), raw=True)


def _click(g, x, y):
    g.perform_action(ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y}), raw=True)


def _cell(s):
    return (s.x // 4, s.y // 4)


def check_flee_straight_backs_away(GameClass):
    """A straight creature within scare radius steps directly away from the shepherd."""
    g = GameClass()
    g.set_level(0)
    creature = g.current_level.get_sprites_by_tag("straight")[0]  # L1 timid at (10,8)
    cy0 = _cell(creature)[1]
    # shepherd starts (7,11); step UP repeatedly to get level with the creature.
    _act(g, 1); _act(g, 1); _act(g, 1)  # shepherd 11->8, creature now level => flees
    cy1 = _cell(creature)[1]
    # shepherd is below/left; the creature should have moved up or right (away), never toward.
    cx1 = _cell(creature)[0]
    passed = (cx1 >= 10 and cy1 <= cy0)  # moved away (right and/or up), never closer
    return passed, f"creature start(10,{cy0}) -> ({cx1},{cy1})"


def check_outside_radius_no_move(GameClass):
    """A creature beyond the scare radius does not move when the shepherd steps far away."""
    g = GameClass()
    g.set_level(0)
    creature = g.current_level.get_sprites_by_tag("straight")[0]  # at (10,8)
    before = _cell(creature)
    # shepherd at (7,11): Manhattan to (10,8)=3+3=6 > 4. Step LEFT (away) -> still >4.
    _act(g, 3)  # shepherd -> (6,11), dist to creature = 4+3=7 > 4
    after = _cell(creature)
    passed = (after == before)
    return passed, f"creature {before} -> {after} (shepherd far)"


def check_perp_creature_sidesteps(GameClass):
    """A perp (skittish) creature veers perpendicular, not straight back."""
    g = GameClass()
    g.set_level(2)  # L3 has the skittish creature at (5,11), shepherd at (2,8)
    sk = g.current_level.get_sprites_by_tag("perp")[0]
    before = _cell(sk)  # (5,11)
    # shepherd (2,8) -> move DOWN to (2,9): dist to (5,11)=3+2=5 >4 still; DOWN again (2,10) dist=3+1=4
    _act(g, 2)  # (2,9)
    _act(g, 2)  # (2,10): now within radius; away-vector dominant x (dx=3>dy=1) -> straight would be +x (right);
    after = _cell(sk)
    # perp = CW rotation of away (ax=+1,ay=0) -> (ay,-ax)=(0,-1) => moves UP (y decreases), NOT right.
    passed = (after[1] < before[1] and after[0] == before[0])
    return passed, f"skittish {before} -> {after} (expected vertical sidestep)"


def check_closed_gate_blocks_then_opens(GameClass):
    """Clicking the gate post toggles it from closed (blocking) to open (passable)."""
    g = GameClass()
    g.set_level(1)  # L2, gate at cell (8,8) closed
    closed = [s for s in g.current_level.get_sprites_by_tag("gate") if "gate_closed" in s.tags][0]
    from novaengine import InteractionMode
    was_blocking = closed.interaction != InteractionMode.REMOVED
    _click(g, 34, 34)  # gate cell (8,8) center -> display px 34,34
    now_open = closed.interaction == InteractionMode.REMOVED
    passed = (was_blocking and now_open)
    return passed, f"closed-gate blocking={was_blocking} after-click removed={now_open}"
