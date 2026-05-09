import numpy as np
from scipy.ndimage import gaussian_filter


class PhysicsModel:
    @staticmethod
    def mu(E, mat_type):
        x = E / 50.0
        if mat_type == 'bone':
            return 1.8 * (x ** -3) + 0.22 * (x ** -0.5)
        else:
            return 0.38 * (x ** -3) + 0.185 * (x ** -0.5)

    @classmethod
    def simulate_projection(cls, phantom, E, noise_sigma, scatter, base_sz=512):
        bone = phantom['bone']
        tissue = phantom['tissue']
        muB = cls.mu(E, 'bone')
        muT = cls.mu(E, 'tissue')

        proj = muB * bone + muT * tissue

        if scatter > 0.002:
            blr = gaussian_filter(proj, sigma=8 * (base_sz / 128.0))
            proj += scatter * blr

        if noise_sigma > 0.001:
            seed = 12345 + int(round(E * 1000))
            rng = np.random.default_rng(seed)
            noise = rng.normal(0, noise_sigma, proj.shape).astype(np.float32)
            proj += noise

        return proj

    @classmethod
    def decompose(cls, pL, pH, eL, eH):
        muBL = cls.mu(eL, 'bone')
        muTL = cls.mu(eL, 'tissue')
        muBH = cls.mu(eH, 'bone')
        muTH = cls.mu(eH, 'tissue')

        det = muBL * muTH - muTL * muBH

        pL = np.asarray(pL, dtype=np.float32)
        pH = np.asarray(pH, dtype=np.float32)

        eps = 1e-8

        # If energies are equal or determinant is too close to zero,
        # dual-energy decomposition is not valid.
        if abs(det) < eps:
            boneMap = np.zeros_like(pL, dtype=np.float32)
            tissueMap = np.zeros_like(pL, dtype=np.float32)
        else:
            boneMap = (muTH * pL - muTL * pH) / det
            tissueMap = (-muBH * pL + muBL * pH) / det

            boneMap = np.nan_to_num(boneMap, nan=0.0, posinf=0.0, neginf=0.0)
            tissueMap = np.nan_to_num(tissueMap, nan=0.0, posinf=0.0, neginf=0.0)

            boneMap = np.maximum(0, boneMap).astype(np.float32)
            tissueMap = np.maximum(0, tissueMap).astype(np.float32)

        return {
            'boneMap': boneMap,
            'tissueMap': tissueMap,
            'muBL': muBL,
            'muTL': muTL,
            'muBH': muBH,
            'muTH': muTH,
            'det': det
        }
