# -*- coding: utf-8 -*-
#El siguiente código busca la carpeta llamada 'reporting'
#en una instancia de Looker Platform y lista su contenido
#(subcarpetas, dashboards y looks)
#un prerrequisito para usar este código ejemplo
#es generar dentro de Looker Platform en el apartado Admin
#la API key para poder conectarse a la instancia

#iniciamos instalando el sdk
!pip install looker-sdk

import looker_sdk
import os

#las credenciales nos ayudarán a conectarnos a la instancia, se recomienda usar un ini file
#ya que este solo es un ejemplo sencillo, incluimos las credenciales en el mismo código
os.environ['LOOKERSDK_BASE_URL'] = 'https://nombre_de_la_instancia.cloud.looker.com'
os.environ['LOOKERSDK_CLIENT_ID'] = 'el_id_de_la_key'
os.environ['LOOKERSDK_CLIENT_SECRET'] = 'secreto'

#Primero inicializamos el SDK
sdk = looker_sdk.init40()

#buscamos la carpeta por su nombre
#equivale a la llamada GET /api/4.0/folders/search?name=reporting
carpetas = sdk.search_folders(name='reporting', fields='id,name,parent_id')

#si no hay coincidencia exacta, probamos con comodines (%)
#por si el nombre real es por ejemplo 'Reporting Ventas'
if len(carpetas) == 0:
    carpetas = sdk.search_folders(name='%reporting%', fields='id,name,parent_id')

if len(carpetas) == 0:
    print("No se encontró ninguna carpeta llamada 'reporting'")
    print("Revisa el nombre o los permisos del usuario de la API key")

#puede existir más de una carpeta con el mismo nombre
#(por ejemplo en espacios personales de distintos usuarios)
#por eso recorremos todas las coincidencias
for carpeta in carpetas:
    print("=" * 60)
    print(f"Carpeta: {carpeta.name} (id {carpeta.id}, carpeta padre {carpeta.parent_id})")

    #listamos las subcarpetas
    #equivale a la llamada GET /api/4.0/folders/{folder_id}/children
    subcarpetas = sdk.folder_children(folder_id=carpeta.id, fields='id,name')
    print("\nSubcarpetas:")
    for sub in subcarpetas:
        print(f"  {sub.id} - {sub.name}")

    #listamos los dashboards que contiene la carpeta
    #equivale a la llamada GET /api/4.0/folders/{folder_id}/dashboards
    dashboards = sdk.folder_dashboards(folder_id=carpeta.id, fields='id,title')
    print("\nDashboards:")
    for d in dashboards:
        print(f"  {d.id} - {d.title}")

    #listamos los looks que contiene la carpeta
    #equivale a la llamada GET /api/4.0/folders/{folder_id}/looks
    looks = sdk.folder_looks(folder_id=carpeta.id, fields='id,title')
    print("\nLooks:")
    for lk in looks:
        print(f"  {lk.id} - {lk.title}")

#nota: el usuario asociado a la API key solo verá las carpetas
#a las que tiene acceso según sus permisos en Looker
