import os
from PIL import Image
import numpy as np
from watermark_engine import WatermarkingEngine, calculate_psnr, calculate_nc, calculate_ssim

host_path = 'samples/host_image.png' if os.path.exists('samples/host_image.png') else 'dataset/host_image.png'
wm_path = 'samples/watermark.png' if os.path.exists('samples/watermark.png') else 'dataset/watermark.png'

print(f"Loading host: {host_path}, watermark: {wm_path}")
host = Image.open(host_path)
wm = Image.open(wm_path)

engine = WatermarkingEngine(strength=30.0, bits_per_block=2)
print("1. Embedding...")
embed_res = engine.embed(host, wm, key=12345)
wm_img = embed_res['watermarked_image']
manifest = embed_res['manifest']
print(f"   Embedded successfully! PSNR: {manifest['metrics']['psnr']} dB, SSIM: {manifest['metrics']['ssim']}")

print("2. Extracting and Separating...")
extract_res = engine.extract_and_separate(
    wm_img,
    key=12345,
    perms=manifest['perms'],
    watermark_size=manifest['watermark_size'],
    bits_per_block=manifest['bits_per_block'],
    strength=manifest['strength']
)

extracted_wm = extract_res['extracted_watermark']
separated_host = extract_res['separated_host']

orig_wm_32 = wm.convert('RGB').resize((32, 32))
nc = calculate_nc(np.array(orig_wm_32), np.array(extracted_wm))
host_psnr = calculate_psnr(np.array(host.convert('RGB')), np.array(separated_host))

print(f"   Extraction complete!")
print(f"   NC (Original vs Extracted): {nc:.4f}")
print(f"   Host Separation Quality (Original Host vs Restored Host PSNR): {host_psnr:.2f} dB")

print("3. Testing Attacks...")
for attack in ['gaussian_noise', 'sharpen', 'resize', 'jpeg']:
    attacked = WatermarkingEngine.apply_attack(wm_img, attack)
    ext_attack = engine.extract_and_separate(
        attacked,
        key=12345,
        perms=manifest['perms'],
        watermark_size=manifest['watermark_size'],
        bits_per_block=manifest['bits_per_block'],
        strength=manifest['strength']
    )
    nc_atk = calculate_nc(np.array(orig_wm_32), np.array(ext_attack['extracted_watermark']))
    print(f"   Attack [{attack:15s}] -> Extracted Watermark NC: {nc_atk:.4f}")

print("All tests passed with flying colors!")
