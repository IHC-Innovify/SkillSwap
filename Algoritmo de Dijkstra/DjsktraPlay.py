import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
import os, random
import networkx as nx
import heapq
import time

# Crear ventana
ventana = tk.Tk()
ventana.title("Algoritmo de Dijkstra")
ventana.geometry("900x600")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
imagen_path_menu = os.path.join(BASE_DIR, "fondo.png")
imagen_path_instr = os.path.join(BASE_DIR, "fondo1.png")
imagen_path_juego1 = os.path.join(BASE_DIR, "fondo2.png")
imagen_path_juego2 = os.path.join(BASE_DIR, "fondo3.png")
imagen_path_fondo_dijk = os.path.join(BASE_DIR, "fondo4.png")

# --- Imagen de fondo ---
imagen = Image.open(imagen_path_menu)  # usa tu propia imagen
imagen = imagen.resize((900, 600))  # ajusta al tamaño de la ventana
fondo = ImageTk.PhotoImage(imagen)

# --- Frames (pantallas) ---
pantalla_menu = tk.Frame(ventana, width=900, height=600)
pantalla_juego1 = tk.Frame(ventana, width=900, height=600)
pantalla_juego2 = tk.Frame(ventana, width=900, height=600)
pantalla_fondo_dijk = tk.Frame(ventana, width=900, height=600)
pantalla_instrucciones = tk.Frame(ventana, width=900, height=600)
pantalla_menu.pack(fill="both", expand=True)

