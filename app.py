import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox, filedialog  # Añadimos filedialog aquí
from PIL import Image, ImageTk
import os
import sys
import csv
import pandas as pd

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SolarTech")  # Nombre comercial en español
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Establecer el favicon de la ventana
        try:
            favicon_path = os.path.join(os.path.dirname(__file__), "images", "favicon.png")
            favicon = PhotoImage(file=favicon_path)
            self.root.iconphoto(True, favicon)
        except Exception as e:
            print(f"Error cargando el favicon: {e}")
    
        # Configure the style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12, "bold"), padding=10)
        self.style.configure("TLabel", font=("Arial", 14))
        self.style.configure("Title.TLabel", font=("Arial", 24, "bold"))
        
        # Create frames for different pages
        self.home_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.start_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.about_frame = tk.Frame(self.root, bg="#f0f0f0")
        
        # Initialize all frames
        self.setup_home_frame()
        self.setup_start_frame()
        self.setup_about_frame()
        
        # Show home frame initially
        self.show_frame(self.home_frame)
    
    def setup_home_frame(self):
        # Set up background image that fills the entire frame
        try:
            # Try to load the solar panel image
            img_path = os.path.join(os.path.dirname(__file__), "images", "solarpanelhero.jpg")
            self.bg_img = Image.open(img_path)
            
            # Create a function to resize the image when window is resized
            def resize_image(event):
                new_width = event.width
                new_height = event.height
                resized_img = self.bg_img.resize((new_width, new_height), Image.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(resized_img)
                bg_label.config(image=self.bg_photo)
                
            # Initial resize
            self.bg_photo = ImageTk.PhotoImage(self.bg_img.resize((800, 600), Image.LANCZOS))
            bg_label = tk.Label(self.home_frame, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire frame
            
            # Bind resize event
            self.home_frame.bind('<Configure>', resize_image)
            
        except Exception as e:
            print(f"Error loading background image: {e}")
            # Just continue without background image if it fails
    
        # Central content panel with semi-transparent background and better sizing
        content_panel = tk.Frame(self.home_frame, bg='white', padx=40, pady=40, bd=2, relief=tk.RIDGE)
        content_panel.place(relx=0.5, rely=0.5, anchor='center')
        
        # Make content panel responsive to window size but with minimum width
        def update_content_panel(event=None):
            # Calculate panel width based on window size (50% of window width, min 400px)
            window_width = self.home_frame.winfo_width()
            panel_width = max(400, min(500, int(window_width * 0.5)))
            content_panel.config(width=panel_width)
        
        # Bind resize event for content panel
        self.home_frame.bind('<Configure>', lambda e: [resize_image(e), update_content_panel(e)])
        
        # Title
        title_label = ttk.Label(
            content_panel, 
            text="Análisis de Energía de Paneles Solares", 
            style="Title.TLabel",
            background='white',
            anchor='center',
            justify='center'
        )
        title_label.pack(pady=10, fill='x')
        
        # Description
        desc_label = ttk.Label(
            content_panel,
            text="Analiza la relación entre las condiciones ambientales y la generación de energía solar.",
            wraplength=400,
            background='white',
            anchor='center',
            justify='center'
        )
        desc_label.pack(pady=20, fill='x')
        
        # Buttons frame - centered
        buttons_frame = tk.Frame(content_panel, bg='white')
        buttons_frame.pack(pady=10, fill='x')
        
        # Create an inner frame to hold the buttons and center them
        inner_buttons_frame = tk.Frame(buttons_frame, bg='white')
        inner_buttons_frame.pack(anchor='center')
        
        # Navigation buttons
        start_button = ttk.Button(inner_buttons_frame, text="Iniciar Análisis", command=lambda: self.show_frame(self.start_frame))
        start_button.grid(row=0, column=0, padx=10)
        
        about_button = ttk.Button(inner_buttons_frame, text="Acerca De", command=lambda: self.show_frame(self.about_frame))
        about_button.grid(row=0, column=1, padx=10)
        
        exit_button = ttk.Button(inner_buttons_frame, text="Salir", command=self.exit_app)
        exit_button.grid(row=0, column=2, padx=10)
        
        # Center the buttons frame inside content panel
        buttons_frame.pack(pady=10, fill='x')
        buttons_frame.update()
        buttons_frame.pack_propagate(False)
        
        # Initial update for the content panel
        self.home_frame.update()
        update_content_panel()

    def setup_start_frame(self):        # Header (reduced top padding)
        header_label = ttk.Label(
            self.start_frame, 
            text="Análisis de Datos Solares", 
            style="Title.TLabel"
        )
        header_label.pack(pady=15)
          # Create a container to center content with reduced height
        container = tk.Frame(self.start_frame, bg="#f0f0f0", padx=40, pady=10)
        container.pack(fill="both", expand=True, padx=50, pady=10)
        
        # Introduction text (more concise to save vertical space)
        intro_text = """Este programa permite analizar la relación entre las condiciones ambientales y la generación de energía en paneles solares.

El análisis incluye:
• Correlación entre temperatura y rendimiento energético
• Impacto de la humedad en la eficiencia
• Efectos de la presión atmosférica en la generación
• Visualización de datos mediante gráficos comparativos

Seleccione una opción para comenzar:"""        

        intro_label = ttk.Label(
            container,
            text=intro_text,
            wraplength=600,
            justify="left",
            background="#f0f0f0"
        )
        intro_label.pack(pady=10, fill="x")
        
        # Button container with reduced padding
        button_container = tk.Frame(container, bg="#f0f0f0")
        button_container.pack(pady=15)
          # Option buttons with icons
        manual_button = ttk.Button(
            button_container, 
            text="Carga Manual de Datos", 
            command=self.open_manual_input,
            width=25
        )
        manual_button.grid(row=0, column=0, padx=15, pady=10)
        
        file_button = ttk.Button(
            button_container, 
            text="Carga desde Archivo", 
            command=self.open_file_input,
            width=25
        )
        file_button.grid(row=0, column=1, padx=15, pady=10)
          # Back button below main buttons with balanced padding
        back_button = ttk.Button(
            button_container, 
            text="Volver al Inicio", 
            command=lambda: self.show_frame(self.home_frame),
            width=25
        )
        back_button.grid(row=1, column=0, columnspan=2, padx=15, pady=(10, 10))
    
    def setup_about_frame(self):
        # Add a container frame that will center all content
        container = tk.Frame(self.about_frame, bg="#f0f0f0")
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Header
        header_label = ttk.Label(
            container, 
            text="Acerca del Proyecto", 
            style="Title.TLabel",
            background="#f0f0f0"
        )
        header_label.pack(pady=20)
        
        # Content
        content_label = ttk.Label(
            container,
            text="""Este proyecto tiene como objetivo desarrollar un programa en Python para analizar la relación entre las condiciones ambientales y la generación de energía solar. 

Se investigan variables como temperatura, humedad y presión, que influyen en la eficiencia de los paneles solares.

La metodología abarca la adquisición de datos, el procesamiento estadístico utilizando NumPy y la visualización de los resultados con Matplotlib.""",
            wraplength=600,
            justify="left",
            background="#f0f0f0"
        )
        content_label.pack(pady=20)
        
        # Credits info
        version_label = ttk.Label(
            container,
            text="Elaborado por: David Alfredo Giménez Sánchez",
            background="#f0f0f0"
        )
        version_label.pack(pady=5)

        # About info
        version_label = ttk.Label(
            container,
            text="Versión: 1.0.0",
            background="#f0f0f0"
        )
        version_label.pack(pady=5)
        
        # Back button
        back_button = ttk.Button(container, text="Volver al Inicio", command=lambda: self.show_frame(self.home_frame))
        back_button.pack(pady=20)
    
    def show_frame(self, frame):
        # Hide all frames
        for f in [self.home_frame, self.start_frame, self.about_frame]:
            f.pack_forget()
        
        # Show the selected frame
        frame.pack(fill="both", expand=True)
    
    def exit_app(self):
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
            self.root.destroy()
            sys.exit()
    
    def open_manual_input(self):
        # Crear una ventana modal para ingresar datos manualmente
        manual_window = tk.Toplevel(self.root)
        manual_window.title("Ingreso Manual de Datos")
        manual_window.geometry("600x600")  # Aumentar el tamaño para acomodar la lista
        manual_window.resizable(True, True)
        manual_window.transient(self.root)  # Hace que la ventana sea modal
        manual_window.grab_set()  # Bloquea interacciones con la ventana principal
        
        # Marco principal con dos columnas
        main_frame = tk.Frame(manual_window, padx=20, pady=20, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Ingreso Manual de Datos", 
            style="Title.TLabel",
            background="#f0f0f0"
        )
        title_label.pack(pady=(0, 20))
        
        # Dividir en dos columnas: formulario y lista
        columns_frame = tk.Frame(main_frame, bg="#f0f0f0")
        columns_frame.pack(fill="both", expand=True)
        
        # Marco para el formulario (columna izquierda)
        form_frame = tk.Frame(columns_frame, bg="#f0f0f0", padx=10)
        form_frame.pack(side="left", fill="both", expand=True)
        
        # Marco para la lista de datos ingresados (columna derecha)
        list_frame = tk.Frame(columns_frame, bg="#f0f0f0", padx=10)
        list_frame.pack(side="right", fill="both", expand=True)
        
        # Lista para mostrar datos ingresados
        list_label = ttk.Label(list_frame, text="Datos ingresados:", background="#f0f0f0")
        list_label.pack(pady=(0, 10))
        
        # Crear listbox con scrollbar para mostrar datos
        list_frame_scroll = tk.Frame(list_frame, bg="#f0f0f0")
        list_frame_scroll.pack(fill="both", expand=True)
        
        data_listbox = tk.Listbox(list_frame_scroll, width=40, height=10)
        data_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame_scroll, orient="vertical", command=data_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        data_listbox.config(yscrollcommand=scrollbar.set)
        
        # Vincular la rueda del ratón al Listbox
        def _on_mousewheel(event):
            data_listbox.yview_scroll(int(-1*(event.delta/120)), "units")
            
        list_frame_scroll.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Asegurar que se desvincula el evento cuando se cierra la ventana
        def _on_manual_window_closing():
            list_frame_scroll.unbind_all("<MouseWheel>")
            manual_window.destroy()
            
        manual_window.protocol("WM_DELETE_WINDOW", _on_manual_window_closing)
        
        # Lista para almacenar los datos ingresados
        datos_ingresados = []
        
        # Crear variables para cada campo
        fecha_var = tk.StringVar()
        hora_var = tk.StringVar()
        temperatura_var = tk.DoubleVar()
        humedad_var = tk.DoubleVar()
        presion_var = tk.DoubleVar()
        energia_var = tk.DoubleVar()
        
        # Función para validar que sólo se ingresen números con punto decimal
        def validate_float(action, value_if_allowed):
            if action != '1':  # Si no es una inserción
                return True
            if value_if_allowed == "":
                return True
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        
        # Crear validador para campos numéricos
        validate_cmd = manual_window.register(validate_float)
        
        # Etiquetas y campos de entrada
        # Fecha (con formato DD/MM/AAAA)
        fecha_label = ttk.Label(form_frame, text="Fecha (DD/MM/AAAA):", background="#f0f0f0")
        fecha_label.grid(row=0, column=0, sticky="w", padx=5, pady=8)
        fecha_entry = ttk.Entry(form_frame, textvariable=fecha_var, width=20)
        fecha_entry.grid(row=0, column=1, sticky="w", padx=5, pady=8)
        
        # Hora (con formato HH:MM:SS)
        hora_label = ttk.Label(form_frame, text="Hora (HH:MM:SS):", background="#f0f0f0")
        hora_label.grid(row=1, column=0, sticky="w", padx=5, pady=8)
        hora_entry = ttk.Entry(form_frame, textvariable=hora_var, width=20)
        hora_entry.grid(row=1, column=1, sticky="w", padx=5, pady=8)
        
        # Temperatura (°C)
        temperatura_label = ttk.Label(form_frame, text="Temperatura (°C):", background="#f0f0f0")
        temperatura_label.grid(row=2, column=0, sticky="w", padx=5, pady=8)
        temperatura_entry = ttk.Entry(
            form_frame, 
            textvariable=temperatura_var, 
            width=20, 
            validate="key",
            validatecommand=(validate_cmd, '%d', '%P')
        )
        temperatura_entry.grid(row=2, column=1, sticky="w", padx=5, pady=8)
        
        # Humedad (%)
        humedad_label = ttk.Label(form_frame, text="Humedad (%):", background="#f0f0f0")
        humedad_label.grid(row=3, column=0, sticky="w", padx=5, pady=8)
        humedad_entry = ttk.Entry(
            form_frame, 
            textvariable=humedad_var, 
            width=20,
            validate="key",
            validatecommand=(validate_cmd, '%d', '%P')
        )
        humedad_entry.grid(row=3, column=1, sticky="w", padx=5, pady=8)
        
        # Presión (hPa)
        presion_label = ttk.Label(form_frame, text="Presión (hPa):", background="#f0f0f0")
        presion_label.grid(row=4, column=0, sticky="w", padx=5, pady=8)
        presion_entry = ttk.Entry(
            form_frame, 
            textvariable=presion_var, 
            width=20,
            validate="key",
            validatecommand=(validate_cmd, '%d', '%P')
        )
        presion_entry.grid(row=4, column=1, sticky="w", padx=5, pady=8)
        
        # Energía (W)
        energia_label = ttk.Label(form_frame, text="Energía (W):", background="#f0f0f0")
        energia_label.grid(row=5, column=0, sticky="w", padx=5, pady=8)
        energia_entry = ttk.Entry(
            form_frame, 
            textvariable=energia_var, 
            width=20,
            validate="key",
            validatecommand=(validate_cmd, '%d', '%P')
        )
        energia_entry.grid(row=5, column=1, sticky="w", padx=5, pady=8)
        
        # Mensaje de información
        info_label = ttk.Label(
            form_frame,
            text="Ingrese datos y presione 'Añadir'. Cuando termine, presione 'Finalizar'.",
            foreground="gray",
            background="#f0f0f0",
            wraplength=300
        )
        info_label.grid(row=6, columnspan=2, pady=10)
        
        # Marco para botones en la parte inferior
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(pady=10, side="bottom", fill="x")
        
        # Función para añadir datos a la lista
        def añadir_datos():
            # Validar los datos ingresados
            fecha = fecha_var.get()
            hora = hora_var.get()
            
            # Validar formato de fecha y hora usando las funciones existentes
            if not self.validar_fecha(fecha):
                messagebox.showerror("Error", "Formato de fecha inválido.\nUse el formato DD/MM/AAAA.")
                return
                
            if not self.validar_hora(hora):
                messagebox.showerror("Error", "Formato de hora inválido.\nUse el formato HH:MM:SS.")
                return
                
            try:
                temperatura = temperatura_var.get()
                humedad = humedad_var.get()
                presion = presion_var.get()
                energia = energia_var.get()
                
                # Simulamos una fila de datos como la que vendría de un archivo
                fila_datos = {
                    'Fecha': fecha,
                    'Hora': hora,
                    'Temperatura': str(temperatura),
                    'Humedad': str(humedad),
                    'Presion': str(presion),
                    'Energia': str(energia)
                }
                
                # Usar la misma función de validación que para archivos
                if not self.validar_datos(fila_datos):
                    messagebox.showerror("Error", "Los datos no cumplen con los criterios de validación.")
                    return
                
                # Verificar rangos específicos para datos manuales
                if not (0 <= humedad <= 100):
                    messagebox.showerror("Error", "La humedad debe estar entre 0 y 100%.")
                    return
                    
                if not (800 <= presion <= 1100):
                    respuesta = messagebox.askokcancel(
                        "Advertencia", 
                        f"El valor de presión ({presion} hPa) está fuera del rango normal (800-1100 hPa).\n\n¿Desea continuar de todos modos?"
                    )
                    if not respuesta:
                        return
                
                if temperatura < -50 or temperatura > 70:
                    respuesta = messagebox.askokcancel(
                        "Advertencia", 
                        f"La temperatura ({temperatura} °C) está fuera del rango normal (-50 a 70 °C).\n\n¿Desea continuar de todos modos?"
                    )
                    if not respuesta:
                        return
                
                if energia < 0 or energia > 2000:
                    respuesta = messagebox.askokcancel(
                        "Advertencia", 
                        f"El valor de energía ({energia} W) parece inusual.\n\n¿Desea continuar de todos modos?"
                    )
                    if not respuesta:
                        return
            
            except tk.TclError:
                messagebox.showerror("Error", "Todos los campos numéricos deben contener valores válidos.")
                return
            
            # Procesar la fila usando la misma función que con archivos
            fecha, hora, temperatura, humedad, presion, energia = self.procesar_fila(fila_datos)
            
            # Preparar los datos para guardarlos
            datos = {
                'Fecha': fecha,
                'Hora': hora,
                'Temperatura': temperatura,
                'Humedad': humedad,
                'Presion': presion,
                'Energia': energia
            }
            
            # Añadir a la lista de datos ingresados
            datos_ingresados.append(datos)
            
            # Mostrar en la listbox
            data_listbox.insert(tk.END, f"{fecha}, {hora}, {temperatura}°C, {humedad}%, {presion}hPa, {energia}W")
            
            # Limpiar los campos para un nuevo ingreso
            fecha_var.set("")
            hora_var.set("")
            temperatura_var.set(0.0)
            humedad_var.set(0.0)
            presion_var.set(0.0)
            energia_var.set(0.0)
            
            # Enfocar el primer campo para facilitar el siguiente ingreso
            fecha_entry.focus_set()
        
        # Función para finalizar y guardar todos los datos
        def finalizar_carga():
            if not datos_ingresados:
                messagebox.showwarning("Advertencia", "No ha ingresado ningún dato.")
                return
                
            # Guardar todos los datos en el archivo CSV
            archivo_existe = os.path.isfile("datos.csv")
            
            try:
                with open("datos.csv", mode='a', newline='') as archivo:
                    escritor = csv.DictWriter(archivo, fieldnames=['Fecha', 'Hora', 'Temperatura', 'Humedad', 'Presion', 'Energia'])
                    
                    # Escribir encabezados solo si el archivo es nuevo
                    if not archivo_existe:
                        escritor.writeheader()
                    
                    # Escribir todos los datos
                    for datos in datos_ingresados:
                        escritor.writerow(datos)
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Éxito", f"Se guardaron {len(datos_ingresados)} registros en 'datos.csv'")
                
                # Preparar los datos para análisis
                fechas = [datos['Fecha'] for datos in datos_ingresados]
                horas = [datos['Hora'] for datos in datos_ingresados]
                temperaturas = [datos['Temperatura'] for datos in datos_ingresados]
                humedades = [datos['Humedad'] for datos in datos_ingresados]
                presiones = [datos['Presion'] for datos in datos_ingresados]
                energias = [datos['Energia'] for datos in datos_ingresados]
                
                # Guardar los datos procesados para su uso posterior
                self.datos_procesados = {
                    'fechas': fechas,
                    'horas': horas,
                    'temperaturas': temperaturas,
                    'humedades': humedades,
                    'presiones': presiones,
                    'energias': energias
                }
                
                # Cerrar la ventana
                manual_window.destroy()
                
                # Mostrar análisis
                self.mostrar_analisis_datos()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron guardar los datos:\n{str(e)}")
        
        # Botones de acción
        añadir_btn = ttk.Button(buttons_frame, text="Añadir Datos", command=añadir_datos)
        añadir_btn.pack(side="left", padx=10)
        
        finalizar_btn = ttk.Button(buttons_frame, text="Finalizar y Guardar", command=finalizar_carga)
        finalizar_btn.pack(side="left", padx=10)
        
        cancelar_btn = ttk.Button(buttons_frame, text="Cancelar", command=manual_window.destroy)
        cancelar_btn.pack(side="right", padx=10)
        
        # Centrar la ventana en la pantalla
        manual_window.update_idletasks()
        width = manual_window.winfo_width()
        height = manual_window.winfo_height()
        x = (manual_window.winfo_screenwidth() // 2) - (width // 2)
        y = (manual_window.winfo_screenheight() // 2) - (height // 2)
        manual_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Enfocar el primer campo
        fecha_entry.focus_set()
    
    def guardar_en_csv(self, datos):
        """Guarda los datos en un archivo CSV."""
        # Determinar si el archivo ya existe para saber si añadir encabezados
        archivo_existe = os.path.isfile("datos.csv")
        
        try:
            with open("datos.csv", mode='a', newline='') as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=['Fecha', 'Hora', 'Temperatura', 'Humedad', 'Presion', 'Energia'])
                
                # Escribir encabezados solo si el archivo es nuevo
                if not archivo_existe:
                    escritor.writeheader()
                
                # Escribir los datos
                escritor.writerow(datos)
            
            messagebox.showinfo("Éxito", "Datos guardados correctamente en 'datos.csv'")
            
            # Procesar los datos como si vinieran de un archivo
            fechas = [datos['Fecha']]
            horas = [datos['Hora']]
            temperaturas = [datos['Temperatura']]
            humedades = [datos['Humedad']]
            presiones = [datos['Presion']]
            energias = [datos['Energia']]
            
            # Guardar los datos procesados para su uso posterior
            self.datos_procesados = {
                'fechas': fechas,
                'horas': horas,
                'temperaturas': temperaturas,
                'humedades': humedades,
                'presiones': presiones,
                'energias': energias
            }
            
            # Mostrar análisis
            self.mostrar_analisis_datos()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los datos:\n{str(e)}")
    
    def open_file_input(self):
        # Abrir diálogo para seleccionar archivo
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de datos",
            filetypes=[
                ("Archivos de datos", "*.csv *.xlsx *.xls"),
                ("Archivos CSV", "*.csv"),
                ("Archivos Excel", "*.xlsx *.xls"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        # Si el usuario canceló la selección
        if not file_path:
            return
            
        # Verificar extensión del archivo
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.csv':
                # Usar el proceso de validación específico para archivos CSV
                fechas, horas, temperaturas, humedades, presiones, energias = self.leer_datos(file_path)
                
            elif file_extension in ['.xlsx', '.xls']:
                # Para archivos Excel, convertirlos a un DataFrame y luego procesar
                df = pd.read_excel(file_path)
                # Guardar temporalmente como CSV para procesarlo con las funciones de validación
                temp_csv = os.path.join(os.path.dirname(file_path), "temp_data.csv")
                df.to_csv(temp_csv, index=False)
                
                # Procesar el CSV temporal
                fechas, horas, temperaturas, humedades, presiones, energias = self.leer_datos(temp_csv)
                
                # Eliminar el archivo temporal
                os.remove(temp_csv)
            else:
                messagebox.showerror("Error", "Formato de archivo no soportado.\nPor favor seleccione un archivo CSV o Excel.")
                return
                
            # Mostrar resultados
            num_registros = len(fechas)
            if num_registros > 0:
                # Guardar los datos procesados para su uso posterior
                self.datos_procesados = {
                    'fechas': fechas,
                    'horas': horas,
                    'temperaturas': temperaturas,
                    'humedades': humedades,
                    'presiones': presiones,
                    'energias': energias
                }
                
                # Mostrar ventana con los datos cargados
                self.mostrar_datos_cargados_desde_archivo(self.datos_procesados)
            else:
                messagebox.showwarning("Advertencia", "No se encontraron datos válidos en el archivo.")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo:\n{str(e)}")
    
    def mostrar_datos_cargados_desde_archivo(self, datos):
        # Crear una ventana para mostrar los datos cargados
        data_window = tk.Toplevel(self.root)
        data_window.title("Datos Cargados desde Archivo")
        data_window.geometry("800x600")  # Hacer la ventana más grande para mostrar más datos
        data_window.transient(self.root)  # Hace que la ventana sea modal
        
        # Marco principal
        main_frame = tk.Frame(data_window, padx=20, pady=20, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        # Título con el número de registros
        num_registros = len(datos['fechas'])
        title_label = ttk.Label(
            main_frame, 
            text=f"Datos Cargados: {num_registros} Registros", 
            style="Title.TLabel",
            background="#f0f0f0"
        )
        title_label.pack(pady=(0, 20))
        
        # Panel con pestañas para diferentes vistas
        tab_control = ttk.Notebook(main_frame)
        
        # Pestaña 1: Vista de Lista
        list_tab = tk.Frame(tab_control, bg="#f0f0f0")
        tab_control.add(list_tab, text="Vista de Lista")
        
        # Crear un marco con scroll para la lista de datos
        list_frame = tk.Frame(list_tab, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear un Canvas con scrollbar para manejar muchos registros
        canvas = tk.Canvas(list_frame, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        
        # Frame que contendrá la lista dentro del canvas
        data_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        # Configurar el canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Crear una ventana en el canvas que contiene el data_frame
        canvas_window = canvas.create_window((0, 0), window=data_frame, anchor="nw")
        
        # Configurar eventos de scroll con la rueda del ratón
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        # Vincular la rueda del ratón al canvas
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Asegurar que se desvincula el evento cuando se cierra la ventana
        def _on_closing():
            canvas.unbind_all("<MouseWheel>")
            data_window.destroy()
            
        data_window.protocol("WM_DELETE_WINDOW", _on_closing)
        
        # Ajustar el ancho del frame cuando cambia el tamaño del canvas
        def _configure_data_frame(event):
            # Actualizar el ancho de la ventana del canvas al ancho del canvas
            canvas.itemconfig(canvas_window, width=event.width)
            
        canvas.bind('<Configure>', _configure_data_frame)
        
        # Encabezados de tabla
        headers = ["Fecha", "Hora", "Temperatura (°C)", "Humedad (%)", "Presión (hPa)", "Energía (W)"]
        for i, header in enumerate(headers):
            tk.Label(data_frame, text=header, bg="#e0e0e0", font=("Arial", 10, "bold"), 
                    width=15, relief=tk.RIDGE).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        
        # Insertar datos en la tabla
        for i in range(num_registros):
            # Limitamos a mostrar los primeros 200 registros por rendimiento
            if i >= 200:
                tk.Label(data_frame, text=f"... y {num_registros-200} registros más", 
                       bg="#f0f0f0", font=("Arial", 10, "italic")).grid(
                       row=i+1, column=0, columnspan=len(headers), pady=10)
                break
            
            # Fecha
            tk.Label(data_frame, text=datos['fechas'][i], bg="white", width=15).grid(
                row=i+1, column=0, sticky="nsew", padx=1, pady=1)
            
            # Hora
            tk.Label(data_frame, text=datos['horas'][i], bg="white", width=15).grid(
                row=i+1, column=1, sticky="nsew", padx=1, pady=1)
            
            # Temperatura
            tk.Label(data_frame, text=f"{datos['temperaturas'][i]:.1f}", bg="white", width=15).grid(
                row=i+1, column=2, sticky="nsew", padx=1, pady=1)
            
            # Humedad
            tk.Label(data_frame, text=f"{datos['humedades'][i]:.1f}", bg="white", width=15).grid(
                row=i+1, column=3, sticky="nsew", padx=1, pady=1)
            
            # Presión
            tk.Label(data_frame, text=f"{datos['presiones'][i]:.1f}", bg="white", width=15).grid(
                row=i+1, column=4, sticky="nsew", padx=1, pady=1)
            
            # Energía
            tk.Label(data_frame, text=f"{datos['energias'][i]:.1f}", bg="white", width=15).grid(
                row=i+1, column=5, sticky="nsew", padx=1, pady=1)
        
        # Pestaña 2: Resumen Estadístico
        stats_tab = tk.Frame(tab_control, bg="#f0f0f0")
        tab_control.add(stats_tab, text="Resumen Estadístico")
        
        # Marco para el resumen
        stats_frame = tk.Frame(stats_tab, bg="#f0f0f0", padx=20, pady=20)
        stats_frame.pack(fill="both", expand=True)
        
        # Calcular estadísticas básicas
        def calcular_estadisticas(valores):
            import numpy as np
            return {
                'min': min(valores),
                'max': max(valores),
                'promedio': sum(valores) / len(valores),
                'mediana': sorted(valores)[len(valores) // 2],
                'desv_est': np.std(valores) if 'numpy' in sys.modules else 0
            }
        
        # Estadísticas para cada tipo de dato
        temp_stats = calcular_estadisticas(datos['temperaturas'])
        hum_stats = calcular_estadisticas(datos['humedades'])
        pres_stats = calcular_estadisticas(datos['presiones'])
        ener_stats = calcular_estadisticas(datos['energias'])
        
        # Mostrar estadísticas en una tabla
        tk.Label(stats_frame, text="Variable", bg="#e0e0e0", font=("Arial", 10, "bold"), 
                width=15, relief=tk.RIDGE).grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text="Mínimo", bg="#e0e0e0", font=("Arial", 10, "bold"), 
                width=10, relief=tk.RIDGE).grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text="Máximo", bg="#e0e0e0", font=("Arial", 10, "bold"), 
                width=10, relief=tk.RIDGE).grid(row=0, column=2, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text="Promedio", bg="#e0e0e0", font=("Arial", 10, "bold"), 
                width=10, relief=tk.RIDGE).grid(row=0, column=3, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text="Mediana", bg="#e0e0e0", font=("Arial", 10, "bold"), 
                width=10, relief=tk.RIDGE).grid(row=0, column=4, sticky="nsew", padx=1, pady=1)
        
        # Temperatura
        tk.Label(stats_frame, text="Temperatura (°C)", bg="white", width=15).grid(
            row=1, column=0, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{temp_stats['min']:.1f}", bg="white", width=10).grid(
            row=1, column=1, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{temp_stats['max']:.1f}", bg="white", width=10).grid(
            row=1, column=2, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{temp_stats['promedio']:.1f}", bg="white", width=10).grid(
            row=1, column=3, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{temp_stats['mediana']:.1f}", bg="white", width=10).grid(
            row=1, column=4, sticky="nsew", padx=1, pady=1)
        
        # Humedad
        tk.Label(stats_frame, text="Humedad (%)", bg="white", width=15).grid(
            row=2, column=0, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{hum_stats['min']:.1f}", bg="white", width=10).grid(
            row=2, column=1, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{hum_stats['max']:.1f}", bg="white", width=10).grid(
            row=2, column=2, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{hum_stats['promedio']:.1f}", bg="white", width=10).grid(
            row=2, column=3, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{hum_stats['mediana']:.1f}", bg="white", width=10).grid(
            row=2, column=4, sticky="nsew", padx=1, pady=1)
        
        # Presión
        tk.Label(stats_frame, text="Presión (hPa)", bg="white", width=15).grid(
            row=3, column=0, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{pres_stats['min']:.1f}", bg="white", width=10).grid(
            row=3, column=1, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{pres_stats['max']:.1f}", bg="white", width=10).grid(
            row=3, column=2, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{pres_stats['promedio']:.1f}", bg="white", width=10).grid(
            row=3, column=3, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{pres_stats['mediana']:.1f}", bg="white", width=10).grid(
            row=3, column=4, sticky="nsew", padx=1, pady=1)
        
        # Energía
        tk.Label(stats_frame, text="Energía (W)", bg="white", width=15).grid(
            row=4, column=0, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{ener_stats['min']:.1f}", bg="white", width=10).grid(
            row=4, column=1, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{ener_stats['max']:.1f}", bg="white", width=10).grid(
            row=4, column=2, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{ener_stats['promedio']:.1f}", bg="white", width=10).grid(
            row=4, column=3, sticky="nsew", padx=1, pady=1)
        tk.Label(stats_frame, text=f"{ener_stats['mediana']:.1f}", bg="white", width=10).grid(
            row=4, column=4, sticky="nsew", padx=1, pady=1)
        
        # Configurar el tamaño adecuado del canvas
        data_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Mostrar el control de pestañas
        tab_control.pack(expand=1, fill="both")
        
        # Botones de acción en la parte inferior
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(pady=10, side="bottom", fill="x")
        
        # Función para proceder al análisis
        def continuar_analisis():
            data_window.destroy()
            self.mostrar_analisis_datos()
        
        # Botón para ir a análisis
        analisis_btn = ttk.Button(buttons_frame, text="Continuar con análisis", command=continuar_analisis)
        analisis_btn.pack(side="left", padx=10)
        
        # Botón para cerrar
        cerrar_btn = ttk.Button(buttons_frame, text="Cerrar", command=data_window.destroy)
        cerrar_btn.pack(side="right", padx=10)
        
        # Mensaje informativo
        info_label = ttk.Label(
            main_frame,
            text="Se muestran hasta 200 registros. Use las pestañas para ver diferentes vistas de los datos.",
            foreground="gray",
            background="#f0f0f0"
        )
        info_label.pack(side="bottom", pady=5)
    
    # Funciones de validación y procesamiento de datos
    def es_bisiesto(self, anho):
        return (anho % 4 == 0 and anho % 100 != 0) or (anho % 400 == 0)
    
    def validar_fecha(self, fecha_str):
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
        dias_por_mes = [31, 29 if self.es_bisiesto(anho) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return 1 <= dia <= dias_por_mes[mes - 1]
    
    def validar_hora(self, hora_str):
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
    
    def validar_datos(self, fila):
        try:
            if not self.validar_fecha(fila['Fecha']):
                return False
            if not self.validar_hora(fila['Hora']):
                return False
            float(fila['Temperatura'])
            float(fila['Humedad'])
            float(fila['Presion'])
            float(fila['Energia'])
            return True
        except (ValueError, KeyError):
            return False
    
    def procesar_fila(self, fila):
        fecha = fila['Fecha']
        hora = fila['Hora']
        temperatura = float(fila['Temperatura'])
        humedad = float(fila['Humedad'])
        presion = float(fila['Presion'])
        energia = float(fila['Energia'])
        return fecha, hora, temperatura, humedad, presion, energia
    
    def leer_datos(self, archivo):
        fechas = []
        horas = []
        temperaturas = []
        humedades = []
        presiones = []
        energias = []
        
        with open(archivo, mode='r') as file:
            reader = csv.DictReader(file)
            for fila in reader:
                if self.validar_datos(fila):
                    fecha, hora, temperatura, humedad, presion, energia = self.procesar_fila(fila)
                    fechas.append(fecha)
                    horas.append(hora)
                    temperaturas.append(temperatura)
                    humedades.append(humedad)
                    presiones.append(presion)
                    energias.append(energia)
                else:
                    print(f"Fila ignorada por datos inválidos: {fila}")
        
        return fechas, horas, temperaturas, humedades, presiones, energias
    def mostrar_analisis_datos(self):
        # Importaciones necesarias para análisis
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import numpy as np
            from datetime import datetime
            # Eliminadas importaciones de sklearn (LinearRegression, r2_score, StandardScaler)
        except ImportError:
            messagebox.showerror("Error", "Se requieren bibliotecas adicionales para el análisis.\n\nPor favor instale matplotlib y numpy con:\npip install matplotlib numpy")
            return
        
        # Crear ventana para mostrar análisis
        analisis_window = tk.Toplevel(self.root)
        analisis_window.title("Análisis de Datos Solares")
        analisis_window.geometry("1200x800")  # Ventana más grande para los gráficos
        analisis_window.state('zoomed')  # Maximizar ventana en Windows
        
        # Crear notebook para pestañas
        tab_control = ttk.Notebook(analisis_window)
        
        # Pestaña 1: Energía vs Tiempo
        energia_tiempo_tab = ttk.Frame(tab_control)
        tab_control.add(energia_tiempo_tab, text="Energía vs Tiempo")
        
        # Pestaña 2: Temperatura vs Energía
        temp_energia_tab = ttk.Frame(tab_control)
        tab_control.add(temp_energia_tab, text="Temperatura vs Energía")
        
        # Pestaña 3: Presión vs Energía
        presion_energia_tab = ttk.Frame(tab_control)
        tab_control.add(presion_energia_tab, text="Presión vs Energía")
        
        # Pestaña 4: Humedad vs Energía
        humedad_energia_tab = ttk.Frame(tab_control)
        tab_control.add(humedad_energia_tab, text="Humedad vs Energía")
        
        # Pestaña 5: Energía por hora del día
        energia_hora_tab = ttk.Frame(tab_control)
        tab_control.add(energia_hora_tab, text="Energía por Hora")
        
        # Pestaña 6: Datos Estadísticos
        datos_tab = ttk.Frame(tab_control)
        tab_control.add(datos_tab, text="Estadísticas")
        
        # Mostrar el notebook
        tab_control.pack(expand=1, fill="both")
        
        # Extraer datos
        temperaturas = np.array(self.datos_procesados['temperaturas'])
        humedades = np.array(self.datos_procesados['humedades'])
        presiones = np.array(self.datos_procesados['presiones'])
        energias = np.array(self.datos_procesados['energias'])
        fechas = self.datos_procesados['fechas']
        horas = self.datos_procesados['horas']
        
        # ---------- PESTAÑA 1: ENERGÍA VS TIEMPO ----------
        # Convertir fechas y horas a objetos datetime
        fecha_hora = []
        for fecha, hora in zip(fechas, horas):
            fecha_hora_str = f"{fecha} {hora}"
            fecha_hora_obj = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M:%S")
            fecha_hora.append(fecha_hora_obj)
        
        etiquetas_fecha = [dt.strftime("%d/%m %H:%M") for dt in fecha_hora]
        
        # Crear figura para el gráfico de energía vs tiempo
        fig_energia_tiempo = plt.figure(figsize=(12, 6))
        ax = fig_energia_tiempo.add_subplot(111)
        
        # Crear barras
        bars = ax.bar(range(len(energias)), energias, width=0.8, color='green')
        
        # Configurar etiquetas del eje X
        ax.set_xticks(range(len(energias)))
        ax.set_xticklabels(etiquetas_fecha, rotation=45)
        
        # Títulos y etiquetas
        ax.set_title('Energía generada en función del tiempo')
        ax.set_xlabel('Fecha y Hora')
        ax.set_ylabel('Energía (W)')
        ax.grid(axis='y')
        
        # Mostrar valores sobre las barras si hay pocos datos
        if len(energias) <= 20:
            for i, valor in enumerate(energias):
                ax.text(i, valor + 0.5, f"{valor:.1f}", ha='center', va='bottom', fontsize=9)
        
        fig_energia_tiempo.tight_layout()
        
        # Agregar el gráfico al frame
        canvas_energia_tiempo = FigureCanvasTkAgg(fig_energia_tiempo, energia_tiempo_tab)
        canvas_energia_tiempo.draw()
        canvas_energia_tiempo.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ---------- PESTAÑA 2: TEMPERATURA VS ENERGÍA ----------
        fig_temp_energia = plt.figure(figsize=(10, 6))
        ax_temp = fig_temp_energia.add_subplot(111)
        
        # Crear el gráfico de dispersión
        ax_temp.scatter(temperaturas, energias, alpha=0.7, color='red')
        
        # Añadir línea de tendencia si hay más de un punto
        if len(temperaturas) > 1:
            coef = np.polyfit(temperaturas, energias, 1)
            polinomio = np.poly1d(coef)
            x_tendencia = np.linspace(min(temperaturas), max(temperaturas), 100)
            ax_temp.plot(x_tendencia, polinomio(x_tendencia), 'b--', 
                     label=f'Tendencia: {coef[0]:.2f}x + {coef[1]:.2f}')
            ax_temp.legend()
        
        # Configurar títulos y etiquetas
        ax_temp.set_title('Relación entre Temperatura y Energía')
        ax_temp.set_xlabel('Temperatura (°C)')
        ax_temp.set_ylabel('Energía (W)')
        ax_temp.grid(True)
        
        fig_temp_energia.tight_layout()
        
        # Agregar el gráfico al frame
        canvas_temp_energia = FigureCanvasTkAgg(fig_temp_energia, temp_energia_tab)
        canvas_temp_energia.draw()
        canvas_temp_energia.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ---------- PESTAÑA 3: PRESIÓN VS ENERGÍA ----------
        fig_presion_energia = plt.figure(figsize=(10, 6))
        ax_presion = fig_presion_energia.add_subplot(111)
        
        # Crear el gráfico de dispersión
        ax_presion.scatter(presiones, energias, alpha=0.7, color='purple')
        
        # Añadir línea de tendencia si hay más de un punto
        if len(presiones) > 1:
            coef = np.polyfit(presiones, energias, 1)
            polinomio = np.poly1d(coef)
            x_tendencia = np.linspace(min(presiones), max(presiones), 100)
            ax_presion.plot(x_tendencia, polinomio(x_tendencia), 'b--', 
                     label=f'Tendencia: {coef[0]:.2f}x + {coef[1]:.2f}')
            ax_presion.legend()
        
        # Configurar títulos y etiquetas
        ax_presion.set_title('Relación entre Presión y Energía')
        ax_presion.set_xlabel('Presión (hPa)')
        ax_presion.set_ylabel('Energía (W)')
        ax_presion.grid(True)
        
        fig_presion_energia.tight_layout()
        
        # Agregar el gráfico al frame
        canvas_presion_energia = FigureCanvasTkAgg(fig_presion_energia, presion_energia_tab)
        canvas_presion_energia.draw()
        canvas_presion_energia.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ---------- PESTAÑA 4: HUMEDAD VS ENERGÍA ----------
        fig_humedad_energia = plt.figure(figsize=(10, 6))
        ax_humedad = fig_humedad_energia.add_subplot(111)
        
        # Crear el gráfico de dispersión
        ax_humedad.scatter(humedades, energias, alpha=0.7, color='blue')
        
        # Añadir línea de tendencia si hay más de un punto
        if len(humedades) > 1:
            coef = np.polyfit(humedades, energias, 1)
            polinomio = np.poly1d(coef)
            x_tendencia = np.linspace(min(humedades), max(humedades), 100)
            ax_humedad.plot(x_tendencia, polinomio(x_tendencia), 'r--', 
                     label=f'Tendencia: {coef[0]:.2f}x + {coef[1]:.2f}')
            ax_humedad.legend()
        
        # Configurar títulos y etiquetas
        ax_humedad.set_title('Relación entre Humedad y Energía')
        ax_humedad.set_xlabel('Humedad (%)')
        ax_humedad.set_ylabel('Energía (W)')
        ax_humedad.grid(True)
        
        fig_humedad_energia.tight_layout()
        
        # Agregar el gráfico al frame
        canvas_humedad_energia = FigureCanvasTkAgg(fig_humedad_energia, humedad_energia_tab)
        canvas_humedad_energia.draw()
        canvas_humedad_energia.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ---------- PESTAÑA 5: ENERGÍA POR HORA DEL DÍA ----------
        # Extraer las horas del día y agrupar la energía por hora
        horas_del_dia = [datetime.strptime(hora, "%H:%M:%S").hour for hora in horas]
        energia_por_hora = {}
        
        for hora, energia in zip(horas_del_dia, energias):
            if hora not in energia_por_hora:
                energia_por_hora[hora] = []
            energia_por_hora[hora].append(energia)
        
        # Calcular el promedio de energía para cada hora
        horas_ordenadas = sorted(energia_por_hora.keys())
        energia_promedio = [sum(energia_por_hora[h])/len(energia_por_hora[h]) for h in horas_ordenadas]
        
        fig_energia_hora = plt.figure(figsize=(12, 6))
        ax_hora = fig_energia_hora.add_subplot(111)
        
        # Crear barras
        ax_hora.bar(horas_ordenadas, energia_promedio, width=0.7, color='orange')
        
        # Configurar títulos y etiquetas
        ax_hora.set_title('Energía Promedio por Hora del Día')
        ax_hora.set_xlabel('Hora del Día')
        ax_hora.set_ylabel('Energía Promedio (W)')
        ax_hora.set_xticks(range(0, 24))
        ax_hora.grid(axis='y')
        
        fig_energia_hora.tight_layout()
        
        # Agregar el gráfico al frame
        canvas_energia_hora = FigureCanvasTkAgg(fig_energia_hora, energia_hora_tab)
        canvas_energia_hora.draw()
        canvas_energia_hora.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ---------- PESTAÑA 3: DATOS Y ESTADÍSTICAS ----------
        # Crear un frame con scrollbar para la tabla
        datos_frame = ttk.Frame(datos_tab)
        datos_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear un Canvas con scrollbar para manejar muchos registros
        canvas = tk.Canvas(datos_frame)
        scrollbar = ttk.Scrollbar(datos_frame, orient="vertical", command=canvas.yview)
        
        # Frame que contendrá la tabla dentro del canvas
        tabla_frame = tk.Frame(canvas)
        
        # Configurar el canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Crear una ventana en el canvas que contiene el tabla_frame
        canvas_window = canvas.create_window((0, 0), window=tabla_frame, anchor="nw")
        
        # Configurar eventos de scroll con la rueda del ratón
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        # Vincular la rueda del ratón al canvas
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Asegurar que se desvincula el evento cuando se cierra la ventana
        def _on_closing():
            canvas.unbind_all("<MouseWheel>")
            analisis_window.destroy()
            
        analisis_window.protocol("WM_DELETE_WINDOW", _on_closing)
        
        # Ajustar el ancho del frame cuando cambia el tamaño del canvas
        def _configure_tabla_frame(event):
            # Actualizar el ancho de la ventana del canvas al ancho del canvas
            canvas.itemconfig(canvas_window, width=event.width)
            
        canvas.bind('<Configure>', _configure_tabla_frame)
        
        # Calcular estadísticas para mostrar en tabla
        stats = {
            'Temperatura': {
                'min': min(temperaturas),
                'max': max(temperaturas),
                'mean': np.mean(temperaturas),
                'median': np.median(temperaturas),
                'std': np.std(temperaturas)
            },
            'Humedad': {
                'min': min(humedades),
                'max': max(humedades),
                'mean': np.mean(humedades),
                'median': np.median(humedades),
                'std': np.std(humedades)
            },
            'Presión': {
                'min': min(presiones),
                'max': max(presiones),
                'mean': np.mean(presiones),
                'median': np.median(presiones),
                'std': np.std(presiones)
            },
            'Energía': {
                'min': min(energias),
                'max': max(energias),
                'mean': np.mean(energias),
                'median': np.median(energias),
                'std': np.std(energias)
            }
        }
        
        # Crear tabla de estadísticas
        stats_label = ttk.Label(tabla_frame, text="Estadísticas Descriptivas", font=("Arial", 12, "bold"))
        stats_label.grid(row=0, column=0, columnspan=6, pady=10)
        
        # Encabezados de tabla de estadísticas
        headers = ["Variable", "Mínimo", "Máximo", "Media", "Mediana", "Desv. Est."]
        for i, header in enumerate(headers):
            tk.Label(tabla_frame, text=header, bg="#e0e0e0", font=("Arial", 10, "bold"), 
                    width=15, relief=tk.RIDGE).grid(row=1, column=i, sticky="nsew", padx=1, pady=1)
        
        # Llenar tabla de estadísticas
        row = 2
        for var_name, var_stats in stats.items():
            tk.Label(tabla_frame, text=var_name, bg="white", width=15).grid(
                row=row, column=0, sticky="nsew", padx=1, pady=1)
            tk.Label(tabla_frame, text=f"{var_stats['min']:.2f}", bg="white", width=15).grid(
                row=row, column=1, sticky="nsew", padx=1, pady=1)
            tk.Label(tabla_frame, text=f"{var_stats['max']:.2f}", bg="white", width=15).grid(
                row=row, column=2, sticky="nsew", padx=1, pady=1)
            tk.Label(tabla_frame, text=f"{var_stats['mean']:.2f}", bg="white", width=15).grid(
                row=row, column=3, sticky="nsew", padx=1, pady=1)
            tk.Label(tabla_frame, text=f"{var_stats['median']:.2f}", bg="white", width=15).grid(
                row=row, column=4, sticky="nsew", padx=1, pady=1)
            tk.Label(tabla_frame, text=f"{var_stats['std']:.2f}", bg="white", width=15).grid(
                row=row, column=5, sticky="nsew", padx=1, pady=1)
            row += 1
        
        # Ajustar el tamaño del canvas al contenido
        tabla_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Análisis Completo", 
                          "El análisis de los datos se ha completado correctamente.\n\n"
                          "Utilice las pestañas para explorar los diferentes tipos de análisis.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.exit_app)
    root.mainloop()
