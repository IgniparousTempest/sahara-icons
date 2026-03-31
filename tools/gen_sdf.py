#!/usr/bin/env python3
"""Generate per-icon SDF textures with one colour layer per RGB channel."""
import json, math, sys, os, tempfile, subprocess
import numpy as np
from scipy.ndimage import distance_transform_edt
from PIL import Image

COLORS = {
    "R": "#e8873d",  # primary subject
    "G": "#0f1b2d",  # reference object
    "B": "#d6e4f0",  # annotations
}

def make_css(keep_color, all_colors):
    """CSS that hides everything except keep_color."""
    rules = []
    for color in all_colors.values():
        if color == keep_color:
            rules.append(f'[style*="{color}"] {{ opacity: 1; }}')
        else:
            rules.append(f'[style*="{color}"] {{ opacity: 0; }}')
    return "\n".join(rules)

def render_layer(svg_path, css_content, size):
    with tempfile.NamedTemporaryFile(suffix=".css", mode="w", delete=False) as f:
        f.write(css_content)
        css_path = f.name
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        png_path = f.name
    try:
        subprocess.run(
            ["rsvg-convert", "-w", str(size), "-h", str(size), "-s", css_path, svg_path, "-o", png_path],
            check=True, capture_output=True,
        )
        return np.array(Image.open(png_path).convert("RGBA"))
    finally:
        os.unlink(css_path)
        os.unlink(png_path)

def alpha_to_sdf(alpha, spread):
    inside = distance_transform_edt(alpha > 128)
    outside = distance_transform_edt(alpha <= 128)
    dist = inside - outside
    dist = np.clip(dist / spread, -1, 1)
    return ((dist + 1) * 0.5 * 255).astype(np.uint8)

def process_svg(svg_path, output_path, size, spread):
    channels = {}
    for channel, color in COLORS.items():
        css = make_css(color, COLORS)
        layer = render_layer(svg_path, css, size)
        channels[channel] = alpha_to_sdf(layer[:, :, 3], spread)

    sdf_img = Image.merge("RGB", [Image.fromarray(channels[c]) for c in "RGB"])
    sdf_img.save(output_path)

def main():
    svg_dir, out_dir, size, spread = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
    os.makedirs(out_dir, exist_ok=True)
    for f in sorted(os.listdir(svg_dir)):
        if not f.endswith(".svg"):
            continue
        name = f.removesuffix(".svg")
        process_svg(os.path.join(svg_dir, f), os.path.join(out_dir, name + ".png"), size, spread)
        print(f"  {name}")

if __name__ == "__main__":
    main()
