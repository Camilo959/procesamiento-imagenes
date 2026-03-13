# Práctica de Proyecto - Procesamiento de Imágenes

## Descripción
Este proyecto implementa conversiones de espacios de color y visualización de canales para imágenes digitales. Incluye conversiones de RGB a YUV y HSV, además de herramientas para análisis de histogramas y visualización de canales individuales.

## Estructura del Proyecto
```
Practica_proyecto/
│
├── main.py                      # Archivo principal de ejecución
├── imgs/                        # Carpeta de imágenes de entrada
│   └── 1005.jpg
├── utils/                       # Módulos de utilidades
│   ├── conversiones_color.py   # Funciones de conversión de espacios de color
│   └── __pycache__/
└── README.md                    # Este archivo
```

## Funcionalidades Implementadas

### 1. Conversiones de Espacios de Color

#### RGB a YUV
Convierte una imagen RGB al espacio de color YUV utilizando la siguiente matriz de transformación:

$$
\begin{bmatrix}
Y \\
U \\
V
\end{bmatrix}
=
\begin{bmatrix}
0.299 & 0.587 & 0.114 \\
-0.14713 & -0.28886 & 0.436 \\
0.615 & -0.51499 & -0.10001
\end{bmatrix}
\begin{bmatrix}
R \\
G \\
B
\end{bmatrix}
$$

Donde:
- **Y**: Canal de luminancia (brillo)
- **U**: Diferencia de color azul
- **V**: Diferencia de color rojo

#### RGB a HSV
Convierte una imagen RGB al espacio de color HSV:
- **H (Hue)**: Tono (0-360°)
- **S (Saturation)**: Saturación (0-1)
- **V (Value)**: Valor/Brillo (0-1)

### 2. Cálculo de Histogramas
Función que calcula el histograma de intensidades para un canal dado, contando la frecuencia de cada valor de píxel (0-255).

### 3. Visualización de Canales RGB
Visualiza los tres canales de una imagen RGB por separado en escala de grises:
- Canal R (Rojo)
- Canal G (Verde)
- Canal B (Azul)

## Uso de espacio de color
Estas son las notas para la elección del espacio de color que se va a usar para el proyecto.

- Del espacio de color RGB, el canal Blue no hace ningún aporte para la descripción de problema, este no se va a tener en consideración. Los canales Red y Green son espacios de color que pueden servir, sin embargo, se va a buscar más opciones.
- Del espacio de color YUV, el canal Y (luminancia) es el mas adecuado para tener en consideración, ya que es el que aporta la información de brillo, mientras que los canales U y V aportan información de color que no es relevante para la descripción del problema.
- Del espacio de color HSV, el canal V (valor) es el mas adecuado para tener en consideración, ya que es el que aporta la información de brillo, mientras que los canales H y S aportan información de color que no es relevante para la descripción del problema.

Se evaluaron los espacios de color RGB, YUV y HSV para determinar cuál canal representaba mejor la diferencia entre los insectos y el fondo de la trampa amarilla. Aunque el canal Y del espacio YUV representa la luminancia perceptual, se observó que resalta con mayor intensidad pequeños residuos presentes en la superficie de la trampa. En contraste, el canal V del espacio HSV mostró una representación más limpia del contraste entre los insectos oscuros y el fondo brillante, reduciendo la visibilidad de dichos residuos. Por esta razón se seleccionó el canal V del espacio HSV como base para la detección.

## Requisitos

### Librerías Python Necesarias
```bash
pip install numpy
pip install matplotlib
pip install pillow
```

O usando un archivo `requirements.txt`:
```
numpy
matplotlib
pillow
```

## Uso

### Ejecución Básica
```bash
python main.py
```

### Cambiar la Imagen de Entrada
Edita la ruta de la imagen en `main.py`:
```python
ruta_imagen = "./imgs/tu_imagen.jpg"
```

### Funciones Disponibles

#### Convertir RGB a YUV
```python
from utils.conversiones_color import rgb_a_yuv
import numpy as np

imagen_yuv = rgb_a_yuv(datos_numericos_de_imagen)
```

#### Convertir RGB a HSV
```python
from utils.conversiones_color import rgb_a_hsv

imagen_hsv = rgb_a_hsv(datos_numericos_de_imagen)
```

#### Calcular Histograma
```python
def calcular_histograma(imagen):
    histograma = []
    xticks = []
    for i in range(256):
        xticks.append(i)
        histograma.append(np.count_nonzero(imagen == i))
    return histograma, xticks

# Uso
histograma, xticks = calcular_histograma(datos_numericos_de_imagen[:, :, 0])
```

## Ejemplos de Visualización

### Ver Canales RGB
El código actual muestra los tres canales RGB en gráficas separadas:

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(datos_numericos_de_imagen[:, :, 0], cmap='gray')
axes[0].set_title("Canal R (Rojo)")

axes[1].imshow(datos_numericos_de_imagen[:, :, 1], cmap='gray')
axes[1].set_title("Canal G (Verde)")

axes[2].imshow(datos_numericos_de_imagen[:, :, 2], cmap='gray')
axes[2].set_title("Canal B (Azul)")

plt.show()
```

### Ver Canal Y de YUV
```python
plt.imshow(imagen_yuv[:, :, 0], cmap='gray')
plt.title("Canal Y (luminancia)")
plt.show()
```

### Ver Canal H de HSV
```python
plt.imshow(imagen_hsv[:, :, 0], cmap='gray')
plt.title("Canal H (Hue)")
plt.show()
```

## Conceptos Teóricos

### Espacio de Color RGB
- Modelo aditivo de color
- Cada píxel se representa con tres valores (Rojo, Verde, Azul)
- Rango de valores: 0-255 para cada canal

### Espacio de Color YUV
- Separa luminancia (Y) de crominancia (U, V)
- Usado en sistemas de video y compresión
- Más eficiente para compresión que RGB

### Espacio de Color HSV
- Más intuitivo para la percepción humana
- Útil para segmentación por color
- H (tono) determina el color base
- S (saturación) determina la pureza del color
- V (valor) determina el brillo

## Notas Técnicas

1. **Normalización**: Los valores de entrada RGB (0-255) se normalizan a (0-1) antes de las conversiones
2. **Tipo de datos**: Se usa `float` para mantener precisión en las operaciones matemáticas
3. **Optimización**: Las operaciones usan NumPy para procesamiento vectorizado eficiente

## Posibles Extensiones

- [ ] Implementar conversión RGB a LAB
- [ ] Añadir ecualización de histogramas
- [ ] Implementar filtros de convolución
- [ ] Agregar detección de bordes
- [ ] Crear interfaz gráfica (GUI)
- [ ] Procesamiento por lotes de múltiples imágenes

## Autor
Proyecto de Procesamiento de Imágenes - 10° Semestre

## Fecha
Marzo 2026
