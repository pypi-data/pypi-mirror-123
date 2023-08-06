import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response



HEADER_FIELDS = ['Origin', 'X-Mbx-Apikey', 'Accept-Encoding', 'Content-Type', 'Referer']

# TODO: properly configure for custom permissions
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def proxy(request):
    new_headers = {}
    for field in HEADER_FIELDS:
        if field in request.headers:
            new_headers[field] = request.headers[field]
    print(new_headers)
    try:
        full_path = request.get_full_path()
        path = full_path[11:18] + "/" + full_path[18:]
        print(path)
        if (request.method == "GET"):
            proxied_request = requests.get(path, headers=new_headers)
        elif (request.method == "POST"):
            proxied_request = requests.post(path, headers=new_headers)
        print(proxied_request)
        print(proxied_request.content)
        try:
            data = proxied_request.json()
        except:
            data = proxied_request.content
        return Response(status=proxied_request.status_code, data=data)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)