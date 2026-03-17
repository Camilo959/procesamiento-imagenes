import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from utils.conversiones_color import convolucion, rgb_a_hsv_only_value

# Ruta de la imagen
ruta_imagen = "./imgs/1003.jpg"

# Abrir la imagen con PIL
imagen = Image.open(ruta_imagen)

# Convertir la imagen a arreglo de numpy
datos_numericos_de_imagen = np.asarray(imagen)

kernel = [[1/9, 1/9, 1/9],
          [1/9, 1/9, 1/9],
          [1/9, 1/9, 1/9]]

def calcular_histograma(imagen):
  histograma = []
  xticks = []
  for i in range(256):
    xticks.append(i)
    histograma.append(np.count_nonzero(imagen == i))

  return histograma, xticks

# --- Convertir a HSV ---
imagen_hsv = rgb_a_hsv_only_value(datos_numericos_de_imagen)

# =================================================================
# CONCLUSIÓN: Se seleccionó el canal V del espacio HSV
# Razón: Mostró una representación más limpia del contraste entre
# los insectos oscuros y el fondo brillante, reduciendo la visibilidad
# de residuos presentes en la superficie de la trampa
# =================================================================

# Extraer canal V (valor/brillo)
canal_v = imagen_hsv[:, :]  # Canal V del espacio HSV para procesamiento
canal_b = datos_numericos_de_imagen[:, :, 2]  # Canal B del espacio RGB para comparación

imagen_filtrada = convolucion(canal_v, kernel)

imagen_filtrada = np.array(imagen_filtrada)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(canal_v, cmap='gray')
plt.title("Canal V (original)")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(imagen_filtrada, cmap='gray')
plt.title("Canal V con filtro aplicado")
plt.axis("off")

plt.tight_layout()
plt.show()

# Mostrar histograma
#histograma_v, xticks_v = calcular_histograma(canal_v)
#plt.bar(xticks_v, histograma_v)
#plt.show()

#V = imagen_hsv[:, :, 2]
#
#plt.hist(V.flatten(), bins=100)
#plt.title("Histograma del canal V (HSV)")
#plt.xlabel("Valor de brillo")
#plt.ylabel("Cantidad de píxeles")
#plt.show()

# Mostrar canal V
#plt.figure(figsize=(10, 8))
#plt.imshow(canal_v, cmap='gray')
#plt.title("Canal V (Valor/Brillo) - Espacio de Color HSV", fontsize=14, fontweight='bold')
#plt.colorbar(label='Intensidad')
#plt.axis('off')
#plt.tight_layout()
#plt.show()