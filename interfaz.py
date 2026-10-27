import tkinter as tk
from tkinter import ttk

import datos
from planificador import distancia_km, planificar

AZUL, GRIS, NEGRO = "#1d4f91", "#8a94a6", "#121c2b"

LON_MIN, LON_MAX, LAT_MIN, LAT_MAX = -108, -54, -38, 30
ANCHO_MAPA, ALTO_MAPA = 380, 440
LADO_NOMBRE = {"BOG": "derecha", "PTY": "izquierda", "MIA": "derecha", "MEX": "abajo", "LIM": "izquierda", "SCL": "izquierda"}

def miles(numero):
    return f"{numero:,}".replace(",", ".")

def ciudad(codigo):
    return datos.AEROPUERTOS[codigo]["ciudad"]

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("InterFly")
        self.geometry("1120x630")
        self.resizable(False, False) 
        self.plan = planificar(datos.AEROPUERTOS, datos.VUELOS, datos.AVION, datos.CAJAS, datos.BASE, datos.PESO_MAX_CAJA)

        self.crear_titulo()
        izquierda = tk.Frame(self)
        izquierda.pack(side="left", fill="y", padx=10, pady=(0, 10))
        derecha = tk.Frame(self)
        derecha.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=(0, 10))
        self.crear_mapa(izquierda)
        self.crear_tabla(derecha)
        self.crear_resultado(derecha)

    def crear_titulo(self):
        tk.Label(self, text="InterFly - Carga aerea entre paises", font=("Segoe UI", 16, "bold"), fg=AZUL).pack(anchor="w", padx=10, pady=(8, 0))
        avion = datos.AVION
        texto = (f'Avion {avion["nombre"]}   |   Capacidad {miles(avion["peso_max"])} kg y {avion["volumen_max"]} m3   |   '
                 f'Sale de Bogota y vuelve a Bogota   |   Cada caja maximo {miles(datos.PESO_MAX_CAJA)} kg')
        tk.Label(self, text=texto, font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=(0, 8))

    def crear_mapa(self, padre):
        marco = tk.LabelFrame(padre, text=" Mapa de los trayectos ", font=("Segoe UI", 10, "bold"), padx=6, pady=6)
        marco.pack(fill="y")
        self.mapa = tk.Canvas(marco, width=ANCHO_MAPA, height=ALTO_MAPA, bg="white", highlightthickness=1, highlightbackground="#d5dbe5")
        self.mapa.pack()
        self.dibujar_mapa()

    def punto(self, codigo):
        aeropuerto = datos.AEROPUERTOS[codigo]
        x = (aeropuerto["lon"] - LON_MIN) / (LON_MAX - LON_MIN) * ANCHO_MAPA
        y = (LAT_MAX - aeropuerto["lat"]) / (LAT_MAX - LAT_MIN) * ALTO_MAPA
        return x, y

    def dibujar_mapa(self):
        mapa = self.mapa

        for lat in [-30, -20, -10, 0, 10, 20]:
            y = (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * ALTO_MAPA
            mapa.create_line(0, y, ANCHO_MAPA, y, fill="#eceff4")
            if lat == 0:
                texto = "Ecuador"
            elif lat > 0:
                texto = str(lat) + " N"
            else:
                texto = str(-lat) + " S"
            mapa.create_text(4, y - 7, text=texto, anchor="w", fill=GRIS, font=("Segoe UI", 7))

        for a, b in datos.VUELOS:
            x1, y1 = self.punto(a)
            x2, y2 = self.punto(b)
            mapa.create_line(x1, y1, x2, y2, fill="#b4bfcf", dash=(3, 3))

        for tramo in self.plan["tramos"]:
            puntos = []
            for codigo in tramo["pasa_por"]:
                x, y = self.punto(codigo)
                puntos.append(x)
                puntos.append(y)
            mapa.create_line(puntos, fill=AZUL, width=3, arrow="last", arrowshape=(10, 12, 4))

        for a, b in datos.VUELOS:
            x1, y1 = self.punto(a)
            x2, y2 = self.punto(b)
            km = distancia_km(datos.AEROPUERTOS[a], datos.AEROPUERTOS[b])
            texto = mapa.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=miles(km), fill="#4f5f7a", font=("Consolas", 8))
            fondo = mapa.create_rectangle(mapa.bbox(texto), fill="white", outline="")
            mapa.tag_lower(fondo, texto)

        for codigo in datos.AEROPUERTOS:
            x, y = self.punto(codigo)
            if codigo == datos.BASE:
                mapa.create_oval(x - 8, y - 8, x + 8, y + 8, fill=NEGRO, outline=NEGRO)
            elif codigo in self.plan["orden"]:
                mapa.create_oval(x - 8, y - 8, x + 8, y + 8, fill=AZUL, outline=AZUL)
                numero = self.plan["orden"].index(codigo) + 1
                mapa.create_text(x, y, text=str(numero), fill="white", font=("Segoe UI", 8, "bold"))
            else:
                mapa.create_oval(x - 7, y - 7, x + 7, y + 7, fill="white", outline=AZUL, width=2)
            lado = LADO_NOMBRE[codigo]
            if lado == "derecha":
                mapa.create_text(x + 12, y, text=ciudad(codigo), anchor="w", font=("Segoe UI", 9, "bold"))
            elif lado == "izquierda":
                mapa.create_text(x - 12, y, text=ciudad(codigo), anchor="e", font=("Segoe UI", 9, "bold"))
            else:
                mapa.create_text(x, y + 12, text=ciudad(codigo), anchor="n", font=("Segoe UI", 9, "bold"))

    def crear_tabla(self, padre):
        marco = tk.LabelFrame(padre, text=" Cajas ", font=("Segoe UI", 10, "bold"), padx=6, pady=6)
        marco.pack(fill="x")
        columnas = ("Caja", "Destino", "Lat", "Lon", "Medidas (cm)", "Peso", "Precio", "Sube")
        anchos = (125, 115, 50, 55, 105, 65, 95, 45)
        tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=8, selectmode="none", takefocus=False)
        for i in range(len(columnas)):
            tabla.heading(columnas[i], text=columnas[i])
            tabla.column(columnas[i], width=anchos[i], anchor="w")
        tabla.tag_configure("no", foreground="#b05f00")
        for caja in datos.CAJAS:
            aeropuerto = datos.AEROPUERTOS[caja["destino"]]
            medidas = f'{caja["alto"]} x {caja["ancho"]} x {caja["profundidad"]}'
            if caja in self.plan["a_bordo"]:
                sube, color = "Si", ()
            else:
                sube, color = "No", ("no",)
            tabla.insert("", "end", tags=color, values=(caja["nombre"], aeropuerto["ciudad"], aeropuerto["lat"], aeropuerto["lon"],
                                                        medidas, f'{caja["peso"]} kg', "$ " + miles(caja["precio"]), sube))
        tabla.pack(fill="x")


    def crear_resultado(self, padre):
        marco = tk.LabelFrame(padre, text=" Resultado ", font=("Segoe UI", 10, "bold"), padx=6, pady=6)
        marco.pack(fill="both", expand=True, pady=(8, 0))
        texto = tk.Text(marco, font=("Segoe UI", 10), wrap="word", relief="flat", bg="#f7f8fa", cursor="arrow", takefocus=False)
        texto.pack(fill="both", expand=True)
        texto.tag_configure("titulo", font=("Segoe UI", 10, "bold"), foreground=AZUL)
        plan, avion = self.plan, datos.AVION

        texto.insert("end", "Paso 1 - Mochila 0/1: que cajas suben al avion\n", "titulo")
        no_suben = []
        for caja in datos.CAJAS:
            if caja not in plan["a_bordo"]:
                no_suben.append(caja["nombre"])
        texto.insert("end", f'   Suben {len(plan["a_bordo"])} de {len(datos.CAJAS)} cajas   |   No suben: {" y ".join(no_suben)}\n')
        texto.insert("end", f'   Peso {miles(plan["peso"])} de {miles(avion["peso_max"])} kg   |   '
                            f'Volumen {plan["volumen"]:.2f} de {avion["volumen_max"]} m3   |   Precio total $ {miles(plan["precio"])}\n\n')

        texto.insert("end", "Paso 2 - Vecino mas cercano: orden del viaje\n", "titulo")
        ruta = ["Bogota"]
        for codigo in plan["orden"]:
            ruta.append(ciudad(codigo))
        ruta.append("Bogota")
        texto.insert("end", "   " + "  →  ".join(ruta) + "\n\n")

        texto.insert("end", "Paso 3 - Dijkstra: camino mas corto de cada tramo\n", "titulo")
        for numero in range(len(plan["tramos"])):
            tramo = plan["tramos"][numero]
            linea = f'   {numero + 1}. {ciudad(tramo["desde"])} → {ciudad(tramo["hasta"])}: {miles(tramo["km"])} km'
            escalas = []
            for codigo in tramo["pasa_por"][1:-1]: 
                escalas.append(ciudad(codigo))
            if escalas:
                linea += "  (escala en " + " y ".join(escalas) + ")"
            texto.insert("end", linea + "\n")
        texto.insert("end", f'   Distancia total: {miles(plan["km"])} km', "titulo")
        texto.config(state="disabled") 