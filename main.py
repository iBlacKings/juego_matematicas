import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import random
from datetime import datetime
import re
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


global usuario_registrado 
usuario_registrado = False

# Cargar datos de vuelos
def cargar_vuelos():
    vuelos = []
    with open('Datos_Vuelos _Finales.txt') as f:
        for line in f:
            if line.startswith('['):
                data = line.strip()[1:-1].replace("'", "").split(', ')
                vuelo = {
                    'codigo': data[0],
                    'fecha': data[1],
                    'hora_salida': data[2],
                    'hora_llegada': data[3],
                    'valor_min': int(data[4]),
                    'valor_medio': int(data[5]),
                    'valor_max': int(data[6]),
                    'origen': data[7],
                    'destino': data[8]
                }
                vuelos.append(vuelo)
    return vuelos

# Generar código de pasajero
def generar_codigo_pasajero(nombre):
    return f"{nombre[0].upper()}-{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))}"

# Validar correo electrónico
def validar_correo(correo):
    return re.match(r"[^@]+@[^@]+\.[^@]+", correo)

# Validar número de tarjeta
def validar_tarjeta(numero):
    return re.match(r"^\d{16}$", numero)

# Validar CVV
def validar_cvv(cvv):
    return re.match(r"^\d{3}$", cvv)

# Validar número celular en Colombia
def validar_numero_celular(numero):
    return re.match(r"^\d{10}$", numero)

# Limpiar ventana
def limpiar_ventana(root):
    for widget in root.winfo_children():
        widget.destroy()

# Crear interfaz inicial
def crear_interfaz_inicial(root):
    global imagen_tk

    limpiar_ventana(root)
    root.title("LA AIRLINES")
    ventana_width = 860
    ventana_height = 500

    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()
        
    center_x = int(pantalla_width/2 - ventana_width/2)
    
    center_y = int(pantalla_height/2 - ventana_height/2)

    root.geometry(f"{ventana_width}x{ventana_height}+{center_x}+{center_y}")
    root.resizable(False, False)
    root.state("normal")

    frame = tk.Frame(root, bg="white")
    frame.pack(pady=20)

    imagen = Image.open("logo.png")
    imagen = imagen.resize((260, 170))
    imagen_tk = ImageTk.PhotoImage(imagen)
    imgenlabel = tk.Label(frame, image=imagen_tk, text="", bg="white")
    imgenlabel.grid(row=0, column=1, padx=10, pady=10)
    
    ctk.CTkLabel(frame, text="LA AIRLINES", text_color="#C00A41", font=("Comic Sans MS", 50, "bold")).grid(row=1, column=1, padx=10, pady=10)
    ctk.CTkLabel(frame, text="").grid(row=2, column=1, padx=10, pady=10)

    ctk.CTkButton(frame, text="Registrarse", fg_color="#C00A41",bg_color="white", font=("Comic Sans MS", 15) ,command=lambda: registrar_usuario(root)).grid(row=3, column=0, padx=10, pady=10, )
    ctk.CTkButton(frame, text="Agendar Vuelo", fg_color="#C00A41",bg_color="white", font=("Comic Sans MS", 15), command=lambda: mostrar_interfaz_agendar_vuelo(root)).grid(row=3, column=1, padx=10, pady=10, )
    ctk.CTkButton(frame, text="Check-in",fg_color="#C00A41",bg_color="white", font=("Comic Sans MS", 15), command=lambda: check_in(root)).grid(row=3, column=2, padx=10, pady=10)

