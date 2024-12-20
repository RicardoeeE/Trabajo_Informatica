import os
import numpy as np
from stl import mesh
import vtkplotlib as vpl
from copy import deepcopy

def load_stl(file_name):
    """Carga un archivo STL desde la carpeta Figuras."""
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "Figuras", file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
    return mesh.Mesh.from_file(file_path)

def create_translation_matrix(tx, ty, tz):
    """Crea una matriz de traslación."""
    matrix = np.identity(4)
    matrix[0:3, 3] = [tx, ty, tz]
    return matrix

def create_rotation_matrix(axis, angle):
    """Crea una matriz de rotación en el eje especificado."""
    matrix = np.identity(4)
    c, s = np.cos(angle), np.sin(angle)
    if axis == 'x':
        matrix[1:3, 1:3] = [[c, -s], [s, c]]
    elif axis == 'y':
        matrix[0:3:2, 0:3:2] = [[c, s], [-s, c]]
    elif axis == 'z':
        matrix[0:2, 0:2] = [[c, -s], [s, c]]
    return matrix

def apply_transformation(mesh_obj, transformation):
    """Aplica una transformación a un objeto STL."""
    mesh_obj.transform(transformation)

def draw_axes():
    """Dibuja los ejes X, Y y Z."""
    vpl.plot(np.array([[0, 0, 0], [5, 0, 0]]), color=(1, 0, 0), line_width=3.0, label="X")
    vpl.plot(np.array([[0, 0, 0], [0, 5, 0]]), color=(0, 1, 0), line_width=3.0, label="Y")
    vpl.plot(np.array([[0, 0, 0], [0, 0, 5]]), color=(0, 0, 1), line_width=3.0, label="Z")

if __name__ == "__main__":
    # Cargar las piezas
    piezas = {
        "camion": load_stl("dump_track.stl"),
        "empujador": load_stl("empujador.stl"),
        "deslizadera": load_stl("rampa.stl"),
        "brazo1": load_stl("brazo1.stl"),
        "brazo2": load_stl("brazo2.stl"),
        "contenedor": load_stl("contenedor.stl"),
        "tapa": load_stl("tapa.stl"),
    }

    # Posiciones relativas según la tabla
    posiciones = {
        "camion": create_translation_matrix(0.0, 0.0, 0.0),
        "empujador": create_translation_matrix(-0.075283, 0.73129, -0.19924),
        "deslizadera": create_translation_matrix(-0.2416, 2.2309, 0.19993),
        "brazo1": create_translation_matrix(0.0, -0.8463, 0.07907),
        "brazo2": create_translation_matrix(0.0, -0.81879, 0.0),
        "contenedor": create_translation_matrix(-0.17888, 0.83539, 0.98371086),
        "tapa": create_translation_matrix(-0.03811, 0.0, 0.0),
    }

    # Composición de transformaciones
    transformaciones = {
        "camion": posiciones["camion"],
        "empujador": posiciones["camion"] @ posiciones["empujador"],
        "deslizadera": posiciones["camion"] @ posiciones["deslizadera"],
        "brazo1": posiciones["camion"] @ posiciones["deslizadera"] @ posiciones["brazo1"],
        "brazo2": posiciones["camion"] @ posiciones["deslizadera"] @ posiciones["brazo1"] @ posiciones["brazo2"],
        "contenedor": posiciones["contenedor"],
        "tapa": posiciones["contenedor"] @ posiciones["tapa"],
    }

    # Visualizar las piezas ensambladas
    vpl.QtFigure()
    draw_axes()
    colores = {
        "camion": (0.5, 0.5, 0.5),
        "empujador": (1, 0, 0),
        "deslizadera": (0, 1, 0),
        "brazo1": (0, 0, 1),
        "brazo2": (1, 1, 0),
        "contenedor": (1, 0, 1),
        "tapa": (0, 1, 1),
    }

    for nombre, malla in piezas.items():
        malla_copiada = deepcopy(malla)
        malla_copiada.transform(transformaciones[nombre])
        vpl.mesh_plot(malla_copiada, color=colores[nombre])

    vpl.view(camera_position=(10.0, 6.0, 10.0), focal_point=(0.0, 0.0, 0.0))
    vpl.show()
