"""
Copyright (C) 2021 Kaskada Inc. All rights reserved.

This package cannot be used, copied or distributed without the express 
written permission of Kaskada Inc.

For licensing inquiries, please contact us at info@kaskada.com.
"""

from kaskada.client import Client
import kaskada
import kaskada.api.v1alpha.compute_pb2 as compute

import grpc

def query(**kwargs):
    """
    Performs a query
    """
    try:
        client = kwargs.pop('client', kaskada.KASKADA_DEFAULT_CLIENT)
        kaskada.validate_client(client)
        response_as = kwargs.pop('response_as', None)
        if response_as == 'json_values':
            kwargs['json_values'] = {}
        elif response_as == 'redis_bulk':
            kwargs['redis_bulk'] = {}
        else:
            kwargs['parquet'] = {}
        query_request = compute.QueryRequest(**kwargs)
        return client.computeStub.Query(query_request, metadata=client.get_metadata())
    except grpc.RpcError as e:
        kaskada.handleGrpcError(e)
    except Exception as e:
        kaskada.handleException(e)
