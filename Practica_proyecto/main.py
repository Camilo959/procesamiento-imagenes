import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from utils.conversiones_color import rgb_a_yuv

# Ruta de la imagen
ruta_imagen = "./imgs/1000.jpg"

# Abrir la imagen con PIL
imagen = Image.open(ruta_imagen)

# Convertir la imagen a arreglo de numpy
datos_numericos_de_imagen = np.asarray(imagen)

# --- Convertir a YUV ---
imagen_yuv = rgb_a_yuv(datos_numericos_de_imagen)

# =================================================================
# CONCLUSIÓN: Se seleccionó el canal Y del espacio YUV
# Razón: Representa la luminancia y permite separar insectos oscuros
# del fondo brillante de la trampa amarilla
# =================================================================

# Extraer canal Y (luminancia)
canal_y = imagen_yuv[:, :, 0]

# Mostrar canal Y
plt.figure(figsize=(10, 8))
plt.imshow(canal_y, cmap='gray')
plt.title("Canal Y (Luminancia) - Espacio de Color YUV", fontsize=14, fontweight='bold')
plt.colorbar(label='Intensidad')
plt.axis('off')
plt.tight_layout()
plt.show()