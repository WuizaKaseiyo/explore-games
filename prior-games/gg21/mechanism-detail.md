# gg21 — flashlight-key-maze

Hidden-information maze with an embodied avatar. Arrow keys move the player
and set the flashlight facing. The short cone reveals only nearby cells in
front of the avatar; previously seen cells remain dim memory. `ACTION5` picks
up a key on the current cell if the backpack has room, or drops the oldest
carried key when standing on an empty floor. Moving into a locked door consumes
a matching carried key and opens the door; moving onto the exit wins.

Level 1 teaches the loop: discover a red door, search for the red key, return
and open the door to reach the hidden exit. Level 2 adds two door colours and
capacity-one inventory, so the player must spend the red key before carrying
the blue key. Level 3 increases backpack capacity to two and adds three locked
regions plus a decoy key, making exploration order and inventory management
matter.

The game now avoids blind panel-clicking: all meaningful interaction happens
through navigation and locally visible objects inside the maze. The board uses
a full 15x15 logical maze on the 64x64 frame, with fog, dim memory, flashlight
cones, shaped keys, keyed doors, backpack slots, and a discovered-door colour
strip.