def mostrar_interfaz_agendar_vuelo(root):
    global imagen_tkper, servicio_var
    if not usuario_registrado:
        messagebox.showwarning("Advertencia", "Debe registrarse antes de agendar un vuelo.")
        return

    limpiar_ventana(root)
    root.title("Agendar Vuelo")
    root.state("zoomed")

    ctk.CTkLabel(root, text="Agendar Vuelo", text_color="black", font=("Comic Sans MS", 20)).pack(pady=10)
    frame = ctk.CTkFrame(root, border_color="#C00A41", border_width=4, bg_color="white", fg_color="white")
    frame.pack(pady=20)

    ctk.CTkLabel(frame, text="Origen", text_color="black", font=("Comic Sans MS", 15)).grid(row=1, column=0, padx=10, pady=5)
    origen_var = tk.StringVar()
    origen_menu = ttk.Combobox(frame, textvariable=origen_var, font=("Comic Sans MS", 12), state="readonly", background="white")
    origen_menu['values'] = origenes
    origen_menu.grid(row=2, column=0, padx=10, pady=5)
    origen_menu.bind("<<ComboboxSelected>>", lambda event: actualizar_destinos(origen_var, destino_menu))

    ctk.CTkLabel(frame, text="Destino", text_color="black", font=("Comic Sans MS", 15)).grid(row=1, column=1, padx=10, pady=5)
    destino_var = tk.StringVar()
    destino_menu = ttk.Combobox(frame, textvariable=destino_var, font=("Comic Sans MS", 12), state="readonly", background="white")
    destino_menu.grid(row=2, column=1, padx=10, pady=5)
    destino_menu.bind("<<ComboboxSelected>>", lambda event: actualizar_fechas(origen_var, destino_var, fecha_menu))

    ctk.CTkLabel(frame, text="Fecha ida", text_color="black", font=("Comic Sans MS", 15)).grid(row=1, column=2, padx=10, pady=5)
    fecha_var = tk.StringVar()
    fecha_menu = ttk.Combobox(frame, textvariable=fecha_var, font=("Comic Sans MS", 12), state="readonly", background="white")
    fecha_menu.grid(row=2, column=2, padx=10, pady=5)
    fecha_menu.bind("<<ComboboxSelected>>", lambda event: actualizar_horas_salida(origen_var, destino_var, fecha_var, hora_salida_menu))

    ctk.CTkLabel(frame, text="Hora Salida",text_color="black", font=("Comic Sans MS", 15)).grid(row=3, column=0, padx=10, pady=5)
    hora_salida_var = tk.StringVar()
    hora_salida_menu = ttk.Combobox(frame,state="readonly" ,textvariable=hora_salida_var)
    hora_salida_menu.grid(row=3, column=1, padx=10, pady=5)
    hora_salida_menu.bind("<<ComboboxSelected>>", lambda event: actualizar_hora_llegada(origen_var, destino_var, fecha_var, hora_salida_var, hora_llegada_var))

    ctk.CTkLabel(frame, text="Hora Llegada", text_color="black", font=("Comic Sans MS", 15)).grid(row=4, column=0, padx=10, pady=5)
    hora_llegada_var = tk.StringVar()
    hora_llegada_entry = ttk.Combobox(frame, textvariable=hora_llegada_var, state="disabled")
    hora_llegada_entry.grid(row=4, column=1, padx=10, pady=5)


    imagenper = Image.open("cantidad.png")
    imagenper = imagenper.resize((30, 30))
    imagen_tkper = ImageTk.PhotoImage(imagenper)
    imgenlabelper = tk.Label(frame, image=imagen_tkper, text="", bg="white")
    imgenlabelper.grid(row=0, column=4, padx=10, pady=10)
    
    cantidad_personas = tk.Entry(frame, width=2, font=("Comic Sans MS", 12))
    cantidad_personas.grid(row=0, column=5, padx=10, pady=5)
    cantidad_personas.insert(0,"1")  # Establece el valor inicial a 1
    cantidad_personas.config(state='disabled')  # Deshabilita la entrada

    ctk.CTkLabel(frame, text="Tipo", text_color="black", font=("Comic Sans MS", 15)).grid(row=6, column=0, padx=10, pady=5)
    servicio_var = tk.StringVar()
    servicio_menu = ttk.Combobox(frame, textvariable=servicio_var, font=("Comic Sans MS", 12), state="readonly", background="white")
    servicio_menu['values'] = ['Aluminio', 'Diamante', 'Premium']
    servicio_menu.grid(row=6, column=1, padx=10, pady=5)
    servicio_menu.bind("<<ComboboxSelected>>", lambda event: mostrar_info_plan(servicio_var, etiqueta_info_plan))

    ctk.CTkButton(root, text="Buscar Vuelos", font=("Comic Sans MS", 14), fg_color="#C00A41", bg_color="white", text_color="white", 
                  command=lambda: buscar_vuelos(origen_var, destino_var, fecha_var, 
                                                cantidad_personas, servicio_var, 
                                                hora_salida_var, hora_llegada_var, 
                                                resultados, etiqueta_info_plan)).pack(pady=10)
    
    frame_etiqueta = ctk.CTkFrame(frame, bg_color="white", fg_color="white", height=400, width=900, border_width=4, border_color="#C00A41")
    frame_etiqueta.grid(row=6, column=2, columnspan=3, padx=10, pady=10)

    # Etiqueta para mostrar la información del plan seleccionado
    etiqueta_info_plan = tk.Label(frame_etiqueta, text='', bg='white', font=("Comic Sans MS", 10))
    etiqueta_info_plan.grid(row=5, column=2, padx=10, pady=5, sticky='w')

    resultados = tk.Listbox(root, width=80, height=10, font=("Comic Sans MS", 10))
    resultados.pack()

    frame_botones = ctk.CTkFrame(root, bg_color="transparent")
    frame_botones.pack()

    ctk.CTkButton(frame_botones, text="Seleccionar Vuelo", command=lambda: seleccionar_vuelo(root, resultados), 
                  font=("Comic Sans MS", 14),fg_color="#C00A41", bg_color="white").grid(row=0, column=2, sticky="e")
    
    espacio = ctk.CTkLabel(frame_botones, text="        ", fg_color="white", bg_color="white")
    espacio.grid(row=0, column=1)
    
    ctk.CTkButton(frame_botones, text="Atrás",font=("Comic Sans MS", 14),fg_color="#C00A41", 
                  bg_color="white",command=lambda: [crear_interfaz_inicial(root), root.state("normal")]).grid(row=0, column=0, sticky="w")


    datos_usuario['servicio_var'] = servicio_var  # Guardar la selección del servicio

