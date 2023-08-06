import os

import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response



# TODO: properly configure for custom permissions
@api_view(['GET'])
def proxy(request):
    try:
        full_path = request.get_full_path()
        path = full_path[11:18] + "/" + full_path[18:]
        print(path)
        proxied_request = requests.get(path)
        try:
            data = proxied_request.json()
        except:
            data = proxied_request.content
        return Response(status=proxied_request.status_code, data=data)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)