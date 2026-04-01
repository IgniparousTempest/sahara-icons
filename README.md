# sahara-icons
Icons for Sahara CAD software

## Icons

| Icon | Name |
|------|------|
| ![constraint_coincidence](icons/svg/constraint_coincidence.svg) | constraint_coincidence |
| ![constraint_distance](icons/svg/constraint_distance.svg) | constraint_distance |
| ![constraint_divide](icons/svg/constraint_divide.svg) | constraint_divide |
| ![constraint_parallel](icons/svg/constraint_parallel.svg) | constraint_parallel |
| ![constraint_perpendicular](icons/svg/constraint_perpendicular.svg) | constraint_perpendicular |
| ![constraint_symetry](icons/svg/constraint_symetry.svg) | constraint_symetry |

## Design Language

Background: `#23456D`

| Colour | Hex | Usage |
|--------|-----|-------|
| Orange | `#E8873D` | Primary subject — the object being acted upon |
| Dark | `#0F1B2D` | Reference object — the object in relation to |
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
