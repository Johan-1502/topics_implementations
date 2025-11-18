import ttkbootstrap as tb
from PIL import Image, ImageTk
import math
from default_values import quadratic_title, rosenbrock_title, rastrigin_title, constriction_factor, inertia_factor
from function import QuadraticFunction, RosenbrockFunction, RastriginFunction
from pso import PSO, Particle
import numpy as np

def show_parameters(event):
    selection = function_box.get()
    if selection == quadratic_title:
        quadratic_frame.pack()
        rosenbrock_frame.pack_forget()
        rastrigin_frame.pack_forget()
        return
    if selection == rosenbrock_title:
        rosenbrock_frame.pack()
        quadratic_frame.pack_forget()
        rastrigin_frame.pack_forget()
        return
    if selection == rastrigin_title:
        rastrigin_frame.pack()
        rosenbrock_frame.pack_forget()
        quadratic_frame.pack_forget()
        return

app = tb.Window(themename="superhero")
app.title("Simulación algoritmo PSO")

w, h = 600, 800
sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
x, y = (sw - w) // 2, (sh - h) // 2

app.geometry(f"{w}x{h}+{x}+{y}")

principal_frame = tb.Frame(app)
principal_frame.pack()

tb.Label(principal_frame, text="Simulador PSO", bootstyle="primary", font=("Arial", 14, "bold"), foreground="white").pack(pady=(20,5))

frame_superior = tb.Frame(principal_frame)
frame_superior.pack(pady=20)

frame_funciones = tb.Frame(principal_frame)
frame_funciones.pack()

frame_inferior = tb.Frame(principal_frame)
frame_inferior.pack(pady=20)

factor_label = tb.Label(frame_superior, text="Factor a implementar:", font=("Arial", 12), foreground="white")
factor_label.grid(row=0, column=0, padx=10, pady=10)

factor_box = tb.Combobox(frame_superior, values=[constriction_factor, inertia_factor], state="readonly")
factor_box.grid(row=0, column=1, padx=10, pady=10)
factor_box.set(constriction_factor)

quantity_particles_label = tb.Label(frame_superior, text="Cantidad de partículas:", font=("Arial", 12), foreground="white")
quantity_particles_label.grid(row=1, column=0, pady=10)

quantity_particles_entry = tb.Entry(frame_superior)
quantity_particles_entry.grid(row=1, column=1, pady=10)

quantity_iterations_label = tb.Label(frame_superior, text="Cantidad de iteraciones:", font=("Arial", 12), foreground="white")
quantity_iterations_label.grid(row=2, column=0, pady=10)

quantity_iterations_entry = tb.Entry(frame_superior)
quantity_iterations_entry.grid(row=2, column=1, pady=10)

label = tb.Label(frame_superior, text="Función a utilizar:", font=("Arial", 12), foreground="white")
label.grid(row=3, column=0, padx=10)

function_box = tb.Combobox(frame_superior, values=[quadratic_title, rosenbrock_title, rastrigin_title], state="readonly")
function_box.grid(row=3, column=1, padx=10)
function_box.bind("<<ComboboxSelected>>", show_parameters)
function_box.set(quadratic_title)

# FUNCIONES 
# Función cuadrática
quadratic_frame = tb.Frame(frame_funciones)
quadratic_frame.pack()

quad_img = Image.open("images/Quadratic.png")
quad_img = quad_img.resize((math.trunc(quad_img.size[0]*0.5), math.trunc(quad_img.size[1]*0.5)))
quad_photo = ImageTk.PhotoImage(quad_img)

quad_title_label = tb.Label(quadratic_frame, text="Función Cuadrática", font=("Arial", 13, "bold"))
quad_title_label.grid(row=0, column=0, columnspan=2, pady=15)

image_label = tb.Label(quadratic_frame, image=quad_photo)
image_label.grid(row=1, column=0, columnspan=2)

quad_param_label = tb.Label(quadratic_frame, text="Coeficientes", font=("Arial", 12, "bold"))
quad_param_label.grid(row=2, column=0, columnspan=2)

