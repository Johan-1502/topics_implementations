import sys
import os
import argparse
import time
import matplotlib.pyplot as plt

# Ensure project root is on sys.path so `src` can be imported when running the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.aco import AntColony
from src.tsp import random_coords, coords_to_distance_matrix, route_to_coords


def plot_solution(coords, route_coords, title=None, annotate=True, save_path=None):
    xs = [c[0] for c in route_coords] + [route_coords[0][0]]
    ys = [c[1] for c in route_coords] + [route_coords[0][1]]
    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, '-o')
    if annotate:
        for idx, (x, y) in enumerate(route_coords):
            plt.text(x, y, str(idx), fontsize=9, color='red')
    if title:
        plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        print('Figura guardada en', save_path)
    else:
        plt.show()


def plot_pheromone(pheromone, save_path=None):
    plt.figure(figsize=(6, 5))
    plt.imshow(pheromone, cmap='viridis')
    plt.colorbar(label='Pheromone')
    plt.title('Matriz de feromona')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        print('Matriz de feromona guardada en', save_path)
    else:
        plt.show()


def print_formulas():
    print('Fórmulas usadas en ACO:')
    print(' P_ij = (tau_ij^alpha * (1/d_ij)^beta) / sum_k (tau_ik^alpha * (1/d_ik)^beta)')
    print(' tau_ij <- (1-rho)*tau_ij + sum_k (Q / L_k)  (si la hormiga k usó el arco i->j)')


def main():
    parser = argparse.ArgumentParser(description='Ejemplo ACO para TSP (intuitivo y visual)')
    parser.add_argument('--n', type=int, default=12, help='Número de ciudades')
    parser.add_argument('--seed', type=int, default=42, help='Seed aleatorio')
    parser.add_argument('--save', action='store_true', help='Guardar figuras en outputs/')
    parser.add_argument('--no-show', action='store_true', help='No mostrar ventanas interactivas')
    args = parser.parse_args()

    # generar instancia de ejemplo
    coords = random_coords(args.n, seed=args.seed, scale=100)
    dist_matrix = coords_to_distance_matrix(coords)

    # imprimir fórmulas para que el usuario las vea
    print_formulas()

    aco = AntColony(dist_matrix, n_ants=20, n_best=5, n_iterations=200, decay=0.3, alpha=1, beta=3)
    best_route, best_dist = aco.run(verbose=True)

    print('\nMejor distancia encontrada:', best_dist)
    print('Ruta (indices):', best_route)

    route_coords = route_to_coords(best_route, coords)

    # outputs
    timestamp = time.strftime('%Y%m%d-%H%M%S')
    outputs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs'))
    if args.save:
        os.makedirs(outputs_dir, exist_ok=True)
        route_path = os.path.join(outputs_dir, f'route_{timestamp}.png')
        pher_path = os.path.join(outputs_dir, f'pheromone_{timestamp}.png')
        plot_solution(coords, route_coords, title=f"ACO - distancia {best_dist:.2f}", save_path=route_path)
        plot_pheromone(aco.get_pheromone_matrix(), save_path=pher_path)
        if not args.no_show:
            plot_solution(coords, route_coords, title=f"ACO - distancia {best_dist:.2f}")
            plot_pheromone(aco.get_pheromone_matrix())
    else:
        if not args.no_show:
            plot_solution(coords, route_coords, title=f"ACO - distancia {best_dist:.2f}")
            plot_pheromone(aco.get_pheromone_matrix())


if __name__ == '__main__':
    main()