# --- Fondos de pantalla ---
label_fondo = tk.Label(pantalla_menu, image=fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# --- Grafo ---
G = None
canvas_grafo = None
nodos_canvas = {}

def instruc():
    imagen = Image.open(imagen_path_instr)
    imagen = imagen.resize((900, 600))
    fondo = ImageTk.PhotoImage(imagen)

    pantalla_menu.pack_forget()
    pantalla_instrucciones.pack(fill="both", expand=True)

    label_fondo_instr = tk.Label(pantalla_instrucciones, image=fondo)
    label_fondo_instr.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo_instr.image = fondo

    boton_return = tk.Button(
        pantalla_instrucciones,
        text="Volver",
        command=lambda: [pantalla_instrucciones.pack_forget(), pantalla_menu.pack(fill="both", expand=True)],
        font=("Arial", 25),
        bg="#315373",
        fg="white",
        activebackground="#315373",
        relief="flat",
        padx=40, pady=0
    )
    boton_return.place(x=353, y=480)

def inicio():
    # Al entrar a la pantalla juego: crear canvas con imagen de fondo y widgets
    global canvas_juego1, fondo_juego1_img
    pantalla_menu.pack_forget()
    pantalla_juego1.pack(fill="both", expand=True)

    # crear canvas
    if "canvas_juego1" in globals() and canvas_juego1:
        canvas_juego1.destroy()
    canvas_juego1 = tk.Canvas(pantalla_juego1, width=900, height=600, highlightthickness=0)
    canvas_juego1.pack(fill="both", expand=True)

    # cargar y dibujar fondo del juego (mapa)
    try:
        img_j = Image.open(imagen_path_juego1).resize((900,600))
        fondo_juego1_img = ImageTk.PhotoImage(img_j)
        canvas_juego1.create_image(0, 0, anchor="nw", image=fondo_juego1_img)
        canvas_juego1.image = fondo_juego1_img
    except Exception:
        canvas_juego1.configure(bg="#efe6b7")

    entry_nodos = tk.Entry(pantalla_juego1, font=("Arial", 25))
    canvas_juego1.create_window(450, 320, window=entry_nodos, width=80)

    # botón para validar después de que el usuario escriba
    def validar_nodos():
        try:
            n = int(entry_nodos.get())
            if not 8 <= n <= 16:
                messagebox.showerror("Error", "Ingrese un número entre 8 y 16")
                return
            messagebox.showinfo("Correcto", f"Se usarán {n} nodos.")
            modo_juego(n)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido")

    boton_validar = tk.Button(pantalla_juego1, text="Confirmar", command=validar_nodos,
                              font=("Arial", 25, "bold"), bg="#FFA831", fg="white",
                              activebackground="#FFA931", relief="flat", padx=60, pady=0)
    canvas_juego1.create_window(265, 470, window=boton_validar)

    boton_regresar = tk.Button(pantalla_juego1, text="Regresar", command=lambda: [pantalla_juego1.pack_forget(), pantalla_menu.pack(fill="both", expand=True)],
                              font=("Arial", 25, "bold"), bg="#365785", fg="white",
                              activebackground="#365785", relief="flat", padx=60, pady=0)
    canvas_juego1.create_window(640, 470, window=boton_regresar)

def modo_juego(n):
    # Al entrar a la pantalla juego: crear canvas con imagen de fondo y widgets
    global canvas_juego2, fondo_juego2_img
    pantalla_juego1.pack_forget()
    pantalla_juego2.pack(fill="both", expand=True)

    # crear canvas
    if "canvas_juego2" in globals() and canvas_juego2:
        canvas_juego2.destroy()
    canvas_juego2 = tk.Canvas(pantalla_juego2, width=900, height=600, highlightthickness=0)
    canvas_juego2.pack(fill="both", expand=True)

    # cargar y dibujar fondo del juego (mapa)
    try:
        img_j = Image.open(imagen_path_juego2).resize((900,600))
        fondo_juego2_img = ImageTk.PhotoImage(img_j)
        canvas_juego2.create_image(0, 0, anchor="nw", image=fondo_juego2_img)
        canvas_juego2.image = fondo_juego2_img
    except Exception:
        canvas_juego2.configure(bg="#efe6b7")

    boton_manual = tk.Button(pantalla_juego2, text="Manual", command=lambda:juego_manual(n),
                             font=("Arial", 25, "bold"), bg="#FFF186", fg="white",
                             activebackground="#FFF186", relief="flat", padx=60, pady=0)
    canvas_juego2.create_window(246, 300, window=boton_manual)

    boton_aleatorio = tk.Button(pantalla_juego2, text="Aleatorio", command=lambda:juego_aleatorio(n),
                                font=("Arial", 25, "bold"), bg="#365785", fg="white",
                                activebackground="#365785", relief="flat", padx=60, pady=0)
    canvas_juego2.create_window(655, 300, window=boton_aleatorio)

def fondo_juego():
    # Al entrar a la pantalla juego: crear canvas con imagen de fondo y widgets
    global canvas_fondo_dijk, fondo_dijk_img
    pantalla_juego2.pack_forget()
    pantalla_fondo_dijk.pack(fill="both", expand=True)

    # crear canvas
    if "canvas_fondo_dijk" in globals() and canvas_fondo_dijk:
        canvas_fondo_dijk.destroy()
    canvas_fondo_dijk = tk.Canvas(pantalla_fondo_dijk, width=900, height=600, highlightthickness=0)
    canvas_fondo_dijk.pack(fill="both", expand=True)

    # cargar y dibujar fondo del juego (mapa)
    try:
        img_j = Image.open(imagen_path_fondo_dijk).resize((900,600))
        fondo_dijk_img = ImageTk.PhotoImage(img_j)
        canvas_fondo_dijk.create_image(0, 0, anchor="nw", image=fondo_dijk_img)
        canvas_fondo_dijk.image = fondo_dijk_img
    except Exception:
        canvas_fondo_dijk.configure(bg="#efe6b7")

def juego_manual(n):
    fondo_juego()

    nodos_pos = {}
    nodos_canvas = {}
    G = nx.DiGraph()

    def continuar_manual(nodos_pos, G):
        global boton_continuar
        if boton_continuar:
            boton_continuar.destroy()
        # Aquí seguirá la lógica del juego después de colocar los nodos
        print("Posiciones de nodos:", nodos_pos)
        # Aquí puedes continuar con la parte de aristas o pasar al algoritmo de Dijkstra
        messagebox.showinfo("Aristas", "Ahora haz clic en dos nodos para conectar una arista (se pedirá el peso).")

        seleccion = []  # lista temporal para guardar dos clics
        highlights = []

        def seleccionar_nodo(event):
            # Buscar qué nodo fue clicado (basado en cercanía)
            for nodo_id, (x, y) in nodos_pos.items():
                if (x - event.x)**2 + (y - event.y)**2 <= 20**2:  # radio 20 px
                    seleccion.append(nodo_id)
                    # Resaltar nodo clicado (opcional)
                    highlight = canvas_fondo_dijk.create_oval(x-20, y-20, x+20, y+20, outline="red", width=2)
                    highlights.append(highlight)
                    break

            # Si ya hay dos nodos seleccionados, pedimos peso
            if len(seleccion) == 2:
                n1, n2 = seleccion
                if n1 == n2:
                    messagebox.showerror("Error", "No puedes conectar un nodo consigo mismo.")
                else:
                    peso = simpledialog.askinteger("Peso", f"Ingrese el peso que habrá entre la arista {n1} y {n2}:")
                    if peso is not None:
                        if peso <= 0:  # 🚨 validación extra
                            messagebox.showerror("Error", "El peso debe ser un número positivo mayor que 0.")
                        else:
                            # Dibujar arista
                            x1, y1 = nodos_pos[n1]
                            x2, y2 = nodos_pos[n2]
                            canvas_fondo_dijk.create_line(x1, y1, x2, y2, fill="white", width=2, arrow=tk.LAST, arrowshape=(15, 18, 5))
                            xm, ym = (x1+x2)//2, (y1+y2)//2
                            canvas_fondo_dijk.create_text(xm, ym, text=str(peso), fill="black", font=("Arial", 18, "bold"))
                            G.add_edge(n1, n2, weight=peso)

                # limpiar selección SIEMPRE
                for h in highlights:
                    canvas_fondo_dijk.delete(h)
                highlights.clear()
                seleccion.clear()

                seleccion.clear()  # listo para nueva arista

        # Enlazamos clics al canvas para elegir nodos
        canvas_fondo_dijk.bind("<Button-1>", seleccionar_nodo)

        # Puedes añadir un botón “Finalizar” si quieres terminar esta fase
        boton_finalizar = tk.Button(
            pantalla_fondo_dijk,
            text="Finalizar",
            command=lambda: [terminar_aristas(G), boton_finalizar.destroy()],
            font=("Arial", 25, "bold"),
            bg="#FFA831", fg="white", relief="flat"
        )
        canvas_fondo_dijk.create_window(450, 550, window=boton_finalizar)

    def terminar_aristas(G):
        messagebox.showinfo("Listo", f"Aristas creadas: {list(G.edges(data=True))}.")
        canvas_fondo_dijk.unbind("<Button-1>")

        elegir_nodo(G, nodos_pos, nodos_canvas)

    def colocar_nodo(event):
        if len(nodos_pos) < n:
            nodo_id = len(nodos_pos) + 1
            x, y = event.x, event.y
            nodos_pos[nodo_id] = (x, y)
            # dibujar círculo
            oval_id = canvas_fondo_dijk.create_oval(x-15, y-15, x+15, y+15, fill="#FFA831")
            canvas_fondo_dijk.create_text(x, y, text=str(nodo_id), font=("Arial", 12, "bold"), fill="white")

            nodos_canvas[nodo_id] = oval_id

            # cuando termina de colocar todos los nodos -> mostrar botón continuar
            if len(nodos_pos) == n:
                global boton_continuar
                boton_continuar= tk.Button(
                    pantalla_fondo_dijk,
                    text="Continuar",
                    command=lambda: [continuar_manual(nodos_pos, G), boton_continuar.destroy()],
                    font=("Arial", 20, "bold"),
                    bg="#365785", fg="white",
                    activebackground="#365785",
                    relief="flat", padx=40, pady=5
                )
                canvas_fondo_dijk.create_window(450, 550, window=boton_continuar)
        else:
            # cada click extra muestra mensaje
            messagebox.showinfo("Aviso", "Ya colocaste todos los nodos.")

    messagebox.showinfo("Modo Manual", f"Haz clic en el mapa para colocar {n} nodos.")
    canvas_fondo_dijk.bind("<Button-1>", colocar_nodo)

def elegir_nodo(G, nodos_pos, nodos_canvas):
    messagebox.showinfo("Dijkstra", "Haz clic en el nodo de inicio.")

    seleccion = {"inicio": None, "fin": None}

    def seleccionar(event):
        for nodo_id, (x, y) in nodos_pos.items():
            if (x - event.x)**2 + (y - event.y)**2 <= 20**2:  # radio 20 px
                if seleccion["inicio"] is None:
                    # Provisionalmente pintar de verde
                    canvas_fondo_dijk.itemconfig(nodos_canvas[nodo_id], fill="green")
                    confirmar = messagebox.askyesno("Confirmar inicio", f"¿Quieres elegir el nodo {nodo_id} como inicio?")
                    if confirmar:
                        # --- INICIO DE LA VALIDACIÓN ---
                        if G.out_degree(nodo_id) == 0:
                            messagebox.showerror("Error de inicio", f"El nodo {nodo_id} no tiene aristas de salida.\nNo puede usarse como nodo inicial.")
                            # Revertimos el color y no hacemos nada más
                            canvas_fondo_dijk.itemconfig(nodos_canvas[nodo_id], fill="#FFA831")
                        else:
                            # Si es válido (tiene aristas), continuamos
                            seleccion["inicio"] = nodo_id
                            messagebox.showinfo("Inicio confirmado", f"Nodo {nodo_id} será el inicio.\nAhora selecciona el nodo final.")
                        # --- FIN DE LA VALIDACIÓN ---
                    else:
                        # Revertir color
                        canvas_fondo_dijk.itemconfig(nodos_canvas[nodo_id], fill="#FFA831")

                elif seleccion["fin"] is None and nodo_id != seleccion["inicio"]:
                    # Provisionalmente pintar de rojo
                    canvas_fondo_dijk.itemconfig(nodos_canvas[nodo_id], fill="red")
                    confirmar = messagebox.askyesno("Confirmar final", f"¿Quieres elegir el nodo {nodo_id} como final?")
                    if confirmar:
                        seleccion["fin"] = nodo_id
                        messagebox.showinfo("Final confirmado", f"Nodo {nodo_id} será el final.")
                        # Una vez confirmados ambos, ejecutar Dijkstra
                        ejecutar_dijkstra(G, seleccion["inicio"], seleccion["fin"], nodos_pos, nodos_canvas)
                    else:
                        # Revertir color
                        canvas_fondo_dijk.itemconfig(nodos_canvas[nodo_id], fill="#FFA831")
                break

    canvas_fondo_dijk.bind("<Button-1>", seleccionar)

def juego_aleatorio(n):
    fondo_juego()

    nodos_pos = {}
    nodos_canvas = {}
    G = nx.DiGraph()

    # 1. Crear posiciones aleatorias de los nodos
    min_dist = 70  # distancia mínima entre nodos (ajusta este valor)

    for nodo_id in range(1, n+1):
        while True:
            x = random.randint(50, 850)
            y = random.randint(50, 550)

            # Verificar si está lo suficientemente lejos de los nodos ya puestos
            valido = True
            for (nx_, ny_) in nodos_pos.values():
                if (x - nx_)**2 + (y - ny_)**2 < min_dist**2:
                    valido = False
                    break

            if valido:
                nodos_pos[nodo_id] = (x, y)
                break

        # Dibujar nodo
        oval_id = canvas_fondo_dijk.create_oval(x-15, y-15, x+15, y+15, fill="#FFA831")
        canvas_fondo_dijk.create_text(x, y, text=str(nodo_id), font=("Arial", 12, "bold"), fill="white")
        nodos_canvas[nodo_id] = oval_id

    # 2. Conectar nodos de manera aleatoria
    # Empezamos conectando todos en forma de "árbol" (para asegurar conexidad)
    nodos_ids = list(nodos_pos.keys())
    random.shuffle(nodos_ids)
    for i in range(n-1):
        n1, n2 = nodos_ids[i], nodos_ids[i+1]
        peso = random.randint(1, 10)
        G.add_edge(n1, n2, weight=peso)

        x1, y1 = nodos_pos[n1]
        x2, y2 = nodos_pos[n2]
        canvas_fondo_dijk.create_line(x1, y1, x2, y2, fill="white", width=2, arrow=tk.LAST, arrowshape=(15, 18, 5))
        xm, ym = (x1+x2)//2, (y1+y2)//2
        canvas_fondo_dijk.create_text(xm, ym, text=str(peso), fill="black", font=("Arial", 18, "bold"))

    # 3. Añadir algunas aristas extra para hacerlo más interesante
    extra_edges = random.randint(max(1, n//3), max(2, n//2))
    for _ in range(extra_edges):
        n1, n2 = random.sample(nodos_ids, 2)
        if not G.has_edge(n1, n2):  # evitar duplicados
            peso = random.randint(1, 10)
            G.add_edge(n1, n2, weight=peso)

            x1, y1 = nodos_pos[n1]
            x2, y2 = nodos_pos[n2]
            canvas_fondo_dijk.create_line(x1, y1, x2, y2, fill="white", width=2, arrow=tk.LAST, arrowshape=(15, 18, 5))
            xm, ym = (x1+x2)//2, (y1+y2)//2
            canvas_fondo_dijk.create_text(xm, ym, text=str(peso), fill="black", font=("Arial", 18, "bold"))

    messagebox.showinfo("Modo Aleatorio", f"Grafo generado con {n} nodos.")
    print("Aristas generadas:", list(G.edges(data=True)))

    # Aquí podrías añadir botón para ejecutar Dijkstra
    boton_dijkstra = tk.Button(
        pantalla_fondo_dijk,
        text="Continuar",
        command=lambda: [elegir_nodo(G, nodos_pos, nodos_canvas), boton_dijkstra.destroy()],
        font=("Arial", 20, "bold"),
        bg="#365785", fg="white", relief="flat"
    )
    canvas_fondo_dijk.create_window(450, 550, window=boton_dijkstra)

def ejecutar_dijkstra(G, inicio, fin, nodos_pos, nodos_canvas):
    dist = {nodo: float("inf") for nodo in G.nodes()}
    prev = {nodo: None for nodo in G.nodes()}
    dist[inicio] = 0

    pq = [(0, inicio, 0)]  # (distancia acumulada, nodo, movimiento)
    visitados = set()

    while pq:
        d, u, nivel = heapq.heappop(pq)
        if u in visitados:
            continue
        visitados.add(u)

        # Pintar nodo actual
        if u != fin:
            canvas_fondo_dijk.itemconfig(nodos_canvas[u], fill="green")

        # Etiqueta del nodo actual
        x, y = nodos_pos[u]
        texto = f"[({dist[u]};{prev[u] if prev[u] else '-'})] ({nivel})"
        canvas_fondo_dijk.create_text(x, y+25, text=texto, fill="black", font=("Arial", 10, "bold"))

        if u == fin:
            break

        # Relajación: procesar vecinos
        for v in G.neighbors(u):
            peso = G[u][v]["weight"]
            if dist[u] + peso < dist[v]:
                dist[v] = dist[u] + peso
                prev[v] = u
                heapq.heappush(pq, (dist[v], v, nivel+1))

                # Pintar arista temporal en verde
                x1, y1 = nodos_pos[u]
                x2, y2 = nodos_pos[v]
                canvas_fondo_dijk.create_line(x1, y1, x2, y2, fill="green", width=3, arrow=tk.LAST, arrowshape=(15, 18, 5))

                # Etiqueta provisional del vecino
                xv, yv = nodos_pos[v]
                texto_v = f"[({dist[v]};{u})] ({nivel+1})"
                canvas_fondo_dijk.create_text(xv, yv+25, text=texto_v, fill="black", font=("Arial", 10, "bold"))

                canvas_fondo_dijk.update()
                time.sleep(0.8)

    # Pintar el nodo final amarillo
    canvas_fondo_dijk.itemconfig(nodos_canvas[fin], fill="yellow")

    # Resaltar el camino más corto en azul
    camino = []
    actual = fin
    while actual is not None:
        camino.insert(0, actual)
        actual = prev[actual]

    for i in range(len(camino)-1):
        n1, n2 = camino[i], camino[i+1]
        x1, y1 = nodos_pos[n1]
        x2, y2 = nodos_pos[n2]
        canvas_fondo_dijk.create_line(x1, y1, x2, y2, fill="blue", width=4, arrow=tk.LAST, arrowshape=(16, 20, 6))
        canvas_fondo_dijk.update()
        time.sleep(1)

    messagebox.showinfo("Dijkstra terminado", f"Camino más corto de {inicio} a {fin}: {camino}\nLa distancia mínima desde {inicio} hasta {fin} es {dist[fin]}")

    boton_menu = tk.Button(
        pantalla_fondo_dijk,
        text="Regresar al menú principal",
        command=lambda:[pantalla_fondo_dijk.pack_forget(), pantalla_menu.pack(fill="both", expand=True)],
        font=("Arial", 25, "bold"), bg="#FFA831", fg="white",
        activebackground="#FFA831", relief="flat"
    )
    canvas_fondo_dijk.create_window(450, 550, window=boton_menu)

# --- Botones del menú ---
boton_inicio = tk.Button(pantalla_menu, text="Inicio", command=inicio,
                         font=("Arial", 25, "bold"),
                         bg="#FFA831", fg="white", activebackground="#FFA931",
                         relief="flat", padx=95, pady=0)
boton_inicio.place(x=110, y=496)

boton_instruc = tk.Button(pantalla_menu, text="Instrucciones", command=instruc,
                          font=("Arial", 25, "bold"),
                          bg="#365785", fg="white", activebackground="#365785",
                          relief="flat", padx=25, pady=0)
boton_instruc.place(x=495, y=497)

# Iniciar ventana
ventana.mainloop()