# -*- coding: utf-8 -*-
# Autor: José Israel Maldonado
# Diciembre de 2024
#El siguiente código muestra como consumir datos desde una Looker
#desde una instancia de Looker Platform
#un prerrequisito para usar este código ejemplo 
#es generar dentro de Looker Platform en el apartado Admin
#la API key para poder conectarse a la instancia
#iniciamos instalando el sdk
!pip install looker_sdk
import looker_sdk
import os
import json
import io
import pprint
import pandas as pd
#las credenciales nos ayudarán a conectarnos a la instancia, se recomienda usar un ini file
#ya que este solo es un ejemplo sencillo, incluimos las credenciales en el mismo código
os.environ['LOOKERSDK_BASE_URL'] = 'https://nombre_de_la_instancia.cloud.looker.com'
os.environ['LOOKERSDK_CLIENT_ID'] = 'el_id_de_la_key'
os.environ['LOOKERSDK_CLIENT_SECRET'] = 'secreto'
#Después inicializar el Sdk
sdk = looker_sdk.init40()
# Para consumir data de una look es importante utilizar el id de la Look y 
# especificar el formato en que deseamos la data.
result = sdk.run_look(look_id="2", result_format="json")
# Posteriormente convertimos el resultado JSON a un DataFrame de Pandas
info = pd.read_json(io.StringIO(result))
# Finalmente mostramos el contenido
print(info)
