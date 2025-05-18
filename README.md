# Relación entre las condiciones ambientales y la generación de energía de un panel solar — Versión GUI

**Autor:** David Alfredo Giménez Sánchez  
**Cátedra:** Fundamentos de Programación - Sección F  
**Carrera:** Ingeniería Mecatrónica  
**Fecha:** 18 de mayo del 2025

## Descripción

Esta versión incorpora una **interfaz gráfica de usuario (GUI)** que facilita el manejo, la visualización y el análisis de los datos ambientales y la energía generada por un panel solar. Todo el flujo de trabajo original se ha adaptado para interactuar mediante ventanas y controles gráficos, haciendo la experiencia más intuitiva y amigable.

## Funcionalidades

- **Carga de datos manual:** Ingreso de registros a través de formularios gráficos.
- **Carga automática:** Importación de datos desde archivos CSV.
- **Validación de datos:** Verificaciones automáticas de formato y valores.
- **Visualización gráfica:** 
  - Gráficos interactivos de energía generada en función del tiempo.
  - Análisis visual de la relación entre temperatura, humedad, presión y la energía generada.
  - Energía promedio por hora del día.
- **Estadísticas:** Consulta de estadísticas descriptivas de las variables principales.
- **Interfaz gráfica:** Navegación por ventanas, menús y botones.

## Requisitos y dependencias

- **Python 3.7 o superior**
- **numpy**
- **matplotlib**
- **tkinter** (librería estándar para interfaces gráficas en Python)

Puedes instalar las dependencias principales, excepto `tkinter` (que suele venir incluida en la instalación estándar de Python) ejecutando:

```bash
pip install numpy matplotlib
```

### Instalación de tkinter

- En **Windows** y **macOS** normalmente ya viene incluida junto con Python.
- En algunas distribuciones de **Linux**, puedes instalarla con:
  - Debian/Ubuntu:  
    ```bash
    sudo apt-get install python3-tk
    ```
  - Fedora:  
    ```bash
    sudo dnf install python3-tkinter
    ```

**Nota:**  
La presencia de `tkinter` es obligatoria para el funcionamiento de la versión GUI.

## Instalación y ejecución

1. Cambia al branch `version-GUI`:

   ```bash
   git checkout version-GUI
   ```

2. Instala las dependencias necesarias como se describe arriba.

3. Ejecuta el programa principal de la versión GUI (reemplaza `proyecto_desafio_gui.py` por el nombre real del archivo):

   ```bash
   python proyecto_desafio_gui.py
   ```

## Estructura de los datos

El archivo CSV debe tener la siguiente estructura de columnas:

- `Fecha` (formato: DD/MM/YYYY)
- `Hora` (formato: HH:MM:SS)
- `Temperatura` (°C)
- `Humedad` (%)
- `Presion` (hPa)
- `Energia` (W)

Ejemplo de una línea en el CSV:

```
Fecha,Hora,Temperatura,Humedad,Presion,Energia
18/05/2025,12:00:00,32.5,45.0,1013.2,156.8
```

## Uso general

1. Al iniciar el programa se mostrará la ventana principal de la aplicación.
2. Utiliza los menús para cargar datos, visualizar gráficos y consultar estadísticas.
3. Puedes ingresar datos manualmente o importar un archivo CSV.
4. Todos los resultados y gráficas se mostrarán en la ventana, sin necesidad de usar la consola.

## Notas

- Asegúrate de que el archivo `datos.csv` esté en la misma carpeta que el script si usas la carga automática.
- Las validaciones se realizan automáticamente al ingresar o importar datos.
- Si algún dato es inválido, la aplicación lo notificará mediante la interfaz gráfica.

## Licencia

Este proyecto se publica con fines educativos. Puedes usarlo y modificarlo libremente para tus propios fines académicos.
