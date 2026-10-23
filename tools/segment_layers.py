"""Segment the symmetric back-view body and clean tail into animated rig layers."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

WORKDIR = Path("projects/mo_den_motion_demo/back_wiggle")

def main():
    body_img = Image.open(WORKDIR / "test_symmetric_body.png").convert("RGBA")
    body_arr = np.array(body_img)
    H, W = body_arr.shape[:2]

    # --- 1. Separate Upper Body / Head ---
    # Head and upper back down to y = 620
    # Soft vertical transition around y=580..630
    upper = body_arr.copy()
    upper_alpha = upper[:, :, 3].astype(np.float32)
    # Mask out below 630 with a smooth 20px ramp
    ramp_y = np.arange(H)
    upper_weight = np.clip((630 - ramp_y) / 30.0, 0.0, 1.0)[:, None]
    upper[:, :, 3] = (upper_alpha * upper_weight).astype(np.uint8)
    Image.fromarray(upper).save(WORKDIR / "layer_upper_head.png")
    print("Saved layer_upper_head.png")

    # --- 2. Separate Rump / Buttocks ---
    # Buttocks from y = 570 down to y = 880 (without paws)
    rump = body_arr.copy()
    rump_alpha = rump[:, :, 3].astype(np.float32)
    # Top ramp around 570..600
    top_weight = np.clip((ramp_y - 565) / 30.0, 0.0, 1.0)[:, None]
    # Bottom cut above paws (y < 860)
    bot_weight = np.clip((860 - ramp_y) / 20.0, 0.0, 1.0)[:, None]
    rump[:, :, 3] = (rump_alpha * top_weight * bot_weight).astype(np.uint8)
    Image.fromarray(rump).save(WORKDIR / "layer_rump.png")
    print("Saved layer_rump.png")

    # --- 3. Separate Hind Paws ---
    # Dark brown paws at the floor (y > 780)
    paws = body_arr.copy()
    paws_alpha = paws[:, :, 3].astype(np.float32)
    paw_weight = np.clip((ramp_y - 785) / 20.0, 0.0, 1.0)[:, None]
    # Only keep the brown paw pads
    is_brown = (paws[:, :, 0] < 120) & (paws[:, :, 1] < 90) & (paws[:, :, 2] < 80)
    paws[:, :, 3] = (paws_alpha * paw_weight * is_brown.astype(np.float32)).astype(np.uint8)
    Image.fromarray(paws).save(WORKDIR / "layer_paws.png")
    print("Saved layer_paws.png")

    # --- 4. Clean Tail Sprite ---
    tail_raw = Image.open(WORKDIR / "test_tail_cleaned.png").convert("RGBA")
    t_arr = np.array(tail_raw)
    
    # Crop tail to its bounding box
    ys, xs = np.where(t_arr[:, :, 3] > 0)
    min_y, max_y = ys.min(), ys.max()
    min_x, max_x = xs.min(), xs.max()
    
    tail_cropped = tail_raw.crop((min_x - 5, min_y - 5, max_x + 5, max_y + 5))
    tail_cropped.save(WORKDIR / "layer_tail.png")
    
    # Record metadata
    # Root of tail in original canvas was at: x ≈ 565, y ≈ 779
    # In the cropped image, root is at:
    root_in_crop_x = 565 - (min_x - 5)
    root_in_crop_y = 779 - (min_y - 5)
    print(f"Tail crop size: {tail_cropped.size}, root in crop: ({root_in_crop_x}, {root_in_crop_y})")

if __name__ == "__main__":
    main()
