# sahara-icons
Icons for Sahara CAD software

## Icons

| Icon | Name | Label |
|------|------|-------|
| ![action_boolean_difference](icons/svg/action_boolean_difference.svg) | action_boolean_difference | Boolean Difference |
| ![action_boolean_intersection](icons/svg/action_boolean_intersection.svg) | action_boolean_intersection | Boolean Intersection |
| ![action_boolean_none](icons/svg/action_boolean_none.svg) | action_boolean_none | Boolean None |
| ![action_boolean_union](icons/svg/action_boolean_union.svg) | action_boolean_union | Boolean Union |
| ![constraint_angle](icons/svg/constraint_angle.svg) | constraint_angle | Angle Constraint |
| ![constraint_coincidence](icons/svg/constraint_coincidence.svg) | constraint_coincidence | Coincidence Constraint |
| ![constraint_distance](icons/svg/constraint_distance.svg) | constraint_distance | Distance Constraint |
| ![constraint_divide](icons/svg/constraint_divide.svg) | constraint_divide | Divide Constraint |
| ![constraint_horizontal_vertical](icons/svg/constraint_horizontal_vertical.svg) | constraint_horizontal_vertical | Horizontal/Vertical Constraint |
| ![constraint_parallel](icons/svg/constraint_parallel.svg) | constraint_parallel | Parallel Constraint |
| ![constraint_perpendicular](icons/svg/constraint_perpendicular.svg) | constraint_perpendicular | Perpendicular Constraint |
| ![constraint_symetry](icons/svg/constraint_symetry.svg) | constraint_symetry | Symmetry Constraint |
| ![tool_chamfer](icons/svg/tool_chamfer.svg) | tool_chamfer | Chamfer |
| ![tool_circle_centre_point](icons/svg/tool_circle_centre_point.svg) | tool_circle_centre_point | Circle (Centre Point) |
| ![tool_extrude](icons/svg/tool_extrude.svg) | tool_extrude | Extrude |
| ![tool_fillet](icons/svg/tool_fillet.svg) | tool_fillet | Fillet |
| ![tool_hole](icons/svg/tool_hole.svg) | tool_hole | Hole |
| ![tool_line](icons/svg/tool_line.svg) | tool_line | Line |
| ![tool_move_rotate](icons/svg/tool_move_rotate.svg) | tool_move_rotate | Move Rotate |
| ![tool_point](icons/svg/tool_point.svg) | tool_point | Point |
| ![tool_rectangle_2_point](icons/svg/tool_rectangle_2_point.svg) | tool_rectangle_2_point | Rectangle (2 Point) |
| ![tool_revolve](icons/svg/tool_revolve.svg) | tool_revolve | Revolve |
| ![tool_select](icons/svg/tool_select.svg) | tool_select | Select |
| ![tool_sketch](icons/svg/tool_sketch.svg) | tool_sketch | Sketch |
| ![tool_sketch_fillet](icons/svg/tool_sketch_fillet.svg) | tool_sketch_fillet | Sketch Fillet |
| ![tool_slot_centre_to_centre](icons/svg/tool_slot_centre_to_centre.svg) | tool_slot_centre_to_centre | Slot (Centre to Centre) |

## Design Language

Background: `#23456D`

| Colour | Hex | Usage |
|--------|-----|-------|
| Orange | `#E8873D` | Primary subject — the object being acted upon |
| Orange Highlight | `#F2A96A` | Primary subject — highlighted |
| Orange Shadow | `#B5642A` | Primary subject — shaded |
| Dark | `#0F1B2D` | Reference object — the object in relation to |
| Dark Highlight | `#1E3454` | Reference object — highlighted |
| Dark Shadow | `#080E18` | Reference object — shaded |
| Light | `#D6E4F0` | Annotations |

## Prerequisites

[librsvg](https://wiki.gnome.org/Projects/LibRsvg) for SVG to PNG conversion.
Python 3 with Pillow, scipy, and numpy for SDF atlas generation.

macOS:
```bash
brew install librsvg
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Debian/Ubuntu:
```bash
sudo apt install librsvg2-bin
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Fedora:
```bash
sudo dnf install librsvg2-tools
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## SDF Atlas

The build pipeline generates a Signed Distance Field (SDF) texture atlas for efficient, resolution-independent icon rendering in OpenGL.

Each icon is rasterised three times — once per design language colour — to isolate each layer. A distance transform is then applied to each layer, producing a greyscale SDF where values above 0.5 are inside the shape and below 0.5 are outside. The three SDFs are packed into the RGB channels of a single image:

| Channel | Colour | Layer |
|---------|--------|-------|
| R | `#E8873D` | Primary subject |
| G | `#0F1B2D` | Reference object |
| B | `#D6E4F0` | Annotations |

The individual SDF images are then packed into a single texture atlas (`icons/atlas.png`) with a JSON manifest (`icons/atlas.json`) containing pixel coordinates and normalised UV coordinates for each icon.

At render time, a fragment shader samples each channel, applies a smoothstep threshold, and composites the layers with their original colours. This allows icons to scale cleanly to any size without aliasing artefacts.

## Building

Generate all PNGs and SDF atlas:
```bash
make
```

Generate only PNGs:
```bash
make png
```

Generate only SDF textures:
```bash
make sdf
```

Generate atlas:
```bash
make atlas
```

Clean generated files:
```bash
make clean
```
