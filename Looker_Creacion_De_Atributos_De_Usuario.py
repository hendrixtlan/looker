# -*- coding: utf-8 -*-
# Autor: José Israel Maldonado
# Diciembre de 2024
#El siguiente código muestra como generar un atributo de usuario
#para una instancia de Looker Platform
#un prerrequisito para usar este código ejemplo
#es generar dentro de Looker Platform en el apartado Admin
#la API key para poder conectarse a la instancia
#iniciamos instalando el sdk
!pip install looker-sdk
import looker_sdk
import os
import json
import pprint
#las credenciales nos ayudarán a conectarnos a la instancia, se recomienda usar un ini file
#ya que este solo es un ejemplo sencillo, incluimos las credenciales en el mismo código
os.environ['LOOKERSDK_BASE_URL'] = 'https://nombre_de_la_instancia.cloud.looker.com'
os.environ['LOOKERSDK_CLIENT_ID'] = 'el_id_de_la_key'
os.environ['LOOKERSDK_CLIENT_SECRET'] = 'secreto'

#Primero inicializamos el SDK
sdk = looker_sdk.init40()

# el resultado de la creación del atributo será posible comprobarse en la consola de Looker en Admin - User Attributes
respuesta = sdk.create_user_attribute(
    body=looker_sdk.models40.WriteUserAttribute(
        name="mi_atributo",
        label="Mi Atributo",
        type="string",
        default_value="",
        value_is_hidden=False,
        user_can_view=True,
        user_can_edit=True
    )
)

print (respuesta)
