import math
import random

import numpy as np
from novaengine import (
    NovaBaseGame,
    BlockingMode,
    Camera,
    GameAction,
    Level,
    RenderableUserDisplay,
    Sprite,
)

sprites = {
    "background": Sprite(
        pixels=[
            [3, 3],
        ],
        name="background",
        visible=True,
        collidable=True,
        layer=-2,
    ),
    "background2": Sprite(
        pixels=[
            [3],
            [3],
        ],
        name="background2",
        visible=True,
        collidable=True,
        layer=-2,
    ),
    "gyrdjxybtcmA": Sprite(
        pixels=[
            [10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10],
        ],
        name="gyrdjxybtcmA",
        visible=True,
        collidable=True,
        tags=["gyrdjxybtcm"],
        layer=-1,
    ),
    "gyrdjxybtcmB": Sprite(
        pixels=[
            [7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7],
        ],
        name="gyrdjxybtcmB",
        visible=True,
        collidable=True,
        tags=["gyrdjxybtcm"],
        layer=-1,
    ),
    "gyrdjxybtcmC": Sprite(
        pixels=[
            [11, 11, 11, 11, 11, 11, 11],
            [11, 11, 11, 11, 11, 11, 11],
            [11, 11, 11, 11, 11, 11, 11],
            [11, 11, 11, 11, 11, 11, 11],
            [11, 11, 11, 11, 11, 11, 11],
            [11, 11, 11, 11, 11, 11, 11],
            [11, 11, 11, 11, 11, 11, 11],
        ],
        name="gyrdjxybtcmC",
        visible=True,
        collidable=True,
        tags=["gyrdjxybtcm"],
        layer=-1,
    ),
    "iqrduxrukrk": Sprite(
        pixels=[
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        ],
        name="iqrduxrukrk",
        visible=True,
        collidable=True,
        layer=-2,
    ),
    "jpafjzbfwiqA1": Sprite(
        pixels=[
            [8],
        ],
        name="jpafjzbfwiqA1",
        visible=True,
        collidable=True,
        tags=["tjaqvwdgkxe"],
        layer=1,
    ),
    "jpafjzbfwiqA2": Sprite(
        pixels=[
            [12],
        ],
        name="jpafjzbfwiqA2",
        visible=True,
        collidable=True,
        tags=["tjaqvwdgkxe"],
        layer=1,
    ),
    "jpafjzbfwiqB1": Sprite(
        pixels=[
            [9],
        ],
        name="jpafjzbfwiqB1",
        visible=True,
        collidable=True,
        tags=["tjaqvwdgkxe"],
        layer=1,
    ),
    "jpafjzbfwiqB2": Sprite(
        pixels=[
            [14],
        ],
        name="jpafjzbfwiqB2",
        visible=True,
        collidable=True,
        tags=["tjaqvwdgkxe"],
        layer=1,
    ),
    "nxkictbbvztA1": Sprite(
        pixels=[
            [-1, -1, 5, -1, -1],
            [-1, -1, 5, -1, -1],
            [-1, 5, 5, 5, -1],
            [-1, -1, 5, -1, -1],
            [5, 5, 5, 5, 5],
        ],
        name="nxkictbbvztA1",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztA2": Sprite(
        pixels=[
            [-1, -1, -1, -1, 5],
            [-1, -1, 5, -1, 5],
            [5, 5, 5, 5, 5],
            [5, -1, 5, -1, -1],
            [5, -1, -1, -1, -1],
        ],
        name="nxkictbbvztA2",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztA3": Sprite(
        pixels=[
            [5, 5, 5, 5, 5],
            [5, -1, 5, -1, -1],
            [5, -1, -1, -1, -1],
            [5, -1, 5, -1, -1],
            [5, 5, 5, 5, 5],
        ],
        name="nxkictbbvztA3",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztA4": Sprite(
        pixels=[
            [-1, -1, 5, -1, -1],
            [5, 5, 5, 5, 5],
            [5, -1, 5, -1, 5],
            [5, -1, 5, -1, 5],
            [-1, -1, 5, -1, -1],
        ],
        name="nxkictbbvztA4",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztA5": Sprite(
        pixels=[
            [5, -1, -1, -1, 5],
            [5, 5, 5, 5, 5],
            [-1, -1, 5, -1, -1],
            [5, 5, 5, 5, 5],
            [5, -1, -1, -1, 5],
        ],
        name="nxkictbbvztA5",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztA6": Sprite(
        pixels=[
            [5, 5, 5, 5, 5],
            [-1, -1, 5, -1, -1],
            [5, 5, 5, -1, -1],
            [5, -1, -1, -1, -1],
            [5, 5, 5, 5, 5],
        ],
        name="nxkictbbvztA6",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztA7": Sprite(
        pixels=[
            [5, -1, -1, -1, 5],
            [5, 5, 5, 5, 5],
            [5, -1, -1, -1, 5],
            [5, -1, -1, -1, 5],
            [5, 5, -1, 5, 5],
        ],
        name="nxkictbbvztA7",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztB1": Sprite(
        pixels=[
            [5, -1, -1, -1, -1],
            [5, 5, 5, 5, -1],
            [5, -1, -1, 5, -1],
            [5, -1, -1, 5, -1],
            [5, 5, 5, 5, 5],
        ],
        name="nxkictbbvztB1",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztB2": Sprite(
        pixels=[
            [5, 5, 5, 5, 5],
            [5, -1, -1, -1, 5],
            [5, 5, 5, -1, 5],
            [5, -1, 5, -1, 5],
            [5, 5, 5, 5, 5],
        ],
        name="nxkictbbvztB2",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztB3": Sprite(
        pixels=[
            [-1, -1, 5, 5, 5],
            [-1, -1, 5, -1, 5],
            [5, 5, 5, 5, 5],
            [5, -1, 5, -1, -1],
            [5, 5, 5, -1, -1],
        ],
        name="nxkictbbvztB3",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztB4": Sprite(
        pixels=[
            [-1, 5, 5, 5, -1],
            [-1, 5, -1, 5, -1],
            [5, 5, 5, 5, 5],
            [5, -1, -1, -1, 5],
            [5, 5, 5, 5, 5],
        ],
        name="nxkictbbvztB4",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztB5": Sprite(
        pixels=[
            [5, 5, 5, 5, 5],
            [5, -1, -1, -1, 5],
            [5, -1, -1, -1, 5],
            [5, 5, 5, 5, 5],
            [-1, -1, 5, -1, -1],
        ],
        name="nxkictbbvztB5",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztB6": Sprite(
        pixels=[
            [5, 5, 5, 5, -1],
            [5, -1, -1, 5, 5],
            [5, -1, -1, -1, 5],
            [5, 5, -1, -1, 5],
            [-1, 5, 5, 5, 5],
        ],
        name="nxkictbbvztB6",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztB7": Sprite(
        pixels=[
            [-1, -1, 5, -1, -1],
            [5, 5, 5, 5, 5],
            [5, -1, 5, -1, 5],
            [5, 5, 5, 5, 5],
            [-1, -1, 5, -1, -1],
        ],
        name="nxkictbbvztB7",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztC1": Sprite(
        pixels=[
            [5, -1, 5, -1, 5],
            [5, -1, -1, -1, -1],
            [5, -1, 5, -1, 5],
            [5, -1, -1, -1, -1],
            [5, 5, 5, 5, 5],
        ],
        name="nxkictbbvztC1",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztC2": Sprite(
        pixels=[
            [5, 5, 5, -1, 5],
            [5, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, 5],
            [5, -1, 5, 5, 5],
        ],
        name="nxkictbbvztC2",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztC3": Sprite(
        pixels=[
            [5, -1, 5, 5, 5],
            [-1, -1, 5, -1, -1],
            [-1, -1, 5, -1, -1],
            [-1, -1, 5, -1, -1],
            [5, 5, 5, -1, 5],
        ],
        name="nxkictbbvztC3",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztC4": Sprite(
        pixels=[
            [-1, -1, 5, -1, -1],
            [5, -1, 5, -1, 5],
            [-1, -1, 5, -1, -1],
            [5, -1, 5, -1, 5],
            [-1, -1, 5, -1, -1],
        ],
        name="nxkictbbvztC4",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztC5": Sprite(
        pixels=[
            [5, 5, -1, 5, 5],
            [5, -1, -1, -1, 5],
            [5, -1, 5, -1, 5],
            [5, -1, -1, -1, 5],
            [5, 5, -1, 5, 5],
        ],
        name="nxkictbbvztC5",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztC6": Sprite(
        pixels=[
            [5, -1, 5, 5, 5],
            [5, -1, 5, -1, 5],
            [5, 5, 5, -1, 5],
            [-1, -1, -1, -1, -1],
            [5, -1, 5, -1, 5],
        ],
        name="nxkictbbvztC6",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztC7": Sprite(
        pixels=[
            [5, -1, -1, -1, 5],
            [-1, -1, -1, -1, -1],
            [5, -1, -1, -1, 5],
            [5, 5, -1, 5, 5],
            [-1, 5, -1, 5, -1],
        ],
        name="nxkictbbvztC7",
        visible=True,
        collidable=True,
        tags=["nxkictbbvzt"],
    ),
    "nxkictbbvztedxeenecwqa": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        name="nxkictbbvztedxeenecwqa",
        visible=True,
        collidable=True,
        layer=-2,
    ),
    "qvtymdcqear1": Sprite(
        pixels=[
            [0, 0, 0, 0, 0],
            [0, -1, -1, -1, 0],
        ],
        name="qvtymdcqear1",
        visible=True,
        collidable=True,
    ),
    "qvtymdcqear2": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0],
        ],
        name="qvtymdcqear2",
        visible=True,
        collidable=True,
    ),
    "qvtymdcqear3": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0],
        ],
        name="qvtymdcqear3",
        visible=True,
        collidable=True,
    ),
}
levels = [Level(sprites=[sprites['background'].clone().set_position(0, 34).set_scale(32), sprites['gyrdjxybtcmA'].clone().set_position(12, 4), sprites['gyrdjxybtcmA'].clone().set_position(12, 13), sprites['gyrdjxybtcmA'].clone().set_position(12, 22), sprites['gyrdjxybtcmA'].clone().set_position(35, 13), sprites['gyrdjxybtcmA'].clone().set_position(35, 4), sprites['gyrdjxybtcmA'].clone().set_position(35, 22), sprites['gyrdjxybtcmA'].clone().set_position(14, 40), sprites['gyrdjxybtcmA'].clone().set_position(21, 40), sprites['gyrdjxybtcmA'].clone().set_position(35, 40), sprites['gyrdjxybtcmA'].clone().set_position(28, 40), sprites['gyrdjxybtcmA'].clone().set_position(42, 40), sprites['gyrdjxybtcmB'].clone().set_position(22, 4), sprites['gyrdjxybtcmB'].clone().set_position(22, 13), sprites['gyrdjxybtcmB'].clone().set_position(22, 22), sprites['gyrdjxybtcmB'].clone().set_position(45, 13), sprites['gyrdjxybtcmB'].clone().set_position(45, 22), sprites['gyrdjxybtcmB'].clone().set_position(45, 4), sprites['gyrdjxybtcmB'].clone().set_position(14, 51), sprites['gyrdjxybtcmB'].clone().set_position(21, 51), sprites['gyrdjxybtcmB'].clone().set_position(28, 51), sprites['gyrdjxybtcmB'].clone().set_position(35, 51), sprites['gyrdjxybtcmB'].clone().set_position(42, 51), sprites['iqrduxrukrk'].clone().set_position(15, 7), sprites['iqrduxrukrk'].clone().set_position(15, 16), sprites['iqrduxrukrk'].clone().set_position(15, 25), sprites['iqrduxrukrk'].clone().set_position(38, 16), sprites['iqrduxrukrk'].clone().set_position(38, 7), sprites['iqrduxrukrk'].clone().set_position(38, 25), sprites['nxkictbbvztA1'].clone().set_position(13, 14), sprites['nxkictbbvztA1'].clone().set_position(43, 41), sprites['nxkictbbvztA2'].clone().set_position(13, 23), sprites['nxkictbbvztA2'].clone().set_position(22, 41), sprites['nxkictbbvztA3'].clone().set_position(13, 5), sprites['nxkictbbvztA3'].clone().set_position(29, 41), sprites['nxkictbbvztA4'].clone().set_position(36, 14), sprites['nxkictbbvztA4'].clone().set_position(15, 41), sprites['nxkictbbvztA5'].clone().set_position(36, 5), sprites['nxkictbbvztA5'].clone().set_position(36, 41), sprites['nxkictbbvztA7'].clone().set_position(36, 23), sprites['nxkictbbvztB1'].clone().set_position(23, 14), sprites['nxkictbbvztB2'].clone().set_position(23, 23), sprites['nxkictbbvztB3'].clone().set_position(46, 14), sprites['nxkictbbvztB5'].clone().set_position(46, 5), sprites['nxkictbbvztB6'].clone().set_position(23, 5), sprites['nxkictbbvztB6'].clone().set_position(15, 52), sprites['nxkictbbvztB6'].clone().set_position(22, 52), sprites['nxkictbbvztB6'].clone().set_position(29, 52), sprites['nxkictbbvztB6'].clone().set_position(36, 52), sprites['nxkictbbvztB6'].clone().set_position(43, 52), sprites['nxkictbbvztB7'].clone().set_position(46, 23)], grid_size=(64, 64)), Level(sprites=[sprites['background'].clone().set_position(0, 34).set_scale(32), sprites['gyrdjxybtcmB'].clone().set_position(5, 13), sprites['gyrdjxybtcmB'].clone().set_position(5, 4), sprites['gyrdjxybtcmB'].clone().set_position(5, 22), sprites['gyrdjxybtcmB'].clone().set_position(42, 22), sprites['gyrdjxybtcmB'].clone().set_position(28, 4), sprites['gyrdjxybtcmB'].clone().set_position(35, 13), sprites['gyrdjxybtcmB'].clone().set_position(18, 40), sprites['gyrdjxybtcmB'].clone().set_position(25, 40), sprites['gyrdjxybtcmB'].clone().set_position(32, 40), sprites['gyrdjxybtcmB'].clone().set_position(39, 40), sprites['gyrdjxybtcmC'].clone().set_position(15, 13), sprites['gyrdjxybtcmC'].clone().set_position(22, 13), sprites['gyrdjxybtcmC'].clone().set_position(15, 4), sprites['gyrdjxybtcmC'].clone().set_position(15, 22), sprites['gyrdjxybtcmC'].clone().set_position(22, 22), sprites['gyrdjxybtcmC'].clone().set_position(29, 22), sprites['gyrdjxybtcmC'].clone().set_position(7, 51), sprites['gyrdjxybtcmC'].clone().set_position(52, 22), sprites['gyrdjxybtcmC'].clone().set_position(38, 4), sprites['gyrdjxybtcmC'].clone().set_position(45, 4), sprites['gyrdjxybtcmC'].clone().set_position(52, 4), sprites['gyrdjxybtcmC'].clone().set_position(45, 13), sprites['gyrdjxybtcmC'].clone().set_position(52, 13), sprites['gyrdjxybtcmC'].clone().set_position(14, 51), sprites['gyrdjxybtcmC'].clone().set_position(28, 51), sprites['gyrdjxybtcmC'].clone().set_position(21, 51), sprites['gyrdjxybtcmC'].clone().set_position(49, 51), sprites['gyrdjxybtcmC'].clone().set_position(42, 51), sprites['gyrdjxybtcmC'].clone().set_position(35, 51), sprites['iqrduxrukrk'].clone().set_position(8, 16), sprites['iqrduxrukrk'].clone().set_position(8, 7), sprites['iqrduxrukrk'].clone().set_position(8, 25), sprites['iqrduxrukrk'].clone().set_position(38, 16), sprites['iqrduxrukrk'].clone().set_position(31, 7), sprites['iqrduxrukrk'].clone().set_position(45, 25), sprites['nxkictbbvztB1'].clone().set_position(6, 5), sprites['nxkictbbvztB1'].clone().set_position(19, 41), sprites['nxkictbbvztB3'].clone().set_position(6, 23), sprites['nxkictbbvztB3'].clone().set_position(26, 41), sprites['nxkictbbvztB4'].clone().set_position(29, 5), sprites['nxkictbbvztB5'].clone().set_position(36, 14), sprites['nxkictbbvztB5'].clone().set_position(33, 41), sprites['nxkictbbvztB6'].clone().set_position(6, 14), sprites['nxkictbbvztB7'].clone().set_position(43, 23), sprites['nxkictbbvztB7'].clone().set_position(40, 41), sprites['nxkictbbvztC1'].clone().set_position(16, 23), sprites['nxkictbbvztC1'].clone().set_position(30, 23), sprites['nxkictbbvztC2'].clone().set_position(23, 14), sprites['nxkictbbvztC2'].clone().set_position(46, 14), sprites['nxkictbbvztC2'].clone().set_position(53, 14), sprites['nxkictbbvztC3'].clone().set_position(16, 5), sprites['nxkictbbvztC3'].clone().set_position(46, 5), sprites['nxkictbbvztC4'].clone().set_position(16, 14), sprites['nxkictbbvztC4'].clone().set_position(39, 5), sprites['nxkictbbvztC5'].clone().set_position(23, 23), sprites['nxkictbbvztC5'].clone().set_position(8, 52), sprites['nxkictbbvztC5'].clone().set_position(15, 52), sprites['nxkictbbvztC5'].clone().set_position(29, 52), sprites['nxkictbbvztC5'].clone().set_position(22, 52), sprites['nxkictbbvztC5'].clone().set_position(50, 52), sprites['nxkictbbvztC5'].clone().set_position(43, 52), sprites['nxkictbbvztC5'].clone().set_position(36, 52), sprites['nxkictbbvztC6'].clone().set_position(53, 5), sprites['nxkictbbvztC7'].clone().set_position(53, 23)], grid_size=(64, 64)), Level(sprites=[sprites['background'].clone().set_position(0, 34).set_scale(32), sprites['gyrdjxybtcmA'].clone().set_position(7, 51), sprites['gyrdjxybtcmA'].clone().set_position(14, 51), sprites['gyrdjxybtcmA'].clone().set_position(28, 51), sprites['gyrdjxybtcmA'].clone().set_position(21, 51), sprites['gyrdjxybtcmA'].clone().set_position(42, 51), sprites['gyrdjxybtcmA'].clone().set_position(35, 51), sprites['gyrdjxybtcmA'].clone().set_position(29, 22), sprites['gyrdjxybtcmA'].clone().set_position(52, 13), sprites['gyrdjxybtcmA'].clone().set_position(45, 4), sprites['gyrdjxybtcmA'].clone().set_position(15, 4), sprites['gyrdjxybtcmA'].clone().set_position(52, 4), sprites['gyrdjxybtcmA'].clone().set_position(52, 22), sprites['gyrdjxybtcmA'].clone().set_position(22, 13), sprites['gyrdjxybtcmA'].clone().set_position(15, 13), sprites['gyrdjxybtcmA'].clone().set_position(49, 51), sprites['gyrdjxybtcmC'].clone().set_position(5, 13), sprites['gyrdjxybtcmC'].clone().set_position(5, 4), sprites['gyrdjxybtcmC'].clone().set_position(5, 22), sprites['gyrdjxybtcmC'].clone().set_position(12, 22), sprites['gyrdjxybtcmC'].clone().set_position(19, 22), sprites['gyrdjxybtcmC'].clone().set_position(4, 40), sprites['gyrdjxybtcmC'].clone().set_position(42, 22), sprites['gyrdjxybtcmC'].clone().set_position(28, 4), sprites['gyrdjxybtcmC'].clone().set_position(35, 4), sprites['gyrdjxybtcmC'].clone().set_position(35, 13), sprites['gyrdjxybtcmC'].clone().set_position(42, 13), sprites['gyrdjxybtcmC'].clone().set_position(11, 40), sprites['gyrdjxybtcmC'].clone().set_position(25, 40), sprites['gyrdjxybtcmC'].clone().set_position(18, 40), sprites['gyrdjxybtcmC'].clone().set_position(53, 40), sprites['gyrdjxybtcmC'].clone().set_position(46, 40), sprites['gyrdjxybtcmC'].clone().set_position(39, 40), sprites['gyrdjxybtcmC'].clone().set_position(32, 40), sprites['iqrduxrukrk'].clone().set_position(8, 16), sprites['iqrduxrukrk'].clone().set_position(8, 7), sprites['iqrduxrukrk'].clone().set_position(22, 25), sprites['iqrduxrukrk'].clone().set_position(45, 16), sprites['iqrduxrukrk'].clone().set_position(38, 7), sprites['iqrduxrukrk'].clone().set_position(45, 25), sprites['nxkictbbvztA1'].clone().set_position(53, 5), sprites['nxkictbbvztA3'].clone().set_position(22, 52), sprites['nxkictbbvztA3'].clone().set_position(8, 52), sprites['nxkictbbvztA3'].clone().set_position(15, 52), sprites['nxkictbbvztA3'].clone().set_position(29, 52), sprites['nxkictbbvztA3'].clone().set_position(43, 52), sprites['nxkictbbvztA3'].clone().set_position(36, 52), sprites['nxkictbbvztA3'].clone().set_position(53, 14), sprites['nxkictbbvztA3'].clone().set_position(50, 52), sprites['nxkictbbvztA4'].clone().set_position(16, 5), sprites['nxkictbbvztA5'].clone().set_position(53, 23), sprites['nxkictbbvztA6'].clone().set_position(30, 23), sprites['nxkictbbvztA6'].clone().set_position(46, 5), sprites['nxkictbbvztA7'].clone().set_position(23, 14), sprites['nxkictbbvztA7'].clone().set_position(16, 14), sprites['nxkictbbvztC1'].clone().set_position(6, 23), sprites['nxkictbbvztC1'].clone().set_position(20, 23), sprites['nxkictbbvztC1'].clone().set_position(12, 41), sprites['nxkictbbvztC1'].clone().set_position(26, 41), sprites['nxkictbbvztC2'].clone().set_position(43, 23), sprites['nxkictbbvztC2'].clone().set_position(40, 41), sprites['nxkictbbvztC3'].clone().set_position(36, 5), sprites['nxkictbbvztC3'].clone().set_position(29, 5), sprites['nxkictbbvztC3'].clone().set_position(47, 41), sprites['nxkictbbvztC3'].clone().set_position(54, 41), sprites['nxkictbbvztC4'].clone().set_position(6, 14), sprites['nxkictbbvztC4'].clone().set_position(33, 41), sprites['nxkictbbvztC5'].clone().set_position(13, 23), sprites['nxkictbbvztC5'].clone().set_position(19, 41), sprites['nxkictbbvztC6'].clone().set_position(6, 5), sprites['nxkictbbvztC6'].clone().set_position(5, 41), sprites['nxkictbbvztC7'].clone().set_position(36, 14), sprites['nxkictbbvztC7'].clone().set_position(43, 14)], grid_size=(64, 64))]
BACKGROUND_COLOR = 2
PADDING_COLOR = 3
iokndxodxw = 7
kjgicbtgrt = 7
fiwynmpoeb = 1
efblfzysop = 4
rhoqllymmn = [5, 8, 14, 15, 6, 9, 12, 0]


