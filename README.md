<h1>BoneVision DX-Ray</h1>
  <p><b>Advanced Dual-Energy X-Ray Material Decomposition & Visualization Simulation</b></p>
  
![Application Overview](https://github.com/user-attachments/assets/ff2425e3-497d-476d-871f-a8859cf677e3)

## Demo 

https://github.com/user-attachments/assets/31cce0be-7b53-4689-9c1b-8fae2ceaed53



  <p>
    <a href="#overview">Overview</a> •
    <a href="#features">Features</a> •
    <a href="#physics-foundation">Physics</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#installation">Installation</a> •
    <a href="#credits">Credits</a>
  </p>
</div>

---

## Overview

In standard single-energy radiography, all tissue types are projected onto the same 2D image plane simultaneously. Bone and soft tissue absorb X-rays differently—but a single acquisition collapses both into one measurement, making separation impossible. The result is overlapping structures, reduced diagnostic contrast, and ambiguous material boundaries.

**BoneVision DX-Ray** solves this underdetermined system. By acquiring two images at different energy levels ($e_L$ and $e_H$), we gain a second independent measurement, making the system fully determined. This Python-based PyQt5 desktop application simulates this dual-energy X-ray acquisition and performs mathematical material decomposition to visualize separate, clear **bone** and **soft-tissue** maps.

---

## Key Features

- **Digital Phantom Library:** Generate mathematically defined 512×512 phantoms with zero baseline noise. Choose from three anatomical configurations:
  - **Ribcage:** Spine, ribs, torso with arc-shaped bone features.
  - **Cylinder:** Nested ellipses and concentric bone structures.
  - **Layers:** Planar cross geometry with horizontal/vertical layers.
- **Dual-Energy Acquisition Pipeline:** Simulates Low-E (27–60 keV) and High-E (80–140 keV) projections, following the Beer-Lambert law.
- **Material Decomposition:** Robust matrix-inversion method to isolate bone vs. soft tissue, calculating precise thickness maps.
- **Real-Time Degradation Modeling:** Dynamically inject configurable noise ($\sigma$) and scatter ($\beta$) to test decomposition stability.
- **Live Quantitative Metrics:** Instantly compute Mean Absolute Error (MAE), Contrast-to-Noise Ratio (CNR), Signal-to-Noise Ratio (SNR), and the system's determinant `det(A)`.
- **Interactive Attenuation Chart:** Real-time Matplotlib curves tracking attenuation coefficients $\mu(E)$ across varying energy levels.

---

## Physics Foundation

### The Beer-Lambert Law & Matrix Inversion
Different materials attenuate X-rays at different rates, and that rate changes with energy. Bone has high attenuation at low energies due to the photoelectric effect. 

For a two-material scene (bone + tissue), the system of equations for projection values ($p$) is:
$$p_L = \mu_{BL} \cdot t_B + \mu_{TL} \cdot t_T$$
$$p_H = \mu_{BH} \cdot t_B + \mu_{TH} \cdot t_T$$

Expressed in matrix form $[p_L, p_H]^T = A \cdot [t_B, t_T]^T$, we isolate thickness ($t$) using **Matrix Inversion**:
$$[t_B, t_T]^T = A^{-1} \cdot [p_L, p_H]^T$$

> **The Critical Determinant:** If $det(A) \to 0$ (e.g., when energy separation is too small), matrix inversion amplifies any noise to infinity. Energy separation $\Delta E$ is the single most critical parameter in the pipeline.

---

## Architecture

BoneVision features a strict **MVC Architecture** with 16 modular components and **<50ms pipeline latency**. 

- **Model (`core/`)**: Pure NumPy/SciPy physics, entirely isolated from the UI logic.
  - `physics.py` — Beer-Lambert model & matrix decomposition.
  - `phantom.py` — 512×512 mathematically defined phantoms.
  - `metrics.py` — Quality metric computations.
- **View (`ui/`)**: PyQt5 widget assembly with custom design tokens, colormaps (`colormap.py`), and 8 reusable components.
- **Controller (`controllers/`)**: Single source of state (`main_controller.py`) binding UI signals to core physics.

---

## Quick Start

### Requirements
- Python 3.11+
- macOS (tested) / Linux / Windows

### Installation & Execution

```bash
# Clone the repository
git clone https://github.com/YassienTawfikk/BoneVision-DX-ray.git
cd BoneVision-DX-ray

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## Evaluation Scenarios

The system has been rigorously tested against 4 key degradation scenarios:
1. **Clean Baseline:** Perfect conditions with $\Delta E = 60$ keV. $MAE = 0.000$, showing exact recovery.
2. **Reduced Energy Separation:** $\Delta E = 20$ keV. $det(A)$ collapses, making the matrix near-singular and amplifying noise.
3. **Noisy Acquisition:** Noise ($\sigma$) is scaled by the inverse matrix, severely degrading tissue maps without pre-denoising.
4. **Noise + Scatter:** Scatter ($\beta$) adds a low-frequency bias distinct from noise, revealing a separate mechanism that requires distinct correction strategies.

---

## Contributors

<div>
    <table align="center">
        <tr>
            <td align="center">
                <a href="https://github.com/YassienTawfikk" target="_blank">
                    <img src="https://avatars.githubusercontent.com/u/126521373?v=4" width="150px;"
                         alt="Yassien Tawfik"/>
                    <br/>
                    <sub><b>Yassien Tawfik</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/Seiftaha" target="_blank">
                    <img src="https://avatars.githubusercontent.com/u/127027353?v=4" width="150px;" alt="Seif Taha"/>
                    <br/>
                    <sub><b>Seif Taha</b></sub>
                </a>
            </td>         
            <td align="center">
                <a href="https://github.com/Mazenmarwan023" target="_blank">
                    <img src="https://avatars.githubusercontent.com/u/127551364?v=4" width="150px;" alt="Mazen Marwan"/>
                    <br/>
                    <sub><b>Mazen Marwan</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/mohamedddyasserr" target="_blank">
                    <img src="https://avatars.githubusercontent.com/u/126451832?v=4" width="150px;"
                         alt="Mohamed Yasser"/>
                    <br/>
                    <sub><b>Mohamed Yasser</b></sub>
                </a>
            </td>
              </td>
           <td align="center">
              <a href="https://github.com/yousseftaha167" target="_blank">
                <img src="https://avatars.githubusercontent.com/u/128304243?v=4" width="150px;" alt="Youssef Taha"/>
                <br/>
                <sub><b>Youssef Taha</b></sub>
              </a>
            </td>
        </tr>
    </table>
