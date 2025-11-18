import numpy as np
import math

def coords_to_distance_matrix(coords):
    coords = np.array(coords)
    n = len(coords)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i, j] = 0.0
            else:
                dx = coords[i, 0] - coords[j, 0]
                dy = coords[i, 1] - coords[j, 1]
                dist[i, j] = math.hypot(dx, dy)
    return dist

def haversine_distance_matrix(latlon_coords):
    """Calcula matriz de distancias en km usando la fórmula Haversine.

    `latlon_coords` debe ser iterable de pares (lat, lon) en grados.
    """
    coords = np.array(latlon_coords, dtype=float)
    n = len(coords)
    R = 6371.0  # radio de la Tierra en km
    dist = np.zeros((n, n))
    lat = np.radians(coords[:, 0])
    lon = np.radians(coords[:, 1])
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i, j] = 0.0
            else:
                dlat = lat[j] - lat[i]
                dlon = lon[j] - lon[i]
                a = math.sin(dlat/2)**2 + math.cos(lat[i]) * math.cos(lat[j]) * math.sin(dlon/2)**2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                dist[i, j] = R * c
    return dist

def random_coords(n, seed=None, scale=100):
    rng = np.random.RandomState(seed)
    return rng.rand(n, 2) * scale

def route_to_coords(route, coords):
    return [coords[i] for i in route]

def route_distance(route, dist_matrix):
    d = 0.0
    for i in range(len(route)):
        d += dist_matrix[route[i], route[(i+1)%len(route)]]
    return d

def format_route(route):
    return ' -> '.join(str(r) for r in route)

def load_latlon_csv(path):
    """Carga un CSV simple con columnas: name,lat,lon (con o sin cabecera).

    Devuelve: (names, coords_array)
    - names: lista de nombres
    - coords_array: lista de (lat, lon)
    """
    import csv
    names = []
    coords = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        # intentar detectar header
        first = next(reader)
        try:
            float(first[1])
            # no header
            row = first
            names.append(row[0])
            coords.append((float(row[1]), float(row[2])))
        except Exception:
            # header, continuar
            pass
        for row in reader:
            if not row:
                continue
            names.append(row[0])
            coords.append((float(row[1]), float(row[2])))
    return names, coords
