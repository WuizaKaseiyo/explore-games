import numpy as np
from novaengine import (
    ActionInput,
    NovaBaseGame,
    Camera,
    GameAction,
    Level,
    RenderableUserDisplay,
    Sprite,
)

sprites = {
    "aidclcbjcv": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="aidclcbjcv",
        visible=True,
        collidable=True,
    ),
    "byigobxzpg": Sprite(
        pixels=[
            [12, 12, 12, 12],
            [12, 12, 12, 12],
            [12, 12, 12, 12],
            [12, 12, 12, 12],
        ],
        name="byigobxzpg",
        visible=True,
        collidable=True,
        tags=["kdweefinfi"],
        layer=1,
    ),
    "cwefnfvjhr": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="cwefnfvjhr",
        visible=True,
        collidable=True,
    ),
    "doijajrgdi": Sprite(
        pixels=[
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
        ],
        name="doijajrgdi",
        visible=True,
        collidable=False,
        tags=["fsjjayjoeg"],
    ),
    "geffskzhqq": Sprite(
        pixels=[
            [2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2],
        ],
        name="geffskzhqq",
        visible=True,
        collidable=False,
        tags=["zqxwgacnue"],
    ),
    "ghklglzjuf": Sprite(
        pixels=[
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
        ],
        name="ghklglzjuf",
        visible=True,
        collidable=False,
        tags=["fsjjayjoeg"],
    ),
    "jigtxgzhwt": Sprite(
        pixels=[
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        ],
        name="jigtxgzhwt",
        visible=True,
        collidable=False,
        tags=["fsjjayjoeg"],
    ),
    "jqzhxgbmtz": Sprite(
        pixels=[
            [15, 15, 15, 15],
            [15, 15, 15, 15],
            [15, 15, 15, 15],
            [15, 15, 15, 15],
        ],
        name="jqzhxgbmtz",
        visible=True,
        collidable=True,
        tags=["ysysltqlke"],
        layer=1,
    ),
    "ktghqrydvd": Sprite(
        pixels=[
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
        ],
        name="ktghqrydvd",
        visible=True,
        collidable=False,
        tags=["fsjjayjoeg"],
    ),
    "ofwegeqknn": Sprite(
        pixels=[
            [9, 9, 9, 9],
            [9, 2, 2, 9],
            [9, 2, 2, 9],
            [9, 2, 2, 9],
            [9, 2, 2, 9],
            [9, 2, 2, 9],
            [9, 2, 2, 9],
            [9, 9, 9, 9],
        ],
        name="ofwegeqknn",
        visible=True,
        collidable=False,
        tags=["fsjjayjoeg"],
    ),
    "ooaamfpvqr": Sprite(
        pixels=[
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
        ],
        name="ooaamfpvqr",
        visible=True,
        collidable=False,
        tags=["zqxwgacnue"],
    ),
    "peimznrlqd": Sprite(
        pixels=[
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        ],
        name="peimznrlqd",
        visible=True,
        collidable=False,
        tags=["fsjjayjoeg"],
    ),
    "pktgsotzmw": Sprite(
        pixels=[
            [4, 4, 4, 4],
            [4, 9, 9, 4],
            [4, 9, 9, 4],
            [4, 4, 4, 4],
        ],
        name="pktgsotzmw",
        visible=True,
        collidable=True,
        tags=["geezpjgiyd"],
        layer=1,
    ),
    "pmargquscu": Sprite(
        pixels=[
            [2, -2, 2, 2],
            [-2, 2, 2, 2],
            [2, 2, 2, -2],
            [2, 2, -2, 2],
        ],
        name="pmargquscu",
        visible=True,
        collidable=False,
        tags=["bnzklblgdk"],
    ),
    "uasmnkbzmm": Sprite(
        pixels=[
            [5, 5, 5, 5],
            [5, 5, 5, 5],
            [5, 5, 5, 5],
            [5, 5, 5, 5],
        ],
        name="uasmnkbzmm",
        visible=True,
        collidable=True,
        tags=["debyzcmtnr"],
    ),
    "vikkhnsrzd": Sprite(
        pixels=[
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        ],
        name="vikkhnsrzd",
        visible=True,
        collidable=False,
        tags=["fsjjayjoeg"],
    ),
    "wkmuwhjqyo": Sprite(
        pixels=[
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 2, 2, 2, 2, 2, 2, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
        ],
        name="wkmuwhjqyo",
        visible=True,
        collidable=False,
        tags=["fsjjayjoeg"],
    ),
    "wppuejnwhl": Sprite(
        pixels=[
            [0, 0, 0, 0],
            [14, 14, 14, 14],
            [14, 14, 14, 14],
            [14, 14, 14, 14],
        ],
        name="wppuejnwhl",
        visible=True,
        collidable=True,
        tags=["wbmdvjhthc"],
        layer=1,
    ),
    "xqaqifquaw": Sprite(
        pixels=[
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        ],
        name="xqaqifquaw",
        visible=True,
        collidable=False,
        tags=["zqxwgacnue"],
    ),
    "xxmzyqktqy": Sprite(
        pixels=[
            [9, 9, 9, 9],
            [9, 2, 2, 9],
            [9, 2, 2, 9],
            [9, 9, 9, 9],
        ],
        name="xxmzyqktqy",
        visible=True,
        collidable=False,
        tags=["fsjjayjoeg"],
    ),
}
levels = [Level(sprites=[sprites['jigtxgzhwt'].clone().set_position(28, 28), sprites['pktgsotzmw'].clone().set_position(44, 24), sprites['pktgsotzmw'].clone().set_position(16, 28), sprites['pktgsotzmw'].clone().set_position(32, 36), sprites['wppuejnwhl'].clone().set_position(32, 48)], grid_size=(64, 64), data={'StepCounter': 200}), Level(sprites=[sprites['byigobxzpg'].clone().set_position(24, 36), sprites['doijajrgdi'].clone().set_position(12, 28), sprites['pktgsotzmw'].clone().set_position(48, 32), sprites['pktgsotzmw'].clone().set_position(36, 28), sprites['pktgsotzmw'].clone().set_position(40, 20), sprites['pktgsotzmw'].clone().set_position(48, 24), sprites['pktgsotzmw'].clone().set_position(44, 40), sprites['wppuejnwhl'].clone().set_position(12, 8)], grid_size=(64, 64), data={'StepCounter': 70}), Level(sprites=[sprites['byigobxzpg'].clone().set_position(48, 12), sprites['ktghqrydvd'].clone().set_position(52, 24), sprites['pktgsotzmw'].clone().set_position(32, 32), sprites['pktgsotzmw'].clone().set_position(20, 20), sprites['pktgsotzmw'].clone().set_position(12, 44), sprites['pktgsotzmw'].clone().set_position(8, 16), sprites['pktgsotzmw'].clone().set_position(32, 12), sprites['pmargquscu'].clone().set_position(32, 0), sprites['pmargquscu'].clone().set_position(32, 4), sprites['pmargquscu'].clone().set_position(32, 8), sprites['pmargquscu'].clone().set_position(32, 12), sprites['pmargquscu'].clone().set_position(32, 16), sprites['pmargquscu'].clone().set_position(32, 20), sprites['pmargquscu'].clone().set_position(32, 24), sprites['pmargquscu'].clone().set_position(32, 28), sprites['pmargquscu'].clone().set_position(32, 32), sprites['pmargquscu'].clone().set_position(32, 36), sprites['pmargquscu'].clone().set_position(32, 40), sprites['pmargquscu'].clone().set_position(32, 44), sprites['pmargquscu'].clone().set_position(32, 48), sprites['pmargquscu'].clone().set_position(32, 52), sprites['pmargquscu'].clone().set_position(32, 56), sprites['pmargquscu'].clone().set_position(32, 60), sprites['wppuejnwhl'].clone().set_position(16, 36)], grid_size=(64, 64), data={'StepCounter': 100})]
BACKGROUND_COLOR = 1
PADDING_COLOR = 0
celomdfhbh = 4
wvrpthjfsv = 4
vlzkmytlgh = 3
hgqlwjikqr = 0
qrmfayeqpo = 5
ansrsmsvzs = 15
lajjveeqzb = 11


