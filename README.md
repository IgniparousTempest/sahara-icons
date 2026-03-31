# sahara-icons
Icons for Sahara CAD software

## Icons

| Icon | Name |
|------|------|
| ![constraint_coincidence](icons/svg/constraint_coincidence.svg) | constraint_coincidence |
| ![constraint_parallel](icons/svg/constraint_parallel.svg) | constraint_parallel |
| ![constraint_perpendicular](icons/svg/constraint_perpendicular.svg) | constraint_perpendicular |
| ![constraint_distance](icons/svg/constraint_distance.svg) | constraint_distance |

## Design Language

Background: `#23456D`

| Colour | Hex | Usage |
|--------|-----|-------|
| Orange | `#E8873D` | Primary subject — the object being acted upon |
| Dark | `#0F1B2D` | Reference object — the object in relation to |
| Light | `#D6E4F0` | Annotations |

## Prerequisites

[librsvg](https://wiki.gnome.org/Projects/LibRsvg) for SVG to PNG conversion.
[msdfgen](https://github.com/Chlumsky/msdfgen) for MSDF texture generation.

macOS:
```bash
brew install librsvg cmake
git clone --branch v1.12 https://github.com/Chlumsky/msdfgen.git
cd msdfgen && cmake -B build -DMSDFGEN_USE_VCPKG=OFF -DMSDFGEN_USE_SKIA=OFF && cmake --build build && sudo cmake --install build
```

Debian/Ubuntu:
```bash
sudo apt install librsvg2-bin
# msdfgen must be built from source
git clone https://github.com/Chlumsky/msdfgen.git
cd msdfgen && cmake -B build && cmake --build build
```

Fedora:
```bash
sudo dnf install librsvg2-tools
# msdfgen must be built from source
git clone https://github.com/Chlumsky/msdfgen.git
cd msdfgen && cmake -B build && cmake --build build
```

## Building

Generate all PNGs and MSDFs:
```bash
make
```

Generate only PNGs:
```bash
make png
```

Generate only MSDFs:
```bash
make msdf
```

Clean generated files:
```bash
make clean
```
