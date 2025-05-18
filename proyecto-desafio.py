"""
Título: Relación entre las condiciones ambientales y la generación de energía de un panel solar
Autor: David Alfredo Giménez Sánchez
Cátedra: Fundamentos de Programación - Sección F
Carrera: Ingeniería Mecatrónica
Fecha: 18 de mayo del 2025
"""

import csv 
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

def es_bisiesto(anho):
    return (anho % 4 == 0 and anho % 100 != 0) or (anho % 400 == 0)

def validar_fecha(fecha_str):
    if len(fecha_str) != 10:
        return False
    dia = fecha_str[0:2]
    mes = fecha_str[3:5]
    anho = fecha_str[6:10]
    
    if not (dia.isdigit() and mes.isdigit() and anho.isdigit()):
        return False
    dia = int(dia)
    mes = int(mes)
    anho = int(anho)

    if not (1 <= mes <= 12 and 2000 <= anho <= 2100):
        return False
    dias_por_mes = [31, 29 if es_bisiesto(anho) else 28, 31, 30, 31, 30,
                    31, 31, 30, 31, 30, 31]
    return 1 <= dia <= dias_por_mes[mes - 1]

def validar_hora(hora_str):
    if len(hora_str) != 8:
        return False
    hora = hora_str[0:2]
    minuto = hora_str[3:5]
    segundo = hora_str[6:8]

    if not (hora.isdigit() and minuto.isdigit() and segundo.isdigit()):
        return False
    hora = int(hora)
    minuto = int(minuto)
    segundo = int(segundo)
    return (0 <= hora < 24) and (0 <= minuto < 60) and (0 <= segundo < 60)

def validar_datos(fila):
    try:
        if not validar_fecha(fila['Fecha']):
            return False
        if not validar_hora(fila['Hora']):
            return False
        float(fila['Temperatura'])
        float(fila['Humedad'])
        float(fila['Presion'])
        float(fila['Energia'])
        return True
    except (ValueError, KeyError):
        return False

def procesar_fila(fila):
    fecha = fila['Fecha']
    hora = fila['Hora']
    temperatura = float(fila['Temperatura'])
    humedad = float(fila['Humedad'])
    presion = float(fila['Presion'])
    energia = float(fila['Energia'])
    return fecha, hora, temperatura, humedad, presion, energia

def leer_datos(archivo):
    fechas = []
    horas = []
    temperaturas = []
    humedades = []
    presiones = []
    energias = []

    with open(archivo, mode='r') as file:
        reader = csv.DictReader(file)
        for fila in reader:
            if validar_datos(fila):
                fecha, hora, temperatura, humedad, presion, energia = procesar_fila(fila)
                fechas.append(fecha)
                horas.append(hora)
                temperaturas.append(temperatura)
                humedades.append(humedad)
                presiones.append(presion)
                energias.append(energia)
            else:
                print(f"Fila ignorada por datos inválidos: {fila}")
    
    return fechas, horas, temperaturas, humedades, presiones, energias

def mostrar_datos(fechas, horas, temperaturas, humedades, presiones, energias):
    for i in range(len(fechas)):
        print(f"Fecha: {fechas[i]}")
        print(f"Hora: {horas[i]}")
        print(f"Temperatura: {temperaturas[i]} °C")
        print(f"Humedad: {humedades[i]} %")
        print(f"Presión: {presiones[i]} hPa")
        print(f"Energía: {energias[i]} W")
        print()

def carga_manual():
    fechas = []
    horas = []
    temperaturas = []
    humedades = []
    presiones = []
    energias = []
    
    try:
        num_puntos = int(input("Ingrese el número de puntos a cargar: "))
        if num_puntos <= 0:
            print("El número de puntos debe ser mayor que cero.")
            return None
    except ValueError:
        print("Debe ingresar un número entero válido.")
        return None
    
    for i in range(num_puntos):
        print(f"\n--- Punto {i+1} ---")
        while True:
            fecha = input("Fecha (DD/MM/YYYY): ")
            if validar_fecha(fecha):
                break
            else:
                print("Formato de fecha inválido. Use DD/MM/YYYY.")
        
        while True:
            hora = input("Hora (HH:MM:SS): ")
            if validar_hora(hora):
                break
            else:
                print("Formato de hora inválido. Use HH:MM:SS.")
        
        try:
            temperatura = float(input("Temperatura (°C): "))
            humedad = float(input("Humedad (%): "))
            presion = float(input("Presión (hPa): "))
            energia = float(input("Energía (W): "))
            
            fechas.append(fecha)
            horas.append(hora)
            temperaturas.append(temperatura)
            humedades.append(humedad)
            presiones.append(presion)
            energias.append(energia)
        except ValueError:
            print("Error: Los valores numéricos deben ser números válidos.")
            i -= 1
    
    return fechas, horas, temperaturas, humedades, presiones, energias

def carga_automatica(archivo):
    return leer_datos(archivo)