class etuniyewsy(RenderableUserDisplay):
    """."""

    def __init__(self, dbdarsgrbj: int):
        """."""
        self.dbdarsgrbj = dbdarsgrbj
        self.current_steps = dbdarsgrbj

    def uwwwedmhqv(self, yfgynsqzmu: int) -> None:
        """."""
        self.current_steps = max(0, min(yfgynsqzmu, self.dbdarsgrbj))

    def pfakmupgbr(self) -> bool:
        """."""
        if self.current_steps > 0:
            self.current_steps -= 1
        return self.current_steps > 0

    def ububboesmh(self) -> None:
        """."""
        self.current_steps = self.dbdarsgrbj

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        """."""
        if self.dbdarsgrbj == 0:
            return frame
        icsbqzymhf = self.current_steps / self.dbdarsgrbj
        eagwaqduxs = round(64 * icsbqzymhf)
        for x in range(64):
            if x < eagwaqduxs:
                frame[63, x] = 7
            else:
                frame[63, x] = 4
        return frame


class wjdpciselr(Camera):
    """."""

    def _raw_render(self, sprites: list[Sprite]) -> np.ndarray:
        output = np.full((self._height, self._width), self._background, dtype=np.int8)
        for sprite in sprites:
            sprite_pixels = sprite.pixels
            sprite_height, sprite_width = sprite_pixels.shape
            rel_x = sprite._x - self._x
            rel_y = sprite._y - self._y
            dest_x_start = max(0, rel_x)
            dest_x_end = min(self._width, rel_x + sprite_width)
            dest_y_start = max(0, rel_y)
            dest_y_end = min(self._height, rel_y + sprite_height)
            if dest_x_end <= dest_x_start or dest_y_end <= dest_y_start:
                continue
            sprite_x_start = max(0, -rel_x)
            sprite_x_end = sprite_width - max(0, rel_x + sprite_width - self._width)
            sprite_y_start = max(0, -rel_y)
            sprite_y_end = sprite_height - max(0, rel_y + sprite_height - self._height)
            sprite_region = sprite_pixels[sprite_y_start:sprite_y_end, sprite_x_start:sprite_x_end]
            visible_mask = sprite_region >= 0
            output[dest_y_start:dest_y_end, dest_x_start:dest_x_end][visible_mask] = sprite_region[visible_mask]
        return output


