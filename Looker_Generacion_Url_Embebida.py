# -*- coding: utf-8 -*-
# Autor: José Israel Maldonado
# Julio de 2024
#El siguiente código muestra como generar una url embebida
#para una instancia de Looker
#un prerrequisito es generar dentro de Looker en el apartado Admin
#la API key para poder conectarse a la instancia
#iniciamos instalando el sdk
!pip install looker_sdk
import looker_sdk
import os
import json
import pprint
#las credenciales nos ayudarán a conectarnos a la instancia
os.environ['LOOKERSDK_BASE_URL'] = 'https://nombre_de_la_instancia.cloud.looker.com'
os.environ['LOOKERSDK_CLIENT_ID'] = 'el_id_de_la_key'
os.environ['LOOKERSDK_CLIENT_SECRET'] = 'secreto'

#Primero inicializamos el SDK
sdk = looker_sdk.init40()

#ajustar las siguientes líneas dependiendo si lo que queremos usar son Looks o Dashboards
#url= 'https://siucom.cloud.looker.com/embed/dashboards/'
url= 'https://siucom.cloud.looker.com/looks/'

numero_de_dashboard_o_look='9'

#podemos agregar los parámetros por ejemplo algún theme que hayamos creado o bien los filtros
parametros='?theme=Looker&filtro1=valor1&filtro2=valor2'
url=url+numero_de_dashboard_o_look+parametros

# hacemos la llamada para generar la url
# estableceremos la longitud de la sesión, el id del usuario
# así como los permisos 
# ojo que en la sección final es muy importante especificar el modelo
respuesta = sdk.create_sso_embed_url(
{
    "target_url": url,
    "session_length": 30000,
    "external_user_id": '2',
    "permissions": [
        "access_data",
        "see_looks",
        "see_user_dashboards",
        "see_lookml_dashboards",
        "download_with_limit",
        "schedule_look_emails",
        "schedule_external_look_emails",
        "create_alerts",
        "see_drill_overlay",
        "save_content",
        "embed_browse_spaces",
        "schedule_look_emails",
        "send_to_sftp",
        "send_to_s3",
        "send_outgoing_webhook",
        "send_to_integration",
        "download_without_limit",
        "explore",
        "see_sql"
    ],
    "models": ['nombre-modelo']
  })
print (respuesta)