# Función para mostrar información basada en la selección del plan
def mostrar_info_plan(servicio_var, etiqueta_info_plan):
    plan = servicio_var.get()
    info = {
        'Aluminio': """➢Aluminio: 
        1 artículo personal (bolso) (Debe caber debajo del asiento)
        1 equipaje de mano (10 kg) (Desde $195.100 COP)
        Equipaje de bodega (23 kg) (Desde $175.600 COP)
        Asiento Economy (Aleatoria-clasificado Aluminio)
        Cambios de vuelo (No es permitido)
        Reembolso (No es permitido)""",

        'Diamante': """➢Diamante:
        1 artículo personal (bolso) (Debe caber debajo del asiento)
        1 equipaje de bodega (23 kg) (Debe caber en el compartimiento superior)
        1 equipaje de mano (10 kg) (Entrega el equipaje en el counter)
        Asiento Economy (Filas específicas disponibles de manera aleatoria)
        Cambios de vuelo (No es permitido)
        Reembolso (No es permitido).""",

        'Premium': """➢ Premium:
        1 artículo personal (bolso) (Debe caber debajo del asiento)
        1 equipaje de mano (10 kg) (Debe caber en el compartimiento superior)
        1 equipaje de bodega (23 kg) (Entrega el equipaje en el counter)
        Asiento Plus (Sujeto a disponibilidad-clasificado Premium)
        Cambios de vuelo (Sin cargo por cambio, antes del vuelo)
        Reembolso (No es permitido)"""
    }
    etiqueta_info_plan.config(text=info.get(plan, ''))


# Actualizar destinos
def actualizar_destinos(origen_var, destino_menu):
    origen = origen_var.get()
    if origen in destinos:
        destinos_actualizados = sorted(destinos[origen])
        destino_menu['values'] = destinos_actualizados
    else:
        destino_menu.set('')
        destino_menu['values'] = []

# Actualizar fechas
def actualizar_fechas(origen_var, destino_var, fecha_menu):
    origen = origen_var.get()
    destino = destino_var.get()
    if origen in fechas and destino in fechas[origen]:
        fechas_actualizadas = sorted(fechas[origen][destino])
        fecha_menu['values'] = fechas_actualizadas
    else:
        fecha_menu.set('')
        fecha_menu['values'] = []

# Actualizar horas de salida
def actualizar_horas_salida(origen_var, destino_var, fecha_var, hora_salida_menu):
    origen = origen_var.get()
    destino = destino_var.get()
    fecha = fecha_var.get()
    if origen in horas_salida and destino in horas_salida[origen] and fecha in horas_salida[origen][destino]:
        horas_salida_actualizadas = sorted(horas_salida[origen][destino][fecha].keys())
        hora_salida_menu['values'] = horas_salida_actualizadas
    else:
        hora_salida_menu.set('')
        hora_salida_menu['values'] = []

# Actualizar hora de llegada
def actualizar_hora_llegada(origen_var, destino_var, fecha_var, hora_salida_var, hora_llegada_var):
    origen = origen_var.get()
    destino = destino_var.get()
    fecha = fecha_var.get()
    hora_salida = hora_salida_var.get()
    if origen in horas_salida and destino in horas_salida[origen] and fecha in horas_salida[origen][destino] and hora_salida in horas_salida[origen][destino][fecha]:
        hora_llegada = horas_salida[origen][destino][fecha][hora_salida]
        hora_llegada_var.set(hora_llegada)
    else:
        hora_llegada_var.set('')

# Buscar vuelos
def buscar_vuelos(origen_var, destino_var, fecha_var, cantidad_personas_entry, servicio_var, hora_salida_var, hora_llegada_var, resultados, etiqueta_info_plan):
    origen = origen_var.get()
    destino = destino_var.get()
    fecha = fecha_var.get()
    global cantidad_personas
    cantidad_personas = int(cantidad_personas_entry.get())
    servicio = servicio_var.get()
    hora_salida = hora_salida_var.get()
    hora_llegada = hora_llegada_var.get()
    
    resultados.delete(0, tk.END)
    for vuelo in vuelos:
        if vuelo['origen'] == origen and vuelo['destino'] == destino and vuelo['fecha'] == fecha and vuelo['hora_salida'] == hora_salida and vuelo['hora_llegada'] == hora_llegada:
            valor = vuelo['valor_min'] if servicio == 'Aluminio' else vuelo['valor_medio'] if servicio == 'Diamante' else vuelo['valor_max']
            resultados.insert(tk.END, f"{vuelo['codigo']} - {vuelo['hora_salida']} - {vuelo['hora_llegada']} - {valor * cantidad_personas} COP")
    
