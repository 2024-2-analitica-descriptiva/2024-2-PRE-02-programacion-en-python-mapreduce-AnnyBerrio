"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os
from itertools import groupby


#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo.
#
def load_input(input_directory):
    """Funcion load_input"""
    lines = []
    for filepath in glob.glob(os.path.join(input_directory, "*.txt")):
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                lines.append((os.path.basename(filepath), line.strip()))
    return lines


#
# Escriba la función line_preprocessing que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor).
#
def line_preprocessing(sequence):
    """Line Preprocessing"""
    processed = []
    for filename, line in sequence:
        # Preprocesamos las líneas (por ejemplo, eliminando caracteres especiales y separando palabras)
        words = line.lower().replace('.', '').replace(',', '').split()
        processed.extend((filename, word) for word in words)
    return processed


#
# Escriba una función llamada mapper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor).
#
def mapper(sequence):
    """Mapper"""
    mapped = [(word, 1) for _, word in sequence]
    return mapped


#
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    return sorted(sequence, key=lambda x: x[0])


#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos.
#
def reducer(sequence):
    """Reducer"""
    reduced = []
    for key, group in groupby(sequence, lambda x: x[0]):
        count = sum(value for _, value in group)
        reduced.append((key, count))
    return reduced


#
# Escriba la función create_ouptput_directory que recibe un nombre de
# directorio y lo crea. Si el directorio existe, lo borra.
#
def create_ouptput_directory(output_directory):
    """Create Output Directory"""
    if os.path.exists(output_directory):
        for file in os.scandir(output_directory):
            os.remove(file.path)
    else:
        os.makedirs(output_directory)


#
# Escriba la función save_output, la cual almacena en un archivo de texto
# llamado part-00000 el resultado del reducer.
#
def save_output(output_directory, sequence):
    """Save Output"""
    with open(os.path.join(output_directory, "part-00000"), 'w', encoding='utf-8') as file:
        for key, value in sequence:
            file.write(f"{key}\t{value}\n")


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    """Create Marker"""
    with open(os.path.join(output_directory, "_SUCCESS"), 'w', encoding='utf-8') as file:
        file.write("")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run_job(input_directory, output_directory):
    """Job"""
    # Paso 1: Cargar entradas
    data = load_input(input_directory)
    
    # Paso 2: Preprocesar las líneas
    processed_data = line_preprocessing(data)
    
    # Paso 3: Mapear palabras
    mapped_data = mapper(processed_data)
    
    # Paso 4: Shuffle y ordenamiento
    shuffled_data = shuffle_and_sort(mapped_data)
    
    # Paso 5: Reducir para contar apariciones
    reduced_data = reducer(shuffled_data)
    
    # Paso 6: Crear directorio de salida
    create_ouptput_directory(output_directory)
    
    # Paso 7: Guardar salida
    save_output(output_directory, reduced_data)
    
    # Paso 8: Crear archivo de marcador de éxito
    create_marker(output_directory)


if __name__ == "__main__":
    run_job(
        "input",
        "output",
    )
