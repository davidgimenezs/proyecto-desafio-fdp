# Relación entre las condiciones ambientales y la generación de energía de un panel solar

**Autor:** David Alfredo Giménez Sánchez  
**Cátedra:** Fundamentos de Programación - Sección F  
**Carrera:** Ingeniería Mecatrónica  
**Fecha:** 18 de mayo del 2025

## Descripción

Este proyecto analiza la relación entre diferentes condiciones ambientales (temperatura, humedad, presión) y la generación de energía de un panel solar, permitiendo la visualización y análisis de datos meteorológicos y energéticos mediante gráficos y estadísticas.

El sistema permite la carga de datos tanto de forma manual como automática (desde un archivo CSV), visualiza los datos ingresados, genera distintos tipos de gráficos y muestra estadísticas descriptivas de las variables analizadas.

## Funcionalidades

- **Carga de datos manual:** Ingreso interactivo de registros de variables ambientales y energía generada.
- **Carga automática:** Lectura de datos desde archivos CSV estructurados.
- **Validación de datos:** Comprueba la validez de fechas, horas y valores numéricos.
- **Visualización:** 
  - Energía generada en función del tiempo.
  - Relación entre temperatura, humedad y presión respecto a la energía generada.
  - Energía promedio por hora del día.
- **Estadísticas:** Muestra estadísticas descriptivas (mínimo, máximo, media, mediana, desviación estándar) de las variables principales.
- **Interfaz de menú interactivo** por consola.

## Versión experimental con interfaz gráfica

En el branch [`version-GUI`](https://github.com/davidgimenezs/proyecto-desafio-fdp/tree/version-GUI) se encuentra disponible una **versión experimental** del programa, la cual incorpora una interfaz gráfica de usuario (GUI) en lugar de la tradicional por terminal.  
Esta versión facilita el manejo y la visualización de los datos de manera más intuitiva y amigable.  
Para probarla, cambia al branch correspondiente:

```bash
git checkout version-GUI
```

Y sigue las instrucciones del README o ejecuta el programa principal.

## Requisitos

- Python 3.7 o superior
- Paquetes:
  - numpy
  - matplotlib

Puedes instalar las dependencias ejecutando:

```bash
pip install numpy matplotlib
```

> **Nota:** La versión experimental GUI puede requerir dependencias adicionales como `tkinter` o librerías específicas para la interfaz gráfica. Consulta el código o README de ese branch para más detalles.

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

## Uso

1. Clona este repositorio:
    ```bash
    git clone https://github.com/davidgimenezs/proyecto-desafio-fdp.git
    cd proyecto-desafio-fdp
    ```

2. Ejecuta el programa principal:
    ```bash
    python proyecto-desafio.py
    ```

3. Selecciona una de las opciones del menú:
    - **Carga manual de datos:** Ingresa los datos ambiental y de energía a mano.
    - **Carga automática desde archivo CSV:** El programa buscará el archivo `datos.csv` en la misma carpeta.
    - **Salir:** Cierra el programa.

4. Después de cargar los datos, puedes:
    - Visualizar gráficos interactivos.
    - Consultar estadísticas descriptivas.

## Notas

- En la carga automática, asegúrate de que el archivo `datos.csv` esté en el mismo directorio que el script.
- Las funciones de validación aseguran la integridad de los datos antes de procesarlos o graficarlos.
- Si algún dato es inválido, se notificará en consola y ese registro será ignorado.

## Licencia

Este proyecto se publica con fines educativos. Puedes usarlo y modificarlo libremente para tus propios fines académicos.