quad_a_label = tb.Label(quadratic_frame, text="a:", font=("Arial", 12), foreground="white")
quad_a_label.grid(row=3, column=0, pady=10)

quad_entry_a = tb.Entry(quadratic_frame)
quad_entry_a.grid(row=3, column=1, pady=10)

quad_b_label = tb.Label(quadratic_frame, text="b:", font=("Arial", 12), foreground="white")
quad_b_label.grid(row=4, column=0, pady=10)

quad_entry_b = tb.Entry(quadratic_frame)
quad_entry_b.grid(row=4, column=1, pady=10)

quad_c_label = tb.Label(quadratic_frame, text="c:", font=("Arial", 12), foreground="white")
quad_c_label.grid(row=5, column=0, pady=10)

quad_entry_c = tb.Entry(quadratic_frame)
quad_entry_c.grid(row=5, column=1, pady=10)

quad_d_label = tb.Label(quadratic_frame, text="d:", font=("Arial", 12), foreground="white")
quad_d_label.grid(row=6, column=0, pady=10)

quad_entry_d = tb.Entry(quadratic_frame)
quad_entry_d.grid(row=6, column=1, pady=10)


# Función rosenbrock
rosenbrock_frame = tb.Frame(frame_funciones)
#rosenbrock_frame.pack(pady=20)

rosenb_img = Image.open("images/Rosenbrock.png")
rosenb_img = rosenb_img.resize((math.trunc(rosenb_img.size[0]*0.5), math.trunc(rosenb_img.size[1]*0.5)))
rosenb_photo = ImageTk.PhotoImage(rosenb_img)

rosenb_title_label = tb.Label(rosenbrock_frame, text="Función Rosenbrock", font=("Arial", 13, "bold"))
rosenb_title_label.grid(row=0, column=0, columnspan=2)

image_label = tb.Label(rosenbrock_frame, image=rosenb_photo)
image_label.grid(row=1, column=0, columnspan=2)

rosenb_param_label = tb.Label(rosenbrock_frame, text="Parámetros")
rosenb_param_label.grid(row=2, column=0, columnspan=2)

rosenb_a_label = tb.Label(rosenbrock_frame, text="a:", font=("Arial", 12), foreground="white")
rosenb_a_label.grid(row=3, column=0, pady=10)

rosenb_entry_a = tb.Entry(rosenbrock_frame)
rosenb_entry_a.grid(row=3, column=1, pady=10)

rosenb_b_label = tb.Label(rosenbrock_frame, text="b:", font=("Arial", 12), foreground="white")
rosenb_b_label.grid(row=4, column=0, pady=10)

rosenb_entry_b = tb.Entry(rosenbrock_frame)
rosenb_entry_b.grid(row=4, column=1, pady=10)


# Función rastrigin
rastrigin_frame = tb.Frame(frame_funciones)
#rastrigin_frame.pack(pady=20)

ras_img = Image.open("images/Rastrigin.png")
ras_img = ras_img.resize((math.trunc(ras_img.size[0]*0.5), math.trunc(ras_img.size[1]*0.5)))
ras_photo = ImageTk.PhotoImage(ras_img)

ras_title_label = tb.Label(rastrigin_frame, text="Función Rastrigin", font=("Arial", 13, "bold"))
ras_title_label.grid(row=0, column=0, columnspan=2)

image_label = tb.Label(rastrigin_frame, image=ras_photo)
image_label.grid(row=1, column=0, columnspan=2)

ras_param_label = tb.Label(rastrigin_frame, text="Parámetros")
ras_param_label.grid(row=2, column=0, columnspan=2)

ras_A_label = tb.Label(rastrigin_frame, text="A:", font=("Arial", 12), foreground="white")
ras_A_label.grid(row=3, column=0, pady=10)

ras_entry_A = tb.Entry(rastrigin_frame)
ras_entry_A.grid(row=3, column=1, pady=10)

ras_n_label = tb.Label(rastrigin_frame, text="n:", font=("Arial", 12), foreground="white")
ras_n_label.grid(row=4, column=0, pady=10)

