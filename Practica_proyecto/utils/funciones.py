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

def rgb_a_hsv_solo_value(img):
    img = img.astype(float) / 255.0  # Normalizar a 0-1
    R = img[..., 0]
    G = img[..., 1]
    B = img[..., 2]

    Cmax = np.maximum(np.maximum(R, G), B)
    return Cmax


def convolucion(I, k):
    I = np.array(I)
    k = np.array(k)

    m, n = I.shape
    c, d = k.shape

    salida = np.zeros((m-c+1, n-d+1))

    for i in range(m-c+1):
        for j in range(n-d+1):
            region = I[i:i+c, j:j+d]
            salida[i, j] = np.sum(region * k)

    return salida


def convolucion_separable(I, factor):
    I = np.array(I, dtype=float)

    m, n = I.shape

    # Paso 1: convolución horizontal
    temp = np.zeros((m, n-2))
    for i in range(m):
        for j in range(n-2):
            temp[i, j] = (I[i, j] + I[i, j+1] + I[i, j+2]) * factor

    # Paso 2: convolución vertical
    salida = np.zeros((m-2, n-2))
    for i in range(m-2):
        for j in range(n-2):
            salida[i, j] = (temp[i, j] + temp[i+1, j] + temp[i+2, j]) * factor

    return salida


# Calcular el histograma de la imagen original 
# solo para el canal V del espacio HSV
def calcular_histograma(imagen):
  if imagen.dtype == np.uint8:
    imagen_u8 = imagen
  else:
    imagen_u8 = (np.clip(imagen, 0, 1) * 255).astype(np.uint8)

  histograma = np.bincount(imagen_u8.ravel(), minlength=256).tolist()
  xticks = list(range(256))
  return histograma, xticks


def otsu(imagen):
  histograma, _ = calcular_histograma(imagen)

  maxima_varianza = 0.0
  valor_intensidad_de_la_maxima_varianza = 0

  numero_de_pixeles = np.sum(histograma)
  suma_intensidades_toda_imagen = np.sum(np.arange(256) * np.array(histograma))

  n1 = 0
  s1 = 0

  for valor_intensidad in range(0, 256):
    frecuencia = histograma[valor_intensidad]
    if frecuencia == 0:
        continue

    n1 += frecuencia
    s1 += valor_intensidad * frecuencia

    n2 = numero_de_pixeles - n1
    if n1 == 0 or n2 == 0:
        continue

    m1 = s1 / n1
    s2 = suma_intensidades_toda_imagen - s1
    m2 = s2 / n2

    varianza = n1 * n2 * ((m1 - m2) ** 2)
    if varianza > maxima_varianza:
        maxima_varianza = varianza
        valor_intensidad_de_la_maxima_varianza = valor_intensidad

    return valor_intensidad_de_la_maxima_varianza


# Recorta la región de interés (ROI) de la imagen, 
# eliminando las partes superior e inferior manualmente
def recortar_roi(imagen):
    alto, ancho = imagen.shape[:2]

    # Valores del 12% al 88% para recortar la parte superior e inferior
    top = int(alto * 0.12)
    bottom = int(alto * 0.88)

    return imagen[top:bottom, :]