# -*- coding: utf-8 -*-
#SOLO LISTA, NO DESCARGA NADA
#Este código imprime el inventario de lo que existe en la instancia:
#  1. las carpetas llamadas 'reporting' (y si son de sistema o de usuario)
#  2. su árbol completo: subcarpetas, dashboards y looks, con conteos
#  3. los reportes de Studio in Looker y en qué carpeta viven
#sirve para ver qué hay realmente antes de intentar exportar,
#y para entender por qué un export con gzr pudo quedar vacío
#(gzr solo exporta dashboards y looks, no reportes de Studio)

#=============================================================
#CONFIGURACIÓN: esta es la ÚNICA sección que debes editar
#=============================================================
INSTANCIA      = 'nombre_de_la_instancia.cloud.looker.com'  #sin https://
CLIENT_ID      = 'el_id_de_la_key'
CLIENT_SECRET  = 'secreto'
NOMBRE_CARPETA = 'reporting'
#=============================================================

!pip install -q looker-sdk

import os
os.environ['LOOKERSDK_BASE_URL'] = f'https://{INSTANCIA}'
os.environ['LOOKERSDK_CLIENT_ID'] = CLIENT_ID
os.environ['LOOKERSDK_CLIENT_SECRET'] = CLIENT_SECRET

import looker_sdk
sdk = looker_sdk.init40()

#verificamos la conexión y con qué usuario estamos entrando
yo = sdk.me()
print(f"Conectado a {INSTANCIA} como: {yo.display_name} (id {yo.id})")

totales = {'carpetas': 0, 'dashboards': 0, 'looks': 0}


def listar_carpeta(id_carpeta, nivel):
    """imprime recursivamente el contenido de la carpeta con sangría"""
    sangria = '    ' * nivel
    try:
        dashboards = sdk.folder_dashboards(folder_id=str(id_carpeta), fields='id,title')
        looks = sdk.folder_looks(folder_id=str(id_carpeta), fields='id,title')
        hijas = sdk.folder_children(folder_id=str(id_carpeta), fields='id,name')
    except Exception as e:
        print(f"{sangria}[error leyendo la carpeta {id_carpeta}: {e}]")
        return
    totales['dashboards'] += len(dashboards)
    totales['looks'] += len(looks)
    for d in dashboards:
        print(f"{sangria}[dashboard] {d.id} - {d.title}")
    for lk in looks:
        print(f"{sangria}[look] {lk.id} - {lk.title}")
    if len(dashboards) + len(looks) + len(hijas) == 0:
        print(f"{sangria}(vacía)")
    for sub in hijas:
        totales['carpetas'] += 1
        print(f"{sangria}[carpeta] {sub.id} - {sub.name}")
        listar_carpeta(sub.id, nivel + 1)


#--- 1 y 2: carpetas llamadas 'reporting' y su contenido ---
print("\n" + "=" * 60)
print(f"CARPETAS LLAMADAS '{NOMBRE_CARPETA}'")
print("=" * 60)
carpetas = sdk.search_folders(name=NOMBRE_CARPETA, fields='id,name,parent_id,creator_id')
if len(carpetas) == 0:
    carpetas = sdk.search_folders(name=f'%{NOMBRE_CARPETA}%', fields='id,name,parent_id,creator_id')
if len(carpetas) == 0:
    print("No se encontró ninguna carpeta con ese nombre.")
for c in carpetas:
    origen = f"creada por usuario id {c.creator_id}" if c.creator_id else "sin creator_id (posible sistema)"
    print(f"\nCarpeta: {c.name} (id {c.id}, padre {c.parent_id}) - {origen}")
    totales['carpetas'] += 1
    listar_carpeta(c.id, 1)

#--- 3: reportes de Studio in Looker (contenido aparte) ---
print("\n" + "=" * 60)
print("REPORTES DE STUDIO IN LOOKER")
print("=" * 60)
try:
    reportes = sdk.search_reports(limit=500)
    if len(reportes) == 0:
        print("La API no devolvió ningún reporte.")
    for r in reportes:
        carp = getattr(r, 'folder', None)
        donde = f"{getattr(carp, 'name', '?')} (id {getattr(carp, 'id', '?')})" if carp else '?'
        print(f"[reporte] {getattr(r, 'id', '?')} - {getattr(r, 'title', '?')} -> carpeta: {donde}")
except Exception as e:
    print(f"No fue posible consultar los reportes: {e}")

#--- resumen ---
print("\n" + "=" * 60)
print(f"RESUMEN: {totales['carpetas']} carpetas, {totales['dashboards']} dashboards, "
      f"{totales['looks']} looks")
print("=" * 60)
print("Si dashboards y looks están en 0, gzr no tenía nada que exportar:")
print("por eso el zip dijo 'Nothing to do'. Los reportes de Studio no")
print("son exportables ni por gzr ni por la API.")
