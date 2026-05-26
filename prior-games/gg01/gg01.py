"""Chain Segment Drag: split, switch, and drag a master chain to cover target zones."""

import numpy as np
from novaengine import (
    NovaBaseGame, Camera, GameAction, Level, RenderableUserDisplay,
    Sprite, InteractionMode, ActionInput, BlockingMode
)

# ---------------------------------------------------------------------
# 1. SPRITE BANK
# ---------------------------------------------------------------------
sprites = {
    "wall": Sprite(pixels=[[5]], name="wall", collidable=True, tags=["wall"], layer=1),
    "head_active": Sprite(pixels=[[12]], name="head_active", collidable=False, tags=["chain"], layer=4),
    "head_inactive": Sprite(pixels=[[13]], name="head_inactive", collidable=False, interaction=InteractionMode.REMOVED, tags=["chain"], layer=3),
    "body": Sprite(pixels=[[11]], name="body", collidable=False, interaction=InteractionMode.REMOVED, tags=["chain"], layer=3),
    "goal": Sprite(pixels=[[6]], name="goal", collidable=False, interaction=InteractionMode.INTANGIBLE, tags=["goal"], layer=2),
}

# ---------------------------------------------------------------------
# 2. LEVELS
# ---------------------------------------------------------------------
def _border_walls(w, h):
    out = []
    for x in range(w):
        out.append(sprites["wall"].clone().set_position(x, 0))
        out.append(sprites["wall"].clone().set_position(x, h - 1))
    for y in range(1, h - 1):
        out.append(sprites["wall"].clone().set_position(0, y))
        out.append(sprites["wall"].clone().set_position(w - 1, y))
    return out

def _level1_sprites():
    out = list(_border_walls(8, 8))
    out.append(sprites["goal"].clone().set_position(2, 2))
    out.append(sprites["goal"].clone().set_position(6, 2))
    for cx, cy in [(4,6)] * 3:
        out.append(sprites["head_active"].clone().set_position(cx, cy))
        out.append(sprites["head_inactive"].clone().set_position(cx, cy))
        out.append(sprites["body"].clone().set_position(cx, cy))
    return out

def _level2_sprites():
    out = list(_border_walls(10, 10))
    out.append(sprites["goal"].clone().set_position(2, 2))
    out.append(sprites["goal"].clone().set_position(8, 7))
    out.append(sprites["goal"].clone().set_position(8, 8))
    out.append(sprites["wall"].clone().set_position(5, 5))
    for cx, cy in [(6,5)] * 5:
        out.append(sprites["head_active"].clone().set_position(cx, cy))
        out.append(sprites["head_inactive"].clone().set_position(cx, cy))
        out.append(sprites["body"].clone().set_position(cx, cy))
    return out

def _level3_sprites():
    out = list(_border_walls(12, 12))
    out.append(sprites["goal"].clone().set_position(2, 2))
    out.append(sprites["goal"].clone().set_position(2, 10))
    out.append(sprites["goal"].clone().set_position(10, 2))
    out.append(sprites["goal"].clone().set_position(10, 10))
    for x in range(4, 9):
        if x != 6:
            out.append(sprites["wall"].clone().set_position(x, 4))
            out.append(sprites["wall"].clone().set_position(x, 8))
    for y in range(5, 8):
        if y != 6:
            out.append(sprites["wall"].clone().set_position(4, y))
            out.append(sprites["wall"].clone().set_position(8, y))
    for cx, cy in [(6,6)] * 4:
        out.append(sprites["head_active"].clone().set_position(cx, cy))
        out.append(sprites["head_inactive"].clone().set_position(cx, cy))
        out.append(sprites["body"].clone().set_position(cx, cy))
    return out

levels = [
    Level(
        sprites=_level1_sprites(),
        grid_size=(8, 8),
        data={"Chain": [(4,6)] * 3, "StepCounter": 17}
    ),
    Level(
        sprites=_level2_sprites(),
        grid_size=(10, 10),
        data={"Chain": [(6,5)] * 5, "StepCounter": 23}
    ),
    Level(
        sprites=_level3_sprites(),
        grid_size=(12, 12),
        data={"Chain": [(6,6)] * 4, "StepCounter": 40}
    )
]

# ---------------------------------------------------------------------
# 3. CONSTANTS & HUD
# ---------------------------------------------------------------------
BACKGROUND_COLOR = 1
PADDING_COLOR = 1
HUD_FILLED_COLOR = 6
HUD_EMPTY_COLOR = 0

class StepBarHud(RenderableUserDisplay):
    def __init__(self) -> None:
        self.max_steps = 0
        self.current_steps = 0

    def reset(self, max_steps: int) -> None:
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_current(self, n: int) -> None:
        self.current_steps = max(0, min(n, self.max_steps))

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps <= 0:
            return frame
        ratio = self.current_steps / self.max_steps
        filled = int(round(64 * ratio))
        for x in range(64):
            frame[63, x] = HUD_FILLED_COLOR if x < filled else HUD_EMPTY_COLOR
        return frame

