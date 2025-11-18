import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# permitir imports relativos
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.aco import AntColony
from src.tsp import random_coords, coords_to_distance_matrix, load_latlon_csv, haversine_distance_matrix


class ACOGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ACO Interactive - GUI')
        self.geometry('1100x700')
        self.create_widgets()
        self.aco = None
        self.coords = None
        self.names = None
        self._run_thread = None
        # image handles for pheromone heatmap (so we can update in-place)
        self.pher_im = None
        self.pher_colorbar = None

    def create_widgets(self):
        control_frame = ttk.Frame(self)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        # Instance controls
        ttk.Label(control_frame, text='Instancia').pack(anchor=tk.W)
        self.instance_var = tk.StringVar(value='Aleatoria')
        ttk.OptionMenu(control_frame, self.instance_var, 'Aleatoria', 'Aleatoria', 'Ciudades España').pack(fill=tk.X)
        ttk.Label(control_frame, text='Número de ciudades').pack(anchor=tk.W, pady=(8,0))
        self.num_cities = tk.IntVar(value=12)
        ttk.Entry(control_frame, textvariable=self.num_cities).pack(fill=tk.X)
        ttk.Label(control_frame, text='Seed').pack(anchor=tk.W, pady=(8,0))
        self.seed_var = tk.IntVar(value=42)
        ttk.Entry(control_frame, textvariable=self.seed_var).pack(fill=tk.X)

        # ACO parameters
        ttk.Separator(control_frame).pack(fill=tk.X, pady=6)
        ttk.Label(control_frame, text='Parámetros ACO').pack(anchor=tk.W)
        self.n_ants = tk.IntVar(value=20)
        ttk.Label(control_frame, text='n_ants').pack(anchor=tk.W)
        ttk.Entry(control_frame, textvariable=self.n_ants).pack(fill=tk.X)
        self.n_best = tk.IntVar(value=5)
        ttk.Label(control_frame, text='n_best').pack(anchor=tk.W)
        ttk.Entry(control_frame, textvariable=self.n_best).pack(fill=tk.X)
        self.n_iterations = tk.IntVar(value=200)
        ttk.Label(control_frame, text='n_iterations').pack(anchor=tk.W)
        ttk.Entry(control_frame, textvariable=self.n_iterations).pack(fill=tk.X)
        self.decay = tk.DoubleVar(value=0.3)
        ttk.Label(control_frame, text='decay (rho)').pack(anchor=tk.W)
        ttk.Entry(control_frame, textvariable=self.decay).pack(fill=tk.X)
        self.alpha = tk.DoubleVar(value=1.0)
        ttk.Label(control_frame, text='alpha').pack(anchor=tk.W)
        ttk.Entry(control_frame, textvariable=self.alpha).pack(fill=tk.X)
        self.beta = tk.DoubleVar(value=2.0)
        ttk.Label(control_frame, text='beta').pack(anchor=tk.W)
        ttk.Entry(control_frame, textvariable=self.beta).pack(fill=tk.X)
        self.q = tk.DoubleVar(value=1.0)
        ttk.Label(control_frame, text='Q').pack(anchor=tk.W)
        ttk.Entry(control_frame, textvariable=self.q).pack(fill=tk.X)

        ttk.Separator(control_frame).pack(fill=tk.X, pady=6)
        # Buttons
        ttk.Button(control_frame, text='Inicializar', command=self.initialize).pack(fill=tk.X, pady=4)
        ttk.Button(control_frame, text='Step', command=self.step_ui).pack(fill=tk.X, pady=4)
        ttk.Button(control_frame, text='Run', command=self.run_ui).pack(fill=tk.X, pady=4)
        self.pause_btn = ttk.Button(control_frame, text='Pausa', command=self.toggle_pause)
        self.pause_btn.pack(fill=tk.X, pady=4)
        ttk.Button(control_frame, text='Reset', command=self.reset_ui).pack(fill=tk.X, pady=4)
        ttk.Button(control_frame, text='Guardar figuras', command=self.save_figures).pack(fill=tk.X, pady=4)

        # speed control and progress
        ttk.Label(control_frame, text='Delay (ms) entre pasos').pack(anchor=tk.W, pady=(8,0))
        self.delay_ms = tk.IntVar(value=10)
        ttk.Scale(control_frame, from_=0, to=1000, variable=self.delay_ms, orient=tk.HORIZONTAL).pack(fill=tk.X)
        ttk.Label(control_frame, text='Progreso').pack(anchor=tk.W, pady=(8,0))
        self.progress = ttk.Progressbar(control_frame, orient='horizontal', mode='determinate')
        self.progress.pack(fill=tk.X)

        ttk.Separator(control_frame).pack(fill=tk.X, pady=6)
        self.status = tk.StringVar(value='No inicializado')
        ttk.Label(control_frame, textvariable=self.status, foreground='blue').pack(anchor=tk.W, pady=(6,0))

        # Plot area
        plot_frame = ttk.Frame(self)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # right side: top route, bottom pheromone + log
        right_top = ttk.Frame(plot_frame)
        right_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        right_bottom = ttk.Frame(plot_frame)
        right_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.fig_route, self.ax_route = plt.subplots(figsize=(6,4))
        self.canvas_route = FigureCanvasTkAgg(self.fig_route, master=right_top)
        self.canvas_route.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.fig_pher, self.ax_pher = plt.subplots(figsize=(4,4))
        self.canvas_pher = FigureCanvasTkAgg(self.fig_pher, master=right_bottom)
        self.canvas_pher.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # log of best distances
        log_frame = ttk.Frame(right_bottom)
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        ttk.Label(log_frame, text='Log (best por iteración)').pack()
        self.log_listbox = tk.Listbox(log_frame, height=12, width=30)
        self.log_listbox.pack(fill=tk.BOTH, expand=True)

    def initialize(self):
        try:
            if self.instance_var.get() == 'Aleatoria':
                coords = random_coords(self.num_cities.get(), seed=self.seed_var.get(), scale=100)
                names = [str(i) for i in range(len(coords))]
                dist = coords_to_distance_matrix(coords)
            else:
                path = os.path.join(os.path.dirname(__file__), 'data', 'spain_cities.csv')
                names, latlon = load_latlon_csv(path)
                coords = np.array(latlon)
                dist = haversine_distance_matrix(coords)
            self.coords = coords
            self.names = names
            self.aco = AntColony(distances=dist, n_ants=int(self.n_ants.get()), n_best=int(self.n_best.get()), n_iterations=int(self.n_iterations.get()), decay=float(self.decay.get()), alpha=float(self.alpha.get()), beta=float(self.beta.get()), q=float(self.q.get()))
            self.aco.reset()
            self.status.set('Inicializado')
            self.update_plots()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def step_ui(self):
        if not self.aco:
            messagebox.showwarning('Atención', 'Inicializa la instancia primero')
            return
        self.aco.step()
        self.status.set(f'Iter {self.aco.iteration}  Best {self.aco.best_distance:.4f}')
        self.update_plots()

    def _run_thread_target(self):
        # run in separate thread
        self._pause_flag = False
        while self.aco.iteration < self.aco.n_iterations and not getattr(self, '_stop_run', False):
            # handle pause
            while getattr(self, '_paused', False):
                time.sleep(0.1)
                if getattr(self, '_stop_run', False):
                    break
            if getattr(self, '_stop_run', False):
                break
            self.aco.step()
            # update progress and log
            self.after(0, lambda: self._update_progress_and_log())
            # periodic plot refresh
            if self.aco.iteration % max(1, self.aco.n_iterations // 20) == 0:
                self.after(0, self.update_plots)
            # delay
            delay = self.delay_ms.get() / 1000.0
            if delay > 0:
                time.sleep(delay)
        self.after(0, lambda: self.status.set(f'Finished. Iter {self.aco.iteration} Best {self.aco.best_distance:.4f}'))
        self._stop_run = False

    def run_ui(self):
        if not self.aco:
            messagebox.showwarning('Atención', 'Inicializa la instancia primero')
            return
        if self._run_thread and self._run_thread.is_alive():
            messagebox.showinfo('Info', 'Ya se está ejecutando')
            return
        self._paused = False
        self._stop_run = False
        self._run_thread = threading.Thread(target=self._run_thread_target, daemon=True)
        self._run_thread.start()

    def toggle_pause(self):
        if not self._run_thread or not self._run_thread.is_alive():
            return
        self._paused = not getattr(self, '_paused', False)
        self.pause_btn.config(text='Resume' if self._paused else 'Pausa')

    def reset_ui(self):
        if not self.aco:
            return
        self.aco.reset()
        self.status.set('Reset')
        self.update_plots()
        self.log_listbox.delete(0, tk.END)
        self.progress['value'] = 0
        # clear pheromone image and colorbar if present
        if self.pher_im is not None:
            try:
                self.pher_im.remove()
            except Exception:
                pass
            self.pher_im = None
        if self.pher_colorbar is not None:
            try:
                self.pher_colorbar.remove()
            except Exception:
                pass
            self.pher_colorbar = None
        # clear route canvas
        self.ax_route.clear()
        self.canvas_route.draw()

    def _update_progress_and_log(self):
        # update progressbar and add log entry for current best
        if not self.aco:
            return
        it = self.aco.iteration
        total = self.aco.n_iterations
        self.progress['maximum'] = total
        self.progress['value'] = it
        # insert log (keep last 200 entries)
        bd = self.aco.best_distance if self.aco.best_distance != float('inf') else None
        entry = f'Iter {it}: {bd:.4f}' if bd is not None else f'Iter {it}: -'
        self.log_listbox.insert(tk.END, entry)
        if self.log_listbox.size() > 200:
            self.log_listbox.delete(0)

    def update_plots(self):
        # pheromone heatmap: update image data instead of recreating colorbar
        if self.aco:
            pher = self.aco.get_pheromone_matrix()
            if self.pher_im is None:
                self.ax_pher.clear()
                self.pher_im = self.ax_pher.imshow(pher, cmap='viridis', vmin=pher.min(), vmax=pher.max())
                # remove old colorbar if exists
                if self.pher_colorbar is not None:
                    try:
                        self.pher_colorbar.remove()
                    except Exception:
                        pass
                self.pher_colorbar = self.fig_pher.colorbar(self.pher_im, ax=self.ax_pher)
                self.ax_pher.set_title('Pheromone matrix')
            else:
                # update existing image
                self.pher_im.set_data(pher)
                self.pher_im.set_clim(vmin=pher.min(), vmax=pher.max())
                if self.pher_colorbar is not None:
                    try:
                        self.pher_colorbar.update_normal(self.pher_im)
                    except Exception:
                        pass
        else:
            self.ax_pher.clear()
            self.ax_pher.set_title('Pheromone matrix (no data)')
        self.canvas_pher.draw()

        # route plot (with annotations and arrows)
        self.ax_route.clear()
        if self.aco and self.aco.best_route is not None and self.coords is not None:
            route = self.aco.best_route
            rc = [self.coords[i] for i in route]
            xs = [c[0] for c in rc] + [rc[0][0]]
            ys = [c[1] for c in rc] + [rc[0][1]]
            self.ax_route.plot(xs, ys, '-o', color='tab:blue')
            # annotate nodes with names or indices
            for idx, (x, y) in enumerate(rc):
                label = self.names[route[idx]] if self.names and len(self.names) > route[idx] else str(route[idx])
                self.ax_route.annotate(label, (x, y), textcoords='offset points', xytext=(3,3), fontsize=8)
            # draw small arrows between points to show direction
            for i in range(len(rc)):
                x0, y0 = rc[i]
                x1, y1 = rc[(i+1) % len(rc)]
                self.ax_route.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle='->', color='gray', lw=0.7))
            self.ax_route.set_title(f'Route (best {self.aco.best_distance:.2f})')
        else:
            self.ax_route.set_title('Route (no data)')
        self.canvas_route.draw()

    def save_figures(self):
        if not self.aco:
            messagebox.showwarning('Atención', 'Inicializa la instancia primero')
            return
        outdir = filedialog.askdirectory(title='Selecciona carpeta para guardar figuras')
        if not outdir:
            return
        t = time.strftime('%Y%m%d-%H%M%S')
        route_path = os.path.join(outdir, f'route_{t}.png')
        pher_path = os.path.join(outdir, f'pheromone_{t}.png')
        self.fig_route.savefig(route_path)
        self.fig_pher.savefig(pher_path)
        messagebox.showinfo('Guardado', f'Guardado: {route_path}\n{pher_path}')


if __name__ == '__main__':
    app = ACOGui()
    app.mainloop()
