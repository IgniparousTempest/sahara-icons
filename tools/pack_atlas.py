#!/usr/bin/env python3
import json, math, sys, os
from PIL import Image

def pack_atlas(msdf_dir, output_png, output_json):
    files = sorted(f for f in os.listdir(msdf_dir) if f.endswith('.png'))
    if not files:
        sys.exit("No MSDF PNGs found in " + msdf_dir)

    images = [(f.removesuffix('.png'), Image.open(os.path.join(msdf_dir, f))) for f in files]
    cell_w = max(img.width for _, img in images)
    cell_h = max(img.height for _, img in images)
    cols = math.ceil(math.sqrt(len(images)))
    rows = math.ceil(len(images) / cols)
    atlas_w = cols * cell_w
    atlas_h = rows * cell_h

    atlas = Image.new('RGBA', (atlas_w, atlas_h), (0, 0, 0, 0))
    manifest = {"width": atlas_w, "height": atlas_h, "icons": {}}

    for i, (name, img) in enumerate(images):
        x = (i % cols) * cell_w
        y = (i // cols) * cell_h
        atlas.paste(img, (x, y))
        manifest["icons"][name] = {
            "x": x, "y": y,
            "w": img.width, "h": img.height,
            "u0": x / atlas_w, "v0": y / atlas_h,
            "u1": (x + img.width) / atlas_w, "v1": (y + img.height) / atlas_h,
        }

    atlas.save(output_png)
    with open(output_json, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"Atlas: {atlas_w}x{atlas_h}, {len(images)} icons -> {output_png}")

if __name__ == '__main__':
    pack_atlas(sys.argv[1], sys.argv[2], sys.argv[3])