# Seleccionar vuelo 
def seleccionar_vuelo(root, resultados):
    seleccion = resultados.get(resultados.curselection())
    codigo_vuelo = seleccion.split(" - ")[0]
    vuelo_seleccionado = next(vuelo for vuelo in vuelos if vuelo['codigo'] == codigo_vuelo)
    interfaz_pago(root, vuelo_seleccionado)

# Validar que la fecha de expiración esté en el formato MM/AA
def validar_fecha_expiracion(fecha_expiracion):
    if len(fecha_expiracion) != 5 or fecha_expiracion[2] != '/':
        messagebox.showerror("Error", "Formato de fecha de expiración incorrecto (MM/AA)")
        return False

    try:
        # Extraer mes y año
        mes = int(fecha_expiracion[:2])
        año = int(fecha_expiracion[3:])

        # Validar mes válido (entre 01 y 12)
        if mes < 1 or mes > 12:
            messagebox.showerror("Error", "Mes de expiración inválido")
            return False

        # Obtener el año actual
        año_actual = datetime.now().year % 100  # Obtener los dos últimos dígitos del año actual

        # Validar que el año sea mayor o igual al año actual
        if año < año_actual:
            messagebox.showerror("Error", "Año de expiración inválido")
            return False

    except ValueError:
        messagebox.showerror("Error", "Ingrese números válidos para mes y año")
        return False

    return True

# Interfaz de pago
def interfaz_pago(root, vuelo):
    limpiar_ventana(root)
    root.title("Pago")
    root.state("normal")

    ctk.CTkLabel(root, text="Pago", text_color="black", font=("Comic Sans MS", 20)).pack(pady=10)

    frame = ctk.CTkFrame(root, bg_color="white", fg_color="white", height=400, width=900, border_width=4, border_color="#C00A41")
    frame.pack(pady=20)

    ctk.CTkLabel(frame, text="").grid(row=0, column=0, columnspan=2, padx=10, pady=5)

    ctk.CTkLabel(frame, text="Titular de la Tarjeta", fg_color="white", bg_color="white", text_color="black", font=("Comic Sans MS", 15)).grid(row=1, column=0, padx=10, pady=5)
    titular_entry = ctk.CTkEntry(frame,text_color="black", border_color="#C00A41", border_width=2, fg_color="white", bg_color="white", font=("Comic Sans MS", 15))
    titular_entry.grid(row=1, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame, text="Numero de la Tarjeta", fg_color="white", bg_color="white", text_color="black", font=("Comic Sans MS", 15)).grid(row=2, column=0, padx=10, pady=5)
    numero_tarjeta_entry = ctk.CTkEntry(frame,text_color="black", border_color="#C00A41", border_width=2, fg_color="white", bg_color="white", font=("Comic Sans MS", 15))
    numero_tarjeta_entry.grid(row=2, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame, text="Fecha de Expiración(MM/AA)", fg_color="white", bg_color="white", text_color="black", font=("Comic Sans MS", 15)).grid(row=3, column=0, padx=10, pady=5)
    expiracion_entry = ctk.CTkEntry(frame,text_color="black", border_color="#C00A41", border_width=2, fg_color="white", bg_color="white", font=("Comic Sans MS", 15))
    expiracion_entry.grid(row=3, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame, text="CVV", fg_color="white", bg_color="white", text_color="black", font=("Comic Sans MS", 15)).grid(row=4, column=0, padx=10, pady=5)
    cvv_entry = ctk.CTkEntry(frame,text_color="black", border_color="#C00A41", border_width=2, fg_color="white", bg_color="white", font=("Comic Sans MS", 15))
    cvv_entry.grid(row=4, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame, text="").grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    frame_boton = ctk.CTkFrame(root, bg_color="white", fg_color="white")
    frame_boton.pack()

    ctk.CTkButton(frame_boton, bg_color="white",fg_color="#C00A41",text_color="white",font=("Comic Sans MS", 15), text="Pagar", command=lambda: procesar_pago(titular_entry.get(), numero_tarjeta_entry.get(), expiracion_entry.get(), cvv_entry.get(), vuelo, datos_usuario['servicio_var'].get())).grid(row=0, column=2, columnspan=2, pady=10)

    ctk.CTkLabel(frame_boton, text="         ").grid(row=0, column=1, columnspan=2, pady=10)

    ctk.CTkButton(frame_boton, bg_color="white",fg_color="#C00A41",text_color="white",font=("Comic Sans MS", 15),text="Atrás", command=lambda: mostrar_interfaz_agendar_vuelo(root)).grid(row=0, column=0, columnspan=2, pady=10)

