"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def print_results(ord_videos, sample=10):
    if ord_videos==None:
        print('Parece que ingresó algún dato mal, vuelva a intentarlo')
    else:
         size = lt.size(ord_videos)
         if size > sample:
            print("Los primeros ", sample, " videos ordenados son:")
            i=1
            while i <= sample:
                video = lt.getElement(ord_videos,i)
                print('Titulo: ',video['title'],'Likes: ',video['likes'], 'Pais: ',video['country'],'Categoria id: ',video['category_id'],'Vistas: ',video['views'])
                i+=1

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Videos Likes categor'ia ")

def init_catalog():
    """
    Inicializa el catalogo de videos
    """
    return controller.init_catalog()


def load_data(catalog):
    """
    Carga los libros en la estructura de datos
    """
    controller.load_data(catalog)

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = init_catalog()
        load_data(catalog)
        print('Se cargaron: ',lt.size(catalog['videos']), ' videos')
    elif int(inputs[0]) == 2:
        category_name=' '+input('Ingrese el nombre de la categoría: ')
        number=int(input('Buscando los TOP ?: '))
        print("Buscando videos con más likes....")
        print_results(controller.get_most_like_videos(catalog,category_name),number)

    else:
        sys.exit(0)
sys.exit(0)