class cjcjtddeyl(RenderableUserDisplay):
    def __init__(self, aqrjzwnzcx: "Tr87") -> None:
        self.aqrjzwnzcx = aqrjzwnzcx

    def render_interface(self, gyrdjxybtcm: np.ndarray) -> np.ndarray:
        nqbxwxgrom = gyrdjxybtcm.shape[0]
        qrrzgzkkgn = self.aqrjzwnzcx.upmkivwyrxz / self.aqrjzwnzcx.vfpimnmtnta
        ysswxajmmd = math.ceil(nqbxwxgrom * qrrzgzkkgn)
        gyrdjxybtcm[gyrdjxybtcm.shape[0] - 1, :] = efblfzysop
        gyrdjxybtcm[gyrdjxybtcm.shape[0] - 1, 0:ysswxajmmd] = fiwynmpoeb
        return gyrdjxybtcm


class Tr87(NovaBaseGame):
    def __init__(self) -> None:
        cvgwmhmdmtp = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[cjcjtddeyl(self)],
        )
        super().__init__(game_id="tr87", levels=levels, camera=cvgwmhmdmtp, available_actions=[1, 2, 3, 4])

    def on_set_level(self, level: Level) -> None:
        self._levels[self._current_level_index] = self._clean_levels[self._current_level_index].clone()
        ofysoutulp = [4, 2, 1, 2, 12, 20]
        fcnjuctdrc = random.Random(ofysoutulp[self._current_level_index])
        ndvofjlcag = self.current_level.get_sprites_by_name("background")[0].y
        self.zdwrfusvmx = self.current_level.get_sprites_by_tag("nxkictbbvzt")
        self.zdwrfusvmx.sort(key=lambda s: (s.y, s.x))
        for ekifeojqhe in self.zdwrfusvmx:
            ekifeojqhe.set_blocking(BlockingMode.BOUNDING_BOX)
            ekifeojqhe.set_rotation(fcnjuctdrc.choice([0, 90, 180, 270]))
        shjobgeklx = [s for s in self.zdwrfusvmx if s.y > ndvofjlcag]
        self.zvojhrjxxm: list[Sprite] = []
        self.ztgmtnnufb: list[Sprite] = []
        bujvmlirav = min(shjobgeklx, key=lambda s: s.y).y
        for ekifeojqhe in shjobgeklx:
            (self.zvojhrjxxm if ekifeojqhe.y == bujvmlirav else self.ztgmtnnufb).append(ekifeojqhe)
        self.cifzvbcuwqe: list[tuple[list[Sprite], list[Sprite]]] = []
        for kubalgsiiy in sorted(
            self.current_level.get_sprites_by_name("iqrduxrukrk"),
            key=lambda len: (len.y, len.x),
        ):
            uqjncpbdwl = self.current_level.get_sprite_at(kubalgsiiy.x, kubalgsiiy.y, "nxkictbbvzt")
            assert uqjncpbdwl
            zvojhrjxxm = [uqjncpbdwl]
            while xvusjrqdea := self.qrkneeaawb(zvojhrjxxm[0], -1):
                zvojhrjxxm.insert(0, xvusjrqdea)
            wipfopcbaq = self.current_level.get_sprite_at(kubalgsiiy.x + kubalgsiiy.width, kubalgsiiy.y, "nxkictbbvzt")
            assert wipfopcbaq
            ztgmtnnufb = [wipfopcbaq]
            while xvusjrqdea := self.qrkneeaawb(ztgmtnnufb[-1], 1):
                ztgmtnnufb.append(xvusjrqdea)
            self.cifzvbcuwqe.append((zvojhrjxxm, ztgmtnnufb))
        ripmydnety = [7, 7, 32, 18, 23, 11]
        fcnjuctdrc.seed(ripmydnety[self._current_level_index])
        if self.current_level.get_data("alter_rules"):
            for zvojhrjxxm, ztgmtnnufb in self.cifzvbcuwqe:
                for zdwrfusvmx in (zvojhrjxxm, ztgmtnnufb):
                    dkmtlqnzhy = fcnjuctdrc.randint(0, 6)
                    for i, ekifeojqhe in enumerate(zdwrfusvmx):
                        for garumvurkj in range(dkmtlqnzhy):
                            ekifeojqhe = self.wpbnovjwkv(ekifeojqhe, 1)
                        zdwrfusvmx[i] = ekifeojqhe
        else:
            for i, wipfopcbaq in enumerate(self.ztgmtnnufb):
                for garumvurkj in range(fcnjuctdrc.randint(0, 6)):
                    wipfopcbaq = self.wpbnovjwkv(wipfopcbaq, 1)
                self.ztgmtnnufb[i] = wipfopcbaq
        for ujwvrzndre in self.current_level.get_sprites_by_tag("tjaqvwdgkxe"):
            ujwvrzndre.set_visible(False)
        self.qvtymdcqear_index = 0
        self.qvtymdcqear_parts = [
            sprites["qvtymdcqear1"].clone(),
            sprites["qvtymdcqear1"].clone().set_rotation(180),
        ]
        for amnujekybw in self.qvtymdcqear_parts:
            self.current_level.add_sprite(amnujekybw)
        self.pjqbnqnbsq()
        self.vfpimnmtnta = 128 if self._current_level_index <= 4 else 256
        self.upmkivwyrxz = self.vfpimnmtnta
        self.yfetxjexviz = -1
        self.pvgetmhmhgk: list[tuple[list[Sprite], list[Sprite]]] = []
        self.hgfgmiagdcc: list[list[Sprite]] = []
        self.crvjftupafy: list[Sprite] = []

    def step(self) -> None:
        if self.yfetxjexviz >= 0:
            sxvrnnaenp = self.yfetxjexviz // (len(rhoqllymmn) - 1)
            wlumnlwumu, iwqlormuzq = self.pvgetmhmhgk[sxvrnnaenp]
            doicrtxjqh = self.yfetxjexviz % (len(rhoqllymmn) - 1) + 1
            tqqhnygzgwn = rhoqllymmn[doicrtxjqh - 1]
            pmrplgnzmz = rhoqllymmn[doicrtxjqh]
            for ekifeojqhe in wlumnlwumu + iwqlormuzq:
                ekifeojqhe.color_remap(tqqhnygzgwn, pmrplgnzmz)
            if doicrtxjqh == 1:
                for mlihpcjjay in self.crvjftupafy:
                    self.current_level.remove_sprite(mlihpcjjay)
                self.crvjftupafy = []
                for ekifeojqhe in self.hgfgmiagdcc[sxvrnnaenp]:
                    mlihpcjjay = sprites["nxkictbbvztedxeenecwqa"].clone().set_position(ekifeojqhe.x - 2, ekifeojqhe.y - 2)
                    self.current_level.add_sprite(mlihpcjjay)
                    self.crvjftupafy.append(mlihpcjjay)
            self.yfetxjexviz += 1
            if self.yfetxjexviz == len(self.pvgetmhmhgk) * (len(rhoqllymmn) - 1):
                self.next_level()
                self.complete_action()
            return
        elif self.action.id in [GameAction.ACTION3, GameAction.ACTION4]:
            pxdsteijos = -1 if self.action.id == GameAction.ACTION3 else 1
            if self.current_level.get_data("alter_rules"):
                qrkshsinvo = len([set for rule in self.cifzvbcuwqe for set in rule])
                self.qvtymdcqear_index = (self.qvtymdcqear_index + pxdsteijos) % qrkshsinvo
            else:
                self.qvtymdcqear_index = (self.qvtymdcqear_index + pxdsteijos) % len(self.ztgmtnnufb)
            self.upmkivwyrxz -= 1
            self.pjqbnqnbsq()
        elif self.action.id in [GameAction.ACTION1, GameAction.ACTION2]:
            pxdsteijos = -1 if self.action.id == GameAction.ACTION1 else 1
            if self.current_level.get_data("alter_rules"):
                hjcabtfnyd = [set for rule in self.cifzvbcuwqe for set in rule][self.qvtymdcqear_index]
                for i in range(len(hjcabtfnyd)):
                    hjcabtfnyd[i] = self.wpbnovjwkv(hjcabtfnyd[i], pxdsteijos)
            else:
                riedikehfs = self.ztgmtnnufb[self.qvtymdcqear_index]
                self.ztgmtnnufb[self.qvtymdcqear_index] = self.wpbnovjwkv(riedikehfs, pxdsteijos)
            self.upmkivwyrxz -= 1
            if self.bsqsshqpox():
                for ovlegoyeof in self.qvtymdcqear_parts:
                    ovlegoyeof.set_visible(False)
                self.yfetxjexviz = 0
                return
        if self.upmkivwyrxz == 0:
            self.lose()
        self.complete_action()

    def wpbnovjwkv(self, ekifeojqhe: Sprite, pxdsteijos: int) -> Sprite:
        eotxrfujzw = ekifeojqhe.name[:-1] + str((int(ekifeojqhe.name[-1]) + pxdsteijos - 1) % kjgicbtgrt + 1)
        qdejgfuxcd = sprites[eotxrfujzw].clone().set_position(ekifeojqhe.x, ekifeojqhe.y).set_rotation(ekifeojqhe.rotation)
        self.current_level.remove_sprite(ekifeojqhe)
        self.current_level.add_sprite(qdejgfuxcd.set_blocking(BlockingMode.BOUNDING_BOX))
        return qdejgfuxcd

    def pjqbnqnbsq(self) -> None:
        ekifeojqhe: Sprite = Sprite([[]])
        if self.current_level.get_data("alter_rules"):
            hjcabtfnyd = [set for rule in self.cifzvbcuwqe for set in rule][self.qvtymdcqear_index]
            ekifeojqhe = hjcabtfnyd[0]
            for ovlegoyeof in self.qvtymdcqear_parts:
                ovlegoyeof.pixels = sprites[f"qvtymdcqear{len(hjcabtfnyd)}"].pixels
        else:
            ekifeojqhe = self.ztgmtnnufb[self.qvtymdcqear_index]
        y_offset = 4
        self.qvtymdcqear_parts[0].set_position(ekifeojqhe.x, ekifeojqhe.y - y_offset)
        self.qvtymdcqear_parts[1].set_position(ekifeojqhe.x, ekifeojqhe.y + ekifeojqhe.height - 2 + y_offset)

    def bsqsshqpox(self) -> bool:
        def lonhgifaes(khgizrwwiq: list[Sprite], xwaazaiaiq: list[Sprite]) -> tuple[list[Sprite], list[Sprite], bool]:
            hbpsxvabst = self.current_level.get_sprite_at(khgizrwwiq[0].x, khgizrwwiq[0].y, "tjaqvwdgkxe")
            if not hbpsxvabst:
                return (khgizrwwiq, xwaazaiaiq, False)
            if hbpsxvabst.name.endswith("2"):
                return ([], [], True)
            opcpzryowp = self.current_level.get_sprites_by_name(hbpsxvabst.name.replace("1", "2"))[0]
            ekifeojqhe = self.current_level.get_sprite_at(opcpzryowp.x, opcpzryowp.y, "nxkictbbvzt")
            oopnsfckvu = next((rule for rule in self.cifzvbcuwqe if ekifeojqhe == rule[0][0]))
            return (khgizrwwiq + oopnsfckvu[0], xwaazaiaiq + oopnsfckvu[1], False)

        eutyeiwurz = 0
        pcxqrgcdzp = 0
        self.pvgetmhmhgk = []
        self.hgfgmiagdcc = []
        while eutyeiwurz < len(self.zvojhrjxxm):
            for khgizrwwiq, xwaazaiaiq in self.cifzvbcuwqe:
                if not self.iwbhnvdaao(self.zvojhrjxxm, eutyeiwurz, khgizrwwiq):
                    continue
                oqayswlmoi = []
                if self.current_level.get_data("tree_translation"):
                    uegbdcgewp = []
                    fqxtknymvq = False
                    for ekifeojqhe in xwaazaiaiq:
                        for avnzkzyzox, cbktvqgplb in self.cifzvbcuwqe:
                            if avnzkzyzox[0].name == ekifeojqhe.name:
                                uegbdcgewp += cbktvqgplb
                                oqayswlmoi += [ekifeojqhe] + avnzkzyzox
                                break
                        else:
                            fqxtknymvq = True
                            break
                    if fqxtknymvq:
                        continue
                    xwaazaiaiq = uegbdcgewp
                elif self.current_level.get_data("double_translation"):
                    khgizrwwiq, xwaazaiaiq, skip = lonhgifaes(khgizrwwiq, xwaazaiaiq)
                    if skip:
                        continue
                    for avnzkzyzox, cbktvqgplb in self.cifzvbcuwqe:
                        avnzkzyzox, cbktvqgplb, skip = lonhgifaes(avnzkzyzox, cbktvqgplb)
                        if skip:
                            continue
                        if all((a.name == b.name for a, b in zip(xwaazaiaiq, avnzkzyzox))):
                            oqayswlmoi = xwaazaiaiq + avnzkzyzox
                            xwaazaiaiq = cbktvqgplb
                            break
                    else:
                        continue
                if not self.iwbhnvdaao(self.ztgmtnnufb, pcxqrgcdzp, xwaazaiaiq):
                    return False
                wlumnlwumu = self.zvojhrjxxm[eutyeiwurz : eutyeiwurz + len(khgizrwwiq)]
                iwqlormuzq = self.ztgmtnnufb[pcxqrgcdzp : pcxqrgcdzp + len(xwaazaiaiq)]
                self.pvgetmhmhgk.append((wlumnlwumu, iwqlormuzq))
                self.hgfgmiagdcc.append(khgizrwwiq + xwaazaiaiq + oqayswlmoi)
                eutyeiwurz += len(khgizrwwiq)
                pcxqrgcdzp += len(xwaazaiaiq)
                break
            else:
                return False
        return True

    def iwbhnvdaao(self, zdwrfusvmx: list[Sprite], pyypoawbid: int, gnxftjtboz: list[Sprite]) -> bool:
        if pyypoawbid + len(gnxftjtboz) > len(zdwrfusvmx):
            return False
        for i in range(len(gnxftjtboz)):
            if zdwrfusvmx[pyypoawbid + i].name != gnxftjtboz[i].name:
                return False
        return True

    def qrkneeaawb(self, ekifeojqhe: Sprite, pxdsteijos: int) -> Sprite | None:
        xvusjrqdea = None
        for s in self.zdwrfusvmx:
            if s.x == ekifeojqhe.x + pxdsteijos * iokndxodxw and s.y == ekifeojqhe.y:
                xvusjrqdea = s
                break
        return xvusjrqdea

    def _get_hidden_state(self) -> np.ndarray:
        return np.array([self.upmkivwyrxz])