def hbipqrhvbm(rfwebuoepa: tuple[int, int], ixzwlkvsbs: tuple[int, int]) -> int:
    return abs(rfwebuoepa[0] - ixzwlkvsbs[0]) + abs(rfwebuoepa[1] - ixzwlkvsbs[1])


def mdbwmdaxuu(rfwebuoepa: tuple[int, int], ixzwlkvsbs: tuple[int, int]) -> bool:
    return hbipqrhvbm(rfwebuoepa, ixzwlkvsbs) == celomdfhbh


def vwiozbtqgi(fqdniajpfh: Sprite, sprite: Sprite) -> bool:
    if fqdniajpfh.rotation == 0:
        return fqdniajpfh.x == sprite.x and fqdniajpfh.y - celomdfhbh == sprite.y
    elif fqdniajpfh.rotation == 180:
        return fqdniajpfh.x == sprite.x and fqdniajpfh.y + celomdfhbh == sprite.y
    elif fqdniajpfh.rotation == 90:
        return fqdniajpfh.x + celomdfhbh == sprite.x and fqdniajpfh.y == sprite.y
    else:
        return fqdniajpfh.x - celomdfhbh == sprite.x and fqdniajpfh.y == sprite.y


def uxricavavq(sprite: Sprite, clhazarisu: int) -> None:
    sprite.pixels[:, 0] = clhazarisu
    sprite.pixels[:, 3] = clhazarisu
    sprite.pixels[0, :] = clhazarisu
    sprite.pixels[3, :] = clhazarisu


def pjedoipwee(dx: int, dy: int) -> int:
    if dy < 0:
        return 0
    elif dx > 0:
        return 90
    elif dy > 0:
        return 180
    return 270


def anojofkynf(v: tuple[int, int], sprite: Sprite) -> bool:
    return v[0] >= sprite.x and v[0] < sprite.x + sprite.width and (v[1] >= sprite.y) and (v[1] < sprite.y + sprite.height)


