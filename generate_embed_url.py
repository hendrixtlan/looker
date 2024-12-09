# -*- coding: utf-8 -*-
# Author: José Israel Maldonado
# July 2024
# The following code shows how to generate an embedded URL
# for a Looker Platform instance.
# A prerequisite to use this example code 
# is to generate an API key within the Looker Platform in the Admin section
# to be able to connect to the instance.
# We start by installing the SDK.
# October 16, 2024: Try installing a previous version to avoid the error when importing looker_sdk.
!pip install looker-sdk==23.2.0
import looker_sdk
import os
import json
import pprint
# The credentials will help us connect to the instance. It is recommended to use an ini file.
# Since this is just a simple example, we include the credentials in the code itself.
os.environ['LOOKERSDK_BASE_URL'] = 'https://instance_name.cloud.looker.com'
os.environ['LOOKERSDK_CLIENT_ID'] = 'key_id'
os.environ['LOOKERSDK_CLIENT_SECRET'] = 'secret'
# First, we initialize the SDK.
sdk = looker_sdk.init40()
# Adjust the following lines depending on whether you want to use Looks or Dashboards.
# When you want to create a URL to embed a dashboard, it is necessary to add /embed/dashboards/ to the base URL. 
# url = 'https://instance_name.cloud.looker.com/embed/dashboards/'
# When you are looking to generate a URL to embed a Look, you only need to add /looks/ to the base URL.
url= 'https://instance_name.cloud.looker.com/looks/'
# The ID of the dashboard or look
dashboard_or_look_id = '9'

# We can add parameters, for example, a theme that we have created or filters.
# The default theme is 'Looker'.
parameters = '?theme=Looker&filter1=value1&filter2=value2'
url = url + dashboard_or_look_id + parameters

# We make the call to generate the URL.
# We will set the session length, the user ID,
# and the permissions.
# Since this is a temporary embed, we will set a time for the session.
# Note that it is very important to specify the model in the final section.
response = sdk.create_sso_embed_url(
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
    "models": ['model-name']  # Replace with the actual model name
})
print(response)