ras_entry_n = tb.Entry(rastrigin_frame)
ras_entry_n.grid(row=4, column=1, pady=10)


def calculate():
    selection = function_box.get()
    if selection == quadratic_title:
        function = QuadraticFunction(float(quad_entry_a.get()),float(quad_entry_b.get()),float(quad_entry_c.get()),float(quad_entry_d.get()))
        simulator = PSO()
        simulator.calculate_function(int(quantity_particles_entry.get()), int(quantity_iterations_entry.get()), function, factor_box.get()==constriction_factor)
        show_results(simulator)
        return
    if selection == rosenbrock_title:
        function = RosenbrockFunction(float(rosenb_entry_a.get()),float(rosenb_entry_b.get()))
        simulator = PSO()
        simulator.calculate_function(int(quantity_particles_entry.get()), int(quantity_iterations_entry.get()), function, factor_box.get()==constriction_factor)
        show_results(simulator)
        return
    if selection == rastrigin_title:
        function = RastriginFunction(float(ras_entry_A.get()), int(ras_entry_n.get()))
        simulator = PSO()
        simulator.calculate_function(int(quantity_particles_entry.get()), int(quantity_iterations_entry.get()), function, factor_box.get()==constriction_factor)
        show_results(simulator)
        return

calculate_button = tb.Button(frame_inferior, text="Calcular", command=calculate)
calculate_button.grid(row=2, column=0, pady=10, columnspan=2)

results_frame = tb.Frame(app)

def obtain_name_particles(simulator:PSO)->list[str]:
    particles_names:list[str] = []
    for particle in simulator.particles:
        particles_names.append(f"Partícula {particle.id}")
    return particles_names

def show_particle_iterations(table, particle:Particle):
    iteration_id = 1
    for iteration in particle.iterations:
        table.insert("", "end", values=(iteration_id, np.array2string(iteration.position, precision=3),
        np.array2string(iteration.velocity, precision=3),
        np.array2string(iteration.pbest, precision=3)))
        iteration_id += 1
        
def obtain_particle_id(particles_combobox:tb.Combobox):
    particle_name = particles_combobox.get()
    particle_id = particle_name.replace("Partícula", "")
    print(f"Partícula id: {particle_id}")
    return int(particle_id)

def update_table(table, simulator:PSO, particles_combobox):
    for row in table.get_children():
        table.delete(row)

    pid = obtain_particle_id(particles_combobox)

    show_particle_iterations(table, simulator.particles[pid])

