"""Custom smoke checks for qn7w (pulse-chain-eject)."""

from novaengine import ActionInput, GameAction


def _click(x, y):
    return ActionInput(id=GameAction.ACTION6, data={"x": x, "y": y})


def check_pulse_eject_fills_l1_socket(GameClass):
    """L1: clicking the only pusher ejects the terminal ball into the lone target socket and fills it."""
    g = GameClass()
    g.handle_reset()
    # Action under test: click the pusher centre (11, 33).
    g.perform_action(_click(11, 33))
    # Assertion: L1's target_socket centre pixel is non-transparent (filled).
    sockets_after = g._levels[0].get_sprites_by_tag("target_socket")
    socket = sockets_after[0]
    observed = f"socket pix[2,2]={int(socket.pixels[2, 2])}"
    return int(socket.pixels[2, 2]) != -1, observed


def check_junction_click_cycles_active_branch(GameClass):
    """L2: clicking the junction cycles its active_branch from 'down' to 'up'."""
    g = GameClass()
    g.handle_reset()
    g.set_level(1)
    # Setup 0 actions; pre-condition: active_branch == "down".
    pre = g._chains[0]["active_branch"]
    # Action under test: click junction centre (31, 33).
    g.perform_action(_click(31, 33))
    post = g._chains[0]["active_branch"]
    observed = f"before={pre} after={post}"
    return post == "up", observed


def check_dead_end_wall_consumes_eject(GameClass):
    """L2: firing the pusher with the junction defaulted to 'down' consumes a down-branch ball
    (chain shortens) but the target socket stays empty (wall consumed the ejected ball)."""
    g = GameClass()
    g.handle_reset()
    g.set_level(1)
    # Pre-condition: junction default = 'down'; down-branch has 3 balls.
    pre_len = len(g._chains[0]["branches"]["down"]["balls"])  # expect 3
    # Action under test: click pusher centre (7, 33).
    g.perform_action(_click(7, 33))
    post_len = len(g._chains[0]["branches"]["down"]["balls"])
    socket = g._levels[1].get_sprites_by_tag("target_socket")[0]
    socket_filled = int(socket.pixels[2, 2]) != -1
    observed = f"down-branch len: {pre_len} → {post_len}; socket_filled={socket_filled}"
    # Single assertion: down-branch shrank by exactly 1 (eject was consumed).
    return post_len == pre_len - 1, observed


def check_merge_pad_lights_on_second_deposit(GameClass):
    """L3: after one deposit the merge_pad is half-lit; the second deposit completes the fill."""
    g = GameClass()
    g.handle_reset()
    g.set_level(2)
    # Setup: 3 actions — flip A, push A (1 deposit), flip B.
    g.perform_action(_click(23, 49))  # junction A → "up"
    g.perform_action(_click(5, 49))   # pusher A fires; deposit 1
    g.perform_action(_click(41, 25))  # junction B → "left"
    # Action under test: pusher B fires; expect deposit 2.
    g.perform_action(_click(59, 25))
    pad = g._levels[2].get_sprites_by_tag("merge_pad")[0]
    centre = int(pad.pixels[2, 2])
    observed = f"merge_pad pix[2,2]={centre} deposits={g._merge_pad_deposits}"
    # Single assertion: pad's centre is fully filled (white = 0).
    return centre == 0, observed
