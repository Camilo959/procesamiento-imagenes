import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Ruta de la imagen
ruta_imagen = "./imgs/1005.jpg"

# Abrir la imagen con PIL
imagen = Image.open(ruta_imagen)

# Convertir la imagen a un arreglo de NumPy
imagen_array = np.array(imagen)

# Mostrar la imagen con matplotlib
plt.imshow(imagen_array)
plt.axis('off')  # Oculta los ejes
plt.title("Imagen cargada")
plt.show()