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
import sys
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf
default_limit=1000
sys.setrecursionlimit(default_limit*1000)

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def new_catalog():
    tipo='PROBING'
    factor=0.5
    catalog = {'videos':None,
               'category_names': None,
               'countries':None,
               'categories':None}

    catalog['videos'] = lt.newList('ARRAY_LIST')
    catalog['category_names'] = lt.newList('ARRAY_LIST')
    catalog['countries']=mp.newMap(20,
                                   maptype=tipo,
                                   loadfactor=factor)
    catalog['categories']=mp.newMap(40,
                                    maptype=tipo,
                                    loadfactor=factor)
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
    lt.addLast(catalog['category_names'], category)

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

# Funciones utilizadas para comparar elementos dentro de una lista

def cmp_videos_by_likes(video1,video2):
    return float(video1['likes'])>float(video2['likes'])

def cmp_videos_by_views(video1,video2):
    return float(video1['views'])>float(video2['views'])

# Funciones de consulta

def get_category_id(catalog,category_name):
    category_id=0
    size=lt.size(catalog['category_names'])
    for i in range(1,size+1):
        category=lt.getElement(catalog['category_names'],i)
        if category_name==category['name']:
            category_id=category['id']
    return category_id

def get_most_view_videos(catalog,country_name,category_name):
    category_id=get_category_id(catalog,category_name)
    videos_country_category=lt.newList('ARRAY_LIST')
    countries=catalog['countries']
    exist_country=mp.contains(countries,country_name)
    if exist_country:
        entry=mp.get(countries,country_name)
        country=me.getValue(entry)
    videos=lt.iterator(country['videos'])
    for video in videos:
          if video['category_id']==category_id:
             lt.addLast(videos_country_category,video)
    return merge.sort(videos_country_category,cmp_videos_by_views)

def get_most_time_trending_country(catalog,country_name):
    countries=catalog['countries']
    exist_country=mp.contains(countries,country_name)
    if exist_country:
        entry=mp.get(countries,country_name)
        country=me.getValue(entry)
    country_videos=country['videos']
    trending_counter=mp.newMap(maptype='Probing', loadfactor=0.5)
    size=lt.size(country_videos)
    for i in range(1,size+1):
        video=lt.getElement(country_videos,i)
        exist_video=mp.contains(trending_counter,video['video_id'])
        if not exist_video:
            video_trending={'video_id':video['video_id'],'title':video['title'],'counter':1,'channel_title':video['channel_title'],'country':country_name}
            mp.put(trending_counter,video['video_id'],video_trending)
        else:
            video_trending=me.getValue(mp.get(trending_counter,video['video_id']))
            video_trending['counter']+=1
    videos=mp.valueSet(trending_counter)
    videos=lt.iterator(videos)
    x=0
    more_trending=None
    for video in videos:
        if video['counter']>x:
            x=video['counter']
            more_trending=video
    return more_trending

def get_most_view_videos(catalog,country_name,category_name):
    category_id=get_category_id(catalog,category_name)
    videos_country_category=lt.newList('ARRAY_LIST')
    countries=catalog['countries']
    exist_country=mp.contains(countries,country_name)
    if exist_country:
        entry=mp.get(countries,country_name)
        country=me.getValue(entry)
    videos=lt.iterator(country['videos'])
    for video in videos:
          if video['category_id']==category_id:
             lt.addLast(videos_country_category,video)
    return merge.sort(videos_country_category,cmp_videos_by_views)

def get_most_time_trending_category(catalog,category_name):
    category_id=get_category_id(catalog,category_name)
    categories=catalog['categories']
    exist_category=mp.contains(categories,category_id)
    if exist_category:
        entry=mp.get(categories,category_id)
        category=me.getValue(entry)
    category_videos=category['videos']
    trending_counter=mp.newMap(maptype='Probing', loadfactor=0.5)
    size=lt.size(category_videos)
    for i in range(1,size+1):
        video=lt.getElement(category_videos,i)
        exist_video=mp.contains(trending_counter,video['video_id'])
        if not exist_video:
            video_trending={'video_id':video['video_id'],'title':video['title'],'counter':1,'channel_title':video['channel_title'],'category_id':category_id}
            mp.put(trending_counter,video['video_id'],video_trending)
        else:
            video_trending=me.getValue(mp.get(trending_counter,video['video_id']))
            video_trending['counter']+=1
    videos=mp.valueSet(trending_counter)
    videos=lt.iterator(videos)
    x=0
    more_trending=None
    for video in videos:
        if video['counter']>x:
            x=video['counter']
            more_trending=video
    return more_trending

def get_most_likes_tag(catalog,tag,country_name):
    countries=catalog['countries']
    entry=mp.get(countries,country_name)
    country=me.getValue(entry)
    country_videos=country['videos']
    videos=lt.iterator(country_videos)
    tag_country_videos=lt.newList('ARRAY_LIST')
    for video in videos:
        video_tags=video['tags']
        if tag in video_tags:
            lt.addLast(tag_country_videos,video)
    return merge.sort(tag_country_videos,cmp_videos_by_likes)





