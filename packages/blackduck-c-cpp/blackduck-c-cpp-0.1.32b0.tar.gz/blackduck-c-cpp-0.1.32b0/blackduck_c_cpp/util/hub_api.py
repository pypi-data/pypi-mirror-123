"""
Copyright (c) 2021 Synopsys, Inc.
Use subject to the terms and conditions of the Synopsys End User Software License and Maintenance Agreement.
All rights reserved worldwide.
"""

from blackduck.HubRestApi import HubInstance
import logging
import sys
from requests.exceptions import ConnectionError


class HubAPI:

    def __init__(self, bd_url, api_token, insecure):
        self.bd_url = bd_url
        self.api_token = api_token
        self.insecure = insecure
        self.hub = None

    def authenticate(self):
        try:
            self.hub = HubInstance(self.bd_url, api_token=self.api_token, insecure=self.insecure,
                                   write_config_flag=False)
        except KeyError:
            logging.error("make sure you have right api key and --insecure flag is set correctly")
            sys.exit(1)
        except ConnectionError:
            logging.error("ConnectionError occurred. Make sure you have correct url and insecure flag is set properly")
            sys.exit(1)

    def create_or_verify_project_version_exists(self, project_name, version_name):
        self.authenticate()
        project = self.hub.get_project_by_name(project_name)
        if project:
            version = self.hub.get_version_by_name(project, version_name)
            if version:
                return
            if not version:
                response = self.hub.create_project_version(project, version_name)
        else:
            response = self.hub.create_project(project_name, version_name)

        if not response.ok:
            logging.error("Error creating project version -- (Response({}): {})".format(response.status_code, response.text))
            sys.exit(1)
