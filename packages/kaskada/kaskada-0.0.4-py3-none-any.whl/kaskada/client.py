"""
Copyright (C) 2021 Kaskada Inc. All rights reserved.

This package cannot be used, copied or distributed without the express 
written permission of Kaskada Inc.

For licensing inquiries, please contact us at info@kaskada.com.
"""

from datetime import datetime, timedelta
from typing import Tuple, List

import grpc
import http.client
import json
import certifi

import kaskada.api.v1alpha.compute_pb2_grpc as compute_grpc
import kaskada.api.v1alpha.table_pb2_grpc as table_grpc
import kaskada.api.v1alpha.staged_file_pb2_grpc as staging_grpc
import kaskada.api.v1alpha.view_pb2_grpc as view_grpc

class Client(object):
    LEGACY_ENGINE = 'LEGACY'

    def getBearerToken(endpoint: str, audience: str, client_id: str, client_secret: str):
        """
        Requests a bearer token given the provided parameters

        Args:
            endpoint (str): the authentication endpoint to request a token from
            audience (str): the audience the token is requesting
            client_id (str): the user provided client id
            client_secret (str): the user provided client secret

        Returns:
            AccessToken: Kaskada Access Token
        """
        conn = http.client.HTTPSConnection(endpoint)
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'audience': audience, 
            'grant_type': 'client_credentials',
        }
        headers = {
            'content-type': 'application/json',
        }
        conn.request('POST', '/oauth/token', json.dumps(payload), headers)
        res = conn.getresponse()
        data = res.read().decode('utf-8')
        return Client.AccessToken(data, endpoint, audience, client_id, client_secret)

    class AccessToken(object):
        def __init__(self, json_data: str, endpoint: str, audience: str, client_id: str, client_secret: str):
            """
            AccessToken constructor

            Args:
                json_data (str): UTF-8 response from the oauth token request
                endpoint (str): the authentication endpoint to request a token from
                audience (str): the audience the token is requesting
                client_id (str): the user provided client id
                client_secret (str): the user provided client secret

            Raises:
                PermissionError: Unable to validate access token.
            """
            self.init_time = datetime.now()
            data = json.loads(json_data)
            if 'access_token' not in data and 'expires_in' not in data and 'token_type' not in data:
                raise PermissionError('Unable to validate access token. Token details: {}'.format(json_data))
            self.access_token = data['access_token']
            # The token is valid from now + expires_in seconds. Set the renewal time to one hour before the expires time for safety.
            self.expires_at = self.init_time + timedelta(0, data['expires_in'] - 3600)
            self.token_type = data['token_type']
            self.endpoint = endpoint
            self.audience = audience
            self.client_id = client_id
            self.client_secret = client_secret

    def authorized(**kwags):
        """
        Creates an authorized client

        Returns:
            Client: Authorized access client
        """
        credentials_exchange_endpoint = kwags.pop('exchange_endpoint', 'prod-kaskada.us.auth0.com')
        credentials_audience = kwags.pop('audience', 'https://api.prod.kaskada.com')
        client_id = kwags.pop('client_id')
        client_secret = kwags.pop('client_secret')
        token = Client.getBearerToken(credentials_exchange_endpoint, credentials_audience, client_id, client_secret)
        return Client(client_id, token, **kwags)

    def demo_only(**kwags):
        """
        Creates a demo only client

        Returns:
            Client: Demo only client
        """
        client_id = kwags.pop('client_id', 'lWYFx0020u4oulh7Z9UB8C5YXVRHNyk4')
        return Client(client_id, None, **kwags)

    def __init__(self, client_id: str, token: AccessToken, **kwags):
        """
        Creates a client

        Args:
            client_id (str): Client ID to send requests as
            token ([Client.AccessToken]): Access token
        """
        engine = kwags.pop('engine', None)
        endpoint = kwags.pop('endpoint', 'api.kaskada.com:50051')
        is_secure = kwags.pop('is_secure', True)
        if is_secure:
            with open(certifi.where(), 'rb') as f:
                trusted_certs = f.read()
            credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
            channel = grpc.secure_channel(endpoint, credentials)
        else:
            channel = grpc.insecure_channel(endpoint)
        self.computeStub = compute_grpc.ComputeServiceStub(channel)
        self.tableStub = table_grpc.TableServiceStub(channel)
        self.viewStub = view_grpc.ViewServiceStub(channel)
        self.stagingStub = staging_grpc.StagedFileServiceStub(channel)
        self.client_id = client_id
        self.token = token
        if engine is not None:
            self.metadata.append(('x-engine', engine))

    def get_metadata(self) -> List[Tuple[str, str]]:
        """
        Fetches the metadata for the current client. Renews token if necessary.

        Raises:
            Exception: invalid token

        Returns:
            List[Tuple[str, str]]: Client metadata
        """
        if self.token is None:
            return [('client-id', self.client_id)]
        else:
            if self.token.expires_at is None:
                raise Exception("invalid token. please re-initialize the Kaskada client for continued use")

            current_time = datetime.now()
            remaining_token_time = (self.token.expires_at - current_time).total_seconds()
            # A token is expired if the difference between the expired time and current time is non-positive
            if (remaining_token_time <= 0):
                # Refresh the token by requesting a new one
                self.token = Client.getBearerToken(self.token.endpoint, self.token.audience, self.token.client_id, self.token.client_secret)
            return [('authorization', self.token.access_token)]
