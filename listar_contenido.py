# -*- coding: utf-8 -*-
#Respaldo de la carpeta 'reporting' de Looker Platform usando gzr (Gazer)
#TODO EN UN ÚNICO ARCHIVO pensado para correr en Google Colab:
#las líneas que comienzan con ! son comandos de terminal que Colab
#ejecuta automáticamente (igual que el !pip install de los otros ejemplos)

#=============================================================
#CONFIGURACIÓN: esta es la ÚNICA sección que debes editar
#=============================================================
INSTANCIA      = 'nombre_de_la_instancia.cloud.looker.com'  #sin https://
CLIENT_ID      = 'el_id_de_la_key'
CLIENT_SECRET  = 'secreto'
NOMBRE_CARPETA = 'reporting'  #la carpeta a respaldar, se busca por nombre
ID_CARPETA     = ''           #opcional: si ya conoces el id ponlo aquí y se omite la búsqueda
#=============================================================

#--- 1. instalamos las herramientas: Ruby + gzr, y el SDK de Python ---
#el gem se llama 'gazer' pero el comando que instala es 'gzr'
!apt-get -qq install ruby-full > /dev/null
!gem install gazer
!gzr --version
!pip install -q looker-sdk

#--- 2. credenciales (tomadas de la configuración de arriba) ---
#el SDK de Python las lee de variables de entorno
import os
os.environ['LOOKERSDK_BASE_URL'] = f'https://{INSTANCIA}'
os.environ['LOOKERSDK_CLIENT_ID'] = CLIENT_ID
os.environ['LOOKERSDK_CLIENT_SECRET'] = CLIENT_SECRET

#gzr las lee del archivo ~/.netrc, lo generamos con las mismas variables
with open('/root/.netrc', 'w') as f:
    f.write(f"machine {INSTANCIA}\n  login {CLIENT_ID}\n  password {CLIENT_SECRET}\n")
!chmod 600 /root/.netrc

#--- 3. ubicamos la carpeta por nombre usando el SDK ---
import looker_sdk
sdk = looker_sdk.init40()

if ID_CARPETA == '':
    carpetas = sdk.search_folders(name=NOMBRE_CARPETA, fields='id,name,parent_id')
    #si no hay coincidencia exacta probamos con comodines
    if len(carpetas) == 0:
        carpetas = sdk.search_folders(name=f'%{NOMBRE_CARPETA}%', fields='id,name,parent_id')
    if len(carpetas) == 0:
        raise SystemExit(f"No se encontró ninguna carpeta llamada '{NOMBRE_CARPETA}'")
    for c in carpetas:
        print(f"Encontrada: {c.name} (id {c.id}, carpeta padre {c.parent_id})")
    #usamos la primera coincidencia; si hay varias y no es la correcta,
    #copia el id correcto en ID_CARPETA en la sección de configuración
    ID_CARPETA = str(carpetas[0].id)

print(f"\nSe respaldará la carpeta id {ID_CARPETA} de {INSTANCIA}")

#--- 4. vemos el árbol de la carpeta antes de exportar ---
#nota: en gzr las carpetas se llaman 'space' (el nombre antiguo de folders)
#nota: --port 443 es necesario en instancias .cloud.looker.com
!gzr space tree {ID_CARPETA} --host {INSTANCIA} --port 443

#--- 5. exportamos la carpeta completa ---
#descarga la carpeta, sus subcarpetas y el JSON de cada dashboard y look
!gzr space export {ID_CARPETA} --dir ./respaldo_gzr --host {INSTANCIA} --port 443

#revisamos lo que se descargó y lo comprimimos para bajarlo de Colab
!find ./respaldo_gzr -type f | head -50
!zip -q -r respaldo_gzr.zip respaldo_gzr
print("\nListo: revisa la carpeta ./respaldo_gzr y el archivo respaldo_gzr.zip")

#--- extras útiles (descomenta la línea si la necesitas) ---
#exportar un solo dashboard o look como JSON:
#!gzr dashboard cat 123 --host {INSTANCIA} --port 443
#!gzr look cat 45 --host {INSTANCIA} --port 443

#re-importar el respaldo en otra carpeta u otra instancia:
#!gzr space import ./respaldo_gzr/nombre_carpeta <id_carpeta_destino> --host otra_instancia.cloud.looker.com --port 443

#notas:
#- si 'gem install gazer' falla por la versión de Ruby, instala una más
#  reciente (por ejemplo con rbenv o rvm) y reintenta
#- gzr y el SDK respetan los permisos del usuario de la API key:
#  solo se exporta lo que ese usuario puede ver
