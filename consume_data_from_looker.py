# -*- coding: utf-8 -*-
# Author: José Israel Maldonado
# December 2024
# The following code shows how to consume data from a Looker
# from a Looker Platform instance
# a prerequisite for using this example code
# is to generate within Looker Platform in the Admin section
# the API key to be able to connect to the instance
# we start by installing the sdk
!pip install looker_sdk
import looker_sdk
import os
import json
import io
import pprint
import pandas as pd
# The credentials will help us connect to the instance, it is recommended to use an ini file
# since this is just a simple example, we include the credentials in the same code
os.environ['LOOKERSDK_BASE_URL'] = 'https://name_looker_instance.cloud.looker.com'
os.environ['LOOKERSDK_CLIENT_ID'] = 'client_id'
os.environ['LOOKERSDK_CLIENT_SECRET'] = 'secret'
# After initializing the Sdk
sdk = looker_sdk.init40()
# To consume data from a look it is important to use the Look's id and
# specify the format in which we want the data.
result = sdk.run_look(look_id="2", result_format="json")
# Subsequently, we convert the JSON result to a Pandas DataFrame
info = pd.read_json(io.StringIO(result))
# Finally, we show the content
print(info)
