import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

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

# Ruta de la imagen
ruta_imagen = "./imgs/1005.jpg"

# Abrir la imagen con PIL
imagen = Image.open(ruta_imagen)

# Convertir la imagen a arreglo de numpy
datos_numericos_de_imagen = np.asarray(imagen)

# --- Convertir a YUV ---
imagen_yuv = rgb_a_yuv(datos_numericos_de_imagen)
# --- Convertir a HSV ---
imagen_hsv = rgb_a_hsv(datos_numericos_de_imagen)

# --- Mostrar solo el canal H ---
plt.imshow(imagen_hsv[:, :, 0], cmap='gray')
plt.title("Canal H (Hue)")
#plt.axis('off')
plt.show()
"""
# Dependiendo de la implementación, el canal Y puede estar 
# en la primera posición (índice 0 para Y) o en la segunda posición 
# (índice 1 para U) o en la tercera posición (índice 2 para V).
plt.imshow(imagen_yuv[:, :, 0], cmap='gray')
plt.title("Canal Y (luminancia)")
#plt.axis('off')
plt.show()"""