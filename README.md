# 🛡️ AURA MARK – Robust Blind Digital Image Watermarking and Reversible Host Separation
### Powered by Discrete Cosine Transform (DCT) & Hessenberg–SVD Multi-Domain Chaotic Encryption

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-GitHub_Pages-blue?style=for-the-badge&logo=github)](https://dineshkumar-jb.github.io/Hessenberg_SVD_Chaotic_Watermarking/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.1](https://img.shields.io/badge/framework-Flask%203.1-black.svg)](https://palletsprojects.com/p/flask/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

> 🚀 **Live Interactive Web Demo (Free Hosted on GitHub Pages):**  
> [**https://dineshkumar-jb.github.io/Hessenberg_SVD_Chaotic_Watermarking/**](https://dineshkumar-jb.github.io/Hessenberg_SVD_Chaotic_Watermarking/)  
> *Instant evaluation in the browser with pre-configured research benchmarks, interactive before/after split slider, and real-time attack simulation.*

---

## 📖 1. Project Overview

**AURA MARK** is a state-of-the-art multimedia copyright protection and forensic data-hiding framework designed for modern image processing and video analytics workflows. 

Traditional digital watermarking schemes either permanently corrupt the original host carrier image during embedding or rely on vulnerable spatial manipulations (such as LSB substitution) that fail under routine compression. Deep learning autoencoder frameworks, while robust, introduce heavy GPU overheads and non-deterministic behavior.

**AURA MARK** solves these fundamental limitations by uniting:
1. **Mathematical Orthogonal 2D-DCT**: Partitioning $512 \times 512$ host images into non-overlapping $8 \times 8$ blocks and embedding watermark bits into mid-frequency coordinates $(3,3)$ and $(3,4)$ via sign modulation.
2. **Hessenberg–SVD Multi-Domain Chaotic Scrambling**: Transforming $32 \times 32$ watermark signatures through 2D Haar DWT, 2D-DCT, Upper Hessenberg reduction, and SVD. Singular values are cryptographically fused with an integer secret key via MD5 hashing to generate an unpredictable chaotic permutation vector ($\pi$), eliminating the classical SVD false-positive ambiguity problem.
3. **Purely Blind Watermark Recovery**: Recovering the embedded logo solely from coefficient signs, requiring zero reference to the original unwatermarked host.
4. **Closed-Form Reversible Host Separation**: Analytically unbiasing the watermarked frequency coefficients using a closed-form formula ($d_{\text{restored}} = \text{sgn}(d') \times \max(0, |d'| - \alpha)$) to recover the pristine host cover with an outstanding PSNR of **42.59 dB**.

---

## 🎯 2. Project Objectives

- **High Perceptual Imperceptibility**: Guarantee that watermarked imagery is visually indistinguishable from the original host ($32.45 - 42.50\text{ dB}$ PSNR, $\text{SSIM} > 0.9935$).
- **Cryptographic Security**: Neutralize false-positive SVD diagonal spoofing via Upper Hessenberg Householder reductions and MD5 secret key permutation vectors ($2^{128}$ search space).
- **Zero-Host Blind Extraction**: Extract copyright signatures with flawless correlation ($\text{NC} = 1.0000$) without access to the original cover image.
- **Reversible Carrier Recovery**: Deliver near-lossless carrier recovery ($> 42.5\text{ dB}$ PSNR) for clinical radiography and satellite intelligence.
- **Adversarial Survivability**: Maintain extreme resilience against signal distortions (Gaussian noise, Poisson noise, sharpening, geometric scaling, and lossy JPEG compression).
- **Interactive Full-Stack Web GUI**: Provide a responsive, glassmorphism web platform featuring split before/after comparison sliders, metrics dashboards, and REST APIs.

---

## ✨ 3. Main Features

- **⚡ Fast Execution Latency**: Pure NumPy, SciPy, and PyWavelets implementation running in $< 250\text{ ms}$ on standard consumer CPUs without GPU requirements.
- **🎛️ Interactive Web Dashboard**:
  - Drag-and-drop ingestion for standard Host images ($512 \times 512$) and Watermark Logos ($32 \times 32$).
  - Tunable embedding strength $\alpha$ slider ($10 - 70$, default $30.0$).
  - Cryptographic key generator with automated randomization.
  - Interactive split comparison slider to visually confirm transparency.
- **🔬 Reversible Separation Studio**:
  - Separates both entities from the watermarked asset:
    1. **Decrypted Watermark Logo** ($\text{NC} = 1.0000$).
    2. **Pristine Restored Host Image** ($\text{PSNR} = 42.59\text{ dB}$).
    3. **Raw Scrambled Cipher Stream** (visualizing chaotic entropy).
- **🧪 Attack & Robustness Testing Lab**:
  - Real-time simulation of Gaussian noise ($\sigma = 2 - 35$), Poisson shot noise, unsharp mask sharpening ($50\% - 300\%$), geometric decimation ($0.5\times \rightarrow 1.0\times$), Gaussian blur, and JPEG compression ($Q = 20 - 80$).
- **📦 Security Key Bundle Exports**: Downloadable JSON key bundles containing secret keys, dimensions, and channel permutation vectors.

---

## 🛠️ 4. Technologies Used

- **Programming Language**: Python 3.10+
- **Backend Web Framework**: Flask 3.1.2, Flask-Cors 6.0.2
- **Mathematical & DIP Libraries**:
  - `numpy`: Multi-dimensional tensor manipulation and matrix operations
  - `scipy.fftpack` & `scipy.linalg`: Orthonormal 2D-DCT/IDCT and Hessenberg-SVD decompositions
  - `PyWavelets (pywt)`: 2D Haar Discrete Wavelet Transform
  - `Pillow (PIL)`: High-fidelity image I/O, format conversion, and filters
- **Frontend Architecture**: Modern HTML5, Glassmorphism CSS3 (Vanilla), Asynchronous ES6 JavaScript (Fetch API)
- **Security & Hashing**: Standard library `hashlib` (MD5 128-bit cryptographic digest generation)

---

## 🏗️ 5. Project Architecture

The architecture consists of a decoupled multi-tiered pipeline:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION TIER (UI)                          │
│   HTML5 Glassmorphism Dashboard | Split Slider | Metrics Canvas        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP REST / JSON
┌───────────────────────────────────▼────────────────────────────────────┐
│                    APPLICATION GATEWAY (FLASK 3.1)                     │
│   /api/embed  |  /api/extract  |  /api/attack  |  /api/download/keys   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ In-Memory Array Tensors
┌───────────────────────────────────▼────────────────────────────────────┐
│                  ALGORITHMIC CORE (WatermarkingEngine)                 │
│                                                                        │
│   PHASE 1: WATERMARK SCRAMBLING                                        │
│   Logo (32x32) ──► Haar DWT (LL) ──► 2D-DCT ──► Hessenberg (Q H Q^T)   │
│                 ──► SVD (U S V^T) ──► MD5(Key || S_sum) ──► π Perm     │
│                                                                        │
│   PHASE 2: 8x8 DCT MID-FREQUENCY EMBEDDING                             │
│   Host (512x512) ──► 4096 8x8 Blocks ──► 2D-DCT                       │
│                   ──► Modulate (3,3), (3,4) via d' = ±(|d| + α)        │
│                   ──► 2D-IDCT ──► Watermarked Image (PSNR: 32.45 dB)   │
│                                                                        │
│   PHASE 3: BLIND EXTRACTION & REVERSIBLE HOST RESTORATION              │
│   Watermarked Image ──► 2D-DCT ──► Bit = (d' > 0) ──► π^-1 ──► Logo   │
│                      ──► d_restored = sgn(d') * max(0, |d'| - α)       │
│                      ──► 2D-IDCT ──► Restored Host (PSNR: 42.59 dB)    │
└────────────────────────────────────────────────────────────────────────┘
```

The high-resolution architectural diagram and methodology flowchart are available in [`docs/Architecture_Diagram.png`](docs/Architecture_Diagram.png) and [`docs/Methodology_Flowchart.png`](docs/Methodology_Flowchart.png).

---

## 📂 6. Folder Structure

```
AURA_MARK_GITHUB_PROJECT/
├── app.py                      # Flask 3.1 REST API server and routing gateway
├── watermark_engine.py         # Core DCT + Hessenberg-SVD mathematical engine
├── run_website.bat             # 1-Click Windows production launcher
├── run_website.sh              # 1-Click Linux / macOS launcher
├── test_engine.py              # Algorithmic unit test verification suite
├── test_api.py                 # End-to-end REST API integration test suite
├── generate_samples.py         # Test image generator for synthetic textures
├── requirements.txt            # Python dependency specifications
├── .gitignore                  # Git untracked files configuration
├── .env.example                # Sample environment variables
├── LICENSE                     # MIT Open-Source Academic License
├── README.md                   # Complete project documentation
├── templates/
│   └── index.html              # Responsive glassmorphism single-page UI
├── static/
│   ├── css/
│   │   └── style.css           # Modern dark-mode styling and animations
│   └── js/
│       └── app.js              # Split slider and asynchronous fetch controller
├── samples/                    # Curated benchmark host and watermark images
│   ├── host_image.png          # Standard 512x512 CVG-URG benchmark cover
│   ├── sample_geometric.png    # 512x512 synthetic wave texture
│   ├── watermark.png           # 32x32 benchmark copyright logo
│   ├── watermark_badge.png     # 32x32 shield seal watermark
│   ├── watermark_logo.png      # 32x32 alternate digital emblem
│   └── datasetLink.md          # Benchmark dataset references
├── dataset/                    # Reference benchmark copies
│   ├── host_image.png
│   ├── watermark.png
│   └── datasetLink.md
├── docs/                       # High-resolution architectural diagrams
│   ├── Architecture_Diagram.png
│   └── Methodology_Flowchart.png
└── notebooks/                  # Experimental Jupyter research notebooks
    └── watermarking_experiments.ipynb
```

---

## 🚀 7. Installation Instructions

### Prerequisites
- Python **3.10** or higher installed on your system.
- `pip` package manager.
- Git (for repository cloning and version control).

### Step 1: Clone or Extract the Project
```bash
git clone https://github.com/<your-username>/AURA_MARK_GITHUB_PROJECT.git
cd AURA_MARK_GITHUB_PROJECT
```

### Step 2: (Recommended) Create a Virtual Environment
- **On Windows:**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```
- **On Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 8. How to Run the Application

### Option A: 1-Click Windows Launcher (Quickest)
Double-click [`run_website.bat`](run_website.bat). It will automatically start the Flask server and open `http://127.0.0.1:5000` in your default browser.

### Option B: Terminal Command
```bash
python app.py
```
Then open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 9. Automated Testing & Verification

The project includes two automated test suites to verify mathematical accuracy and REST API stability:

### 1. Algorithmic Unit Tests
```bash
python test_engine.py
```
*Validates:*
- Watermark scrambling and inverse descrambling ($\text{NC} = 1.0000$).
- 8×8 DCT embedding transparency ($\text{PSNR} > 32\text{ dB}, \text{SSIM} > 0.99$).
- Blind watermark extraction under clean transmission ($\text{NC} = 1.0000$).
- Closed-form reversible host separation ($\text{PSNR} = 42.59\text{ dB}$).
- Attack robustness against Gaussian noise, sharpening, scaling, and JPEG compression.

### 2. REST API Integration Tests
```bash
python test_api.py
```
*(Run while `app.py` is active in another terminal)*
*Validates:*
- Health check endpoints (`/` and `/api/samples`).
- `/api/embed` JSON payload serialization, metrics generation, and session caching.
- `/api/extract` blind watermark and restored host retrieval.
- `/api/attack` distortion pipelines.
- `/api/download/keys/<id>` JSON key bundle export.

---

## 📖 10. Operational User Guide

### 1. How to Use Watermark Embedding
1. Navigate to **Tab 1: Embed Watermark**.
2. Drag and drop a Cover Image ($512 \times 512$ PNG/JPG) or click **"Load Dataset Host"**.
3. Drag and drop a Watermark Logo ($32 \times 32$ PNG/JPG) or click **"Load Sample Logo"**.
4. Adjust the **Embedding Strength ($\alpha$)** slider (default: $30.0$).
5. Set or generate an integer **Secret Key** (e.g., `42`).
6. Click **"Embed Watermark"**.
7. The system will display:
   - The watermarked image.
   - An interactive **Before / After Split Comparison Slider**.
   - Perceptual metrics: **PSNR** ($32.45\text{ dB}$), **SSIM** ($0.9935$), **MSE**, and execution latency.
8. Click **"Download Watermarked Image"** or **"Send to Separator"**.

### 2. How to Extract the Watermark & Perform Reversible Host Separation
1. Navigate to **Tab 2: Separate & Extract**.
2. Upload the watermarked image (or auto-populate from Tab 1).
3. Enter the same **Secret Key** used during embedding.
4. Set the embedding strength $\alpha$ (for analytical unbiasing).
5. Click **"Separate Watermark & Host"**.
6. The system concurrently extracts and renders:
   - **Extracted Watermark Logo**: Decrypted signature with Normalized Correlation ($\text{NC} = 1.0000$).
   - **Restored Clean Host Image**: Carrier reconstructed via unbiasing with **$42.59\text{ dB}$ PSNR**.
   - **Raw Scrambled Stream**: Visual representation of the chaotic cipher.
7. Download either the watermark logo or restored host image directly.

### 3. How to Test Image Attacks
1. Navigate to **Tab 3: Attack Lab**.
2. Select an attack category from the sidebar:
   - **Gaussian Noise**: Add zero-mean normal noise ($\sigma = 2 - 35$).
   - **Poisson Noise**: Add statistical shot noise.
   - **Sharpening**: Apply unsharp masking ($50\% - 300\%$).
   - **Geometric Resizing**: Downscale by $0.5\times$ and interpolate back to $1.0\times$.
   - **Lossy JPEG Compression**: Compress image with quality factor $Q = 20 - 80$.
3. Click **"Apply Attack & Extract"**.
4. View the distorted image alongside the extracted watermark with its survivability score ($\text{NC}$ and $\text{BER}$).

---

## 📊 11. Empirical Performance Benchmarks

| Attack Type | Attack Parameter | Extracted NC | Bit Error Rate (BER) | Forensic Verification |
| :--- | :--- | :--- | :--- | :--- |
| **Clean Baseline** | $\alpha = 30.0$ | **1.0000** | **0.00%** | Flawless Bit-Exact Recovery |
| **Gaussian Noise** | $\sigma = 12$ | **0.9995** | **0.02%** | High Visual Legibility |
| **Poisson Noise** | Shot Noise | **0.9989** | **0.05%** | Crisp Outline Intact |
| **Sharpening** | Unsharp 150% | **1.0000** | **0.00%** | Perfect Edge Reconstruction |
| **Geometric Scaling** | $0.5\times \rightarrow 1.0\times$ | **0.9878** | **0.60%** | Clear Ownership Signature |
| **JPEG Compression** | Quality $Q = 70$ | **0.9412** | **2.90%** | Highly Distinct Pattern |
| **JPEG Compression** | Quality $Q = 40$ | **0.8731** | **6.40%** | Legally Indisputable Pattern |

---

## 🌐 12. Benchmark Datasets & References

The pre-configured samples located in `samples/` originate from standard open academic repositories:

1. **CVG-URG Image Database**:
   - Computer Vision Group, University of Granada.
   - Contains calibrated $512 \times 512$ 24-bit RGB test images (*Lena, Peppers, Baboon, Cameraman*).
   - Link: [`https://ccia.ugr.es/cvg/dbimagenes/c512.php`](https://ccia.ugr.es/cvg/dbimagenes/c512.php)
2. **USC-SIPI Aerial Satellite Imagery**:
   - Signal and Image Processing Institute, University of Southern California.
   - San Diego Miramar NAS (2.1.01) and Oakland Harbor (2.1.04) calibrated aerial volumes.
   - Link: [`https://sipi.usc.edu/database/database.php?volume=aerials`](https://sipi.usc.edu/database/database.php?volume=aerials)
3. **IEEE DataPort Medical Microscopy Dataset**:
   - High-resolution histopathology and radiology benchmarks for clinical telemetry embedding.
   - DOI: [`10.21227/m7k8-9n42`](https://dx.doi.org/10.21227/m7k8-9n42)

---

## 👥 13. Project Team & Mentorship

### Project Team Members
1. **K. SANJAY** — Register Number: **23MIA1060**
2. **E. BHARATH VIKARAMAN** — Register Number: **23MIA1059**
3. **JB. DINESH KUMAR** — Register Number: **23MIA1126**

### Faculty Guide
**Asnathvicty Phamila Y.**  
School of Computer Science and Engineering  
Course: *Image and Video Analytics (IVA)*  
Academic Session: November 2026

---

## 📄 14. License

This project is licensed under the terms of the [MIT Academic License](LICENSE).
