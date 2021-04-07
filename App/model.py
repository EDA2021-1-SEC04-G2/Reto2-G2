"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def new_catalog(tipo,factor):
    catalog = {'videos':None,
               'category_names': None,
               'countries':None,
               'categories':None}

    catalog['videos'] = lt.newList('ARRAY_LIST')
    catalog['category_names'] = mp.newMap(40,
                                          maptype=tipo,
                                          loadfactor=factor)
    catalog['countries']=mp.newMap(20,
                                   maptype=tipo,
                                   loadfactor=factor)
    catalog['categories']=mp.newMap(40,
                                    maptype=tipo,
                                    loadfactor=factor,
                                    comparefunction=compare_categories_by_id)
    return catalog

# Funciones para agregar informacion al catalogo
def add_video(catalog, video):
    lt.addLast(catalog['videos'], video)
    add_video_country(catalog,video['country'],video)
    add_video_category(catalog,video['category_id'],video)

def add_video_category(catalog,category_id,video):
    categories=catalog['categories']
    exist_category = mp.contains(categories,category_id)
    if exist_category:
        entry = mp.get(categories,category_id)
        category = me.getValue(entry)
    else:
        category = new_category(category_id)
        mp.put(categories, category_id, category)
    lt.addLast(category['videos'], video)

def add_video_country(catalog,country_name,video):
    countries=catalog['countries']
    exist_country = mp.contains(countries,country_name)
    if exist_country:
        entry = mp.get(countries,country_name)
        country = me.getValue(entry)
    else:
        country = new_country(country_name)
        mp.put(countries, country_name, country)
    lt.addLast(country['videos'], video)

def add_category_name(catalog, category):
    category=new_category_name(category['name'],category['id'])
    mp.put(catalog['category_names'],category['name'] ,category)

# Funciones para creacion de datos
def new_category(category_id):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'category_id': "", "videos": None}
    entry['category_id'] = category_id
    entry['videos'] = lt.newList('ARRAY_LIST')
    return entry

def new_country(country_name):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'country_name': "", "videos": None}
    entry['country_name'] = country_name
    entry['videos'] = lt.newList('ARRAY_LIST')
    return entry

def new_category_name(name,id):  
    return {'name':name,'id':id}


# Funciones de consulta

def get_category_id(catalog,category_name):
    category_id=0
    category_names=catalog['category_names']
    exist_category=mp.contains(category_names,category_name)
    if exist_category:
        entry=mp.get(category_names,category_name)
        category=me.getValue(entry)
        category_id=category['id']
    return category_id

def get_most_like_videos(catalog,category_name):
    category_id=get_category_id(catalog,category_name)
    if category_id==0:
        return None
    categories=catalog['categories']
    entry=mp.get(categories,category_id)
    category=me.getValue(entry)
    videos=category['videos']
    ans= merge.sort(videos,cmp_videos_by_likes)
    return ans



# Funciones utilizadas para comparar elementos dentro de una lista

def cmp_videos_by_likes(video1,video2):
    return float(video1['likes'])>float(video2['likes'])

def compare_categories_by_id(keyname, category):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    cat_entry = me.getKey(category)
    if (keyname == cat_entry):
        return 0
    elif (keyname > cat_entry):
        return 1
    else:
        return -1

# Funciones de ordenamiento
