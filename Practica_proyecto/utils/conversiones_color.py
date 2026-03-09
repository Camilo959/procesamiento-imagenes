import numpy as np


def rgb_a_yuv(img):
    matriz_conversion = np.array([
        [0.299, 0.587, 0.114],
        [-0.14713, -0.28886, 0.436],
        [0.615, -0.51499, -0.10001]
    ])

    img = img.astype(float) / 255.0
    return np.dot(img, matriz_conversion.T)


def rgb_a_hsv(img):
    """
    Convierte una imagen RGB (0-255) a HSV (H,S,V) usando NumPy.
    H: 0-360, S: 0-1, V: 0-1
    """
    img = img.astype(float) / 255.0  # Normalizar a 0-1
    R = img[..., 0]
    G = img[..., 1]
    B = img[..., 2]

    Cmax = np.maximum(np.maximum(R, G), B)
    Cmin = np.minimum(np.minimum(R, G), B)
    delta = Cmax - Cmin

    # --- HUE ---
    H = np.zeros_like(Cmax)
    mask = delta != 0  # evitar división por cero
    # R es máximo
    idx = (Cmax == R) & mask
    H[idx] = 60 * ((G[idx] - B[idx]) / delta[idx]) % 360
    # G es máximo
    idx = (Cmax == G) & mask
    H[idx] = 60 * ((B[idx] - R[idx]) / delta[idx] + 2)
    # B es máximo
    idx = (Cmax == B) & mask
    H[idx] = 60 * ((R[idx] - G[idx]) / delta[idx] + 4)

    # --- SATURATION ---
    S = np.zeros_like(Cmax)
    S[Cmax != 0] = delta[Cmax != 0] / Cmax[Cmax != 0]

    # --- VALUE ---
    V = Cmax

    hsv = np.stack((H, S, V), axis=2)
    return hsv