# Procesar pago
def procesar_pago(titular, numero_tarjeta, expiracion, cvv, vuelo, servicio):
    if not titular or not numero_tarjeta or not expiracion or not cvv:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    if not validar_tarjeta(numero_tarjeta):
        messagebox.showerror("Error", "Número de tarjeta inválido.")
        return

    if not validar_cvv(cvv):
        messagebox.showerror("Error", "CVV inválido.")
        return
    
    if not validar_fecha_expiracion(expiracion):
        return

    codigo_pago = generar_codigo_pasajero(titular)
    messagebox.showinfo("Éxito", f"Pago procesado exitosamente. Código de pasajero: {codigo_pago}")

    datos_usuario['vuelo'] = vuelo
    datos_usuario['servicio'] = servicio
    datos_usuario['codigo_pasajero'] = codigo_pago

    asignar_sillas(vuelo, codigo_pago, servicio)


# Asignar sillas
def asignar_sillas(vuelo, codigo_pasajero, servicio):
    limpiar_ventana(root)
    root.title("Asignación de Asientos")
    root.state("zoomed")
    frame = ctk.CTkFrame(root, bg_color="white", fg_color="white",border_width=4, border_color="#C00A41")
    frame.pack(pady=20)
    tk.Label(frame, text="Seleccione sus asientos:").grid(row=0, column=0, columnspan=6, padx=10, pady=5)

    sectores = 'ABCDEF'
    filas = 12
    checkboxes = {}

    for i in range(1, filas + 1):
        for j in range(len(sectores)):
            asiento = f"{sectores[j]}{i}"
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame, text=asiento, variable=var, font=("Comic Sans MS", 10), bg="white", height=1, width=3)
            chk.grid(row=i, column=j, padx=5, pady=5)
            
            # Bloquear los asientos según el servicio seleccionado
            if (servicio == "Premium" and i > 4) or (servicio == "Diamante" and (i < 5 or i > 8)) or (servicio == "Aluminio" and i < 9):
                chk.configure(state="disabled")
            
            checkboxes[asiento] = var

    def confirmar_seleccion():
        seleccionados = [asiento for asiento, var in checkboxes.items() if var.get()]
        cantidad_personas = 1

        if servicio == "Aluminio":
            if len(seleccionados) > 0:
                messagebox.showerror("Error", "El servicio Aluminio no permite seleccionar asientos, deseleccione la casilla.")
                return
            silla_asignada = random.choice([asiento for asiento in checkboxes.keys() if int(asiento[1:]) >= 9])
            datos_usuario['sillas'] = [silla_asignada]
            messagebox.showinfo("Silla Asignada", f"Silla asignada: {silla_asignada}")
        elif servicio == "Diamante":
            if len(seleccionados) != 1:
                messagebox.showerror("Error", "Debe seleccionar exactamente una fila para el servicio Diamante.")
                return 
            fila_elegida = seleccionados[0][1:]
            sillas_fila = [asiento for asiento in checkboxes.keys() if asiento[1:] == fila_elegida]
            silla_asignada = random.choice(sillas_fila)
            datos_usuario['sillas'] = [silla_asignada]
            messagebox.showinfo("Silla Asignada", f"Silla asignada: {silla_asignada}")
        elif servicio == "Premium":
            if len(seleccionados) != cantidad_personas:
                messagebox.showerror("Error", f"Debe seleccionar exactamente {cantidad_personas} asientos.")
                return
            datos_usuario['sillas'] = seleccionados
            messagebox.showinfo("Sillas Asignadas", f"Sillas asignadas: {seleccionados}")

        crear_interfaz_inicial(root)

    frame_botones = ctk.CTkFrame(root, bg_color="white", fg_color="white")
    frame_botones.pack()

    ctk.CTkButton(frame_botones, bg_color="white", fg_color="#C00A41",text_color="white" ,text="Confirmar", command=confirmar_seleccion).grid(row=0, column=2, padx=10, pady=10)

    ctk.CTkLabel(frame_botones, text="         ").grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkButton(frame_botones,bg_color="white", fg_color="#C00A41",text_color="white" ,text="Atrás", command=lambda: interfaz_pago(root, datos_usuario['vuelo'])).grid(row=0, column=0, padx=10, pady=10)