def show_results(simulator: PSO):
    principal_frame.pack_forget()
    results_frame.pack()

    w, h = 1500, 900
    sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
    x, y = (sw - w) // 2, (sh - h) // 2
    app.geometry(f"{w}x{h}+{x}+{y}")

    title_frame = tb.Frame(results_frame)
    title_frame.grid(row=0, column=0, columnspan=2, pady=10)

    title_text = tb.Label(title_frame, text="Resultados", font=("Arial", 16, "bold"))
    title_text.grid(row=0, column=0, columnspan=2)

    best_result = ""
    if simulator.gbest is not None:
        best_result:str = np.array2string(simulator.gbest)
    result_text = tb.Label(title_frame, text=f"La mejor configuración de parámetros fue:", font=("Arial", 14))
    result_text.grid(row=1, column=0, pady= 20)
    result_text = tb.Label(title_frame, text=f"{best_result}", font=("Arial", 14, "bold"))
    result_text.grid(row=1, column=1, pady= 20)

    left_frame = tb.Frame(results_frame)
    left_frame.grid(row=1, column=0, padx=20, pady=20, sticky="n")

    it_part_title = tb.Label(left_frame, text="Iteraciones por partícula", font=("Arial", 16, "bold"))
    it_part_title.grid(row=0, column=0, pady=10, columnspan=2)

    particles_label = tb.Label(left_frame, text="Partícula: ", font=("Arial", 13))
    
    particles_label.grid(row=1, column=0, padx =10, pady = 10)

    particles_combobox = tb.Combobox(left_frame, values=obtain_name_particles(simulator), state="readonly")
    particles_combobox.grid(row=1, column=1, pady=10)
    particles_combobox.set("Partícula 0")

    table_frame = tb.Frame(left_frame, width=650, height=800)
    
    columns = ("col1", "col2", "col3", "col4")

    table = tb.Treeview(table_frame, columns=columns, show="headings", height=20)

    # Definir encabezados
    table.heading("col1", text="#Iter.")
    table.heading("col2", text="Posición")
    table.heading("col3", text="Velocidad")
    table.heading("col4", text="Pbest")

    # Definir ancho de columnas
    table.column("col1", width=50, minwidth=50, stretch=False)
    table.column("col2", width=200, minwidth=200, stretch=False)
    table.column("col3", width=200, minwidth=200, stretch=False)
    table.column("col4", width=200, minwidth=200, stretch=False)

    # Insertar filas
    show_particle_iterations(table, simulator.particles[obtain_particle_id(particles_combobox)])
    
    # Scroll vertical
    scroll_y = tb.Scrollbar(table_frame, orient="vertical", command=table.yview)
    scroll_y.grid(row=0, column=1, sticky="ns")

    # Scroll horizontal
    scroll_x = tb.Scrollbar(table_frame, orient="horizontal", command=table.xview)
    scroll_x.grid(row=1, column=0, sticky="we")

    # Conectar scrollbars
    table.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    # Ubicar la tabla
    table.grid(row=0, column=0, sticky="nsew")

    # Expandir tamaño del frame para que la tabla crezca
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)
    
    particles_combobox.bind("<<ComboboxSelected>>", lambda event: update_table(table, simulator, particles_combobox))
    table_frame.grid(row=2, column=0, pady=10, columnspan=2)
    
    right_frame = tb.Frame(results_frame)
    right_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    right_title_text = tb.Label(right_frame, text="Iteraciones completas", font=("Arial", 14, "bold"))
    right_title_text.grid(row=0, column=0, pady=20)

    iterations_table_frame = tb.Frame(right_frame)
    iterations_table_frame.grid(row=1, column=0, pady=20)
    #iterations_table_frame = tb.Frame(right_frame, width=350)
    #iterations_table_frame.grid(row=1, column=0, pady=10)
    #iterations_table_frame.grid_propagate(False) 

    iterations_columns = ("col1", "col2")

    iterations_table = tb.Treeview(iterations_table_frame, columns=iterations_columns, show="headings", height=20)

    particles_combobox.bind("<<ComboboxSelected>>", lambda event: update_table(table, simulator, particles_combobox))
    
    # Definir encabezados
    iterations_table.heading("col1", text="Gbest")
    iterations_table.heading("col2", text="Diversidad")

    # Definir ancho de columnas
    iterations_table.column("col1", width=300, minwidth=200, stretch=True)
    iterations_table.column("col2", width=100, minwidth=100, stretch=True)

    # Insertar filas
    for iteration in simulator.iterations:
        iterations_table.insert("", "end", values=(iteration.gbest, iteration.diversity))
    
    # Scroll vertical
    iterations_scroll_y = tb.Scrollbar(iterations_table_frame, orient="vertical", command=iterations_table.yview)
    iterations_scroll_y.grid(row=0, column=1, sticky="ns")

    # Scroll horizontal
    iterations_scroll_x = tb.Scrollbar(iterations_table_frame, orient="horizontal", command=iterations_table.xview)
    iterations_scroll_x.grid(row=1, column=0, sticky="we")

    # Conectar scrollbars
    iterations_table.configure(yscrollcommand=iterations_scroll_y.set, xscrollcommand=iterations_scroll_x.set)

    # Ubicar la tabla

    # Expandir tamaño del frame para que la tabla crezca
    iterations_table_frame.grid_rowconfigure(0, weight=1)
    iterations_table_frame.grid_columnconfigure(0, weight=1)
    
    iterations_table.grid(row=0, column=0, sticky="nsew")
    

    
app.mainloop()