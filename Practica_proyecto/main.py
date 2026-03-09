import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from utils.conversiones_color import rgb_a_yuv, rgb_a_hsv

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