import numpy as np
import matplotlib.pyplot as plt
import argparse
from PIL import Image
from utils.conversiones_color import convolucion, rgb_a_hsv_only_value

# Ruta de la imagen
ruta_imagen = "./imgs/1003.jpg"

# Abrir la imagen con PIL
imagen = Image.open(ruta_imagen)

# Convertir la imagen a arreglo de numpy
datos_numericos_de_imagen = np.asarray(imagen)

kernel = [[1 / 9, 1 / 9, 1 / 9],
          [1 / 9, 1 / 9, 1 / 9],
          [1 / 9, 1 / 9, 1 / 9]]

# Calcular el histograma de la imagen original 
# solo para el canal V del espacio HSV
def calcular_histograma(imagen):
  imagen = (imagen * 255).astype(np.uint8)
  histograma = []
  xticks = []
  for i in range(256):
    xticks.append(i)
    histograma.append(np.count_nonzero(imagen == i))

  return histograma, xticks


def mostrar_comparacion_filtro(canal):
  imagen_filtrada = convolucion(canal, kernel)
  imagen_filtrada = np.array(imagen_filtrada)

  plt.figure(figsize=(12, 6))

  plt.subplot(1, 2, 1)
  plt.imshow(canal, cmap='gray')
  plt.title("Canal V (original)")
  plt.axis("off")

  plt.subplot(1, 2, 2)
  plt.imshow(imagen_filtrada, cmap='gray')
  plt.title("Canal V con filtro aplicado")
  plt.axis("off")

  plt.tight_layout()
  plt.show()


def mostrar_histograma(canal_v):
  histograma_v, xticks_v = calcular_histograma(canal_v)
  plt.bar(xticks_v, histograma_v)
  plt.title("Histograma del canal V (HSV)")
  plt.xlabel("Valor de brillo")
  plt.ylabel("Cantidad de pixeles")
  plt.show()


def mostrar_canal_v(canal_v):
  plt.figure(figsize=(10, 8))
  plt.imshow(canal_v, cmap='gray')
  plt.title("Canal V (Valor/Brillo) - Espacio de Color HSV", fontsize=14, fontweight='bold')
  plt.colorbar(label='Intensidad')
  plt.axis('off')
  plt.tight_layout()
  plt.show()


def obtener_argumentos():
  parser = argparse.ArgumentParser(
      description="Ejecuta una visualizacion del procesamiento sin editar el codigo"
  )
  parser.add_argument(
      "--accion",
      choices=["histograma", "comparar", "canal_v", "todo"],
      default="histograma",
      help="Selecciona que salida mostrar"
  )
  return parser.parse_args()


def main():
  args = obtener_argumentos()

# --- Convertir a HSV ---
  imagen_hsv_onyly_v = rgb_a_hsv_only_value(datos_numericos_de_imagen)

# =================================================================
# CONCLUSIÓN: Se seleccionó el canal V del espacio HSV
# Razón: Mostró una representación más limpia del contraste entre
# los insectos oscuros y el fondo brillante, reduciendo la visibilidad
# de residuos presentes en la superficie de la trampa
# =================================================================

# Extraer canal V (valor/brillo)
  canal_v = imagen_hsv_onyly_v[:, :, 2]  # Canal V del espacio HSV para procesamiento

  if args.accion == "histograma":
    mostrar_histograma(canal_v)
  elif args.accion == "comparar":
    mostrar_comparacion_filtro(canal_v)
  elif args.accion == "canal_v":
    mostrar_canal_v(canal_v)
  elif args.accion == "todo":
    mostrar_histograma(canal_v)
    mostrar_comparacion_filtro(canal_v)
    mostrar_canal_v(canal_v)


if __name__ == "__main__":
  main()