# Interfaz de check-in
def check_in(root):
    if not usuario_registrado:
        messagebox.showwarning("Advertencia", "Debe registrarse antes de realizar el check-in.")
        return

    limpiar_ventana(root)
    root.title("Check-in")
    root.geometry("500x400")
    root.state("normal")
    ventana_width = 500
    ventana_height = 400

    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()
        
    center_x = int(pantalla_width/2 - ventana_width/2)
    center_y = int(pantalla_height/2 - ventana_height/2)

    root.geometry(f"{ventana_width}x{ventana_height}+{center_x}+{center_y}")

    ctk.CTkLabel(root, text="Check-in", text_color="black", font=("Comic Sans MS", 20)).pack(pady=10)

    frame = ctk.CTkFrame(root, bg_color="white", fg_color="white",border_width=4, border_color="#C00A41")
    frame.pack(pady=20)

    ctk.CTkLabel(frame, text="").grid(row=0, column=0, padx=10, pady=5)

    ctk.CTkLabel(frame, text_color="black",text="Código del Pasajero", font=("Comic Sans MS", 15),
                 fg_color="white",bg_color="white" ).grid(row=1, column=0, padx=10, pady=5)
    codigo_entry = ctk.CTkEntry(frame,text_color="black", border_color="#C00A41", border_width=2, fg_color="white", bg_color="white", font=("Comic Sans MS", 15))
    codigo_entry.grid(row=1, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame,text_color="black" ,text="Primer Apellido", font=("Comic Sans MS", 15),
                 fg_color="white",bg_color="white" ).grid(row=2, column=0, padx=10, pady=5)
    apellido_entry = ctk.CTkEntry(frame,text_color="black" ,border_color="#C00A41", border_width=2, fg_color="white", bg_color="white", font=("Comic Sans MS", 15))
    apellido_entry.grid(row=2, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame, text="").grid(row=3, column=0, padx=10, pady=5)

    frame_botones = ctk.CTkFrame(root, bg_color="white", fg_color="white")
    frame_botones.pack()


    ctk.CTkButton(frame_botones, text="Continuar", text_color="white",fg_color="#C00A41", bg_color="white", border_width=2, border_color="#C00A41" ,font=("Comic Sans MS", 15),
                command=lambda: realizar_check_in(codigo_entry.get(), apellido_entry.get())).grid(row=0, column=2, columnspan=2, pady=10, sticky="e")
    
    ctk.CTkLabel(frame_botones, text=" ").grid(row=0, column=1, columnspan=2, pady=10)

    ctk.CTkButton(frame_botones, text="Atrás", text_color="white",fg_color="#C00A41", bg_color="white", border_width=2, border_color="#C00A41" ,font=("Comic Sans MS", 15), 
                  command=lambda: crear_interfaz_inicial(root)).grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

# Realizar check-in
def realizar_check_in(codigo, apellido):
    if not codigo or not apellido :
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    if codigo == datos_usuario.get('codigo_pasajero') and apellido.lower() == datos_usuario.get('apellido').lower():
        messagebox.showinfo("Check-in", "Check-in realizado exitosamente.")
        generar_ticket()
    else:
        messagebox.showerror("Error", "Código de pasajero o apellido incorrecto.")

