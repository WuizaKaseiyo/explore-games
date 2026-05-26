# gg22 — conveyor-switch-sorter

Clocked conveyor sorter. Parcels are moved only by the belt: `ACTION5`
advances every in-flight parcel one conveyor node and automatically feeds the
next queued parcel when that parcel's own inlet is clear. Each level is one
connected conveyor graph with staggered inlets, rather than isolated direct
lanes. The player does not steer parcels with arrow keys. `ACTION6` toggles
visible control cells: junction switches choose which outgoing branch a parcel
will take when it reaches that junction, and level 3 adds a station-mode switch
that changes a station from blue-circle marking to gold-timer marking.

Level 1 teaches live switch timing on a connected top-fed sorter. Three
staggered parcels merge into a top trunk that drops at the right edge; the
first switch can peel red into the upper stripe lane, while its default branch
continues to a second switch that splits blue's middle circle lane from gold's
lower square lane.

Level 2 mirrors the geometry: parcels enter on the top row from varied columns
and ride right-to-left into a left-edge branch. The output lanes then run back
to the right. Two red parcels must share the upper stripe rail, blue must be
sent through the middle circle lane, and green must wait for the lower square
lane. With no switch timing, the default branch sends parcels to wrong targets.

Level 3 changes orientation. Parcels start on the bottom row, ride left, climb
an upward spine, then split through a central dispatcher. The first red parcel
needs the top stripe rail, blue must clear the lower circle rail before the
second switch is changed, gold must then be diverted into the middle lane after
the mode station has been toggled to timer, and the final red parcel must catch
the top rail again. The default switch states do not solve the level.

The sorting mechanism is controlled through switches, while parcel motion is
conveyor-driven. Switch state is drawn twice: as the switch tile itself and as
a bright directional overlay after parcels render, so the active branch remains
readable even when a parcel sits on the switch. Output cells show their required
colour/mark signatures directly, so there is no separate target legend. A parcel
that reaches its matching-colour output records that output's displayed
signature; this keeps the route result authoritative even if a station mode was
toggled while a parcel was on the station. Parcel collisions fail immediately;
wrong-colour deliveries are resolved after the current belt run drains.
