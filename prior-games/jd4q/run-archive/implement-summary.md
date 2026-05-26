# implement-summary — jd4q

## Files written
- `prior-games/jd4q/jd4q.py` (530 lines)
- `prior-games/jd4q/metadata.json`

## Implementation summary

The avatar walks a 16-cell maze on a 64×64 grid (cell-stride 4). On
every step the previous cell becomes a fading marker; clicking any
visible marker rewinds the avatar to that cell and consumes that
marker plus every later marker. Some level cells are one-way
passages that close behind the avatar after egress, and some cells
wipe the entire marker trail when the avatar enters them. The three
levels progressively introduce these mechanisms — L1 plain walk to a
single goal; L2 adds the marker mechanism plus one-way passages
behind a single dead-end pickup; L3 layers the trail-wipe cell on
top, so a multi-pickup tour with three branches must be ordered
around it. The implementation follows the universal scaffold:
sprite bank → level builders → constants → HUD widget → game class.
All instantiation and a simulated 3-level witness traversal succeed
under the local novaengine.