# Registrar usuario
def registrar_usuario(root):
    limpiar_ventana(root)
    root.title("Registro de Usuario")

    titulo = ctk.CTkLabel(root, text="Registro de Usuario", text_color="black",font=("Comic Sans MS", 20))
    titulo.grid(row=0, padx=10, pady=10, sticky="w")

    frame = ctk.CTkFrame(root, bg_color="white", fg_color="white", height=400, width=900, border_width=4, border_color="#C00A41")
    frame.grid(row=1, padx=10, pady=10)

    ctk.CTkLabel(frame,fg_color="white",text_color="black" ,font=("Comic Sans MS", 15) ,text="Primer Nombre").grid(row=0, column=0, padx=10, pady=5)
    nombre_entry = ctk.CTkEntry(frame,text_color="black" ,font=("Comic Sans MS", 15), fg_color="white", bg_color="white", border_width=2, border_color="#C00A41")
    nombre_entry.grid(row=1, column=0, padx=10, pady=5)

    ctk.CTkLabel(frame,fg_color="white",text_color="black" ,font=("Comic Sans MS", 15) , text="Primer Apellido").grid(row=0, column=1, padx=10, pady=5)
    apellido_entry = ctk.CTkEntry(frame,text_color="black" , font=("Comic Sans MS", 15), fg_color="white", bg_color="white", border_width=2, border_color="#C00A41")
    apellido_entry.grid(row=1, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame,fg_color="white",text_color="black" ,font=("Comic Sans MS", 15) , text="Género").grid(row=0, column=2, padx=10, pady=5)
    genero_var = tk.StringVar()
    genero_menu = ctk.CTkComboBox(frame, values=['Masculino', 'Femenino', 'Otro'], font=("Comic Sans MS", 15), 
                                  fg_color="white", bg_color="white", border_width=2, border_color="#C00A41",
                                  text_color="black", variable=genero_var, state='readonly', dropdown_fg_color="white",
                                  dropdown_text_color="black", button_hover_color="white", dropdown_hover_color="#C00A41",
                                  button_color="#C00A41")
    genero_menu.grid(row=1, column=2, padx=10, pady=5)


    ctk.CTkLabel(frame,fg_color="white",text_color="black" ,font=("Comic Sans MS", 15) , text="Nacionalidad").grid(row=2, column=0, padx=10, pady=5)
    nacionalidad_entry = ctk.CTkEntry(frame,text_color="black" , font=("Comic Sans MS", 15), fg_color="white", bg_color="white", border_width=2, border_color="#C00A41")
    nacionalidad_entry.grid(row=3, column=0, padx=10, pady=5)

    ctk.CTkLabel(frame,fg_color="white",text_color="black" ,font=("Comic Sans MS", 15) , text="Número de Documento").grid(row=2, column=1, padx=10, pady=5)
    documento_entry = ctk.CTkEntry(frame,text_color="black" , font=("Comic Sans MS", 15), fg_color="white", bg_color="white", border_width=2, border_color="#C00A41")
    documento_entry.grid(row=3, column=1, padx=10, pady=5)

    salto = ctk.CTkLabel(frame,fg_color="white",text_color="black" ,font=("Comic Sans MS", 15) , text="").grid(row=4, column=0, padx=10, pady=5)

    ctk.CTkLabel(frame,fg_color="white",text_color="black" ,font=("Comic Sans MS", 15) , text="                        Fecha de Nacimiento (DD/MM/AAAA)").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    fecha_nacimiento_entry = DateEntry(frame, date_pattern='dd/MM/yyyy', font=("Comic Sans MS", 12))
    fecha_nacimiento_entry.grid(row=5, column=1, padx=10, pady=5, sticky="e")

    ctk.CTkLabel(frame,fg_color="white",text_color="black" ,font=("Comic Sans MS", 15) , text="¿Necesita asistencia durante el vuelo?").grid(row=6, column=0, padx=10, pady=5, sticky="e")
    asistencia_var = tk.StringVar(value="No")
    asistencia_check = ctk.CTkCheckBox(frame, variable=asistencia_var,text="", onvalue="Sí", offvalue="No", 
                                       fg_color="white", bg_color="white", font=("Comic Sans MS", 15), border_width=2, 
                                       border_color="#C00A41", hover_color="#C00A41", text_color="black")
    asistencia_check.grid(row=6, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame,fg_color="white",text_color="black" ,font=("Comic Sans MS", 15) , text="Correo Electrónico").grid(row=7, column=0, padx=10, pady=5)
    correo_entry = ctk.CTkEntry(frame,text_color="black" , font=("Comic Sans MS", 15), fg_color="white", bg_color="white", border_width=2, border_color="#C00A41")
    correo_entry.grid(row=8, column=0, padx=10, pady=5)

    ctk.CTkLabel(frame,fg_color="white",text_color="black" ,font=("Comic Sans MS", 15) , text="Número Celular").grid(row=7, column=1, padx=10, pady=5, sticky="w")
    celular_entry = ctk.CTkEntry(frame,text_color="black" , font=("Comic Sans MS", 15), fg_color="white", bg_color="white", border_width=2, border_color="#C00A41")
    celular_entry.grid(row=8, column=1, padx=10, pady=5, sticky="w")

    salto = ctk.CTkLabel(frame,fg_color="white",text_color="black" ,font=("Comic Sans MS", 15) , text="                        ").grid(row=9, column=3, padx=10, pady=5)

    ctk.CTkButton(frame, text="Registrar", text_color="white",fg_color="#C00A41", bg_color="white", border_width=2, border_color="#C00A41" ,font=("Comic Sans MS", 15) ,command=lambda: procesar_registro(nombre_entry.get(), 
                                                                         apellido_entry.get(), genero_var.get(), nacionalidad_entry.get(), documento_entry.get(), fecha_nacimiento_entry.get(), asistencia_var.get(), 
                                                                         correo_entry.get(), celular_entry.get())).grid(row=9, column=1, columnspan=2, pady=10)

    ctk.CTkButton(frame, text="Atrás",text_color="white",fg_color="#C00A41", bg_color="white", border_width=2, border_color="#C00A41" ,font=("Comic Sans MS", 15) , command=lambda: crear_interfaz_inicial(root)).grid(row=9, column=0, columnspan=2, pady=10)

def validar_fecha_nacimiento(fecha_nacimiento_str):
    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%d/%m/%Y").date()
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha de nacimiento incorrecto (DD/MM/YYYY)")
        return False

    # Verificar que la persona sea mayor de edad (nacida antes de 2006)
    if fecha_nacimiento.year > 2006:
        messagebox.showerror("Error", "Debes ser mayor de edad para registrarte")
        return False

    return True

# Procesar registro
def procesar_registro(nombre, apellido, genero, nacionalidad, documento, fecha_nacimiento, asistencia, correo, celular):
    if not nombre or not apellido or not genero or not nacionalidad or not documento or not fecha_nacimiento or not correo or not celular:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    if not validar_correo(correo):
        messagebox.showerror("Error", "Correo electrónico inválido.")
        return

    if not validar_numero_celular(celular):
        messagebox.showerror("Error", "Número celular inválido.")
        return
    
    if not validar_correo(correo):
            messagebox.showerror("Error", "Correo electrónico inválido")
            return False

    if not documento.isdigit():
        messagebox.showerror("Error", "El número de documento debe contener solo números")
        return False

    # Validar que la fecha de nacimiento sea mayor de edad 
    if not validar_fecha_nacimiento(fecha_nacimiento):
        return False
    

    global usuario_registrado, datos_usuario
    usuario_registrado = True
    datos_usuario = {
        'nombre': nombre,
        'apellido': apellido,
        'genero': genero,
        'nacionalidad': nacionalidad,
        'documento': documento,
        'fecha_nacimiento': fecha_nacimiento,
        'asistencia': asistencia,
        'correo': correo,
        'celular': celular,
    }

    messagebox.showinfo("Inicio de Sesión Exitoso", "Inicio de sesión realizado con éxito.")
    crear_interfaz_inicial(root)
    usuario_registrado = True

