# -*- coding: utf-8 -*-
# Autor: José Israel Maldonado
# Diciembre de 2024

#para una instancia de Looker Platform
#un prerrequisito para usar este código ejemplo
#es generar dentro de Looker Platform en el apartado Admin
#la API key para poder conectarse a la instancia
#iniciamos instalando el sdk
!pip install looker-sdk
import looker_sdk
import os
import pprint
#las credenciales nos ayudarán a conectarnos a la instancia, se recomienda usar un ini file
#ya que este solo es un ejemplo sencillo, incluimos las credenciales en el mismo código
os.environ['LOOKERSDK_BASE_URL'] = 'https://nombre_de_la_instancia.cloud.looker.com'
os.environ['LOOKERSDK_CLIENT_ID'] = 'el_id_de_la_key'
os.environ['LOOKERSDK_CLIENT_SECRET'] = 'secreto'
#Primero inicializamos el SDK
sdk = looker_sdk.init40()

# Define los datos del nuevo usuario
nombre_usuario = "usuario_creado_mediante_api"  # Nombre de usuario
nombre = "Nuevo"  # Nombre
apellido = "Usuario"  # Apellido
email = "nuevo.usuario@example.com"  # Correo electrónico
rol_id = 3  # ID del rol que deseas asignar (ej. 3 para "Viewer")
# Crea el usuario en Looker
try:
    credentials_email = {'email': email}

    usuario = sdk.create_user(
        body=looker_sdk.models40.WriteUser(
            first_name=nombre,
            last_name=apellido,
            # role_ids=[rol_id], # if you need to set roles during creation you can uncomment this
            credentials_email=credentials_email, # Pass the dictionary here
        )
    )

    # Imprime la información del usuario creado
    print(f"Usuario creado con éxito: {usuario}")

except looker_sdk.error.SDKError as e:
    print(f"Error al crear el usuario: {e}")
