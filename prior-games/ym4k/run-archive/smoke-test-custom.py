from novaengine import ActionInput, GameAction
from ym4k import Ym4k


def run_actions(game, actions):
    for action_id in actions:
        game.perform_action(ActionInput(id=GameAction.from_id(action_id)), raw=True)


def check_l1_first_lift():
    g = Ym4k()
    run_actions(g, [4, 4, 1, 1, 4, 5])
    return g._current_level_index == 0 and g._avatar_cell() == (5, 7)


def check_l2_latch_restores_right():
    g = Ym4k()
    g.set_level(1)
    run_actions(g, [4, 4, 1, 1, 4, 5, 4])
    latched = g.left_platform_latched
    run_actions(g, [4, 4, 2, 2, 2, 4, 5])
    return latched and g.right_platform_high and g._avatar_cell() == (9, 7)


def check_l2_witness_wins():
    g = Ym4k()
    g.set_level(1)
    run_actions(g, [4, 4, 1, 1, 4, 5, 4, 4, 4, 2, 2, 2, 4, 5, 4, 4, 4, 4, 4])
    return g._current_level_index == 2


def check_l3_bridge_deploys():
    g = Ym4k()
    g.set_level(2)
    run_actions(g, [4, 4, 1, 1, 4, 5, 4, 4, 4, 2, 2, 2, 4, 5, 4, 4, 4])
    return g.bridge_deployed and g._avatar_cell() == (12, 7)


def check_l3_witness_wins():
    g = Ym4k()
    g.set_level(2)
    run_actions(g, [4, 4, 1, 1, 4, 5, 4, 4, 4, 2, 2, 2, 4, 5, 4, 4, 4, 4, 4, 4])
    return g.bridge_deployed and g._avatar_cell() == (15, 7)
