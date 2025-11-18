import sys
import os
import time

# permitir imports relativos al proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.aco import AntColony
from src.tsp import load_latlon_csv, haversine_distance_matrix
import matplotlib.pyplot as plt


def plot_real_solution(names, coords, route, title=None, save_path=None):
    # coords: lista de (lat, lon) -- para plot simple usamos lon = x, lat = y
    route_coords = [coords[i] for i in route]
    xs = [c[1] for c in route_coords] + [route_coords[0][1]]
    ys = [c[0] for c in route_coords] + [route_coords[0][0]]
    plt.figure(figsize=(8, 6))
    plt.plot(xs, ys, '-o')
    for idx, (lat, lon) in enumerate(route_coords):
        plt.text(lon, lat, names[route[idx]], fontsize=9)
    if title:
        plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        print('Figura guardada en', save_path)
    else:
        plt.show()


def main():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'spain_cities.csv'))
    names, coords = load_latlon_csv(data_path)
    dist_matrix = haversine_distance_matrix(coords)

    print('Ejecutando ACO sobre instancia real (ciudades españolas).')
    aco = AntColony(dist_matrix, n_ants=30, n_best=5, n_iterations=300, decay=0.4, alpha=1, beta=2, q=1.0)
    best_route, best_dist = aco.run(verbose=True)

    print('\nMejor distancia (km):', best_dist)
    print('Ruta (indices):', best_route)
    print('\nRuta (nombres):')
    for idx in best_route:
        print('-', names[idx])

    outputs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs'))
    os.makedirs(outputs_dir, exist_ok=True)
    ts = time.strftime('%Y%m%d-%H%M%S')
    route_path = os.path.join(outputs_dir, f'real_route_{ts}.png')
    plot_real_solution(names, coords, best_route, title=f'Ruta ACO ({best_dist:.1f} km)', save_path=route_path)


if __name__ == '__main__':
    main()
