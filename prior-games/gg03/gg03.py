"""Chimera-Merge-Split: pawns merge into 2-cell chimeras to bridge gaps and navigate narrow corners."""

import numpy as np
from novaengine import (
    NovaBaseGame, Camera, GameAction, Level,
    Sprite, ActionInput, RenderableUserDisplay
)

FLOOR_COLOR = 11
WALL_COLOR = 0
GAP_COLOR = 10
ACTIVE_COLOR = 8 # Teal
TARGET_MARK = 14
WALL_EDGE = 5
GRID_W = 12
GRID_H = 12
CELL = 5
ORIGIN_X = 2
ORIGIN_Y = 3
CAM_SIZE = 64

class PawnState:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class ChimeraState:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

class TargetAndActiveHUD(RenderableUserDisplay):
    def __init__(self, game):
        self.game = game
        
    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        # Draw step bar
        if self.game.max_steps > 0:
            ratio = self.game.current_steps / self.game.max_steps
            filled = int(round(frame.shape[1] * ratio))
            for x in range(frame.shape[1]):
                frame[0, x] = 3 if x < filled else 5
                
        return frame


class Gg03(NovaBaseGame):
    def __init__(self) -> None:
        self.hud = TargetAndActiveHUD(self)
        camera = Camera(
            background=WALL_COLOR,
            letter_box=WALL_COLOR,
            interfaces=[self.hud],
        )
        # Dummy levels to init, real init in on_set_level
        levels = [
            Level(grid_size=(CAM_SIZE, CAM_SIZE), sprites=[], data={"Level": 1}),
            Level(grid_size=(CAM_SIZE, CAM_SIZE), sprites=[], data={"Level": 2}),
            Level(grid_size=(CAM_SIZE, CAM_SIZE), sprites=[], data={"Level": 3}),
        ]
        super().__init__(
            game_id="gg03",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6],
        )
        self.pawns = []
        self.chimeras = []
        self.targets = []
        self.walls = set()
        self.gaps = set()
        self.active_entity = None
        self.max_steps = 0
        self.current_steps = 0

    def on_set_level(self, level: Level) -> None:
        self.camera.width = CAM_SIZE
        self.camera.height = CAM_SIZE
        self.current_level._grid_size = (CAM_SIZE, CAM_SIZE)
        
        lvl = level.get_data("Level")
        self.pawns = []
        self.chimeras = []
        self.targets = []
        self.walls = set()
        self.gaps = set()
        
        if lvl == 1:
            self.max_steps = 40
            self.pawns = [PawnState(1, 10, 7), PawnState(10, 10, 1)]
            self.targets = [(1, 1, 7), (10, 1, 1)]
            for x in range(GRID_W): self.gaps.add((x, 5))
            for x in range(GRID_W):
                if x not in (5, 6):
                    self.walls.add((x, 8))
                    self.walls.add((x, 3))
            self.active_entity = self.pawns[0]
            
        elif lvl == 2:
            self.max_steps = 60
            self.pawns = [PawnState(5, 10, 7), PawnState(6, 10, 1)]
            self.targets = [(10, 1, 7), (1, 1, 1)]
            for x in range(GRID_W): self.gaps.add((x, 8))
            for x in range(GRID_W):
                for y in range(2, 8):
                    self.walls.add((x, y))
            for y in (7, 6, 5, 4): self.walls.remove((5, y))
            for x in (6, 7, 8): self.walls.remove((x, 4))
            for y in (3, 2): self.walls.remove((8, y))
            for x in (7, 6, 5, 4, 3, 2): self.walls.remove((x, 2))
            self.active_entity = self.pawns[0]
            
        elif lvl == 3:
            self.max_steps = 60
            self.pawns = [PawnState(1, 10, 7), PawnState(5, 10, 1), PawnState(9, 5, 4)]
            self.targets = [(1, 6, 1), (6, 1, 7), (9, 1, 4)]
            for x in range(8): self.gaps.add((x, 8))
            for x in range(8, GRID_W): self.walls.add((x, 8))
            for x in range(GRID_W):
                if x not in (1, 2, 9): self.walls.add((x, 6))
            for x in range(4, GRID_W): self.gaps.add((x, 4))
            for x in range(4): self.walls.add((x, 4))
            self.active_entity = self.pawns[0]
            
        self.current_steps = self.max_steps
        self._sync_sprites()

    def _sync_sprites(self):
        sprites = []
        sprites.append(Sprite(pixels=[[WALL_COLOR] * CAM_SIZE for _ in range(CAM_SIZE)], name="backdrop", layer=-2).set_position(0, 0))
        # Floor
        for x in range(GRID_W):
            for y in range(GRID_H):
                if (x, y) in self.walls:
                    pixels = self._wall_pixels()
                    name = "wall"
                elif (x, y) in self.gaps:
                    pixels = self._gap_pixels()
                    name = "gap"
                else:
                    pixels = self._floor_pixels()
                    name = "floor"
                px, py = self._cell_to_pixel(x, y)
                sprites.append(Sprite(pixels=pixels, name=name, layer=0).set_position(px, py))

        # Targets
        for tx, ty, c in self.targets:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                rx, ry = tx + dx, ty + dy
                if 0 <= rx < GRID_W and 0 <= ry < GRID_H and (rx, ry) not in self.walls:
                    px, py = self._cell_to_pixel(rx, ry)
                    sprites.append(Sprite(pixels=self._target_mark_pixels(), name=f"target_ring_{c}", layer=1).set_position(px, py))
            px, py = self._cell_to_pixel(tx, ty)
            sprites.append(Sprite(pixels=self._pawn_pixels(c), name=f"target_{c}", layer=1).set_position(px, py))
                    
        # Pawns & Chimeras
        for p in self.pawns:
            px, py = self._cell_to_pixel(p.x, p.y)
            sprites.append(Sprite(pixels=self._pawn_pixels(p.color), name=f"pawn_{p.color}", layer=2).set_position(px, py))
            if p is self.active_entity:
                sprites.append(Sprite(pixels=self._active_pixels(), name="active_marker", layer=3).set_position(px, py))
            
        for c in self.chimeras:
            p1x, p1y = self._cell_to_pixel(c.p1.x, c.p1.y)
            p2x, p2y = self._cell_to_pixel(c.p2.x, c.p2.y)
            sprites.append(Sprite(pixels=self._pawn_pixels(c.p1.color), name=f"chimera_1_{c.p1.color}", layer=2).set_position(p1x, p1y))
            sprites.append(Sprite(pixels=self._pawn_pixels(c.p2.color), name=f"chimera_2_{c.p2.color}", layer=2).set_position(p2x, p2y))
            if c is self.active_entity:
                sprites.append(Sprite(pixels=self._active_pixels(), name="active_chimera_1", layer=3).set_position(p1x, p1y))
                sprites.append(Sprite(pixels=self._active_pixels(), name="active_chimera_2", layer=3).set_position(p2x, p2y))
            
        self.current_level._sprites = sprites

    def _cell_to_pixel(self, x, y):
        return ORIGIN_X + x * CELL, ORIGIN_Y + y * CELL

    def _pixel_to_cell(self, x, y):
        if not (ORIGIN_X <= x < ORIGIN_X + GRID_W * CELL and ORIGIN_Y <= y < ORIGIN_Y + GRID_H * CELL):
            return None
        return (x - ORIGIN_X) // CELL, (y - ORIGIN_Y) // CELL

    def _floor_pixels(self):
        px = [[FLOOR_COLOR] * CELL for _ in range(CELL)]
        px[2][2] = 12
        return px

    def _wall_pixels(self):
        return [
            [WALL_EDGE, WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_EDGE],
            [WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR],
            [WALL_COLOR, WALL_COLOR, WALL_EDGE, WALL_COLOR, WALL_COLOR],
            [WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_COLOR],
            [WALL_EDGE, WALL_COLOR, WALL_COLOR, WALL_COLOR, WALL_EDGE],
        ]

    def _gap_pixels(self):
        return [
            [WALL_COLOR, GAP_COLOR, GAP_COLOR, GAP_COLOR, WALL_COLOR],
            [GAP_COLOR, 1, GAP_COLOR, 1, GAP_COLOR],
            [GAP_COLOR, GAP_COLOR, 1, GAP_COLOR, GAP_COLOR],
            [GAP_COLOR, 1, GAP_COLOR, 1, GAP_COLOR],
            [WALL_COLOR, GAP_COLOR, GAP_COLOR, GAP_COLOR, WALL_COLOR],
        ]

    def _target_mark_pixels(self):
        return [[TARGET_MARK if x == 2 or y == 2 else -1 for x in range(CELL)] for y in range(CELL)]

    def _pawn_pixels(self, color):
        return [
            [-1, color, color, color, -1],
            [color, color, color, color, color],
            [color, color, color, color, color],
            [color, color, color, color, color],
            [-1, color, color, color, -1],
        ]

    def _active_pixels(self):
        return [
            [ACTIVE_COLOR, ACTIVE_COLOR, ACTIVE_COLOR, ACTIVE_COLOR, ACTIVE_COLOR],
            [ACTIVE_COLOR, -1, -1, -1, ACTIVE_COLOR],
            [ACTIVE_COLOR, -1, -1, -1, ACTIVE_COLOR],
            [ACTIVE_COLOR, -1, -1, -1, ACTIVE_COLOR],
            [ACTIVE_COLOR, ACTIVE_COLOR, ACTIVE_COLOR, ACTIVE_COLOR, ACTIVE_COLOR],
        ]

    def _is_wall(self, x, y):
        if x < 0 or x >= GRID_W or y < 0 or y >= GRID_H: return True
        return (x, y) in self.walls

    def _is_gap(self, x, y):
        return (x, y) in self.gaps

    def _try_move(self, entity, dx, dy):
        if isinstance(entity, PawnState):
            nx, ny = entity.x + dx, entity.y + dy
            if self._is_wall(nx, ny): return
            if self._is_gap(nx, ny): return
            
            # Check collision with chimeras
            for c in self.chimeras:
                if (nx, ny) in ((c.p1.x, c.p1.y), (c.p2.x, c.p2.y)):
                    return # blocked
                    
            # Check auto-merge with another pawn
            for p in self.pawns:
                if p != entity and p.x == nx and p.y == ny:
                    self.pawns.remove(entity)
                    self.pawns.remove(p)
                    new_chimera = ChimeraState(entity, p)
                    self.chimeras.append(new_chimera)
                    self.active_entity = new_chimera
                    return
                    
            # Move
            entity.x, entity.y = nx, ny
            
        elif isinstance(entity, ChimeraState):
            n1x, n1y = entity.p1.x + dx, entity.p1.y + dy
            n2x, n2y = entity.p2.x + dx, entity.p2.y + dy
            
            if self._is_wall(n1x, n1y) or self._is_wall(n2x, n2y): return
            
            g1 = self._is_gap(n1x, n1y)
            g2 = self._is_gap(n2x, n2y)
            if g1 and g2: return # Both fall
            
            # Check collisions
            for p in self.pawns:
                if (p.x, p.y) in ((n1x, n1y), (n2x, n2y)):
                    return
            for c in self.chimeras:
                if c != entity:
                    if (c.p1.x, c.p1.y) in ((n1x, n1y), (n2x, n2y)) or (c.p2.x, c.p2.y) in ((n1x, n1y), (n2x, n2y)):
                        return
                        
            entity.p1.x, entity.p1.y = n1x, n1y
            entity.p2.x, entity.p2.y = n2x, n2y

    def _check_win(self) -> bool:
        # Check if all targets are covered by pawns of the same color
        # Chimeras count as their constituent pawns
        all_cells = []
        for p in self.pawns:
            all_cells.append((p.x, p.y, p.color))
        for c in self.chimeras:
            all_cells.append((c.p1.x, c.p1.y, c.p1.color))
            all_cells.append((c.p2.x, c.p2.y, c.p2.color))
            
        for tx, ty, tc in self.targets:
            if (tx, ty, tc) not in all_cells:
                return False
        return True

    def _get_hidden_state(self) -> np.ndarray:
        return np.zeros((1, 1), dtype=np.int16)

    def step(self) -> None:
        aid = self.action.id
        
        dx, dy = 0, 0
        if aid == GameAction.ACTION1: dy = -1
        elif aid == GameAction.ACTION2: dy = 1
        elif aid == GameAction.ACTION3: dx = -1
        elif aid == GameAction.ACTION4: dx = 1
        
        if dx != 0 or dy != 0:
            if self.active_entity:
                self._try_move(self.active_entity, dx, dy)
                
        elif aid == GameAction.ACTION5: # Split
            if isinstance(self.active_entity, ChimeraState):
                c = self.active_entity
                self.chimeras.remove(c)
                self.pawns.append(c.p1)
                self.pawns.append(c.p2)
                self.active_entity = c.p1
                
        elif aid == GameAction.ACTION6: # Click switch
            gx = self.action.data.get("x", -1)
            gy = self.action.data.get("y", -1)
            if hasattr(self.camera, "display_to_grid"):
                grid_coords = self.camera.display_to_grid(gx, gy)
                if grid_coords:
                    mapped = self._pixel_to_cell(*grid_coords)
                    if mapped is not None:
                        gx, gy = mapped
                    
            for p in self.pawns:
                if p.x == gx and p.y == gy:
                    self.active_entity = p
            for c in self.chimeras:
                if (c.p1.x == gx and c.p1.y == gy) or (c.p2.x == gx and c.p2.y == gy):
                    self.active_entity = c
                    
        self.current_steps = self.max_steps - self._action_count - 1
        self._sync_sprites()
        
        if self._check_win():
            self.next_level()
        elif self.current_steps <= 0:
            self.lose()
            
        self.complete_action()