def menu_principal():
    print("\n===== SISTEMA DE GESTIÓN DE DATOS METEOROLÓGICOS =====")
    print("1. Carga manual de datos")
    print("2. Carga automática desde archivo CSV")
    print("3. Salir")
    
    while True:
        try:
            opcion = int(input("\nSeleccione una opción (1-3): "))
            if 1 <= opcion <= 3:
                return opcion
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Por favor, ingrese un número entero.")

def convertir_fecha_hora(fechas, horas):
    fecha_hora = []
    for fecha, hora in zip(fechas, horas):
        fecha_hora_str = f"{fecha} {hora}"
        fecha_hora_obj = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M:%S")
        fecha_hora.append(fecha_hora_obj)
    return fecha_hora

def graficar_energia_tiempo(fechas, horas, energias):
    fecha_hora = convertir_fecha_hora(fechas, horas)
    
    etiquetas_fecha = [dt.strftime("%d/%m %H:%M") for dt in fecha_hora]
    
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(energias)), energias, width=0.8, color='green')
    
    plt.xticks(range(len(energias)), etiquetas_fecha, rotation=45)
    
    plt.title('Energía generada en función del tiempo')
    plt.xlabel('Fecha y Hora')
    plt.ylabel('Energía (W)')
    plt.grid(axis='y')
    
    if len(energias) <= 20:
        for i, valor in enumerate(energias):
            plt.text(i, valor + 0.5, f"{valor:.1f}", ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.show()

def graficar_temperatura_energia(temperaturas, energias):
    plt.figure(figsize=(10, 6))
    plt.scatter(temperaturas, energias, alpha=0.7, color='red')
    
    if len(temperaturas) > 1:
        coef = np.polyfit(temperaturas, energias, 1)
        polinomio = np.poly1d(coef)
        x_tendencia = np.linspace(min(temperaturas), max(temperaturas), 100)
        plt.plot(x_tendencia, polinomio(x_tendencia), 'b--', 
                 label=f'Tendencia: {coef[0]:.2f}x + {coef[1]:.2f}')
        plt.legend()
    
    plt.title('Relación entre Temperatura y Energía')
    plt.xlabel('Temperatura (°C)')
    plt.ylabel('Energía (W)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def graficar_presion_energia(presiones, energias):
    plt.figure(figsize=(10, 6))
    plt.scatter(presiones, energias, alpha=0.7, color='purple')
    
    if len(presiones) > 1:
        coef = np.polyfit(presiones, energias, 1)
        polinomio = np.poly1d(coef)
        x_tendencia = np.linspace(min(presiones), max(presiones), 100)
        plt.plot(x_tendencia, polinomio(x_tendencia), 'b--', 
                 label=f'Tendencia: {coef[0]:.2f}x + {coef[1]:.2f}')
        plt.legend()
    
    plt.title('Relación entre Presión y Energía')
    plt.xlabel('Presión (hPa)')
    plt.ylabel('Energía (W)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def graficar_humedad_energia(humedades, energias):
    plt.figure(figsize=(10, 6))
    plt.scatter(humedades, energias, alpha=0.7, color='blue')
    
    if len(humedades) > 1:
        coef = np.polyfit(humedades, energias, 1)
        polinomio = np.poly1d(coef)
        x_tendencia = np.linspace(min(humedades), max(humedades), 100)
        plt.plot(x_tendencia, polinomio(x_tendencia), 'r--', 
                 label=f'Tendencia: {coef[0]:.2f}x + {coef[1]:.2f}')
        plt.legend()
    
    plt.title('Relación entre Humedad y Energía')
    plt.xlabel('Humedad (%)')
    plt.ylabel('Energía (W)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def graficar_tiempo_dia_energia(fechas, horas, energias):
    fecha_hora = convertir_fecha_hora(fechas, horas)
    
    horas_del_dia = [dt.hour for dt in fecha_hora]
    energia_por_hora = {}
    
    for hora, energia in zip(horas_del_dia, energias):
        if hora not in energia_por_hora:
            energia_por_hora[hora] = []
        energia_por_hora[hora].append(energia)
    
    horas_ordenadas = sorted(energia_por_hora.keys())
    energia_promedio = [sum(energia_por_hora[h])/len(energia_por_hora[h]) for h in horas_ordenadas]
    
    plt.figure(figsize=(12, 6))
    plt.bar(horas_ordenadas, energia_promedio, width=0.7, color='orange')
    plt.title('Energía Promedio por Hora del Día')
    plt.xlabel('Hora del Día')
    plt.ylabel('Energía Promedio (W)')
    plt.xticks(range(0, 24))
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def calcular_mediana(datos):
    datos_ordenados = sorted(datos)
    n = len(datos_ordenados)
    if n % 2 == 0:
        return (datos_ordenados[n // 2 - 1] + datos_ordenados[n // 2]) / 2
    else:
        return datos_ordenados[n // 2]

def calcular_desviacion_estandar(datos, media):
    if len(datos) <= 1:
        return 0
    
    suma_cuadrados = sum((x - media) ** 2 for x in datos)
    
    return (suma_cuadrados / (len(datos) - 1)) ** 0.5

def calcular_estadisticas(datos, nombre_variable):
    minimo = min(datos)
    maximo = max(datos)
    media = sum(datos) / len(datos)
    mediana = calcular_mediana(datos)
    desviacion = calcular_desviacion_estandar(datos, media)
    
    return {
        'nombre': nombre_variable,
        'minimo': minimo,
        'maximo': maximo,
        'media': media,
        'mediana': mediana,
        'desviacion': desviacion
    }

def mostrar_estadisticas(temperaturas, humedades, presiones, energias):
    variables = [
        calcular_estadisticas(temperaturas, "Temperatura (°C)"),
        calcular_estadisticas(humedades, "Humedad (%)"),
        calcular_estadisticas(presiones, "Presión (hPa)"),
        calcular_estadisticas(energias, "Energía (W)")
    ]
    
    nombres = [var['nombre'] for var in variables]
    minimos = [var['minimo'] for var in variables]
    maximos = [var['maximo'] for var in variables]
    medias = [var['media'] for var in variables]
    medianas = [var['mediana'] for var in variables]
    desviaciones = [var['desviacion'] for var in variables]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('tight')
    ax.axis('off')
    
    encabezados = ['Variable', 'Mínimo', 'Máximo', 'Media', 'Mediana', 'Desv. Est.']
    datos_tabla = []
    
    for i in range(len(nombres)):
        datos_tabla.append([
            nombres[i], 
            f"{minimos[i]:.2f}", 
            f"{maximos[i]:.2f}", 
            f"{medias[i]:.2f}", 
            f"{medianas[i]:.2f}", 
            f"{desviaciones[i]:.2f}"
        ])
    
    tabla = ax.table(
        cellText=datos_tabla, 
        colLabels=encabezados,
        loc='center',
        cellLoc='center'
    )
    
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1.2, 1.5)
    
    for i, encabezado in enumerate(encabezados):
        tabla[(0, i)].set_facecolor('#4472C4')
        tabla[(0, i)].set_text_props(color='white', fontweight='bold')
    
    for i in range(len(nombres)):
        for j in range(len(encabezados)):
            if i % 2 == 0:
                tabla[(i+1, j)].set_facecolor('#D9E1F2')
            else:
                tabla[(i+1, j)].set_facecolor('#E9EDF4')
    
    plt.suptitle('Estadísticas de los Datos', fontsize=16, fontweight='bold', y=0.95)
    plt.tight_layout()
    
    plt.show()

def menu_graficos(fechas, horas, temperaturas, humedades, presiones, energias):
    while True:
        print("\n===== GENERACIÓN DE GRÁFICOS Y ESTADÍSTICAS =====")
        print("1. Energía generada en el tiempo")
        print("2. Temperatura vs Energía")
        print("3. Presión vs Energía")
        print("4. Humedad vs Energía")
        print("5. Hora del día vs Energía promedio")
        print("6. Mostrar datos estadísticos")
        print("7. Volver al menú principal")
        
        try:
            opcion = int(input("\nSeleccione una opción (1-7): "))
            
            if opcion == 1:
                graficar_energia_tiempo(fechas, horas, energias)
            elif opcion == 2:
                graficar_temperatura_energia(temperaturas, energias)
            elif opcion == 3:
                graficar_presion_energia(presiones, energias)
            elif opcion == 4:
                graficar_humedad_energia(humedades, energias)
            elif opcion == 5:
                graficar_tiempo_dia_energia(fechas, horas, energias)
            elif opcion == 6:
                mostrar_estadisticas(temperaturas, humedades, presiones, energias)
            elif opcion == 7:
                break
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Por favor, ingrese un número entero.")

# Programa principal
while True:
    opcion = menu_principal()
    
    if opcion == 1:
        print("\n--- CARGA MANUAL DE DATOS ---")
        resultado = carga_manual()
        if resultado:
            fechas, horas, temperaturas, humedades, presiones, energias = resultado
            print("\nDatos cargados correctamente!")
            mostrar_datos(fechas, horas, temperaturas, humedades, presiones, energias)
            menu_graficos(fechas, horas, temperaturas, humedades, presiones, energias)
        else:
            print("\nError en la carga manual de datos.")
    
    elif opcion == 2:
        print("\n--- CARGA AUTOMÁTICA DESDE ARCHIVO CSV ---")
        archivo = 'datos.csv'
        try:
            fechas, horas, temperaturas, humedades, presiones, energias = carga_automatica(archivo)
            print(f"\nDatos cargados correctamente desde '{archivo}'!")
            mostrar_datos(fechas, horas, temperaturas, humedades, presiones, energias)
            menu_graficos(fechas, horas, temperaturas, humedades, presiones, energias)
        except FileNotFoundError:
            print(f"Error: El archivo '{archivo}' no fue encontrado.")
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
    
    elif opcion == 3:
        print("\nSaliendo del programa. ¡Hasta luego!")
        break
