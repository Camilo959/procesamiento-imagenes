import numpy as np
import matplotlib.pyplot as plt
import argparse
from PIL import Image
from utils.funciones import convolucion, rgb_a_hsv_solo_value, convolucion_separable, otsu, recortar_roi



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


def mostrar_comparacion_filtro(canal):
  imagen_filtrada = convolucion_separable(canal, 1/9)
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


def mostrar_filtro_convolucion(canal_v):
  imagen_filtrada = convolucion_separable(canal_v, 1/9)
  plt.figure(figsize=(10, 8))
  plt.imshow(imagen_filtrada, cmap='gray')
  plt.title("Canal V con filtro de convolución aplicado", fontsize=14, fontweight='bold')
  plt.colorbar(label='Intensidad')
  plt.axis('off')
  plt.tight_layout()
  plt.show()


def mostrar_binaria_umbral_181(canal_v):
  canal_v_255 = (np.clip(canal_v, 0, 1) * 255).astype(np.uint8)

  # <= 181 -> 0, > 181 -> 255
  imagen_binaria_255 = np.where(canal_v_255 <= 181, 0, 255).astype(np.uint8)

  # Versión normalizada equivalente (0 y 1)
  imagen_binaria_01 = (imagen_binaria_255 > 0).astype(np.uint8)

  plt.figure(figsize=(10, 8))
  plt.imshow(imagen_binaria_255, cmap='gray', vmin=0, vmax=255)
  plt.title("Binaria umbral=181 (0 y 255)", fontsize=14, fontweight='bold')
  plt.colorbar(label='Intensidad')
  plt.axis('off')
  plt.tight_layout()
  plt.show()

  print("Imagen binaria generada.")
  print("Regla aplicada: <= 181 -> 0, > 181 -> 255")
  print(f"Valores unicos (0/255): {np.unique(imagen_binaria_255)}")
  print(f"Valores unicos normalizados (0/1): {np.unique(imagen_binaria_01)}")


def obtener_argumentos():
  parser = argparse.ArgumentParser(
      description="Ejecuta una visualizacion del procesamiento sin editar el codigo"
  )
  parser.add_argument(
      "--accion",
      choices=["histograma", "comparar", "canal_v", "todo", "filtro_convolucion", "umbral_otsu", "binaria_181"],
      default="histograma",
      help="Selecciona que salida mostrar"
  )
  return parser.parse_args()


def main():

  args = obtener_argumentos()

    # Ruta de la imagen
  ruta_imagen = "./imgs/1004.jpg"

  # Abrir la imagen con PIL
  imagen = Image.open(ruta_imagen)

  # Convertir la imagen a arreglo de numpy
  datos_numericos_de_imagen = np.asarray(imagen)

  # Recortar la imagen para enfocarnos en la región de interés (ROI)
  imagen_recortada = recortar_roi(datos_numericos_de_imagen)

  kernel = [[1 / 9, 1 / 9, 1 / 9],
          [1 / 9, 1 / 9, 1 / 9],
          [1 / 9, 1 / 9, 1 / 9]]

# --- Convertir a HSV ---
  imagen_hsv_onyly_v = rgb_a_hsv_solo_value(imagen_recortada)

# =================================================================
# CONCLUSIÓN: Se seleccionó el canal V del espacio HSV
# Razón: Mostró una representación más limpia del contraste entre
# los insectos oscuros y el fondo brillante, reduciendo la visibilidad
# de residuos presentes en la superficie de la trampa
# =================================================================

# Extraer canal V (valor/brillo)
  canal_v = imagen_hsv_onyly_v[:, :]  # Canal V del espacio HSV para procesamiento

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
  elif args.accion == "filtro_convolucion":
    mostrar_filtro_convolucion(canal_v)
  elif args.accion == "umbral_otsu":
    umbral = otsu(canal_v)
    print(f"Umbral Otsu (canal V, 0-255): {umbral}")
  elif args.accion == "binaria_181":
    mostrar_binaria_umbral_181(canal_v)

"""
Flujo de la aplicación
python main.py
python main.py --accion histograma
python main.py --accion comparar
python main.py --accion canal_v
python main.py --accion todo
python main.py --accion filtro_convolucion
python main.py --accion umbral_otsu
python main.py --accion binaria_181
"""

if __name__ == "__main__":
  main()