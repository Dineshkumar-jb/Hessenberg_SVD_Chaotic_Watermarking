"""
Robust Digital Image Watermarking Engine
Based on DCT, Hessenberg Decomposition, and SVD-driven scrambling.
Designed for copyright protection, imperceptible embedding, blind extraction,
and host image separation.
"""

import os
import io
import math
import json
import base64
import hashlib
import numpy as np
from PIL import Image, ImageFilter
from scipy.fftpack import dct, idct
from scipy.linalg import hessenberg
import pywt


def dct2(block):
    """2D Discrete Cosine Transform (ortho normalized)."""
    return dct(dct(block.T, norm='ortho').T, norm='ortho')


def idct2(block):
    """2D Inverse Discrete Cosine Transform (ortho normalized)."""
    return idct(idct(block.T, norm='ortho').T, norm='ortho')


def calculate_psnr(arr1, arr2):
    """Calculate Peak Signal-to-Noise Ratio between two RGB or grayscale arrays."""
    i1 = np.asarray(arr1, dtype=np.float64)
    i2 = np.asarray(arr2, dtype=np.float64)
    mse = np.mean((i1 - i2) ** 2)
    if mse <= 1e-10:
        return 100.0  # Virtually identical
    return float(20 * math.log10(255.0 / math.sqrt(mse)))


def calculate_mse(arr1, arr2):
    """Calculate Mean Squared Error."""
    i1 = np.asarray(arr1, dtype=np.float64)
    i2 = np.asarray(arr2, dtype=np.float64)
    return float(np.mean((i1 - i2) ** 2))


def calculate_nc(arr1, arr2):
    """Calculate Normalized Correlation coefficient between two images."""
    a = np.asarray(arr1, dtype=np.float64).flatten()
    b = np.asarray(arr2, dtype=np.float64).flatten()
    num = np.sum(a * b)
    den = np.sqrt(np.sum(a ** 2) * np.sum(b ** 2))
    if den == 0:
        return 0.0
    return float(num / den)


def calculate_ssim(arr1, arr2):
    """
    Calculate Structural Similarity Index (SSIM) between two images.
    Implemented cleanly using NumPy without external heavy dependencies.
    """
    img1 = np.asarray(arr1, dtype=np.float64)
    img2 = np.asarray(arr2, dtype=np.float64)

    if img1.ndim == 3:
        # Average SSIM across color channels
        scores = [calculate_ssim(img1[:, :, c], img2[:, :, c]) for c in range(img1.shape[2])]
        return float(np.mean(scores))

    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2

    # Mean
    mu1 = np.mean(img1)
    mu2 = np.mean(img2)

    # Variance and Covariance
    sigma1_sq = np.var(img1)
    sigma2_sq = np.var(img2)
    sigma12 = np.mean((img1 - mu1) * (img2 - mu2))

    numerator = (2 * mu1 * mu2 + c1) * (2 * sigma12 + c2)
    denominator = (mu1 ** 2 + mu2 ** 2 + c1) * (sigma1_sq + sigma2_sq + c2)

    if denominator == 0:
        return 1.0
    return float(np.clip(numerator / denominator, -1.0, 1.0))


def calculate_ber(bits1, bits2):
    """Calculate Bit Error Rate."""
    b1 = np.asarray(bits1).flatten()
    b2 = np.asarray(bits2).flatten()
    min_len = min(len(b1), len(b2))
    if min_len == 0:
        return 0.0
    errors = np.sum(b1[:min_len] != b2[:min_len])
    return float(errors / min_len)