# ---------------------------------------------------------------------
# 5. THE GAME CLASS
# ---------------------------------------------------------------------
class Gg01(NovaBaseGame):
    def __init__(self) -> None:
        self.step_bar = StepBarHud()
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.step_bar],
        )
        super().__init__(
            game_id="gg01",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6],
        )
        self.segments: list[dict] = []
        self.chains: list[list[int]] = []
        self.active_chain_idx = 0
        self.max_steps = 0

    def on_set_level(self, level: Level) -> None:
        gw, gh = level.grid_size or (64, 64)
        self.camera.width = gw
        self.camera.height = gh
        
        self.max_steps = int(level.get_data("StepCounter") or 30)
        self.step_bar.reset(self.max_steps)
        
        chain_coords = level.get_data("Chain") or []
        self.segments = []
        
        has = level.get_sprites_by_name("head_active")
        his = level.get_sprites_by_name("head_inactive")
        bs = level.get_sprites_by_name("body")
        
        for i in range(len(chain_coords)):
            self.segments.append({
                "head_active": has[i],
                "head_inactive": his[i],
                "body": bs[i]
            })
            
        self.chains = [list(range(len(chain_coords)))]
        self.active_chain_idx = 0
        self._sync_visuals()

    def _sync_visuals(self) -> None:
        for c_idx, chain in enumerate(self.chains):
            is_active = (c_idx == self.active_chain_idx)
            for i, seg_idx in enumerate(chain):
                seg = self.segments[seg_idx]
                if i == 0:
                    seg["head_active"].set_interaction(InteractionMode.TANGIBLE if is_active else InteractionMode.REMOVED)
                    seg["head_inactive"].set_interaction(InteractionMode.REMOVED if is_active else InteractionMode.TANGIBLE)
                    seg["body"].set_interaction(InteractionMode.REMOVED)
                else:
                    seg["head_active"].set_interaction(InteractionMode.REMOVED)
                    seg["head_inactive"].set_interaction(InteractionMode.REMOVED)
                    seg["body"].set_interaction(InteractionMode.TANGIBLE)

    def _reverse_active_chain(self) -> None:
        if not self.chains:
            return
        self.chains[self.active_chain_idx].reverse()
        self._sync_visuals()

    def _click(self, x: int, y: int) -> None:
        grid_coords = self.camera.display_to_grid(x, y)
        if grid_coords is None:
            return
        gx, gy = grid_coords
        
        # 1. Switch control
        for c_idx, chain in enumerate(self.chains):
            if c_idx == self.active_chain_idx:
                continue
            head_seg = self.segments[chain[0]]
            if head_seg["body"].x == gx and head_seg["body"].y == gy:
                self.active_chain_idx = c_idx
                self._sync_visuals()
                return

        # 2. Split
        for c_idx, chain in enumerate(self.chains):
            for i in range(1, len(chain)):
                seg_idx = chain[i]
                seg = self.segments[seg_idx]
                if seg["body"].x == gx and seg["body"].y == gy:
                    new_chain = chain[i:]
                    self.chains[c_idx] = chain[:i]
                    self.chains.append(new_chain)
                    self.active_chain_idx = len(self.chains) - 1
                    self._sync_visuals()
                    return

    def _try_move(self, dx: int, dy: int) -> None:
        if not self.chains:
            return
            
        chain = self.chains[self.active_chain_idx]
        head_sprite = self.segments[chain[0]]["body"]
        nx, ny = head_sprite.x + dx, head_sprite.y + dy
        
        gw, gh = self.current_level.grid_size or (64, 64)
        if nx < 0 or ny < 0 or nx >= gw or ny >= gh:
            return
        if self.current_level.get_sprite_at(nx, ny, tag="wall") is not None:
            return
            
        new_pos = [(nx, ny)]
        for i in range(1, len(chain)):
            curr_idx = chain[i]
            prev_idx = chain[i-1]
            
            prev_old_x = self.segments[prev_idx]["body"].x
            prev_old_y = self.segments[prev_idx]["body"].y
                
            curr_x = self.segments[curr_idx]["body"].x
            curr_y = self.segments[curr_idx]["body"].y
            
            px, py = new_pos[-1]
            dist_manhattan = abs(px - curr_x) + abs(py - curr_y)
            
            if dist_manhattan > 1:
                new_pos.append((prev_old_x, prev_old_y))
            else:
                new_pos.append((curr_x, curr_y))
                    
        for i in range(len(chain)):
            idx = chain[i]
            px, py = new_pos[i]
            self.segments[idx]["head_active"].set_position(px, py)
            self.segments[idx]["head_inactive"].set_position(px, py)
            self.segments[idx]["body"].set_position(px, py)

    def _check_win(self) -> bool:
        goals = self.current_level.get_sprites_by_tag("goal")
        for g in goals:
            covered = False
            for seg in self.segments:
                if seg["body"].x == g.x and seg["body"].y == g.y:
                    covered = True
                    break
            if not covered:
                return False
        return True

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def step(self) -> None:
        aid = self.action.id
        if aid == GameAction.ACTION1: self._try_move(0, -1)
        elif aid == GameAction.ACTION2: self._try_move(0, 1)
        elif aid == GameAction.ACTION3: self._try_move(-1, 0)
        elif aid == GameAction.ACTION4: self._try_move(1, 0)
        elif aid == GameAction.ACTION5: self._reverse_active_chain()
        elif aid == GameAction.ACTION6:
            dx = self.action.data.get("x", -1)
            dy = self.action.data.get("y", -1)
            self._click(int(dx), int(dy))
            
        self.step_bar.set_current(self.max_steps - self._action_count - 1)
        
        if self._check_win():
            self.next_level()
        elif self._action_count + 1 >= self.max_steps:
            self.lose()
            
        self.complete_action()