def generar_ticket():
    global datos_usuario

    # Crear la ventana del ticket
    ticket_window = tk.Toplevel(root)
    ticket_window.title("Ticket de Vuelo")
    ticket_window.iconbitmap("logo.ico")
    ventana_descarga_width = 330
    ventana_descarga_height = 225

    pantalla_width = ticket_window.winfo_screenwidth()
    pantalla_height = ticket_window.winfo_screenheight()
        
    center_x = int(pantalla_width/2 - ventana_descarga_width/2)
    center_y = int(pantalla_height/2 - ventana_descarga_height/2)
    ticket_window.geometry(f'{ventana_descarga_width}x{ventana_descarga_height}+{center_x}+{center_y}')


    
    frame = tk.Frame(ticket_window)
    frame.pack(pady=20)
    # Guardar ticket
    ctk.CTkButton(ticket_window,text_color="white",fg_color="#C0041A", bg_color="white",font=("Comic Sans MS", 15) ,text="Descargar Ticket", command=lambda: [guardar_ticket(datos_usuario), crear_interfaz_inicial(root)]).pack(pady=10)


def guardar_ticket(datos_usuario):
    # Cargar la imagen de fondo
    img = Image.open("tiquete.png")
    draw = ImageDraw.Draw(img)

    # Colores y fuentes
    color_texto = (0, 0, 0)  # Negro
    font_path = "Comic Sans MS.ttf"  # Ruta de la fuente Comic Sans MS

    try:
        font_codigo = ImageFont.truetype(font_path, 100)  # Tamaño de fuente para el código
        font_origen_destino = ImageFont.truetype(font_path, 100)  # Tamaño de fuente para el origen y destino
        font_sillas = ImageFont.truetype(font_path, 100)  # Tamaño de fuente para las sillas
        font_nombre = ImageFont.truetype(font_path, 100)  # Tamaño de fuente para el nombre y apellido
        font_fecha_hora = ImageFont.truetype(font_path, 100)  # Tamaño de fuente para la fecha y hora
    except IOError:
        font_codigo = font_origen_destino = font_sillas = font_nombre = font_fecha_hora = ImageFont.load_default()

    # Dibujar el texto en la imagen
    draw.text((210, 90), datos_usuario['vuelo']['codigo'], font=font_codigo, fill=color_texto)
    draw.text((550, 65), f"{datos_usuario['vuelo']['origen']} -> {datos_usuario['vuelo']['destino']}", font=font_origen_destino, fill=color_texto)
    draw.text((460, 213), ', '.join(datos_usuario['sillas']), font=font_sillas, fill=color_texto)
    draw.text((515, 243), f"{datos_usuario['nombre']} {datos_usuario['apellido']}", font=font_nombre, fill=color_texto)
    draw.text((785, 243), f"{datos_usuario['vuelo']['fecha']} {datos_usuario['vuelo']['hora_salida']}", font=font_fecha_hora, fill=color_texto)
    img.show()

    # Guardar la imagen
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        img.save(file_path)
        messagebox.showinfo("Ticket Guardado", f"El ticket ha sido guardado en: {file_path}")



if __name__ == "__main__":
    # Datos de ejemplo para destinos y vuelos
    vuelos = cargar_vuelos()
    origenes = sorted(list(set(vuelo['origen'] for vuelo in vuelos)))
    destinos = {origen: set(vuelo['destino'] for vuelo in vuelos if vuelo['origen'] == origen) for origen in origenes}
    fechas = {origen: {destino: set(vuelo['fecha'] for vuelo in vuelos if vuelo['origen'] == origen and vuelo['destino'] == destino) for destino in destinos[origen]} for origen in origenes}
    horas_salida = {origen: {destino: {fecha: {vuelo['hora_salida']: vuelo['hora_llegada'] for vuelo in vuelos if vuelo['origen'] == origen and vuelo['destino'] == destino and vuelo['fecha'] == fecha} for fecha in fechas[origen][destino]} for destino in destinos[origen]} for origen in origenes}


    # Crear ventana principal
    root = tk.Tk()
    ventana_width = 860
    ventana_height = 500

    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()
        
    center_x = int(pantalla_width/2 - ventana_width/2)
    center_y = int(pantalla_height/2 - ventana_height/2)


    root.title("LA AIRLINES")
    root.config(background="white")
    root.geometry(f'{ventana_width}x{ventana_height}+{center_x}+{center_y}')
    root.state("normal")
    root.iconbitmap("logo.ico")
    crear_interfaz_inicial(root)
    root.mainloop()