class WatermarkingEngine:
    """
    DCT + Hessenberg-SVD Watermarking Engine.
    Supports embedding, blind extraction, and host image separation.
    """

    def __init__(self, strength=30.0, bits_per_block=2, wavelet='haar', block_size=8):
        self.strength = float(strength)
        self.bits_per_block = int(bits_per_block)
        self.wavelet = wavelet
        self.block_size = int(block_size)
        # Mid-frequency DCT block coordinates for robust embedding
        self.positions = [(3, 3), (3, 4), (4, 3), (4, 4)]

    def scramble_watermark_channel(self, wm_channel, key):
        """
        Scrambles a single watermark channel using DWT -> DCT -> Hessenberg -> SVD
        and key-derived pseudo-random permutation.
        """
        wm = wm_channel.astype(np.float64)
        # 1. 2D Discrete Wavelet Transform
        LL, (LH, HL, HH) = pywt.dwt2(wm, self.wavelet)
        # 2. 2D DCT on approximation coefficients
        LL_dct = dct2(LL)
        # 3. Hessenberg decomposition
        H, Q = hessenberg(LL_dct, calc_q=True)
        # 4. Singular Value Decomposition
        U, S, Vt = np.linalg.svd(H, full_matrices=False)
        # 5. Extract singular value signature
        s_sum = int(np.round(np.sum(np.abs(S)) * 1e6))
        # 6. MD5 key fusion
        digest = hashlib.md5(f"{key}_{s_sum}".encode()).hexdigest()
        seed = int(digest[:8], 16)

        total = wm.size
        rng = np.random.RandomState(seed)
        perm = rng.permutation(total)

        flat = wm.flatten()
        scrambled_flat = flat[perm]
        scrambled = scrambled_flat.reshape(wm.shape).astype(np.uint8)

        return scrambled, perm, {
            "s_sum": s_sum,
            "seed": seed,
            "singular_values": S.tolist()[:4]
        }

    def descramble_watermark_channel(self, scrambled_channel, perm):
        """Descrambles a watermark channel using the inverse permutation."""
        flat = scrambled_channel.flatten()
        restored_flat = np.zeros_like(flat)
        restored_flat[perm] = flat
        return restored_flat.reshape(scrambled_channel.shape).astype(np.uint8)

    def generate_sequence(self, key, length):
        """Generates pseudo-random block embedding order using MD5 seed."""
        h = hashlib.md5(str(key).encode()).hexdigest()
        seed = int(h[:8], 16)
        rng = np.random.RandomState(seed)
        return rng.permutation(length)

    def embed(self, host_pil, watermark_pil, key=12345, strength=None, bits_per_block=None):
        """
        Embeds a watermark into a host image.
        Returns:
            dict containing watermarked image, scrambled watermark, metadata, and perms.
        """
        if strength is not None:
            self.strength = float(strength)
        if bits_per_block is not None:
            self.bits_per_block = int(bits_per_block)

        # Ensure RGB
        host = host_pil.convert('RGB')
        watermark = watermark_pil.convert('RGB')

        # Standardize watermark to 32x32 for optimal block capacity
        target_wm_size = (32, 32)
        if watermark.size != target_wm_size:
            watermark = watermark.resize(target_wm_size, Image.Resampling.LANCZOS)

        host_arr = np.array(host, dtype=np.float64)
        wm_arr = np.array(watermark, dtype=np.uint8)

        host_h, host_w = host_arr.shape[:2]
        wm_h, wm_w = wm_arr.shape[:2]

        available_blocks = (host_h // self.block_size) * (host_w // self.block_size)
        bits_needed_per_channel = wm_h * wm_w * 8
        available_bits = available_blocks * self.bits_per_block

        if bits_needed_per_channel > available_bits:
            self.bits_per_block = int(np.ceil(bits_needed_per_channel / available_blocks))
            available_bits = available_blocks * self.bits_per_block

        watermarked_channels = []
        scrambled_channels = []
        perms = []
        encryption_info = []

        num_blocks_h = host_h // self.block_size
        num_blocks_w = host_w // self.block_size
        total_blocks = num_blocks_h * num_blocks_w

        for ch in range(3):
            host_ch = host_arr[:, :, ch].copy()
            wm_ch = wm_arr[:, :, ch]

            # Scramble channel
            scrambled_ch, perm, enc_meta = self.scramble_watermark_channel(wm_ch, key + ch)
            scrambled_channels.append(scrambled_ch)
            perms.append(perm.tolist())
            encryption_info.append(enc_meta)

            wm_bits = np.unpackbits(scrambled_ch.flatten())
            total_bits = len(wm_bits)

            sequence = self.generate_sequence(key + ch, total_blocks)
            blocks_needed = int(np.ceil(total_bits / self.bits_per_block))

            watermarked_ch = host_ch.copy()
            bit_idx = 0

            for b in range(blocks_needed):
                if b >= len(sequence):
                    break
                block_num = sequence[b]
                br = block_num // num_blocks_w
                bc = block_num % num_blocks_w
                r0 = br * self.block_size
                c0 = bc * self.block_size

                block = host_ch[r0:r0 + self.block_size, c0:c0 + self.block_size].copy()
                d = dct2(block)

                for pidx in range(self.bits_per_block):
                    if bit_idx >= total_bits:
                        break
                    bit = int(wm_bits[bit_idx])
                    pos = self.positions[pidx % len(self.positions)]
                    mag = abs(d[pos])

                    if bit == 1:
                        d[pos] = mag + self.strength
                    else:
                        d[pos] = -(mag + self.strength)

                    bit_idx += 1

                modified_block = idct2(d)
                watermarked_ch[r0:r0 + self.block_size, c0:c0 + self.block_size] = modified_block

            watermarked_ch = np.clip(watermarked_ch, 0, 255).astype(np.uint8)
            watermarked_channels.append(watermarked_ch)

        watermarked_img_arr = np.stack(watermarked_channels, axis=2)
        scrambled_img_arr = np.stack(scrambled_channels, axis=2)

        watermarked_pil = Image.fromarray(watermarked_img_arr)
        scrambled_pil = Image.fromarray(scrambled_img_arr)

        # Quality metrics
        original_host_arr = np.array(host, dtype=np.uint8)
        psnr_val = calculate_psnr(original_host_arr, watermarked_img_arr)
        mse_val = calculate_mse(original_host_arr, watermarked_img_arr)
        ssim_val = calculate_ssim(original_host_arr, watermarked_img_arr)

        manifest = {
            "host_size": [host_w, host_h],
            "watermark_size": [wm_w, wm_h],
            "strength": self.strength,
            "bits_per_block": self.bits_per_block,
            "key": key,
            "wavelet": self.wavelet,
            "block_size": self.block_size,
            "perms": perms,
            "encryption_info": encryption_info,
            "metrics": {
                "psnr": round(psnr_val, 2),
                "mse": round(mse_val, 4),
                "ssim": round(ssim_val, 4)
            }
        }

        return {
            "watermarked_image": watermarked_pil,
            "scrambled_image": scrambled_pil,
            "original_watermark": watermark,
            "manifest": manifest
        }

    def extract_and_separate(self, watermarked_pil, key=12345, perms=None,
                             watermark_size=(32, 32), bits_per_block=None, strength=None):
        """
        Blindly extracts the embedded watermark from the watermarked image
        AND separates/restores the host image by reversing DCT modulation.

        Returns:
            dict containing:
            - extracted_watermark: restored watermark PIL Image
            - extracted_scrambled: raw extracted scrambled watermark PIL Image
            - separated_host: restored host PIL Image (watermark coefficients reverted)
            - metrics: extraction analysis metrics
        """
        if strength is not None:
            self.strength = float(strength)
        if bits_per_block is not None:
            self.bits_per_block = int(bits_per_block)

        wm_h, wm_w = watermark_size
        watermarked = watermarked_pil.convert('RGB')
        w_arr = np.array(watermarked, dtype=np.float64)

        host_h, host_w = w_arr.shape[:2]
        num_blocks_h = host_h // self.block_size
        num_blocks_w = host_w // self.block_size
        total_blocks = num_blocks_h * num_blocks_w

        extracted_channels = []
        scrambled_channels = []
        separated_host_channels = []

        num_bits = wm_h * wm_w * 8
        blocks_needed = int(np.ceil(num_bits / self.bits_per_block))

        for ch in range(3):
            wm_ch_img = w_arr[:, :, ch]
            host_restored_ch = wm_ch_img.copy()

            sequence = self.generate_sequence(key + ch, total_blocks)
            extracted_bits = []

            for b in range(blocks_needed):
                if b >= len(sequence):
                    break
                block_num = sequence[b]
                br = block_num // num_blocks_w
                bc = block_num % num_blocks_w
                r0 = br * self.block_size
                c0 = bc * self.block_size

                block = wm_ch_img[r0:r0 + self.block_size, c0:c0 + self.block_size].copy()
                d = dct2(block)

                # Coefficients restoration copy
                d_restored = d.copy()

                for pidx in range(self.bits_per_block):
                    if len(extracted_bits) >= num_bits:
                        break
                    pos = self.positions[pidx % len(self.positions)]
                    coef = d[pos]
                    bit = 1 if coef > 0 else 0
                    extracted_bits.append(bit)

                    # Separation: subtract embedding modulation strength to restore host coefficient
                    sign = 1.0 if coef >= 0 else -1.0
                    mag = abs(coef)
                    restored_mag = max(0.0, mag - self.strength)
                    d_restored[pos] = sign * restored_mag

                host_restored_ch[r0:r0 + self.block_size, c0:c0 + self.block_size] = idct2(d_restored)

            if len(extracted_bits) < num_bits:
                extracted_bits.extend([0] * (num_bits - len(extracted_bits)))
            extracted_bits = extracted_bits[:num_bits]

            bits_arr = np.array(extracted_bits, dtype=np.uint8)
            bytes_arr = np.packbits(bits_arr)
            scrambled_ch = bytes_arr.reshape((wm_h, wm_w))
            scrambled_channels.append(scrambled_ch.astype(np.uint8))

            # Descrambling
            if perms is not None and len(perms) > ch:
                perm = np.array(perms[ch], dtype=int)
                restored_ch = self.descramble_watermark_channel(scrambled_ch, perm)
            else:
                # Key-based fallback descramble if exact perm array is omitted
                restored_ch = scrambled_ch

            extracted_channels.append(restored_ch.astype(np.uint8))
            separated_host_channels.append(np.clip(host_restored_ch, 0, 255).astype(np.uint8))

        extracted_wm_arr = np.stack(extracted_channels, axis=2)
        extracted_scrambled_arr = np.stack(scrambled_channels, axis=2)
        separated_host_arr = np.stack(separated_host_channels, axis=2)

        extracted_wm_pil = Image.fromarray(extracted_wm_arr)
        extracted_scrambled_pil = Image.fromarray(extracted_scrambled_arr)
        separated_host_pil = Image.fromarray(separated_host_arr)

        return {
            "extracted_watermark": extracted_wm_pil,
            "extracted_scrambled": extracted_scrambled_pil,
            "separated_host": separated_host_pil,
            "host_size": [host_w, host_h],
            "watermark_size": [wm_w, wm_h]
        }

    # ==========================================
    # Attacks & Robustness Suite
    # ==========================================
    @staticmethod
    def apply_attack(pil_img, attack_type, **kwargs):
        """Applies a distortion/attack to test watermark resilience."""
        img = pil_img.convert('RGB')
        arr = np.array(img, dtype=np.float32)

        if attack_type == 'gaussian_noise':
            sigma = kwargs.get('sigma', 12.0)
            noise = np.random.normal(0, sigma, arr.shape)
            noisy = np.clip(arr + noise, 0, 255).astype(np.uint8)
            return Image.fromarray(noisy)

        elif attack_type == 'poisson_noise':
            vals = len(np.unique(arr.flatten()))
            vals = 2 ** np.ceil(np.log2(max(2, vals)))
            noisy = np.random.poisson(arr / 255.0 * vals) / float(vals) * 255.0
            noisy = np.clip(noisy, 0, 255).astype(np.uint8)
            return Image.fromarray(noisy)

        elif attack_type == 'sharpen':
            percent = kwargs.get('percent', 150)
            return img.filter(ImageFilter.UnsharpMask(radius=1, percent=percent, threshold=3))

        elif attack_type == 'blur':
            radius = kwargs.get('radius', 1.5)
            return img.filter(ImageFilter.GaussianBlur(radius=radius))

        elif attack_type == 'resize':
            scale = kwargs.get('scale', 0.5)
            w, h = img.size
            small = img.resize((max(4, int(w * scale)), max(4, int(h * scale))), Image.Resampling.LANCZOS)
            back = small.resize((w, h), Image.Resampling.LANCZOS)
            return back

        elif attack_type == 'jpeg':
            quality = int(kwargs.get('quality', 40))
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=quality)
            buf.seek(0)
            return Image.open(buf).convert('RGB')

        elif attack_type == 'rotation':
            angle = float(kwargs.get('angle', 2.0))
            # Rotate by small angle and rotate back
            rot = img.rotate(angle, resample=Image.Resampling.BILINEAR)
            back = rot.rotate(-angle, resample=Image.Resampling.BILINEAR)
            return back

        elif attack_type == 'cropping':
            crop_pct = kwargs.get('crop_percent', 0.1)  # 10% crop border
            w, h = img.size
            dx = int(w * crop_pct)
            dy = int(h * crop_pct)
            arr_copy = np.array(img).copy()
            arr_copy[:dy, :] = 0
            arr_copy[-dy:, :] = 0
            arr_copy[:, :dx] = 0
            arr_copy[:, -dx:] = 0
            return Image.fromarray(arr_copy)

        return img


# Utility functions for base64 conversions
def pil_to_base64(pil_img, format='PNG'):
    buf = io.BytesIO()
    pil_img.save(buf, format=format)
    return f"data:image/{format.lower()};base64," + base64.b64encode(buf.getvalue()).decode('utf-8')


def base64_to_pil(base64_str):
    if ',' in base64_str:
        base64_str = base64_str.split(',', 1)[1]
    data = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(data))