class Wa30(NovaBaseGame):
    kuncbnslnm: etuniyewsy
    nsevyuople: dict[Sprite, Sprite]
    zmqreragji: dict[Sprite, Sprite]
    pkbufziase: set[tuple[int, int]]
    wyzquhjerd: set[tuple[int, int]]
    lqctaojiby: set[tuple[int, int]]
    qthdiggudy: set[tuple[int, int]]
    lkvghqfwan: set[tuple[int, int]]
    uuorgjazmj: set[tuple[int, int]]

    def __init__(self) -> None:
        self.kuncbnslnm = etuniyewsy(0)
        sfahrdviv = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[self.kuncbnslnm],
        )
        super().__init__(
            game_id="wa30",
            levels=levels,
            camera=sfahrdviv,
            available_actions=[1, 2, 3, 4, 5],
        )

    def _get_hidden_state(self) -> np.ndarray:
        kfbkxhumcv = np.zeros((1, 1), dtype=np.int16)
        kfbkxhumcv[0] = self.kuncbnslnm.current_steps
        return kfbkxhumcv

    def on_set_level(self, level: Level) -> None:
        self.xcuqvqnmiu()
        self.nsevyuople = dict()
        self.zmqreragji = dict()
        self.pkbufziase = set()
        self.wyzquhjerd = set()
        self.lqctaojiby = set()
        self.qthdiggudy = set()
        self.lkvghqfwan = set()
        self.uuorgjazmj = set()
        xdatcqhbr = self.current_level.get_sprites()
        for wunpnzavk in xdatcqhbr:
            if wunpnzavk.is_collidable:
                self.pkbufziase.add((wunpnzavk.x, wunpnzavk.y))
        for i in range(0, 64, celomdfhbh):
            self.pkbufziase.add((-celomdfhbh, i))
            self.pkbufziase.add((64, i))
            self.pkbufziase.add((i, -celomdfhbh))
            self.pkbufziase.add((i, 64))
        qiitczxxug = self.current_level.get_sprites_by_tag("fsjjayjoeg")
        for yotccnlopr in qiitczxxug:
            for i in range(yotccnlopr.height):
                for iiffofdbmb in range(yotccnlopr.width):
                    self.wyzquhjerd.add((yotccnlopr.x + iiffofdbmb, yotccnlopr.y + i))
        djpjnippwv = self.current_level.get_sprites_by_tag("zqxwgacnue")
        for tsrsytlfgb in djpjnippwv:
            for i in range(tsrsytlfgb.height):
                for iiffofdbmb in range(tsrsytlfgb.width):
                    self.lqctaojiby.add((tsrsytlfgb.x + iiffofdbmb, tsrsytlfgb.y + i))
        gflnevqmdv = self.current_level.get_sprites_by_tag("bnzklblgdk")
        for adxrpmucwx in gflnevqmdv:
            self.qthdiggudy.add((adxrpmucwx.x, adxrpmucwx.y))
        self.vyltpasvhc()
        self.lgirylubbp()

    def vyltpasvhc(self) -> None:
        """."""
        self.lkvghqfwan = set()
        fyfxmnwzhp = self.current_level.get_sprites_by_tag("geezpjgiyd")
        for ijudbtgsll in fyfxmnwzhp:
            if ijudbtgsll not in self.zmqreragji and (not self.shbxbhnhjc((ijudbtgsll.x, ijudbtgsll.y))):
                qrcmkiozlr = [
                    (ijudbtgsll.x - celomdfhbh, ijudbtgsll.y),
                    (ijudbtgsll.x + celomdfhbh, ijudbtgsll.y),
                    (ijudbtgsll.x, ijudbtgsll.y - celomdfhbh),
                    (ijudbtgsll.x, ijudbtgsll.y + celomdfhbh),
                ]
                for v in qrcmkiozlr:
                    self.lkvghqfwan.add(v)

    def lgirylubbp(self) -> None:
        """."""
        self.uuorgjazmj = set()
        fyfxmnwzhp = self.current_level.get_sprites_by_tag("geezpjgiyd")
        for ijudbtgsll in fyfxmnwzhp:
            if not self.jrrltylxpp(ijudbtgsll) and (not self.ahzqkfjpsc((ijudbtgsll.x, ijudbtgsll.y))):
                qrcmkiozlr = [
                    (ijudbtgsll.x - celomdfhbh, ijudbtgsll.y),
                    (ijudbtgsll.x + celomdfhbh, ijudbtgsll.y),
                    (ijudbtgsll.x, ijudbtgsll.y - celomdfhbh),
                    (ijudbtgsll.x, ijudbtgsll.y + celomdfhbh),
                ]
                for v in qrcmkiozlr:
                    self.uuorgjazmj.add(v)

    def xcuqvqnmiu(self) -> None:
        """."""
        drogceccgh = self.current_level.get_data("StepCounter")
        self.kuncbnslnm.dbdarsgrbj = drogceccgh
        self.kuncbnslnm.ububboesmh()

    def wqwsvmhhzj(self, fqdniajpfh: Sprite, x: int, y: int) -> None:
        if fqdniajpfh in self.nsevyuople:
            tkrlgpoppf = self.nsevyuople[fqdniajpfh]
            if self.fuykgiiwit(fqdniajpfh, tkrlgpoppf, (x, y)):
                dx, dy = (tkrlgpoppf.x - fqdniajpfh.x, tkrlgpoppf.y - fqdniajpfh.y)
                self.pkbufziase.remove((fqdniajpfh.x, fqdniajpfh.y))
                self.pkbufziase.remove((tkrlgpoppf.x, tkrlgpoppf.y))
                fqdniajpfh.set_position(x, y)
                tkrlgpoppf.set_position(x + dx, y + dy)
                self.pkbufziase.add((fqdniajpfh.x, fqdniajpfh.y))
                self.pkbufziase.add((tkrlgpoppf.x, tkrlgpoppf.y))
                self.lgirylubbp()
        elif self.kblzhbvysd((x, y)):
            self.pkbufziase.remove((fqdniajpfh.x, fqdniajpfh.y))
            fqdniajpfh.set_position(x, y)
            self.pkbufziase.add((fqdniajpfh.x, fqdniajpfh.y))

    def qnmfimgpwc(self, fqdniajpfh: Sprite, dx: int, dy: int) -> None:
        if fqdniajpfh not in self.nsevyuople:
            rotation = pjedoipwee(dx, dy)
            fqdniajpfh.set_rotation(rotation)
        self.wqwsvmhhzj(fqdniajpfh, fqdniajpfh.x + dx, fqdniajpfh.y + dy)

    def kblzhbvysd(self, v: tuple[int, int]) -> bool:
        return v not in self.pkbufziase and v not in self.qthdiggudy

    def fuykgiiwit(self, fqdniajpfh: Sprite, tkrlgpoppf: Sprite, v: tuple[int, int]) -> bool:
        dx = tkrlgpoppf.x - fqdniajpfh.x
        dy = tkrlgpoppf.y - fqdniajpfh.y
        tsvynrmpmm = (v[0] + dx, v[1] + dy)
        vouzrxjshl = (v not in self.pkbufziase or v == (tkrlgpoppf.x, tkrlgpoppf.y)) and v not in self.qthdiggudy and (tsvynrmpmm not in self.pkbufziase or tsvynrmpmm == (fqdniajpfh.x, fqdniajpfh.y))
        return vouzrxjshl

    def shbxbhnhjc(self, v: tuple[int, int]) -> bool:
        return v in self.wyzquhjerd

    def ahzqkfjpsc(self, v: tuple[int, int]) -> bool:
        return v in self.lqctaojiby

    def czrprbohhe(self, fqdniajpfh: Sprite) -> list[tuple[int, int]] | None:
        kpiyvjksem = (fqdniajpfh.x, fqdniajpfh.y)
        qkmekaxaqf = set()
        qkmekaxaqf.add(kpiyvjksem)
        mbkpalarob = [[kpiyvjksem]]
        while mbkpalarob:
            sfivrisylh = mbkpalarob.pop(0)
            omhkabyvpg = sfivrisylh[-1]
            if omhkabyvpg in self.lkvghqfwan:
                return sfivrisylh
            qrcmkiozlr = [
                (omhkabyvpg[0] - celomdfhbh, omhkabyvpg[1]),
                (omhkabyvpg[0] + celomdfhbh, omhkabyvpg[1]),
                (omhkabyvpg[0], omhkabyvpg[1] - celomdfhbh),
                (omhkabyvpg[0], omhkabyvpg[1] + celomdfhbh),
            ]
            for yweobqdxhg in qrcmkiozlr:
                if yweobqdxhg not in qkmekaxaqf and self.kblzhbvysd(yweobqdxhg):
                    qkmekaxaqf.add(yweobqdxhg)
                    mbkpalarob.append(sfivrisylh + [yweobqdxhg])
        return None

    def cyjrduhzmz(self, fqdniajpfh: Sprite) -> list[tuple[int, int]] | None:
        kpiyvjksem = (fqdniajpfh.x, fqdniajpfh.y)
        qkmekaxaqf = set()
        qkmekaxaqf.add(kpiyvjksem)
        mbkpalarob = [[kpiyvjksem]]
        tkrlgpoppf = self.nsevyuople[fqdniajpfh]
        dx = tkrlgpoppf.x - fqdniajpfh.x
        dy = tkrlgpoppf.y - fqdniajpfh.y
        while mbkpalarob:
            sfivrisylh = mbkpalarob.pop(0)
            omhkabyvpg = sfivrisylh[-1]
            if self.shbxbhnhjc((omhkabyvpg[0] + dx, omhkabyvpg[1] + dy)):
                return sfivrisylh
            qrcmkiozlr = [
                (omhkabyvpg[0] - celomdfhbh, omhkabyvpg[1]),
                (omhkabyvpg[0] + celomdfhbh, omhkabyvpg[1]),
                (omhkabyvpg[0], omhkabyvpg[1] - celomdfhbh),
                (omhkabyvpg[0], omhkabyvpg[1] + celomdfhbh),
            ]
            for yweobqdxhg in qrcmkiozlr:
                if yweobqdxhg not in qkmekaxaqf and self.fuykgiiwit(fqdniajpfh, tkrlgpoppf, yweobqdxhg):
                    qkmekaxaqf.add(yweobqdxhg)
                    mbkpalarob.append(sfivrisylh + [yweobqdxhg])
        return None

    def zauouvdhta(self, fqdniajpfh: Sprite) -> list[tuple[int, int]] | None:
        kpiyvjksem = (fqdniajpfh.x, fqdniajpfh.y)
        qkmekaxaqf = set()
        qkmekaxaqf.add(kpiyvjksem)
        mbkpalarob = [[kpiyvjksem]]
        while mbkpalarob:
            sfivrisylh = mbkpalarob.pop(0)
            omhkabyvpg = sfivrisylh[-1]
            if omhkabyvpg in self.uuorgjazmj:
                return sfivrisylh
            qrcmkiozlr = [
                (omhkabyvpg[0] - celomdfhbh, omhkabyvpg[1]),
                (omhkabyvpg[0] + celomdfhbh, omhkabyvpg[1]),
                (omhkabyvpg[0], omhkabyvpg[1] - celomdfhbh),
                (omhkabyvpg[0], omhkabyvpg[1] + celomdfhbh),
            ]
            for yweobqdxhg in qrcmkiozlr:
                if yweobqdxhg not in qkmekaxaqf and self.kblzhbvysd(yweobqdxhg):
                    qkmekaxaqf.add(yweobqdxhg)
                    mbkpalarob.append(sfivrisylh + [yweobqdxhg])
        return None

    def egqayvffim(self, fqdniajpfh: Sprite) -> list[tuple[int, int]] | None:
        kpiyvjksem = (fqdniajpfh.x, fqdniajpfh.y)
        qkmekaxaqf = set()
        qkmekaxaqf.add(kpiyvjksem)
        mbkpalarob = [[kpiyvjksem]]
        tkrlgpoppf = self.nsevyuople[fqdniajpfh]
        dx = tkrlgpoppf.x - fqdniajpfh.x
        dy = tkrlgpoppf.y - fqdniajpfh.y
        while mbkpalarob:
            sfivrisylh = mbkpalarob.pop(0)
            omhkabyvpg = sfivrisylh[-1]
            if self.ahzqkfjpsc((omhkabyvpg[0] + dx, omhkabyvpg[1] + dy)):
                return sfivrisylh
            qrcmkiozlr = [
                (omhkabyvpg[0] - celomdfhbh, omhkabyvpg[1]),
                (omhkabyvpg[0] + celomdfhbh, omhkabyvpg[1]),
                (omhkabyvpg[0], omhkabyvpg[1] - celomdfhbh),
                (omhkabyvpg[0], omhkabyvpg[1] + celomdfhbh),
            ]
            for yweobqdxhg in qrcmkiozlr:
                if yweobqdxhg not in qkmekaxaqf and self.fuykgiiwit(fqdniajpfh, tkrlgpoppf, yweobqdxhg):
                    qkmekaxaqf.add(yweobqdxhg)
                    mbkpalarob.append(sfivrisylh + [yweobqdxhg])
        return None

    def xpcvspllwr(self, fqdniajpfh: Sprite, sprite: Sprite) -> None:
        if sprite in self.zmqreragji:
            self.kqrtstlzkg(self.zmqreragji[sprite])
        self.nsevyuople[fqdniajpfh] = sprite
        self.zmqreragji[sprite] = fqdniajpfh
        self.vyltpasvhc()
        self.lgirylubbp()

    def kqrtstlzkg(self, fqdniajpfh: Sprite) -> None:
        if fqdniajpfh in self.nsevyuople:
            sprite = self.nsevyuople[fqdniajpfh]
            del self.zmqreragji[sprite]
            del self.nsevyuople[fqdniajpfh]
            self.vyltpasvhc()
            self.lgirylubbp()

    def zzppkjnqgk(self) -> None:
        xfkkaooadb = self.current_level.get_sprites_by_tag("wbmdvjhthc")
        fyfxmnwzhp = self.current_level.get_sprites_by_tag("geezpjgiyd")
        for ijudbtgsll in fyfxmnwzhp:
            if ijudbtgsll in self.zmqreragji:
                fqdniajpfh = self.zmqreragji[ijudbtgsll]
                if fqdniajpfh in xfkkaooadb:
                    uxricavavq(ijudbtgsll, hgqlwjikqr)
                elif any([vwiozbtqgi(olxydpaqfn, ijudbtgsll) for olxydpaqfn in xfkkaooadb]):
                    uxricavavq(ijudbtgsll, vlzkmytlgh)
                else:
                    uxricavavq(ijudbtgsll, qrmfayeqpo)
            elif any([vwiozbtqgi(olxydpaqfn, ijudbtgsll) for olxydpaqfn in xfkkaooadb]):
                uxricavavq(ijudbtgsll, vlzkmytlgh)
            else:
                uxricavavq(ijudbtgsll, wvrpthjfsv)
        zyjsukrrpd = self.current_level.get_sprites_by_tag("ysysltqlke")
        for kkkwtxdnov in zyjsukrrpd:
            if any([vwiozbtqgi(olxydpaqfn, kkkwtxdnov) for olxydpaqfn in xfkkaooadb]):
                uxricavavq(kkkwtxdnov, lajjveeqzb)
            else:
                uxricavavq(kkkwtxdnov, ansrsmsvzs)

    def ynmgxjqkgh(self) -> None:
        makxrwhhlc = self.current_level.get_sprites_by_tag("kdweefinfi")
        for dhptvmzfpx in makxrwhhlc:
            if dhptvmzfpx in self.nsevyuople:
                tkrlgpoppf = self.nsevyuople[dhptvmzfpx]
                if self.shbxbhnhjc((tkrlgpoppf.x, tkrlgpoppf.y)):
                    self.kqrtstlzkg(dhptvmzfpx)
                else:
                    sfivrisylh = self.cyjrduhzmz(dhptvmzfpx)
                    if sfivrisylh and len(sfivrisylh) > 1:
                        czvpytgvaw = sfivrisylh[1]
                        self.wqwsvmhhzj(dhptvmzfpx, czvpytgvaw[0], czvpytgvaw[1])
            else:
                fyfxmnwzhp = self.current_level.get_sprites_by_tag("geezpjgiyd")
                for ijudbtgsll in fyfxmnwzhp:
                    if mdbwmdaxuu((dhptvmzfpx.x, dhptvmzfpx.y), (ijudbtgsll.x, ijudbtgsll.y)) and ijudbtgsll not in self.zmqreragji and (not self.shbxbhnhjc((ijudbtgsll.x, ijudbtgsll.y))):
                        self.xpcvspllwr(dhptvmzfpx, ijudbtgsll)
                        return
                sfivrisylh = self.czrprbohhe(dhptvmzfpx)
                if sfivrisylh:
                    czvpytgvaw = sfivrisylh[1]
                    self.wqwsvmhhzj(dhptvmzfpx, czvpytgvaw[0], czvpytgvaw[1])

    def jrrltylxpp(self, sprite: Sprite) -> bool:
        if sprite in self.zmqreragji:
            fqdniajpfh = self.zmqreragji[sprite]
            return "ysysltqlke" in fqdniajpfh.tags
        return False

    def aoeyzovteg(self) -> None:
        zyjsukrrpd = self.current_level.get_sprites_by_tag("ysysltqlke")
        for kkkwtxdnov in zyjsukrrpd:
            if kkkwtxdnov in self.nsevyuople:
                tkrlgpoppf = self.nsevyuople[kkkwtxdnov]
                if self.ahzqkfjpsc((tkrlgpoppf.x, tkrlgpoppf.y)):
                    self.kqrtstlzkg(kkkwtxdnov)
                else:
                    sfivrisylh = self.egqayvffim(kkkwtxdnov)
                    if sfivrisylh and len(sfivrisylh) > 1:
                        czvpytgvaw = sfivrisylh[1]
                        self.wqwsvmhhzj(kkkwtxdnov, czvpytgvaw[0], czvpytgvaw[1])
            else:
                fyfxmnwzhp = self.current_level.get_sprites_by_tag("geezpjgiyd")
                for ijudbtgsll in fyfxmnwzhp:
                    if mdbwmdaxuu((kkkwtxdnov.x, kkkwtxdnov.y), (ijudbtgsll.x, ijudbtgsll.y)) and (not self.jrrltylxpp(ijudbtgsll)) and (not self.ahzqkfjpsc((ijudbtgsll.x, ijudbtgsll.y))):
                        self.xpcvspllwr(kkkwtxdnov, ijudbtgsll)
                        return
                sfivrisylh = self.zauouvdhta(kkkwtxdnov)
                if sfivrisylh:
                    czvpytgvaw = sfivrisylh[1]
                    self.wqwsvmhhzj(kkkwtxdnov, czvpytgvaw[0], czvpytgvaw[1])

    def ymzfopzgbq(self) -> bool:
        fyfxmnwzhp = self.current_level.get_sprites_by_tag("geezpjgiyd")
        return all([self.shbxbhnhjc((ijudbtgsll.x, ijudbtgsll.y)) and ijudbtgsll not in self.zmqreragji for ijudbtgsll in fyfxmnwzhp])

    def dhrikuybfo(self) -> None:
        self.ynmgxjqkgh()
        self.aoeyzovteg()
        self.zzppkjnqgk()

    def yygfcvqoyx(self, action: ActionInput) -> None:
        olxydpaqfn = self.current_level.get_sprites_by_tag("wbmdvjhthc")[0]
        if action.id == GameAction.ACTION1:
            self.kuncbnslnm.pfakmupgbr()
            dx = 0
            dy = -celomdfhbh
            self.qnmfimgpwc(olxydpaqfn, dx, dy)
            self.dhrikuybfo()
        elif action.id == GameAction.ACTION2:
            self.kuncbnslnm.pfakmupgbr()
            dx = 0
            dy = celomdfhbh
            self.qnmfimgpwc(olxydpaqfn, dx, dy)
            self.dhrikuybfo()
        elif action.id == GameAction.ACTION3:
            self.kuncbnslnm.pfakmupgbr()
            dx = -celomdfhbh
            dy = 0
            self.qnmfimgpwc(olxydpaqfn, dx, dy)
            self.dhrikuybfo()
        elif action.id == GameAction.ACTION4:
            self.kuncbnslnm.pfakmupgbr()
            dx = celomdfhbh
            dy = 0
            self.qnmfimgpwc(olxydpaqfn, dx, dy)
            self.dhrikuybfo()
        elif action.id == GameAction.ACTION5:
            self.kuncbnslnm.pfakmupgbr()
            if olxydpaqfn in self.nsevyuople:
                self.kqrtstlzkg(olxydpaqfn)
            else:
                fyfxmnwzhp = self.current_level.get_sprites_by_tag("geezpjgiyd")
                for ijudbtgsll in fyfxmnwzhp:
                    if vwiozbtqgi(olxydpaqfn, ijudbtgsll):
                        self.xpcvspllwr(olxydpaqfn, ijudbtgsll)
                        break
                zyjsukrrpd = self.current_level.get_sprites_by_tag("ysysltqlke")
                for kkkwtxdnov in zyjsukrrpd:
                    if vwiozbtqgi(olxydpaqfn, kkkwtxdnov):
                        self.kqrtstlzkg(kkkwtxdnov)
                        self.pkbufziase.remove((kkkwtxdnov.x, kkkwtxdnov.y))
                        self.current_level.remove_sprite(kkkwtxdnov)
                        break
            self.dhrikuybfo()

    def step(self) -> None:
        self.yygfcvqoyx(self.action)
        if self.ymzfopzgbq():
            self.next_level()
        elif not self.kuncbnslnm.current_steps:
            self.lose()
        self.complete_action()
