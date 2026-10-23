"""Prepare segmented character rig layers from the back-view master illustration.

Inputs:
- projects/mo_den_motion_demo/back_wiggle/mo_den_back_view_source.jpg

Outputs in projects/mo_den_motion_demo/back_wiggle/:
- master_transparent.png: Full cat with transparent background
- body_rump_clean.png: Full body with intact symmetrical buttocks (infilled behind tail)
- tail.png: Isolated tail sprite with transparent background
- head.png: Head and ears isolated
- hind_paws.png: Hind paws isolated
"""
import os
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import binary_fill_holes

ROOT = Path(__file__).resolve().parents[1]
WORKDIR = ROOT / "projects/mo_den_motion_demo/back_wiggle"
SRC_PATH = WORKDIR / "mo_den_back_view_source.jpg"

def main():
    img = Image.open(SRC_PATH).convert("RGBA")
    arr = np.array(img, dtype=np.float32)
    rgb = arr[:, :, :3]

    # 1. Background Masking:
    # The background is solid white / off-white (~250-255).
    # Cat outlines are dark ink (#080807), fur is cream (#faeee0 to #eed0ad), brown parts are #3e271d.
    # We can detect background by flood filling from edges where color is nearly white.
    is_white = np.all(rgb > 240, axis=2)
    
    # Flood fill from image boundary
    from scipy.ndimage import label
    labeled, num_features = label(is_white)
    
    # Find boundary labels (corners and edges)
    edge_labels = set()
    edge_labels.update(np.unique(labeled[0, :]))
    edge_labels.update(np.unique(labeled[-1, :]))
    edge_labels.update(np.unique(labeled[:, 0]))
    edge_labels.update(np.unique(labeled[:, -1]))
    edge_labels.discard(0)
    
    bg_mask = np.isin(labeled, list(edge_labels))
    
    # Smooth alpha matte with anti-aliasing
    alpha = np.where(bg_mask, 0.0, 255.0).astype(np.uint8)
    alpha_img = Image.fromarray(alpha, mode="L")
    alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(radius=0.8))
    
    # Save master transparent
    master = img.copy()
    master.putalpha(alpha_img)
    master.save(WORKDIR / "master_transparent.png")
    print("Saved master_transparent.png")
    
    # Find center axis of symmetry for the body
    # Center between the ears / butt cheeks
    # Let's inspect center axis
    arr_alpha = np.array(master)
    cat_mask = arr_alpha[:, :, 3] > 128
    
    # Find center of bottom rump
    rump_mask = cat_mask & (np.arange(1024)[:, None] > 600) & (np.arange(1024)[:, None] < 880)
    ys_r, xs_r = np.where(rump_mask)
    rump_center_x = (xs_r.min() + xs_r.max()) / 2.0
    print(f"Rump x-span: [{xs_r.min()}, {xs_r.max()}], center: {rump_center_x:.2f}")

if __name__ == "__main__":
    main()
